2025-12-29 21:49:44,721 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-29 21:49:44,725 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-29 21:49:44,726 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2025-12-29 21:49:44,728 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63308 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-29 21:49:44,760 - app.api.v1.ai - INFO - [预加载元数据] 用户: 2072855200@qq.com(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: f141c5ed-0a75-4429-ba2a-912c74d167a3, chapter_id: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-29 21:49:44,768 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c726baba-b01b-42ea-9c5d-0d2d5b221d94
2025-12-29 21:49:44,768 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2025-12-29 21:49:44,770 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54714 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2025-12-29 21:49:44,927 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-29 21:49:44,929 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94
INFO:     127.0.0.1:60814 - "PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94 HTTP/1.1" 200 OK
2025-12-29 21:49:44,930 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2025-12-29 21:49:45,779 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
2025-12-29 21:49:45,805 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:f141c5ed-0a75-4429-ba2a-912c74d167a3
2025-12-29 21:49:45,806 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94
INFO:     127.0.0.1:57258 - "PUT /api/v1/chapters/c726baba-b01b-42ea-9c5d-0d2d5b221d94 HTTP/1.1" 200 OK
2025-12-29 21:49:45,807 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2025-12-29 21:49:46,464 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2025-12-29 21:49:46,464 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (7 chunks)
INFO:     127.0.0.1:50108 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-29 21:49:50,810 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/users/me/preferences
INFO:     127.0.0.1:63454 - "PUT /api/v1/users/me/preferences HTTP/1.1" 200 OK
2025-12-29 21:49:58,837 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/users/me/preferences
INFO:     127.0.0.1:60543 - "PUT /api/v1/users/me/preferences HTTP/1.1" 200 OK
2025-12-29 21:50:02,314 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:51582 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2025-12-29 21:50:02,327 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-29 21:50:02,328 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-29 21:50:02,328 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-29 21:50:03,848 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-29 21:50:03,849 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-29 21:50:03,853 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:57135 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-29 21:50:03,857 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 帮我续写第1章的后续内容，段融吞噬器灵后会发生什么...
2025-12-29 21:50:03,857 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-29 21:50:03,858 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-29 21:50:03,858 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-29 21:50:03,858 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-29 21:50:03,859 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-29 21:50:03,860 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=4b62cd68-1f40-497c-bd70-740a258b2562)
2025-12-29 21:50:03,862 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562
2025-12-29 21:50:03,862 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562: 0/16000 tokens
2025-12-29 21:50:03,935 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='帮我续写第1章的后续内容，段融吞噬器灵后会发生什么...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-29 21:50:03,936 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-29 21:50:03,936 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 75.65ms
2025-12-29 21:50:03,937 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0)
2025-12-29 21:50:03,937 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 帮我续写第1章的后续内容，段融吞噬器灵后会发生什么...
2025-12-29 21:50:03,941 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.20.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-29 21:50:03,947 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-29 21:50:03,947 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-29 21:50:03,948 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-29 21:50:05,847 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-29 21:50:07,241 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 606
2025-12-29 21:50:07,242 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 8507 (prompt=8139, completion=368)
2025-12-29 21:50:07,243 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-29 21:50:07,243 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-29 21:50:07,273 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 11.92 积分, 余额: 45947.17 → 45935.25
2025-12-29 21:50:07,275 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8507, cost=$0.000961, time=3296ms
2025-12-29 21:50:07,276 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=8507
2025-12-29 21:50:07,277 - app.services.agent.planning.plan_generator - INFO - [Planning] AI 决定直接回答，跳过任务执行
2025-12-29 21:50:07,277 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望我续写第一章的后续内容，具体是段融吞噬器灵后会发生什, 原料=需要第一章的内容作为上下文。, 处理=续写新的章节内容。
2025-12-29 21:50:07,277 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 341
2025-12-29 21:50:07,278 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共0个任务
2025-12-29 21:50:07,279 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共0个任务，耗时: 3.34s
2025-12-29 21:50:07,279 - app.api.v1.agent - INFO - [Stream] Plan tasks: 0 items
2025-12-29 21:50:07,280 - app.services.agent.langgraph_agent - INFO - [Planning] 检测到 direct_answer(341字)，直接返回答案，跳过任务执行
2025-12-29 21:50:08,596 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.65
2025-12-29 21:50:09,932 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-29 21:50:09,938 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562, token=421
2025-12-29 21:50:09,939 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562, 消息数=2, Token=421
2025-12-29 21:50:09,940 - app.services.agent.langgraph_agent - INFO - [Planning] direct_answer 对话已保存到 ContextManager
2025-12-29 21:50:09,940 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-29 21:50:09,945 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2025-12-29 21:51:17,155 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2025-12-29 21:51:17,156 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2025-12-29 21:51:17,156 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2025-12-29 21:51:18,598 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2025-12-29 21:51:18,600 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2025-12-29 21:51:18,603 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:65086 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2025-12-29 21:51:18,613 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 好的，开始吧...
2025-12-29 21:51:18,615 - app.api.v1.agent - INFO - [agent_chat_stream] 📥 收到的 context 字段:
2025-12-29 21:51:18,616 - app.api.v1.agent - INFO -   - selected_text: N/A...
2025-12-29 21:51:18,617 - app.api.v1.agent - INFO -   - selection_position: N/A
2025-12-29 21:51:18,618 - app.api.v1.agent - INFO -   - chapter_context: 当前章节ID: c726baba-b01b-42ea-9c5d-0d2d5b221d94...
2025-12-29 21:51:18,619 - app.api.v1.agent - INFO -   - instruction_context: N/A...
2025-12-29 21:51:18,619 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3, conversation_id=4b62cd68-1f40-497c-bd70-740a258b2562)
2025-12-29 21:51:18,623 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562, 2条消息
2025-12-29 21:51:18,624 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562: 421/16000 tokens
2025-12-29 21:51:18,702 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='好的，开始吧...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:f141c5ed-0a75-4429-ba2a-912c74d167a3', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2025-12-29 21:51:18,702 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=f141c5ed-0a75-4429-ba2a-912c74d167a3 | 含用户级=True | 找到=3条
2025-12-29 21:51:18,702 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 3条消息, 421 tokens, 耗时 82.36ms
2025-12-29 21:51:18,702 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 3 条历史消息 (token: 421)
2025-12-29 21:51:18,702 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 好的，开始吧...
2025-12-29 21:51:18,706 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.20.0:get_planning_static_prompt:fca6eb91156619d0
2025-12-29 21:51:18,712 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2025-12-29 21:51:18,712 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=simple_qa, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2025-12-29 21:51:18,712 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2000, temp=0.3, task_type=TaskType.SIMPLE_QA
2025-12-29 21:51:20,309 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-12-29 21:51:22,475 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 10 个数据块，总长度: 684
2025-12-29 21:51:22,477 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 8806 (prompt=8387, completion=419)
2025-12-29 21:51:22,478 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2025-12-29 21:51:22,478 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2025-12-29 21:51:22,501 - app.services.ai.http_ai_service - INFO - [积分扣除] 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456: 扣除 12.48 积分, 余额: 45935.25 → 45922.77
2025-12-29 21:51:22,502 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8806, cost=$0.001006, time=3765ms
2025-12-29 21:51:22,503 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=8806
2025-12-29 21:51:22,503 - app.services.agent.planning.plan_generator - INFO - [Planning] AI 决定直接回答，跳过任务执行
2025-12-29 21:51:22,503 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望我续写第一章的后续内容，即段融吞噬器灵之后会发生什么, 原料=需要第一章的结尾内容和器灵的特点，以便更, 处理=展示创作计划，询问用户意见，待用户确认后
2025-12-29 21:51:22,504 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 343
2025-12-29 21:51:22,504 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共0个任务
2025-12-29 21:51:22,505 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共0个任务，耗时: 3.80s
2025-12-29 21:51:22,505 - app.api.v1.agent - INFO - [Stream] Plan tasks: 0 items
2025-12-29 21:51:22,506 - app.services.agent.langgraph_agent - INFO - [Planning] 检测到 direct_answer(343字)，直接返回答案，跳过任务执行
2025-12-29 21:51:23,734 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:f141c5ed-0a75-4429-ba2a-912c74d167a3 | 重要度=0.60
2025-12-29 21:51:23,737 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562, token=814
2025-12-29 21:51:23,739 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:f141c5ed-0a75-4429-ba2a-912c74d167a3:4b62cd68-1f40-497c-bd70-740a258b2562, 消息数=4, Token=814
2025-12-29 21:51:23,739 - app.services.agent.langgraph_agent - INFO - [Planning] direct_answer 对话已保存到 ContextManager
2025-12-29 21:51:23,740 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2025-12-29 21:51:23,744 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed