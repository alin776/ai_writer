17:02:03 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 1d322be6-3ff1-405b-a589-f963a9f89866, Mode: planning, Message: 这个讲了什么内容？...
17:02:03 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
17:02:03 app.api.v1.agent INFO     - selected_text: N/A...
17:02:03 app.api.v1.agent INFO     - selection_position: N/A
17:02:03 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 573fa16e-017f-45ed-8c7b-d7651ccbf712...
17:02:03 app.api.v1.agent INFO     - instruction_context: N/A...
17:02:03 app.services.knowledge_service INFO   引用次数增加: item_id=d53763ab-a4ad-4fb1-a27e-1124600ba946, count=2
17:02:03 app.api.v1.agent INFO   [agent_chat_stream] Injected 1 knowledge docs into context
17:02:03 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 1d322be6-3ff1-405b-a589-f963a9f89866:ede5109c-aedb-4f49-b664-c5904624ac06:35a109bf-14c2-4bf7-bbff-7e03baf26a5d (user_id=1d322be6-3ff1-405b-a589-f963a9f89866, work_id=ede5109c-aedb-4f49-b664-c5904624ac06, conversation_id=35a109bf-14c2-4bf7-bbff-7e03baf26a5d)
17:02:03 app.services.context.store INFO   [ContextStore] 加载上下文: 1d322be6-3ff1-405b-a589-f963a9f89866:ede5109c-aedb-4f49-b664-c5904624ac06:35a109bf-14c2-4bf7-bbff-7e03baf26a5d, 2条消息
17:02:03 app.services.context.manager INFO   [ContextManager] Session 1d322be6-3ff1-405b-a589-f963a9f89866:ede5109c-aedb-4f49-b664-c5904624ac06:35a109bf-14c2-4bf7-bbff-7e03baf26a5d: 13/16000 tokens
17:02:04 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='这个讲了什么内容？...' | 隔离键=['user:1d322be6-3ff1-405b-a589-f963a9f89866:work:ede5109c-aedb-4f49-b664-c5904624ac06', 'user:1d322be6-3ff1-405b-a589-f963a9f89866'] | 找到=0条
17:02:04 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=ede5109c-aedb-4f49-b664-c5904624ac06 | 含用户级=True | 找到=0条
17:02:04 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 13 tokens, 耗时 495.46ms
17:02:04 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 2 条历史消息 (token: 13)
17:02:04 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 这个讲了什么内容？...
17:02:04 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
17:02:04 app.services.agent.langgraph_agent INFO   [Planning] 注入 1 个知识库文档到prompt
17:02:04 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:02:04 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:02:04 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
17:02:06 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:02:09 app.services.ai.http_ai_service INFO   API 响应完成，共接收 14 个数据块，总长度: 1313
17:02:09 app.services.ai.http_ai_service INFO   流式响应Token统计: 7705 (prompt=6803, completion=902)
17:02:09 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:02:09 app.services.ai.http_ai_service INFO   [积分扣除] 用户 1d322be6-3ff1-405b-a589-f963a9f89866: 扣除 217.29 积分, 余额: 49632.71 → 49415.42
17:02:09 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7705, cost=$0.017524, time=5145ms
17:02:09 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7705
17:02:09 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
17:02:09 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一个概括性的回答，总结所提供文档的内容。, 原料=用户提供的知识库文档内容。, 处理=使用 analyze_text_tool
17:02:09 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 5.62s
17:02:09 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
17:02:09 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:02:09 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
17:02:09 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
17:02:09 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
17:02:09 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
17:02:09 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
17:02:09 app.api.v1.agent INFO   [Stream] Task started: 概括文档内容
17:02:09 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '概括这一段文字的主要内容，包括故事背景、主角能力和开篇情节。...'
17:02:09 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
17:02:09 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
17:02:09 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
17:02:09 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:02:09 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:02:09 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
17:02:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:02:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 4 个数据块，总长度: 301
17:02:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 2352 (prompt=2114, completion=238)
17:02:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:02:20 app.services.ai.http_ai_service INFO   [积分扣除] 用户 1d322be6-3ff1-405b-a589-f963a9f89866: 扣除 62.28 积分, 余额: 49415.42 → 49353.14
17:02:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2352, cost=$0.005023, time=11057ms
17:02:20 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
17:02:20 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 301
17:02:21 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 11.250s)
17:02:21 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
17:02:21 app.api.v1.agent INFO   [Stream] 任务完成: 概括文档内容 (11.3s)
17:02:21 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
17:02:21 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
17:02:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:02:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:02:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:02:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:02:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:02:24 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
17:02:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 449 (prompt=448, completion=1)
17:02:24 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:02:24 app.services.ai.http_ai_service INFO   [积分扣除] 用户 1d322be6-3ff1-405b-a589-f963a9f89866: 扣除 7.07 积分, 余额: 49353.14 → 49346.07
17:02:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=449, cost=$0.000570, time=3440ms
17:02:24 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=449
17:02:24 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
17:02:24 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:02:24 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:02:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
17:02:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:02:27 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 111
17:02:27 app.services.ai.http_ai_service INFO   流式响应Token统计: 1700 (prompt=1647, completion=53)
17:02:27 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:02:27 app.services.ai.http_ai_service INFO   [积分扣除] 用户 1d322be6-3ff1-405b-a589-f963a9f89866: 扣除 32.1 积分, 余额: 49346.07 → 49313.97
17:02:27 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1700, cost=$0.002589, time=3337ms
17:02:27 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1700
17:02:27 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
17:02:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:02:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:02:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:02:29 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:02:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:02:31 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
17:02:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 482 (prompt=481, completion=1)
17:02:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:02:31 app.services.ai.http_ai_service INFO   [积分扣除] 用户 1d322be6-3ff1-405b-a589-f963a9f89866: 扣除 7.58 积分, 余额: 49313.97 → 49306.39
17:02:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=482, cost=$0.000611, time=3760ms
17:02:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=482
17:02:31 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
17:02:31 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
17:02:31 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 22.05s
17:02:31 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:02:31 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
17:02:31 app.services.agent.langgraph_agent INFO   [Response] 检测到知识库文档(1个)，使用AI整合（确保流式输出）
17:02:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
17:02:31 app.services.agent.langgraph_agent INFO   [Summarization] 注入 1 个知识库文档到总结prompt
17:02:31 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=326字符, 压缩后=337字符, 压缩率=-3%
17:02:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
17:02:31 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
17:02:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:02:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:02:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
17:02:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:02:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 324
17:02:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 1991 (prompt=1748, completion=243)
17:02:35 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:02:35 app.services.ai.http_ai_service INFO   [积分扣除] 用户 1d322be6-3ff1-405b-a589-f963a9f89866: 扣除 57.23 积分, 余额: 49306.39 → 49249.16
17:02:35 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1991, cost=$0.004615, time=3285ms
17:02:35 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=324
17:02:41 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=1d322be6-3ff1-405b-a... | 隔离=work:ede5109c-aedb-4f49-b664-c5904624ac06 | 重要度=0.88
17:02:41 app.services.context.store INFO   [ContextStore] 保存上下文: 1d322be6-3ff1-405b-a589-f963a9f89866:ede5109c-aedb-4f49-b664-c5904624ac06:35a109bf-14c2-4bf7-bbff-7e03baf26a5d, token=218
17:02:41 app.services.context.manager INFO   [ContextManager] 更新上下文: 1d322be6-3ff1-405b-a589-f963a9f89866:ede5109c-aedb-4f49-b664-c5904624ac06:35a109bf-14c2-4bf7-bbff-7e03baf26a5d, 消息数=4, Token=218
17:02:41 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=1d322be6-3ff1-405b-a589-f963a9f89866:ede5109c-aedb-4f49-b664-c5904624ac06:35a109bf-14c2-4bf7-bbff-7e03baf26a5d)
17:02:41 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
17:02:41 app.api.v1.agent INFO   [LangGraph Agent Stream] User 1d322be6-3ff1-405b-a589-f963a9f89866 - Mode: planning, Stream completed
17:03:08 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/tasks/user/my-tasks
INFO:     127.0.0.1:58456 - "GET /api/v1/tasks/user/my-tasks HTTP/1.1" 200 OK
17:03:08 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/tasks/user/my-tasks
INFO:     127.0.0.1:58458 - "GET /api/v1/tasks/user/my-tasks HTTP/1.1" 200 OK
17:03:10 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/credits/balance
INFO:     127.0.0.1:49212 - "GET /api/v1/credits/balance HTTP/1.1" 200 OK
17:03:10 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/credits/transactions
INFO:     127.0.0.1:49214 - "GET /api/v1/credits/transactions?page=1&page_size=5 HTTP/1.1" 200 OK
17:03:10 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/credits/balance
INFO:     127.0.0.1:64330 - "GET /api/v1/credits/balance HTTP/1.1" 200 OK
17:03:10 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/credits/transactions
INFO:     127.0.0.1:55229 - "GET /api/v1/credits/transactions?page=1&page_size=5 HTTP/1.1" 200 OK
17:03:11 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/credits/transactions
INFO:     127.0.0.1:64288 - "GET /api/v1/credits/transactions?page=1&page_size=20 HTTP/1.1" 200 OK
17:03:11 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/credits/transactions
INFO:     127.0.0.1:61344 - "GET /api/v1/credits/transactions?page=1&page_size=20 HTTP/1.1" 200 OK
17:03:12 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/invitations/my-codes
INFO:     127.0.0.1:54032 - "GET /api/v1/invitations/my-codes HTTP/1.1" 200 OK
17:03:12 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/invitations/stats
INFO:     127.0.0.1:54030 - "GET /api/v1/invitations/stats HTTP/1.1" 200 OK
17:03:12 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/invitations/my-codes
INFO:     127.0.0.1:65419 - "GET /api/v1/invitations/my-codes HTTP/1.1" 200 OK
17:03:12 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/invitations/stats
INFO:     127.0.0.1:65421 - "GET /api/v1/invitations/stats HTTP/1.1" 200 OK
17:03:14 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:57655 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=100 HTTP/1.1" 200 OK
17:03:14 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:57657 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=100 HTTP/1.1" 200 OK
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me/notification-settings
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:56244 - "GET /api/v1/users/me/notification-settings HTTP/1.1" 200 OK
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me/preferences
INFO:     127.0.0.1:56245 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     127.0.0.1:56247 - "GET /api/v1/users/me/preferences HTTP/1.1" 200 OK
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me/sessions
INFO:     127.0.0.1:56249 - "GET /api/v1/users/me/sessions HTTP/1.1" 200 OK
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me/notification-settings
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:53922 - "GET /api/v1/users/me/notification-settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:56555 - "GET /api/v1/users/me HTTP/1.1" 200 OK
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me/preferences
INFO:     127.0.0.1:52175 - "GET /api/v1/users/me/preferences HTTP/1.1" 200 OK
17:03:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me/sessions
INFO:     127.0.0.1:63349 - "GET /api/v1/users/me/sessions HTTP/1.1" 200 OK
17:03:43 qcloud_cos.cos_client INFO   generate built-in connection pool success. maxsize=10,10
17:03:43 qcloud_cos.cos_client INFO   bound built-in connection pool when new client. maxsize=10,10
17:03:43 qcloud_cos.cos_client INFO   put object, url=:https://ai-writer-1365374837.cos.ap-guangzhou.myqcloud.com/uploads/avatars/7f093b44-4979-45e3-bfe4-e0b423e0cc93/a18980034c0345af89ecae28e92f6a45.png ,headers=:{'Content-Type': 'image/png'}
[Avatar Upload] About to check avatar task for user 7f093b44-4979-45e3-bfe4-e0b423e0cc93
[TaskService] Checking avatar task for user 7f093b44-4979-45e3-bfe4-e0b423e0cc93
[TaskService] Avatar task result: None
[Avatar Upload] Avatar task check completed
[Avatar Upload] Transaction committed
17:03:47 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/users/me/avatar
INFO:     127.0.0.1:62299 - "POST /api/v1/users/me/avatar HTTP/1.1" 200 OK
[Username Update] Transaction committed
17:03:52 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/users/me
INFO:     127.0.0.1:53919 - "PUT /api/v1/users/me HTTP/1.1" 200 OK
17:04:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
17:04:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52971 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52969 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:04:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:62304 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:04:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:62305 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:04:04 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:04 app.api.v1.chapters INFO   [GET chapters] work_id=01002d6b-3e2e-439d-81f9-22840d6eae11, user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     127.0.0.1:56452 - "GET /api/v1/works/01002d6b-3e2e-439d-81f9-22840d6eae11 HTTP/1.1" 200 OK
17:04:04 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:04 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=01002d6b-3e2e-439d-81f9-22840d6eae11, type=<class 'uuid.UUID'>
17:04:04 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:04 app.services.chapter_service INFO   [ChapterService] Found 50 chapters
17:04:04 app.services.chapter_service INFO     - Chapter: 第1章 重生斗气大陆, order=1
17:04:04 app.services.chapter_service INFO     - ... (48 more chapters)
17:04:04 app.services.chapter_service INFO     - Chapter: 第50章 抵达加码, order=50
17:04:04 app.api.v1.chapters INFO   [GET chapters] Returning 50 chapters
17:04:04 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=60s)
17:04:04 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:04 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:04 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:04 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/characters
17:04:04 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:04 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/locations
17:04:04 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/settings
INFO:     127.0.0.1:56456 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/characters HTTP/1.1" 200 OK
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/guidelines
INFO:     127.0.0.1:56455 - "GET /api/v1/chapters/work/01002d6b-3e2e-439d-81f9-22840d6eae11 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56460 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:56461 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:56462 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/guidelines HTTP/1.1" 200 OK
17:04:05 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/ai-guidelines
17:04:05 app.api.v1.chapters INFO   [GET chapters] work_id=01002d6b-3e2e-439d-81f9-22840d6eae11, user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     127.0.0.1:53602 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/ai-guidelines HTTP/1.1" 200 OK
17:04:05 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:05 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:05 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:05 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:01002d6b-3e2e-439d-81f9-22840d6eae11 (expire=300s)
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/characters
INFO:     127.0.0.1:61227 - "GET /api/v1/works/01002d6b-3e2e-439d-81f9-22840d6eae11 HTTP/1.1" 200 OK
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/locations
INFO:     127.0.0.1:56068 - "GET /api/v1/chapters/work/01002d6b-3e2e-439d-81f9-22840d6eae11 HTTP/1.1" 200 OK
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/settings
INFO:     127.0.0.1:56067 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60715 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:60717 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/settings HTTP/1.1" 200 OK
17:04:05 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:05 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/guidelines
INFO:     127.0.0.1:63728 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/guidelines HTTP/1.1" 200 OK
17:04:06 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:06 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/ai-guidelines
INFO:     127.0.0.1:52962 - "GET /api/v1/worldview/works/01002d6b-3e2e-439d-81f9-22840d6eae11/ai-guidelines HTTP/1.1" 200 OK
17:04:06 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/01002d6b-3e2e-439d-81f9-22840d6eae11/status
INFO:     127.0.0.1:56420 - "GET /api/v1/analysis/works/01002d6b-3e2e-439d-81f9-22840d6eae11/status HTTP/1.1" 404 Not Found
17:04:06 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/01002d6b-3e2e-439d-81f9-22840d6eae11/status
INFO:     127.0.0.1:50663 - "GET /api/v1/analysis/works/01002d6b-3e2e-439d-81f9-22840d6eae11/status HTTP/1.1" 404 Not Found
17:04:06 app.api.v1.ai INFO   [预加载元数据] 用户: kukulica(7f093b44-4979-45e3-bfe4-e0b423e0cc93), work_id: 01002d6b-3e2e-439d-81f9-22840d6eae11, chapter_id: 41cdf069-2f98-476f-a187-50203476f496
17:04:06 app.api.v1.ai INFO   [预加载] 当前章节已加载: 41cdf069-2f98-476f-a187-50203476f496
17:04:06 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:04:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53649 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:04:06 app.api.v1.ai INFO   [预加载元数据] 用户: kukulica(7f093b44-4979-45e3-bfe4-e0b423e0cc93), work_id: 01002d6b-3e2e-439d-81f9-22840d6eae11, chapter_id: 41cdf069-2f98-476f-a187-50203476f496
17:04:06 app.api.v1.ai INFO   [预加载] 当前章节已加载: 41cdf069-2f98-476f-a187-50203476f496
17:04:06 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:04:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61037 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:04:06 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:06 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/41cdf069-2f98-476f-a187-50203476f496
INFO:     127.0.0.1:65475 - "PUT /api/v1/chapters/41cdf069-2f98-476f-a187-50203476f496 HTTP/1.1" 200 OK
17:04:06 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
17:04:09 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
17:04:09 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:53034 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:04:09 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:53033 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:04:09 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:50393 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:04:09 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:49679 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:04:09 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:01002d6b-3e2e-439d-81f9-22840d6eae11
17:04:09 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/41cdf069-2f98-476f-a187-50203476f496
INFO:     127.0.0.1:49929 - "PUT /api/v1/chapters/41cdf069-2f98-476f-a187-50203476f496 HTTP/1.1" 200 OK
17:04:09 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
17:04:10 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
WARNING:  WatchFiles detected changes in 'app\services\ai\humanize_service.py', 'app\schemas\contact.py', 'app\api\v1\contact.py', 'app\api\__init__.py', 'app\services\ai\fast_ai_service.py', 'app\main.py'. Reloading...
17:06:32 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:06:32 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:64183 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
INFO:     Shutting down
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
17:06:32 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:06:32 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:64185 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
INFO:     Waiting for application shutdown.
17:06:32 app.main INFO   [SHUTDOWN] 应用关闭中...
17:06:32 app.tasks.cleanup_humanize_details INFO   定时任务调度器已停止
17:06:32 apscheduler.scheduler INFO   Scheduler has been shut down
17:06:32 app.main INFO   [SHUTDOWN] 应用已关闭
INFO:     Application shutdown complete.
INFO:     Finished server process [27724]
WARNING:  WatchFiles detected changes in 'app\services\ai\humanize_service.py', 'app\schemas\contact.py', 'app\api\v1\contact.py', 'app\api\__init__.py', 'app\services\ai\fast_ai_service.py', 'app\main.py'. Reloading...
Process SpawnProcess-3:
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\_subprocess.py", line 72, in subprocess_started
    sys.stdin = os.fdopen(stdin_fileno)
                ^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen os>", line 1066, in fdopen
  File "<frozen codecs>", line 309, in __init__
KeyboardInterrupt
已注册策略: web_novel_11d - 网文11维度分析
17:07:10 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
17:07:10 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [33396]
INFO:     Waiting for application startup.
17:07:10 app.main INFO   [STARTUP] 应用启动中...
17:07:10 app.core.database INFO   正在初始化数据库... (尝试 1/3)
17:07:10 app.core.database INFO   ✅ 数据库初始化成功
17:07:10 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
17:07:10 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
17:07:10 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
17:07:10 apscheduler.scheduler INFO   Added job "清理过期的 Agent 会话" to job store "default"
17:07:10 apscheduler.scheduler INFO   Scheduler started
17:07:10 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
17:07:10 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
17:07:10 app.api.v1.agent INFO   [Redis] 全局连接池已创建
17:07:10 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
17:07:10 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
17:07:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
17:07:10 redisvl.index.index INFO   Index already exists, not overwriting.
17:07:10 redisvl.index.index INFO   Index already exists, not overwriting.
17:07:10 redisvl.index.index INFO   Index already exists, not overwriting.
17:07:10 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
17:07:10 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
17:07:10 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
17:07:10 app.main INFO   [STARTUP] 开始预加载Embedding模型...
17:07:10 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
17:07:17 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 6.81秒
17:07:17 app.main INFO   [STARTUP] Embedding模型预加载完成
17:07:17 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
17:07:17 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
17:07:17 monitoring INFO   Registered health check: cpu_usage
17:07:17 monitoring INFO   Registered health check: memory_usage
17:07:17 monitoring INFO   Registered health check: disk_usage
17:07:17 monitoring INFO   Registered health check: process_status
17:07:17 monitoring INFO   Added alert rule: high_cpu_usage
17:07:17 monitoring INFO   Added alert rule: high_memory_usage
17:07:17 monitoring INFO   Added alert rule: low_disk_space
INFO:     ('127.0.0.1', 54240) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:07:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 57548) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
17:07:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 52260) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:07:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 56582) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
17:07:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     ('127.0.0.1', 60093) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
17:07:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 58909) - "WebSocket /api/v1/ws/notifications/1d322be6-3ff1-405b-a589-f963a9f89866" [accepted]
17:07:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=1d322be6-3ff1-405b-a589-f963a9f89866
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection closed
17:07:18 app.api.v1.ws ERROR   [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 945, in transfer_data
    message = await self.read_message()
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1015, in read_message
    frame = await self.read_data_frame(max_size=self.max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1090, in read_data_frame
    frame = await self.read_frame(max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1147, in read_frame
    frame = await Frame.read(
            ^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\framing.py", line 71, in read
    data = await reader(2)
           ^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\streams.py", line 750, in readexactly
    raise exceptions.IncompleteReadError(incomplete, n)
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: no close frame received or sent

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 196, in notifications_stream
    await websocket.send_json({
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 173, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 50, in sender
    await send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 365, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected
17:07:18 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:18 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:49774 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:07:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:52687 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:07:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
17:07:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:52689 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:07:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:52684 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52681 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:07:19 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:19 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:52685 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 51085) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:07:26 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     ('127.0.0.1', 54986) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:07:26 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
WARNING:  WatchFiles detected changes in 'app\services\ai\humanize_service.py', 'app\schemas\contact.py', 'app\api\v1\contact.py', 'app\api\__init__.py', 'app\services\ai\fast_ai_service.py', 'app\main.py'. Reloading...
17:07:56 app.api.v1.chapters INFO   [GET chapters] work_id=ede5109c-aedb-4f49-b664-c5904624ac06, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:07:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ede5109c-aedb-4f49-b664-c5904624ac06
17:07:56 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:07:56 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=ede5109c-aedb-4f49-b664-c5904624ac06, type=<class 'uuid.UUID'>
17:07:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
INFO:     127.0.0.1:62982 - "GET /api/v1/works/ede5109c-aedb-4f49-b664-c5904624ac06 HTTP/1.1" 200 OK
17:07:56 app.services.chapter_service INFO   [ChapterService] Found 2 chapters
17:07:56 app.services.chapter_service INFO     - Chapter: 第一章, order=1
17:07:56 app.services.chapter_service INFO     - Chapter: 第一章, order=1
17:07:56 app.api.v1.chapters INFO   [GET chapters] Returning 2 chapters
17:07:56 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=60s)
INFO:     Shutting down
17:07:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/characters
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
17:07:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:07:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:07:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ede5109c-aedb-4f49-b664-c5904624ac06
INFO:     127.0.0.1:62984 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62983 - "GET /api/v1/chapters/work/ede5109c-aedb-4f49-b664-c5904624ac06 HTTP/1.1" 200 OK
17:07:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/guidelines
17:07:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/locations
INFO:     127.0.0.1:62989 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62985 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/locations HTTP/1.1" 200 OK
17:07:56 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
INFO:     Waiting for connections to close. (CTRL+C to force quit)
17:07:56 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/settings
INFO:     127.0.0.1:62988 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/settings HTTP/1.1" 200 OK
17:07:57 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:07:57 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/ai-guidelines
INFO:     127.0.0.1:63203 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/ai-guidelines HTTP/1.1" 200 OK
INFO:     Waiting for application shutdown.
17:07:57 app.main INFO   [SHUTDOWN] 应用关闭中...
17:07:57 app.tasks.cleanup_humanize_details INFO   定时任务调度器已停止
17:07:57 apscheduler.scheduler INFO   Scheduler has been shut down
17:07:57 app.main INFO   [SHUTDOWN] 应用已关闭
INFO:     Application shutdown complete.
INFO:     Finished server process [33396]
Process SpawnProcess-5:
Traceback (most recent call last):
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python312\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\_subprocess.py", line 78, in subprocess_started
    target(sockets=sockets)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\server.py", line 62, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\base_events.py", line 687, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\server.py", line 69, in serve
    config.load()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\config.py", line 458, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\importer.py", line 21, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\importlib\__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 995, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "D:\Java\ai_writer\backend\app\main.py", line 19, in <module>
    from app.api import api_router
  File "D:\Java\ai_writer\backend\app\api\__init__.py", line 2, in <module>
    from app.api.v1 import (
  File "D:\Java\ai_writer\backend\app\api\v1\humanize.py", line 32, in <module>
    from app.services.ai.humanize_service import HumanizeService
  File "D:\Java\ai_writer\backend\app\services\ai\humanize_service.py", line 15, in <module>
    from app.services.ai.fast_ai_service import FastAIService
  File "D:\Java\ai_writer\backend\app\services\ai\fast_ai_service.py", line 45
    timeout: 超时时间(秒)，默认60秒（gemini-2.5-flash-lite响应较慢）
                    ^
SyntaxError: invalid character '，' (U+FF0C)
WARNING:  WatchFiles detected changes in 'app\services\ai\fast_ai_service.py'. Reloading...
已注册策略: web_novel_11d - 网文11维度分析
17:08:27 app.utils.file_storage INFO   临时文件存储目录: D:\Temp\novelaide_exports
17:08:27 app.main INFO   [STARTUP] 监控中间件已注册: TraceMiddleware, MonitoringMiddleware
INFO:     Started server process [23788]
INFO:     Waiting for application startup.
17:08:28 app.main INFO   [STARTUP] 应用启动中...
17:08:28 app.core.database INFO   正在初始化数据库... (尝试 1/3)
17:08:28 app.core.database INFO   ✅ 数据库初始化成功
17:08:28 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
17:08:28 apscheduler.scheduler INFO   Adding job tentatively -- it will be properly scheduled when the scheduler starts
17:08:28 apscheduler.scheduler INFO   Added job "清理过期的去痕迹会话详情" to job store "default"
17:08:28 apscheduler.scheduler INFO   Added job "清理过期的 Agent 会话" to job store "default"
17:08:28 apscheduler.scheduler INFO   Scheduler started
17:08:28 app.tasks.cleanup_humanize_details INFO   定时任务调度器已启动
17:08:28 app.main INFO   [STARTUP] 开始预初始化同步Redis连接...
17:08:28 app.api.v1.agent INFO   [Redis] 全局连接池已创建
17:08:28 app.main INFO   [STARTUP] ✅ 同步Redis连接池预初始化完成
17:08:28 app.main INFO   [STARTUP] 开始初始化AsyncRedisSaver索引...
17:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ setup_checkpointer Redis连接验证成功
17:08:28 redisvl.index.index INFO   Index already exists, not overwriting.
17:08:28 redisvl.index.index INFO   Index already exists, not overwriting.
17:08:28 redisvl.index.index INFO   Index already exists, not overwriting.
17:08:28 langgraph.checkpoint.redis.aio INFO   Redis client is a standalone client
17:08:28 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AsyncRedisSaver索引预创建成功
17:08:28 app.main INFO   [STARTUP] AsyncRedisSaver索引初始化完成
17:08:28 app.main INFO   [STARTUP] 开始预加载Embedding模型...
17:08:28 app.services.vector_store_service INFO   🔄 预加载Embedding模型: paraphrase-multilingual-MiniLM-L12-v2
17:08:35 app.services.vector_store_service INFO   ✅ Embedding模型预加载成功，耗时: 6.93秒
17:08:35 app.main INFO   [STARTUP] Embedding模型预加载完成
17:08:35 app.main INFO   [STARTUP] P0性能优化已暂时禁用（诊断模式）
17:08:35 app.main INFO   [STARTUP] 应用启动完成
INFO:     Application startup complete.
17:08:35 monitoring INFO   Registered health check: cpu_usage
17:08:35 monitoring INFO   Registered health check: memory_usage
17:08:35 monitoring INFO   Registered health check: disk_usage
17:08:35 monitoring INFO   Registered health check: process_status
17:08:35 monitoring INFO   Added alert rule: high_cpu_usage
17:08:35 monitoring INFO   Added alert rule: high_memory_usage
17:08:35 monitoring INFO   Added alert rule: low_disk_space
INFO:     ('127.0.0.1', 62494) - "WebSocket /api/v1/ws/notifications/1d322be6-3ff1-405b-a589-f963a9f89866" [accepted]
17:08:35 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=1d322be6-3ff1-405b-a589-f963a9f89866
INFO:     ('127.0.0.1', 58016) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
17:08:35 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     ('127.0.0.1', 59765) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:08:35 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 59056) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:08:35 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     ('127.0.0.1', 59077) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
17:08:35 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     ('127.0.0.1', 64109) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
17:08:35 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection open
INFO:     connection closed
17:08:36 app.api.v1.chapters INFO   [GET chapters] work_id=ede5109c-aedb-4f49-b664-c5904624ac06, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:08:36 app.api.v1.ws ERROR   [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 945, in transfer_data
    message = await self.read_message()
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1015, in read_message
    frame = await self.read_data_frame(max_size=self.max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1090, in read_data_frame
    frame = await self.read_frame(max_size)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 1147, in read_frame
    frame = await Frame.read(
            ^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\framing.py", line 71, in read
    data = await reader(2)
           ^^^^^^^^^^^^^^^
  File "C:\Program Files\Python312\Lib\asyncio\streams.py", line 750, in readexactly
    raise exceptions.IncompleteReadError(incomplete, n)
asyncio.exceptions.IncompleteReadError: 0 bytes read on a total of 2 expected bytes

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedError: no close frame received or sent

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 196, in notifications_stream
    await websocket.send_json({
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 173, in send_json
    await self.send({"type": "websocket.send", "text": text})
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\websockets.py", line 85, in send
    await self._send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\starlette\_exception_handler.py", line 50, in sender
    await send(message)
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 365, in asgi_send
    raise ClientDisconnected from exc
uvicorn.protocols.utils.ClientDisconnected
17:08:36 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:08:36 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/locations
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/characters
17:08:36 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
INFO:     127.0.0.1:57487 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/locations HTTP/1.1" 200 OK
17:08:36 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:ede5109c-aedb-4f49-b664-c5904624ac06
INFO:     127.0.0.1:62260 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/characters HTTP/1.1" 200 OK
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ede5109c-aedb-4f49-b664-c5904624ac06
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ede5109c-aedb-4f49-b664-c5904624ac06
INFO:     127.0.0.1:62640 - "GET /api/v1/chapters/work/ede5109c-aedb-4f49-b664-c5904624ac06 HTTP/1.1" 200 OK
17:08:36 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
INFO:     127.0.0.1:62259 - "GET /api/v1/works/ede5109c-aedb-4f49-b664-c5904624ac06 HTTP/1.1" 200 OK
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/guidelines
INFO:     127.0.0.1:55102 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/guidelines HTTP/1.1" 200 OK
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/settings
INFO:     127.0.0.1:52768 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/settings HTTP/1.1" 200 OK
17:08:36 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/ai-guidelines
INFO:     127.0.0.1:59400 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/ai-guidelines HTTP/1.1" 200 OK
17:08:37 app.api.v1.chapters INFO   [GET chapters] work_id=ede5109c-aedb-4f49-b664-c5904624ac06, user_id=1d322be6-3ff1-405b-a589-f963a9f89866
17:08:37 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ede5109c-aedb-4f49-b664-c5904624ac06
INFO:     127.0.0.1:60434 - "GET /api/v1/chapters/work/ede5109c-aedb-4f49-b664-c5904624ac06 HTTP/1.1" 200 OK
17:08:37 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/characters
INFO:     127.0.0.1:60436 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/characters HTTP/1.1" 200 OK
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ede5109c-aedb-4f49-b664-c5904624ac06
INFO:     127.0.0.1:60433 - "GET /api/v1/works/ede5109c-aedb-4f49-b664-c5904624ac06 HTTP/1.1" 200 OK
17:08:37 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/settings
INFO:     127.0.0.1:64761 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/settings HTTP/1.1" 200 OK
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ede5109c-aedb-4f49-b664-c5904624ac06/status
INFO:     127.0.0.1:60431 - "GET /api/v1/analysis/works/ede5109c-aedb-4f49-b664-c5904624ac06/status HTTP/1.1" 404 Not Found
17:08:37 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/guidelines
INFO:     127.0.0.1:64762 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/guidelines HTTP/1.1" 200 OK
17:08:37 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:ede5109c-aedb-4f49-b664-c5904624ac06 (expire=300s)
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/locations
INFO:     127.0.0.1:64758 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/locations HTTP/1.1" 200 OK
17:08:37 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/ai-guidelines
INFO:     127.0.0.1:53989 - "GET /api/v1/worldview/works/ede5109c-aedb-4f49-b664-c5904624ac06/ai-guidelines HTTP/1.1" 200 OK
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ede5109c-aedb-4f49-b664-c5904624ac06/status
INFO:     127.0.0.1:63823 - "GET /api/v1/analysis/works/ede5109c-aedb-4f49-b664-c5904624ac06/status HTTP/1.1" 404 Not Found
17:08:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/ede5109c-aedb-4f49-b664-c5904624ac06/status
INFO:     127.0.0.1:59612 - "GET /api/v1/analysis/works/ede5109c-aedb-4f49-b664-c5904624ac06/status HTTP/1.1" 404 Not Found
17:08:38 app.api.v1.ai INFO   [预加载元数据] 用户: zrt3ljnygz@sina.com(1d322be6-3ff1-405b-a589-f963a9f89866), work_id: ede5109c-aedb-4f49-b664-c5904624ac06, chapter_id: 573fa16e-017f-45ed-8c7b-d7651ccbf712
17:08:38 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
17:08:38 app.api.v1.ai INFO   [预加载] 当前章节已加载: 573fa16e-017f-45ed-8c7b-d7651ccbf712
17:08:38 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:08:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59614 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:08:38 app.api.v1.ai INFO   [预加载元数据] 用户: zrt3ljnygz@sina.com(1d322be6-3ff1-405b-a589-f963a9f89866), work_id: ede5109c-aedb-4f49-b664-c5904624ac06, chapter_id: 573fa16e-017f-45ed-8c7b-d7651ccbf712
17:08:38 app.api.v1.ai INFO   [预加载] 当前章节已加载: 573fa16e-017f-45ed-8c7b-d7651ccbf712
17:08:38 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:08:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60344 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:08:38 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:38 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:54134 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:08:38 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:38 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:63411 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:08:40 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:40 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:65110 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
17:08:40 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:ede5109c-aedb-4f49-b664-c5904624ac06
17:08:40 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712
INFO:     127.0.0.1:60071 - "PUT /api/v1/chapters/573fa16e-017f-45ed-8c7b-d7651ccbf712 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 50140) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:08:40 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     ('127.0.0.1', 61639) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:09:12 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     ('127.0.0.1', 52146) - "WebSocket /api/v1/ws/notifications/1d322be6-3ff1-405b-a589-f963a9f89866" [accepted]
17:11:29 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=1d322be6-3ff1-405b-a589-f963a9f89866
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 56780) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
17:14:59 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     connection open
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 51837) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:18:51 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 61974) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:19:11 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:19:11 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65413 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:19:11 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:65415 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:19:11 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:55393 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:19:12 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:64042 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 53510) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:19:17 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:24:04 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/users/me/preferences
INFO:     127.0.0.1:56200 - "PUT /api/v1/users/me/preferences HTTP/1.1" 401 Unauthorized
17:24:04 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:56203 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
17:24:04 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/users/me/preferences
INFO:     127.0.0.1:56206 - "PUT /api/v1/users/me/preferences HTTP/1.1" 200 OK
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/characters
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ddc0183e-76f5-4187-a491-9692a341996b
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ddc0183e-76f5-4187-a491-9692a341996b
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/locations
INFO:     127.0.0.1:51840 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/characters HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:51837 - "GET /api/v1/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:51839 - "GET /api/v1/chapters/work/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 401 Unauthorized
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:51841 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/locations HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:51836 - "POST /api/v1/agent/sessions HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:51838 - "POST /api/v1/agent/sessions HTTP/1.1" 401 Unauthorized
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/settings
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/guidelines
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/ai-guidelines
INFO:     127.0.0.1:60432 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/settings HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:60433 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/guidelines HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:60435 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/ai-guidelines HTTP/1.1" 401 Unauthorized
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/characters
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/ddc0183e-76f5-4187-a491-9692a341996b
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/ddc0183e-76f5-4187-a491-9692a341996b
INFO:     127.0.0.1:64314 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/characters HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:52935 - "GET /api/v1/chapters/work/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:52933 - "GET /api/v1/works/ddc0183e-76f5-4187-a491-9692a341996b HTTP/1.1" 401 Unauthorized
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:53040 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/locations
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/settings
INFO:     127.0.0.1:53042 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/locations HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:53044 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/settings HTTP/1.1" 401 Unauthorized
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/ai-guidelines
17:26:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/guidelines
INFO:     127.0.0.1:53987 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/ai-guidelines HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:53985 - "GET /api/v1/worldview/works/ddc0183e-76f5-4187-a491-9692a341996b/guidelines HTTP/1.1" 401 Unauthorized
INFO:     connection closed
INFO:     connection closed
17:26:41 app.api.v1.auth INFO   [LOGIN] 尝试登录: zrt3ljnygz@163.com (记住我: False)
17:26:41 app.services.login_rate_limit_service INFO   登录限流服务初始化成功
17:26:42 app.api.v1.auth WARNING   [LOGIN] 登录失败: zrt3ljnygz@163.com - 用户名或密码错误，剩余 4 次尝试
17:26:43 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:59001 - "POST /api/v1/auth/login HTTP/1.1" 401 Unauthorized
17:26:49 app.api.v1.auth INFO   [LOGIN] 尝试登录: zrt3ljnygz@163.com (记住我: False)
17:26:51 app.api.v1.auth INFO   [LOGIN] 登录成功: zrt3ljnygz@163.com (refreshToken 有效期: 7天)
17:26:51 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
17:26:51 app.api.v1.auth INFO   [LOGIN] 登录成功: testuser_new-1 (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
17:26:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:52201 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
17:26:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:57818 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 60471) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:26:52 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:26:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60474 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:26:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:60475 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:26:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:52950 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:26:52 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60477 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 53093) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:26:57 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection closed
INFO:     ('127.0.0.1', 52742) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:27:16 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:27:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
17:27:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52748 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:52749 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 401 Unauthorized
17:27:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
17:27:16 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52753 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:52752 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 401 Unauthorized
17:27:16 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:52756 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
17:27:17 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:52761 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
17:27:17 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
17:27:17 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:52763 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52765 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:27:17 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
17:27:17 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52771 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:52770 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 59719) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:27:21 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
INFO:     127.0.0.1:65046 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
INFO:     127.0.0.1:65047 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:65051 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
INFO:     127.0.0.1:65050 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:65048 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:65049 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
17:27:25 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:25 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:25 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:25 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:26 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
INFO:     127.0.0.1:64966 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
INFO:     127.0.0.1:64969 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:64978 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:64977 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:64972 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64981 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:27:26 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:27:26 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:26 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, type=<class 'uuid.UUID'>
17:27:26 app.services.chapter_service INFO   [ChapterService] Found 39 chapters
17:27:26 app.services.chapter_service INFO     - Chapter: 第1章 吞噬, order=1
17:27:26 app.services.chapter_service INFO     - ... (37 more chapters)
17:27:26 app.services.chapter_service INFO     - Chapter: 第5章 太一门, order=39
17:27:26 app.api.v1.chapters INFO   [GET chapters] Returning 39 chapters
17:27:26 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=60s)
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:64984 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:27:26 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:27:26 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:52777 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:52780 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:27:26 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:52784 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:27:27 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:27:27 app.api.v1.ai INFO   [预加载] 当前章节已加载: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:27:27 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:27:27 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52787 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:27:27 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:27:27 app.api.v1.ai INFO   [预加载] 当前章节已加载: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:27:27 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:27:27 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52792 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:27:28 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:28 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:64521 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
17:27:28 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 吞噬 (order=1)
17:27:33 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 吞噬 (7 chunks)
17:27:33 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:33 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:59502 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
17:27:33 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 吞噬 (order=1)
17:27:36 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 吞噬 (7 chunks)
17:27:40 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 29cdb754-a652-4caa-b251-f6e83057b680
17:27:40 app.api.v1.ai INFO   [预加载] 当前章节已加载: 29cdb754-a652-4caa-b251-f6e83057b680
17:27:40 app.api.v1.ai INFO   [预加载] 前一章节已加载: 18fdea35-9460-4984-87d4-7aeb59747d40
17:27:40 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:27:40 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 29cdb754-a652-4caa-b251-f6e83057b680
17:27:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53213 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:27:40 app.api.v1.ai INFO   [预加载] 当前章节已加载: 29cdb754-a652-4caa-b251-f6e83057b680
17:27:40 app.api.v1.ai INFO   [预加载] 前一章节已加载: 18fdea35-9460-4984-87d4-7aeb59747d40
17:27:40 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:27:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53218 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:27:40 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53219 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:27:43 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:43 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680
INFO:     127.0.0.1:58936 - "PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680 HTTP/1.1" 200 OK
17:27:43 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 家底 (order=4)
17:27:46 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 家底 (6 chunks)
17:27:46 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:46 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680
INFO:     127.0.0.1:58939 - "PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680 HTTP/1.1" 200 OK
17:27:46 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 家底 (order=4)
17:27:47 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 家底 (6 chunks)
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 65204) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:27:52 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:27:54 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:27:54 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:54 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:54 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:54 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, type=<class 'uuid.UUID'>
17:27:54 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:27:54 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
17:27:54 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
INFO:     127.0.0.1:62971 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:27:54 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
17:27:55 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:27:55 app.services.chapter_service INFO   [ChapterService] Found 39 chapters
17:27:55 app.services.chapter_service INFO     - Chapter: 第1章 吞噬, order=1
17:27:55 app.services.chapter_service INFO     - ... (37 more chapters)
17:27:55 app.services.chapter_service INFO     - Chapter: 第5章 太一门, order=39
17:27:55 app.api.v1.chapters INFO   [GET chapters] Returning 39 chapters
17:27:55 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=60s)
INFO:     127.0.0.1:62972 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62976 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
17:27:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
17:27:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
17:27:55 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:62974 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:62975 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:62973 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 55679) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:28:00 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:28:00 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:28:00 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:00 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
17:28:00 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:62979 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:00 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
INFO:     127.0.0.1:62985 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62983 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
17:28:00 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
INFO:     127.0.0.1:62988 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62991 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
INFO:     127.0.0.1:62994 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
17:28:00 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:00 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:55682 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:55687 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:28:00 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:55688 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:28:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:55691 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:28:01 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 29cdb754-a652-4caa-b251-f6e83057b680
17:28:01 app.api.v1.ai INFO   [预加载] 当前章节已加载: 29cdb754-a652-4caa-b251-f6e83057b680
17:28:01 app.api.v1.ai INFO   [预加载] 前一章节已加载: 18fdea35-9460-4984-87d4-7aeb59747d40
17:28:01 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:28:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55694 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:28:01 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 29cdb754-a652-4caa-b251-f6e83057b680
17:28:01 app.api.v1.ai INFO   [预加载] 当前章节已加载: 29cdb754-a652-4caa-b251-f6e83057b680
17:28:01 app.api.v1.ai INFO   [预加载] 前一章节已加载: 18fdea35-9460-4984-87d4-7aeb59747d40
17:28:01 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:28:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55697 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:28:01 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:01 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680
INFO:     127.0.0.1:55700 - "PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680 HTTP/1.1" 200 OK
17:28:01 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 家底 (order=4)
17:28:05 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 家底 (6 chunks)
17:28:05 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:28:05 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680
INFO:     127.0.0.1:55703 - "PUT /api/v1/chapters/29cdb754-a652-4caa-b251-f6e83057b680 HTTP/1.1" 200 OK
17:28:05 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 家底 (order=4)
17:28:07 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 家底 (6 chunks)
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:56971 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 401 Unauthorized
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:56973 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 401 Unauthorized
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:52140 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:52142 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 401 Unauthorized
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:63979 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
INFO:     127.0.0.1:63980 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60985 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:55978 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60609 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:29:58 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:50313 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:30:32 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:30:33 app.api.v1.agent WARNING   [create_agent_session] chapter_id c9dd9cbf-fa57-447e-9605-3020bbde5350 不存在，已忽略
17:30:33 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:33 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, type=<class 'uuid.UUID'>
17:30:33 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:33 app.services.chapter_service INFO   [ChapterService] Found 39 chapters
17:30:33 app.services.chapter_service INFO     - Chapter: 第1章 吞噬, order=1
17:30:33 app.services.chapter_service INFO     - ... (37 more chapters)
17:30:33 app.services.chapter_service INFO     - Chapter: 第5章 太一门, order=39
17:30:33 app.api.v1.chapters INFO   [GET chapters] Returning 39 chapters
17:30:33 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=60s)
17:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
17:30:33 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:30:33 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:57744 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
INFO:     127.0.0.1:57748 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:57747 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
17:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
INFO:     127.0.0.1:57750 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57749 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
17:30:33 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57743 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:30:34 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:34 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:34 app.api.v1.agent WARNING   [create_agent_session] chapter_id c9dd9cbf-fa57-447e-9605-3020bbde5350 不存在，已忽略
17:30:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
17:30:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
17:30:34 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:characters:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:34 app.api.v1.chapters INFO   [GET chapters] work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     127.0.0.1:51889 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51891 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:30:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters
17:30:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:34 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:61956 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54735 - "GET /api/v1/works/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:30:34 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350
INFO:     127.0.0.1:51478 - "GET /api/v1/chapters/work/c9dd9cbf-fa57-447e-9605-3020bbde5350 HTTP/1.1" 200 OK
17:30:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
17:30:35 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
17:30:35 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:c9dd9cbf-fa57-447e-9605-3020bbde5350 (expire=300s)
INFO:     127.0.0.1:54377 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:30:35 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations
17:30:35 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:35 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:35 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings
INFO:     127.0.0.1:56149 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:58939 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/settings HTTP/1.1" 200 OK
17:30:35 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines
17:30:35 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines
INFO:     127.0.0.1:62353 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62355 - "GET /api/v1/worldview/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/ai-guidelines HTTP/1.1" 200 OK
17:30:35 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:52841 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:30:36 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:59328 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:30:37 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:30:37 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:30:37 app.api.v1.ai INFO   [预加载] 当前章节已加载: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:30:37 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:30:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status
INFO:     127.0.0.1:56308 - "GET /api/v1/analysis/works/c9dd9cbf-fa57-447e-9605-3020bbde5350/status HTTP/1.1" 200 OK
17:30:37 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58358 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:30:37 app.api.v1.ai INFO   [预加载] 当前章节已加载: 627feba4-2097-4f28-a3f3-7641d10f7f40
17:30:37 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:30:37 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58360 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:30:37 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:37 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:52639 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
17:30:37 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 吞噬 (order=1)
17:30:39 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 吞噬 (7 chunks)
17:30:39 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:39 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40
INFO:     127.0.0.1:62476 - "PUT /api/v1/chapters/627feba4-2097-4f28-a3f3-7641d10f7f40 HTTP/1.1" 200 OK
17:30:39 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 吞噬 (order=1)
17:30:40 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 吞噬 (7 chunks)
17:30:48 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 2699b75a-456b-43cf-8733-7698c56afad0
17:30:48 app.api.v1.ai INFO   [预加载] 当前章节已加载: 2699b75a-456b-43cf-8733-7698c56afad0
17:30:48 app.api.v1.ai INFO   [预加载] 前一章节已加载: 74d61ed7-2ad9-490a-9f20-b14825b01dde
17:30:48 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:30:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50080 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:30:48 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: c9dd9cbf-fa57-447e-9605-3020bbde5350, chapter_id: 2699b75a-456b-43cf-8733-7698c56afad0
17:30:48 app.api.v1.ai INFO   [预加载] 当前章节已加载: 2699b75a-456b-43cf-8733-7698c56afad0
17:30:48 app.api.v1.ai INFO   [预加载] 前一章节已加载: 74d61ed7-2ad9-490a-9f20-b14825b01dde
17:30:48 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:30:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49916 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:30:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:49917 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:30:49 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:49 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/2699b75a-456b-43cf-8733-7698c56afad0
INFO:     127.0.0.1:51640 - "PUT /api/v1/chapters/2699b75a-456b-43cf-8733-7698c56afad0 HTTP/1.1" 200 OK
17:30:49 app.services.chapter_vector_service INFO   Vectorizing chapter: 第10章 呼吸感 (order=10)
17:30:51 app.services.chapter_vector_service INFO   Stored chapter vectors: 第10章 呼吸感 (6 chunks)
17:30:52 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:c9dd9cbf-fa57-447e-9605-3020bbde5350
17:30:52 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/2699b75a-456b-43cf-8733-7698c56afad0
INFO:     127.0.0.1:55046 - "PUT /api/v1/chapters/2699b75a-456b-43cf-8733-7698c56afad0 HTTP/1.1" 200 OK
17:30:52 app.services.chapter_vector_service INFO   Vectorizing chapter: 第10章 呼吸感 (order=10)
17:30:53 app.services.chapter_vector_service INFO   Stored chapter vectors: 第10章 呼吸感 (6 chunks)
17:31:07 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58176 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:31:07 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
17:31:07 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:31:07 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:31:07 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
17:31:16 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:31:16 app.api.v1.agent INFO   [Chat Stream] Mode: planning
17:31:17 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56133 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:31:17 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请帮我续写第10章"吸收兽火"的后续内容，描写萧凌吸收完桃花火后的感受，以及他决定去找萧战汇报打算去...
17:31:17 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:31:17 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:31:17 app.services.ai.http_ai_service INFO   [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
17:31:24 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:31:24 app.services.agent.tools.writing_tools INFO   Writing tools AI service initialized
17:31:24 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ AI Service 已同时设置到 langgraph_tools 和 writing_tools
17:31:24 app.services.context.adaptive_budget INFO   ✅ 所有预算配置验证通过
17:31:35 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
17:31:35 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
17:31:35 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
17:31:35 app.services.context.manager INFO   ✅ ContextManager: 自适应预算已启用
17:31:35 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用，自适应预算已启用，总预算=16000 tokens）
成功加载模板: analyze_text (版本 3.1.0)
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
成功加载模板: system_agent_prompt (版本 2.0.0)
成功加载模板: creative_writing_prompt (版本 1.0.0)
17:31:35 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
17:31:35 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ Redis连接验证成功
17:31:35 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
17:31:35 app.services.agent.memory.metrics INFO   [MemoryMetrics] 监控系统已初始化
17:31:35 app.services.agent.memory.long_term_store INFO   [LongTermStore] Initialized: base_dir=./data/long_term_memory, max_size=50KB, compression=True
17:31:35 app.services.agent.memory.enhanced_memory_manager INFO   EnhancedMemoryManager initialized: short=10, medium=100, threshold=0.1, long_term_backup=enabled
17:31:35 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ EnhancedMemoryManager已创建
17:31:35 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 初始化统一记忆协调器
17:31:35 app.services.agent.memory.unified_coordinator INFO   [UnifiedMemoryCoordinator] 全局实例已设置
17:31:35 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ UnifiedMemoryCoordinator已初始化 | checkpointer=AsyncRedisSaver | enhanced_memory=yes | context_manager=yes
17:31:35 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 初始化完成，最大并发数=5，并行安全工具=4个
17:31:35 app.api.v1.agent INFO   [Global Agent] created global agent instance; MemorySaver shared across requests
17:31:35 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
17:31:35 app.api.v1.agent INFO     - selected_text: N/A...
17:31:35 app.api.v1.agent INFO     - selection_position: N/A
17:31:35 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 2699b75a-456b-43cf-8733-7698c56afad0...
17:31:35 app.api.v1.agent INFO     - instruction_context: N/A...
17:31:35 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:c9dd9cbf-fa57-447e-9605-3020bbde5350:32fe84b0-0808-431b-bc4b-e6938667da19 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350, conversation_id=32fe84b0-0808-431b-bc4b-e6938667da19)
17:31:35 app.services.context.monitoring_integration INFO   ✅ ContextManager监控收集器已初始化
17:31:35 app.services.context.store INFO   [ContextStore] Redis连接成功
17:31:35 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:c9dd9cbf-fa57-447e-9605-3020bbde5350:32fe84b0-0808-431b-bc4b-e6938667da19
17:31:35 app.services.context.token_counter WARNING   ⚠️ tiktoken初始化失败: 'Could not automatically map gemini-2.5-pro to a tokeniser. Please use `tiktoken.get_encoding` to explicitly get the tokeniser you expect.'，将使用降级策略
17:31:35 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:c9dd9cbf-fa57-447e-9605-3020bbde5350:32fe84b0-0808-431b-bc4b-e6938667da19: 0/16000 tokens
17:31:36 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请帮我续写第10章"吸收兽火"的后续内容，描写萧凌吸收完桃花...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:c9dd9cbf-fa57-447e-9605-3020bbde5350', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
17:31:36 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=c9dd9cbf-fa57-447e-9605-3020bbde5350 | 含用户级=True | 找到=3条
17:31:36 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 852.41ms
17:31:36 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
17:31:36 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请帮我续写第10章"吸收兽火"的后续内容，描写萧凌吸收完桃花火后的感受，以及他决定去找萧战汇报打算去...
17:31:36 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
17:31:36 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:31:36 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:31:36 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
17:31:39 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:31:45 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 1104
17:31:45 app.services.ai.http_ai_service INFO   流式响应Token统计: 7413 (prompt=6860, completion=553)
17:31:45 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:31:45 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:31:45 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7413, cost=$0.014105, time=9068ms
17:31:45 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7413
17:31:45 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
17:31:45 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到的是对第10章“吸收兽火”内容的续写，重点描写主, 原料=需要第10章“吸收兽火”的内容作为续写的, 处理=使用`continue_writing_
17:31:45 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 9.16s
17:31:45 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
17:31:45 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:31:45 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
17:31:45 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
17:31:45 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
17:31:45 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
17:31:45 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
17:31:45 app.api.v1.agent INFO   [Stream] Task started: 获取第10章“吸收兽火”的内容作为续写上下文
17:31:45 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(get_chapter_by_order)
17:31:45 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 开始执行工具
17:31:45 app.services.agent.langgraph_tools INFO   [get_chapter_by_order_tool] ✅ 找到第10章: 第10章 呼吸感
17:31:45 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 执行成功 (耗时: 0.015s)
17:31:45 app.services.agent.tools.tool_monitor INFO   ToolMonitor initialized with Memory storage, retention: 7 days
17:31:45 app.services.agent.langgraph_agent INFO   [StandardTool] get_chapter_by_order 执行成功（DeepAgent模式）
17:31:45 app.api.v1.agent INFO   [Stream] 任务完成: 获取第10章“吸收兽火”的内容作为续写上下文 (0.0s)
17:31:45 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
17:31:45 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
17:31:45 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
17:31:45 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:31:45 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:31:45 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
17:31:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:31:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 118
17:31:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 1923 (prompt=1862, completion=61)
17:31:53 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:31:53 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:31:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1923, cost=$0.002937, time=7378ms
17:31:53 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1923
17:31:53 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
17:31:53 app.api.v1.agent INFO   [Stream] Task started: 根据用户要求续写第10章内容
17:31:53 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
17:31:53 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
17:31:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
17:31:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
17:31:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
17:31:56 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:32:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 624
17:32:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 5168 (prompt=4655, completion=513)
17:32:24 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:32:24 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:32:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5168, cost=$0.010949, time=30944ms
17:32:24 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 31.297s)
17:32:24 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
17:32:24 app.api.v1.agent INFO   [Stream] 任务完成: 根据用户要求续写第10章内容 (31.3s)
17:32:24 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:32:24 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:32:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=200, temp=0.1, task_type=TaskType.SIMPLE_QA
17:32:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:32:44 app.services.ai.http_ai_service INFO   [HTTPAIService] 流式请求被取消，关闭连接
17:32:44 app.services.agent.deep_agent.executor WARNING   末尾验收调用失败，忽略校验:
17:32:44 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
17:32:44 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
17:32:44 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 58.84s
17:32:44 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:32:44 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
17:32:44 app.services.agent.langgraph_agent INFO   [Response] 单个创作任务(continue_writing_tool)，输出624字符，直接返回（跳过AI调用）
17:32:46 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:c9dd9cbf-fa57-447e-9605-3020bbde5350 | 重要度=0.84
17:32:47 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:c9dd9cbf-fa57-447e-9605-3020bbde5350 | 重要度=0.58
17:32:47 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:c9dd9cbf-fa57-447e-9605-3020bbde5350:32fe84b0-0808-431b-bc4b-e6938667da19, token=423
17:32:47 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:c9dd9cbf-fa57-447e-9605-3020bbde5350:32fe84b0-0808-431b-bc4b-e6938667da19, 消息数=2, Token=423
17:32:47 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:c9dd9cbf-fa57-447e-9605-3020bbde5350:32fe84b0-0808-431b-bc4b-e6938667da19)
17:32:47 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
17:32:47 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
17:37:44 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/users/me/preferences
INFO:     127.0.0.1:51827 - "PUT /api/v1/users/me/preferences HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
17:44:48 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:62753 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:44:49 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:62754 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:44:49 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:62758 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:44:49 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:54782 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:45:34 app.api.v1.auth INFO   [LOGIN] 尝试登录: zrt3ljnygz@sina.com (记住我: True)
17:45:35 app.api.v1.auth INFO   [LOGIN] 登录成功: zrt3ljnygz@sina.com (refreshToken 有效期: 30天)
17:45:35 app.api.v1.auth INFO   [LOGIN] 会话创建成功: 1d322be6-3ff1-405b-a589-f963a9f89866 (127.0.0.1)
17:45:35 app.api.v1.auth INFO   [LOGIN] 登录成功: zrt3ljnygz@sina.com (1d322be6-3ff1-405b-a589-f963a9f89866) from 127.0.0.1
17:45:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:51691 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
17:45:36 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:61707 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 60649) - "WebSocket /api/v1/ws/notifications/1d322be6-3ff1-405b-a589-f963a9f89866" [accepted]
17:45:36 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=1d322be6-3ff1-405b-a589-f963a9f89866
INFO:     connection open
17:45:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60652 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:45:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:60654 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:45:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:50765 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:45:37 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60658 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:45:39 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/users/me/preferences
INFO:     127.0.0.1:57799 - "PUT /api/v1/users/me/preferences HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 63848) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:47:42 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:47:43 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:63855 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:47:43 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:63862 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
17:47:43 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63856 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:47:43 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63859 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 60069) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
17:47:47 app.api.v1.ws INFO   [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
17:48:38 app.api.v1.import_routes INFO   用户 602f5147-846a-4cde-95d3-405fa75f133f 预览导入文件: 斗破：开局获取抽取系统.txt, 格式: txt
17:48:38 app.api.v1.import_routes INFO   预览成功: 作品=斗破：开局获取抽取系统, 章节数=50
17:48:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:65152 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
17:48:53 app.api.v1.import_routes INFO   用户 602f5147-846a-4cde-95d3-405fa75f133f 导入文件: 斗破：开局获取抽取系统.txt, 格式: txt
17:48:53 app.services.import_service INFO   用户 602f5147-846a-4cde-95d3-405fa75f133f 开始导入文本数据
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service WARNING   Failed to record delta for imported chapter None: badly formed hexadecimal UUID string
17:48:53 app.services.import_service INFO   文本导入完成: 作品ID=972a2087-ff2c-4fb7-a501-18b36906dd1b, 章节=50
17:48:53 app.api.v1.import_routes INFO   导入成功: 作品ID=972a2087-ff2c-4fb7-a501-18b36906dd1b, 章节=50, 人物=0
17:48:53 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:59672 - "POST /api/v1/works/import HTTP/1.1" 200 OK
17:48:53 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
17:48:54 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52618 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
17:48:54 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
17:48:54 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 萧薰儿 (order=2)
17:48:56 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 萧薰儿 (6 chunks)
17:48:56 app.services.chapter_vector_service INFO   Vectorizing chapter: 第3章 蕴养筋脉 (order=3)
17:48:59 app.api.v1.chapters INFO   [GET chapters] work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:48:59 app.services.chapter_vector_service INFO   Stored chapter vectors: 第3章 蕴养筋脉 (6 chunks)
17:48:59 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 逛街 (order=4)
17:48:59 app.api.v1.agent WARNING   [create_agent_session] chapter_id 972a2087-ff2c-4fb7-a501-18b36906dd1b 不存在，已忽略
17:49:01 app.api.v1.chapters INFO   ⚠️ [GET chapters] 缓存未命中: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:01 app.services.chapter_service INFO   [ChapterService] Querying chapters for work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, type=<class 'uuid.UUID'>
17:49:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:01 app.services.chapter_service INFO   [ChapterService] Found 50 chapters
17:49:01 app.services.chapter_service INFO     - Chapter: 第1章 重生斗气大陆, order=1
17:49:01 app.services.chapter_service INFO     - ... (48 more chapters)
17:49:01 app.services.chapter_service INFO     - Chapter: 第50章 抵达加码, order=50
17:49:01 app.api.v1.chapters INFO   [GET chapters] Returning 50 chapters
17:49:01 app.api.v1.chapters INFO   💾 [GET chapters] 缓存已保存: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=60s)
17:49:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/locations
17:49:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/settings
17:49:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/972a2087-ff2c-4fb7-a501-18b36906dd1b
INFO:     127.0.0.1:61224 - "GET /api/v1/works/972a2087-ff2c-4fb7-a501-18b36906dd1b HTTP/1.1" 200 OK
17:49:01 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 逛街 (6 chunks)
17:49:01 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
INFO:     127.0.0.1:61228 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61229 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:61226 - "GET /api/v1/chapters/work/972a2087-ff2c-4fb7-a501-18b36906dd1b HTTP/1.1" 200 OK
17:49:01 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
17:49:01 app.services.chapter_vector_service INFO   Vectorizing chapter: 第5章 黑铁片 (order=5)
INFO:     127.0.0.1:61225 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:49:01 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/characters
INFO:     127.0.0.1:61227 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/characters HTTP/1.1" 200 OK
17:49:02 app.services.chapter_vector_service INFO   Stored chapter vectors: 第5章 黑铁片 (5 chunks)
17:49:02 app.services.chapter_vector_service INFO   Vectorizing chapter: 第6章 斗者 (order=6)
17:49:02 app.api.v1.chapters INFO   [GET chapters] work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:49:03 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:ai-guidelines:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:03 app.api.v1.agent WARNING   [create_agent_session] chapter_id 972a2087-ff2c-4fb7-a501-18b36906dd1b 不存在，已忽略
17:49:03 app.api.v1.chapters INFO   ✅ [GET chapters] 缓存命中: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:03 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/ai-guidelines
17:49:03 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/works/972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:03 app.services.chapter_vector_service INFO   Stored chapter vectors: 第6章 斗者 (6 chunks)
17:49:03 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/chapters/work/972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:03 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:guidelines:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:03 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:characters:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:03 app.services.chapter_vector_service INFO   Vectorizing chapter: 第7章 《弄炎决》 (order=7)
INFO:     127.0.0.1:61236 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61243 - "GET /api/v1/works/972a2087-ff2c-4fb7-a501-18b36906dd1b HTTP/1.1" 200 OK
INFO:     127.0.0.1:61246 - "GET /api/v1/chapters/work/972a2087-ff2c-4fb7-a501-18b36906dd1b HTTP/1.1" 200 OK
17:49:03 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/guidelines
17:49:03 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/characters
INFO:     127.0.0.1:61234 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61247 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/characters HTTP/1.1" 200 OK
17:49:05 app.services.chapter_vector_service INFO   Stored chapter vectors: 第7章 《弄炎决》 (5 chunks)
17:49:05 app.services.chapter_vector_service INFO   Vectorizing chapter: 第8章 米特尔拍卖场 (order=8)
17:49:05 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61239 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:49:06 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:guidelines:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:06 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:settings:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:06 app.api.v1.worldview INFO   ✅ [Worldview] 缓存命中: worldview:ai-guidelines:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:06 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/guidelines
17:49:06 app.services.chapter_vector_service INFO   Stored chapter vectors: 第8章 米特尔拍卖场 (5 chunks)
17:49:06 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/settings
17:49:06 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/ai-guidelines
17:49:06 app.services.chapter_vector_service INFO   Vectorizing chapter: 第9章 后山水池 (order=9)
INFO:     127.0.0.1:55501 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:55498 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:55504 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/ai-guidelines HTTP/1.1" 200 OK
17:49:06 app.api.v1.worldview INFO   💾 [Worldview] 缓存已保存: worldview:locations:972a2087-ff2c-4fb7-a501-18b36906dd1b (expire=300s)
17:49:07 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/locations
INFO:     127.0.0.1:55497 - "GET /api/v1/worldview/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/locations HTTP/1.1" 200 OK
17:49:07 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/status
17:49:07 app.services.chapter_vector_service INFO   Stored chapter vectors: 第9章 后山水池 (5 chunks)
INFO:     127.0.0.1:55507 - "GET /api/v1/analysis/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/status HTTP/1.1" 404 Not Found
17:49:07 app.services.chapter_vector_service INFO   Vectorizing chapter: 第10章 吸收兽火 (order=10)
17:49:07 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:63829 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:49:09 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
17:49:09 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
17:49:09 app.api.v1.ai INFO   [预加载] 当前章节已加载: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
17:49:09 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:49:09 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52893 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:49:09 app.api.v1.ai INFO   [预加载] 当前章节已加载: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
17:49:09 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
17:49:09 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52895 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:49:09 app.api.middleware.monitoring_middleware INFO   API请求完成: GET /api/v1/analysis/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/status
INFO:     127.0.0.1:52889 - "GET /api/v1/analysis/works/972a2087-ff2c-4fb7-a501-18b36906dd1b/status HTTP/1.1" 404 Not Found
17:49:09 app.services.chapter_vector_service INFO   Stored chapter vectors: 第10章 吸收兽火 (6 chunks)
17:49:09 app.services.chapter_vector_service INFO   Vectorizing chapter: 第11章 迦南学院招生 (order=11)
17:49:09 app.services.chapter_vector_service INFO   Stored chapter vectors: 第11章 迦南学院招生 (5 chunks)
17:49:09 app.services.chapter_vector_service INFO   Vectorizing chapter: 第12章 启程迦南 (order=12)
17:49:10 app.services.chapter_vector_service INFO   Stored chapter vectors: 第12章 启程迦南 (5 chunks)
17:49:10 app.services.chapter_vector_service INFO   Vectorizing chapter: 第13章 抵达学院 (order=13)
17:49:12 app.services.chapter_vector_service INFO   Stored chapter vectors: 第13章 抵达学院 (7 chunks)
17:49:12 app.services.chapter_vector_service INFO   Vectorizing chapter: 第14章 入炼药系 (order=14)
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
17:49:13 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:13 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
INFO:     127.0.0.1:52898 - "PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa HTTP/1.1" 200 OK
17:49:13 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
17:49:13 app.services.chapter_vector_service INFO   Stored chapter vectors: 第14章 入炼药系 (9 chunks)
17:49:13 app.services.chapter_vector_service INFO   Vectorizing chapter: 第15章 炼药 (order=15)
17:49:17 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
17:49:17 app.services.chapter_vector_service INFO   Stored chapter vectors: 第15章 炼药 (5 chunks)
17:49:17 app.services.chapter_vector_service INFO   Vectorizing chapter: 第16章 修炼 (order=16)
17:49:19 app.services.chapter_vector_service INFO   Stored chapter vectors: 第16章 修炼 (5 chunks)
17:49:19 app.services.chapter_vector_service INFO   Vectorizing chapter: 第17章 裂空座 (order=17)
17:49:20 app.services.chapter_vector_service INFO   Stored chapter vectors: 第17章 裂空座 (5 chunks)
17:49:20 app.services.chapter_vector_service INFO   Vectorizing chapter: 第18章 抽取 (order=18)
17:49:21 app.services.chapter_vector_service INFO   Stored chapter vectors: 第18章 抽取 (5 chunks)
17:49:21 app.services.chapter_vector_service INFO   Vectorizing chapter: 第19章 前往历练 (order=19)
17:49:22 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:22 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
INFO:     127.0.0.1:52155 - "PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa HTTP/1.1" 200 OK
17:49:22 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
17:49:22 app.services.chapter_vector_service INFO   Stored chapter vectors: 第19章 前往历练 (5 chunks)
17:49:22 app.services.chapter_vector_service INFO   Vectorizing chapter: 第20章 历练 (order=20)
17:49:24 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
17:49:24 app.services.chapter_vector_service INFO   Stored chapter vectors: 第20章 历练 (5 chunks)
17:49:24 app.services.chapter_vector_service INFO   Vectorizing chapter: 第21章 回学院 (order=21)
17:49:25 app.services.chapter_vector_service INFO   Stored chapter vectors: 第21章 回学院 (5 chunks)
17:49:25 app.services.chapter_vector_service INFO   Vectorizing chapter: 第22章 韩月 (order=22)
17:49:26 app.services.chapter_vector_service INFO   Stored chapter vectors: 第22章 韩月 (5 chunks)
17:49:26 app.services.chapter_vector_service INFO   Vectorizing chapter: 第23章 无上自在门 (order=23)
17:49:27 app.services.chapter_vector_service INFO   Stored chapter vectors: 第23章 无上自在门 (8 chunks)
17:49:27 app.services.chapter_vector_service INFO   Vectorizing chapter: 第24章 选拔赛开始 (order=24)
17:49:29 app.services.chapter_vector_service INFO   Stored chapter vectors: 第24章 选拔赛开始 (6 chunks)
17:49:29 app.services.chapter_vector_service INFO   Vectorizing chapter: 第25章 选拔赛结束 (order=25)
17:49:29 app.services.chapter_vector_service INFO   Stored chapter vectors: 第25章 选拔赛结束 (5 chunks)
17:49:29 app.services.chapter_vector_service INFO   Vectorizing chapter: 第26章 你真美 (order=26)
17:49:30 app.services.chapter_vector_service INFO   Stored chapter vectors: 第26章 你真美 (5 chunks)
17:49:30 app.services.chapter_vector_service INFO   Vectorizing chapter: 第27章 第二十七 进入藏书阁 (order=27)
17:49:31 app.services.chapter_vector_service INFO   Stored chapter vectors: 第27章 第二十七 进入藏书阁 (5 chunks)
17:49:31 app.services.chapter_vector_service INFO   Vectorizing chapter: 第28章 取宝 (order=28)
17:49:32 app.services.chapter_vector_service INFO   Stored chapter vectors: 第28章 取宝 (6 chunks)
17:49:32 app.services.chapter_vector_service INFO   Vectorizing chapter: 第29章 抽取 (order=29)
17:49:33 app.services.chapter_vector_service INFO   Stored chapter vectors: 第29章 抽取 (6 chunks)
17:49:33 app.services.chapter_vector_service INFO   Vectorizing chapter: 第30章 前往内院 (order=30)
17:49:34 app.services.chapter_vector_service INFO   Stored chapter vectors: 第30章 前往内院 (5 chunks)
17:49:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第31章 飞行路途 (order=31)
17:49:34 app.services.chapter_vector_service INFO   Stored chapter vectors: 第31章 飞行路途 (7 chunks)
17:49:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第32章 火能猎捕赛 (order=32)
17:49:36 app.services.chapter_vector_service INFO   Stored chapter vectors: 第32章 火能猎捕赛 (6 chunks)
17:49:36 app.services.chapter_vector_service INFO   Vectorizing chapter: 第33章 进入内院 (order=33)
17:49:38 app.services.chapter_vector_service INFO   Stored chapter vectors: 第33章 进入内院 (6 chunks)
17:49:38 app.services.chapter_vector_service INFO   Vectorizing chapter: 第34章 安顿 (order=34)
17:49:40 app.services.chapter_vector_service INFO   Stored chapter vectors: 第34章 安顿 (5 chunks)
17:49:40 app.services.chapter_vector_service INFO   Vectorizing chapter: 第35章 纳贡费 (order=35)
17:49:42 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 9578da5d-3109-49b7-aa04-807fb36d31f3
17:49:42 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 9578da5d-3109-49b7-aa04-807fb36d31f3
17:49:42 app.services.chapter_vector_service INFO   Stored chapter vectors: 第35章 纳贡费 (6 chunks)
17:49:42 app.api.v1.ai INFO   [预加载] 当前章节已加载: 9578da5d-3109-49b7-aa04-807fb36d31f3
17:49:42 app.services.chapter_vector_service INFO   Vectorizing chapter: 第36章 天焚练气塔 (order=36)
17:49:42 app.api.v1.ai INFO   [预加载] 前一章节已加载: 7e2cdf1b-ca99-4f63-aa8d-2294fb71e34c
17:49:42 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:49:42 app.api.v1.ai INFO   [预加载] 当前章节已加载: 9578da5d-3109-49b7-aa04-807fb36d31f3
17:49:43 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
17:49:43 app.api.v1.ai INFO   [预加载] 前一章节已加载: 7e2cdf1b-ca99-4f63-aa8d-2294fb71e34c
17:49:43 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:57529 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:49:43 app.services.chapter_vector_service INFO   Stored chapter vectors: 第36章 天焚练气塔 (5 chunks)
17:49:43 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
17:49:43 app.services.chapter_vector_service INFO   Vectorizing chapter: 第37章 淬炼斗气 (order=37)
17:49:43 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57524 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:57530 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:49:45 app.services.chapter_vector_service INFO   Stored chapter vectors: 第37章 淬炼斗气 (7 chunks)
17:49:45 app.services.chapter_vector_service INFO   Vectorizing chapter: 第38章 紫妍 (order=38)
17:49:46 app.services.chapter_vector_service INFO   Stored chapter vectors: 第38章 紫妍 (6 chunks)
17:49:46 app.services.chapter_vector_service INFO   Vectorizing chapter: 第39章 炼制药丸 (order=39)
17:49:47 app.services.chapter_vector_service INFO   Stored chapter vectors: 第39章 炼制药丸 (6 chunks)
17:49:47 app.services.chapter_vector_service INFO   Vectorizing chapter: 第40章 日常 (order=40)
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
17:49:47 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:49:47 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/9578da5d-3109-49b7-aa04-807fb36d31f3
17:49:47 app.services.chapter_vector_service INFO   Stored chapter vectors: 第40章 日常 (5 chunks)
17:49:47 app.services.chapter_vector_service INFO   Vectorizing chapter: 第41章 晋升斗王 (order=41)
INFO:     127.0.0.1:54032 - "PUT /api/v1/chapters/9578da5d-3109-49b7-aa04-807fb36d31f3 HTTP/1.1" 200 OK
17:49:47 app.services.chapter_vector_service INFO   Vectorizing chapter: 第10章 吸收兽火 (order=10)
17:49:48 app.services.chapter_vector_service INFO   Stored chapter vectors: 第41章 晋升斗王 (5 chunks)
17:49:48 app.services.chapter_vector_service INFO   Vectorizing chapter: 第42章 与苏千交谈 (order=42)
17:49:48 app.services.chapter_vector_service INFO   Stored chapter vectors: 第10章 吸收兽火 (6 chunks)
17:49:49 app.services.chapter_vector_service INFO   Stored chapter vectors: 第42章 与苏千交谈 (7 chunks)
17:49:49 app.services.chapter_vector_service INFO   Vectorizing chapter: 第43章 抽取 (order=43)
17:49:50 app.services.chapter_vector_service INFO   Stored chapter vectors: 第43章 抽取 (6 chunks)
17:49:50 app.services.chapter_vector_service INFO   Vectorizing chapter: 第44章 夜访韩月 (order=44)
17:49:51 app.services.chapter_vector_service INFO   Stored chapter vectors: 第44章 夜访韩月 (5 chunks)
17:49:51 app.services.chapter_vector_service INFO   Vectorizing chapter: 第45章 金帝焚天炎子火 (order=45)
17:49:52 app.services.chapter_vector_service INFO   Stored chapter vectors: 第45章 金帝焚天炎子火 (5 chunks)
17:49:52 app.services.chapter_vector_service INFO   Vectorizing chapter: 第46章 《帝印诀》 (order=46)
17:49:52 app.services.chapter_vector_service INFO   Stored chapter vectors: 第46章 《帝印诀》 (5 chunks)
17:49:52 app.services.chapter_vector_service INFO   Vectorizing chapter: 第47章 吞噬金帝焚天炎子火 (order=47)
17:49:52 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53948 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:49:55 app.services.chapter_vector_service INFO   Stored chapter vectors: 第47章 吞噬金帝焚天炎子火 (10 chunks)
17:49:55 app.services.chapter_vector_service INFO   Vectorizing chapter: 第48章 启程加玛帝国 (order=48)
17:49:55 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:49:55 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:49:55 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
17:49:58 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:49:58 app.api.v1.agent INFO   [Chat Stream] Mode: planning
17:50:00 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
17:50:00 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
INFO:     127.0.0.1:53952 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:50:00 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/9578da5d-3109-49b7-aa04-807fb36d31f3
17:50:00 app.services.chapter_vector_service INFO   Stored chapter vectors: 第48章 启程加玛帝国 (10 chunks)
17:50:00 app.services.chapter_vector_service INFO   Vectorizing chapter: 第49章 飞行路途 (order=49)
INFO:     127.0.0.1:53945 - "PUT /api/v1/chapters/9578da5d-3109-49b7-aa04-807fb36d31f3 HTTP/1.1" 200 OK
17:50:01 app.services.chapter_vector_service INFO   Vectorizing chapter: 第10章 吸收兽火 (order=10)
17:50:01 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请帮我续写第10章"吸收兽火"的后续内容，描写萧凌吸收完桃花火后的感受，以及他决定去找萧战汇报打算去...
17:50:04 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
17:50:04 app.api.v1.agent INFO     - selected_text: N/A...
17:50:04 app.api.v1.agent INFO     - selection_position: N/A
17:50:04 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 9578da5d-3109-49b7-aa04-807fb36d31f3...
17:50:04 app.api.v1.agent INFO     - instruction_context: N/A...
17:50:04 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=55a1a141-c158-4818-8422-900eaa938d66)
17:50:04 app.services.chapter_vector_service INFO   Stored chapter vectors: 第49章 飞行路途 (6 chunks)
17:50:04 app.services.chapter_vector_service INFO   Stored chapter vectors: 第10章 吸收兽火 (6 chunks)
17:50:04 app.services.chapter_vector_service INFO   Vectorizing chapter: 第50章 抵达加码 (order=50)
17:50:04 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66
17:50:04 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66: 0/16000 tokens
17:50:04 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请帮我续写第10章"吸收兽火"的后续内容，描写萧凌吸收完桃花...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=0条
17:50:04 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=0条
17:50:04 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 290.41ms
17:50:04 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请帮我续写第10章"吸收兽火"的后续内容，描写萧凌吸收完桃花火后的感受，以及他决定去找萧战汇报打算去...
17:50:04 app.core.cache INFO   ✅ 缓存命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
17:50:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:50:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:50:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
17:50:06 app.services.chapter_vector_service INFO   Stored chapter vectors: 第50章 抵达加码 (7 chunks)
17:50:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:50:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 872
17:50:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 7130 (prompt=6737, completion=393)
17:50:22 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:50:22 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:50:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7130, cost=$0.012351, time=16832ms
17:50:22 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7130
17:50:22 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
17:50:22 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到的是续写内容，即新的章节正文。, 原料=需要获取第10章的现有内容作为续写的基础, 处理=使用continue_writing_t
17:50:22 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 18.40s
17:50:22 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
17:50:22 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:50:22 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
17:50:22 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
17:50:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 第一层并行=1, 第二层并行=0, 串行=1
17:50:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
17:50:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第10章的内容作为续写上下文
17:50:22 app.api.v1.agent INFO   [Stream] Task started: 获取第10章的内容作为续写上下文
17:50:22 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(get_chapter_by_order)
17:50:22 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 开始执行工具
17:50:22 app.services.agent.langgraph_tools INFO   [get_chapter_by_order_tool] ✅ 找到第10章: 第10章 吸收兽火
17:50:22 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 执行成功 (耗时: 0.124s)
17:50:22 app.services.agent.langgraph_agent INFO   [StandardTool] get_chapter_by_order 执行成功（DeepAgent模式）
17:50:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
17:50:22 app.api.v1.agent INFO   [Stream] 任务完成: 获取第10章的内容作为续写上下文 (0.1s)
17:50:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行1个任务
17:50:22 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 续写第10章后续内容
17:50:23 app.api.v1.agent INFO   [Stream] Task started: 续写第10章后续内容
17:50:23 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
17:50:23 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
17:50:23 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
17:50:23 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
17:50:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
17:50:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:50:57 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 576
17:50:57 app.services.ai.http_ai_service INFO   流式响应Token统计: 5228 (prompt=4783, completion=445)
17:50:57 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:50:57 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:50:57 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5228, cost=$0.010429, time=34003ms
17:50:57 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 34.051s)
17:50:57 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
17:50:57 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
17:50:57 app.api.v1.agent INFO   [Stream] 任务完成: 续写第10章后续内容 (34.1s)
17:50:57 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 34.21s
17:50:57 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:50:57 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
17:50:57 app.services.agent.langgraph_agent INFO   [Response] 单个创作任务(continue_writing_tool)，输出576字符，直接返回（跳过AI调用）
17:50:57 app.services.context.vector_memory_store INFO   🔁 跳过重复记忆，复用ID=602f5147-846a-4cde-95d3-405fa75f133f_1765791164826_e37f920b
17:50:57 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.84
17:50:57 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.58
17:50:57 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, token=394
17:50:57 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, 消息数=2, Token=394
17:50:57 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66)
17:50:57 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
17:50:57 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
INFO:     connection closed
17:52:50 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:52:50 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:52:50 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
17:52:54 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:52:54 app.api.v1.agent INFO   [Chat Stream] Mode: planning
17:52:54 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61777 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:52:54 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请帮我润色以下段落，让描写更加生动细腻：

"萧凌缓缓睁开双眼，感受着体内比三天前磅礴一些的斗气，心...
17:52:54 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
17:52:54 app.api.v1.agent INFO     - selected_text: N/A...
17:52:54 app.api.v1.agent INFO     - selection_position: N/A
17:52:54 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 9578da5d-3109-49b7-aa04-807fb36d31f3...
17:52:54 app.api.v1.agent INFO     - instruction_context: N/A...
17:52:54 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=55a1a141-c158-4818-8422-900eaa938d66)
17:52:54 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, 2条消息
17:52:54 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66: 394/16000 tokens
17:52:54 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请帮我润色以下段落，让描写更加生动细腻：

"萧凌缓缓睁开双...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=1条
17:52:54 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=1条
17:52:54 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 394 tokens, 耗时 119.45ms
17:52:54 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 394)
17:52:54 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请帮我润色以下段落，让描写更加生动细腻：

"萧凌缓缓睁开双眼，感受着体内比三天前磅礴一些的斗气，心...
17:52:54 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
17:52:54 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:52:54 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:52:54 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
17:52:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
INFO:     connection closed
INFO:     connection closed
17:53:03 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 1032
17:53:03 app.services.ai.http_ai_service INFO   流式响应Token统计: 8326 (prompt=7807, completion=519)
17:53:03 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:53:03 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:53:03 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8326, cost=$0.014949, time=8670ms
17:53:03 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8326
17:53:03 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
17:53:03 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到对指定段落的润色和改写，使其更加生动细腻，包含环, 原料=需要用户提供的待润色段落，以及该段落所属, 处理=首先读取指定章节的上下文内容，然后使用
17:53:03 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 8.80s
17:53:03 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
17:53:03 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:53:03 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
17:53:03 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
17:53:03 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
17:53:03 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
17:53:03 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
17:53:03 app.api.v1.agent INFO   [Stream] Task started: 读取第9578da5d-3109-49b7-aa04-807fb36d31f3章节内容以获取上下文
17:53:03 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(read_chapter)
17:53:03 app.services.agent.tools.tool_types INFO   [read_chapter] 开始执行工具
17:53:03 app.services.agent.langgraph_tools INFO   [read_chapter_tool] ✅ 读取章节成功: 第10章 吸收兽火
17:53:03 app.services.agent.tools.tool_types INFO   [read_chapter] 执行成功 (耗时: 0.060s)
17:53:03 app.services.agent.langgraph_agent INFO   [StandardTool] read_chapter 执行成功（DeepAgent模式）
17:53:03 app.api.v1.agent INFO   [Stream] 任务完成: 读取第9578da5d-3109-49b7-aa04-807fb36d31f3章节内容以获取上下文 (0.1s)
17:53:03 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
17:53:03 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
17:53:03 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
17:53:03 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:53:03 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:53:03 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
17:53:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:53:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 148
17:53:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 2994 (prompt=2923, completion=71)
17:53:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:53:17 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:53:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2994, cost=$0.004364, time=14077ms
17:53:17 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2994
17:53:17 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
17:53:17 app.api.v1.agent INFO   [Stream] Task started: 分析并润色用户提供的段落，加入环境描写和内心感受，提升文学性
17:53:17 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '分析原文并进行润色，加入清晨的环境描写，细化萧凌内心的满足感和对实力的感知，提升整体的文学性和画面感。...'
17:53:17 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
17:53:17 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
17:53:17 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
17:53:17 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:53:17 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:53:17 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
17:53:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:53:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 507
17:53:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 1734 (prompt=1368, completion=366)
17:53:26 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:53:26 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:53:26 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1734, cost=$0.005370, time=9246ms
17:53:26 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
17:53:26 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 507
17:53:26 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 9.301s)
17:53:26 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
17:53:26 app.api.v1.agent INFO   [Stream] 任务完成: 分析并润色用户提供的段落，加入环境描写和内心感受，提升文学性 (9.3s)
17:53:26 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:53:26 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:53:26 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:53:28 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:53:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:53:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 719 (prompt=718, completion=1)
17:53:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:53:31 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:53:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=719, cost=$0.000907, time=4259ms
17:53:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=719
17:53:31 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
17:53:31 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
17:53:31 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 27.85s
17:53:31 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:53:31 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=1
17:53:31 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
17:53:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
17:53:31 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=3296字符, 压缩后=3380字符, 压缩率=-2%
17:53:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
17:53:31 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
17:53:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:53:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:53:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
17:53:32 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:53:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 5 个数据块，总长度: 313
17:53:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 4451 (prompt=4224, completion=227)
17:53:41 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:53:41 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:53:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4451, cost=$0.007550, time=10225ms
17:53:41 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=313
17:53:42 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.84
17:53:43 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.73
17:53:43 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, token=630
17:53:43 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, 消息数=4, Token=630
17:53:43 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66)
17:53:43 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
17:53:43 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
17:54:47 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:54:47 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:54:47 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
17:54:51 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:54:51 app.api.v1.agent INFO   [Chat Stream] Mode: planning
17:54:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51076 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:54:51 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 根据目前的故事发展（第10章萧凌即将前往迦南学院），请帮我规划接下来3章的大纲：
1. 第11章：萧...
17:54:51 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
17:54:51 app.api.v1.agent INFO     - selected_text: N/A...
17:54:51 app.api.v1.agent INFO     - selection_position: N/A
17:54:51 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 9578da5d-3109-49b7-aa04-807fb36d31f3...
17:54:51 app.api.v1.agent INFO     - instruction_context: N/A...
17:54:51 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=55a1a141-c158-4818-8422-900eaa938d66)
17:54:51 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, 4条消息
17:54:51 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66: 630/16000 tokens
17:54:52 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='根据目前的故事发展（第10章萧凌即将前往迦南学院），请帮我规...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=2条
17:54:52 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=2条
17:54:52 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 5条消息, 630 tokens, 耗时 438.68ms
17:54:52 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 630)
17:54:52 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 根据目前的故事发展（第10章萧凌即将前往迦南学院），请帮我规划接下来3章的大纲：
1. 第11章：萧...
17:54:52 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
17:54:52 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:54:52 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:54:52 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
17:54:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:02 app.services.ai.http_ai_service INFO   API 响应完成，共接收 0 个数据块，总长度: 0
17:55:02 app.services.ai.http_ai_service INFO   流式响应Token统计: 7200 (prompt=7200, completion=0)
17:55:02 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:02 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:02 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7200, cost=$0.009000, time=10007ms
17:55:02 app.services.ai.http_ai_service ERROR   警告: AI 响应为空！未接收到任何内容块。
17:55:02 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7200
17:55:02 app.services.agent.langgraph_agent ERROR   [JSON解析] 输入文本为空
17:55:02 app.services.agent.langgraph_agent WARNING   [Planning] 无法解析规划JSON，AI返回:
17:55:02 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 10.05s
17:55:02 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
17:55:02 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:55:02 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
17:55:02 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
17:55:02 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
17:55:02 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
17:55:02 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
17:55:02 app.api.v1.agent INFO   [Stream] Task started: 理解用户意图并获取相关上下文
17:55:02 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(get_context)
17:55:02 app.services.agent.tools.tool_types INFO   [get_context] 开始执行工具
17:55:02 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=10, query=作品背景、人物关系、情节发展、伏笔线索...
17:55:02 app.services.chapter_vector_service INFO   RAG retrieved 5 segments within order<=10
17:55:02 app.services.agent.langgraph_tools INFO   [get_context_tool] ✅ 获取上下文成功
17:55:02 app.services.agent.tools.tool_types INFO   [get_context] 执行成功 (耗时: 0.305s)
17:55:02 app.services.agent.langgraph_agent INFO   [StandardTool] get_context 执行成功（DeepAgent模式）
17:55:02 app.api.v1.agent INFO   [Stream] 任务完成: 理解用户意图并获取相关上下文 (0.3s)
17:55:02 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 任务 1 标记了 checkpoint，触发反思
17:55:02 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
17:55:02 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:55:02 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:55:02 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:55:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:55:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 486 (prompt=485, completion=1)
17:55:05 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:05 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=486, cost=$0.000616, time=3094ms
17:55:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=486
17:55:05 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
17:55:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:55:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:55:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
17:55:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:12 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 109
17:55:12 app.services.ai.http_ai_service INFO   流式响应Token统计: 1635 (prompt=1586, completion=49)
17:55:12 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:12 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:12 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1635, cost=$0.002472, time=6609ms
17:55:12 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1635
17:55:12 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
17:55:12 app.api.v1.agent INFO   [Stream] Task started: 基于上下文响应用户请求
17:55:12 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '根据用户请求进行分析或回答...'
17:55:12 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
17:55:12 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
17:55:12 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
17:55:12 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:55:12 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:55:12 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
17:55:14 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:21 app.services.ai.http_ai_service INFO   API 响应完成，共接收 3 个数据块，总长度: 233
17:55:21 app.services.ai.http_ai_service INFO   流式响应Token统计: 4490 (prompt=4322, completion=168)
17:55:21 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:21 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:21 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4490, cost=$0.007083, time=9106ms
17:55:21 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
17:55:21 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 233
17:55:21 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 9.137s)
17:55:21 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
17:55:21 app.api.v1.agent INFO   [Stream] 任务完成: 基于上下文响应用户请求 (9.1s)
17:55:21 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:55:21 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:55:21 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:55:23 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:25 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:55:25 app.services.ai.http_ai_service INFO   流式响应Token统计: 410 (prompt=409, completion=1)
17:55:25 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:25 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:25 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=410, cost=$0.000521, time=3442ms
17:55:25 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=410
17:55:25 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:55:25 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:55:25 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:55:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:28 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:55:28 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
17:55:28 app.services.ai.http_ai_service INFO   流式响应Token统计: 709 (prompt=708, completion=1)
17:55:28 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:28 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:28 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=709, cost=$0.000895, time=3726ms
17:55:28 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=709
17:55:28 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
17:55:28 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
17:55:28 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 26.46s
17:55:28 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:55:28 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
17:55:28 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
17:55:28 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
17:55:28 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=4895字符, 压缩后=4925字符, 压缩率=0%
17:55:28 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
17:55:28 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
17:55:28 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:55:28 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:55:28 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
17:55:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:55:46 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 1961
17:55:46 app.services.ai.http_ai_service INFO   流式响应Token统计: 6675 (prompt=5378, completion=1297)
17:55:46 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:55:46 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:55:46 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6675, cost=$0.019692, time=17587ms
17:55:46 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=1961
17:55:50 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=1.00
17:55:54 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.77
17:55:54 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, token=1764
17:55:54 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66, 消息数=6, Token=1764
17:55:54 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:55a1a141-c158-4818-8422-900eaa938d66)
17:55:54 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
17:55:54 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
17:58:45 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 05527755-20bb-46d3-850f-dc729f11eea3
17:58:45 app.api.v1.ai INFO   [预加载] 当前章节已加载: 05527755-20bb-46d3-850f-dc729f11eea3
17:58:45 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
17:58:45 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:58:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64411 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:58:45 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 05527755-20bb-46d3-850f-dc729f11eea3
17:58:45 app.api.v1.ai INFO   [预加载] 当前章节已加载: 05527755-20bb-46d3-850f-dc729f11eea3
17:58:45 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
17:58:45 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
17:58:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64414 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
17:58:45 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64417 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
17:58:46 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:58:46 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3
INFO:     127.0.0.1:64420 - "PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3 HTTP/1.1" 200 OK
17:58:46 app.services.chapter_vector_service INFO   Vectorizing chapter: 第50章 抵达加码 (order=50)
17:58:48 app.services.chapter_vector_service INFO   Stored chapter vectors: 第50章 抵达加码 (7 chunks)
17:58:48 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
17:58:48 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3
INFO:     127.0.0.1:52074 - "PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3 HTTP/1.1" 200 OK
17:58:48 app.services.chapter_vector_service INFO   Vectorizing chapter: 第50章 抵达加码 (order=50)
17:58:49 app.services.chapter_vector_service INFO   Stored chapter vectors: 第50章 抵达加码 (7 chunks)
17:58:51 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52077 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
17:58:51 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
17:58:51 app.services.ai.http_ai_service INFO   ModelSelector 已启用
17:58:51 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
17:58:54 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
17:58:54 app.api.v1.agent INFO   [Chat Stream] Mode: planning
17:58:54 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:52080 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
17:58:54 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请分析小说中萧凌这个角色的性格特点、行为动机和成长轨迹。需要结合具体情节进行分析，并与原著萧炎进行对...
17:58:54 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
17:58:54 app.api.v1.agent INFO     - selected_text: N/A...
17:58:54 app.api.v1.agent INFO     - selection_position: N/A
17:58:54 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 05527755-20bb-46d3-850f-dc729f11eea3...
17:58:54 app.api.v1.agent INFO     - instruction_context: N/A...
17:58:54 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=cd2a04ad-5e95-4b64-9864-51d0edbbdf74)
17:58:54 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74
17:58:54 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74: 0/16000 tokens
17:58:55 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请分析小说中萧凌这个角色的性格特点、行为动机和成长轨迹。需要...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
17:58:55 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
17:58:55 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 168.66ms
17:58:55 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
17:58:55 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请分析小说中萧凌这个角色的性格特点、行为动机和成长轨迹。需要结合具体情节进行分析，并与原著萧炎进行对...
17:58:55 app.core.cache INFO   ⚠️ 缓存未命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
17:58:55 app.core.cache INFO   ⚠️ 缓存未命中: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0
17:58:55 app.core.cache INFO   💾 缓存已保存: prompt:planning:v2.12.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
17:58:55 app.core.cache INFO   💾 缓存已保存: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0 (expire=3600s)
17:58:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:58:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:58:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
17:58:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:02 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 1302
17:59:02 app.services.ai.http_ai_service INFO   流式响应Token统计: 7475 (prompt=6850, completion=625)
17:59:02 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:02 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:02 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7475, cost=$0.014813, time=7689ms
17:59:02 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7475
17:59:02 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
17:59:02 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一份详细的分析报告，内容包括萧凌的性格特点、行为, 原料=需要获取小说中关于萧凌和萧炎的相关内容，, 处理=首先使用搜索工具查找关于萧凌和萧炎的关键
17:59:02 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 7.76s
17:59:02 app.api.v1.agent INFO   [Stream] Plan tasks: 3 items
17:59:02 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
17:59:02 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
17:59:02 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
17:59:02 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
17:59:02 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 3 个任务，反思功能已启用
17:59:02 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
17:59:02 app.api.v1.agent INFO   [Stream] Task started: 搜索关于萧凌的性格特点、行为动机和成长轨迹的相关内容
17:59:02 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(search_analysis_fragments)
17:59:02 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 开始执行工具
17:59:07 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=50, query=分析萧凌的性格特点、行为动机、成长轨迹...
17:59:08 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=52
Building prefix dict from the default dictionary ...
17:59:08 jieba DEBUG   Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
17:59:08 jieba DEBUG   Loading model from cache D:\Temp\jieba.cache
Loading model cost 3.021 seconds.
17:59:11 jieba DEBUG   Loading model cost 3.021 seconds.
Prefix dict has been built successfully.
17:59:11 jieba DEBUG   Prefix dict has been built successfully.
17:59:11 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
17:59:11 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 执行成功 (耗时: 8.284s)
17:59:11 app.services.agent.langgraph_agent INFO   [StandardTool] search_analysis_fragments 执行成功（DeepAgent模式）
17:59:11 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于萧凌的性格特点、行为动机和成长轨迹的相关内容 (8.3s)
17:59:11 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
17:59:11 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
17:59:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:59:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:59:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:59:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:14 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:59:14 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
17:59:14 app.services.ai.http_ai_service INFO   流式响应Token统计: 389 (prompt=388, completion=1)
17:59:14 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:14 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:14 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=389, cost=$0.000495, time=3631ms
17:59:14 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=389
17:59:14 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
17:59:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:59:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:59:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
17:59:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 111
17:59:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 1868 (prompt=1816, completion=52)
17:59:18 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:18 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1868, cost=$0.002790, time=4203ms
17:59:18 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1868
17:59:18 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
17:59:18 app.api.v1.agent INFO   [Stream] Task started: 搜索关于萧炎的性格特点、行为动机和成长轨迹的相关内容，用于对比
17:59:18 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(search_analysis_fragments)
17:59:18 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 开始执行工具
17:59:19 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=50, query=分析萧炎的性格特点、行为动机、成长轨迹...
17:59:19 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=52
17:59:19 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
17:59:19 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 执行成功 (耗时: 0.187s)
17:59:19 app.services.agent.langgraph_agent INFO   [StandardTool] search_analysis_fragments 执行成功（DeepAgent模式）
17:59:19 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于萧炎的性格特点、行为动机和成长轨迹的相关内容，用于对比 (0.2s)
17:59:19 app.api.v1.agent INFO   [Stream] Task started: 综合搜索结果，分析萧凌的性格特点、行为动机和成长轨迹，并与萧炎进行对比
17:59:19 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '分析萧凌的性格特点、行为动机和成长轨迹，并结合具体情节与原著萧炎进行对比分析。...'
17:59:19 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
17:59:19 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
17:59:19 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
17:59:19 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:59:19 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:59:19 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
17:59:21 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:32 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 838
17:59:32 app.services.ai.http_ai_service INFO   流式响应Token统计: 5304 (prompt=4682, completion=622)
17:59:32 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:32 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:32 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5304, cost=$0.012072, time=13745ms
17:59:32 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
17:59:32 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 838
17:59:32 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 13.796s)
17:59:32 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
17:59:32 app.api.v1.agent INFO   [Stream] 任务完成: 综合搜索结果，分析萧凌的性格特点、行为动机和成长轨迹，并与萧炎进行对比 (13.8s)
17:59:32 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:59:32 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:59:32 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:59:34 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:35 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:59:35 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
17:59:35 app.services.ai.http_ai_service INFO   流式响应Token统计: 410 (prompt=409, completion=1)
17:59:35 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:35 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:35 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=410, cost=$0.000521, time=2177ms
17:59:35 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=410
17:59:35 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:59:35 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:59:35 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:59:36 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:37 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:59:37 app.services.ai.http_ai_service INFO   流式响应Token统计: 371 (prompt=370, completion=1)
17:59:37 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:37 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:37 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=371, cost=$0.000473, time=2469ms
17:59:37 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=371
17:59:37 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
17:59:37 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
17:59:37 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
17:59:38 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:40 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
17:59:40 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
17:59:40 app.services.ai.http_ai_service INFO   流式响应Token统计: 414 (prompt=413, completion=1)
17:59:40 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:40 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:40 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=414, cost=$0.000526, time=2340ms
17:59:40 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=414
17:59:40 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=3, 反思=1, 重规划=0
17:59:40 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
17:59:40 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 37.26s
17:59:40 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
17:59:40 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
17:59:40 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
17:59:40 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
17:59:40 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=5703字符, 压缩后=5800字符, 压缩率=-1%
17:59:40 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
17:59:40 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
17:59:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
17:59:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
17:59:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
17:59:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
17:59:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 0 个数据块，总长度: 0
17:59:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 4377 (prompt=4377, completion=0)
17:59:48 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
17:59:49 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
17:59:49 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4377, cost=$0.005471, time=8935ms
17:59:49 app.services.ai.http_ai_service ERROR   警告: AI 响应为空！未接收到任何内容块。
17:59:49 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=0
17:59:50 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.89
17:59:50 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74, token=33
17:59:50 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74, 消息数=2, Token=33
17:59:50 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74)
17:59:50 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:00:26 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:00:26 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:00:26 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:00:29 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:00:29 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:00:29 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51178 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:00:29 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请分析这本小说的世界观设定，包括：
1. 修炼体系（斗之气→斗者→...）
2. 抽取系统的规则
3...
18:00:29 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:00:29 app.api.v1.agent INFO     - selected_text: N/A...
18:00:29 app.api.v1.agent INFO     - selection_position: N/A
18:00:29 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 05527755-20bb-46d3-850f-dc729f11eea3...
18:00:29 app.api.v1.agent INFO     - instruction_context: N/A...
18:00:29 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=cd2a04ad-5e95-4b64-9864-51d0edbbdf74)
18:00:29 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74, 2条消息
18:00:29 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74: 33/16000 tokens
18:00:29 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请分析这本小说的世界观设定，包括：
1. 修炼体系（斗之气→...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:00:29 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:00:29 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 33 tokens, 耗时 230.48ms
18:00:29 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 33)
18:00:29 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请分析这本小说的世界观设定，包括：
1. 修炼体系（斗之气→斗者→...）
2. 抽取系统的规则
3...
18:00:29 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:00:29 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:00:29 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:00:29 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:00:32 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:00:39 app.services.ai.http_ai_service INFO   API 响应完成，共接收 12 个数据块，总长度: 1353
18:00:39 app.services.ai.http_ai_service INFO   流式响应Token统计: 8017 (prompt=7273, completion=744)
18:00:39 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:00:39 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:00:39 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8017, cost=$0.016531, time=9512ms
18:00:39 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8017
18:00:39 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:00:39 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一份关于小说世界观设定的分析报告，内容需涵盖修炼, 原料=需要检索与小说世界观设定相关的文本片段，, 处理=首先，使用 `search_analys
18:00:39 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 9.55s
18:00:39 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
18:00:39 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:00:39 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:00:39 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:00:39 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:00:39 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
18:00:39 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:00:39 app.api.v1.agent INFO   [Stream] Task started: 检索小说中关于修炼体系、系统抽取规则、与《斗破苍穹》的异同点以及关键道具（焚诀、聚气散、二十四桥明月夜）作用的相关文本片段。
18:00:39 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(search_analysis_fragments)
18:00:39 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 开始执行工具
18:00:39 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=50, query=分析小说世界观：修炼体系（斗之气→斗者等阶）、系统抽取规则、与原著《斗破苍穹》的异同点、关键道具（焚...
18:00:39 app.services.chapter_vector_service INFO   RAG retrieved 10 segments within order<=52
18:00:39 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
18:00:39 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 执行成功 (耗时: 0.086s)
18:00:39 app.services.agent.langgraph_agent INFO   [StandardTool] search_analysis_fragments 执行成功（DeepAgent模式）
18:00:39 app.api.v1.agent INFO   [Stream] 任务完成: 检索小说中关于修炼体系、系统抽取规则、与《斗破苍穹》的异同点以及关键道具（焚诀、聚气散、二十四桥明月夜）作用的相关文本片段。 (0.1s)
18:00:39 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:00:39 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:00:39 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:00:39 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:00:39 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:00:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:00:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:00:43 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
18:00:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 902 (prompt=901, completion=1)
18:00:43 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:00:43 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:00:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=902, cost=$0.001136, time=4635ms
18:00:43 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=902
18:00:43 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:00:43 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:00:43 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:00:43 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:00:45 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:00:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 113
18:00:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 1944 (prompt=1889, completion=55)
18:00:47 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:00:48 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:00:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1944, cost=$0.002911, time=4178ms
18:00:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1944
18:00:48 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:00:48 app.api.v1.agent INFO   [Stream] Task started: 根据检索到的文本片段，分析并总结小说的世界观设定，重点阐述修炼体系、系统抽取规则、与《斗破苍穹》的异同点以及关键道具的作用。
18:00:48 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '请根据提供的文本片段，详细分析以下四个方面：1. 修炼体系（从斗之气到斗者及后续等级的设定）；2. 抽取系统的具体规则和条件；3. 与原著《斗破苍穹》在世界观、...'
18:00:48 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
18:00:48 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
18:00:48 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
18:00:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:00:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:00:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:00:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:00:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 920
18:00:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 3519 (prompt=2885, completion=634)
18:00:59 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:00:59 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:00:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3519, cost=$0.009946, time=11390ms
18:00:59 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
18:00:59 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 920
18:00:59 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 11.439s)
18:00:59 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
18:00:59 app.api.v1.agent INFO   [Stream] 任务完成: 根据检索到的文本片段，分析并总结小说的世界观设定，重点阐述修炼体系、系统抽取规则、与《斗破苍穹》的异同点以及关键道具的作用。 (11.4s)
18:00:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:00:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:00:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:01:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:01:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:01:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 952 (prompt=951, completion=1)
18:01:08 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:01:08 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:01:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=952, cost=$0.001199, time=8627ms
18:01:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=952
18:01:08 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:01:08 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:01:08 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:01:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:01:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:01:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 784 (prompt=783, completion=1)
18:01:11 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:01:11 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:01:11 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=784, cost=$0.000989, time=3448ms
18:01:11 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=784
18:01:11 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
18:01:11 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:01:11 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 32.53s
18:01:11 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:01:11 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
18:01:11 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
18:01:11 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
18:01:11 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=2917字符, 压缩后=3046字符, 压缩率=-4%
18:01:11 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
18:01:11 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
18:01:11 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:01:11 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:01:11 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
18:01:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:01:15 app.services.ai.http_ai_service INFO   API 响应完成，共接收 0 个数据块，总长度: 0
18:01:15 app.services.ai.http_ai_service INFO   流式响应Token统计: 2218 (prompt=2218, completion=0)
18:01:15 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:01:15 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:01:15 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2218, cost=$0.002772, time=3728ms
18:01:15 app.services.ai.http_ai_service ERROR   警告: AI 响应为空！未接收到任何内容块。
18:01:15 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=0
18:01:16 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=1.00
18:01:16 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74, token=81
18:01:16 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74, 消息数=4, Token=81
18:01:16 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:cd2a04ad-5e95-4b64-9864-51d0edbbdf74)
18:01:16 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:02:02 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:02:02 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:02:02 app.api.v1.ai INFO   [预加载] 前一章节已加载: d9924a45-250a-4c28-8500-38e519cc1348
18:02:02 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:02:02 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
18:02:02 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 0674f1e7-821b-4684-9c89-eca564ec71b4
INFO:     127.0.0.1:52306 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:02:02 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:02:02 app.api.v1.ai INFO   [预加载] 前一章节已加载: d9924a45-250a-4c28-8500-38e519cc1348
18:02:02 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:02:02 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52309 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:02:02 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:52313 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
18:02:02 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:02:02 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4
INFO:     127.0.0.1:52316 - "PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4 HTTP/1.1" 200 OK
18:02:02 app.services.chapter_vector_service INFO   Vectorizing chapter: 第49章 飞行路途 (order=49)
18:02:04 app.services.chapter_vector_service INFO   Stored chapter vectors: 第49章 飞行路途 (6 chunks)
18:02:04 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:02:04 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4
INFO:     127.0.0.1:52319 - "PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4 HTTP/1.1" 200 OK
18:02:04 app.services.chapter_vector_service INFO   Vectorizing chapter: 第49章 飞行路途 (order=49)
18:02:06 app.services.chapter_vector_service INFO   Stored chapter vectors: 第49章 飞行路途 (6 chunks)
18:02:07 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:65292 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
18:02:07 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:02:07 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:02:07 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:02:10 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:02:10 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:02:10 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:65295 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:02:10 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 我在写萧凌和萧薰儿感情线的时候卡住了，不知道怎么让两人的感情发展更自然。目前他们已经是青梅竹马、互有...
18:02:10 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:02:10 app.api.v1.agent INFO     - selected_text: N/A...
18:02:10 app.api.v1.agent INFO     - selection_position: N/A
18:02:10 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 0674f1e7-821b-4684-9c89-eca564ec71b4...
18:02:10 app.api.v1.agent INFO     - instruction_context: N/A...
18:02:10 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=4ac544e4-f1c3-43bc-898d-e675fc9a015f)
18:02:10 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f
18:02:10 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f: 0/16000 tokens
18:02:10 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='我在写萧凌和萧薰儿感情线的时候卡住了，不知道怎么让两人的感情...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:02:10 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:02:10 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 265.66ms
18:02:10 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
18:02:10 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 我在写萧凌和萧薰儿感情线的时候卡住了，不知道怎么让两人的感情发展更自然。目前他们已经是青梅竹马、互有...
18:02:10 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:02:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:02:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:02:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:02:13 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:02:23 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 692
18:02:23 app.services.ai.http_ai_service INFO   流式响应Token统计: 7828 (prompt=7490, completion=338)
18:02:23 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:02:23 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:02:23 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7828, cost=$0.012742, time=12240ms
18:02:23 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7828
18:02:23 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:02:23 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户需要创作建议，以生成一个更有冲击力、更自然的表白场景。这, 原料=用户提供了当前人物关系（青梅竹马、互有好, 处理=使用 `continue_writing
18:02:23 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 12.29s
18:02:23 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
18:02:23 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:02:23 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:02:23 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:02:23 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:02:23 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
18:02:23 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:02:23 app.api.v1.agent INFO   [Stream] Task started: 构思萧凌和萧薰儿的表白场景
18:02:23 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
18:02:23 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
18:02:23 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
18:02:23 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
18:02:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
18:02:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:02:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 577
18:02:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 2580 (prompt=2119, completion=461)
18:02:53 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:02:53 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:02:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2580, cost=$0.007259, time=30814ms
18:02:53 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 30.841s)
18:02:53 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
18:02:53 app.api.v1.agent INFO   [Stream] 任务完成: 构思萧凌和萧薰儿的表白场景 (30.8s)
18:02:53 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:02:53 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:02:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:02:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:02:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:02:55 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:02:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:02:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 358 (prompt=357, completion=1)
18:02:56 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:02:56 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:02:56 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=358, cost=$0.000456, time=2354ms
18:02:56 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=358
18:02:56 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:02:56 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:02:56 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:02:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:03:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:03:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 138
18:03:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 1886 (prompt=1814, completion=72)
18:03:06 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:03:06 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:03:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1886, cost=$0.002988, time=9862ms
18:03:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1886
18:03:06 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:03:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:03:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:03:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:03:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:03:08 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:03:08 app.services.ai.http_ai_service INFO   流式响应Token统计: 326 (prompt=325, completion=1)
18:03:08 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:03:08 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:03:08 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=326, cost=$0.000416, time=2266ms
18:03:08 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=326
18:03:08 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
18:03:08 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:03:08 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 45.39s
18:03:08 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:03:08 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
18:03:08 app.services.agent.langgraph_agent INFO   [Response] 单个创作任务(continue_writing_tool)，输出577字符，直接返回（跳过AI调用）
18:03:08 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.58
18:03:08 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f, token=389
18:03:08 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f, 消息数=2, Token=389
18:03:08 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f)
18:03:08 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
18:03:08 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:03:31 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: f941b6e3-3fa3-4b6d-b31f-05a6bbc22254
18:03:31 app.api.v1.ai INFO   [预加载] 当前章节已加载: f941b6e3-3fa3-4b6d-b31f-05a6bbc22254
18:03:31 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: f941b6e3-3fa3-4b6d-b31f-05a6bbc22254
18:03:31 app.api.v1.ai INFO   [预加载] 前一章节已加载: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
18:03:31 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:03:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
18:03:31 app.api.v1.ai INFO   [预加载] 当前章节已加载: f941b6e3-3fa3-4b6d-b31f-05a6bbc22254
18:03:31 app.api.v1.ai INFO   [预加载] 前一章节已加载: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
18:03:31 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:54637 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:03:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54640 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:03:31 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54643 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
18:03:32 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:03:32 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f941b6e3-3fa3-4b6d-b31f-05a6bbc22254
INFO:     127.0.0.1:61242 - "PUT /api/v1/chapters/f941b6e3-3fa3-4b6d-b31f-05a6bbc22254 HTTP/1.1" 200 OK
18:03:32 app.services.chapter_vector_service INFO   Vectorizing chapter: 第5章 黑铁片 (order=5)
18:03:33 app.services.chapter_vector_service INFO   Stored chapter vectors: 第5章 黑铁片 (5 chunks)
18:03:33 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:03:33 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/f941b6e3-3fa3-4b6d-b31f-05a6bbc22254
INFO:     127.0.0.1:61245 - "PUT /api/v1/chapters/f941b6e3-3fa3-4b6d-b31f-05a6bbc22254 HTTP/1.1" 200 OK
18:03:33 app.services.chapter_vector_service INFO   Vectorizing chapter: 第5章 黑铁片 (order=5)
18:03:35 app.services.chapter_vector_service INFO   Stored chapter vectors: 第5章 黑铁片 (5 chunks)
18:03:37 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53538 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
18:03:37 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:03:37 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:03:37 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:03:39 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:03:39 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:03:39 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:53541 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:03:39 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请分析小说中萧凌这个角色的性格特点、行为动机和成长轨迹。需要结合具体情节进行分析，并与原著萧炎进行对...
18:03:39 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:03:39 app.api.v1.agent INFO     - selected_text: N/A...
18:03:39 app.api.v1.agent INFO     - selection_position: N/A
18:03:39 app.api.v1.agent INFO     - chapter_context: 当前章节ID: f941b6e3-3fa3-4b6d-b31f-05a6bbc22254...
18:03:39 app.api.v1.agent INFO     - instruction_context: N/A...
18:03:39 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:ccd98eb3-b988-457c-b084-dd22a30aeddf (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=ccd98eb3-b988-457c-b084-dd22a30aeddf)
18:03:39 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:ccd98eb3-b988-457c-b084-dd22a30aeddf
18:03:39 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:ccd98eb3-b988-457c-b084-dd22a30aeddf: 0/16000 tokens
18:03:40 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请分析小说中萧凌这个角色的性格特点、行为动机和成长轨迹。需要...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:03:40 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:03:40 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 154.35ms
18:03:40 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
18:03:40 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请分析小说中萧凌这个角色的性格特点、行为动机和成长轨迹。需要结合具体情节进行分析，并与原著萧炎进行对...
18:03:40 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:03:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:03:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:03:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:03:42 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:03:55 app.services.ai.http_ai_service INFO   API 响应完成，共接收 14 个数据块，总长度: 1371
18:03:55 app.services.ai.http_ai_service INFO   流式响应Token统计: 9646 (prompt=9014, completion=632)
18:03:55 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:03:55 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:03:55 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9646, cost=$0.017587, time=15240ms
18:03:55 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=9646
18:03:55 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:03:55 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一份详细的分析报告，内容包括萧凌的性格特点、行为, 原料=需要关于萧凌和萧炎这两个角色的详细信息，, 处理=首先使用search_analysis_
18:03:55 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 15.29s
18:03:55 app.api.v1.agent INFO   [Stream] Plan tasks: 3 items
18:03:55 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:03:55 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:03:55 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:03:55 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:03:55 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 3 个任务，反思功能已启用
18:03:55 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:03:55 app.api.v1.agent INFO   [Stream] Task started: 搜索关于萧凌的性格特点、行为动机、成长轨迹及相关情节信息
18:03:55 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(search_analysis_fragments)
18:03:55 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 开始执行工具
18:03:55 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=5, query=萧凌 性格特点 行为动机 成长轨迹 具体情节...
18:03:55 app.services.chapter_vector_service INFO   RAG retrieved 20 segments within order<=7
18:03:55 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到10个片段
18:03:55 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 执行成功 (耗时: 0.247s)
18:03:55 app.services.agent.langgraph_agent INFO   [StandardTool] search_analysis_fragments 执行成功（DeepAgent模式）
18:03:55 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于萧凌的性格特点、行为动机、成长轨迹及相关情节信息 (0.2s)
18:03:55 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:03:55 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:03:55 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:03:55 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:03:55 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:03:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:03:59 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:03:59 app.services.ai.http_ai_service INFO   流式响应Token统计: 569 (prompt=568, completion=1)
18:03:59 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:03:59 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:03:59 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=569, cost=$0.000720, time=3536ms
18:03:59 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=569
18:03:59 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:03:59 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:03:59 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:03:59 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:04:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:04:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 98
18:04:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 1866 (prompt=1824, completion=42)
18:04:05 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:04:05 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:04:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1866, cost=$0.002700, time=5852ms
18:04:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1866
18:04:05 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:04:05 app.api.v1.agent INFO   [Stream] Task started: 搜索关于原著萧炎的性格特点、行为动机、成长轨迹及相关情节信息，用于对比
18:04:05 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(search_analysis_fragments)
18:04:05 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 开始执行工具
18:04:05 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=5, query=萧炎 性格特点 行为动机 成长轨迹 具体情节...
18:04:05 app.services.chapter_vector_service INFO   RAG retrieved 20 segments within order<=7
18:04:05 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到10个片段
18:04:05 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 执行成功 (耗时: 0.091s)
18:04:05 app.services.agent.langgraph_agent INFO   [StandardTool] search_analysis_fragments 执行成功（DeepAgent模式）
18:04:05 app.api.v1.agent INFO   [Stream] 任务完成: 搜索关于原著萧炎的性格特点、行为动机、成长轨迹及相关情节信息，用于对比 (0.1s)
18:04:05 app.api.v1.agent INFO   [Stream] Task started: 综合搜索结果，分析萧凌的性格特点、行为动机和成长轨迹，并与萧炎进行对比
18:04:05 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '结合提供的关于萧凌和萧炎的信息，分析萧凌的性格特点、行为动机和成长轨迹，并与原著萧炎进行详细对比，引用具体情节进行阐述。...'
18:04:05 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
18:04:05 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
18:04:05 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
18:04:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:04:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:04:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:04:10 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:04:22 app.services.ai.http_ai_service INFO   API 响应完成，共接收 7 个数据块，总长度: 527
18:04:22 app.services.ai.http_ai_service INFO   流式响应Token统计: 8644 (prompt=8235, completion=409)
18:04:22 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:04:22 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:04:22 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8644, cost=$0.014384, time=17087ms
18:04:22 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
18:04:22 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 527
18:04:22 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 17.129s)
18:04:22 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
18:04:22 app.api.v1.agent INFO   [Stream] 任务完成: 综合搜索结果，分析萧凌的性格特点、行为动机和成长轨迹，并与萧炎进行对比 (17.1s)
18:04:22 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:04:22 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:04:22 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:04:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:04:25 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:04:25 app.services.ai.http_ai_service INFO   流式响应Token统计: 548 (prompt=547, completion=1)
18:04:25 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:04:25 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:04:25 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=548, cost=$0.000694, time=3497ms
18:04:25 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=548
18:04:25 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:04:25 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:04:25 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:04:27 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:04:29 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:04:29 app.services.ai.http_ai_service WARNING   [Token估算] API返回completion_tokens=0，使用TokenCounter估算: 1 tokens (内容4字符)
18:04:29 app.services.ai.http_ai_service INFO   流式响应Token统计: 451 (prompt=450, completion=1)
18:04:29 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:04:29 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:04:29 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=451, cost=$0.000572, time=3103ms
18:04:29 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=451
18:04:29 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:04:29 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:04:29 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:04:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:04:31 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:04:31 app.services.ai.http_ai_service INFO   流式响应Token统计: 434 (prompt=433, completion=1)
18:04:31 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:04:31 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:04:31 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=434, cost=$0.000551, time=2526ms
18:04:31 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=434
18:04:31 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=3, 反思=1, 重规划=0
18:04:31 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:04:31 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 36.15s
18:04:31 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:04:31 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=2, 输出型=1, 展示型=0
18:04:31 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
18:04:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
18:04:31 app.services.agent.utils.context_builder INFO   [Compress] 任务2工具'search_analysis_fragments_tool'，内容长度5571，保留4000字符（省略1571字符）
18:04:31 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=9977字符, 压缩后=4478字符, 压缩率=56%
18:04:31 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
18:04:31 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
18:04:31 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:04:31 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:04:31 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
18:04:33 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:04:42 app.services.ai.http_ai_service INFO   API 响应完成，共接收 20 个数据块，总长度: 1358
18:04:42 app.services.ai.http_ai_service INFO   流式响应Token统计: 5276 (prompt=4309, completion=967)
18:04:42 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:04:42 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:04:42 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5276, cost=$0.015056, time=10873ms
18:04:42 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=1358
18:04:42 app.services.context.vector_memory_store INFO   🔁 跳过重复记忆，复用ID=602f5147-846a-4cde-95d3-405fa75f133f_1765792789002_de0c31a9
18:04:42 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.89
18:04:46 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.91
18:04:46 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:ccd98eb3-b988-457c-b084-dd22a30aeddf, token=790
18:04:46 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:ccd98eb3-b988-457c-b084-dd22a30aeddf, 消息数=2, Token=790
18:04:46 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:ccd98eb3-b988-457c-b084-dd22a30aeddf)
18:04:46 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
18:04:46 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:05:38 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
18:05:38 app.api.v1.ai INFO   [预加载] 当前章节已加载: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
18:05:38 app.api.v1.ai INFO   [预加载] 前一章节已加载: e32ba0f9-3886-4b79-93fc-dfa1b16102fe
18:05:38 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:05:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50365 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:05:38 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
18:05:38 app.api.v1.ai INFO   [预加载] 当前章节已加载: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
18:05:38 app.api.v1.ai INFO   [预加载] 前一章节已加载: e32ba0f9-3886-4b79-93fc-dfa1b16102fe
18:05:38 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:05:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
18:05:38 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50369 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:50371 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
18:05:39 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:05:39 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
INFO:     127.0.0.1:50374 - "PUT /api/v1/chapters/eb327c02-9b4f-4e5a-a553-1cf0c500a8d2 HTTP/1.1" 200 OK
18:05:39 app.services.chapter_vector_service INFO   Vectorizing chapter: 第7章 《弄炎决》 (order=7)
18:05:41 app.services.chapter_vector_service INFO   Stored chapter vectors: 第7章 《弄炎决》 (5 chunks)
18:05:41 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:05:41 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
INFO:     127.0.0.1:50377 - "PUT /api/v1/chapters/eb327c02-9b4f-4e5a-a553-1cf0c500a8d2 HTTP/1.1" 200 OK
18:05:41 app.services.chapter_vector_service INFO   Vectorizing chapter: 第7章 《弄炎决》 (order=7)
18:05:42 app.services.chapter_vector_service INFO   Stored chapter vectors: 第7章 《弄炎决》 (5 chunks)
18:05:44 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58081 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
18:05:44 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:05:44 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:05:44 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:05:47 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:05:47 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:05:47 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58084 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:05:47 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请分析这本小说的世界观设定，包括：
1. 修炼体系（斗之气→斗者→...）
2. 抽取系统的规则
3...
18:05:47 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:05:47 app.api.v1.agent INFO     - selected_text: N/A...
18:05:47 app.api.v1.agent INFO     - selection_position: N/A
18:05:47 app.api.v1.agent INFO     - chapter_context: 当前章节ID: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2...
18:05:47 app.api.v1.agent INFO     - instruction_context: N/A...
18:05:47 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:8856fabe-420f-4b0f-8eb3-2cf6a3551a5d (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=8856fabe-420f-4b0f-8eb3-2cf6a3551a5d)
18:05:47 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:8856fabe-420f-4b0f-8eb3-2cf6a3551a5d
18:05:47 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:8856fabe-420f-4b0f-8eb3-2cf6a3551a5d: 0/16000 tokens
18:05:47 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请分析这本小说的世界观设定，包括：
1. 修炼体系（斗之气→...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:05:47 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:05:47 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 186.37ms
18:05:47 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
18:05:47 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请分析这本小说的世界观设定，包括：
1. 修炼体系（斗之气→斗者→...）
2. 抽取系统的规则
3...
18:05:47 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:05:47 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:05:47 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:05:47 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:05:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:02 app.services.ai.http_ai_service INFO   API 响应完成，共接收 12 个数据块，总长度: 1441
18:06:02 app.services.ai.http_ai_service INFO   流式响应Token统计: 8965 (prompt=8210, completion=755)
18:06:02 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:02 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:02 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8965, cost=$0.017813, time=14933ms
18:06:02 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8965
18:06:02 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:06:02 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到一份关于小说世界观设定的分析报告，详细解答关于修, 原料=需要找到小说中描述修炼体系、抽取系统规则, 处理=1. 使用 `search_analys
18:06:02 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共2个任务，耗时: 14.98s
18:06:02 app.api.v1.agent INFO   [Stream] Plan tasks: 2 items
18:06:02 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:06:02 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:06:02 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:06:02 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:06:02 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 2 个任务，反思功能已启用
18:06:02 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:06:02 app.api.v1.agent INFO   [Stream] Task started: 检索与小说世界观设定相关的文本片段，涵盖修炼体系、抽取系统、与原著对比及关键道具。
18:06:02 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(search_analysis_fragments)
18:06:02 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 开始执行工具
18:06:02 app.services.chapter_vector_service INFO   RAG retrieve work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, current_order=7, query=修炼体系 斗之气 斗者 等级 境界 晋升 抽取系统 规则 机制 运作 斗破苍穹 原著 异同点 不同 ...
18:06:03 app.services.chapter_vector_service INFO   RAG retrieved 20 segments within order<=9
18:06:03 app.services.agent.langgraph_tools INFO   [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到10个片段
18:06:03 app.services.agent.tools.tool_types INFO   [search_analysis_fragments] 执行成功 (耗时: 0.525s)
18:06:03 app.services.agent.langgraph_agent INFO   [StandardTool] search_analysis_fragments 执行成功（DeepAgent模式）
18:06:03 app.api.v1.agent INFO   [Stream] 任务完成: 检索与小说世界观设定相关的文本片段，涵盖修炼体系、抽取系统、与原著对比及关键道具。 (0.5s)
18:06:03 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:06:03 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:06:03 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:06:03 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:06:03 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:06:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:06:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 542 (prompt=541, completion=1)
18:06:05 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:05 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=542, cost=$0.000686, time=2758ms
18:06:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=542
18:06:05 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:06:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:06:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:06:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:06:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 137
18:06:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 2007 (prompt=1940, completion=67)
18:06:10 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:10 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2007, cost=$0.003095, time=4306ms
18:06:10 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2007
18:06:10 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:06:10 app.api.v1.agent INFO   [Stream] Task started: 根据检索到的文本内容，分析小说的修炼体系、抽取系统规则、与原著《斗破苍穹》的异同点以及关键道具作用。
18:06:10 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '请根据提供的文本内容，详细分析以下四个方面：
1. 小说的修炼体系（包括从斗之气到斗者的晋升过程及后续等级）。
2. 抽取系统的具体规则和运作机制。
3. 本小...'
18:06:10 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
18:06:10 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
18:06:10 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
18:06:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:06:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:06:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:06:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:20 app.services.ai.http_ai_service INFO   API 响应完成，共接收 10 个数据块，总长度: 890
18:06:20 app.services.ai.http_ai_service INFO   流式响应Token统计: 4437 (prompt=3834, completion=603)
18:06:20 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:20 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:20 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4437, cost=$0.010823, time=10008ms
18:06:20 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
18:06:20 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 890
18:06:20 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 10.031s)
18:06:20 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
18:06:20 app.api.v1.agent INFO   [Stream] 任务完成: 根据检索到的文本内容，分析小说的修炼体系、抽取系统规则、与原著《斗破苍穹》的异同点以及关键道具作用。 (10.0s)
18:06:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:06:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:06:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:06:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:23 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:06:23 app.services.ai.http_ai_service INFO   流式响应Token统计: 592 (prompt=591, completion=1)
18:06:23 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:23 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:23 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=592, cost=$0.000749, time=2949ms
18:06:23 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=592
18:06:23 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:06:23 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:06:23 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:06:24 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:06:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 581 (prompt=580, completion=1)
18:06:26 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:26 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:26 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=581, cost=$0.000735, time=3244ms
18:06:26 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=581
18:06:26 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=2, 反思=1, 重规划=0
18:06:26 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:06:26 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共2个任务，耗时: 23.94s
18:06:26 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:06:26 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=1, 展示型=0
18:06:26 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(analyze_text_tool)，使用AI格式化
18:06:26 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
18:06:26 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=4789字符, 压缩后=4885字符, 压缩率=-2%
18:06:26 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
18:06:26 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
18:06:26 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:06:26 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:06:26 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
18:06:28 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:06:38 app.services.ai.http_ai_service INFO   API 响应完成，共接收 16 个数据块，总长度: 1145
18:06:38 app.services.ai.http_ai_service INFO   流式响应Token统计: 5572 (prompt=4833, completion=739)
18:06:38 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:06:38 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:06:38 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5572, cost=$0.013431, time=11574ms
18:06:38 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=1145
18:06:38 app.services.context.vector_memory_store INFO   🔁 跳过重复记忆，复用ID=602f5147-846a-4cde-95d3-405fa75f133f_1765792875343_f1edbcf7
18:06:38 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=1.00
18:06:38 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.73
18:06:38 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:8856fabe-420f-4b0f-8eb3-2cf6a3551a5d, token=680
18:06:38 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:8856fabe-420f-4b0f-8eb3-2cf6a3551a5d, 消息数=2, Token=680
18:06:38 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:8856fabe-420f-4b0f-8eb3-2cf6a3551a5d)
18:06:38 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
18:06:38 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:07:35 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 151b765c-0f6f-4b62-b9a0-03c480020f41
18:07:35 app.api.v1.ai INFO   [预加载] 当前章节已加载: 151b765c-0f6f-4b62-b9a0-03c480020f41
18:07:35 app.api.v1.ai INFO   [预加载] 前一章节已加载: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
18:07:35 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:07:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64782 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:07:35 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 151b765c-0f6f-4b62-b9a0-03c480020f41
18:07:35 app.api.v1.ai INFO   [预加载] 当前章节已加载: 151b765c-0f6f-4b62-b9a0-03c480020f41
18:07:35 app.api.v1.ai INFO   [预加载] 前一章节已加载: eb327c02-9b4f-4e5a-a553-1cf0c500a8d2
18:07:35 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:07:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64786 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:07:35 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64788 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
18:07:35 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:07:35 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/151b765c-0f6f-4b62-b9a0-03c480020f41
INFO:     127.0.0.1:64791 - "PUT /api/v1/chapters/151b765c-0f6f-4b62-b9a0-03c480020f41 HTTP/1.1" 200 OK
18:07:35 app.services.chapter_vector_service INFO   Vectorizing chapter: 第8章 米特尔拍卖场 (order=8)
18:07:37 app.services.chapter_vector_service INFO   Stored chapter vectors: 第8章 米特尔拍卖场 (5 chunks)
18:07:37 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:07:37 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/151b765c-0f6f-4b62-b9a0-03c480020f41
INFO:     127.0.0.1:64794 - "PUT /api/v1/chapters/151b765c-0f6f-4b62-b9a0-03c480020f41 HTTP/1.1" 200 OK
18:07:37 app.services.chapter_vector_service INFO   Vectorizing chapter: 第8章 米特尔拍卖场 (order=8)
18:07:38 app.services.chapter_vector_service INFO   Stored chapter vectors: 第8章 米特尔拍卖场 (5 chunks)
18:07:41 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
18:07:41 app.api.v1.ai INFO   [预加载] 当前章节已加载: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
18:07:41 app.api.v1.ai INFO   [预加载] 前一章节已加载: dda3704d-0276-4649-a2c3-8739b3839da0
18:07:41 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:07:41 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58650 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:07:41 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
18:07:41 app.api.v1.ai INFO   [预加载] 当前章节已加载: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
18:07:41 app.api.v1.ai INFO   [预加载] 前一章节已加载: dda3704d-0276-4649-a2c3-8739b3839da0
18:07:41 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:07:41 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58654 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:07:41 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58656 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
18:07:41 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:07:41 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
INFO:     127.0.0.1:58659 - "PUT /api/v1/chapters/b456ae1b-d4eb-42fd-9cb8-bdfc699e854e HTTP/1.1" 200 OK
18:07:41 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 逛街 (order=4)
18:07:44 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 逛街 (6 chunks)
18:07:44 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:07:44 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/b456ae1b-d4eb-42fd-9cb8-bdfc699e854e
INFO:     127.0.0.1:58662 - "PUT /api/v1/chapters/b456ae1b-d4eb-42fd-9cb8-bdfc699e854e HTTP/1.1" 200 OK
18:07:44 app.services.chapter_vector_service INFO   Vectorizing chapter: 第4章 逛街 (order=4)
18:07:45 app.services.chapter_vector_service INFO   Stored chapter vectors: 第4章 逛街 (6 chunks)
18:07:46 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54623 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
18:07:46 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:07:46 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:07:46 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:07:50 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:07:50 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:07:50 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54626 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:07:50 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请完成以下任务：
1. 首先分析第4章"逛街"中萧凌和萧薰儿的互动描写技巧
2. 然后基于分析结果，...
18:07:50 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:07:50 app.api.v1.agent INFO     - selected_text: N/A...
18:07:50 app.api.v1.agent INFO     - selection_position: N/A
18:07:50 app.api.v1.agent INFO     - chapter_context: 当前章节ID: b456ae1b-d4eb-42fd-9cb8-bdfc699e854e...
18:07:50 app.api.v1.agent INFO     - instruction_context: N/A...
18:07:50 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:077e1183-4064-4c84-9980-3cff88c6acc6 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=077e1183-4064-4c84-9980-3cff88c6acc6)
18:07:50 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:077e1183-4064-4c84-9980-3cff88c6acc6
18:07:50 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:077e1183-4064-4c84-9980-3cff88c6acc6: 0/16000 tokens
18:07:50 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请完成以下任务：
1. 首先分析第4章"逛街"中萧凌和萧薰儿...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:07:50 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:07:50 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 269.00ms
18:07:50 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
18:07:50 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请完成以下任务：
1. 首先分析第4章"逛街"中萧凌和萧薰儿的互动描写技巧
2. 然后基于分析结果，...
18:07:50 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:07:50 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:07:50 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:07:50 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:07:53 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:08:02 app.services.ai.http_ai_service INFO   API 响应完成，共接收 13 个数据块，总长度: 1766
18:08:02 app.services.ai.http_ai_service INFO   流式响应Token统计: 8751 (prompt=7913, completion=838)
18:08:02 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:08:02 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:08:02 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8751, cost=$0.018271, time=12515ms
18:08:03 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8751
18:08:03 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:08:03 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到三个部分的输出：1. 对第4章互动描写技巧的分析, 原料=需要第4章“逛街”的内容来分析互动技巧。, 处理=1. 使用 `get_chapter_b
18:08:03 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共4个任务，耗时: 12.61s
18:08:03 app.api.v1.agent INFO   [Stream] Plan tasks: 4 items
18:08:03 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:08:03 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:08:03 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:08:03 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:08:03 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 4 个任务，反思功能已启用
18:08:03 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:08:03 app.api.v1.agent INFO   [Stream] Task started: 获取第4章'逛街'的内容
18:08:03 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(get_chapter_by_order)
18:08:03 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 开始执行工具
18:08:03 app.services.agent.langgraph_tools INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 第4章 逛街
18:08:03 app.services.agent.tools.tool_types INFO   [get_chapter_by_order] 执行成功 (耗时: 0.103s)
18:08:03 app.services.agent.langgraph_agent INFO   [StandardTool] get_chapter_by_order 执行成功（DeepAgent模式）
18:08:03 app.api.v1.agent INFO   [Stream] 任务完成: 获取第4章'逛街'的内容 (0.1s)
18:08:03 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:08:03 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:08:03 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:08:03 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:08:03 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:08:03 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:08:04 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:08:06 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 122
18:08:06 app.services.ai.http_ai_service INFO   流式响应Token统计: 1910 (prompt=1843, completion=67)
18:08:06 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:08:06 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:08:06 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1910, cost=$0.002974, time=3326ms
18:08:06 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1910
18:08:06 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:08:06 app.api.v1.agent INFO   [Stream] Task started: 分析第4章'逛街'中萧凌和萧薰儿的互动描写技巧
18:08:06 app.services.agent.langgraph_agent INFO   [_execute_task] analyze_text_tool 使用 focus: '分析第4章'逛街'中萧凌和萧薰儿的互动描写技巧，包括但不限于对话方式、神态表情、动作细节、心理活动描写等方面。...'
18:08:06 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(analyze_text)
18:08:06 app.services.agent.tools.tool_types INFO   [analyze_text] 开始执行工具
18:08:06 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 尝试第 1 次调用，config={'temperature': 0.3, 'task_type': <TaskType.SUMMARIZATION: 'summarization'>}
18:08:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:08:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:08:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:08:11 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:08:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 9 个数据块，总长度: 733
18:08:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 5042 (prompt=4475, completion=567)
18:08:24 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:08:24 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:08:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5042, cost=$0.011264, time=17591ms
18:08:24 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 第 1 次调用成功
18:08:24 app.services.agent.tools.analysis_tools INFO   [analyze_text_tool] 分析完成，结果长度: 733
18:08:24 app.services.agent.tools.tool_types INFO   [analyze_text] 执行成功 (耗时: 17.630s)
18:08:24 app.services.agent.langgraph_agent INFO   [StandardTool] analyze_text 执行成功（DeepAgent模式）
18:08:24 app.api.v1.agent INFO   [Stream] 任务完成: 分析第4章'逛街'中萧凌和萧薰儿的互动描写技巧 (17.6s)
18:08:24 app.api.v1.agent INFO   [Stream] Task started: 基于分析结果，续写萧凌和萧薰儿在迦南学院重逢的场景
18:08:24 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
18:08:24 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
18:08:24 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
18:08:24 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
18:08:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
18:08:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:09:01 app.services.ai.http_ai_service INFO   API 响应完成，共接收 11 个数据块，总长度: 896
18:09:01 app.services.ai.http_ai_service INFO   流式响应Token统计: 4384 (prompt=3685, completion=699)
18:09:01 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:09:02 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:09:02 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4384, cost=$0.011596, time=37716ms
18:09:02 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 37.824s)
18:09:02 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
18:09:02 app.api.v1.agent INFO   [Stream] 任务完成: 基于分析结果，续写萧凌和萧薰儿在迦南学院重逢的场景 (37.8s)
18:09:02 app.api.v1.agent INFO   [Stream] Task started: 给出3个可能的后续发展方向
18:09:02 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
18:09:02 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
18:09:02 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
18:09:02 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
18:09:02 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
18:09:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:09:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 11 个数据块，总长度: 892
18:09:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 3662 (prompt=2991, completion=671)
18:09:41 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:09:41 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:09:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3662, cost=$0.010449, time=39726ms
18:09:41 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 39.803s)
18:09:41 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
18:09:41 app.api.v1.agent INFO   [Stream] 任务完成: 给出3个可能的后续发展方向 (39.8s)
18:09:41 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=4, 反思=1, 重规划=0
18:09:41 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:09:41 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共4个任务，耗时: 98.83s
18:09:41 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:09:41 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=1
18:09:41 app.services.agent.langgraph_agent INFO   [Response] 3个输出任务，简单拼接
18:09:44 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.68
18:09:47 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.77
18:09:47 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:077e1183-4064-4c84-9980-3cff88c6acc6, token=1599
18:09:47 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:077e1183-4064-4c84-9980-3cff88c6acc6, 消息数=2, Token=1599
18:09:47 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:077e1183-4064-4c84-9980-3cff88c6acc6)
18:09:47 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
18:09:47 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:10:34 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
18:10:34 app.api.v1.ai INFO   [预加载] 当前章节已加载: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
18:10:34 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
18:10:34 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64394 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:10:34 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
18:10:34 app.api.v1.ai INFO   [预加载] 当前章节已加载: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
18:10:34 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
18:10:34 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64397 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:10:34 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:10:34 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
INFO:     127.0.0.1:64400 - "PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa HTTP/1.1" 200 OK
18:10:34 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
18:10:36 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
18:10:36 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:10:36 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
INFO:     127.0.0.1:57394 - "PUT /api/v1/chapters/4598b368-a71a-4b1c-8bd3-a03b5c0ebafa HTTP/1.1" 200 OK
18:10:36 app.services.chapter_vector_service INFO   Vectorizing chapter: 第1章 重生斗气大陆 (order=1)
18:10:38 app.services.chapter_vector_service INFO   Stored chapter vectors: 第1章 重生斗气大陆 (7 chunks)
18:10:47 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: c2864cda-f1e9-4279-ba13-6204202c8c88
18:10:47 app.api.v1.ai INFO   [预加载] 当前章节已加载: c2864cda-f1e9-4279-ba13-6204202c8c88
18:10:47 app.api.v1.ai INFO   [预加载] 前一章节已加载: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
18:10:47 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:10:47 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49268 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:10:48 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: c2864cda-f1e9-4279-ba13-6204202c8c88
18:10:48 app.api.v1.ai INFO   [预加载] 当前章节已加载: c2864cda-f1e9-4279-ba13-6204202c8c88
18:10:48 app.api.v1.ai INFO   [预加载] 前一章节已加载: 4598b368-a71a-4b1c-8bd3-a03b5c0ebafa
18:10:48 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:10:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49271 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:10:48 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:49274 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
[TaskService] Checking daily writing task for user 602f5147-846a-4cde-95d3-405fa75f133f, word_count: 7
[TaskService] Daily writing task result: None
18:10:48 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:10:48 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/c2864cda-f1e9-4279-ba13-6204202c8c88
INFO:     127.0.0.1:49277 - "PUT /api/v1/chapters/c2864cda-f1e9-4279-ba13-6204202c8c88 HTTP/1.1" 200 OK
18:10:48 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 萧薰儿 (order=2)
18:10:50 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 萧薰儿 (6 chunks)
18:10:50 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:10:50 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/c2864cda-f1e9-4279-ba13-6204202c8c88
INFO:     127.0.0.1:49280 - "PUT /api/v1/chapters/c2864cda-f1e9-4279-ba13-6204202c8c88 HTTP/1.1" 200 OK
18:10:50 app.services.chapter_vector_service INFO   Vectorizing chapter: 第2章 萧薰儿 (order=2)
18:10:51 app.services.chapter_vector_service INFO   Stored chapter vectors: 第2章 萧薰儿 (6 chunks)
18:11:02 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:61305 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
18:11:02 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:11:02 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:11:02 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:11:05 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:11:05 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:11:05 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:61308 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:11:05 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 请帮我改写萧炎第一次出场的描写，让他的形象更加鲜明，同时保留原有的"年少轻狂"特质。

原文：
"只...
18:11:05 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:11:05 app.api.v1.agent INFO     - selected_text: N/A...
18:11:05 app.api.v1.agent INFO     - selection_position: N/A
18:11:05 app.api.v1.agent INFO     - chapter_context: 当前章节ID: c2864cda-f1e9-4279-ba13-6204202c8c88...
18:11:05 app.api.v1.agent INFO     - instruction_context: N/A...
18:11:05 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:e63b3d2e-85a7-420b-977e-8cc28d97d505 (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=e63b3d2e-85a7-420b-977e-8cc28d97d505)
18:11:05 app.services.context.manager INFO   [ContextManager] 创建新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:e63b3d2e-85a7-420b-977e-8cc28d97d505
18:11:05 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:e63b3d2e-85a7-420b-977e-8cc28d97d505: 0/16000 tokens
18:11:06 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='请帮我改写萧炎第一次出场的描写，让他的形象更加鲜明，同时保留...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:11:06 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:11:06 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 275.27ms
18:11:06 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
18:11:06 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 请帮我改写萧炎第一次出场的描写，让他的形象更加鲜明，同时保留原有的"年少轻狂"特质。

原文：
"只...
18:11:06 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:11:06 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:11:06 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:11:06 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:11:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:11:18 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 678
18:11:18 app.services.ai.http_ai_service INFO   流式响应Token统计: 8314 (prompt=7957, completion=357)
18:11:18 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:11:18 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:11:18 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8314, cost=$0.013516, time=12010ms
18:11:18 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=8314
18:11:18 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:11:18 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到创作内容，即改写后的文本。, 原料=需要用户提供的原文片段以及改写要求（形象, 处理=使用 continue_writing_
18:11:18 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 12.11s
18:11:18 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
18:11:18 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:11:18 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:11:18 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:11:18 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:11:18 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
18:11:18 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:11:18 app.api.v1.agent INFO   [Stream] Task started: 根据用户要求，改写萧炎第一次出场的描写，使其形象更鲜明并突出年少轻狂特质。
18:11:18 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
18:11:18 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
18:11:18 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
18:11:18 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
18:11:18 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
18:11:20 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:11:44 app.services.ai.http_ai_service INFO   API 响应完成，共接收 6 个数据块，总长度: 428
18:11:44 app.services.ai.http_ai_service INFO   流式响应Token统计: 3066 (prompt=2741, completion=325)
18:11:44 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:11:45 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:11:45 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3066, cost=$0.006676, time=26640ms
18:11:45 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 26.762s)
18:11:45 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
18:11:45 app.api.v1.agent INFO   [Stream] 任务完成: 根据用户要求，改写萧炎第一次出场的描写，使其形象更鲜明并突出年少轻狂特质。 (26.8s)
18:11:45 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:11:45 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:11:45 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:11:45 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:11:45 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:11:47 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:11:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:11:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 526 (prompt=525, completion=1)
18:11:48 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:11:48 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:11:48 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=526, cost=$0.000666, time=3685ms
18:11:48 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=526
18:11:48 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:11:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:11:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:11:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:11:50 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:11:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 107
18:11:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 1958 (prompt=1904, completion=54)
18:11:53 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:11:53 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:11:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1958, cost=$0.002920, time=4313ms
18:11:53 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=1958
18:11:53 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:11:53 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:11:53 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:11:53 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:11:54 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:11:56 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 4
18:11:56 app.services.ai.http_ai_service INFO   流式响应Token统计: 521 (prompt=520, completion=1)
18:11:56 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:11:56 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:11:56 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=521, cost=$0.000660, time=3744ms
18:11:56 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=521
18:11:56 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
18:11:56 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:11:56 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 38.61s
18:11:56 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:11:56 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
18:11:56 app.services.agent.langgraph_agent INFO   [Response] 单个分析任务(continue_writing_tool)，使用AI格式化
18:11:56 app.services.agent.langgraph_agent INFO   [Summarization] 使用AI整合任务结果
18:11:56 app.services.agent.langgraph_agent INFO   [Summarization] 上下文压缩: 原始=530字符, 压缩后=572字符, 压缩率=-7%
18:11:56 app.services.agent.langgraph_agent INFO   [Summarization] 使用流式生成（_generate_text_stream）
18:11:56 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 开始流式生成，buffer_size=1
18:11:56 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:11:56 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:11:56 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
18:11:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:11:57 app.services.ai.http_ai_service INFO   API 响应完成，共接收 0 个数据块，总长度: 0
18:11:57 app.services.ai.http_ai_service INFO   流式响应Token统计: 596 (prompt=596, completion=0)
18:11:57 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:11:57 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:11:57 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=596, cost=$0.000745, time=492ms
18:11:57 app.services.ai.http_ai_service ERROR   警告: AI 响应为空！未接收到任何内容块。
18:11:57 app.services.agent.langgraph_agent INFO   [_generate_text_stream] 流式生成完成，总长度=0
18:11:58 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.68
18:11:58 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:e63b3d2e-85a7-420b-977e-8cc28d97d505, token=50
18:11:58 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:e63b3d2e-85a7-420b-977e-8cc28d97d505, 消息数=2, Token=50
18:11:58 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:e63b3d2e-85a7-420b-977e-8cc28d97d505)
18:11:58 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
18:12:06 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 05527755-20bb-46d3-850f-dc729f11eea3
18:12:06 app.api.v1.ai INFO   [预加载] 当前章节已加载: 05527755-20bb-46d3-850f-dc729f11eea3
18:12:06 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:12:06 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:12:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54633 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:12:06 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 05527755-20bb-46d3-850f-dc729f11eea3
18:12:06 app.api.v1.ai INFO   [预加载] 当前章节已加载: 05527755-20bb-46d3-850f-dc729f11eea3
18:12:06 app.api.v1.ai INFO   [预加载] 前一章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:12:06 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:12:06 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54636 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:12:07 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:12:07 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3
INFO:     127.0.0.1:54639 - "PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3 HTTP/1.1" 200 OK
18:12:07 app.services.chapter_vector_service INFO   Vectorizing chapter: 第50章 抵达加码 (order=50)
18:12:09 app.services.chapter_vector_service INFO   Stored chapter vectors: 第50章 抵达加码 (7 chunks)
18:12:09 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:12:09 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3
INFO:     127.0.0.1:54643 - "PUT /api/v1/chapters/05527755-20bb-46d3-850f-dc729f11eea3 HTTP/1.1" 200 OK
18:12:09 app.services.chapter_vector_service INFO   Vectorizing chapter: 第50章 抵达加码 (order=50)
18:12:12 app.services.chapter_vector_service INFO   Stored chapter vectors: 第50章 抵达加码 (7 chunks)
18:12:12 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:12:12 app.api.v1.ai INFO   [预加载元数据] 用户: testuser_new-1(602f5147-846a-4cde-95d3-405fa75f133f), work_id: 972a2087-ff2c-4fb7-a501-18b36906dd1b, chapter_id: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:12:12 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:12:12 app.api.v1.ai INFO   [预加载] 当前章节已加载: 0674f1e7-821b-4684-9c89-eca564ec71b4
18:12:12 app.api.v1.ai INFO   [预加载] 前一章节已加载: d9924a45-250a-4c28-8500-38e519cc1348
18:12:12 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:12:12 app.api.v1.ai INFO   [预加载] 前一章节已加载: d9924a45-250a-4c28-8500-38e519cc1348
18:12:12 app.api.v1.ai INFO   [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
18:12:12 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
18:12:12 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54649 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:54646 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
18:12:12 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:12:12 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4
INFO:     127.0.0.1:54652 - "PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4 HTTP/1.1" 200 OK
18:12:12 app.services.chapter_vector_service INFO   Vectorizing chapter: 第49章 飞行路途 (order=49)
18:12:14 app.services.chapter_vector_service INFO   Stored chapter vectors: 第49章 飞行路途 (6 chunks)
18:12:14 app.api.v1.chapters INFO   🗑️ [Chapters] 缓存已失效: chapters:work:972a2087-ff2c-4fb7-a501-18b36906dd1b
18:12:14 app.api.middleware.monitoring_middleware INFO   API请求完成: PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4
INFO:     127.0.0.1:51190 - "PUT /api/v1/chapters/0674f1e7-821b-4684-9c89-eca564ec71b4 HTTP/1.1" 200 OK
18:12:14 app.services.chapter_vector_service INFO   Vectorizing chapter: 第49章 飞行路途 (order=49)
18:12:15 app.services.chapter_vector_service INFO   Stored chapter vectors: 第49章 飞行路途 (6 chunks)
18:12:23 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
18:12:23 app.services.ai.http_ai_service INFO   ModelSelector 已启用
18:12:23 app.services.ai.http_ai_service INFO   AILogService 已启用 (用于成本追踪)
18:12:29 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
18:12:29 app.api.v1.agent INFO   [Chat Stream] Mode: planning
18:12:29 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54060 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
18:12:29 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 我想给这本小说增加一条新的支线：萧凌在迦南学院遇到一个神秘的炼药师长老，这个长老似乎认识药尘。

请...
18:12:29 app.api.v1.agent INFO   [agent_chat_stream] 📥 收到的 context 字段:
18:12:29 app.api.v1.agent INFO     - selected_text: N/A...
18:12:29 app.api.v1.agent INFO     - selection_position: N/A
18:12:29 app.api.v1.agent INFO     - chapter_context: 当前章节ID: 0674f1e7-821b-4684-9c89-eca564ec71b4...
18:12:29 app.api.v1.agent INFO     - instruction_context: N/A...
18:12:29 app.services.agent.langgraph_agent INFO   [Planning] 使用隔离的thread_id: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f (user_id=602f5147-846a-4cde-95d3-405fa75f133f, work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b, conversation_id=4ac544e4-f1c3-43bc-898d-e675fc9a015f)
18:12:29 app.services.context.store INFO   [ContextStore] 加载上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f, 2条消息
18:12:29 app.services.context.manager INFO   [ContextManager] Session 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f: 389/16000 tokens
18:12:29 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='我想给这本小说增加一条新的支线：萧凌在迦南学院遇到一个神秘的...' | 隔离键=['user:602f5147-846a-4cde-95d3-405fa75f133f:work:972a2087-ff2c-4fb7-a501-18b36906dd1b', 'user:602f5147-846a-4cde-95d3-405fa75f133f'] | 找到=3条
18:12:29 app.services.context.manager INFO   🔍 检索长期记忆 | 级别=work | work_id=972a2087-ff2c-4fb7-a501-18b36906dd1b | 含用户级=True | 找到=3条
18:12:29 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 3条消息, 389 tokens, 耗时 170.97ms
18:12:29 app.services.agent.langgraph_agent INFO   [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 389)
18:12:29 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 我想给这本小说增加一条新的支线：萧凌在迦南学院遇到一个神秘的炼药师长老，这个长老似乎认识药尘。

请...
18:12:29 app.core.cache INFO   ✅ 缓存命中: prompt:planning_agent:v2.12.0:get_planning_agent_mode_prompt:fca6eb91156619d0
18:12:29 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:12:29 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:12:29 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
18:12:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:12:34 app.services.ai.http_ai_service INFO   API 响应完成，共接收 8 个数据块，总长度: 898
18:12:34 app.services.ai.http_ai_service INFO   流式响应Token统计: 7084 (prompt=6605, completion=479)
18:12:34 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:12:34 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:12:34 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7084, cost=$0.013046, time=5220ms
18:12:34 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=7084
18:12:34 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:12:34 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到创作内容：包括新角色的背景设定、与主角的互动规划, 原料=需要作品的整体背景和当前主角（萧凌）所处, 处理=使用 continue_writing_
18:12:34 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共1个任务，耗时: 5.39s
18:12:34 app.api.v1.agent INFO   [Stream] Plan tasks: 1 items
18:12:34 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:12:34 app.services.agent.langgraph_agent INFO   [DeepAgent] 启用反思模式
18:12:34 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:12:34 app.services.agent.langgraph_agent INFO   [DeepAgent] ParameterResolver 已启用
18:12:34 app.services.agent.deep_agent.executor INFO   DeepAgent 开始执行，共 1 个任务，反思功能已启用
18:12:34 app.services.agent.deep_agent.task_enricher INFO   [TaskEnricher] AI 推断功能已启用
18:12:34 app.api.v1.agent INFO   [Stream] Task started: 创作神秘炼药师长老的角色背景设定，规划与萧凌的3次关键互动，并撰写第一次相遇的场景。
18:12:34 app.services.agent.langgraph_agent INFO   [_execute_task] 调用 registry.call_tool(continue_writing)
18:12:34 app.services.agent.tools.tool_types INFO   [continue_writing] 开始执行工具
18:12:34 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: complex
18:12:34 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
18:12:34 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-pro, max_tokens=1000, temp=0.8, task_type=TaskType.CONTENT_CREATION
18:12:37 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:13:07 app.services.ai.http_ai_service INFO   API 响应完成，共接收 16 个数据块，总长度: 1321
18:13:07 app.services.ai.http_ai_service INFO   流式响应Token统计: 3200 (prompt=2163, completion=1037)
18:13:07 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:13:07 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:13:07 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3200, cost=$0.013074, time=32336ms
18:13:07 app.services.agent.tools.tool_types INFO   [continue_writing] 执行成功 (耗时: 32.568s)
18:13:07 app.services.agent.langgraph_agent INFO   [StandardTool] continue_writing 执行成功（DeepAgent模式）
18:13:07 app.api.v1.agent INFO   [Stream] 任务完成: 创作神秘炼药师长老的角色背景设定，规划与萧凌的3次关键互动，并撰写第一次相遇的场景。 (32.6s)
18:13:07 app.services.agent.deep_agent.reflection INFO   [Checkpoint] 首个任务 1 未标记 checkpoint，触发一次兜底反思以校验规划
18:13:07 app.services.agent.deep_agent.executor INFO   任务 1 触发反思检查点
18:13:07 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:13:07 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:13:07 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:13:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:13:10 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 58
18:13:10 app.services.ai.http_ai_service INFO   流式响应Token统计: 537 (prompt=515, completion=22)
18:13:10 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:13:10 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:13:10 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=537, cost=$0.000864, time=3058ms
18:13:10 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=537
18:13:10 app.services.agent.deep_agent.reflection INFO   [DeepAgent反思] 开始调用 AI，task_id=1
18:13:10 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:13:10 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:13:10 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=500, temp=0.3, task_type=TaskType.SIMPLE_QA
18:13:12 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:13:14 app.services.ai.http_ai_service INFO   API 响应完成，共接收 2 个数据块，总长度: 130
18:13:14 app.services.ai.http_ai_service INFO   流式响应Token统计: 2134 (prompt=2066, completion=68)
18:13:14 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:13:14 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:13:14 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2134, cost=$0.003263, time=4105ms
18:13:14 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=2134
18:13:14 app.services.agent.deep_agent.reflection INFO   [Reflection] JSON提取成功: needs_replan=False
18:13:14 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:13:14 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:13:14 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=100, temp=0.1, task_type=TaskType.SIMPLE_QA
18:13:16 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:13:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 1 个数据块，总长度: 58
18:13:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 546 (prompt=524, completion=22)
18:13:17 app.services.ai.http_ai_service INFO   [成本追踪] user_id来源: 上下文, user_id=602f5147-846a-4cde-95d3-405fa75f133f
18:13:17 app.services.ai.http_ai_service INFO   [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
18:13:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=546, cost=$0.000875, time=2954ms
18:13:17 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=546
18:13:17 app.services.agent.deep_agent.executor INFO   DeepAgent 执行完成: 任务=1, 反思=1, 重规划=0
18:13:17 app.services.agent.langgraph_agent INFO   [DeepAgent] 执行完成: 反思=1次, 重规划=0次
18:13:17 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共1个任务，耗时: 43.14s
18:13:17 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:13:17 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=1, 展示型=0
18:13:17 app.services.agent.langgraph_agent INFO   [Response] 单个创作任务(continue_writing_tool)，输出1321字符，直接返回（跳过AI调用）
18:13:19 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=1.00
18:13:20 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 隔离=work:972a2087-ff2c-4fb7-a501-18b36906dd1b | 重要度=0.58
18:13:20 app.services.context.store INFO   [ContextStore] 保存上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f, token=1245
18:13:20 app.services.context.manager INFO   [ContextManager] 更新上下文: 602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f, 消息数=4, Token=1245
18:13:20 app.services.agent.langgraph_agent INFO   [Planning] 已保存对话到 ContextManager (session=602f5147-846a-4cde-95d3-405fa75f133f:972a2087-ff2c-4fb7-a501-18b36906dd1b:4ac544e4-f1c3-43bc-898d-e675fc9a015f)
18:13:20 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
18:13:20 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed