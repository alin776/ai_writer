纲
2025-11-04 23:41:55,606 - app.api.v1.agent - INFO - [Stream] 任务开始: 整合信息并生成剧情大纲
2025-11-04 23:41:55,610 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2025-11-04 23:41:55,612 - app.services.ai.http_ai_service - INFO - [ModelSelector] 任务=content_creation, 模型=gemini-2.5-pro, 原因=任务复杂度为 complex; 任务类型: content_creation; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$5.0 per 1M tokens)
2025-11-04 23:41:55,612 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=TaskType.CONTENT_CREATION
2025-11-04 23:42:01,620 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
2025-11-04 23:42:01,620 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-11-04 23:43:29,697 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 84 个数据块，总长度: 6983
2025-11-04 23:43:29,697 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 7818 (prompt=2598, completion=5220)
2025-11-04 23:43:29,698 - app.services.agent.cost_tracker - INFO - [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2598+5220=7818, cost: $0.000704
2025-11-04 23:43:29,698 - app.services.ai.http_ai_service - INFO - [CostTracker] API调用已记录: tokens=2598+5220, cost=$0.000704, time=94.08s
2025-11-04 23:43:29,700 - app.services.agent.langgraph_agent - INFO - [Execution] 任务6完成
2025-11-04 23:43:29,700 - app.api.v1.agent - INFO - [Stream] 任务完成: 整合信息并生成剧情大纲 (0.0s)
2025-11-04 23:43:29,700 - app.services.agent.langgraph_agent - INFO - [Summarization] 生成最终响应
2025-11-04 23:43:29,700 - app.services.agent.langgraph_agent - INFO - [Summarization] 上下文压缩: 原始=19149字符, 压缩后=1229字符, 压缩率=94%
2025-11-04 23:43:29,700 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2025-11-04 23:43:29,700 - app.services.ai.http_ai_service - INFO - [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
2025-11-04 23:43:29,705 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2025-11-04 23:43:32,239 - httpx - INFO - HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
2025-11-04 23:43:32,239 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2025-11-04 23:44:04,598 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 26 个数据块，总长度: 2528
2025-11-04 23:44:04,598 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 4868 (prompt=3209, completion=1659)
2025-11-04 23:44:04,598 - app.services.agent.cost_tracker - INFO - [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 3209+1659=4868, cost: $0.000295
2025-11-04 23:44:04,598 - app.services.ai.http_ai_service - INFO - [CostTracker] API调用已记录: tokens=3209+1659, cost=$0.000295, time=34.89s
2025-11-04 23:44:04,601 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存 2 条新消息到checkpointer (总计: 2)
2025-11-04 23:44:04,601 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Stream completed
