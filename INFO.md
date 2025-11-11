20:45:11 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: react, Message: 第一章：浊地 讲了什么？...
20:45:11 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 开始流式执行: 第一章：浊地 讲了什么？...
20:45:11 app.services.agent.langgraph_agent INFO   [Context] 设置用户ID: 602f5147-846a-4cde-95d3-405fa75f133f
20:45:11 app.services.context.manager INFO   [ContextManager] 创建新上下文: f8528ea5-3111-4c45-8f7c-2408d12e5412
20:45:11 app.services.context.manager INFO   [ContextManager] Session f8528ea5-3111-4c45-8f7c-2408d12e5412: 600/8000 tokens
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  8.06it/s]
20:45:11 app.services.context.vector_memory_store INFO   🔍 检索记忆 | 查询='第一章：浊地 讲了什么？...' | 用户=602f5147-846a-4cde-95d3-405fa75f133f | 找到=3条 | 阈值=0.3
20:45:11 app.services.context.manager INFO   🔍 检索长期记忆 | 查询='第一章：浊地 讲了什么？...' | 找到=3条 | 阈值=0.3
20:45:11 app.services.context.monitoring_integration INFO   [Monitor] 上下文构建: 2条消息, 600 tokens, 耗时 175.92ms
20:45:11 app.services.agent.langgraph_agent INFO   [Context] 加载上下文: {'session_id': 'f8528ea5-3111-4c45-8f7c-2408d12e5412', 'token_count': 600, 'short_memory_size': 0, 'has_summary': False, 'compression_triggered': False, 'long_term_memories': 3, 'adaptive_budget_enabled': False, 'task_type': None}
20:45:11 app.services.agent.progress_tracker INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）
20:45:11 app.services.agent.langgraph_agent INFO   [ProgressTracker] 初始化完成，使用动态节点追踪模式
20:45:11 app.services.agent.langgraph_agent INFO   [LangGraph] 意图分类（规则识别）
20:45:11 app.services.agent.langgraph_agent INFO   [Intent] 规则识别结果: writing, 置信度: 0.90
20:45:11 app.services.agent.langgraph_agent INFO   [LangGraph] 路由到: writing
20:45:11 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_intent
20:45:11 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: intent_classifier
20:45:11 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'intent_analysis', 'description': '识别为：写作任务', 'node': 'intent_classifier', 'details': {'intent': 'writing'}, 'timestamp': '2025-11-11T20:45:11.677882', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 3, 'total_steps': 3, 'step_description': '第 3/3 步', 'elapsed': 0.0}
20:45:11 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:45:11 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=intent_analysis, desc=识别为：写作任务
20:45:11 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
20:45:11 Action.writing INFO   [writing] PromptManager已初始化
20:45:11 Action.writing INFO   [writing] work_id=7caa9cfb-e028-4d84-9eb3-42550d11d3a4, chapter_id=7295d191-a203-47f1-bdd7-9ff28258cff1, phase=None, chapter_num=None
20:45:11 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=None, chapter_num=None
20:45:11 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
20:45:15 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:45:23 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=91547b89-8fc1-4ad8-976c-58632b20b02c, model=unknown, duration=12.19s, tokens=N/A
20:45:23 app.services.agent.langgraph_agent INFO   [LangGraph] 检测到工具调用: 1 个工具
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-11T20:45:23.881492', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 5, 'total_steps': 5, 'step_description': '第 5/5 步', 'elapsed': 12.2}
20:45:23 app.api.v1.agent INFO   [Stream] Activity完成: intent_analysis (12.2s)
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:45:23 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=intent_analysis, elapsed=12.2s
20:45:23 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
20:45:23 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 工具分组: 并行=1, 串行=0
20:45:23 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 开始并行执行1个工具
20:45:23 app.services.agent.parallel_tool_node INFO   [ParallelToolNode] 并行执行完成，成功=1，失败=0
20:45:23 app.services.agent.langgraph_agent INFO   [LangGraph] 工具执行完毕，路由回: writing_agent
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _route_after_tools
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: tools
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'tool_execution', 'description': '📚 正在读取第?章...', 'node': 'tools', 'details': {'tools': ['get_chapter_by_order_tool'], 'tool_args': {}}, 'timestamp': '2025-11-11T20:45:23.898598', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 7, 'total_steps': 7, 'step_description': '第 7/7 步', 'elapsed': 12.3}
20:45:23 app.api.v1.agent INFO   [Stream] Activity完成: thinking (0.0s)
20:45:23 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:45:23 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.0s
20:45:23 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=tool_execution, desc=📚 正在读取第?章...
20:45:23 app.services.agent.langgraph_agent INFO   [LangGraph] 处理写作请求（新架构）
20:45:23 Action.writing INFO   [writing] PromptManager已初始化
20:45:23 Action.writing INFO   [writing] 从消息中识别到章节号: 1
20:45:23 Action.writing INFO   [writing] 章节 1 属于阶段: opening
20:45:23 Action.writing INFO   [writing] work_id=7caa9cfb-e028-4d84-9eb3-42550d11d3a4, chapter_id=7295d191-a203-47f1-bdd7-9ff28258cff1, phase=opening, chapter_num=1
20:45:23 app.services.agent.langgraph_agent INFO   [LangGraph] WritingAction准备完成: phase=opening, chapter_num=1
20:45:23 app.services.agent.langgraph_agent INFO   [LangGraph] 处理writing场景 (use_chatgpt=True)
20:45:23 app.services.agent.langgraph_agent INFO   [LangGraph] writing - 处理工具执行结果 (ChatOpenAI)
20:45:26 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
20:45:43 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=10994675-01b4-438c-a39b-860938089cd0, model=unknown, duration=19.35s, tokens=N/A
20:45:43 app.services.agent.langgraph_agent INFO   [LangGraph] 无需工具调用，结束流程
20:45:43 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: _should_continue
20:45:43 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: writing_agent
20:45:43 app.services.agent.langgraph_agent INFO   [Stream Event] progress_event = {'type': 'progress', 'step': 'thinking', 'description': '正在思考如何帮助您...', 'node': 'writing_agent', 'details': {}, 'timestamp': '2025-11-11T20:45:43.244441', 'progress': 100.0, 'eta': 0, 'eta_display': '即将完成', 'eta_confidence': 'high', 'current_step': 7, 'total_steps': 7, 'step_description': '第 7/7 步', 'elapsed': 31.6}
20:45:43 app.api.v1.agent INFO   [Stream] Activity完成: tool_execution (19.3s)
20:45:43 app.services.agent.langgraph_agent INFO   [Stream Event] on_progress 回调已调用
20:45:43 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=tool_execution, elapsed=19.3s
20:45:43 app.api.v1.agent INFO   [SSE] 发送 progress 事件: step=thinking, desc=正在思考如何帮助您...
20:45:43 app.services.agent.langgraph_agent INFO   [Stream Event] 节点: LangGraph
20:45:43 app.services.agent.langgraph_agent INFO   [LangGraph Stream] 流式执行完成，共48个事件
Batches: 100%|█████████████████████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00,  9.92it/s]
20:45:43 app.services.context.manager INFO   ✅ 保存长期记忆 | ID=602f5147-846a-4cde-9... | 重要度=0.60 | 长度=633
20:45:43 app.services.context.store INFO   [ContextStore] 保存上下文: f8528ea5-3111-4c45-8f7c-2408d12e5412, token=1385
20:45:43 app.services.context.manager INFO   [ContextManager] 更新上下文: f8528ea5-3111-4c45-8f7c-2408d12e5412, 消息数=2, Token=1385
20:45:43 app.services.agent.langgraph_agent INFO   [Context] 上下文已更新: f8528ea5-3111-4c45-8f7c-2408d12e5412
20:45:43 app.services.agent.progress_tracker INFO   [ProgressTracker] 状态已重置
20:45:43 app.api.v1.agent INFO   [Stream] 最后活动完成: thinking (0.3s)
20:45:43 app.api.v1.agent INFO   [SSE] 发送 activity_complete 事件: step=thinking, elapsed=0.3s
20:45:43 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: react, Stream completed
