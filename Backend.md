18:19:57 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 1到5章分别讲了什么?...
18:19:57 app.core.cache INFO   ✅ 缓存命中: prompt:get_planning_static_prompt:fca6eb91156619d0
18:19:57 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: simple
18:19:57 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=simple_qa, 模型=gemini-2.5-flash-lite, 原因=任务复杂度为 simple; 任务类型: simple_qa; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
18:19:57 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=1200, temp=0.3, task_type=TaskType.SIMPLE_QA
18:20:00 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 18 个数据块，总长度: 2450
18:20:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 4589 (prompt=3477, completion=1112)
18:20:05 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4589, cost=$0.015466, time=7326ms
18:20:05 app.services.agent.langgraph_agent INFO   [_generate_text] 使用HTTPAIService生成文本，tokens=4589
18:20:05 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
18:20:05 app.services.agent.langgraph_agent INFO   [Planning] 思维链: 输出=用户期望看到对1到5章内容的概括性总结，需要分别说明每一章讲, 原料=需要获取作品 ID '9398f47b-, 处理=获取这五章的原文内容，然后分别使用 an
18:20:05 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共10个任务，耗时: 7.45s
18:20:05 app.api.v1.agent INFO   [Stream] Plan tasks: 10 items
18:20:05 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
18:20:05 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
18:20:05 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 第一层并行=5, 第二层并行=5, 串行=0
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行5个任务
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 获取第1章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 获取第1章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3开始: 获取第2章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 获取第2章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5开始: 获取第3章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 获取第3章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务7开始: 获取第4章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 获取第4章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务9开始: 获取第5章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 获取第5章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第1章: 百年关，天机变
18:20:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第3章: 下山
18:20:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第5章: 一饭之恩，乱世人心
18:20:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第4章: 荒村孤烟，道祖传心
18:20:05 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] ✅ 找到第2章: 道祖出关，太极震群魔
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
18:20:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第1章内容 (0.2s)
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务5完成
18:20:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第3章内容 (0.2s)
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务9完成
18:20:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第5章内容 (0.2s)
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务7完成
18:20:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第4章内容 (0.2s)
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务3完成
18:20:05 app.api.v1.agent INFO   [Stream] 任务完成: 获取第2章内容 (0.2s)
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始第二层并行执行5个分析任务
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 第二层并行任务2开始: 概括第1章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 概括第1章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 第二层并行任务4开始: 概括第2章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 概括第2章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 第二层并行任务6开始: 概括第3章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 概括第3章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 第二层并行任务8开始: 概括第4章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 概括第4章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.services.agent.langgraph_agent INFO   [ParallelExecution] 第二层并行任务10开始: 概括第5章内容
18:20:05 app.api.v1.agent INFO   [Stream] Task started: 概括第5章内容
18:20:05 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v3.1.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: creative_writing (v1.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: system_agent (v2.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
18:20:05 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载8个模板, 注册0个验证器
18:20:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:05 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:05 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:05 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:07 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:08 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:09 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:19 app.services.ai.http_ai_service INFO   API 响应完成，共接收 25 个数据块，总长度: 2000
18:20:19 app.services.ai.http_ai_service INFO   流式响应Token统计: 4646 (prompt=3065, completion=1581)
18:20:19 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:19 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4646, cost=$0.019641, time=14095ms
18:20:19 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2000
18:20:19 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务2失败，重试...
18:20:20 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:20 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:20 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:20 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:22 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:23 app.services.ai.http_ai_service INFO   API 响应完成，共接收 30 个数据块，总长度: 2477
18:20:23 app.services.ai.http_ai_service INFO   流式响应Token统计: 5455 (prompt=3505, completion=1950)
18:20:23 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:23 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5455, cost=$0.023881, time=17300ms
18:20:23 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2477
18:20:23 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务6失败，重试...
18:20:24 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:24 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:24 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:24 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:24 app.services.ai.http_ai_service INFO   API 响应完成，共接收 25 个数据块，总长度: 2221
18:20:24 app.services.ai.http_ai_service INFO   流式响应Token统计: 6402 (prompt=4742, completion=1660)
18:20:24 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:24 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6402, cost=$0.022527, time=18624ms
18:20:24 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2221
18:20:24 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务8失败，重试...
18:20:25 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:25 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:25 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:25 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:26 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:26 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2356
18:20:26 app.services.ai.http_ai_service INFO   流式响应Token统计: 6528 (prompt=4708, completion=1820)
18:20:26 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:26 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6528, cost=$0.024085, time=20735ms
18:20:26 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2356
18:20:26 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务4失败，重试...
18:20:27 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:27 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:27 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:27 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:27 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:29 app.services.ai.http_ai_service INFO   API 响应完成，共接收 35 个数据块，总长度: 3062
18:20:29 app.services.ai.http_ai_service INFO   流式响应Token统计: 6755 (prompt=4470, completion=2285)
18:20:29 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:29 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6755, cost=$0.028438, time=23307ms
18:20:29 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3062
18:20:29 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务10失败，重试...
18:20:30 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:30 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:30 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:30 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:30 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:31 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:39 app.services.ai.http_ai_service INFO   API 响应完成，共接收 32 个数据块，总长度: 1991
18:20:39 app.services.ai.http_ai_service INFO   流式响应Token统计: 5605 (prompt=4067, completion=1538)
18:20:39 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:39 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5605, cost=$0.020464, time=18184ms
18:20:39 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 1991
18:20:39 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务2失败，重试...
18:20:40 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:40 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:40 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:40 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:41 app.services.ai.http_ai_service INFO   API 响应完成，共接收 31 个数据块，总长度: 2604
18:20:41 app.services.ai.http_ai_service INFO   流式响应Token统计: 5470 (prompt=3445, completion=2025)
18:20:41 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:41 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5470, cost=$0.024556, time=17063ms
18:20:41 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2604
18:20:41 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务6失败，重试...
18:20:41 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:42 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:42 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:42 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:42 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:43 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2289
18:20:43 app.services.ai.http_ai_service INFO   流式响应Token统计: 6568 (prompt=4840, completion=1728)
18:20:43 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:43 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6568, cost=$0.023330, time=17998ms
18:20:43 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2289
18:20:43 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务8失败，重试...
18:20:43 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:44 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:44 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:44 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:44 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:46 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:47 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2352
18:20:47 app.services.ai.http_ai_service INFO   流式响应Token统计: 6312 (prompt=4518, completion=1794)
18:20:47 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:47 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6312, cost=$0.023588, time=19836ms
18:20:47 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2352
18:20:47 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务4失败，重试...
18:20:48 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:48 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:48 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:48 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:49 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:20:53 app.services.ai.http_ai_service INFO   API 响应完成，共接收 45 个数据块，总长度: 3012
18:20:53 app.services.ai.http_ai_service INFO   流式响应Token统计: 6856 (prompt=4674, completion=2182)
18:20:53 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:53 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6856, cost=$0.027662, time=23155ms
18:20:53 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3012
18:20:53 app.services.agent.langgraph_agent WARNING   [ParallelExecution] 第二层任务10失败，重试...
18:20:54 app.services.agent.multi_agent.executor INFO   [MultiAgent] 执行器初始化完成
18:20:54 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
18:20:54 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
18:20:54 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.3, task_type=TaskType.SUMMARIZATION
18:20:54 app.services.ai.http_ai_service INFO   API 响应完成，共接收 24 个数据块，总长度: 1974
18:20:54 app.services.ai.http_ai_service INFO   流式响应Token统计: 4696 (prompt=3134, completion=1562)
18:20:54 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:20:54 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=4696, cost=$0.019537, time=14453ms
18:20:54 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 1974
18:20:54 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 第二层任务2最终失败: agent_chat_stream.<locals>.event_generator.<locals>.on_task_done() missing 1 required positional argument: 'result_data'
18:20:57 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
18:21:04 app.services.ai.http_ai_service INFO   API 响应完成，共接收 28 个数据块，总长度: 2464
18:21:04 app.services.ai.http_ai_service INFO   流式响应Token统计: 6332 (prompt=4496, completion=1836)
18:21:04 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:21:04 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6332, cost=$0.023980, time=20181ms
18:21:04 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2464
18:21:04 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 第二层任务8最终失败: agent_chat_stream.<locals>.event_generator.<locals>.on_task_done() missing 1 required positional argument: 'result_data'
18:21:05 app.services.ai.http_ai_service INFO   API 响应完成，共接收 47 个数据块，总长度: 2951
18:21:05 app.services.ai.http_ai_service INFO   流式响应Token统计: 6934 (prompt=4647, completion=2287)
18:21:05 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:21:05 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6934, cost=$0.028679, time=23021ms
18:21:05 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2951
18:21:05 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 第二层任务6最终失败: agent_chat_stream.<locals>.event_generator.<locals>.on_task_done() missing 1 required positional argument: 'result_data'
18:21:11 app.services.ai.http_ai_service INFO   API 响应完成，共接收 54 个数据块，总长度: 3305
18:21:11 app.services.ai.http_ai_service INFO   流式响应Token统计: 7438 (prompt=4823, completion=2615)
18:21:11 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:21:11 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7438, cost=$0.032179, time=23377ms
18:21:11 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 3305
18:21:11 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 第二层任务4最终失败: agent_chat_stream.<locals>.event_generator.<locals>.on_task_done() missing 1 required positional argument: 'result_data'
18:21:17 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2320
18:21:17 app.services.ai.http_ai_service INFO   流式响应Token统计: 6279 (prompt=4544, completion=1735)
18:21:17 app.services.ai.http_ai_service INFO   [积分扣费] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣费
18:21:17 app.services.ai.http_ai_service INFO   [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6279, cost=$0.023030, time=23060ms
18:21:17 app.services.agent.langgraph_agent INFO   ✅ [Agent分析] 分析完成，结果长度: 2320
18:21:17 app.services.agent.langgraph_agent ERROR   [ParallelExecution] 第二层任务10最终失败: agent_chat_stream.<locals>.event_generator.<locals>.on_task_done() missing 1 required positional argument: 'result_data'
18:21:17 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共10个任务，耗时: 72.04s
18:21:17 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
18:21:17 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=0, 输出型=5, 展示型=5
18:21:17 app.services.agent.langgraph_agent INFO   [Response] 5个输出任务，简单拼接
18:21:17 app.api.v1.agent INFO   [Stream] 跳过最终响应（内容已流式发送）
18:21:17 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed