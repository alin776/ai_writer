2026-01-26 16:19:59,638 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:56954 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 16:19:59,646 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 第1章读起来像流水账，帮我改得更有小说味一点...
2026-01-26 16:19:59,654 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=6, 规范=无
2026-01-26 16:19:59,655 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, conversation_id=b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:19:59,657 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f
2026-01-26 16:19:59,657 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f: 0/16000 tokens
2026-01-26 16:19:59,729 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='第1章读起来像流水账，帮我改得更有小说味一点...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=1条
2026-01-26 16:19:59,730 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 含用户级=True | 找到=1条
2026-01-26 16:19:59,738 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 1条消息, 0 tokens, 耗时 82.66ms
2026-01-26 16:19:59,738 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 1 条历史消息 (token: 0, has_summary: False)
2026-01-26 16:19:59,738 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:19:59,739 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:19:59,739 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:20:01,044 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:20:01,045 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:20:01,054 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:20:01,055 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=361, cost=$0.000042, time=1306ms
2026-01-26 16:20:01,056 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-26 16:20:01,057 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:20:01,058 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:20:01,058 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:20:02,228 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:20:02,229 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:20:02,246 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:20:02,247 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=298, cost=$0.000030, time=1171ms
2026-01-26 16:20:02,247 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 16:20:02,247 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 16:20:02,248 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 16:20:02,248 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 第1章读起来像流水账，帮我改得更有小说味一点...
2026-01-26 16:20:02,253 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:20:02,258 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:20:02,258 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:20:02,258 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:20:22,104 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:20:26,892 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 11 个数据块，总长度: 1453
2026-01-26 16:20:26,892 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22115 (prompt=21460, completion=655)
2026-01-26 16:20:26,892 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:20:26,892 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:20:26,900 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:20:26,900 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22115, cost=$0.033375, time=24635ms
2026-01-26 16:20:26,900 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22115
2026-01-26 16:20:26,900 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望修改第一章，使其更有小说感，不再像流水账。这是一个创, 原料=为了进行高质量的改写，我需要先阅读第一章, 处理=这是一个创作类请求，应采用分阶段执行的策
2026-01-26 16:20:26,900 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 76
2026-01-26 16:20:26,900 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-26 16:20:26,900 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 24.65s
2026-01-26 16:20:26,900 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-26 16:20:26,900 - app.services.agent.langgraph_agent - WARNING - [Planning-Alert] AI 违反协议：同时返回 direct_answer(76字) 和 2 个 tasks，将执行 tasks 而忽略 direct_answer
2026-01-26 16:20:26,910 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:20:26,910 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:20:26,910 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:20:26,911 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=2, 有依赖任务=1
2026-01-26 16:20:26,911 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 读取当前章节（第一章）的原文内容，为后续的分析和改写做准备。
2026-01-26 16:20:26,911 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节（第一章）的原文内容，为后续的分析和改写做准备。 (icon=Wrench)
2026-01-26 16:20:26,912 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:20:26,912 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=读取章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 的内容，为改写做...
2026-01-26 16:20:26,912 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['第一章']
2026-01-26 16:20:26,912 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第484-600章
2026-01-26 16:20:26,912 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=读取章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 的内容，为改写做...
2026-01-26 16:20:26,912 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:20:26,920 - app.services.agent.tools.explore_tools - INFO - [_extract_keywords] 提取关键词: ['bc18c9d1', 'f600', '484f', 'ab5a', 'bead3c7a6803', '读取', '章节', '改写', '内容', '准备']...
2026-01-26 16:20:26,920 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用提取的关键词: ['bc18c9d1', 'f600', '484f', 'ab5a', 'bead3c7a6803', '读取', '章节', '改写', '内容', '准备']
2026-01-26 16:20:26,920 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围: (484, 600)
2026-01-26 16:20:26,940 - app.services.chapter_vector_service - INFO - [exact_search] work=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, keywords=['bc18c9d1', 'f600', '484f']..., mode=any, range=(484, 600), hits=0
2026-01-26 16:20:26,940 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 0 条
2026-01-26 16:20:26,942 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段3：AI 补充循环，当前 0 条证据
2026-01-26 16:20:26,942 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:20:26,942 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:20:26,943 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.3, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:20:50,314 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:20:50,314 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:20:50,328 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:20:50,328 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2435, cost=$0.007025, time=23370ms
2026-01-26 16:20:50,328 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=722, 尝试次数=1
2026-01-26 16:20:50,328 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 任务理解完成: 核心任务是定位并全面理解一个由UUID标识的特定章节，包括其内容、情节、人物关系及在整个作品中的作用，为改写提供充分的原始信息和背景支持。...
2026-01-26 16:20:50,328 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:20:50,333 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:20:50,333 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:20:51,882 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:20:51,882 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:20:51,898 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:20:51,898 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=946, cost=$0.000166, time=1549ms
2026-01-26 16:20:51,898 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=394, 尝试次数=1
2026-01-26 16:20:51,898 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, type=<class 'uuid.UUID'>
2026-01-26 16:20:51,898 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:20:51,898 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:20:51,906 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:20:51,906 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:20:51,917 - app.services.agent.tools.explore_tools - WARNING - [ContentExplorer] 章节范围映射为空，保持原始范围: 第484-600章
2026-01-26 16:20:51,917 - app.services.agent.tools.explore_tools - WARNING - [ContentExplorer] 章节范围解析失败: {
  "error": "未找到第484章",
  "work_id": "be92c72a-311f-4ebb-9d5f-78ce68aeb73d",
  "total_chapters": 5
}
2026-01-26 16:20:51,928 - app.services.agent.tools.explore_tools - WARNING - [ContentExplorer] 章节范围解析失败: {
  "error": "未找到第484章",
  "work_id": "be92c72a-311f-4ebb-9d5f-78ce68aeb73d",
  "total_chapters": 5
}
2026-01-26 16:20:51,929 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-26 16:20:51,929 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 的原始内容文本...
2026-01-26 16:20:52,013 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:20:52,520 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:20:52,520 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:20:52,527 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 的核心情节摘要...
2026-01-26 16:20:52,597 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:20:53,070 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:20:53,074 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:20:53,076 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 在作品结构中的功能...
2026-01-26 16:20:53,149 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:20:53,600 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 9 个候选 -> top 5
2026-01-26 16:20:53,608 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:20:53,610 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:20:53,610 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:20:53,611 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:21:13,029 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:21:13,030 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:21:13,039 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:21:13,040 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2676, cost=$0.005025, time=19419ms
2026-01-26 16:21:13,040 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=410, 尝试次数=1
2026-01-26 16:21:13,041 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "第一章": false
  },
  "chapters_with_evidence": [],
  "has_direct_quotes": false,
  "has_character_interactions": false,
  "has_plot_details": false,
  "summary": "已收集信息定义了任务范围为第484-600章。目前没有已读章节原文或证据片段，仅有24个世界观条目。",
  "next_action": "基于收集到的章节原文、情节细节和人物互动，整理出该章节的核心情节摘要、人物关系变化以及其在作品结构中的作用，并据此进行改写。",
  "potential_gaps": [
    "章节原始内容文本",
    "具体情节细节",
    "人物互动描写"
  ]
}
```
2026-01-26 16:21:13,041 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=0/1, 章节=[], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:21:13,041 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=0, 章节=0, 关键词覆盖=0.0%, 质量=0/3
2026-01-26 16:21:13,041 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节覆盖不足: missing=[484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600]
2026-01-26 16:21:13,042 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:21:13,042 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:21:13,042 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:21:15,667 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:21:15,667 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:21:15,676 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:21:15,676 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1107, cost=$0.000230, time=2625ms
2026-01-26 16:21:15,676 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=605, 尝试次数=1
2026-01-26 16:21:15,676 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 的上下文情节...
2026-01-26 16:21:15,754 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:21:16,239 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:21:16,239 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:21:16,241 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 中人物关系及状态变化...
2026-01-26 16:21:16,312 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:21:16,779 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:21:16,779 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:21:16,787 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 的叙事风格、基调和情...
2026-01-26 16:21:16,859 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:21:17,254 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:21:17,255 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:21:17,255 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:21:17,255 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:21:17,255 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:21:32,237 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:21:32,237 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:21:32,248 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:21:32,250 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2233, cost=$0.004944, time=14982ms
2026-01-26 16:21:32,250 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=478, 尝试次数=1
2026-01-26 16:21:32,250 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "第一章": false
  },
  "chapters_with_evidence": [],
  "has_direct_quotes": false,
  "has_character_interactions": false,
  "has_plot_details": false,
  "summary": "已收集的信息定义了任务范围为第484-600章，并包含24个世界观条目。目前没有已读的章节原文或从章节中提取的证据片段。",
  "next_action": "基于任务要求，下一步将首先定位并阅读目标章节（bc18c9d1-f600-484f-ab5a-bead3c7a6803）的原文。然后，将结合已有的24个世界观条目，提取章节的核心情节、人物互动、上下文关系及叙事特征，以完成为改写做准备的目标。",
  "potential_gaps": [
    "章节原始内容文本",
    "章节核心情节",
    "上下文情节"
  ]
}
```
2026-01-26 16:21:32,250 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=0/1, 章节=[], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:21:32,250 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=0, 章节=0, 关键词覆盖=0.0%, 质量=0/3
2026-01-26 16:21:32,252 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节覆盖不足: missing=[484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600]
2026-01-26 16:21:32,252 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 2轮, 原因=连续无新增信息（覆盖不足）
2026-01-26 16:21:32,252 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:21:32,253 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节（第一章）的原文内容，为后续的分析和改写做准备。 (65.3s)
2026-01-26 16:21:32,253 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:21:32,253 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 分析第一章的文本，诊断其读起来像“流水账”的具体原因，例如叙事平淡、缺少细节、节奏过快等。
2026-01-26 16:21:32,253 - app.api.v1.agent - INFO - [Stream] Task started: 分析第一章的文本，诊断其读起来像“流水账”的具体原因，例如叙事平淡、缺少细节、节奏过快等。 (icon=FileSearch)
2026-01-26 16:21:32,253 - app.services.agent.parameter_resolver - WARNING - [ParameterResolver] 数组索引 0 越界，降级返回完整结果
2026-01-26 16:21:32,254 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-26 16:21:32,254 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.text: None → ''
2026-01-26 16:21:32,254 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 的 text 参数为空或含占位符，使用 context 兜底（1203字符）
2026-01-26 16:21:32,254 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析文本读起来像流水账的原因...'
2026-01-26 16:21:32,254 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-26 16:21:32,257 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-26 16:21:32,264 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:21:32,264 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=quality_evaluation, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: quality_evaluation; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2026-01-26 16:21:32,264 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2500, temp=0.3, task_type=TaskType.QUALITY_EVALUATION
2026-01-26 16:21:33,730 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:21:44,196 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 38 个数据块，总长度: 3316
2026-01-26 16:21:44,196 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3353 (prompt=1155, completion=2198)
2026-01-26 16:21:44,196 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:21:44,196 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:21:44,205 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:21:44,205 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3353, cost=$0.000995, time=11931ms
2026-01-26 16:21:44,205 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 11.948s)
2026-01-26 16:21:44,209 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-26 16:21:44,209 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-26 16:21:44,209 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第一章的文本，诊断其读起来像“流水账”的具体原因，例如叙事平淡、缺少细节、节奏过快等。 (12.0s)
2026-01-26 16:21:44,209 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:21:44,209 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 77.30s
2026-01-26 16:21:44,209 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-26 16:21:44,209 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=3875字符, 处理后=3955字符
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:21:44,209 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:21:44,209 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:21:44,209 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:21:44,216 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:21:44,217 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:21:44,217 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:21:57,118 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:21:57,118 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:21:57,119 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:22:03,724 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 21 个数据块，总长度: 1984
2026-01-26 16:22:03,724 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 9181 (prompt=7862, completion=1319)
2026-01-26 16:22:03,724 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:22:03,724 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:22:03,734 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:22:03,739 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9181, cost=$0.005656, time=19507ms
2026-01-26 16:22:03,739 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1984
2026-01-26 16:22:04,169 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 重要度=0.77
2026-01-26 16:22:04,173 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, token=2083
2026-01-26 16:22:04,173 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 消息数=2, 摘要长度=0, Token=2083
2026-01-26 16:22:04,173 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:22:04,173 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:22:04,178 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:22:21,229 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f
INFO:     127.0.0.1:54368 - "GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f HTTP/1.1" 200 OK
2026-01-26 16:23:20,965 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:23:20,965 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:23:20,965 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:23:22,465 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:23:22,465 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 16:23:22,465 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:49571 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 16:23:22,476 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 段融吞噬器灵那段太平淡了，这可是金手指第一次发动，应该更有仪式感...
2026-01-26 16:23:22,482 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=6, 规范=无
2026-01-26 16:23:22,483 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, conversation_id=b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:23:22,488 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 2条消息
2026-01-26 16:23:22,492 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f: 2083/16000 tokens
2026-01-26 16:23:22,564 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='段融吞噬器灵那段太平淡了，这可是金手指第一次发动，应该更有仪...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-26 16:23:22,564 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 含用户级=True | 找到=0条
2026-01-26 16:23:22,575 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 2条消息, 2083 tokens, 耗时 91.56ms
2026-01-26 16:23:22,575 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 2 条历史消息 (token: 2083, has_summary: False)
2026-01-26 16:23:22,575 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:23:22,575 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:23:22,575 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:23:23,919 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:23:23,920 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:23:23,935 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:23:23,938 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1713, cost=$0.000177, time=1345ms
2026-01-26 16:23:23,939 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-26 16:23:23,939 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:23:23,940 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:23:23,940 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:23:24,776 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:23:24,776 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:23:24,786 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:23:24,787 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=302, cost=$0.000030, time=836ms
2026-01-26 16:23:24,788 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-26 16:23:24,788 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-26 16:23:24,788 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-26 16:23:24,788 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 段融吞噬器灵那段太平淡了，这可是金手指第一次发动，应该更有仪式感...
2026-01-26 16:23:24,791 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:23:24,795 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:23:24,796 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:23:24,796 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:23:47,576 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:23:55,562 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 16 个数据块，总长度: 2202
2026-01-26 16:23:55,563 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23982 (prompt=23000, completion=982)
2026-01-26 16:23:55,563 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:23:55,563 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:23:55,580 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:23:55,580 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23982, cost=$0.038570, time=30766ms
2026-01-26 16:23:55,580 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23982
2026-01-26 16:23:55,588 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望改写'段融吞噬器灵'的段落，使其更有仪式感和冲击力，, 原料=需要读取当前章节内容，并定位到'吞噬器灵, 处理=这是一个典型的“改写”场景，应该遵循“获
2026-01-26 16:23:55,588 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-26 16:23:55,588 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 30.80s
2026-01-26 16:23:55,588 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-26 16:23:55,588 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:23:55,588 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:23:55,588 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:23:55,588 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-01-26 16:23:55,588 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在当前章节中定位并获取用户指定的“段融吞噬器灵那段”的原文内容，为改写做准备。
2026-01-26 16:23:55,588 - app.api.v1.agent - INFO - [Stream] Task started: 在当前章节中定位并获取用户指定的“段融吞噬器灵那段”的原文内容，为改写做准备。 (icon=Wrench)
2026-01-26 16:23:55,588 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:23:55,593 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=定位并获取'段融吞噬器灵'的原文段落...
2026-01-26 16:23:55,593 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段融', '吞噬', '器灵', '赵穆', '佩刀']
2026-01-26 16:23:55,593 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=定位并获取'段融吞噬器灵'的原文段落...
2026-01-26 16:23:55,594 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:23:55,594 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用规划传入的关键词: ['段融', '吞噬', '器灵', '赵穆', '佩刀']
2026-01-26 16:23:55,632 - app.services.chapter_vector_service - INFO - [exact_search] work=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, keywords=['段融', '吞噬', '器灵']..., mode=any, range=None, hits=100
2026-01-26 16:23:55,633 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 100 条
2026-01-26 16:23:55,634 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 100 条
2026-01-26 16:23:55,634 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 100 条证据)
2026-01-26 16:23:55,635 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:23:55,635 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:23:55,636 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:24:09,225 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:24:09,225 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:24:09,239 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:24:09,241 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2207, cost=$0.005139, time=13588ms
2026-01-26 16:24:09,241 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=541, 尝试次数=1
2026-01-26 16:24:09,241 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true,
    "吞噬": true,
    "器灵": true,
    "赵穆": true,
    "佩刀": false
  },
  "chapters_with_evidence": [
    1,
    2,
    3
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "已收集的信息包含角色段融和赵穆的互动，提及段融的身体状况、赵穆演练刀法，以及段融在梦境中能“看见”内息流转。证据片段来自第1、2、3章。",
  "next_action": "基于关键词“段融”、“吞噬”、“器灵”均有覆盖，下一步将检索并分析这些关键词共同出现的证据片段，以定位并获取描述“段融吞噬器灵”的原文段落。",
  "potential_gaps": [
...
2026-01-26 16:24:09,241 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=4/5, 章节=[1, 2, 3], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:24:09,241 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=100, 章节=3, 关键词覆盖=80.0%, 质量=0/3
2026-01-26 16:24:09,241 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 16:24:09,241 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 判断信息充足，跳过补充循环: 证据充足：100条证据，覆盖3个章节，关键词覆盖80%
2026-01-26 16:24:09,256 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,256 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 2 -> UUID fd3a6888-aac3-43f8-a8da-fcacc17d3836
2026-01-26 16:24:09,266 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 3 -> UUID 0a038ff1-17a0-411f-a9ad-da8031878324
2026-01-26 16:24:09,272 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,277 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,281 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,285 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,289 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,293 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,297 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,303 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,310 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,316 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:24:09,316 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:24:09,316 - app.api.v1.agent - INFO - [Stream] 任务完成: 在当前章节中定位并获取用户指定的“段融吞噬器灵那段”的原文内容，为改写做准备。 (13.7s)
2026-01-26 16:24:09,316 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:24:09,316 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户要求，将金手指首次发动的过程改写得更有仪式感和冲击力，增加心理、感官和过程描写。
2026-01-26 16:24:09,316 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，将金手指首次发动的过程改写得更有仪式感和冲击力，增加心理、感官和过程描写。 (icon=Edit3)
2026-01-26 16:24:09,316 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-26 16:24:09,316 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-26 16:24:09,330 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 4547, 用户要求: 将这段吞噬器灵的描写改写得更有仪式感和冲击力，突出金手指首次发动的震撼感，不要像流水账。需要详细描写主角的内心感受、能力的运作过程以及吞噬完成后的变化。
2026-01-26 16:24:09,331 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-26 16:24:09,331 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:24:09,332 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:24:09,332 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-26 16:24:39,331 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:24:39,331 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:24:39,341 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:24:39,341 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6990, cost=$0.013909, time=29998ms
2026-01-26 16:24:39,343 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=758, 尝试次数=1
2026-01-26 16:24:39,343 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 758
2026-01-26 16:24:39,343 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-01-26 16:24:39,345 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 30.029s)
2026-01-26 16:24:39,345 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-26 16:24:39,345 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，将金手指首次发动的过程改写得更有仪式感和冲击力，增加心理、感官和过程描写。 (30.0s)
2026-01-26 16:24:39,345 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:24:39,348 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将AI生成的新段落替换掉原文中平淡的段落。
2026-01-26 16:24:39,348 - app.api.v1.agent - INFO - [Stream] Task started: 将AI生成的新段落替换掉原文中平淡的段落。 (icon=Check)
2026-01-26 16:24:39,348 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-01-26 16:24:39,349 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-01-26 16:24:39,349 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=replace, chapter=bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:24:39,349 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace, needs_locate=True
2026-01-26 16:24:39,353 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=bc18c9d1-f600-484f-ab5a-bead3c7a6803, query=## 相关片段 - [1章20段] 就在这时，段融抹了把额头的细汗，从角门跑进了这片院子。 - [1章22段] 段融穿了一身褐色短打，身体略显单薄，但这都是长期吃不饱肚子，给饿得。 - [1章24段] 段融扫了一眼院子里的人数，大约只有十多个人了。 - [1章26段] 段融叹了口气，不过他其实能够理解走了的那些人的想法，这些杂役弟子每天都要辛苦劳作，傍晚还要到此处练功，要是有奔头，还能咬牙坚持下
2026-01-26 16:24:39,363 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 70 个段落
2026-01-26 16:24:39,364 - app.services.agent.tools.locate_tools - INFO - [locate_content] 模糊匹配结果: None
2026-01-26 16:24:39,364 - app.services.agent.tools.locate_tools - INFO - [locate_content] 无模糊匹配结果，尝试 LLM 辅助定位
2026-01-26 16:24:39,378 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] 开始调用 LLM，候选数量: 8
2026-01-26 16:24:39,379 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:24:39,379 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:24:39,380 - app.services.ai.http_ai_service - INFO - [成本追踪] 初始化未传db/user_id，将使用请求上下文按需记录成本
2026-01-26 16:24:40,765 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:24:40,766 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:24:40,766 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:24:40,767 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:24:42,260 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:24:42,260 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:24:42,275 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:24:42,275 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=534, cost=$0.000054, time=1493ms
2026-01-26 16:24:42,275 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-26 16:24:42,275 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] LLM 选择候选 1 → 原始第 12 段
2026-01-26 16:24:42,275 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位返回: (11, 0.85)
2026-01-26 16:24:42,281 - app.services.agent.tools.locate_tools - WARNING - [locate_content] LLM 辅助定位候选缺乏关键词匹配，忽略: 第12段
2026-01-26 16:24:42,281 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节内未找到，尝试全局搜索: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:24:42,281 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1000000, query=## 相关片段 - [1章20段] 就在这时，段融抹了把额头的细汗，从角门跑进了这片院子。 - [1...
2026-01-26 16:24:42,481 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 16:25:06,315 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 15 个候选 -> top 5
2026-01-26 16:25:06,315 - app.services.agent.tools.locate_tools - INFO - [_llm_rerank] top-2 相似度接近 (1.00 vs 1.00)，调用 LLM 重排序
2026-01-26 16:25:06,315 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:25:06,317 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:25:06,317 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:25:07,814 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:25:07,814 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:25:07,826 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:25:07,831 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=384, cost=$0.000039, time=1497ms
2026-01-26 16:25:07,832 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-26 16:25:07,832 - app.services.agent.tools.locate_tools - INFO - [_llm_rerank] LLM 选择候选 3
2026-01-26 16:25:07,837 - app.services.agent.tools.locate_tools - INFO - [locate_content] 全局降级成功: chapter=0c076d6c-abc8-4077-a518-05d24f3e12ce, para=20
2026-01-26 16:25:07,845 - app.services.agent.tools.operate_tools - WARNING - [Operate] 全局降级：定位到其他章节 0c076d6c-abc8-4077-a518-05d24f3e12ce，原章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:25:07,845 - app.services.agent.tools.operate_tools - WARNING - [Operate] 跨章节定位：原章节 bc18c9d1-f600-484f-ab5a-bead3c7a6803 → 实际章节 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:25:07,845 - app.services.agent.tools.operate_tools - INFO - [Operate] 定位完成: method=text_match, para=20
2026-01-26 16:25:07,846 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=0c076d6c-abc8-4077-a518-05d24f3e12ce, operation=replace, content_len=642
2026-01-26 16:25:07,866 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 28.516s)
2026-01-26 16:25:07,866 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-01-26 16:25:07,877 - app.api.v1.agent - INFO - [Stream] 任务完成: 将AI生成的新段落替换掉原文中平淡的段落。 (28.5s)
2026-01-26 16:25:07,877 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-26 16:25:07,877 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 72.29s
2026-01-26 16:25:07,878 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:25:07,879 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:25:07,879 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-26 16:25:07,879 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:25:07,880 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:25:07,880 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=8583字符, 处理后=8711字符
2026-01-26 16:25:07,881 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:25:07,881 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:25:07,881 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:25:07,882 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:25:07,882 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:25:07,891 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:25:07,891 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:25:07,892 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:25:12,096 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: be92c72a-311f-4ebb-9d5f-78ce68aeb73d, chapter_id: 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:25:12,105 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:25:12,105 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:25:12,108 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54934 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:25:12,116 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: be92c72a-311f-4ebb-9d5f-78ce68aeb73d, chapter_id: 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:25:12,119 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:25:12,120 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:25:12,121 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce/revisions
INFO:     127.0.0.1:65168 - "GET /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:25:12,124 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:65167 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:25:12,138 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce/revisions
INFO:     127.0.0.1:56966 - "GET /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:25:12,198 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:25:12,199 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce
INFO:     127.0.0.1:58535 - "PUT /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce HTTP/1.1" 200 OK
2026-01-26 16:25:12,202 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:25:14,422 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:25:14,426 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:25:14,426 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:25:14,468 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:25:14,525 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:25:14,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce
INFO:     127.0.0.1:58489 - "PUT /api/v1/chapters/0c076d6c-abc8-4077-a518-05d24f3e12ce HTTP/1.1" 200 OK
2026-01-26 16:25:14,528 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:25:16,922 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 5 个数据块，总长度: 377
2026-01-26 16:25:16,923 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 12288 (prompt=12015, completion=273)
2026-01-26 16:25:16,923 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:25:16,924 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:25:16,938 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:25:16,943 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:25:16,944 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=12288, cost=$0.004287, time=9030ms
2026-01-26 16:25:16,945 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=377
2026-01-26 16:25:18,162 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 重要度=0.60
2026-01-26 16:25:18,173 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, token=2565
2026-01-26 16:25:18,174 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 消息数=4, 摘要长度=0, Token=2565
2026-01-26 16:25:18,175 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:25:18,175 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:25:18,181 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:25:50,761 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: be92c72a-311f-4ebb-9d5f-78ce68aeb73d, chapter_id: bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:25:50,769 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:25:50,772 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 22e5d51e-481e-431f-b7e4-b79fadcc832c
2026-01-26 16:25:50,772 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:25:50,777 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:25:50,778 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: be92c72a-311f-4ebb-9d5f-78ce68aeb73d, chapter_id: bc18c9d1-f600-484f-ab5a-bead3c7a6803
INFO:     127.0.0.1:58637 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:25:50,784 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:25:50,786 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 22e5d51e-481e-431f-b7e4-b79fadcc832c
2026-01-26 16:25:50,786 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:25:50,787 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803/revisions
INFO:     127.0.0.1:62361 - "GET /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:25:50,788 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62360 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:25:50,805 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803/revisions
INFO:     127.0.0.1:53527 - "GET /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:25:50,956 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f
INFO:     127.0.0.1:62341 - "GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f HTTP/1.1" 200 OK
2026-01-26 16:25:50,979 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f
INFO:     127.0.0.1:52873 - "GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f HTTP/1.1" 200 OK
2026-01-26 16:25:51,033 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:25:51,035 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803
INFO:     127.0.0.1:62342 - "PUT /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803 HTTP/1.1" 200 OK
2026-01-26 16:25:51,036 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:25:54,066 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:25:54,106 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:25:54,107 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803
INFO:     127.0.0.1:58131 - "PUT /api/v1/chapters/bc18c9d1-f600-484f-ab5a-bead3c7a6803 HTTP/1.1" 200 OK
2026-01-26 16:25:54,108 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:25:56,712 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:27:00,667 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:27:00,668 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:27:00,668 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:27:02,231 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:27:02,231 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 16:27:02,231 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:59011 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 16:27:02,241 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 赵穆出场到离开这段，情绪起伏太弱，帮我加强一下压迫感和段融的隐忍...
2026-01-26 16:27:02,249 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=6, 规范=无
2026-01-26 16:27:02,250 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, conversation_id=b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:27:02,252 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 4条消息
2026-01-26 16:27:02,252 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f: 2565/16000 tokens
2026-01-26 16:27:02,352 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='赵穆出场到离开这段，情绪起伏太弱，帮我加强一下压迫感和段融的...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=1条
2026-01-26 16:27:02,355 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 含用户级=True | 找到=1条
2026-01-26 16:27:02,399 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 5条消息, 2565 tokens, 耗时 148.96ms
2026-01-26 16:27:02,399 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 5 条历史消息 (token: 2565, has_summary: False)
2026-01-26 16:27:02,399 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:27:02,399 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:27:02,399 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:27:04,109 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:27:04,109 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:27:04,127 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:27:04,130 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1726, cost=$0.000178, time=1710ms
2026-01-26 16:27:04,130 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-26 16:27:04,130 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:27:04,132 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:27:04,132 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:27:04,944 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:27:04,945 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:27:04,959 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:27:04,961 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=308, cost=$0.000031, time=814ms
2026-01-26 16:27:04,961 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 16:27:04,963 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 16:27:04,963 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 16:27:04,964 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 赵穆出场到离开这段，情绪起伏太弱，帮我加强一下压迫感和段融的隐忍...
2026-01-26 16:27:04,973 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:27:04,980 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:27:04,981 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:27:04,982 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:27:20,282 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:27:29,073 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 18 个数据块，总长度: 2237
2026-01-26 16:27:29,073 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23832 (prompt=22762, completion=1070)
2026-01-26 16:27:29,073 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:27:29,073 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:27:29,088 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:27:29,088 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23832, cost=$0.039152, time=24093ms
2026-01-26 16:27:29,088 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23832
2026-01-26 16:27:29,088 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望改写一个特定段落，使其更有戏剧冲突。具体来说，是“赵, 原料=为了准确改写，我需要：
1. 读取当前章, 处理=处理流程如下：
1. 使用 `explo
2026-01-26 16:27:29,088 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-26 16:27:29,088 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 24.12s
2026-01-26 16:27:29,088 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-26 16:27:29,088 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:27:29,088 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:27:29,088 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:27:29,088 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-01-26 16:27:29,088 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 读取当前章节的完整内容，以定位需要改写的段落。
2026-01-26 16:27:29,097 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节的完整内容，以定位需要改写的段落。 (icon=Wrench)
2026-01-26 16:27:29,097 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=读取第一章的全部内容，用于定位并改写赵穆出场的段落...
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['赵穆', '段融', '佩刀', '擦拭']
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1章
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=读取第一章的全部内容，用于定位并改写赵穆出场的段落...
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用规划传入的关键词: ['赵穆', '段融', '佩刀', '擦拭']
2026-01-26 16:27:29,097 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围: (1, 1)
2026-01-26 16:27:29,109 - app.services.chapter_vector_service - INFO - [exact_search] work=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, keywords=['赵穆', '段融', '佩刀']..., mode=any, range=(1, 1), hits=32
2026-01-26 16:27:29,109 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 32 条
2026-01-26 16:27:29,109 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 32 条
2026-01-26 16:27:29,109 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 32 条证据)
2026-01-26 16:27:29,109 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:27:29,109 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:27:29,109 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:27:43,032 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:27:43,032 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:27:43,044 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:27:43,044 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2070, cost=$0.004653, time=13922ms
2026-01-26 16:27:43,044 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=479, 尝试次数=1
2026-01-26 16:27:43,044 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "赵穆": true,
    "段融": true,
    "佩刀": false,
    "擦拭": false
  },
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "已收集的信息来自第1章，包含32条证据片段。内容提及了“赵穆”和“段融”两位角色，并有关于段融外貌和行动的描述。",
  "next_action": "基于已收集的第1章中关于“赵穆”和“段融”的32条证据片段，定位赵穆出场的具体段落，并根据任务要求进行改写。",
  "potential_gaps": [
    "佩刀的描述",
    "擦拭动作的描写"
  ]
}
```
2026-01-26 16:27:43,044 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=2/4, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:27:43,044 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=32, 章节=1, 关键词覆盖=50.0%, 质量=0/3
2026-01-26 16:27:43,044 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 16:27:43,044 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 判断信息充足，跳过补充循环: 证据充足：32条证据，覆盖1个章节，关键词覆盖50%
2026-01-26 16:27:43,054 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,059 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,062 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,062 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,062 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,071 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,072 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,072 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,072 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,082 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,082 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:27:43,087 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:27:43,087 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节的完整内容，以定位需要改写的段落。 (14.0s)
2026-01-26 16:27:43,087 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:27:43,087 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户要求，改写赵穆出场到离开的段落，加强压迫感和段融的隐忍。
2026-01-26 16:27:43,087 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，改写赵穆出场到离开的段落，加强压迫感和段融的隐忍。 (icon=Edit3)
2026-01-26 16:27:43,087 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-26 16:27:43,087 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-26 16:27:43,093 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 未提供text_to_rewrite，自动获取章节内容: bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:27:43,103 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 自动获取章节内容成功，长度: 4281
2026-01-26 16:27:43,106 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 4281, 用户要求: 请改写从赵穆出场到他离开的整个段落。核心要求是：1. 极大地增强赵穆的压迫感，通过他的语气、眼神、不耐烦的细微动作（如敲击桌面、轻蔑的嗤笑）来体现他的傲慢和对段融的轻视。2. 深刻地刻画段融的“隐忍”，通过描写他紧握的拳头、压抑的呼吸、低垂眼眸下隐藏的怒火，以及对自身弱小的无力感和对力量的极度渴望，来表现他内心的激烈冲突。
2026-01-26 16:27:43,106 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-26 16:27:43,106 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:27:43,106 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:27:43,106 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-26 16:28:32,839 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:28:32,841 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:28:32,851 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:28:32,853 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8673, cost=$0.022391, time=49734ms
2026-01-26 16:28:32,853 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1823, 尝试次数=1
2026-01-26 16:28:32,853 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 1823
2026-01-26 16:28:32,853 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-01-26 16:28:32,853 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 49.765s)
2026-01-26 16:28:32,853 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-26 16:28:32,853 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，改写赵穆出场到离开的段落，加强压迫感和段融的隐忍。 (49.8s)
2026-01-26 16:28:32,853 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:28:32,853 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将AI生成的新段落替换回原文。
2026-01-26 16:28:32,857 - app.api.v1.agent - INFO - [Stream] Task started: 将AI生成的新段落替换回原文。 (icon=Check)
2026-01-26 16:28:32,857 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-01-26 16:28:32,857 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-01-26 16:28:32,857 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=replace, chapter=bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:28:32,857 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace, needs_locate=True
2026-01-26 16:28:32,860 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=bc18c9d1-f600-484f-ab5a-bead3c7a6803, query=<p data-id="gg68k2ly">段融在想：兵器架上的废刀的器灵不是二阶就是三阶，而赵穆用的那柄好刀的器灵却是不入阶的。</p><p data-id="icd1uja3">也就是说器灵等级，其实与器物本身的好坏，没有直接的关系。</p><p data-id="1qj7ym7h">“那决定器灵等阶的，到底是什么？”</p><p data-id="cy3wol3t">段融眉头紧锁，苦苦沉思着
2026-01-26 16:28:32,868 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 70 个段落
2026-01-26 16:28:32,868 - app.services.agent.tools.locate_tools - INFO - [locate_content] 模糊匹配结果: None
2026-01-26 16:28:32,869 - app.services.agent.tools.locate_tools - INFO - [locate_content] 无模糊匹配结果，尝试 LLM 辅助定位
2026-01-26 16:28:32,873 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] 开始调用 LLM，候选数量: 8
2026-01-26 16:28:32,874 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:28:32,875 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:28:32,875 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:28:34,032 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:28:34,032 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:28:34,040 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:28:34,040 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=447, cost=$0.000045, time=1157ms
2026-01-26 16:28:34,040 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-26 16:28:34,040 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] LLM 选择候选 1 → 原始第 1 段
2026-01-26 16:28:34,040 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位返回: (0, 0.85)
2026-01-26 16:28:34,040 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位成功: 第1段
2026-01-26 16:28:34,045 - app.services.agent.tools.operate_tools - INFO - [Operate] 定位完成: method=text_match, para=0
2026-01-26 16:28:34,046 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=bc18c9d1-f600-484f-ab5a-bead3c7a6803, operation=replace, content_len=1689
2026-01-26 16:28:34,056 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 1.199s)
2026-01-26 16:28:34,056 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-01-26 16:28:34,061 - app.services.agent.utils.tool_cache - INFO - [ToolCache] invalidated 2 keys: tool_cache:*:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:chapter:bc18c9d1-f600-484f-ab5a-bead3c7a6803:*
2026-01-26 16:28:34,068 - app.api.v1.agent - INFO - [Stream] 任务完成: 将AI生成的新段落替换回原文。 (1.2s)
2026-01-26 16:28:34,068 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-26 16:28:34,068 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 64.98s
2026-01-26 16:28:34,068 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:28:34,068 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:28:34,068 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-26 16:28:34,068 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:28:34,069 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:28:34,069 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=13940字符, 处理后=4470字符
2026-01-26 16:28:34,069 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:28:34,069 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:28:34,069 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:28:34,070 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:28:34,070 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:28:34,075 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:28:34,075 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:28:34,075 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:28:43,900 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:28:43,902 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:28:43,902 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:28:45,907 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 7 个数据块，总长度: 508
2026-01-26 16:28:45,908 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 9207 (prompt=8829, completion=378)
2026-01-26 16:28:45,909 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:28:45,910 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:28:45,919 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:28:45,919 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9207, cost=$0.003594, time=11834ms
2026-01-26 16:28:45,919 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=508
2026-01-26 16:28:46,242 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 重要度=0.60
2026-01-26 16:28:46,249 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, token=3210
2026-01-26 16:28:46,250 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 消息数=6, 摘要长度=0, Token=3210
2026-01-26 16:28:46,250 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:28:46,251 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:28:46,254 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:28:51,666 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f
INFO:     127.0.0.1:64147 - "GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f HTTP/1.1" 200 OK
2026-01-26 16:31:07,249 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:31:07,249 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:31:07,249 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:31:08,846 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:31:08,846 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 16:31:08,853 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:58260 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 16:31:08,861 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 段融半夜练刀那段写得太实了，缺乏留白和想象空间，帮我改得更有意境...
2026-01-26 16:31:08,870 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=6, 规范=无
2026-01-26 16:31:08,870 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, conversation_id=b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:31:08,873 - app.services.context.store - INFO - [ContextStore] 加载上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 6条消息
2026-01-26 16:31:08,877 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f: 3210/16000 tokens
2026-01-26 16:31:08,976 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='段融半夜练刀那段写得太实了，缺乏留白和想象空间，帮我改得更有...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=3条
2026-01-26 16:31:08,976 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 含用户级=True | 找到=3条
2026-01-26 16:31:09,109 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 7条消息, 3210 tokens, 耗时 237.93ms
2026-01-26 16:31:09,109 - app.services.agent.langgraph_agent - INFO - [Planning] 从 ContextManager 加载了 7 条历史消息 (token: 3210, has_summary: False)
2026-01-26 16:31:09,110 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:31:09,111 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:31:09,111 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:31:10,578 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:31:10,578 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:31:10,599 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:31:10,599 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1747, cost=$0.000181, time=1466ms
2026-01-26 16:31:10,599 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-26 16:31:10,599 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:31:10,599 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:31:10,599 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:31:11,449 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:31:11,449 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:31:11,459 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:31:11,470 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=307, cost=$0.000031, time=849ms
2026-01-26 16:31:11,470 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 16:31:11,470 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 16:31:11,470 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 16:31:11,470 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 段融半夜练刀那段写得太实了，缺乏留白和想象空间，帮我改得更有意境...
2026-01-26 16:31:11,481 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:31:11,486 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:31:11,486 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:31:11,486 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:31:23,509 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:31:30,118 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 2002
2026-01-26 16:31:30,119 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 23737 (prompt=22825, completion=912)
2026-01-26 16:31:30,120 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:31:30,121 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:31:30,150 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:31:30,153 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=23737, cost=$0.037651, time=18636ms
2026-01-26 16:31:30,154 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=23737
2026-01-26 16:31:30,156 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望获得一段改写后的文本，这段文本需要更有意境，并替换掉, 原料=需要读取当前章节中“段融半夜练刀”的原始, 处理=首先，通过`explore_conten
2026-01-26 16:31:30,159 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-26 16:31:30,162 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 18.69s
2026-01-26 16:31:30,164 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-26 16:31:30,165 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:31:30,165 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:31:30,166 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:31:30,166 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-01-26 16:31:30,166 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在当前章节中，查找并读取“段融半夜练刀”的相关段落原文。
2026-01-26 16:31:30,167 - app.api.v1.agent - INFO - [Stream] Task started: 在当前章节中，查找并读取“段融半夜练刀”的相关段落原文。 (icon=Wrench)
2026-01-26 16:31:30,169 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:31:30,170 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=查找并读取第一章中段融半夜练刀的段落...
2026-01-26 16:31:30,171 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段融', '练刀', '半夜', '月光', '柴刀']
2026-01-26 16:31:30,173 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1章
2026-01-26 16:31:30,174 - app.services.agent.tools.explore_tools - INFO - [explore_content] 复用共享状态: searched=0, read_paragraphs=0, read_chapters=0
2026-01-26 16:31:30,175 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, target=查找并读取第一章中段融半夜练刀的段落...
2026-01-26 16:31:30,176 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:31:30,177 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用规划传入的关键词: ['段融', '练刀', '半夜', '月光', '柴刀']
2026-01-26 16:31:30,178 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围: (1, 1)
2026-01-26 16:31:30,277 - app.services.chapter_vector_service - INFO - [exact_search] work=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, keywords=['段融', '练刀', '半夜']..., mode=any, range=(1, 1), hits=29
2026-01-26 16:31:30,281 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 29 条
2026-01-26 16:31:30,286 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 29 条
2026-01-26 16:31:30,289 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 29 条证据)
2026-01-26 16:31:30,291 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:31:30,294 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:31:30,295 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:31:47,581 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:31:47,584 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:31:47,596 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:31:47,596 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2351, cost=$0.005362, time=17290ms
2026-01-26 16:31:47,596 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=556, 尝试次数=1
2026-01-26 16:31:47,596 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true,
    "练刀": false,
    "半夜": false,
    "月光": false,
    "柴刀": false
  },
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "已收集的信息来自第1章，包含29条关于角色“段融”的证据。内容描述了段融的外貌、衣着以及他进入一个院子的情景，但未提及“练刀”、“半夜”等与任务目标直接相关的关键词。",
  "next_action": "基于已收集信息中“练刀”、“半夜”等核心关键词在第1章的覆盖率为零，可以判断目标段落不存在于第1章。将向用户报告在第1章未找到相关内容。",
  "potential_gaps": ...
2026-01-26 16:31:47,596 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=1/5, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:31:47,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=29, 章节=1, 关键词覆盖=20.0%, 质量=0/3
2026-01-26 16:31:47,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则0命中: 关键词覆盖<50%% → 不足（需继续探索）
2026-01-26 16:31:47,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 评估不足，缺失项: ['练刀的情节', '半夜的时间背景', '使用的刀具（如柴刀）']
2026-01-26 16:31:47,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段3：AI 补充循环，当前 29 条证据
2026-01-26 16:31:47,601 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:31:47,601 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:31:47,601 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.3, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:32:03,173 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:32:03,173 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:32:03,195 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:32:03,199 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1714, cost=$0.004208, time=15573ms
2026-01-26 16:32:03,201 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=403, 尝试次数=1
2026-01-26 16:32:03,202 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 任务理解完成: 任务的核心是在一个已知范围（第一章）内，定位一个特定人物（段融）在特定时间（半夜）进行特定活动（练刀）的具体文字片段。...
2026-01-26 16:32:03,203 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:32:03,204 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:32:03,205 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:32:04,571 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:32:04,571 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:32:04,593 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:32:04,597 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=905, cost=$0.000147, time=1365ms
2026-01-26 16:32:04,598 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=338, 尝试次数=1
2026-01-26 16:32:04,598 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, type=<class 'uuid.UUID'>
2026-01-26 16:32:04,622 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:32:04,622 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:32:04,622 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:32:04,622 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:32:04,681 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1章 -> 第1章
2026-01-26 16:32:04,692 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:04,709 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-26 16:32:04,729 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1, query=段融深夜练刀的场景描述...
2026-01-26 16:32:04,912 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 16:32:18,333 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:32:18,333 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:32:18,346 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第68段
2026-01-26 16:32:18,386 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第20段
2026-01-26 16:32:18,398 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第69段
2026-01-26 16:32:18,408 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1, query=段融在半夜进行武术训练的细节...
2026-01-26 16:32:18,507 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 16:32:31,314 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 11 个候选 -> top 5
2026-01-26 16:32:31,314 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:32:31,324 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d, current_order=1, query=段融练习刀法的具体动作和环境...
2026-01-26 16:32:31,387 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 16:32:36,565 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:32:36,568 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:32:36,570 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:32:36,571 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:32:36,572 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:32:59,532 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:32:59,533 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:32:59,540 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:32:59,541 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3112, cost=$0.006183, time=22961ms
2026-01-26 16:32:59,541 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=529, 尝试次数=1
2026-01-26 16:32:59,542 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true,
    "练刀": true,
    "半夜": true,
    "月光": false,
    "柴刀": false
  },
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": false,
    "has_plot_details": true
  },
  "summary": "已收集的信息确认了关键词“段融”、“练刀”和“半夜”在第一章中均有出现。证据片段包含对段融外貌的描述，以及他进入院子、抽出并查看刀具的行为。",
  "next_action": "在第一章的范围内，定位同时包含“段融”、“半夜”和“练刀”这三个关键词的段落，并提取该段落的完整原文以完成任务。",
  "potential_gaps": [
    "关于场景环境（如月光）的描述",
  ...
2026-01-26 16:32:59,543 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=3/5, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:32:59,543 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=36, 章节=1, 关键词覆盖=60.0%, 质量=0/3
2026-01-26 16:32:59,543 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 16:32:59,543 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 2轮, 原因=AI 判断信息充足: 证据充足：36条证据，覆盖1个章节，关键词覆盖60%
2026-01-26 16:32:59,547 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,547 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,553 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,555 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,565 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,568 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,568 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,586 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,589 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,591 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 0c076d6c-abc8-4077-a518-05d24f3e12ce
2026-01-26 16:32:59,593 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:32:59,595 - app.api.v1.agent - INFO - [Stream] 任务完成: 在当前章节中，查找并读取“段融半夜练刀”的相关段落原文。 (89.4s)
2026-01-26 16:32:59,595 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:32:59,595 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户“更有意境，缺乏留白和想象空间”的要求，对找到的练刀段落进行改写。
2026-01-26 16:32:59,596 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户“更有意境，缺乏留白和想象空间”的要求，对找到的练刀段落进行改写。 (icon=Edit3)
2026-01-26 16:32:59,596 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-26 16:32:59,597 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-26 16:32:59,601 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 3607, 用户要求: 将段融半夜练刀的段落改写得更有意境，减少写实的动作描写，增加氛围、心境和留白，营造出一种与刀交融、物我两忘的感觉。重点描绘月光、刀光与人的影子三者之间的互动，而不是具体的招式。
2026-01-26 16:32:59,601 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-26 16:32:59,601 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:32:59,602 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:32:59,602 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-26 16:33:26,725 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:33:26,725 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:33:26,745 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:33:26,748 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=6071, cost=$0.009304, time=27123ms
2026-01-26 16:33:26,748 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=271, 尝试次数=1
2026-01-26 16:33:26,748 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 271
2026-01-26 16:33:26,751 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-01-26 16:33:26,751 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 27.154s)
2026-01-26 16:33:26,751 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-26 16:33:26,751 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户“更有意境，缺乏留白和想象空间”的要求，对找到的练刀段落进行改写。 (27.2s)
2026-01-26 16:33:26,751 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:33:26,755 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将新生成的、更具意境的练刀段落替换掉章节中的原始内容。
2026-01-26 16:33:26,757 - app.api.v1.agent - INFO - [Stream] Task started: 将新生成的、更具意境的练刀段落替换掉章节中的原始内容。 (icon=Check)
2026-01-26 16:33:26,758 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-01-26 16:33:26,758 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-01-26 16:33:26,758 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=replace, chapter=bc18c9d1-f600-484f-ab5a-bead3c7a6803
2026-01-26 16:33:26,763 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace, needs_locate=True
2026-01-26 16:33:26,768 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=bc18c9d1-f600-484f-ab5a-bead3c7a6803, query=## 世界观设定 ### characters - **段融**: 故事的主角，一个穿越者。他继承了原主的记忆，并拥有一个可以“吞噬器灵”的特殊能力，通过吸收物品（尤其是武器）的器灵来快速获得相关技能和经验。故事开始时，他是源顺镖局的一名杂役弟子，目标是利用能力变强并改变命运。 - **赵穆**: 源顺镖局的实习镖师，负责教导杂役弟子。为人傲慢，看不起底层弟子。他的佩刀是主角第一次成功吞噬器灵的对
2026-01-26 16:33:26,788 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 70 个段落
2026-01-26 16:33:26,788 - app.services.agent.tools.locate_tools - INFO - [locate_content] 定位到开头
2026-01-26 16:33:26,791 - app.services.agent.tools.operate_tools - INFO - [Operate] 定位完成: method=text_match, para=0
2026-01-26 16:33:26,793 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=bc18c9d1-f600-484f-ab5a-bead3c7a6803, operation=replace, content_len=179
2026-01-26 16:33:26,806 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 0.049s)
2026-01-26 16:33:26,806 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-01-26 16:33:26,811 - app.services.agent.utils.tool_cache - INFO - [ToolCache] invalidated 1 keys: tool_cache:*:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:chapter:bc18c9d1-f600-484f-ab5a-bead3c7a6803:*
2026-01-26 16:33:26,818 - app.api.v1.agent - INFO - [Stream] 任务完成: 将新生成的、更具意境的练刀段落替换掉章节中的原始内容。 (0.1s)
2026-01-26 16:33:26,819 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-26 16:33:26,819 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 116.65s
2026-01-26 16:33:26,820 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:33:26,821 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:33:26,821 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-26 16:33:26,822 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:33:26,822 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:33:26,823 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=10455字符, 处理后=6149字符
2026-01-26 16:33:26,824 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:33:26,824 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:33:26,825 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:33:26,825 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:33:26,826 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:33:26,831 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:33:26,831 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:33:26,831 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:33:49,633 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:33:49,633 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:33:49,637 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:33:50,852 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 271
2026-01-26 16:33:50,853 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 13036 (prompt=12844, completion=192)
2026-01-26 16:33:50,853 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:33:50,854 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:33:50,878 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:33:50,879 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=13036, cost=$0.004333, time=24023ms
2026-01-26 16:33:50,879 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=271
2026-01-26 16:33:51,790 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d | 重要度=0.77
2026-01-26 16:33:51,803 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, token=3538
2026-01-26 16:33:51,806 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f, 消息数=8, 摘要长度=0, Token=3538
2026-01-26 16:33:51,806 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:be92c72a-311f-4ebb-9d5f-78ce68aeb73d:b44dc2e9-06a4-43af-a09f-3646958eb76f)
2026-01-26 16:33:51,806 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:33:51,814 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:33:52,580 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f
INFO:     127.0.0.1:53988 - "GET /api/v1/agent/operations/b44dc2e9-06a4-43af-a09f-3646958eb76f HTTP/1.1" 200 OK
2026-01-26 16:37:23,206 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:51573 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:37:23,278 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:51575 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:37:23,303 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:64359 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:37:23,326 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:50278 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:37:36,826 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,829 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 缓存已失效: worldview:characters:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,830 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 缓存已失效: worldview:locations:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,832 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 缓存已失效: worldview:settings:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,834 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 缓存已失效: worldview:guidelines:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,836 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 缓存已失效: worldview:worlddata:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,838 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 缓存已失效: worldview:ai-guidelines:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,840 - app.api.v1.worldview - INFO - 🗑️ [Worldview] 聚合缓存已失效: worldview:worlddata:be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,841 - app.api.v1.works - INFO - [Works] 作品及相关缓存已删除: work_id=be92c72a-311f-4ebb-9d5f-78ce68aeb73d
2026-01-26 16:37:36,845 - app.api.middleware.monitoring_middleware - INFO - API请求完成: DELETE /api/v1/works/be92c72a-311f-4ebb-9d5f-78ce68aeb73d
INFO:     127.0.0.1:59029 - "DELETE /api/v1/works/be92c72a-311f-4ebb-9d5f-78ce68aeb73d HTTP/1.1" 204 No Content
2026-01-26 16:37:36,883 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:51752 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     connection closed
2026-01-26 16:37:55,493 - app.api.v1.auth - INFO - [LOGIN] 尝试登录: 18845572908@139.com (记住我: True)
2026-01-26 16:37:55,501 - app.services.login_rate_limit_service - INFO - 登录限流服务初始化成功
INFO:     ('127.0.0.1', 61568) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 16:37:56,159 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-26 16:37:56,172 - app.api.v1.auth - INFO - [LOGIN] 登录成功: 18845572908@139.com (refreshToken 有效期: 30天)
2026-01-26 16:37:56,197 - app.api.v1.auth - INFO - [LOGIN] 会话创建成功: 7f093b44-4979-45e3-bfe4-e0b423e0cc93 (127.0.0.1)
2026-01-26 16:37:56,197 - app.api.v1.auth - INFO - [LOGIN] 登录成功: 文枢 (7f093b44-4979-45e3-bfe4-e0b423e0cc93) from 127.0.0.1
2026-01-26 16:37:56,197 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:61311 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2026-01-26 16:37:56,237 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:61570 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 62409) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
2026-01-26 16:37:56,283 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     connection open
INFO:     connection closed
2026-01-26 16:37:56,292 - app.api.v1.ws - ERROR - [WebSocket] 通知推送错误:
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
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 320, in notifications_stream
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
INFO:     ('127.0.0.1', 52452) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
2026-01-26 16:37:56,310 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     connection open
2026-01-26 16:37:56,494 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:37:56,501 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:55388 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:55386 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:37:56,581 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:37:56,584 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:61771 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61770 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 60043) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
2026-01-26 16:38:01,296 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     connection open
INFO:     connection closed
2026-01-26 16:38:05,313 - app.api.v1.auth - INFO - [LOGIN] 尝试登录: zrt3ljnygz@163.com (记住我: True)
2026-01-26 16:38:05,676 - app.api.v1.auth - INFO - [LOGIN] 登录成功: zrt3ljnygz@163.com (refreshToken 有效期: 30天)
2026-01-26 16:38:05,690 - app.api.v1.auth - INFO - [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
2026-01-26 16:38:05,690 - app.api.v1.auth - INFO - [LOGIN] 登录成功: 文枢AI(Join) (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
2026-01-26 16:38:05,690 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:50102 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2026-01-26 16:38:05,713 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:61069 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 57545) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
2026-01-26 16:38:05,757 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection closed
2026-01-26 16:38:05,763 - app.api.v1.ws - ERROR - [WebSocket] 通知推送错误:
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
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 320, in notifications_stream
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
INFO:     ('127.0.0.1', 58252) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
2026-01-26 16:38:05,779 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
2026-01-26 16:38:05,898 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:56759 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:38:05,933 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:56761 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:38:05,953 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:38:05,956 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:50477 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:60790 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 63589) - "WebSocket /api/v1/ws/notifications/7f093b44-4979-45e3-bfe4-e0b423e0cc93" [accepted]
2026-01-26 16:38:06,414 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=7f093b44-4979-45e3-bfe4-e0b423e0cc93
INFO:     connection open
2026-01-26 16:38:16,068 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:55837 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=100 HTTP/1.1" 200 OK
2026-01-26 16:38:16,084 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:55839 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=100 HTTP/1.1" 200 OK
2026-01-26 16:38:21,753 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63745 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:38:21,778 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52694 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:38:21,786 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:63746 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:38:21,806 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:53310 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:38:26,636 - app.api.v1.import_routes - INFO - 用户 602f5147-846a-4cde-95d3-405fa75f133f 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:38:26,640 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-26 16:38:26,642 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:58057 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:38:28,045 - app.api.v1.import_routes - INFO - 用户 602f5147-846a-4cde-95d3-405fa75f133f 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:38:28,046 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-26 16:38:28,047 - app.services.import_service - INFO - 用户 602f5147-846a-4cde-95d3-405fa75f133f 开始导入文本数据
2026-01-26 16:38:28,061 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=c2d9bc27-c8ab-4510-bcae-7ee9aca87f06, delta=3005, edit_event_id=None
2026-01-26 16:38:28,062 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=19a901c4-03f0-4f0d-9ae8-185662f029ad, delta=2674, edit_event_id=None
2026-01-26 16:38:28,062 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9440daf1-2a00-47b6-82f5-b4c2aba753a0, delta=2565, edit_event_id=None
2026-01-26 16:38:28,062 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9e647ceb-8785-441d-b330-fb84ccabf92a, delta=2481, edit_event_id=None
2026-01-26 16:38:28,063 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=e040c67f-e302-4e69-a74b-26c22912abd4, delta=2951, edit_event_id=None
2026-01-26 16:38:28,132 - app.services.import_service - INFO - 文本导入完成: 作品ID=d807d2bd-eaf5-4f59-8442-fbbe84616efa, 章节=5
2026-01-26 16:38:28,132 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 d807d2bd-eaf5-4f59-8442-fbbe84616efa 排队世界观提取任务
2026-01-26 16:38:28,132 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=d807d2bd-eaf5-4f59-8442-fbbe84616efa, 章节=5, 人物=0
2026-01-26 16:38:28,135 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:62251 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:38:28,137 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:38:31,448 - app.api.v1.chapters - INFO - [GET chapters] work_id=d807d2bd-eaf5-4f59-8442-fbbe84616efa, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2026-01-26 16:38:31,473 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:38:31,474 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=d807d2bd-eaf5-4f59-8442-fbbe84616efa, type=<class 'uuid.UUID'>
2026-01-26 16:38:31,481 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:38:31,486 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:31,490 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:31,492 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-26 16:38:31,496 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:31,498 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:38:31,498 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:38:31,499 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:38:31,499 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:38:31,531 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:38:31,535 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=60s)
2026-01-26 16:38:31,541 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:31,546 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/characters
2026-01-26 16:38:31,547 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/locations
2026-01-26 16:38:31,549 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:38:31,551 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/settings
2026-01-26 16:38:31,551 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/guidelines
INFO:     127.0.0.1:63327 - "GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:63328 - "GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:63326 - "GET /api/v1/chapters/work/d807d2bd-eaf5-4f59-8442-fbbe84616efa HTTP/1.1" 200 OK
INFO:     127.0.0.1:63329 - "GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:63330 - "GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/guidelines HTTP/1.1" 200 OK
2026-01-26 16:38:33,750 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa
INFO:     127.0.0.1:63323 - "GET /api/v1/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa HTTP/1.1" 200 OK
2026-01-26 16:38:33,766 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:33,769 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/ai-guidelines
2026-01-26 16:38:33,771 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
INFO:     127.0.0.1:62530 - "GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:38:33,774 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-26 16:38:36,304 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:38:36,305 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:38:36,305 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50509 - "POST /api/v1/agent/sessions HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:50510 - "POST /api/v1/agent/sessions HTTP/1.1" 401 Unauthorized
INFO:     127.0.0.1:50508 - "POST /api/v1/agent/sessions HTTP/1.1" 401 Unauthorized
2026-01-26 16:38:36,319 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-26 16:38:36,326 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-26 16:38:36,340 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/status
INFO:     127.0.0.1:50513 - "GET /api/v1/analysis/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/status HTTP/1.1" 404 Not Found
2026-01-26 16:38:39,286 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:52629 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:38:39,309 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:39,311 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
2026-01-26 16:38:39,321 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:38:39,335 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/characters
2026-01-26 16:38:39,356 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
2026-01-26 16:38:42,546 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/locations
2026-01-26 16:38:42,562 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:38:42,597 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:38:42,598 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c2d9bc27-c8ab-4510-bcae-7ee9aca87f06/revisions
2026-01-26 16:38:42,602 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:d807d2bd-eaf5-4f59-8442-fbbe84616efa (expire=300s)
2026-01-26 16:38:42,608 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:38:42,612 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/guidelines
2026-01-26 16:38:42,613 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 d807d2bd-eaf5-4f59-8442-fbbe84616efa 提取世界观
2026-01-26 16:38:42,616 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/settings
2026-01-26 16:38:42,616 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/d807d2bd-eaf5-4f59-8442-fbbe84616efa/ai-guidelines
2026-01-26 16:38:42,655 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=4677
2026-01-26 16:38:42,657 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-26 16:38:42,657 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-26 16:38:42,657 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-26 16:38:42,662 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-26 16:38:42,662 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 15427
2026-01-26 16:38:42,663 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p data-id="5119v7fd">青州。</p><p data-id="nshptcmz">渊阳府，贤古县。</p><p data-id="86c4d7ym">源顺镖局，后院偏房的一片空地内。</p><p data-id="8uyst2ic">此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p data-id="5mgctvf0">这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p data-id="tyogjxzl">这些少年都是源顺镖局，今年新招的杂役弟子。</p><p data-id="07y2fryv">刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p data-id="9x8tfsl2">因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p data-id="o2nfriar">学得好的，有机会晋升为学徒。</p><p data-id="9ze4udac">一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖...
2026-01-26 16:38:42,669 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 15427
2026-01-26 16:38:42,670 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:38:42,671 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF50C3D1C0>, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2026-01-26 16:38:42,671 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:38:42,672 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:38:42,672 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:38:44,363 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:38:44,363 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-26 16:38:44,369 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:38:44,369 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-26 16:38:44,401 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:38:44,401 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c2d9bc27-c8ab-4510-bcae-7ee9aca87f06
2026-01-26 16:38:44,401 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:38:47,231 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:38:55,331 - app.api.v1.auth - INFO - [LOGIN] 尝试登录: zrt3ljnygz@163.com (记住我: True)
2026-01-26 16:38:55,699 - app.api.v1.auth - INFO - [LOGIN] 登录成功: zrt3ljnygz@163.com (refreshToken 有效期: 30天)
2026-01-26 16:38:55,706 - app.api.v1.auth - INFO - [LOGIN] 会话创建成功: 602f5147-846a-4cde-95d3-405fa75f133f (127.0.0.1)
2026-01-26 16:38:55,707 - app.api.v1.auth - INFO - [LOGIN] 登录成功: 文枢AI(Join) (602f5147-846a-4cde-95d3-405fa75f133f) from 127.0.0.1
2026-01-26 16:38:55,708 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:63196 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2026-01-26 16:38:55,738 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:55931 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 51879) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
2026-01-26 16:38:55,785 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
INFO:     connection closed
2026-01-26 16:38:55,808 - app.api.v1.ws - ERROR - [WebSocket] 通知推送错误:
Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py", line 349, in asgi_send
    await self.send(data)  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 620, in send
    await self.ensure_open()
  File "D:\Java\ai_writer\backend\venv\Lib\site-packages\websockets\legacy\protocol.py", line 921, in ensure_open
    raise self.connection_closed_exc()
websockets.exceptions.ConnectionClosedOK: received 1001 (going away); then sent 1001 (going away)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 320, in notifications_stream
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
INFO:     ('127.0.0.1', 58285) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
2026-01-26 16:38:55,821 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
2026-01-26 16:38:56,237 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:59735 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:38:56,242 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:59734 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:38:56,259 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:59737 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:38:56,268 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:57060 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 55365) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
2026-01-26 16:39:00,803 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
2026-01-26 16:39:27,003 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
INFO:     connection closed
INFO:     ('127.0.0.1', 61880) - "WebSocket /api/v1/ws/notifications/602f5147-846a-4cde-95d3-405fa75f133f" [accepted]
2026-01-26 16:39:37,428 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=602f5147-846a-4cde-95d3-405fa75f133f
INFO:     connection open
2026-01-26 16:39:37,829 - app.api.v1.auth - INFO - [LOGIN] 尝试登录: 2072855200@qq.com (记住我: True)
2026-01-26 16:39:38,226 - app.api.v1.auth - INFO - [LOGIN] 登录成功: 2072855200@qq.com (refreshToken 有效期: 30天)
2026-01-26 16:39:38,231 - app.api.v1.auth - INFO - [LOGIN] 会话创建成功: 79913e7e-d5cd-4e09-bce6-ca6639bd8456 (127.0.0.1)
2026-01-26 16:39:38,231 - app.api.v1.auth - INFO - [LOGIN] 登录成功: 文枢AI管理者 (79913e7e-d5cd-4e09-bce6-ca6639bd8456) from 127.0.0.1
2026-01-26 16:39:38,234 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/login
INFO:     127.0.0.1:59745 - "POST /api/v1/auth/login HTTP/1.1" 200 OK
2026-01-26 16:39:38,257 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/users/me
INFO:     127.0.0.1:50874 - "GET /api/v1/users/me HTTP/1.1" 200 OK
INFO:     connection closed
INFO:     ('127.0.0.1', 51150) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 16:39:38,296 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection closed
2026-01-26 16:39:38,302 - app.api.v1.ws - ERROR - [WebSocket] 通知推送错误:
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
  File "D:\Java\ai_writer\backend\app\api\v1\ws.py", line 320, in notifications_stream
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
INFO:     ('127.0.0.1', 64352) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 16:39:38,316 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-26 16:39:38,479 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:39:38,479 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:54541 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54540 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:39:38,526 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:53446 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:39:38,536 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:53448 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     ('127.0.0.1', 59502) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 16:39:43,303 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-26 16:39:44,648 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 35 个数据块，总长度: 4462
2026-01-26 16:39:44,648 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 17984 (prompt=15792, completion=2192)
2026-01-26 16:39:44,648 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=602f5147-846a-4cde-95d3-405fa75f133f
2026-01-26 16:39:44,648 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:39:44,659 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 602f5147-846a-4cde-95d3-405fa75f133f 豁免积分扣除
2026-01-26 16:39:44,659 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=17984, cost=$0.041660, time=60278ms
2026-01-26 16:39:44,659 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4462
2026-01-26 16:39:44,659 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: ```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "小说主角，一名十五六岁的少年。原为地球人，魂穿至此界，继承了原主的记忆。拥有“吞噬器灵”的特殊能力，可以通过吞噬兵器中的器灵来快速获得武学经验。目前是源顺镖局的杂役弟子，目标是成为学徒。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "段融的发小，在贤古县县衙担任捕快。为人仗义，有些爱显摆。因其二叔在生药铺做账房，有一些门路和背景。是主角在外界的重要伙伴和信息来源。",
      "first_appearance": "第5章",
      "importance": "高"
    },
    {
      "name": "赵穆",
      "role":...
2026-01-26 16:39:44,659 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=7, 新设定=6
2026-01-26 16:39:44,667 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 11人物, 7地点, 6设定
2026-01-26 16:39:44,682 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-26 16:39:44,691 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-26 16:39:44,700 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-26 16:39:44,708 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-26 16:39:44,712 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-26 16:39:44,727 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-26 16:39:44,740 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-26 16:39:44,749 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-26 16:39:44,761 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-26 16:39:44,776 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-26 16:39:44,784 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-26 16:39:44,796 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-26 16:39:44,804 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-26 16:39:44,814 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-26 16:39:44,820 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-26 16:39:44,830 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-26 16:39:44,837 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-26 16:39:44,844 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-26 16:39:44,853 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-26 16:39:44,861 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治
2026-01-26 16:39:44,873 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵设定
2026-01-26 16:39:44,885 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学体系
2026-01-26 16:39:44,893 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学与资源
2026-01-26 16:39:44,901 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 镖局晋升体系
2026-01-26 16:39:44,909 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小/挚友
2026-01-26 16:39:44,911 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 赵穆: 上下级与被欺凌者
2026-01-26 16:39:44,913 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 孔斌: 同期弟子/潜在竞争对手
2026-01-26 16:39:44,926 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:39:44,928 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:39:44,930 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:39:44,932 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:39:44,934 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:d807d2bd-eaf5-4f59-8442-fbbe84616efa
2026-01-26 16:39:44,935 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 11, 'characters_updated': 0, 'locations_created': 7, 'settings_created': 6, 'relationships_created': 3}
INFO:     connection closed
INFO:     connection closed
INFO:     connection closed
2026-01-26 16:40:16,581 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:40:16,593 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65355 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65354 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:40:16,789 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:58301 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:40:16,883 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58303 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:40:24,361 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 下一步开发目标.md, 格式: markdown
2026-01-26 16:40:24,365 - app.api.v1.import_routes - INFO - 预览成功: 作品=AI写作系统 - 重新设计的开发目标, 章节数=9
2026-01-26 16:40:24,368 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:64743 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:40:25,966 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 下一步开发目标.md, 格式: markdown
2026-01-26 16:40:25,968 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=markdown, background_tasks=True
2026-01-26 16:40:25,969 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-26 16:40:26,000 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=32adac1b-516d-49cd-8e88-4b2098f124f5, delta=68, edit_event_id=None
2026-01-26 16:40:26,001 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=3ff79a4f-7eb1-4270-9c2b-f4203ae354cc, delta=550, edit_event_id=None
2026-01-26 16:40:26,002 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=8ecb48ac-5a96-450b-a143-33909328622e, delta=7386, edit_event_id=None
2026-01-26 16:40:26,003 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=37a13a83-9952-4f59-a1fc-60ceefeed3a3, delta=1315, edit_event_id=None
2026-01-26 16:40:26,005 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=430885a1-8a99-4785-a53e-5e822836cce0, delta=5536, edit_event_id=None
2026-01-26 16:40:26,007 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9c425784-c12d-42ae-839b-0c898edaab59, delta=545, edit_event_id=None
2026-01-26 16:40:26,008 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=61c8e457-bb4b-4207-a53d-8c30a8f7826b, delta=474, edit_event_id=None
2026-01-26 16:40:26,009 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=88531a75-0ae1-4575-8b8b-97b8b0ebef95, delta=358, edit_event_id=None
2026-01-26 16:40:26,010 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=640e900d-2dac-4986-8737-da49893bd83a, delta=357, edit_event_id=None
2026-01-26 16:40:26,295 - app.services.import_service - INFO - 文本导入完成: 作品ID=3e308f36-2885-48da-8da1-ddfb9d00a66c, 章节=9
2026-01-26 16:40:26,296 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 3e308f36-2885-48da-8da1-ddfb9d00a66c 排队世界观提取任务
2026-01-26 16:40:26,296 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=3e308f36-2885-48da-8da1-ddfb9d00a66c, 章节=9, 人物=0
2026-01-26 16:40:26,300 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:60074 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:40:26,303 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 🎯 现有系统分析 (order=2)
2026-01-26 16:40:27,054 - app.api.v1.chapters - INFO - [GET chapters] work_id=3e308f36-2885-48da-8da1-ddfb9d00a66c, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:40:27,067 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 🎯 现有系统分析 (17 paragraphs)
2026-01-26 16:40:27,086 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:27,086 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=3e308f36-2885-48da-8da1-ddfb9d00a66c, type=<class 'uuid.UUID'>
2026-01-26 16:40:27,093 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 🚀 重新设计的开发目标 (order=3)
2026-01-26 16:40:27,099 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:27,102 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:27,103 - app.services.chapter_service - INFO - [ChapterService] Found 9 chapters
2026-01-26 16:40:27,104 - app.services.chapter_service - INFO -   - Chapter: 📋 项目概述, order=1
2026-01-26 16:40:27,104 - app.services.chapter_service - INFO -   - ... (7 more chapters)
2026-01-26 16:40:27,104 - app.services.chapter_service - INFO -   - Chapter: 📝 总结, order=9
2026-01-26 16:40:27,422 - app.api.v1.chapters - INFO - [GET chapters] Returning 9 chapters
2026-01-26 16:40:27,429 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=60s)
2026-01-26 16:40:27,437 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:27,444 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:27,445 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:27,447 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/characters
2026-01-26 16:40:27,452 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/settings
2026-01-26 16:40:27,452 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:27,455 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/locations
INFO:     127.0.0.1:53590 - "GET /api/v1/works/3e308f36-2885-48da-8da1-ddfb9d00a66c HTTP/1.1" 200 OK
INFO:     127.0.0.1:53592 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:53595 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:53591 - "GET /api/v1/chapters/work/3e308f36-2885-48da-8da1-ddfb9d00a66c HTTP/1.1" 200 OK
INFO:     127.0.0.1:53593 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/locations HTTP/1.1" 200 OK
2026-01-26 16:40:27,483 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/guidelines
INFO:     127.0.0.1:53594 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/guidelines HTTP/1.1" 200 OK
2026-01-26 16:40:31,297 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:31,300 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/ai-guidelines
INFO:     127.0.0.1:62139 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:40:31,360 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 🚀 重新设计的开发目标 (253 paragraphs)
2026-01-26 16:40:31,365 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 📅 详细的实施时间线 (order=4)
2026-01-26 16:40:32,745 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 📅 详细的实施时间线 (64 paragraphs)
2026-01-26 16:40:32,754 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 🔧 技术实现细节 (order=5)
2026-01-26 16:40:32,758 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 3e308f36-2885-48da-8da1-ddfb9d00a66c, chapter_id: 32adac1b-516d-49cd-8e88-4b2098f124f5
2026-01-26 16:40:32,765 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 3e308f36-2885-48da-8da1-ddfb9d00a66c, chapter_id: 32adac1b-516d-49cd-8e88-4b2098f124f5
2026-01-26 16:40:32,796 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 32adac1b-516d-49cd-8e88-4b2098f124f5
2026-01-26 16:40:32,797 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:40:32,799 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 32adac1b-516d-49cd-8e88-4b2098f124f5
2026-01-26 16:40:32,800 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:40:36,311 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:40:36,316 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:40:36,319 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59420 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58311 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:55029 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:40:36,694 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 🔧 技术实现细节 (187 paragraphs)
2026-01-26 16:40:36,710 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:40:36,712 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 📊 成功指标和验收标准 (order=6)
2026-01-26 16:40:36,732 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:40:36,737 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54460 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:54463 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:54462 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:40:37,699 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 📊 成功指标和验收标准 (21 paragraphs)
2026-01-26 16:40:37,704 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 🚨 风险控制和应急预案 (order=7)
2026-01-26 16:40:37,710 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5/revisions
INFO:     127.0.0.1:59919 - "GET /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:40:37,754 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:37,759 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:38,197 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/status
INFO:     127.0.0.1:51759 - "GET /api/v1/analysis/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/status HTTP/1.1" 404 Not Found
2026-01-26 16:40:38,210 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/locations
2026-01-26 16:40:38,211 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/characters
INFO:     127.0.0.1:56575 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:56573 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/characters HTTP/1.1" 200 OK
2026-01-26 16:40:38,224 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 🚨 风险控制和应急预案 (22 paragraphs)
2026-01-26 16:40:38,230 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 🎯 关键里程碑 (order=8)
2026-01-26 16:40:38,250 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:3e308f36-2885-48da-8da1-ddfb9d00a66c (expire=300s)
2026-01-26 16:40:38,268 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:38,620 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/settings
INFO:     127.0.0.1:53661 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/settings HTTP/1.1" 200 OK
2026-01-26 16:40:38,635 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/guidelines
INFO:     127.0.0.1:53513 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/guidelines HTTP/1.1" 200 OK
2026-01-26 16:40:38,652 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 🎯 关键里程碑 (17 paragraphs)
2026-01-26 16:40:38,659 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:38,668 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 📝 总结 (order=9)
2026-01-26 16:40:38,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/ai-guidelines
INFO:     127.0.0.1:53066 - "GET /api/v1/worldview/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:40:38,698 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:40:39,323 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:54644 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54642 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:40:39,375 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 📝 总结 (11 paragraphs)
2026-01-26 16:40:39,390 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 3e308f36-2885-48da-8da1-ddfb9d00a66c 提取世界观
2026-01-26 16:40:39,435 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5/revisions
INFO:     127.0.0.1:62738 - "GET /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:40:39,467 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '📋 项目概述': 内容长度=87
2026-01-26 16:40:39,470 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '🎯 现有系统分析': 内容长度=587
2026-01-26 16:40:39,474 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '🚀 重新设计的开发目标': 内容长度=7767
2026-01-26 16:40:39,477 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '📅 详细的实施时间线': 内容长度=1492
2026-01-26 16:40:39,480 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '🔧 技术实现细节': 内容长度=5928
2026-01-26 16:40:39,485 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 6 '📊 成功指标和验收标准': 内容长度=618
2026-01-26 16:40:39,488 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 7 '🚨 风险控制和应急预案': 内容长度=497
2026-01-26 16:40:39,491 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 8 '🎯 关键里程碑': 内容长度=388
2026-01-26 16:40:39,493 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 9 '📝 总结': 内容长度=362
2026-01-26 16:40:39,497 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 9 个章节，总内容长度: 17883
2026-01-26 16:40:39,498 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 📋 项目概述】
<p data-id="1k6bfqbk">基于对现有系统的深入分析，本文档重新设计了实际可行的开发计划。新计划充分利用现有技术栈和功能，避免重复开发，确保有效落地。</p>

【第2章 🎯 现有系统分析】
<p>### 技术架构现状</p><p>- **编辑器核心**：TipTap + Novel.js（基于TipTap的高级封装）</p><p>- **前端框架**：React + TypeScript + Tailwind CSS</p><p>- **后端框架**：FastAPI + PostgreSQL + Redis</p><p>- **AI集成**：已实现完整的AI交互系统</p><p>### 现有AI功能盘点</p><p>✅ **已完成功能**：</p><p>- AI文本选中和处理（`AISelectorCommands.tsx`）</p><p>- AI操作命令（improve, fix grammar, make shorter/longer, continue writing）</p><p>- AI结果应用（replace, insert,...
2026-01-26 16:40:39,538 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 9, 内容长度: 17883
2026-01-26 16:40:39,540 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:40:39,541 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF00250050>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:40:39,542 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:40:39,544 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:40:39,545 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:40:42,170 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:40:42,171 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-26 16:40:42,182 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:40:42,184 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/status
INFO:     127.0.0.1:54118 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:57230 - "GET /api/v1/analysis/works/3e308f36-2885-48da-8da1-ddfb9d00a66c/status HTTP/1.1" 404 Not Found
2026-01-26 16:40:42,190 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:59926 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:40:42,196 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:40:42,197 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-26 16:40:42,201 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:42,203 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5
INFO:     127.0.0.1:57133 - "PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5 HTTP/1.1" 200 OK
2026-01-26 16:40:43,239 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 32adac1b-516d-49cd-8e88-4b2098f124f5 内容更新，新段落数: 1
2026-01-26 16:40:43,254 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 32adac1b-516d-49cd-8e88-4b2098f124f5 内容更新，新段落数: 1
2026-01-26 16:40:43,294 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 32adac1b-516d-49cd-8e88-4b2098f124f5 内容更新，新段落数: 1
2026-01-26 16:40:43,309 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 32adac1b-516d-49cd-8e88-4b2098f124f5 内容更新，新段落数: 1
2026-01-26 16:40:43,350 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:43,377 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5
2026-01-26 16:40:43,384 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:43,397 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c
INFO:     127.0.0.1:65505 - "PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5 HTTP/1.1" 200 OK
2026-01-26 16:40:43,413 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5
2026-01-26 16:40:43,423 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5
INFO:     127.0.0.1:65507 - "PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65504 - "PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5 HTTP/1.1" 200 OK
2026-01-26 16:40:43,448 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:40:43,460 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5
INFO:     127.0.0.1:65506 - "PUT /api/v1/chapters/32adac1b-516d-49cd-8e88-4b2098f124f5 HTTP/1.1" 200 OK
2026-01-26 16:40:47,995 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:40:48,002 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-26 16:40:48,007 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:55184 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:40:49,605 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:40:49,606 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-26 16:40:49,607 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-26 16:40:49,623 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=13869f82-8947-4992-a6bc-8d6ea4de1b2d, delta=3005, edit_event_id=None
2026-01-26 16:40:49,624 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=ed554b61-acab-428c-a8dd-a13f4843ce21, delta=2674, edit_event_id=None
2026-01-26 16:40:49,625 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=a3b2898b-57e1-4cb7-b46c-cb2c0fa7134d, delta=2565, edit_event_id=None
2026-01-26 16:40:49,625 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=e43a4f06-f97c-43bf-8801-7b25b8a3f4af, delta=2481, edit_event_id=None
2026-01-26 16:40:49,626 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=4010049e-6d95-4abe-872d-1eb0c0d756d5, delta=2951, edit_event_id=None
2026-01-26 16:40:49,830 - app.services.import_service - INFO - 文本导入完成: 作品ID=b0a47953-7246-42d6-bb24-eba29c2606ad, 章节=5
2026-01-26 16:40:49,833 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 b0a47953-7246-42d6-bb24-eba29c2606ad 排队世界观提取任务
2026-01-26 16:40:49,835 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=b0a47953-7246-42d6-bb24-eba29c2606ad, 章节=5, 人物=0
2026-01-26 16:40:49,839 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:53926 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:40:49,843 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:40:52,542 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:40:52,576 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:40:52,577 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, type=<class 'uuid.UUID'>
2026-01-26 16:40:52,586 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:40:52,590 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:40:52,593 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:40:52,593 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:40:52,594 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:40:52,594 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:40:52,607 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:40:52,614 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=60s)
2026-01-26 16:40:52,616 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:40:52,621 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:40:52,625 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:40:52,629 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-26 16:40:52,632 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:40:52,634 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
2026-01-26 16:40:52,635 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
2026-01-26 16:40:52,637 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:40:52,640 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
2026-01-26 16:40:52,642 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
INFO:     127.0.0.1:63575 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
INFO:     127.0.0.1:63578 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:63577 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:63576 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
INFO:     127.0.0.1:63579 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:63580 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
2026-01-26 16:40:54,382 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:40:54,383 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
INFO:     127.0.0.1:65031 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:40:54,402 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-26 16:40:54,403 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-26 16:40:57,439 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-26 16:40:57,444 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-26 16:40:57,471 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:40:57,497 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:40:57,536 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:40:57,538 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:41:00,955 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:41:00,956 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:41:00,966 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:41:00,969 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:49510 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:41:00,976 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63533 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:50714 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:41:01,207 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
2026-01-26 16:41:01,211 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:41:01,214 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:41:01,230 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:41:01,233 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:56119 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:56118 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:56117 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:41:04,098 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:41:04,100 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:41:04,101 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions
2026-01-26 16:41:04,104 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:41:04,117 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 b0a47953-7246-42d6-bb24-eba29c2606ad 提取世界观
INFO:     127.0.0.1:62348 - "GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:41:04,123 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
2026-01-26 16:41:04,124 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
2026-01-26 16:41:04,126 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
INFO:     127.0.0.1:60570 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55408 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55409 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
2026-01-26 16:41:04,215 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=4677
2026-01-26 16:41:04,217 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-26 16:41:04,221 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-26 16:41:04,222 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-26 16:41:04,223 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-26 16:41:04,224 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 15427
2026-01-26 16:41:04,225 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p data-id="0vcmka9d">青州。</p><p data-id="ogoliqp7">渊阳府，贤古县。</p><p data-id="7nydwn9k">源顺镖局，后院偏房的一片空地内。</p><p data-id="rp1y4pb6">此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p data-id="9mr672ud">这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p data-id="d5i7yfpt">这些少年都是源顺镖局，今年新招的杂役弟子。</p><p data-id="f1gplgt8">刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p data-id="yfbldazt">因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p data-id="rhvpcbfs">学得好的，有机会晋升为学徒。</p><p data-id="5zc66yyo">一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖...
2026-01-26 16:41:04,246 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:41:04,261 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 15427
2026-01-26 16:41:04,262 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:41:04,262 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF53FFAF60>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:41:04,263 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:41:04,264 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:41:04,265 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:41:05,677 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:41:05,678 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-26 16:41:05,682 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
2026-01-26 16:41:05,691 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:50084 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
2026-01-26 16:41:05,705 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:41:05,708 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
2026-01-26 16:41:05,710 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:41:05,711 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
INFO:     127.0.0.1:52763 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
2026-01-26 16:41:05,718 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
INFO:     127.0.0.1:51203 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:41:05,729 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:41:05,732 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:51207 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51206 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:41:05,778 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions
INFO:     127.0.0.1:60375 - "GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:41:05,790 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:41:05,793 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:41:05,793 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:65511 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:41:05,798 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:56046 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:41:05,802 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:41:05,804 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:56048 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:54552 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 16:41:09,943 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:10,127 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 13869f82-8947-4992-a6bc-8d6ea4de1b2d 内容更新，新段落数: 88
2026-01-26 16:41:10,130 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 13869f82-8947-4992-a6bc-8d6ea4de1b2d 内容更新，新段落数: 88
2026-01-26 16:41:10,133 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 13869f82-8947-4992-a6bc-8d6ea4de1b2d 内容更新，新段落数: 88
2026-01-26 16:41:10,148 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 13869f82-8947-4992-a6bc-8d6ea4de1b2d 内容更新，新段落数: 88
2026-01-26 16:41:10,153 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:41:10,155 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:41:10,157 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:41:10,159 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
INFO:     127.0.0.1:53452 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:41:10,162 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:53456 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:41:10,166 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:10,179 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:41:10,183 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
INFO:     127.0.0.1:53453 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:41:12,955 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:12,965 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:41:12,968 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
INFO:     127.0.0.1:53454 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:41:12,974 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:12,976 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:17,157 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:41:17,159 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:17,164 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:41:17,167 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-26 16:41:17,171 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
2026-01-26 16:41:17,172 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
INFO:     127.0.0.1:59417 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:41:19,391 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:21,461 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:41:21,462 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-26 16:41:21,463 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-26 16:41:21,496 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=6a1cf453-f405-4bd1-a789-3f0b71fd9ef3, delta=3005, edit_event_id=None
2026-01-26 16:41:21,496 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=b1738dc2-4c97-425f-b459-5ea347e4d3bc, delta=2674, edit_event_id=None
2026-01-26 16:41:21,497 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=50c824ba-9793-4ff5-9f2f-79d4481401b8, delta=2565, edit_event_id=None
2026-01-26 16:41:21,497 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9bd86e66-886f-4e36-bf3d-29a755a8053a, delta=2481, edit_event_id=None
2026-01-26 16:41:21,498 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=19c51863-a5d0-40a9-b891-f6124d9446f0, delta=2951, edit_event_id=None
2026-01-26 16:41:21,678 - app.services.import_service - INFO - 文本导入完成: 作品ID=7414c983-ce5d-4d9e-a503-01ce30ae2b26, 章节=5
2026-01-26 16:41:21,679 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 7414c983-ce5d-4d9e-a503-01ce30ae2b26 排队世界观提取任务
2026-01-26 16:41:21,680 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=7414c983-ce5d-4d9e-a503-01ce30ae2b26, 章节=5, 人物=0
2026-01-26 16:41:21,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:63846 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:41:21,684 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:23,765 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:41:23,773 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:23,783 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:23,786 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-26 16:41:23,788 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:23,791 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:41:23,791 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, type=<class 'uuid.UUID'>
2026-01-26 16:41:23,793 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:23,797 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:23,799 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:41:23,800 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
2026-01-26 16:41:23,801 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:41:23,801 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:41:23,802 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:41:23,802 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:41:23,810 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:41:23,814 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=60s)
2026-01-26 16:41:23,816 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
2026-01-26 16:41:23,817 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
INFO:     127.0.0.1:54174 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 16:41:23,819 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
INFO:     127.0.0.1:54178 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:54176 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:54179 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:54177 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
2026-01-26 16:41:25,769 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:54175 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 16:41:25,782 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-26 16:41:25,784 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-26 16:41:28,802 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:28,808 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
INFO:     127.0.0.1:49704 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:41:28,822 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-26 16:41:28,824 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-26 16:41:31,108 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
2026-01-26 16:41:31,118 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:41:31,136 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 16:41:31,141 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 16:41:31,188 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 16:41:31,189 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:41:31,194 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 16:41:31,195 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:41:33,403 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:41:33,406 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:41:33,406 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:41:33,406 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 24 个数据块，总长度: 3322
2026-01-26 16:41:33,407 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 13169 (prompt=11611, completion=1558)
2026-01-26 16:41:33,407 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:41:33,407 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
INFO:     127.0.0.1:51105 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:55313 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:49787 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:41:33,460 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:41:33,460 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=13169, cost=$0.030094, time=51210ms
2026-01-26 16:41:33,461 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 3322
2026-01-26 16:41:33,461 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: 好的，遵命。作为专业的小说世界观分析师，我已经综合分析了您提供的9个章节内容。

由于【现有世界观】数据为空，本次分析提取的所有内容均为**新增世界观**。以下是基于全部章节内容提炼出的世界观要素，以严格的JSON格式呈现：

```json
{
  "new_characters": [
    {
      "name": "用户 (User)",
      "role": "主角",
      "description": "这个世界的中心行动者。他们通过“编辑器”进行创造（写作），并能调用“AI服务”的强大力量来辅助自己。所有新规则和系统的建立都是为了增强其创造能力和保障其成果安全。",
      "first_appearance": "第2章 🎯 现有系统分析",
      "importance": "高"
    },
    {
      "name": "AI服务 (AI Service)",
      "role": "配角/核心系统",
      "description": "一个强大的、类似魔法系统的存在。它能理解并处理语言，执行“润色”、“...
2026-01-26 16:41:33,462 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=4, 新地点=4, 新设定=7
2026-01-26 16:41:33,465 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 9章, 发现 4人物, 4地点, 7设定
2026-01-26 16:41:33,466 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:41:33,516 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 7414c983-ce5d-4d9e-a503-01ce30ae2b26 提取世界观
2026-01-26 16:41:33,565 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:41:33,576 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:59057 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:41:33,578 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:59059 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:59058 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:41:33,592 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=3005
2026-01-26 16:41:33,593 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-26 16:41:33,595 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-26 16:41:33,596 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-26 16:41:33,597 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-26 16:41:33,597 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 13755
2026-01-26 16:41:33,598 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p>青州。</p><p>渊阳府，贤古县。</p><p>源顺镖局，后院偏房的一片空地内。</p><p>此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p>这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p>这些少年都是源顺镖局，今年新招的杂役弟子。</p><p>刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p>因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p>学得好的，有机会晋升为学徒。</p><p>一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖。</p><p>假以时日，业务熟练了，自己也能成为镖师。</p><p>镖师虽说是吃江湖饭的，有些危险，但对这些贫苦出身的少年们，这已经是相当好的职业了。</p><p>起码能吃饱肚子，而且多少是可以捞些油水的。</p><p>但现在，他们已经进门两个半月了。</p><p>心绪也从兴奋，慢慢变得黯淡了。</p><p>杂役弟子能成为学徒的，一批里，最多一二个，而且经常的，是成批成批的覆...
2026-01-26 16:41:33,600 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 用户 (User)
2026-01-26 16:41:33,619 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 13755
2026-01-26 16:41:33,620 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:41:33,620 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF54155BE0>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:41:33,620 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:41:33,620 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:41:33,621 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:41:34,995 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:41:34,995 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-26 16:41:35,013 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: AI服务 (AI Service)
2026-01-26 16:41:35,022 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:41:35,022 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-26 16:41:35,029 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:35,032 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
2026-01-26 16:41:35,035 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
INFO:     127.0.0.1:57509 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 16:41:35,045 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions
2026-01-26 16:41:35,046 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
2026-01-26 16:41:35,048 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
INFO:     127.0.0.1:58087 - "GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:58402 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:53563 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
2026-01-26 16:41:35,057 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 编辑器 (Editor)
2026-01-26 16:41:35,077 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 16:41:35,100 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
2026-01-26 16:41:35,104 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:41:35,106 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 上下文压缩器 (ContextCompressor)
INFO:     127.0.0.1:57571 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
2026-01-26 16:41:35,133 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
2026-01-26 16:41:35,139 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:54195 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
2026-01-26 16:41:35,147 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
2026-01-26 16:41:35,149 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
2026-01-26 16:41:35,149 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 内容版本库 (content_versions Table)
INFO:     127.0.0.1:61365 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61368 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 16:41:35,156 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions
INFO:     127.0.0.1:61369 - "GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:41:35,166 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 编辑会话存储区 (editing_sessions Table)
2026-01-26 16:41:35,173 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:41:35,175 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
INFO:     127.0.0.1:58400 - "PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 HTTP/1.1" 200 OK
2026-01-26 16:41:35,176 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:35,180 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: AI操作历史记录馆 (ai_operations Table)
2026-01-26 16:41:37,586 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:37,593 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 后端服务中枢 (FastAPI Backend)
2026-01-26 16:41:37,633 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:51475 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:41:37,648 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:41:37,649 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 内容版本控制与回滚
INFO:     127.0.0.1:51474 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:41:37,778 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 编辑会话管理
2026-01-26 16:41:37,839 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:57143 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:41:37,851 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: AI能力扩展与上下文感知
2026-01-26 16:41:37,859 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:56327 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:41:37,869 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 内容更新，新段落数: 88
2026-01-26 16:41:37,878 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 内容更新，新段落数: 88
2026-01-26 16:41:37,880 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 内容更新，新段落数: 88
2026-01-26 16:41:37,882 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 智能上下文压缩
2026-01-26 16:41:37,893 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:41:37,902 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 16:41:37,905 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:41:37,910 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:52447 - "PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 HTTP/1.1" 200 OK
2026-01-26 16:41:37,912 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:37,915 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 16:41:37,916 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
INFO:     127.0.0.1:52446 - "PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 HTTP/1.1" 200 OK
2026-01-26 16:41:37,921 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:52448 - "PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 HTTP/1.1" 200 OK
2026-01-26 16:41:37,924 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:37,939 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 云端自动保存
2026-01-26 16:41:41,948 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 分支与合并（远期规划）
2026-01-26 16:41:41,954 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:47,064 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:47,069 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 量化成功指标
2026-01-26 16:41:47,077 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:47,080 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:41:47,083 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:41:47,086 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:41:47,089 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:41:47,092 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:3e308f36-2885-48da-8da1-ddfb9d00a66c
2026-01-26 16:41:47,094 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 4, 'characters_updated': 0, 'locations_created': 4, 'settings_created': 7, 'relationships_created': 0}
2026-01-26 16:41:47,097 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:41:47,104 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-26 16:41:47,109 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:63156 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:41:49,042 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:41:49,043 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-26 16:41:49,043 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-26 16:41:49,060 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=d272bd22-39dc-4133-875d-2936d17f7762, delta=3005, edit_event_id=None
2026-01-26 16:41:49,061 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=2418c164-8a87-4e39-9b8f-319cdea6b5b1, delta=2674, edit_event_id=None
2026-01-26 16:41:49,061 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9698b76a-1119-4be2-b491-5439b57ba277, delta=2565, edit_event_id=None
2026-01-26 16:41:49,062 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=f54cc63f-7eb2-4eb3-9949-a4541dd4efec, delta=2481, edit_event_id=None
2026-01-26 16:41:49,062 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9becc1b4-4bc4-4ac1-992f-035440e66ec0, delta=2951, edit_event_id=None
2026-01-26 16:41:49,205 - app.services.import_service - INFO - 文本导入完成: 作品ID=84892aef-e8dc-49a8-8e1e-3d863045b9ba, 章节=5
2026-01-26 16:41:49,206 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 84892aef-e8dc-49a8-8e1e-3d863045b9ba 排队世界观提取任务
2026-01-26 16:41:49,207 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=84892aef-e8dc-49a8-8e1e-3d863045b9ba, 章节=5, 人物=0
2026-01-26 16:41:49,210 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:63333 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:41:49,214 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:41:51,468 - app.api.v1.chapters - INFO - [GET chapters] work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:41:51,494 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:41:51,496 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, type=<class 'uuid.UUID'>
2026-01-26 16:41:51,506 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:41:51,514 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:41:51,518 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:41:51,523 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:41:51,526 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-26 16:41:51,529 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:41:51,530 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:41:51,531 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:41:51,532 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:41:51,546 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:41:51,551 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=60s)
2026-01-26 16:41:51,558 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:41:51,565 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:41:51,566 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations
2026-01-26 16:41:51,568 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings
2026-01-26 16:41:51,569 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters
INFO:     127.0.0.1:64586 - "GET /api/v1/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba HTTP/1.1" 200 OK
2026-01-26 16:41:51,571 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/84892aef-e8dc-49a8-8e1e-3d863045b9ba
INFO:     127.0.0.1:64589 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64590 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:64588 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:64587 - "GET /api/v1/chapters/work/84892aef-e8dc-49a8-8e1e-3d863045b9ba HTTP/1.1" 200 OK
2026-01-26 16:41:51,581 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines
INFO:     127.0.0.1:64591 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines HTTP/1.1" 200 OK
2026-01-26 16:41:53,461 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-26 16:41:53,464 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:41:53,465 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-26 16:41:53,467 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines
INFO:     127.0.0.1:62837 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:41:57,310 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:41:57,355 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-26 16:41:57,375 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-26 16:41:57,403 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 16:41:57,419 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 16:41:59,610 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 16:41:59,610 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:41:59,615 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 16:41:59,616 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:41:59,619 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:41:59,622 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:65518 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:41:59,630 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53458 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:41:59,633 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
INFO:     127.0.0.1:56468 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:41:59,712 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:41:59,855 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:41:59,864 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:41:59,866 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:60968 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:60966 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:60967 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:42:02,018 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:42:02,025 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 84892aef-e8dc-49a8-8e1e-3d863045b9ba 提取世界观
2026-01-26 16:42:02,027 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status
INFO:     127.0.0.1:53162 - "GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status HTTP/1.1" 404 Not Found
2026-01-26 16:42:02,038 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
2026-01-26 16:42:02,044 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:42:02,049 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
INFO:     127.0.0.1:58436 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:42:02,052 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=3005
2026-01-26 16:42:02,053 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-26 16:42:02,054 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-26 16:42:02,055 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-26 16:42:02,057 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-26 16:42:02,057 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 13755
2026-01-26 16:42:02,057 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p>青州。</p><p>渊阳府，贤古县。</p><p>源顺镖局，后院偏房的一片空地内。</p><p>此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p>这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p>这些少年都是源顺镖局，今年新招的杂役弟子。</p><p>刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p>因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p>学得好的，有机会晋升为学徒。</p><p>一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖。</p><p>假以时日，业务熟练了，自己也能成为镖师。</p><p>镖师虽说是吃江湖饭的，有些危险，但对这些贫苦出身的少年们，这已经是相当好的职业了。</p><p>起码能吃饱肚子，而且多少是可以捞些油水的。</p><p>但现在，他们已经进门两个半月了。</p><p>心绪也从兴奋，慢慢变得黯淡了。</p><p>杂役弟子能成为学徒的，一批里，最多一二个，而且经常的，是成批成批的覆...
2026-01-26 16:42:02,066 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters
2026-01-26 16:42:02,069 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations
2026-01-26 16:42:02,077 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 13755
2026-01-26 16:42:02,077 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:42:02,077 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF53AA0E90>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:42:02,078 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:42:02,078 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:42:02,079 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:42:03,614 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:42:03,615 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
INFO:     127.0.0.1:51191 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:51192 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations HTTP/1.1" 200 OK
2026-01-26 16:42:03,647 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 16:42:03,653 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:42:03,654 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:42:03,655 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-26 16:42:03,678 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:42:03,679 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings
2026-01-26 16:42:03,686 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines
INFO:     127.0.0.1:56779 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:55185 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines HTTP/1.1" 200 OK
2026-01-26 16:42:03,700 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines
INFO:     127.0.0.1:54312 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:42:03,725 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:60331 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:42:03,732 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60333 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:42:03,791 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status
INFO:     127.0.0.1:56511 - "GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status HTTP/1.1" 404 Not Found
2026-01-26 16:42:03,804 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:61097 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:42:03,821 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:42:03,825 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
INFO:     127.0.0.1:57553 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:42:03,836 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:51188 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 16:42:03,841 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:03,844 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:55886 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:42:08,470 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:08,540 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 d272bd22-39dc-4133-875d-2936d17f7762 内容更新，新段落数: 88
2026-01-26 16:42:08,544 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 d272bd22-39dc-4133-875d-2936d17f7762 内容更新，新段落数: 88
2026-01-26 16:42:08,557 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:42:08,561 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:56588 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 16:42:08,563 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:12,069 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:42:12,075 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:56590 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 16:42:12,078 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:12,092 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 32 个数据块，总长度: 4075
2026-01-26 16:42:12,092 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 18050 (prompt=16041, completion=2009)
2026-01-26 16:42:12,093 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:42:12,094 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:42:12,096 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:15,008 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:42:15,011 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-26 16:42:15,013 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:42:15,014 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=18050, cost=$0.040141, time=66382ms
2026-01-26 16:42:15,016 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4075
2026-01-26 16:42:15,018 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: ```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "穿越者，前世为保险销售。获得了吞噬器物之灵（器灵）以获取技能与记忆的超凡能力。当前身份是源顺镖局的杂役弟子，心智成熟，目标明确，善于利用自身优势改变命运。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "主角段融的发小，在贤古县县衙担任捕快。为人仗义但略带炫耀心理，是主角前期重要的朋友与外部信息来源，将其与更广阔的江湖世界（如太一门）联系起来。",
      "first_appearance": "第5章",
      "importance": "中"
    },
    {
      "name": "赵穆",
      "role": "配角",
    ...
2026-01-26 16:42:15,018 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=9, 新地点=7, 新设定=5
2026-01-26 16:42:15,021 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 9人物, 7地点, 5设定
2026-01-26 16:42:15,030 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:15,032 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:63292 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:42:15,041 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-26 16:42:15,052 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-26 16:42:15,062 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-26 16:42:15,073 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-26 16:42:15,085 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-26 16:42:15,098 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-26 16:42:15,110 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-26 16:42:15,121 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-26 16:42:15,132 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-26 16:42:15,144 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-26 16:42:15,159 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-26 16:42:15,171 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-26 16:42:15,184 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-26 16:42:15,199 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-26 16:42:15,210 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-26 16:42:15,222 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县县衙
2026-01-26 16:42:15,235 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-26 16:42:15,248 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵系统
2026-01-26 16:42:15,259 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治体系
2026-01-26 16:42:15,271 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学修炼体系
2026-01-26 16:42:15,285 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 社会阶级与晋升路径
2026-01-26 16:42:15,293 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小/朋友。杨震在段融穿越后首次见面即表现出亲近和帮助，是主角在世界上第一个可信赖的盟友和信息来源。
2026-01-26 16:42:15,298 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 赵穆: 临时的师徒/上下级。赵穆作为教习轻视段融，而段融通过吞噬其刀灵获得了关键性的成长，两人之间已埋下潜在的冲突。
2026-01-26 16:42:15,299 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 段融(96b1858e-9d28-4f23-9f16-5461e0e44590) -> 孔斌、李充、张征(None)
2026-01-26 16:42:15,309 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:42:15,313 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:42:15,317 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:42:15,320 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:42:15,322 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:42:15,324 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 9, 'characters_updated': 0, 'locations_created': 7, 'settings_created': 5, 'relationships_created': 2}
2026-01-26 16:42:17,149 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:42:17,150 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-26 16:42:17,153 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-26 16:42:17,171 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=27a17757-3987-4117-84da-f9c74f3ab0d0, delta=3005, edit_event_id=None
2026-01-26 16:42:17,172 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=83fb7e17-3d83-4880-a4d0-99ca420a1676, delta=2674, edit_event_id=None
2026-01-26 16:42:17,173 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=bffc65fc-a543-4f4c-b823-a430a572ec52, delta=2565, edit_event_id=None
2026-01-26 16:42:17,174 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=a136312a-0333-4e14-84eb-f856dbb50ad9, delta=2481, edit_event_id=None
2026-01-26 16:42:17,176 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=6903be9b-2bc2-42d0-8b08-75d679ee3591, delta=2951, edit_event_id=None
2026-01-26 16:42:17,321 - app.services.import_service - INFO - 文本导入完成: 作品ID=b1456da2-6a55-49e8-ad42-2332dc579363, 章节=5
2026-01-26 16:42:17,325 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 b1456da2-6a55-49e8-ad42-2332dc579363 排队世界观提取任务
2026-01-26 16:42:17,326 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=b1456da2-6a55-49e8-ad42-2332dc579363, 章节=5, 人物=0
2026-01-26 16:42:17,328 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:63527 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:42:17,330 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:20,320 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:20,327 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-26 16:42:20,334 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:42:20,363 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:42:20,363 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 16:42:20,381 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:42:20,384 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:42:20,385 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:42:20,386 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:42:20,387 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:42:20,400 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:42:20,406 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 16:42:20,412 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:42:20,416 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:42:22,523 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:42:22,528 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:42:22,529 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
2026-01-26 16:42:22,530 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 16:42:22,531 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:42:22,533 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 16:42:22,534 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:51275 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51279 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:51278 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:51276 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51277 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:51280 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 16:42:22,548 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-26 16:42:22,555 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-26 16:42:24,939 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:42:24,959 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:42:24,964 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-26 16:42:24,969 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
2026-01-26 16:42:24,973 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
INFO:     127.0.0.1:51215 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:42:28,234 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
2026-01-26 16:42:28,239 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:42:28,256 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:42:30,687 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:42:30,695 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:42:30,695 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:42:30,782 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:42:30,783 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:42:30,783 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:42:30,852 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:42:30,855 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     127.0.0.1:60876 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:51263 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:42:30,863 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 b1456da2-6a55-49e8-ad42-2332dc579363 提取世界观
2026-01-26 16:42:30,933 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:42:30,939 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:42:30,945 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:65510 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:55834 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:55835 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:42:30,960 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:55837 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:42:30,993 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=3005
2026-01-26 16:42:30,996 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-26 16:42:31,000 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-26 16:42:31,000 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-26 16:42:31,001 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-26 16:42:31,002 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 13755
2026-01-26 16:42:31,004 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p>青州。</p><p>渊阳府，贤古县。</p><p>源顺镖局，后院偏房的一片空地内。</p><p>此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p>这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p>这些少年都是源顺镖局，今年新招的杂役弟子。</p><p>刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p>因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p>学得好的，有机会晋升为学徒。</p><p>一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖。</p><p>假以时日，业务熟练了，自己也能成为镖师。</p><p>镖师虽说是吃江湖饭的，有些危险，但对这些贫苦出身的少年们，这已经是相当好的职业了。</p><p>起码能吃饱肚子，而且多少是可以捞些油水的。</p><p>但现在，他们已经进门两个半月了。</p><p>心绪也从兴奋，慢慢变得黯淡了。</p><p>杂役弟子能成为学徒的，一批里，最多一二个，而且经常的，是成批成批的覆...
2026-01-26 16:42:33,936 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 13755
2026-01-26 16:42:33,936 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:42:33,936 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF53EF4320>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:42:33,936 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:42:33,938 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:42:33,938 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:42:35,739 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:42:35,740 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-26 16:42:35,780 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
2026-01-26 16:42:35,790 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:42:35,792 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
INFO:     127.0.0.1:61176 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 16:42:35,800 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:56559 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:42:35,859 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65346 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:42:35,899 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions
INFO:     127.0.0.1:56555 - "GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:42:35,975 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:50590 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 16:42:35,986 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:63957 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:42:36,109 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:42:36,116 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions
INFO:     127.0.0.1:61035 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56525 - "GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:42:36,158 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:42:36,159 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0
INFO:     127.0.0.1:56558 - "PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0 HTTP/1.1" 200 OK
2026-01-26 16:42:36,161 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:38,922 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:39,026 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 27a17757-3987-4117-84da-f9c74f3ab0d0 内容更新，新段落数: 88
2026-01-26 16:42:39,040 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:42:39,043 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:42:39,044 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 27a17757-3987-4117-84da-f9c74f3ab0d0 内容更新，新段落数: 88
INFO:     127.0.0.1:62868 - "PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0 HTTP/1.1" 200 OK
2026-01-26 16:42:39,047 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:39,060 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:42:42,135 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:42:42,137 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
INFO:     127.0.0.1:62867 - "PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0 HTTP/1.1" 200 OK
2026-01-26 16:42:42,141 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:42,149 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 33 个数据块，总长度: 4389
2026-01-26 16:42:42,150 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 17408 (prompt=15325, completion=2083)
2026-01-26 16:42:42,151 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:42:42,151 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:42:45,296 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:45,300 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:42:45,301 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=17408, cost=$0.039986, time=67130ms
2026-01-26 16:42:45,302 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4389
2026-01-26 16:42:45,303 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: ```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "魂穿者，源顺镖局杂役弟子，拥有“吞噬器灵”的特殊能力。性格坚韧，为提升实力不惜代价，利用前世的社会经验处理人际关系。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "主角段融的发小，贤古县捕快。为人仗义，消息灵通，是主角与外界社会联系的纽带，并引入了“太一门”等更广阔的世界信息。",
      "first_appearance": "第5章",
      "importance": "中"
    },
    {
      "name": "赵穆",
      "role": "配角",
      "description": "源顺镖局实习镖师，负责教导杂役...
2026-01-26 16:42:45,304 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=7, 新设定=7
2026-01-26 16:42:45,308 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 11人物, 7地点, 7设定
2026-01-26 16:42:45,324 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-26 16:42:45,337 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:45,339 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-26 16:42:45,352 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-26 16:42:45,366 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-26 16:42:45,379 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-26 16:42:45,389 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-26 16:42:45,566 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-26 16:42:45,579 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-26 16:42:45,586 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-26 16:42:45,595 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-26 16:42:45,604 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-26 16:42:45,611 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-26 16:42:45,618 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-26 16:42:45,627 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-26 16:42:45,639 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-26 16:42:45,651 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-26 16:42:45,668 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-26 16:42:45,686 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-26 16:42:45,692 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-26 16:42:45,697 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治
2026-01-26 16:42:45,713 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学体系
2026-01-26 16:42:45,736 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵
2026-01-26 16:42:45,764 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 九州八大宗门
2026-01-26 16:42:45,783 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武者修行资源
2026-01-26 16:42:45,798 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 货币体系
2026-01-26 16:42:45,805 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小、朋友
2026-01-26 16:42:45,808 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 李充 -> 段融: 敌对、竞争者
2026-01-26 16:42:45,810 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 赵穆 -> 段融: 有矛盾的上下级
2026-01-26 16:42:45,812 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 孔斌 -> 段融: 竞争者
2026-01-26 16:42:45,822 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:42:45,825 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:42:45,827 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:42:45,829 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:42:45,831 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 16:42:45,832 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 11, 'characters_updated': 0, 'locations_created': 7, 'settings_created': 7, 'relationships_created': 4}
2026-01-26 16:42:46,325 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 预览导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:42:46,334 - app.api.v1.import_routes - INFO - 预览成功: 作品=一夕千悟，从杂役弟子开始, 章节数=5
2026-01-26 16:42:46,339 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import/preview
INFO:     127.0.0.1:59463 - "POST /api/v1/works/import/preview HTTP/1.1" 200 OK
2026-01-26 16:42:48,163 - app.api.v1.import_routes - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 导入文件: 一夕千悟，从杂役弟子开始.txt, 格式: txt
2026-01-26 16:42:48,165 - app.api.v1.import_routes - INFO - [导入参数] auto_extract_worldview=True, format=txt, background_tasks=True
2026-01-26 16:42:48,166 - app.services.import_service - INFO - 用户 79913e7e-d5cd-4e09-bce6-ca6639bd8456 开始导入文本数据
2026-01-26 16:42:48,200 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=c02aff55-7819-4477-b7ff-27300884f662, delta=3005, edit_event_id=None
2026-01-26 16:42:48,202 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=78a840b2-e622-4230-b649-345b5d91f9eb, delta=2674, edit_event_id=None
2026-01-26 16:42:48,203 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=e366c6f6-5e16-47d2-be9b-824b7a49a0ef, delta=2565, edit_event_id=None
2026-01-26 16:42:48,205 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=9e65d7f6-85c9-4bb4-a2f3-6ce886387672, delta=2481, edit_event_id=None
2026-01-26 16:42:48,206 - app.services.chapter_word_stat_service - INFO - 记录字数增量: chapter_id=cf119734-c397-4025-a3f8-0147da826cdb, delta=2951, edit_event_id=None
2026-01-26 16:42:48,371 - app.services.import_service - INFO - 文本导入完成: 作品ID=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, 章节=5
2026-01-26 16:42:48,372 - app.api.v1.import_routes - INFO - [世界观提取] 已为作品 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 排队世界观提取任务
2026-01-26 16:42:48,373 - app.api.v1.import_routes - INFO - 导入成功: 作品ID=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, 章节=5, 人物=0
2026-01-26 16:42:48,376 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/works/import
INFO:     127.0.0.1:63605 - "POST /api/v1/works/import HTTP/1.1" 200 OK
2026-01-26 16:42:48,380 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:42:50,846 - app.api.v1.chapters - INFO - [GET chapters] work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:42:50,859 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:42:50,859 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, type=<class 'uuid.UUID'>
2026-01-26 16:42:50,872 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:42:50,874 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:42:50,878 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:42:50,879 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:42:50,881 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:42:50,882 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:42:50,882 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:42:50,882 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:42:50,890 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:42:50,894 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=60s)
2026-01-26 16:42:50,896 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第2章 浑圆桩 (order=2)
2026-01-26 16:42:50,898 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:42:50,899 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings
2026-01-26 16:42:50,900 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters
2026-01-26 16:42:50,901 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines
2026-01-26 16:42:50,903 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
INFO:     127.0.0.1:56662 - "GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56666 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:56664 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:56667 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:56663 - "GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
2026-01-26 16:42:52,952 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:42:52,955 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第2章 浑圆桩 (65 paragraphs)
2026-01-26 16:42:52,958 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第3章 一夕千悟 (order=3)
2026-01-26 16:42:52,960 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines
INFO:     127.0.0.1:52751 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:42:52,971 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:42:52,975 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations
INFO:     127.0.0.1:56665 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations HTTP/1.1" 200 OK
2026-01-26 16:42:55,472 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第3章 一夕千悟 (64 paragraphs)
2026-01-26 16:42:55,473 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第4章 家底 (order=4)
2026-01-26 16:42:59,445 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第4章 家底 (60 paragraphs)
2026-01-26 16:42:59,454 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:42:59,465 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:42:59,495 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:42:59,498 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:42:59,649 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:42:59,652 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:55788 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:60589 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:42:59,944 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:42:59,956 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62800 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:42:59,969 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:62801 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:62799 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:43:00,034 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:03,256 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status
INFO:     127.0.0.1:51686 - "GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status HTTP/1.1" 404 Not Found
2026-01-26 16:43:03,270 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions
INFO:     127.0.0.1:64080 - "GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:43:03,281 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 37 个数据块，总长度: 4760
2026-01-26 16:43:03,284 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 16343 (prompt=14038, completion=2305)
2026-01-26 16:43:03,288 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:43:03,289 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:43:03,303 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:43:03,318 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters
2026-01-26 16:43:03,320 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:03,321 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
INFO:     127.0.0.1:50954 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters HTTP/1.1" 200 OK
2026-01-26 16:43:03,329 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:43:03,331 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=16343, cost=$0.040598, time=59634ms
2026-01-26 16:43:03,333 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4760
2026-01-26 16:43:03,334 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: 好的，遵照您的指示，这是对《第1章》到《第5章》内容进行综合分析后，提取的世界观新增与变化，以JSON格式呈现。

```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "魂穿者，源顺镖局的杂役弟子。获得了吞噬器灵的金手指，能吸收兵器中的经验与记忆，从而快速掌握武学。性格坚韧、务实，为了变强不惜一切代价。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "主角段融的发小，在贤古县衙门当捕快。为人热情，是主角前期重要的信息来源与人脉支持。其二叔在生药铺做账房，家境尚可。",
      "first_appearance": "第5章",
      "importance": "高"
    },
    {
      "nam...
2026-01-26 16:43:03,335 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=7, 新设定=7
2026-01-26 16:43:03,339 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 11人物, 7地点, 7设定
2026-01-26 16:43:03,346 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:43:03,399 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:43:03,416 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     127.0.0.1:51283 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:43:03,434 - app.api.v1.import_routes - INFO - [世界观提取] 开始为作品 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 提取世界观
2026-01-26 16:43:03,439 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:43:03,441 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations
INFO:     127.0.0.1:54491 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations HTTP/1.1" 200 OK
2026-01-26 16:43:03,448 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings
2026-01-26 16:43:03,449 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
INFO:     127.0.0.1:55832 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings HTTP/1.1" 200 OK
2026-01-26 16:43:03,471 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:43:03,526 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 1 '第1章 吞噬': 内容长度=4677
2026-01-26 16:43:03,532 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 2 '第2章 浑圆桩': 内容长度=2674
2026-01-26 16:43:03,538 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 3 '第3章 一夕千悟': 内容长度=2565
2026-01-26 16:43:03,542 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 4 '第4章 家底': 内容长度=2481
2026-01-26 16:43:03,546 - app.services.worldview_sync_service - INFO - [世界观同步] 章节 5 '第5章 太一门': 内容长度=2951
2026-01-26 16:43:03,549 - app.services.worldview_sync_service - INFO - [世界观同步] 合并 5 个章节，总内容长度: 15427
2026-01-26 16:43:03,551 - app.services.worldview_sync_service - INFO - [世界观同步] 内容预览:

【第1章 第1章 吞噬】
<p data-id="wjd1p5ac">青州。</p><p data-id="grap620u">渊阳府，贤古县。</p><p data-id="zo8bhafm">源顺镖局，后院偏房的一片空地内。</p><p data-id="fs4w4poh">此处是镖局内，堆放柴炭的地方，平常少有人至，但此时，却有十多个单薄的身影，在空地上，稀稀落落地站着。</p><p data-id="xiniw64q">这些人都是十五六岁的少年，身体大多都还没长开，脸上都泛着长期营养不良的菜色。</p><p data-id="kacewcqo">这些少年都是源顺镖局，今年新招的杂役弟子。</p><p data-id="bg6eo5w6">刚进源顺镖局的时候，他们还一个个都兴奋异常。</p><p data-id="wy7io2dz">因为源顺镖局的杂役弟子，是有机会学些粗浅的拳脚武技的。</p><p data-id="kvn00cfj">学得好的，有机会晋升为学徒。</p><p data-id="eyv203df">一旦成为学徒，就能学到真正的武功，而且可以跟随镖师，出去走镖...
2026-01-26 16:43:03,562 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:43:03,577 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines
2026-01-26 16:43:03,590 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines
INFO:     127.0.0.1:59747 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines HTTP/1.1" 200 OK
2026-01-26 16:43:03,596 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
INFO:     127.0.0.1:59749 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:43:03,631 - app.services.worldview_sync_service - INFO - [世界观同步] 开始AI分析，章节数: 5, 内容长度: 15427
2026-01-26 16:43:03,631 - app.services.worldview_sync_service - INFO - [世界观同步] 现有世界观: （暂无世界观数据）...
2026-01-26 16:43:03,632 - app.services.worldview_sync_service - INFO - [世界观同步] db=<sqlalchemy.ext.asyncio.session.AsyncSession object at 0x000001FF7578FBC0>, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:43:03,632 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:43:03,632 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:43:03,633 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:43:05,674 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:43:05,675 - app.services.worldview_sync_service - INFO - [世界观同步] AI服务初始化完成: api_key=***KFzr, base_url=https://204992.xyz:8443/v1, model=gemini-2.5-pro
2026-01-26 16:43:05,698 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions
2026-01-26 16:43:05,700 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
INFO:     127.0.0.1:63364 - "GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:43:05,717 - app.services.ai.http_ai_service - WARNING - [ModelSelector] ⚠️ 未传递task_type，使用默认模型: gemini-2.5-pro
2026-01-26 16:43:05,719 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=3000, temp=0.3, task_type=None
2026-01-26 16:43:05,741 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:43:05,751 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:05,761 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:43:05,762 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
INFO:     127.0.0.1:60396 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:43:05,764 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:56411 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:43:05,769 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60545 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:43:10,606 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status
INFO:     127.0.0.1:49245 - "GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status HTTP/1.1" 404 Not Found
2026-01-26 16:43:10,636 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-26 16:43:10,639 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:43:10,703 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-26 16:43:10,730 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:55421 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:43:10,756 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-26 16:43:10,866 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-26 16:43:10,870 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:57740 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:43:10,938 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-26 16:43:11,035 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-26 16:43:11,043 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 c02aff55-7819-4477-b7ff-27300884f662 内容更新，新段落数: 88
2026-01-26 16:43:11,056 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 c02aff55-7819-4477-b7ff-27300884f662 内容更新，新段落数: 88
2026-01-26 16:43:11,060 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:11,066 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 c02aff55-7819-4477-b7ff-27300884f662 内容更新，新段落数: 88
INFO:     127.0.0.1:57871 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 16:43:11,102 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 c02aff55-7819-4477-b7ff-27300884f662 内容更新，新段落数: 88
2026-01-26 16:43:11,123 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:43:11,152 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:11,167 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-26 16:43:11,184 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:43:11,191 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     127.0.0.1:55418 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:43:11,203 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:43:11,210 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:43:11,223 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:11,233 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:11,235 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, type=<class 'uuid.UUID'>
2026-01-26 16:43:11,242 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:11,245 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:43:11,245 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:43:11,246 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:43:11,247 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:43:11,288 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:43:11,297 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=60s)
2026-01-26 16:43:11,307 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
INFO:     127.0.0.1:55417 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:43:11,318 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:62220 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:43:11,329 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:43:11,346 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:43:11,373 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:43:14,222 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:55419 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:43:14,232 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
INFO:     127.0.0.1:56593 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 16:43:14,257 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
2026-01-26 16:43:14,274 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-26 16:43:17,794 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
INFO:     127.0.0.1:60356 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
2026-01-26 16:43:17,809 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:43:17,821 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:43:19,102 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:43:19,108 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:43:19,130 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:43:19,133 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
2026-01-26 16:43:19,140 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 16:43:19,143 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-26 16:43:19,147 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,152 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
INFO:     127.0.0.1:55189 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
2026-01-26 16:43:19,159 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:43:19,159 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
2026-01-26 16:43:19,161 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
2026-01-26 16:43:19,163 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
INFO:     127.0.0.1:63588 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:56263 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61029 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
2026-01-26 16:43:19,181 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,238 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:54412 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 16:43:19,274 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,286 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,293 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,301 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,305 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
2026-01-26 16:43:19,305 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
2026-01-26 16:43:19,307 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
2026-01-26 16:43:19,309 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
INFO:     127.0.0.1:60830 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64229 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:59530 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:59529 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
2026-01-26 16:43:19,367 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:19,368 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
INFO:     127.0.0.1:61023 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
2026-01-26 16:43:19,376 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-26 16:43:19,392 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-26 16:43:19,399 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-26 16:43:19,404 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:51667 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 16:43:19,409 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-26 16:43:19,418 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-26 16:43:19,427 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-26 16:43:19,432 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵设定
2026-01-26 16:43:19,439 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治
2026-01-26 16:43:19,450 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学体系
2026-01-26 16:43:19,457 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武者修炼方式
2026-01-26 16:43:19,472 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 职业晋升体系（镖局）
2026-01-26 16:43:19,482 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 货币体系
2026-01-26 16:43:19,488 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小/挚友
2026-01-26 16:43:19,490 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 赵穆 -> 段融: 师徒/潜在敌对关系（因器灵被吞噬）
2026-01-26 16:43:19,490 - app.services.worldview_sync_service - WARNING - [世界观同步] 无法找到人物ID: 孔斌、李充、张征(None) -> 段融(2a24672e-8478-4ffb-9ba3-de898614408d)
2026-01-26 16:43:19,492 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 解道寒 -> 杨震: 上司与受信任的下属
2026-01-26 16:43:19,492 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 解道寒 -> 解雷: 叔侄
2026-01-26 16:43:19,503 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:43:19,507 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:43:19,509 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:43:19,512 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:43:19,515 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 16:43:19,515 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 11, 'characters_updated': 0, 'locations_created': 7, 'settings_created': 7, 'relationships_created': 4}
2026-01-26 16:43:20,811 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:43:20,827 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:43:20,827 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:43:20,830 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55940 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:43:20,940 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:43:20,947 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:43:20,947 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:43:20,949 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61978 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:43:21,138 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:21,139 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
INFO:     127.0.0.1:55839 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:43:21,140 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:43:22,469 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:43:22,492 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:59534 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 16:43:22,498 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions
INFO:     127.0.0.1:54525 - "GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:43:22,526 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:22,527 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:51748 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 16:43:22,529 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d
INFO:     127.0.0.1:59143 - "PUT /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d HTTP/1.1" 200 OK
2026-01-26 16:43:22,532 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:43:23,762 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions
INFO:     127.0.0.1:50159 - "GET /api/v1/chapters/13869f82-8947-4992-a6bc-8d6ea4de1b2d/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:43:23,773 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:43:29,577 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 16:43:29,584 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 16:43:29,588 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e43a4f06-f97c-43bf-8801-7b25b8a3f4af
2026-01-26 16:43:29,589 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:43:29,592 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:65087 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:43:29,621 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 16:43:29,639 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions
2026-01-26 16:43:29,641 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:50651 - "GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:43:29,647 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e43a4f06-f97c-43bf-8801-7b25b8a3f4af
2026-01-26 16:43:29,648 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:43:29,653 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50647 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:43:29,730 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:50650 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:43:29,748 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions
INFO:     127.0.0.1:65037 - "GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:43:29,894 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:29,897 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:55702 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 16:43:29,899 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:43:32,584 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:43:32,655 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:57237 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:43:32,707 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:43:32,707 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:43:32,708 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:43:34,652 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:43:34,654 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 16:43:34,659 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4010049e-6d95-4abe-872d-1eb0c0d756d5 内容更新，新段落数: 70
2026-01-26 16:43:34,663 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 34 个数据块，总长度: 4482
2026-01-26 16:43:34,663 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 16517 (prompt=14333, completion=2184)
2026-01-26 16:43:34,664 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:43:34,664 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:43:34,666 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62524 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 16:43:34,672 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:43:34,672 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=16517, cost=$0.039756, time=58871ms
2026-01-26 16:43:34,674 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4482
2026-01-26 16:43:34,674 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: ```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "小说主角，从现代社会魂穿而来。原为源顺镖局的杂役弟子，资质平平。魂穿后获得“吞噬器灵”的特殊能力，可以通过吞噬兵器中的器灵来快速掌握武功。目标是成为学徒，并探索自身能力的秘密。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "主角段融的发小，在贤古县县衙担任捕快。为人仗义但略带炫耀心理。因其二叔在生药铺工作，有一定的人脉和见识，是主角前期获取外界信息的重要来源，也是主角在世界上为数不多的情感纽带。",
      "first_appearance": "第5章",
      "importance": "高"
    },
    {
      "name": "赵穆...
2026-01-26 16:43:34,675 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=7, 新设定=5
2026-01-26 16:43:34,678 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 11人物, 7地点, 5设定
2026-01-26 16:43:34,682 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:34,685 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:65493 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 16:43:34,687 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:43:34,692 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 第1章读起来像流水账，帮我改得更有小说味一点...
2026-01-26 16:43:37,545 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-26 16:43:37,566 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:43:37,605 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=9, 地点=7, 设定=5, 规范=无
2026-01-26 16:43:37,607 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b0a47953-7246-42d6-bb24-eba29c2606ad:d25295f3-b024-477c-9990-a00e67178f26 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, conversation_id=d25295f3-b024-477c-9990-a00e67178f26)
2026-01-26 16:43:37,617 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b0a47953-7246-42d6-bb24-eba29c2606ad:d25295f3-b024-477c-9990-a00e67178f26
2026-01-26 16:43:37,619 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b0a47953-7246-42d6-bb24-eba29c2606ad:d25295f3-b024-477c-9990-a00e67178f26: 0/16000 tokens
2026-01-26 16:43:37,819 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='第1章读起来像流水账，帮我改得更有小说味一点...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:b0a47953-7246-42d6-bb24-eba29c2606ad', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-26 16:43:37,820 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=b0a47953-7246-42d6-bb24-eba29c2606ad | 含用户级=True | 找到=0条
2026-01-26 16:43:37,838 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 230.06ms
2026-01-26 16:43:37,839 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:43:37,839 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:43:37,840 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:43:37,852 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-26 16:43:37,909 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-26 16:43:37,938 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-26 16:43:37,956 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4010049e-6d95-4abe-872d-1eb0c0d756d5 内容更新，新段落数: 70
2026-01-26 16:43:37,965 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-26 16:43:38,125 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-26 16:43:38,129 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:38,135 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:60135 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 16:43:38,138 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:43:38,143 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-26 16:43:40,575 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-26 16:43:40,582 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:43:40,586 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4010049e-6d95-4abe-872d-1eb0c0d756d5 内容更新，新段落数: 70
2026-01-26 16:43:40,590 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-26 16:43:40,597 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 16:43:40,600 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:60136 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 16:43:40,601 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:43:40,607 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-26 16:43:42,867 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:43:42,868 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:43:42,873 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:43:42,874 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-26 16:43:42,885 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-26 16:43:42,894 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:43:42,895 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-26 16:43:42,896 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=360, cost=$0.000042, time=5028ms
2026-01-26 16:43:42,897 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-26 16:43:42,897 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:43:42,897 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:43:42,898 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:43:42,905 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-26 16:43:42,914 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-26 16:43:42,922 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-26 16:43:42,930 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-26 16:43:42,938 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-26 16:43:42,947 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-26 16:43:42,955 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治体系
2026-01-26 16:43:42,964 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵与武学
2026-01-26 16:43:42,972 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学修炼体系
2026-01-26 16:43:42,980 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 镖局职业体系
2026-01-26 16:43:42,987 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 杨震: 发小/朋友
2026-01-26 16:43:42,989 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 赵穆: 上下级与初期对立者
2026-01-26 16:43:42,990 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 段融 -> 孔斌: 同门与竞争对手
2026-01-26 16:43:42,992 - app.services.worldview_sync_service - INFO - [世界观同步] 创建关系: 杨震 -> 解道寒: 上下级（受其信任）
2026-01-26 16:43:43,000 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:43:43,002 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:43:43,004 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:43:43,006 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:43:43,008 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:43:43,009 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 11, 'characters_updated': 0, 'locations_created': 7, 'settings_created': 5, 'relationships_created': 4}
2026-01-26 16:43:45,179 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:43:45,180 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:43:45,204 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:43:45,207 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=298, cost=$0.000030, time=2283ms
2026-01-26 16:43:45,207 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 16:43:45,209 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 16:43:45,209 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 16:43:45,210 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 第1章读起来像流水账，帮我改得更有小说味一点...
2026-01-26 16:43:45,218 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:43:45,224 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:43:45,225 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:43:45,225 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:43:57,709 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:44:00,167 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:44:04,784 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1719
2026-01-26 16:44:04,785 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 21272 (prompt=20431, completion=841)
2026-01-26 16:44:04,785 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:44:04,787 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:44:04,813 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:44:04,815 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=21272, cost=$0.033949, time=19561ms
2026-01-26 16:44:04,816 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=21272
2026-01-26 16:44:04,817 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望将第一章改写得更有小说感，避免流水账风格。最终需要生, 原料=需要读取第一章的原文内容，并对其进行分析, 处理=这是一个创作类请求，应分阶段执行。第一阶
2026-01-26 16:44:04,817 - app.services.agent.planning.plan_generator - INFO - [Planning] 直接回答模式，答案长度: 200
2026-01-26 16:44:04,819 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-26 16:44:04,819 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 19.61s
2026-01-26 16:44:04,820 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-26 16:44:04,820 - app.services.agent.langgraph_agent - WARNING - [Planning-Alert] AI 违反协议：同时返回 direct_answer(200字) 和 2 个 tasks，将执行 tasks 而忽略 direct_answer
2026-01-26 16:44:04,821 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:44:04,822 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:44:04,823 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:44:04,823 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=2, 有依赖任务=1
2026-01-26 16:44:04,825 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 读取当前章节内容，为分析做准备
2026-01-26 16:44:04,826 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节内容，为分析做准备 (icon=Wrench)
2026-01-26 16:44:04,827 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:44:04,829 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, target=读取第一章(chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d7...
2026-01-26 16:44:04,829 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1章
2026-01-26 16:44:04,830 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, target=读取第一章(chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d7...
2026-01-26 16:44:04,831 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:44:04,902 - app.services.agent.tools.explore_tools - INFO - [_extract_keywords] 提取关键词: ['chapter', 'id', '4010049e', '6d95', '4abe', '872d', '1eb0c0d756d5', '读取', '原文', '第一章']...
2026-01-26 16:44:04,903 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用提取的关键词: ['chapter', 'id', '4010049e', '6d95', '4abe', '872d', '1eb0c0d756d5', '读取', '原文', '第一章']
2026-01-26 16:44:04,904 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围: (1, 1)
2026-01-26 16:44:04,938 - app.services.chapter_vector_service - INFO - [exact_search] work=b0a47953-7246-42d6-bb24-eba29c2606ad, keywords=['chapter', 'id', '4010049e']..., mode=any, range=(1, 1), hits=2
2026-01-26 16:44:04,939 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 2 条
2026-01-26 16:44:04,939 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 2 条
2026-01-26 16:44:04,940 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 2 条证据)
2026-01-26 16:44:04,941 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:44:04,941 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:44:04,942 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:44:20,732 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 36 个数据块，总长度: 4645
2026-01-26 16:44:20,733 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 18658 (prompt=16364, completion=2294)
2026-01-26 16:44:20,733 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 实例, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:44:20,734 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:44:20,745 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:44:20,745 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:实例): tokens=18658, cost=$0.043395, time=75013ms
2026-01-26 16:44:20,746 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应长度: 4645
2026-01-26 16:44:20,746 - app.services.worldview_sync_service - INFO - [世界观同步] AI响应内容: ```json
{
  "new_characters": [
    {
      "name": "段融",
      "role": "主角",
      "description": "本作主角。一名穿越者，继承了源顺镖局杂役弟子的身体和记忆。拥有“吞噬器灵”的超凡能力，能通过吸收器物中的“器灵”来直接获得使用者的技能、经验和记忆。性格务实，目标明确，利用能力在新世界求生并力争上游。",
      "first_appearance": "第1章",
      "importance": "高"
    },
    {
      "name": "杨震",
      "role": "配角",
      "description": "段融的发小，在贤古县衙门担任捕快。因其二叔在生药铺做账房而有些人脉。为人热情，是段融在镖局之外的重要社会关系，也是他了解外部世界信息的重要窗口。",
      "first_appearance": "第5章",
      "importance": "中"
    },
    {
      "name": "赵穆",
...
2026-01-26 16:44:20,747 - app.services.worldview_sync_service - INFO - [世界观同步] 解析结果: 新人物=11, 新地点=9, 新设定=7
2026-01-26 16:44:20,752 - app.api.v1.import_routes - INFO - [世界观提取] 扫描完成: 5章, 发现 11人物, 9地点, 7设定
2026-01-26 16:44:20,773 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 段融
2026-01-26 16:44:20,782 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 杨震
2026-01-26 16:44:20,788 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 赵穆
2026-01-26 16:44:20,798 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 许儒虎
2026-01-26 16:44:20,808 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解道寒
2026-01-26 16:44:20,816 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孔斌
2026-01-26 16:44:20,824 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 李充
2026-01-26 16:44:20,833 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 张征
2026-01-26 16:44:20,841 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 萧宗庭
2026-01-26 16:44:20,847 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 孙老头
2026-01-26 16:44:20,855 - app.services.worldview_sync_service - INFO - [世界观同步] 创建人物: 解雷
2026-01-26 16:44:20,861 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 九州大陆
2026-01-26 16:44:20,867 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 太一门
2026-01-26 16:44:20,875 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 青州
2026-01-26 16:44:20,884 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 源顺镖局
2026-01-26 16:44:20,892 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 贤古县
2026-01-26 16:44:20,900 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 渊阳府
2026-01-26 16:44:20,905 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 县衙
2026-01-26 16:44:20,913 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 马坊
2026-01-26 16:44:20,921 - app.services.worldview_sync_service - INFO - [世界观同步] 创建地点: 地牢
2026-01-26 16:44:20,928 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 吞噬器灵
2026-01-26 16:44:20,934 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 器灵设定
2026-01-26 16:44:20,946 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 宗门统治体系
2026-01-26 16:44:20,958 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武学修炼体系
2026-01-26 16:44:20,969 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 镖局晋升体系
2026-01-26 16:44:20,979 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 武者经济学
2026-01-26 16:44:20,987 - app.services.worldview_sync_service - INFO - [世界观同步] 创建设定: 货币体系
2026-01-26 16:44:20,991 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:44:20,995 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:44:20,996 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:44:20,998 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:44:21,000 - app.services.worldview_sync_service - INFO - [Worldview Sync] Cache invalidated: worldview:worlddata:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:44:21,000 - app.api.v1.import_routes - INFO - [世界观提取] 应用完成: {'characters_created': 11, 'characters_updated': 0, 'locations_created': 9, 'settings_created': 7, 'relationships_created': 0}
2026-01-26 16:44:28,978 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:44:28,978 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:44:28,991 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:44:28,992 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3095, cost=$0.005636, time=24037ms
2026-01-26 16:44:28,993 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=420, 尝试次数=1
2026-01-26 16:44:28,993 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {},
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": false,
    "has_plot_details": true
  },
  "summary": "收集到的信息包含第1章的两个片段。片段显示一个名叫“段融”的角色，在紧张状态下念出“读取器灵！”的指令。",
  "next_action": "下一步将读取并提供第一章(chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5)的全部原文内容，以完成任务。",
  "potential_gaps": [
    "第一章的完整原文内容"
  ]
}
```
2026-01-26 16:44:28,994 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=0/0, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:44:28,994 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=2, 章节=1, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 16:44:28,995 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则4命中: 证据<5 → 不足
2026-01-26 16:44:28,995 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 评估不足，缺失项: ['第一章的完整原文内容']
2026-01-26 16:44:28,996 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段3：AI 补充循环，当前 2 条证据
2026-01-26 16:44:28,996 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:44:28,997 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:44:28,997 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.3, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:44:44,895 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:44:44,897 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:44:44,924 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:44:44,929 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2059, cost=$0.005304, time=15900ms
2026-01-26 16:44:44,930 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=517, 尝试次数=1
2026-01-26 16:44:44,931 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 任务理解完成: 根据提供的唯一ID（chapter_id）来精确定位并获取特定章节的文本内容。...
2026-01-26 16:44:44,932 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:44:44,933 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:44:44,934 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:44:46,639 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:44:46,639 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:44:46,655 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:44:46,656 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=904, cost=$0.000164, time=1706ms
2026-01-26 16:44:46,656 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=384, 尝试次数=1
2026-01-26 16:44:46,657 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, type=<class 'uuid.UUID'>
2026-01-26 16:44:46,666 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:44:46,667 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:44:46,668 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:44:46,668 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:44:46,694 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1章 -> 第1章
2026-01-26 16:44:46,700 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:44:46,714 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-26 16:44:46,721 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, current_order=1, query=第一章的完整原文内容...
2026-01-26 16:44:46,812 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 16:44:47,821 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:44:47,822 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:44:47,831 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第38段
2026-01-26 16:44:47,846 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第33段
2026-01-26 16:44:47,854 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第71段
2026-01-26 16:44:47,863 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, current_order=1, query=章节ID 4010049e-6d95-4abe-872d-1eb0c0d756d5的文本...
2026-01-26 16:44:47,978 - app.services.chapter_vector_service - INFO - RAG retrieved 5 segments within order<=1
2026-01-26 16:44:48,592 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 5 个候选 -> top 5
2026-01-26 16:44:48,593 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:44:48,601 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, current_order=1, query=获取章节4010049e-6d95-4abe-872d-1eb0c0d756d5的原文...
2026-01-26 16:44:48,694 - app.services.chapter_vector_service - INFO - RAG retrieved 8 segments within order<=1
2026-01-26 16:44:50,051 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 8 个候选 -> top 5
2026-01-26 16:44:50,052 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:44:50,055 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:44:50,055 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:44:50,055 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:45:21,198 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:45:21,198 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:45:21,226 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:45:21,229 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3283, cost=$0.006081, time=31143ms
2026-01-26 16:45:21,231 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=460, 尝试次数=1
2026-01-26 16:45:21,232 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {},
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": false,
    "has_plot_details": true
  },
  "summary": "已收集的信息包含第1章的3个段落片段。内容提及角色“段融”执行“读取器灵”操作，并观察到“吞噬效果”等数据。",
  "next_action": "使用chapter_id '4010049e-6d95-4abe-872d-1eb0c0d756d5'，通过访问指定的数据源（数据库或API），提取并呈现第1章的完整文本内容。",
  "potential_gaps": [
    "第1章的完整原文内容",
    "访问章节内容的数据源或API接口信息"
  ]
}
```
2026-01-26 16:45:21,232 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=0/0, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:45:21,233 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=2, 章节=1, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 16:45:21,234 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则4命中: 证据<5 → 不足
2026-01-26 16:45:21,235 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:45:21,236 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:45:21,237 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:45:23,379 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:45:23,379 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:45:23,391 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:45:23,392 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=920, cost=$0.000152, time=2142ms
2026-01-26 16:45:23,393 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=337, 尝试次数=1
2026-01-26 16:45:23,393 - app.services.agent.tools.explore_tools - INFO - [ExploreState] 搜索词与已有词相似，跳过: '章节ID 4010049e-6d95-4abe-872d-1' ~ '章节ID 4010049e-6d95-4abe-872d-1'
2026-01-26 16:45:23,400 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, current_order=1, query=第一章原文内容...
2026-01-26 16:45:23,484 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 16:45:24,309 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 16:45:24,310 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:45:24,318 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第43段
2026-01-26 16:45:24,324 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第75段
2026-01-26 16:45:24,332 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第53段
2026-01-26 16:45:24,338 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, current_order=1, query=获取章节4010049e-6d95-4abe-872d-1eb0c0d756d5原文的方法...
2026-01-26 16:45:24,436 - app.services.chapter_vector_service - INFO - RAG retrieved 6 segments within order<=1
2026-01-26 16:45:25,186 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 6 个候选 -> top 5
2026-01-26 16:45:25,187 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:45:25,189 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:45:25,190 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:45:25,190 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:45:50,182 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:45:50,183 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:45:50,203 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:45:50,204 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3366, cost=$0.006141, time=24993ms
2026-01-26 16:45:50,204 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=461, 尝试次数=1
2026-01-26 16:45:50,205 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {},
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": false,
    "has_plot_details": true
  },
  "exploration_summary": "收集到的信息包含角色'段融'执行'读取器灵'的片段，以及该操作产生的'吞噬效果'，具体列出了不同刀法的熟练度等级。",
  "next_action": "使用章节ID '4010049e-6d95-4abe-872d-1eb0c0d756d5'，通过查询数据源（数据库或API）来获取第一章的完整原文内容。",
  "potential_gaps": [
    "章节的完整原文内容",
    "存储章节内容的数据源信息及访问方法"
  ]
}
```
2026-01-26 16:45:50,206 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=0/0, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:45:50,207 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=6, 章节=1, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 16:45:50,208 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则5: 边界情况 → 不足（保守策略）
2026-01-26 16:45:50,209 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:45:50,210 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:45:50,211 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:45:52,076 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:45:52,077 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:45:52,091 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:45:52,092 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1026, cost=$0.000158, time=1867ms
2026-01-26 16:45:52,093 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=325, 尝试次数=1
2026-01-26 16:45:52,093 - app.services.agent.tools.explore_tools - INFO - [ExploreState] 搜索词与已有词相似，跳过: '章节ID 4010049e-6d95-4abe-872d-1' ~ '章节ID 4010049e-6d95-4abe-872d-1'
2026-01-26 16:45:52,100 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, current_order=1, query=如何获取指定章节的原文...
2026-01-26 16:45:52,189 - app.services.chapter_vector_service - INFO - RAG retrieved 4 segments within order<=1
2026-01-26 16:45:52,711 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 4 个候选 -> top 5
2026-01-26 16:45:52,712 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到4个片段
2026-01-26 16:45:52,720 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第66段
2026-01-26 16:45:52,729 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第70段
2026-01-26 16:45:52,738 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第73段
2026-01-26 16:45:52,739 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:45:52,739 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:45:52,740 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:46:21,636 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:46:21,638 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:46:21,654 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:46:21,656 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3312, cost=$0.006082, time=28897ms
2026-01-26 16:46:21,657 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=455, 尝试次数=1
2026-01-26 16:46:21,658 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {},
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": false,
    "has_plot_details": true
  },
  "summary": "收集到的信息包含第一章的数个原文片段。内容描述了角色段融执行“读取器灵”的动作，并展示了该动作产生的“吞噬效果”，即获得了多种刀法技能。",
  "next_action": "根据任务目标中提供的章节ID '4010049e-6d95-4abe-872d-1eb0c0d756d5'，通过访问相应的数据源（如API或数据库），获取并整合第一章的全部文本内容来完成任务。",
  "potential_gaps": [
    "章节的完整原文内容"
  ]
}
```
2026-01-26 16:46:21,658 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=0/0, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:46:21,659 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=6, 章节=1, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 16:46:21,661 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则5: 边界情况 → 不足（保守策略）
2026-01-26 16:46:21,662 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 4轮, 原因=达到最大轮次（覆盖不足）
2026-01-26 16:46:21,676 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:46:21,685 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 13869f82-8947-4992-a6bc-8d6ea4de1b2d
2026-01-26 16:46:21,688 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:46:21,690 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节内容，为分析做准备 (136.9s)
2026-01-26 16:46:21,691 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:46:21,691 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 分析第一章的风格、结构和质量，诊断“流水账”问题的原因
2026-01-26 16:46:21,692 - app.api.v1.agent - INFO - [Stream] Task started: 分析第一章的风格、结构和质量，诊断“流水账”问题的原因 (icon=FileSearch)
2026-01-26 16:46:21,693 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-26 16:46:21,693 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 的 text 参数为空或含占位符，使用 context 兜底（1447字符）
2026-01-26 16:46:21,693 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析文章为何读起来像流水账，并提出改进方向...'
2026-01-26 16:46:21,693 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-26 16:46:21,696 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-26 16:46:21,705 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:46:21,705 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=quality_evaluation, complexity=simple, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro, reason=任务复杂度为 simple; 任务类型: quality_evaluation; 选择 Gemini 2.5 Flash Lite (质量评分: 7.0/10, 成本: $0.1/$0.4 per 1M tokens)
2026-01-26 16:46:21,706 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash-lite, max_tokens=2500, temp=0.3, task_type=TaskType.QUALITY_EVALUATION
2026-01-26 16:46:22,901 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:46:35,034 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 40 个数据块，总长度: 3449
2026-01-26 16:46:35,035 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 3639 (prompt=1354, completion=2285)
2026-01-26 16:46:35,036 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:46:35,037 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:46:35,068 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:46:35,069 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=3639, cost=$0.001049, time=13331ms
2026-01-26 16:46:35,070 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 13.374s)
2026-01-26 16:46:35,074 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-26 16:46:35,075 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-26 16:46:35,076 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析第一章的风格、结构和质量，诊断“流水账”问题的原因 (13.4s)
2026-01-26 16:46:35,077 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:46:35,079 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 150.26s
2026-01-26 16:46:35,080 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:46:35,082 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-26 16:46:35,083 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-26 16:46:35,083 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:46:35,084 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-26 16:46:35,085 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=5016字符, 处理后=5063字符
2026-01-26 16:46:35,086 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:46:35,086 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:46:35,087 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:46:35,088 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:46:35,089 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:46:35,101 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:46:35,102 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:46:35,102 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:46:38,540 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:46:38,542 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:46:38,543 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:46:45,919 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 24 个数据块，总长度: 2212
2026-01-26 16:46:45,920 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 9657 (prompt=8128, completion=1529)
2026-01-26 16:46:45,920 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:46:45,920 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:46:45,939 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:46:45,941 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=9657, cost=$0.006261, time=10817ms
2026-01-26 16:46:45,942 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=2212
2026-01-26 16:46:47,201 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:b0a47953-7246-42d6-bb24-eba29c2606ad | 重要度=0.77
2026-01-26 16:46:47,246 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b0a47953-7246-42d6-bb24-eba29c2606ad:d25295f3-b024-477c-9990-a00e67178f26, token=2498
2026-01-26 16:46:47,248 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b0a47953-7246-42d6-bb24-eba29c2606ad:d25295f3-b024-477c-9990-a00e67178f26, 消息数=2, 摘要长度=0, Token=2498
2026-01-26 16:46:47,249 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:b0a47953-7246-42d6-bb24-eba29c2606ad:d25295f3-b024-477c-9990-a00e67178f26)
2026-01-26 16:46:47,249 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:46:47,254 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:47:00,813 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26
INFO:     127.0.0.1:63918 - "GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26 HTTP/1.1" 200 OK
2026-01-26 16:49:05,777 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58465 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:49:05,808 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:58466 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:49:05,848 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 4010049e-6d95-4abe-872d-1eb0c0d756d5 内容更新，新段落数: 70
2026-01-26 16:49:05,877 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
2026-01-26 16:49:05,884 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:55088 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:49:05,888 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 16:49:05,890 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:55086 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58463 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 16:49:05,897 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:49:09,096 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:49:14,902 - app.api.v1.chapters - INFO - [GET chapters] work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:49:14,919 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:49:14,923 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:49:14,927 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:14,929 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations
2026-01-26 16:49:14,930 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters
INFO:     127.0.0.1:63967 - "GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
2026-01-26 16:49:14,933 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
INFO:     127.0.0.1:63970 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:63969 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters HTTP/1.1" 200 OK
2026-01-26 16:49:14,945 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:14,946 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, type=<class 'uuid.UUID'>
2026-01-26 16:49:14,948 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings
INFO:     127.0.0.1:63971 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings HTTP/1.1" 200 OK
2026-01-26 16:49:14,954 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:49:14,955 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:49:14,956 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:49:14,957 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:49:14,981 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:49:14,985 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=60s)
2026-01-26 16:49:14,994 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
INFO:     127.0.0.1:63968 - "GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
2026-01-26 16:49:15,012 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:49:15,014 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,017 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 16:49:15,022 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,023 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines
2026-01-26 16:49:15,024 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations
2026-01-26 16:49:15,027 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,028 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines
INFO:     127.0.0.1:60108 - "GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63108 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:60110 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64016 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:49:15,035 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters
INFO:     127.0.0.1:61368 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters HTTP/1.1" 200 OK
2026-01-26 16:49:15,046 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,053 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings
INFO:     127.0.0.1:60812 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings HTTP/1.1" 200 OK
2026-01-26 16:49:15,057 - app.api.v1.chapters - INFO - [GET chapters] work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:49:15,065 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,069 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,074 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines
2026-01-26 16:49:15,075 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,078 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
INFO:     127.0.0.1:55723 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:49399 - "GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
2026-01-26 16:49:15,082 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines
INFO:     127.0.0.1:55725 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:49:15,131 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:49:15,140 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:49:15,140 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:49:15,142 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58817 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:49:15,169 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:49:15,174 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:49:15,175 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:49:15,176 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63594 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:49:15,279 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status
INFO:     127.0.0.1:54065 - "GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status HTTP/1.1" 404 Not Found
2026-01-26 16:49:15,286 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions
INFO:     127.0.0.1:54066 - "GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:49:15,480 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions
INFO:     127.0.0.1:49519 - "GET /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:49:15,501 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status
INFO:     127.0.0.1:59834 - "GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status HTTP/1.1" 404 Not Found
2026-01-26 16:49:15,514 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:15,516 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
INFO:     127.0.0.1:54062 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:49:15,518 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:49:18,927 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:49:18,981 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:18,982 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662
INFO:     127.0.0.1:61637 - "PUT /api/v1/chapters/c02aff55-7819-4477-b7ff-27300884f662 HTTP/1.1" 200 OK
2026-01-26 16:49:18,984 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:49:20,411 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:49:24,122 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 16:49:24,130 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 16:49:24,132 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9e65d7f6-85c9-4bb4-a2f3-6ce886387672
2026-01-26 16:49:24,132 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:49:24,144 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62325 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:49:24,177 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 16:49:24,191 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 16:49:24,193 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9e65d7f6-85c9-4bb4-a2f3-6ce886387672
2026-01-26 16:49:24,194 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:49:24,197 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59648 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:49:24,298 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:49:24,300 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions
INFO:     127.0.0.1:59650 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:59652 - "GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:49:24,405 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions
INFO:     127.0.0.1:58311 - "GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:49:24,473 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:24,477 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb
INFO:     127.0.0.1:61164 - "PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb HTTP/1.1" 200 OK
2026-01-26 16:49:24,482 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:49:27,101 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
2026-01-26 16:49:27,103 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     127.0.0.1:60101 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:49:27,121 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:49:27,121 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:49:27,122 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:49:28,865 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:49:28,865 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 16:49:28,871 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62110 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 16:49:28,876 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cf119734-c397-4025-a3f8-0147da826cdb 内容更新，新段落数: 70
2026-01-26 16:49:28,881 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 段融吞噬器灵那段太平淡了，这可是金手指第一次发动，应该更有仪式感...
2026-01-26 16:49:28,889 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:28,893 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb
INFO:     127.0.0.1:54966 - "PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb HTTP/1.1" 200 OK
2026-01-26 16:49:28,894 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:49:28,901 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=9, 设定=7, 规范=无
2026-01-26 16:49:28,902 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:e8da7500-5304-4bca-98a1-9a53b49e4999 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, conversation_id=e8da7500-5304-4bca-98a1-9a53b49e4999)
2026-01-26 16:49:30,891 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:e8da7500-5304-4bca-98a1-9a53b49e4999
2026-01-26 16:49:30,892 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:e8da7500-5304-4bca-98a1-9a53b49e4999: 0/16000 tokens
2026-01-26 16:49:30,982 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='段融吞噬器灵那段太平淡了，这可是金手指第一次发动，应该更有仪...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-26 16:49:30,983 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 | 含用户级=True | 找到=0条
2026-01-26 16:49:30,994 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 2092.49ms
2026-01-26 16:49:30,994 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:49:30,995 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:49:30,996 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:49:31,053 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:49:31,140 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cf119734-c397-4025-a3f8-0147da826cdb 内容更新，新段落数: 70
2026-01-26 16:49:31,142 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 cf119734-c397-4025-a3f8-0147da826cdb 内容更新，新段落数: 70
2026-01-26 16:49:31,159 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:31,162 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb
INFO:     127.0.0.1:50222 - "PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb HTTP/1.1" 200 OK
2026-01-26 16:49:31,164 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:49:33,390 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 16:49:33,391 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb
INFO:     127.0.0.1:50220 - "PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb HTTP/1.1" 200 OK
2026-01-26 16:49:33,393 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:49:33,411 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:49:35,538 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:49:35,538 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:49:35,554 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:49:35,555 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=363, cost=$0.000042, time=4542ms
2026-01-26 16:49:35,557 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-26 16:49:35,558 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:49:35,559 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:49:35,559 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:49:35,572 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:49:36,346 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:49:36,347 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:49:36,365 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:49:36,367 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=302, cost=$0.000030, time=788ms
2026-01-26 16:49:36,368 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=8, 尝试次数=1
2026-01-26 16:49:36,368 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: analysis
2026-01-26 16:49:36,369 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: analysis (置信度: 0.90)
2026-01-26 16:49:36,369 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 段融吞噬器灵那段太平淡了，这可是金手指第一次发动，应该更有仪式感...
2026-01-26 16:49:36,375 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:49:36,380 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:49:36,381 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:49:36,381 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:49:55,378 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:50:02,450 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 15 个数据块，总长度: 2065
2026-01-26 16:50:02,451 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22354 (prompt=21459, completion=895)
2026-01-26 16:50:02,452 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:50:02,452 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:50:02,475 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:50:02,479 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22354, cost=$0.035774, time=26071ms
2026-01-26 16:50:02,479 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22354
2026-01-26 16:50:02,480 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望改写一个特定情节，使其更有冲击力。输出形式是创作内容, 原料=需要读取当前章节的原文，以定位并改写“段, 处理=这是一个典型的“改写”场景。首先，使用
2026-01-26 16:50:02,483 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-26 16:50:02,483 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 26.11s
2026-01-26 16:50:02,483 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-26 16:50:02,484 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:50:02,484 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:50:02,485 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:50:02,485 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-01-26 16:50:02,486 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 读取当前章节内容，为改写做准备。
2026-01-26 16:50:02,487 - app.api.v1.agent - INFO - [Stream] Task started: 读取当前章节内容，为改写做准备。 (icon=Wrench)
2026-01-26 16:50:02,487 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:50:02,488 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, target=读取当前章节的全部内容，用于定位和改写“段融吞噬器灵”的情节。...
2026-01-26 16:50:02,488 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段融', '吞噬', '器灵']
2026-01-26 16:50:02,489 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, target=读取当前章节的全部内容，用于定位和改写“段融吞噬器灵”的情节。...
2026-01-26 16:50:02,490 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:50:02,490 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用规划传入的关键词: ['段融', '吞噬', '器灵']
2026-01-26 16:50:02,528 - app.services.chapter_vector_service - INFO - [exact_search] work=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, keywords=['段融', '吞噬', '器灵']..., mode=any, range=None, hits=100
2026-01-26 16:50:02,530 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 100 条
2026-01-26 16:50:02,531 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 100 条
2026-01-26 16:50:02,531 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 100 条证据)
2026-01-26 16:50:02,532 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:50:02,532 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:50:02,533 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:50:18,015 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:50:18,017 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:50:18,032 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:50:18,034 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2727, cost=$0.005929, time=15483ms
2026-01-26 16:50:18,036 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=563, 尝试次数=1
2026-01-26 16:50:18,037 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true,
    "吞噬": true,
    "器灵": true
  },
  "chapters_with_evidence": [
    1,
    2,
    3,
    4
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "已收集的信息包含角色“段融”的外貌、身份和日常活动，以及他与角色“赵穆”的互动。信息还提及段融经历了一次能“内视”的特殊体验，但提供的证据片段中未展示“吞噬”和“器灵”的具体情节。",
  "next_action": "基于已收集的100条证据片段，将检索“段融”、“吞噬”和“器灵”三个关键词同时出现的段落，以精确定位核心情节。然后，根据定位到的原文内容进行改写。",
  "potential_gaps": [
 ...
2026-01-26 16:50:18,038 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=3/3, 章节=[1, 2, 3, 4], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:50:18,039 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=100, 章节=4, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 16:50:18,040 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 16:50:18,040 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 判断信息充足，跳过补充循环: 证据充足：100条证据，覆盖4个章节，关键词覆盖100%
2026-01-26 16:50:18,051 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,060 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 2 -> UUID 78a840b2-e622-4230-b649-345b5d91f9eb
2026-01-26 16:50:18,070 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 3 -> UUID e366c6f6-5e16-47d2-be9b-824b7a49a0ef
2026-01-26 16:50:18,075 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 4 -> UUID 9e65d7f6-85c9-4bb4-a2f3-6ce886387672
2026-01-26 16:50:18,082 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,088 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,094 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,099 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,106 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,111 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,116 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,123 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,128 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,134 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID c02aff55-7819-4477-b7ff-27300884f662
2026-01-26 16:50:18,136 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:50:18,137 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取当前章节内容，为改写做准备。 (15.7s)
2026-01-26 16:50:18,138 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:50:18,139 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户要求，重写段融吞噬器灵的情节，增加仪式感和冲击力。
2026-01-26 16:50:18,139 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，重写段融吞噬器灵的情节，增加仪式感和冲击力。 (icon=Edit3)
2026-01-26 16:50:18,140 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-26 16:50:18,140 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-26 16:50:18,149 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 未提供text_to_rewrite，自动获取章节内容: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 16:50:18,167 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 自动获取章节内容成功，长度: 4281
2026-01-26 16:50:18,168 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 4281, 用户要求: 请找出并重写'段融吞噬器灵'的相关段落。当前版本太平淡，需要增加金手指首次发动的仪式感和震撼感。请详细描写吞噬过程中的光影、能量变化、段融的感官和心理冲击，以及器灵的反应，使其成为一个令人印象深刻的关键情节。
2026-01-26 16:50:18,169 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-26 16:50:18,169 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:50:18,169 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:50:18,169 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-26 16:51:15,991 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:51:15,991 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:51:16,013 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:51:16,014 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10119, cost=$0.041078, time=57822ms
2026-01-26 16:51:16,014 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=4814, 尝试次数=1
2026-01-26 16:51:16,014 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 4814
2026-01-26 16:51:16,015 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-01-26 16:51:16,017 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 57.877s)
2026-01-26 16:51:16,019 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-26 16:51:16,020 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，重写段融吞噬器灵的情节，增加仪式感和冲击力。 (57.9s)
2026-01-26 16:51:16,021 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:51:16,021 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将新生成的、更具仪式感的情节替换回原文。
2026-01-26 16:51:16,022 - app.api.v1.agent - INFO - [Stream] Task started: 将新生成的、更具仪式感的情节替换回原文。 (icon=Check)
2026-01-26 16:51:16,023 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-01-26 16:51:16,024 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-01-26 16:51:16,028 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=replace, chapter=cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 16:51:16,029 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace, needs_locate=True
2026-01-26 16:51:16,032 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=cf119734-c397-4025-a3f8-0147da826cdb, query=<p data-id="qah0p5aw">段融在想：兵器架上的废刀的器灵不是二阶就是三阶，而赵穆用的那柄好刀的器灵却是不入阶的。</p><p data-id="loohh524">也就是说器灵等级，其实与器物本身的好坏，没有直接的关系。</p><p data-id="93fggwh1">“那决定器灵等阶的，到底是什么？”</p><p data-id="44ndy2nw">段融眉头紧锁，苦苦沉思着
2026-01-26 16:51:16,050 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 70 个段落
2026-01-26 16:51:16,050 - app.services.agent.tools.locate_tools - INFO - [locate_content] 模糊匹配结果: None
2026-01-26 16:51:16,050 - app.services.agent.tools.locate_tools - INFO - [locate_content] 无模糊匹配结果，尝试 LLM 辅助定位
2026-01-26 16:51:16,070 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] 开始调用 LLM，候选数量: 8
2026-01-26 16:51:16,070 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:51:16,071 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:51:16,072 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:51:18,104 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:51:18,105 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:51:18,123 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:51:18,125 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=446, cost=$0.000045, time=2034ms
2026-01-26 16:51:18,126 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-26 16:51:18,127 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] LLM 选择候选 1 → 原始第 1 段
2026-01-26 16:51:18,128 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位返回: (0, 0.85)
2026-01-26 16:51:18,128 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位成功: 第1段
2026-01-26 16:51:18,131 - app.services.agent.tools.operate_tools - INFO - [Operate] 定位完成: method=text_match, para=0
2026-01-26 16:51:18,136 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=cf119734-c397-4025-a3f8-0147da826cdb, operation=replace, content_len=4578
2026-01-26 16:51:18,175 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 2.151s)
2026-01-26 16:51:18,176 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-01-26 16:51:18,181 - app.services.agent.utils.tool_cache - INFO - [ToolCache] invalidated 1 keys: tool_cache:*:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:chapter:cf119734-c397-4025-a3f8-0147da826cdb:*
2026-01-26 16:51:18,190 - app.api.v1.agent - INFO - [Stream] 任务完成: 将新生成的、更具仪式感的情节替换回原文。 (2.2s)
2026-01-26 16:51:18,190 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-26 16:51:18,191 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 75.71s
2026-01-26 16:51:18,192 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:51:18,192 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:51:18,193 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-26 16:51:18,193 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:51:18,194 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:51:18,194 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=21410字符, 处理后=6264字符
2026-01-26 16:51:18,195 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:51:18,196 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:51:18,197 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:51:18,197 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:51:18,197 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:51:18,208 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:51:18,209 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:51:18,209 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:51:24,439 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:51:24,440 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:51:24,441 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:51:26,067 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 5 个数据块，总长度: 338
2026-01-26 16:51:26,067 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 10923 (prompt=10682, completion=241)
2026-01-26 16:51:26,068 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:51:26,068 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:51:26,078 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:51:26,079 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10923, cost=$0.003807, time=7858ms
2026-01-26 16:51:26,080 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=338
2026-01-26 16:51:27,035 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 | 重要度=0.60
2026-01-26 16:51:27,043 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:e8da7500-5304-4bca-98a1-9a53b49e4999, token=435
2026-01-26 16:51:27,044 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:e8da7500-5304-4bca-98a1-9a53b49e4999, 消息数=2, 摘要长度=0, Token=435
2026-01-26 16:51:27,045 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873:e8da7500-5304-4bca-98a1-9a53b49e4999)
2026-01-26 16:51:27,045 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:51:27,051 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:51:28,430 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999
INFO:     127.0.0.1:55720 - "GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999 HTTP/1.1" 200 OK
2026-01-26 16:55:04,806 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58728 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:55:04,826 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:58729 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:55:04,844 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:63463 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:55:04,859 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:49550 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:55:09,238 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:55:09,252 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,253 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 16:55:09,261 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:55:09,266 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:55:09,269 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:55:09,269 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:55:09,269 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:55:09,270 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:55:09,311 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 16:55:09,315 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 16:55:09,318 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:55:09,321 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,323 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
INFO:     127.0.0.1:60588 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 16:55:09,327 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 16:55:09,332 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,335 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:60591 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:60590 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60589 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:60592 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
2026-01-26 16:55:09,438 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:55:09,449 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:63270 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 16:55:09,460 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:55:09,474 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,477 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 16:55:09,481 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,486 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,489 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:60920 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 16:55:09,501 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,502 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
2026-01-26 16:55:09,504 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 16:55:09,505 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
INFO:     127.0.0.1:64915 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:65029 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:64911 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:64914 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
2026-01-26 16:55:09,562 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,567 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:63825 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
2026-01-26 16:55:09,579 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,582 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,585 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
2026-01-26 16:55:09,586 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:64569 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:55479 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 16:55:09,629 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:55:09,642 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:55:09,644 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:55:09,653 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60209 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:55:09,678 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:55:09,695 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:55:09,698 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 16:55:09,705 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59657 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:55:09,751 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions
2026-01-26 16:55:09,756 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:62259 - "GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:62260 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 16:55:09,932 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:55682 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 16:55:09,951 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions
INFO:     127.0.0.1:61724 - "GET /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:55:09,975 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:09,985 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0
INFO:     127.0.0.1:62258 - "PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0 HTTP/1.1" 200 OK
2026-01-26 16:55:09,992 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:55:13,490 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:55:13,490 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:55:13,502 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:55:13,505 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:55:13,512 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:55:13,513 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 16:55:13,513 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:55:13,521 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 16:55:13,521 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 16:55:13,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59097 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 16:55:13,576 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 16:55:13,589 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:64902 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:59098 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:55:13,613 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:59099 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:55:13,646 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:13,664 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0
INFO:     127.0.0.1:64147 - "PUT /api/v1/chapters/27a17757-3987-4117-84da-f9c74f3ab0d0 HTTP/1.1" 200 OK
2026-01-26 16:55:13,669 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 16:55:13,678 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:64325 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 16:55:15,848 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:15,850 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:57075 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 16:55:15,851 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:55:18,443 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 16:55:18,464 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:55:18,566 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53858 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 16:55:18,637 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6903be9b-2bc2-42d0-8b08-75d679ee3591 内容更新，新段落数: 70
2026-01-26 16:55:18,641 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6903be9b-2bc2-42d0-8b08-75d679ee3591 内容更新，新段落数: 70
2026-01-26 16:55:18,644 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 16:55:18,645 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 16:55:18,645 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 16:55:20,307 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 16:55:20,308 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 16:55:20,317 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:20,319 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6903be9b-2bc2-42d0-8b08-75d679ee3591 内容更新，新段落数: 70
2026-01-26 16:55:20,323 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
2026-01-26 16:55:20,325 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:55:20,327 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:54542 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
INFO:     127.0.0.1:57575 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 16:55:20,330 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:55:20,332 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:57573 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 16:55:20,335 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:55:22,345 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 第2章赵穆出场到离开这段，情绪起伏太弱，帮我加强一下压迫感和段融的隐忍...
2026-01-26 16:55:22,352 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:55:22,355 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:57574 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 16:55:22,361 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 16:55:24,492 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:55:24,495 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=5, 规范=无
2026-01-26 16:55:24,496 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b1456da2-6a55-49e8-ad42-2332dc579363:a7f7bd35-cd62-4ce0-821b-239b342cb363 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=b1456da2-6a55-49e8-ad42-2332dc579363, conversation_id=a7f7bd35-cd62-4ce0-821b-239b342cb363)
2026-01-26 16:55:24,498 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b1456da2-6a55-49e8-ad42-2332dc579363:a7f7bd35-cd62-4ce0-821b-239b342cb363
2026-01-26 16:55:24,498 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b1456da2-6a55-49e8-ad42-2332dc579363:a7f7bd35-cd62-4ce0-821b-239b342cb363: 0/16000 tokens
2026-01-26 16:55:24,593 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='第2章赵穆出场到离开这段，情绪起伏太弱，帮我加强一下压迫感和...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:b1456da2-6a55-49e8-ad42-2332dc579363', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-26 16:55:24,593 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=b1456da2-6a55-49e8-ad42-2332dc579363 | 含用户级=True | 找到=0条
2026-01-26 16:55:24,601 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 104.94ms
2026-01-26 16:55:24,601 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:55:24,602 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:55:24,602 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:55:26,863 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:55:26,903 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 16:55:28,987 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:55:28,988 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:55:29,001 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:55:29,004 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=374, cost=$0.000043, time=4387ms
2026-01-26 16:55:29,004 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=42, 尝试次数=1
2026-01-26 16:55:29,005 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:55:29,005 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:55:29,006 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 16:55:29,669 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:55:29,670 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:55:29,690 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:55:29,692 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=311, cost=$0.000031, time=665ms
2026-01-26 16:55:29,693 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 16:55:29,693 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 16:55:29,694 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 16:55:29,694 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 第2章赵穆出场到离开这段，情绪起伏太弱，帮我加强一下压迫感和段融的隐忍...
2026-01-26 16:55:29,702 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 16:55:29,711 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:55:29,712 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 16:55:29,713 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 16:55:40,176 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/auth/refresh
INFO:     127.0.0.1:63639 - "POST /api/v1/auth/refresh HTTP/1.1" 200 OK
2026-01-26 16:55:53,468 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:56:00,543 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 16 个数据块，总长度: 2027
2026-01-26 16:56:00,543 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22904 (prompt=21963, completion=941)
2026-01-26 16:56:00,546 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:56:00,546 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:56:00,561 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:56:00,562 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22904, cost=$0.036864, time=30832ms
2026-01-26 16:56:00,563 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22904
2026-01-26 16:56:00,563 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望改写第二章中的一个特定场景（赵穆出场到离开），目标是, 原料=需要读取第二章的完整内容，以理解该场景的, 处理=这是一个创作改写任务，应遵循“读取-创作
2026-01-26 16:56:00,563 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-26 16:56:00,563 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 30.87s
2026-01-26 16:56:00,563 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-26 16:56:00,563 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 16:56:00,563 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 16:56:00,563 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 16:56:00,563 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-01-26 16:56:00,563 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 读取第2章的原文内容，为改写做准备。
2026-01-26 16:56:00,566 - app.api.v1.agent - INFO - [Stream] Task started: 读取第2章的原文内容，为改写做准备。 (icon=Wrench)
2026-01-26 16:56:00,566 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 16:56:00,566 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=b1456da2-6a55-49e8-ad42-2332dc579363, target=读取当前章节（ID: 6903be9b-2bc2-42d0-8b08-75d679ee3591）的全...
2026-01-26 16:56:00,566 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['赵穆', '段融']
2026-01-26 16:56:00,567 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第0-75章
2026-01-26 16:56:00,567 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=b1456da2-6a55-49e8-ad42-2332dc579363, target=读取当前章节（ID: 6903be9b-2bc2-42d0-8b08-75d679ee3591）的全...
2026-01-26 16:56:00,567 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 16:56:00,567 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用规划传入的关键词: ['赵穆', '段融']
2026-01-26 16:56:00,567 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围: (0, 75)
2026-01-26 16:56:00,586 - app.services.chapter_vector_service - INFO - [exact_search] work=b1456da2-6a55-49e8-ad42-2332dc579363, keywords=['赵穆', '段融']..., mode=any, range=(0, 75), hits=100
2026-01-26 16:56:00,588 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 100 条
2026-01-26 16:56:00,588 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 100 条
2026-01-26 16:56:00,588 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 100 条证据)
2026-01-26 16:56:00,589 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:56:00,589 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:56:00,589 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:56:16,731 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:56:16,732 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:56:16,741 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:56:16,741 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2832, cost=$0.005622, time=16143ms
2026-01-26 16:56:16,741 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=465, 尝试次数=1
2026-01-26 16:56:16,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "赵穆": true,
    "段融": true
  },
  "chapters_with_evidence": [
    1,
    2,
    3,
    4
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "已收集到关于角色赵穆和段融在第1至4章的证据片段。内容包含赵穆向杂役弟子演练刀法的情节，以及段融的外貌、日常活动和在梦中领悟内息流转的细节。",
  "next_action": "基于已收集的第2章证据片段，如赵穆将兵刃交给段融、向众人演练“羚羊献食”刀法等情节，进行场景改写。",
  "potential_gaps": [
    "第2章的完整原文内容"
  ]
}
```
2026-01-26 16:56:16,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=2/2, 章节=[1, 2, 3, 4], 质量=[引用=False,互动=False,情节=False]
2026-01-26 16:56:16,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=100, 章节=4, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 16:56:16,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节覆盖不足: missing=[0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]
2026-01-26 16:56:16,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 评估不足，缺失项: ['缺少第0章的证据片段', '缺少第5章的证据片段', '缺少第6章的证据片段', '缺少第7章的证据片段', '缺少第8章的证据片段']
2026-01-26 16:56:16,743 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段3：AI 补充循环，当前 100 条证据
2026-01-26 16:56:16,743 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:56:16,743 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:56:16,743 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.3, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:56:32,153 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:56:32,154 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:56:32,166 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:56:32,166 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1834, cost=$0.004795, time=15411ms
2026-01-26 16:56:32,166 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=493, 尝试次数=1
2026-01-26 16:56:32,168 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 任务理解完成: 需要全面解析指定章节（第2章）的文本内容，以提取重构场景所需的全部叙事要素。...
2026-01-26 16:56:32,168 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 16:56:32,168 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 16:56:32,168 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 16:56:33,570 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:56:33,570 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 16:56:33,573 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:56:33,573 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1387, cost=$0.000195, time=1401ms
2026-01-26 16:56:33,573 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=330, 尝试次数=1
2026-01-26 16:56:33,583 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 16:56:33,584 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 16:56:33,584 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 16:56:33,584 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 16:56:33,584 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 16:56:33,604 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第0-75章 -> 第1-5章
2026-01-26 16:56:33,604 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:56:33,616 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-26 16:56:33,625 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b1456da2-6a55-49e8-ad42-2332dc579363, current_order=5, query=第2章中赵穆和段融的互动细节...
2026-01-26 16:56:33,681 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-26 16:56:38,011 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 14 个候选 -> top 5
2026-01-26 16:56:38,011 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:56:38,024 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第10段
2026-01-26 16:56:38,032 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第2章第0段
2026-01-26 16:56:38,039 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第4章第0段
2026-01-26 16:56:38,047 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b1456da2-6a55-49e8-ad42-2332dc579363, current_order=5, query=第2章中描述的训练场景和教学内容...
2026-01-26 16:56:38,183 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-26 16:56:38,844 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 9 个候选 -> top 5
2026-01-26 16:56:38,845 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:56:38,852 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=b1456da2-6a55-49e8-ad42-2332dc579363, current_order=5, query=第2章中揭示的杂役弟子的生活状态...
2026-01-26 16:56:38,969 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-26 16:56:45,834 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 14 个候选 -> top 5
2026-01-26 16:56:45,834 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 16:56:45,839 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:56:45,839 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:56:45,839 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 16:57:27,337 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:57:27,338 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:57:27,338 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:57:27,338 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=5741, cost=$0.009259, time=41499ms
2026-01-26 16:57:27,348 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=474, 尝试次数=1
2026-01-26 16:57:27,348 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "赵穆": true,
    "段融": true
  },
  "chapters_with_evidence": [
    1,
    2,
    3,
    4,
    5
  ],
  "has_direct_quotes": true,
  "has_character_interactions": true,
  "has_plot_details": true,
  "summary": "已收集信息包含角色赵穆与段融的互动片段，涉及武艺教导、兵刃擦拭等情节。同时，证据片段也涵盖了段融的特殊能力、对器灵的思考以及准备考核等内容。",
  "next_action": "基于已收集的第2章证据片段，提取人物关系、主要情节、场景环境、关键对话、角色动机和背景设定，以构建用于场景改写的完整叙事要素框架。",
  "potential_gaps": [
    "由于证据以片段形式存在，缺乏章节内事件的完整连续性与上下文"
  ]
}
```
2026-01-26 16:57:27,348 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=2/2, 章节=[1, 2, 3, 4, 5], 质量=[引用=True,互动=True,情节=True]
2026-01-26 16:57:27,348 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=115, 章节=5, 关键词覆盖=100.0%, 质量=3/3
2026-01-26 16:57:27,348 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 16:57:27,348 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 2轮, 原因=AI 判断信息充足: 证据充足：115条证据，覆盖5个章节，关键词覆盖100%
2026-01-26 16:57:27,356 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,359 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,359 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,371 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,373 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,378 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,382 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,386 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,387 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,390 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 27a17757-3987-4117-84da-f9c74f3ab0d0
2026-01-26 16:57:27,390 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 16:57:27,390 - app.api.v1.agent - INFO - [Stream] 任务完成: 读取第2章的原文内容，为改写做准备。 (86.8s)
2026-01-26 16:57:27,390 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 16:57:27,390 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户要求，加强赵穆出场的压迫感和段融的隐忍。
2026-01-26 16:57:27,390 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户要求，加强赵穆出场的压迫感和段融的隐忍。 (icon=Edit3)
2026-01-26 16:57:27,390 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-26 16:57:27,390 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-26 16:57:27,401 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 未提供text_to_rewrite，自动获取章节内容: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:57:27,403 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 自动获取章节内容成功，长度: 4281
2026-01-26 16:57:27,404 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 4281, 用户要求: 请聚焦在【赵穆出场到离开】的片段进行重点改写。你需要极大地加强赵穆身为上位者的压迫感，通过他的言行、神态、以及周围环境的烘托来塑造。同时，要更深刻地刻画段融在面对这种压力时的隐忍，增加他的内心挣扎、细节动作和微表情，体现他表面顺从之下的暗流涌动。章节其余部分保持原意，自然衔接即可。
2026-01-26 16:57:27,405 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-26 16:57:27,405 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 16:57:27,405 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 16:57:27,405 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-26 16:58:20,493 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:58:20,493 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 16:58:20,504 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:58:20,505 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8500, cost=$0.031266, time=53088ms
2026-01-26 16:58:20,506 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=3419, 尝试次数=1
2026-01-26 16:58:20,506 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 3419
2026-01-26 16:58:20,506 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-01-26 16:58:20,506 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 53.116s)
2026-01-26 16:58:20,506 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-26 16:58:20,506 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户要求，加强赵穆出场的压迫感和段融的隐忍。 (53.1s)
2026-01-26 16:58:20,506 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 16:58:20,506 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将重写后的整个章节内容应用到编辑器，替换原有内容。
2026-01-26 16:58:20,506 - app.api.v1.agent - INFO - [Stream] Task started: 将重写后的整个章节内容应用到编辑器，替换原有内容。 (icon=Check)
2026-01-26 16:58:20,506 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-01-26 16:58:20,506 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-01-26 16:58:20,511 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=content, chapter=6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 16:58:20,511 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace_all, needs_locate=False
2026-01-26 16:58:20,512 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=6903be9b-2bc2-42d0-8b08-75d679ee3591, operation=replace_all, content_len=3228
2026-01-26 16:58:20,536 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 0.030s)
2026-01-26 16:58:20,536 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-01-26 16:58:20,551 - app.api.v1.agent - INFO - [Stream] 任务完成: 将重写后的整个章节内容应用到编辑器，替换原有内容。 (0.0s)
2026-01-26 16:58:20,551 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-26 16:58:20,552 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 139.99s
2026-01-26 16:58:20,552 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 16:58:20,552 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:58:20,552 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-26 16:58:20,553 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 16:58:20,554 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 16:58:20,554 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=15850字符, 处理后=9960字符
2026-01-26 16:58:20,554 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 16:58:20,554 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 16:58:20,554 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 16:58:20,554 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 16:58:20,554 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 16:58:20,560 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 16:58:20,560 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 16:58:20,561 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 16:58:35,933 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 16:58:35,933 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 16:58:35,933 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 16:58:37,068 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 272
2026-01-26 16:58:37,068 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 15880 (prompt=15689, completion=191)
2026-01-26 16:58:37,068 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 16:58:37,068 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 16:58:37,068 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 16:58:37,078 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=15880, cost=$0.005184, time=16507ms
2026-01-26 16:58:37,078 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=272
2026-01-26 16:58:37,370 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:b1456da2-6a55-49e8-ad42-2332dc579363 | 重要度=0.94
2026-01-26 16:58:37,375 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b1456da2-6a55-49e8-ad42-2332dc579363:a7f7bd35-cd62-4ce0-821b-239b342cb363, token=324
2026-01-26 16:58:37,376 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:b1456da2-6a55-49e8-ad42-2332dc579363:a7f7bd35-cd62-4ce0-821b-239b342cb363, 消息数=2, 摘要长度=0, Token=324
2026-01-26 16:58:37,376 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:b1456da2-6a55-49e8-ad42-2332dc579363:a7f7bd35-cd62-4ce0-821b-239b342cb363)
2026-01-26 16:58:37,376 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 16:58:37,380 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 16:58:41,249 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:54281 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 16:59:58,300 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:58563 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:59:58,455 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:64476 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 16:59:58,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58562 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:59:58,535 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 6903be9b-2bc2-42d0-8b08-75d679ee3591 内容更新，新段落数: 70
2026-01-26 16:59:58,546 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:56661 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 16:59:58,557 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 16:59:58,559 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:58560 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 16:59:58,560 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:00:01,796 - app.api.v1.chapters - INFO - [GET chapters] work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:00:01,808 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:00:01,815 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:01,816 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, type=<class 'uuid.UUID'>
2026-01-26 17:00:01,819 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 17:00:01,823 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:00:01,824 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:00:01,825 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:00:01,825 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:00:01,859 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:00:01,862 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=60s)
2026-01-26 17:00:01,864 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:01,866 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters
INFO:     127.0.0.1:61272 - "GET /api/v1/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba HTTP/1.1" 200 OK
2026-01-26 17:00:01,868 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/84892aef-e8dc-49a8-8e1e-3d863045b9ba
INFO:     127.0.0.1:61273 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:61275 - "GET /api/v1/chapters/work/84892aef-e8dc-49a8-8e1e-3d863045b9ba HTTP/1.1" 200 OK
2026-01-26 17:00:01,912 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 17:00:01,917 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 17:00:01,927 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations
2026-01-26 17:00:01,928 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings
INFO:     127.0.0.1:61276 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61277 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings HTTP/1.1" 200 OK
2026-01-26 17:00:01,959 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:01,965 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 17:00:01,969 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba (expire=300s)
2026-01-26 17:00:01,970 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:01,972 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters
INFO:     127.0.0.1:63454 - "GET /api/v1/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba HTTP/1.1" 200 OK
2026-01-26 17:00:01,975 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines
2026-01-26 17:00:01,977 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines
INFO:     127.0.0.1:63456 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/characters HTTP/1.1" 200 OK
2026-01-26 17:00:01,981 - app.api.v1.chapters - INFO - [GET chapters] work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     127.0.0.1:63453 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61697 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines HTTP/1.1" 200 OK
2026-01-26 17:00:01,998 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:02,005 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:02,014 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations
2026-01-26 17:00:02,015 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/84892aef-e8dc-49a8-8e1e-3d863045b9ba
INFO:     127.0.0.1:56921 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:53334 - "GET /api/v1/chapters/work/84892aef-e8dc-49a8-8e1e-3d863045b9ba HTTP/1.1" 200 OK
2026-01-26 17:00:02,037 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:02,041 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:02,045 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:02,047 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines
2026-01-26 17:00:02,048 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings
2026-01-26 17:00:02,050 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines
INFO:     127.0.0.1:62684 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:61584 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:51529 - "GET /api/v1/worldview/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:00:02,112 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:00:02,122 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:00:02,122 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:00:02,124 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61035 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:00:02,145 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:00:02,151 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:00:02,152 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:00:02,154 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63376 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:00:02,213 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status
INFO:     127.0.0.1:51921 - "GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status HTTP/1.1" 404 Not Found
2026-01-26 17:00:02,222 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:51922 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:00:02,398 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:02,401 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:51919 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 17:00:02,402 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:00:02,403 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:64287 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:00:02,424 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status
INFO:     127.0.0.1:64042 - "GET /api/v1/analysis/works/84892aef-e8dc-49a8-8e1e-3d863045b9ba/status HTTP/1.1" 404 Not Found
2026-01-26 17:00:06,229 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:00:06,239 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:00:06,245 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions
2026-01-26 17:00:06,246 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:00:06,252 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
INFO:     127.0.0.1:63494 - "GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:00:06,256 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f54cc63f-7eb2-4eb3-9949-a4541dd4efec
2026-01-26 17:00:06,256 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:00:06,273 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:00:06,278 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 17:00:06,279 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f54cc63f-7eb2-4eb3-9949-a4541dd4efec
2026-01-26 17:00:06,280 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:63492 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:00:06,363 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63768 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:00:06,373 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:63493 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 17:00:06,403 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions
INFO:     127.0.0.1:58589 - "GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:00:06,418 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:06,420 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:65063 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 17:00:06,422 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:00:08,824 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:08,825 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0
INFO:     127.0.0.1:61391 - "PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0 HTTP/1.1" 200 OK
2026-01-26 17:00:08,826 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:00:11,034 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:00:11,067 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:00:11,134 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 9becc1b4-4bc4-4ac1-992f-035440e66ec0 内容更新，新段落数: 70
2026-01-26 17:00:11,141 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 9becc1b4-4bc4-4ac1-992f-035440e66ec0 内容更新，新段落数: 70
2026-01-26 17:00:11,150 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:11,152 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:11,154 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:00:11,155 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:00:11,156 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 9becc1b4-4bc4-4ac1-992f-035440e66ec0 内容更新，新段落数: 70
INFO:     127.0.0.1:55986 - "PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0 HTTP/1.1" 200 OK
2026-01-26 17:00:11,158 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
INFO:     127.0.0.1:55987 - "PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0 HTTP/1.1" 200 OK
2026-01-26 17:00:11,159 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:00:13,039 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:00:13,041 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0
INFO:     127.0.0.1:55988 - "PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0 HTTP/1.1" 200 OK
2026-01-26 17:00:13,042 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:00:13,050 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:00:16,846 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:00:16,863 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:03:38,519 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:03:38,525 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:03:38,525 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:03:38,528 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61518 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:03:38,557 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:03:38,562 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:03:38,562 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:03:38,564 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50064 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:03:38,572 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:50065 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:03:38,595 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:58364 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:03:38,902 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:03:38,905 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:58366 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 17:03:38,913 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:03:41,194 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:03:41,196 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:03:41,203 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:03:41,228 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:03:41,229 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:03:41,234 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f54cc63f-7eb2-4eb3-9949-a4541dd4efec
2026-01-26 17:03:41,234 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:03:41,235 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: f54cc63f-7eb2-4eb3-9949-a4541dd4efec
2026-01-26 17:03:41,235 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:03:41,238 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions
INFO:     127.0.0.1:63043 - "GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:03:41,245 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 17:03:41,246 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58597 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:63042 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:03:41,328 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions
INFO:     127.0.0.1:51339 - "GET /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:03:41,359 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:03:41,364 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:59547 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 17:03:41,370 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:03:41,375 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:03:41,378 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0
INFO:     127.0.0.1:52024 - "PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0 HTTP/1.1" 200 OK
2026-01-26 17:03:41,380 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:03:45,336 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:03:45,347 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:03:45,422 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:58574 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 17:03:45,440 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 17:03:45,440 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 17:03:45,440 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 17:03:47,023 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 17:03:47,024 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 17:03:47,032 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:03:47,033 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:51839 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 17:03:47,037 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0
INFO:     127.0.0.1:56560 - "PUT /api/v1/chapters/9becc1b4-4bc4-4ac1-992f-035440e66ec0 HTTP/1.1" 200 OK
2026-01-26 17:03:47,042 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:03:49,200 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 段融半夜练刀那段写得太实了，缺乏留白和想象空间，帮我改得更有意境...
2026-01-26 17:03:49,217 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=7, 规范=无
2026-01-26 17:03:49,218 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:84892aef-e8dc-49a8-8e1e-3d863045b9ba:1d696d9e-af73-44ac-af7b-8ee23f5df7f7 (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, conversation_id=1d696d9e-af73-44ac-af7b-8ee23f5df7f7)
2026-01-26 17:03:49,220 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:84892aef-e8dc-49a8-8e1e-3d863045b9ba:1d696d9e-af73-44ac-af7b-8ee23f5df7f7
2026-01-26 17:03:49,220 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:84892aef-e8dc-49a8-8e1e-3d863045b9ba:1d696d9e-af73-44ac-af7b-8ee23f5df7f7: 0/16000 tokens
2026-01-26 17:03:49,492 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='段融半夜练刀那段写得太实了，缺乏留白和想象空间，帮我改得更有...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-26 17:03:49,493 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba | 含用户级=True | 找到=0条
2026-01-26 17:03:49,506 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 287.35ms
2026-01-26 17:03:49,506 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:03:49,507 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:03:49,508 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 17:03:49,518 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:03:51,499 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:03:51,499 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:03:51,516 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:03:51,517 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=368, cost=$0.000042, time=1992ms
2026-01-26 17:03:51,518 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-26 17:03:51,518 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:03:51,518 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:03:51,519 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 17:03:52,845 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:03:52,847 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:03:52,871 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:03:52,873 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=309, cost=$0.000031, time=1329ms
2026-01-26 17:03:52,874 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 17:03:52,874 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 17:03:52,874 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 17:03:52,875 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 段融半夜练刀那段写得太实了，缺乏留白和想象空间，帮我改得更有意境...
2026-01-26 17:03:52,877 - app.core.cache - INFO - ⚠️ 缓存未命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 17:03:52,884 - app.core.cache - INFO - 💾 缓存已保存: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0 (expire=3600s)
2026-01-26 17:03:52,888 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:03:52,889 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 17:03:52,890 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 17:04:09,358 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 17:04:15,576 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 14 个数据块，总长度: 1864
2026-01-26 17:04:15,576 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 22153 (prompt=21325, completion=828)
2026-01-26 17:04:15,577 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:04:15,577 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:04:15,590 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:04:15,591 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=22153, cost=$0.034936, time=22688ms
2026-01-26 17:04:15,592 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=22153
2026-01-26 17:04:15,592 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望改写特定段落，使其更有意境，并更新到原文中。, 原料=需要读取当前章节内容，并定位到“段融半夜, 处理=首先使用 explore_content
2026-01-26 17:04:15,593 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共3个任务
2026-01-26 17:04:15,593 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共3个任务，耗时: 22.72s
2026-01-26 17:04:15,594 - app.api.v1.agent - INFO - [Stream] Plan tasks: 3 items
2026-01-26 17:04:15,594 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 17:04:15,595 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 17:04:15,595 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 17:04:15,596 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=3, 有依赖任务=2
2026-01-26 17:04:15,596 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 在当前章节中，查找并提取关于“段融半夜练刀”的段落内容。
2026-01-26 17:04:15,597 - app.api.v1.agent - INFO - [Stream] Task started: 在当前章节中，查找并提取关于“段融半夜练刀”的段落内容。 (icon=Wrench)
2026-01-26 17:04:15,597 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 17:04:15,597 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, target=在当前章节中，找到关于'段融半夜练刀'的段落...
2026-01-26 17:04:15,598 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段融', '练刀', '半夜', '刀光']
2026-01-26 17:04:15,598 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, target=在当前章节中，找到关于'段融半夜练刀'的段落...
2026-01-26 17:04:15,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 17:04:15,599 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用规划传入的关键词: ['段融', '练刀', '半夜', '刀光']
2026-01-26 17:04:15,633 - app.services.chapter_vector_service - INFO - [exact_search] work=84892aef-e8dc-49a8-8e1e-3d863045b9ba, keywords=['段融', '练刀', '半夜']..., mode=any, range=None, hits=100
2026-01-26 17:04:15,635 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 100 条
2026-01-26 17:04:15,636 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 100 条
2026-01-26 17:04:15,637 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 100 条证据)
2026-01-26 17:04:15,637 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:04:15,638 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 17:04:15,638 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 17:04:35,674 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:04:35,674 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:04:35,694 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:04:35,695 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2438, cost=$0.005769, time=20037ms
2026-01-26 17:04:35,696 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=585, 尝试次数=1
2026-01-26 17:04:35,696 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true,
    "练刀": true,
    "半夜": false,
    "刀光": false
  },
  "chapters_with_evidence": [
    1,
    2,
    3,
    4
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "已收集的信息包含角色段融的体貌特征、与角色赵穆的互动。第3章描述了段融在夜里处于梦境中，“看见”一个壮硕人影背对他练刀，并能“看见”其内息流转。",
  "next_action": "基于第3章的证据片段，如[第0段]“段融这一夜，仿佛一直处在梦境中…”和[第1段]“他‘看见’一个人影…背对着他在练刀”，可以定位到第3章为目标段落所在章节，并提取相关段落作为答案。",
  "po...
2026-01-26 17:04:35,696 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=2/4, 章节=[1, 2, 3, 4], 质量=[引用=False,互动=False,情节=False]
2026-01-26 17:04:35,696 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=100, 章节=4, 关键词覆盖=50.0%, 质量=0/3
2026-01-26 17:04:35,697 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 17:04:35,698 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 判断信息充足，跳过补充循环: 证据充足：100条证据，覆盖4个章节，关键词覆盖50%
2026-01-26 17:04:35,708 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,714 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 2 -> UUID 2418c164-8a87-4e39-9b8f-319cdea6b5b1
2026-01-26 17:04:35,720 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 3 -> UUID 9698b76a-1119-4be2-b491-5439b57ba277
2026-01-26 17:04:35,726 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 4 -> UUID f54cc63f-7eb2-4eb3-9949-a4541dd4efec
2026-01-26 17:04:35,731 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,736 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,741 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,749 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,755 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,761 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,768 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,776 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,781 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,787 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:04:35,791 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 17:04:35,791 - app.api.v1.agent - INFO - [Stream] 任务完成: 在当前章节中，查找并提取关于“段融半夜练刀”的段落内容。 (20.2s)
2026-01-26 17:04:35,791 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 17:04:35,793 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 根据用户“更有意境，增加留白和想象空间”的要求，对找到的段落进行改写。
2026-01-26 17:04:35,793 - app.api.v1.agent - INFO - [Stream] Task started: 根据用户“更有意境，增加留白和想象空间”的要求，对找到的段落进行改写。 (icon=Edit3)
2026-01-26 17:04:35,793 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: smart_rewrite
2026-01-26 17:04:35,794 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 开始执行工具
2026-01-26 17:04:35,802 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 开始生成改写结果，原文长度: 4791, 用户要求: 用户要求改写得更有意境，增加留白和想象空间，不要写得太实，侧重于氛围和心境的描写。
2026-01-26 17:04:35,803 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 使用传统单Prompt架构
2026-01-26 17:04:35,804 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:04:35,804 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=content_creation, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 17:04:35,804 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=4000, temp=0.8, 尝试=1/3, task_type=TaskType.CONTENT_CREATION
2026-01-26 17:05:15,178 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:05:15,178 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:05:15,194 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:05:15,195 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=7984, cost=$0.019903, time=39374ms
2026-01-26 17:05:15,195 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1353, 尝试次数=1
2026-01-26 17:05:15,196 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] AI返回长度: 1353
2026-01-26 17:05:15,197 - app.services.agent.tools.editor_tools - INFO - [smart_rewrite] 成功生成1条改写结果
2026-01-26 17:05:15,198 - app.services.agent.tools.tool_types - INFO - [smart_rewrite] 执行成功 (耗时: 39.404s)
2026-01-26 17:05:15,199 - app.services.agent.execution.tool_executor - INFO - [StandardTool] smart_rewrite 执行成功
2026-01-26 17:05:15,201 - app.api.v1.agent - INFO - [Stream] 任务完成: 根据用户“更有意境，增加留白和想象空间”的要求，对找到的段落进行改写。 (39.4s)
2026-01-26 17:05:15,201 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 17:05:15,202 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3开始: 将AI生成的更有意境的段落替换掉原文中的旧段落。
2026-01-26 17:05:15,202 - app.api.v1.agent - INFO - [Stream] Task started: 将AI生成的更有意境的段落替换掉原文中的旧段落。 (icon=Check)
2026-01-26 17:05:15,202 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: operate_apply
2026-01-26 17:05:15,202 - app.services.agent.tools.tool_types - INFO - [operate_apply] 开始执行工具
2026-01-26 17:05:15,205 - app.services.agent.tools.operate_tools - INFO - [Operate] 开始: op=replace, chapter=9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:05:15,205 - app.services.agent.tools.operate_tools - INFO - [Operate] 路由: tool=apply_chapter_edit, target_op=replace, needs_locate=True
2026-01-26 17:05:15,209 - app.services.agent.tools.locate_tools - INFO - [locate_content] 开始定位: chapter_id=9becc1b4-4bc4-4ac1-992f-035440e66ec0, query=## 相关片段 - [1章20段] 就在这时，段融抹了把额头的细汗，从角门跑进了这片院子。 - [1章22段] 段融穿了一身褐色短打，身体略显单薄，但这都是长期吃不饱肚子，给饿得。 - [1章24段] 段融扫了一眼院子里的人数，大约只有十多个人了。 - [1章26段] 段融叹了口气，不过他其实能够理解走了的那些人的想法，这些杂役弟子每天都要辛苦劳作，傍晚还要到此处练功，要是有奔头，还能咬牙坚持下
2026-01-26 17:05:15,249 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节共 70 个段落
2026-01-26 17:05:15,249 - app.services.agent.tools.locate_tools - INFO - [locate_content] 模糊匹配结果: None
2026-01-26 17:05:15,249 - app.services.agent.tools.locate_tools - INFO - [locate_content] 无模糊匹配结果，尝试 LLM 辅助定位
2026-01-26 17:05:15,263 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] 开始调用 LLM，候选数量: 8
2026-01-26 17:05:15,264 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:05:15,264 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:05:15,264 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 17:05:16,713 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:05:16,714 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:05:16,734 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:05:16,736 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=534, cost=$0.000054, time=1449ms
2026-01-26 17:05:16,737 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-26 17:05:16,737 - app.services.agent.tools.locate_tools - INFO - [_llm_assisted_locate] LLM 选择候选 1 → 原始第 12 段
2026-01-26 17:05:16,738 - app.services.agent.tools.locate_tools - INFO - [locate_content] LLM 辅助定位返回: (11, 0.85)
2026-01-26 17:05:16,739 - app.services.agent.tools.locate_tools - WARNING - [locate_content] LLM 辅助定位候选缺乏关键词匹配，忽略: 第12段
2026-01-26 17:05:16,739 - app.services.agent.tools.locate_tools - INFO - [locate_content] 章节内未找到，尝试全局搜索: work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:05:16,740 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=84892aef-e8dc-49a8-8e1e-3d863045b9ba, current_order=1000000, query=## 相关片段 - [1章20段] 就在这时，段融抹了把额头的细汗，从角门跑进了这片院子。 - [1...
2026-01-26 17:05:17,033 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=2000000
2026-01-26 17:05:36,236 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 15 个候选 -> top 5
2026-01-26 17:05:36,237 - app.services.agent.tools.locate_tools - INFO - [_llm_rerank] top-2 相似度接近 (1.00 vs 1.00)，调用 LLM 重排序
2026-01-26 17:05:36,239 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:05:36,241 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:05:36,242 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=10, temp=0.1, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 17:05:37,570 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:05:37,570 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:05:37,585 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:05:37,587 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=384, cost=$0.000039, time=1329ms
2026-01-26 17:05:37,587 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=1, 尝试次数=1
2026-01-26 17:05:37,587 - app.services.agent.tools.locate_tools - INFO - [_llm_rerank] LLM 选择候选 3
2026-01-26 17:05:37,591 - app.services.agent.tools.locate_tools - INFO - [locate_content] 全局降级成功: chapter=d272bd22-39dc-4133-875d-2936d17f7762, para=20
2026-01-26 17:05:37,595 - app.services.agent.tools.operate_tools - WARNING - [Operate] 全局降级：定位到其他章节 d272bd22-39dc-4133-875d-2936d17f7762，原章节 9becc1b4-4bc4-4ac1-992f-035440e66ec0
2026-01-26 17:05:37,595 - app.services.agent.tools.operate_tools - WARNING - [Operate] 跨章节定位：原章节 9becc1b4-4bc4-4ac1-992f-035440e66ec0 → 实际章节 d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:05:37,596 - app.services.agent.tools.operate_tools - INFO - [Operate] 定位完成: method=text_match, para=20
2026-01-26 17:05:37,598 - app.services.agent.tools.editor_tools - INFO - [apply_chapter_edit] 参数: chapter_id=d272bd22-39dc-4133-875d-2936d17f7762, operation=replace, content_len=1230
2026-01-26 17:05:37,612 - app.services.agent.tools.tool_types - INFO - [operate_apply] 执行成功 (耗时: 22.410s)
2026-01-26 17:05:37,612 - app.services.agent.execution.tool_executor - INFO - [StandardTool] operate_apply 执行成功
2026-01-26 17:05:37,622 - app.api.v1.agent - INFO - [Stream] 任务完成: 将AI生成的更有意境的段落替换掉原文中的旧段落。 (22.4s)
2026-01-26 17:05:37,623 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务3完成
2026-01-26 17:05:37,623 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共3个任务，耗时: 82.03s
2026-01-26 17:05:37,623 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 17:05:37,625 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 17:05:37,625 - app.services.agent.langgraph_agent - INFO - [Response] 3个输出任务（含续写），使用AI整合
2026-01-26 17:05:37,626 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 17:05:37,626 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=3, 展示型=0
2026-01-26 17:05:37,627 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=10545字符, 处理后=10656字符
2026-01-26 17:05:37,627 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 17:05:37,627 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 17:05:37,628 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 17:05:37,628 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 17:05:37,629 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 17:05:37,636 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 17:05:37,636 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 17:05:37,636 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 17:05:45,286 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 17:05:45,288 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 17:05:45,289 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 17:05:46,257 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 4 个数据块，总长度: 241
2026-01-26 17:05:46,258 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 14927 (prompt=14760, completion=167)
2026-01-26 17:05:46,259 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:05:46,260 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 17:05:46,277 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:05:46,278 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=14927, cost=$0.004845, time=8623ms
2026-01-26 17:05:46,279 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=241
2026-01-26 17:05:47,112 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:84892aef-e8dc-49a8-8e1e-3d863045b9ba | 重要度=0.77
2026-01-26 17:05:47,117 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:84892aef-e8dc-49a8-8e1e-3d863045b9ba:1d696d9e-af73-44ac-af7b-8ee23f5df7f7, token=295
2026-01-26 17:05:47,118 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:84892aef-e8dc-49a8-8e1e-3d863045b9ba:1d696d9e-af73-44ac-af7b-8ee23f5df7f7, 消息数=2, 摘要长度=0, Token=295
2026-01-26 17:05:47,119 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:84892aef-e8dc-49a8-8e1e-3d863045b9ba:1d696d9e-af73-44ac-af7b-8ee23f5df7f7)
2026-01-26 17:05:47,120 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 17:05:47,127 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 17:05:48,023 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/1d696d9e-af73-44ac-af7b-8ee23f5df7f7
INFO:     127.0.0.1:63676 - "GET /api/v1/agent/operations/1d696d9e-af73-44ac-af7b-8ee23f5df7f7 HTTP/1.1" 200 OK
2026-01-26 17:06:45,396 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:06:45,401 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:06:45,401 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:06:45,403 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:54090 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:06:45,430 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 84892aef-e8dc-49a8-8e1e-3d863045b9ba, chapter_id: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:06:45,437 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: d272bd22-39dc-4133-875d-2936d17f7762
2026-01-26 17:06:45,437 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:06:45,440 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57319 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:06:45,445 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:57321 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:06:45,463 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions
INFO:     127.0.0.1:53337 - "GET /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:06:45,602 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:06:45,604 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:53558 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 17:06:45,607 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:06:47,858 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:06:47,876 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:84892aef-e8dc-49a8-8e1e-3d863045b9ba
2026-01-26 17:06:47,878 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762
INFO:     127.0.0.1:55551 - "PUT /api/v1/chapters/d272bd22-39dc-4133-875d-2936d17f7762 HTTP/1.1" 200 OK
2026-01-26 17:06:47,879 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:06:49,923 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:07:22,697 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:53795 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:07:22,711 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:53794 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:07:22,724 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:59350 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:07:22,747 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:50532 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:07:28,633 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:07:28,686 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:28,688 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, type=<class 'uuid.UUID'>
2026-01-26 17:07:28,718 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:07:28,723 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:07:28,729 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:07:28,731 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:07:28,731 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:07:28,732 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:07:28,789 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:07:28,798 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=60s)
2026-01-26 17:07:29,020 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:07:29,028 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
2026-01-26 17:07:29,032 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
2026-01-26 17:07:29,038 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:50072 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
2026-01-26 17:07:29,050 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
INFO:     127.0.0.1:50073 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:50071 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
INFO:     127.0.0.1:50074 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
2026-01-26 17:07:29,185 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:07:29,209 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:07:29,216 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,227 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,235 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:07:29,246 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,266 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
2026-01-26 17:07:29,274 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
2026-01-26 17:07:29,283 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
2026-01-26 17:07:29,289 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
2026-01-26 17:07:29,299 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:55907 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:60766 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:60764 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:53694 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:55239 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:07:29,433 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,449 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,459 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,463 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:29,467 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
2026-01-26 17:07:29,473 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
INFO:     127.0.0.1:50070 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:07:29,481 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
INFO:     127.0.0.1:50214 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:50213 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:50216 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
2026-01-26 17:07:29,533 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:56184 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:07:29,589 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:07:29,610 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:07:29,613 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:07:29,625 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59263 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:07:29,637 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:07:29,656 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:07:29,659 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': False}
2026-01-26 17:07:29,686 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52486 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:07:29,756 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
INFO:     127.0.0.1:54302 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 17:07:29,779 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions
INFO:     127.0.0.1:54304 - "GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:07:29,922 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
INFO:     127.0.0.1:51804 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 17:07:30,021 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions
INFO:     127.0.0.1:61036 - "GET /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:07:30,071 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:30,074 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
INFO:     127.0.0.1:54303 - "PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 HTTP/1.1" 200 OK
2026-01-26 17:07:30,081 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:07:33,184 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:07:33,193 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:07:33,204 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:07:33,212 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:07:33,223 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:07:33,235 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions
2026-01-26 17:07:33,239 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9bd86e66-886f-4e36-bf3d-29a755a8053a
2026-01-26 17:07:33,240 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:07:33,247 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9bd86e66-886f-4e36-bf3d-29a755a8053a
2026-01-26 17:07:33,248 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:53327 - "GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:07:33,257 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 17:07:33,263 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52538 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
INFO:     127.0.0.1:53326 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:07:33,409 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:53328 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 17:07:33,464 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions
INFO:     127.0.0.1:52942 - "GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:07:33,512 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:33,517 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
INFO:     127.0.0.1:64140 - "PUT /api/v1/chapters/6a1cf453-f405-4bd1-a789-3f0b71fd9ef3 HTTP/1.1" 200 OK
2026-01-26 17:07:33,528 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第1章 吞噬 (order=1)
2026-01-26 17:07:35,797 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:35,802 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:61160 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:07:35,805 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:07:38,371 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第1章 吞噬 (88 paragraphs)
2026-01-26 17:07:38,397 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:07:38,487 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 19c51863-a5d0-40a9-b891-f6124d9446f0 内容更新，新段落数: 70
2026-01-26 17:07:38,506 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 19c51863-a5d0-40a9-b891-f6124d9446f0 内容更新，新段落数: 70
2026-01-26 17:07:38,617 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:38,687 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:62674 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:07:38,691 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:07:38,693 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/sessions
INFO:     127.0.0.1:54284 - "POST /api/v1/agent/sessions HTTP/1.1" 200 OK
2026-01-26 17:07:38,709 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:38,712 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:62671 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:07:38,715 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:07:42,334 - app.services.agent.model_selector - INFO - ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
2026-01-26 17:07:42,335 - app.services.ai.http_ai_service - INFO - ModelSelector 已启用
2026-01-26 17:07:42,335 - app.services.ai.http_ai_service - INFO - AILogService 已启用 (用于成本追踪)
2026-01-26 17:07:43,767 - app.services.ai.http_ai_service - INFO - HTTP AI Service 初始化成功，Base URL: https://204992.xyz:8443/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
2026-01-26 17:07:43,767 - app.api.v1.agent - INFO - [Chat Stream] Mode: planning
2026-01-26 17:07:43,773 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:54444 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
2026-01-26 17:07:43,777 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 19c51863-a5d0-40a9-b891-f6124d9446f0 内容更新，新段落数: 70
2026-01-26 17:07:43,785 - app.api.v1.agent - INFO - [LangGraph Agent Stream] ⏱️ 请求开始 - User: 79913e7e-d5cd-4e09-bce6-ca6639bd8456, Mode: planning, Message: 从第1章到第5章，段融的成长感不够明显，帮我在关键节点强化一下他的心态变化...
2026-01-26 17:07:43,791 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:07:45,765 - app.api.v1.agent - INFO - [agent_chat_stream] 📚 世界观数据已注入: 人物=11, 地点=7, 设定=7, 规范=无
2026-01-26 17:07:45,766 - app.services.agent.langgraph_agent - INFO - [Planning] 使用隔离的thread_id: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:7414c983-ce5d-4d9e-a503-01ce30ae2b26:11ff5b2e-4522-4ffd-a89a-504161817f1a (user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456, work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, conversation_id=11ff5b2e-4522-4ffd-a89a-504161817f1a)
2026-01-26 17:07:45,769 - app.services.context.manager - INFO - [ContextManager] 创建新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:7414c983-ce5d-4d9e-a503-01ce30ae2b26:11ff5b2e-4522-4ffd-a89a-504161817f1a
2026-01-26 17:07:45,769 - app.services.context.manager - INFO - [ContextManager] Session 79913e7e-d5cd-4e09-bce6-ca6639bd8456:7414c983-ce5d-4d9e-a503-01ce30ae2b26:11ff5b2e-4522-4ffd-a89a-504161817f1a: 0/16000 tokens
2026-01-26 17:07:45,854 - app.services.context.vector_memory_store - INFO - 🔍 检索记忆 | 查询='从第1章到第5章，段融的成长感不够明显，帮我在关键节点强化一...' | 隔离键=['user:79913e7e-d5cd-4e09-bce6-ca6639bd8456:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26', 'user:79913e7e-d5cd-4e09-bce6-ca6639bd8456'] | 找到=0条
2026-01-26 17:07:45,855 - app.services.context.manager - INFO - 🔍 检索长期记忆 | 级别=work | work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26 | 含用户级=True | 找到=0条
2026-01-26 17:07:45,863 - app.services.context.monitoring_integration - INFO - [Monitor] 上下文构建: 0条消息, 0 tokens, 耗时 96.64ms
2026-01-26 17:07:45,864 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:07:45,864 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:07:45,865 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=200, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 17:07:45,874 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:07:45,876 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:07:45,878 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:62673 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:07:45,881 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:07:48,115 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:07:48,882 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:07:48,882 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:07:48,894 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:07:48,897 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=366, cost=$0.000042, time=3018ms
2026-01-26 17:07:48,897 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=39, 尝试次数=1
2026-01-26 17:07:48,897 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:07:48,898 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=text_classification, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:07:48,898 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=20, temp=0.1, 尝试=1/3, task_type=TaskType.TEXT_CLASSIFICATION
2026-01-26 17:07:50,749 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:07:50,750 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:07:50,773 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:07:50,775 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=305, cost=$0.000031, time=1852ms
2026-01-26 17:07:50,775 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=7, 尝试次数=1
2026-01-26 17:07:50,775 - app.services.agent.intent.classifier - INFO - [Intent] AI识别结果: writing
2026-01-26 17:07:50,776 - app.services.agent.langgraph_agent - INFO - [Planning] AI意图分类: writing (置信度: 0.90)
2026-01-26 17:07:50,776 - app.services.agent.planning.plan_generator - INFO - [Planning] 开始规划: 从第1章到第5章，段融的成长感不够明显，帮我在关键节点强化一下他的心态变化...
2026-01-26 17:07:50,780 - app.core.cache - INFO - ✅ 缓存命中: prompt:planning:v2.41.0:get_planning_static_prompt:fca6eb91156619d0
2026-01-26 17:07:50,785 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:07:50,785 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=story_planning, complexity=complex, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro, reason=任务复杂度为 complex; 任务类型: story_planning; 选择 Gemini 2.5 Pro (质量评分: 9.0/10, 成本: $1.25/$10.0 per 1M tokens)
2026-01-26 17:07:50,786 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.3, task_type=TaskType.STORY_PLANNING
2026-01-26 17:08:00,805 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 17:08:12,141 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 22 个数据块，总长度: 4093
2026-01-26 17:08:12,142 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 21812 (prompt=20491, completion=1321)
2026-01-26 17:08:12,143 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:08:12,144 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:08:12,164 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:08:12,165 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=21812, cost=$0.038824, time=21359ms
2026-01-26 17:08:12,166 - app.services.agent.langgraph_agent - INFO - [_generate_text] 使用HTTPAIService生成文本，tokens=21812
2026-01-26 17:08:12,166 - app.services.agent.planning.plan_generator - INFO - [Planning] 思维链: 输出=用户希望得到一份关于主角“段融”在第1到5章心态变化不够明显, 原料=需要作品的第1章到第5章的全部内容，以及, 处理=首先，使用 explore_conten
2026-01-26 17:08:12,167 - app.services.agent.planning.plan_generator - INFO - [Planning] 规划生成成功，共2个任务
2026-01-26 17:08:12,168 - app.services.agent.langgraph_agent - INFO - [Planning] 规划完成，共2个任务，耗时: 21.39s
2026-01-26 17:08:12,168 - app.api.v1.agent - INFO - [Stream] Plan tasks: 2 items
2026-01-26 17:08:12,169 - app.services.agent.langgraph_agent - INFO - [Execution] 开始智能并行执行任务
2026-01-26 17:08:12,169 - app.services.agent.parameter_resolver - INFO - [ParameterResolver] 初始化完成, 严格模式: False
2026-01-26 17:08:12,171 - app.services.agent.execution.parallel_executor - INFO - [ParameterResolver] 参数解析器已启用
2026-01-26 17:08:12,172 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] DAG 调度启用，任务数=2, 有依赖任务=1
2026-01-26 17:08:12,174 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1开始: 为了分析段融的成长线，需要先读取从第1章到第5章的全部内容。
2026-01-26 17:08:12,175 - app.api.v1.agent - INFO - [Stream] Task started: 为了分析段融的成长线，需要先读取从第1章到第5章的全部内容。 (icon=Wrench)
2026-01-26 17:08:12,175 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 使用统一接口调用未知工具: explore_content
2026-01-26 17:08:12,176 - app.services.agent.tools.explore_tools - INFO - [explore_content] 开始: work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, target=读取第1章到第5章，用于分析段融的成长线
约束：章节范围：第1章、第5章...
2026-01-26 17:08:12,176 - app.services.agent.tools.explore_tools - INFO - [explore_content] 规划传入关键词: ['段融']
2026-01-26 17:08:12,177 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围锁定: 第1章、第5章
2026-01-26 17:08:12,177 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 开始探索 V3: work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, target=读取第1章到第5章，用于分析段融的成长线
约束：章节范围：第1章、第5章...
2026-01-26 17:08:12,178 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] ========== 阶段1：精确搜索 ==========
2026-01-26 17:08:12,202 - app.services.agent.tools.explore_tools - INFO - [_extract_keywords] 提取关键词: ['章到', '段融', '读取', '章节', '约束', '成长', '用于', '范围', '分析', '读取第']...
2026-01-26 17:08:12,203 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 使用提取的关键词: ['章到', '段融', '读取', '章节', '约束', '成长', '用于', '范围', '分析', '读取第']
2026-01-26 17:08:12,203 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围: (1, 5)
2026-01-26 17:08:12,262 - app.services.chapter_vector_service - INFO - [exact_search] work=7414c983-ce5d-4d9e-a503-01ce30ae2b26, keywords=['章到', '段融', '读取']..., mode=any, range=(1, 5), hits=100
2026-01-26 17:08:12,265 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索命中: 100 条
2026-01-26 17:08:12,266 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 精确搜索添加证据: 31 条
2026-01-26 17:08:12,267 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段2：AI 评估覆盖度 (精确搜索找到 31 条证据)
2026-01-26 17:08:12,267 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:08:12,268 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 17:08:12,268 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 17:08:28,740 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:08:28,741 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:08:28,765 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:08:28,768 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2285, cost=$0.004720, time=16473ms
2026-01-26 17:08:28,768 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=443, 尝试次数=1
2026-01-26 17:08:28,768 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true
  },
  "chapters_with_evidence": [
    1
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "exploration_summary": "已收集的信息包含第1章中关于段融的31条证据。内容描述了段融的外貌特征（身体单薄、长期饥饿所致）和在一个特定场景下的行为（跑进院子，观察人数）。",
  "next_action": "基于已收集的第1章和第5章信息，将对比段融在两个章节中的外貌、行为、能力或心理状态，以梳理其变化和成长轨迹。",
  "potential_gaps": [
    "第5章的内容"
  ]
}
```
2026-01-26 17:08:28,769 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=1/1, 章节=[1], 质量=[引用=False,互动=False,情节=False]
2026-01-26 17:08:28,769 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=31, 章节=1, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 17:08:28,771 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节覆盖不足: missing=[5]
2026-01-26 17:08:28,772 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 评估不足，缺失项: ['缺少第5章的证据片段']
2026-01-26 17:08:28,772 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 阶段3：AI 补充循环，当前 31 条证据
2026-01-26 17:08:28,773 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:08:28,773 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 17:08:28,774 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=500, temp=0.3, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 17:08:44,298 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:08:44,299 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:08:44,320 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:08:44,321 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=1803, cost=$0.005395, time=15526ms
2026-01-26 17:08:44,323 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=582, 尝试次数=1
2026-01-26 17:08:44,323 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] AI 任务理解完成: 通过对比分析角色“段融”在第1章和第5章这两个时间点的状态、关系和经历，来梳理出他的成长变化轨迹。...
2026-01-26 17:08:44,323 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: simple
2026-01-26 17:08:44,325 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=simple_qa, selected_model=gemini-2.5-flash-lite, default_model=gemini-2.5-pro
2026-01-26 17:08:44,325 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=400, temp=0.2, 尝试=1/3, task_type=TaskType.SIMPLE_QA
2026-01-26 17:08:45,865 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:08:45,866 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash-lite (actual_model=gemini-2.5-flash-lite, self.model=gemini-2.5-pro)
2026-01-26 17:08:45,883 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:08:45,884 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=969, cost=$0.000154, time=1541ms
2026-01-26 17:08:45,884 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=331, 尝试次数=1
2026-01-26 17:08:45,885 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, type=<class 'uuid.UUID'>
2026-01-26 17:08:45,889 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:08:45,889 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:08:45,890 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:08:45,890 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:08:45,936 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 章节范围映射: 第1章、第5章 -> 第1章、第5章
2026-01-26 17:08:45,936 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 多段章节范围，跳过单范围定位优化
2026-01-26 17:08:45,943 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:08:45,948 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 5 -> UUID 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:08:45,964 - app.services.agent.langgraph_tools - INFO - [get_writing_context] ✅ 获取创作上下文成功: include=worldview
2026-01-26 17:08:45,990 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, current_order=1, query=段融在第五章的状态和经历...
2026-01-26 17:08:46,094 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 17:08:56,649 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 11 个候选 -> top 5
2026-01-26 17:08:56,650 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 17:08:56,661 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, current_order=5, query=段融在第五章的状态和经历...
2026-01-26 17:08:56,769 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-26 17:09:02,469 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 11 个候选 -> top 5
2026-01-26 17:09:02,469 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 17:09:02,483 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第20段
2026-01-26 17:09:02,496 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第43段
2026-01-26 17:09:02,509 - app.services.agent.langgraph_tools - INFO - [read_paragraph] 缓存写入: 第1章第33段
2026-01-26 17:09:02,519 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, current_order=1, query=段融在第五章的人际关系...
2026-01-26 17:09:02,633 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 17:09:13,046 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 11 个候选 -> top 5
2026-01-26 17:09:13,047 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 17:09:13,063 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, current_order=5, query=段融在第五章的人际关系...
2026-01-26 17:09:13,170 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-26 17:09:19,097 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 11 个候选 -> top 5
2026-01-26 17:09:19,098 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 17:09:19,108 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, current_order=1, query=第五章中段融的关键事件或对话...
2026-01-26 17:09:19,224 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=1
2026-01-26 17:09:20,419 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 17:09:20,420 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 17:09:20,431 - app.services.chapter_vector_service - INFO - RAG retrieve work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, current_order=5, query=第五章中段融的关键事件或对话...
2026-01-26 17:09:20,511 - app.services.chapter_vector_service - INFO - RAG retrieved 10 segments within order<=5
2026-01-26 17:09:22,073 - app.services.search.hybrid_retriever - INFO - [Rerank] 重排序完成: 10 个候选 -> top 5
2026-01-26 17:09:22,073 - app.services.agent.langgraph_tools - INFO - [search_analysis_fragments_tool] ✅ Hybrid检索成功: 找到5个片段
2026-01-26 17:09:22,077 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: complex
2026-01-26 17:09:22,077 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 非流式调用智能选择: task_type=deep_analysis, selected_model=gemini-2.5-pro, default_model=gemini-2.5-pro
2026-01-26 17:09:22,078 - app.services.ai.http_ai_service - INFO - 开始非流式AI调用: max_tokens=600, temp=0, 尝试=1/3, task_type=TaskType.DEEP_ANALYSIS
2026-01-26 17:09:38,497 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:09:38,498 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-pro (actual_model=gemini-2.5-pro, self.model=gemini-2.5-pro)
2026-01-26 17:09:38,519 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:09:38,520 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=2561, cost=$0.005581, time=16420ms
2026-01-26 17:09:38,521 - app.services.ai.http_ai_service - INFO - AI响应成功, 长度=534, 尝试次数=1
2026-01-26 17:09:38,522 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取原始响应(截断): ```json
{
  "keyword_coverage": {
    "段融": true
  },
  "chapters_with_evidence": [
    1,
    5
  ],
  "content_quality": {
    "has_direct_quotes": true,
    "has_character_interactions": true,
    "has_plot_details": true
  },
  "summary": "收集到的信息包含角色段融在第1章和第5章的片段。第1章描述了他身体单薄、紧张地尝试“读取器灵”的状态。第5章则展示了他更为从容地思考器灵等级问题，并参与了关于处置他人的对话。",
  "next_action": "基于已收集信息，将对比分析段融在第1章和第5章的状态、能力和心境。通过对比他在第1章身体单薄、紧张的状态与第5章从容、进行策略思考的状态，梳理其成长变化；并根据对话内容初步推断其人际关系和地位的变化。",
  "potential_gaps": [
    "角色的明确目标",
    "社会地...
2026-01-26 17:09:38,522 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 指标提取结果: 关键词覆盖=1/1, 章节=[1, 5], 质量=[引用=False,互动=False,情节=False]
2026-01-26 17:09:38,523 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则判断: 证据=42, 章节=2, 关键词覆盖=100.0%, 质量=0/3
2026-01-26 17:09:38,523 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] V3.4 规则1命中: 证据≥30 且 覆盖≥50%% → 充足
2026-01-26 17:09:38,523 - app.services.agent.tools.explore_tools - INFO - [ContentExplorer] 探索完成: 2轮, 原因=AI 判断信息充足: 证据充足：42条证据，覆盖2个章节，关键词覆盖100%
2026-01-26 17:09:38,533 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,540 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,546 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,551 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,555 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,570 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,575 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,580 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,586 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,593 - app.services.agent.langgraph_tools - INFO - [resolve_chapter_id] 序号 1 -> UUID 6a1cf453-f405-4bd1-a789-3f0b71fd9ef3
2026-01-26 17:09:38,596 - app.services.agent.execution.tool_executor - INFO - [StandardTool] explore_content 执行成功
2026-01-26 17:09:38,598 - app.api.v1.agent - INFO - [Stream] 任务完成: 为了分析段融的成长线，需要先读取从第1章到第5章的全部内容。 (86.4s)
2026-01-26 17:09:38,599 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务1完成
2026-01-26 17:09:38,599 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2开始: 分析段融从第1章到第5章的心态变化和成长弧光，找出成长感不够明显的关键节点。
2026-01-26 17:09:38,600 - app.api.v1.agent - INFO - [Stream] Task started: 分析段融从第1章到第5章的心态变化和成长弧光，找出成长感不够明显的关键节点。 (icon=FileSearch)
2026-01-26 17:09:38,600 - app.services.agent.utils.tool_helpers - INFO - [参数标准化] analyze_content.content → text
2026-01-26 17:09:38,600 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_text_tool 使用 focus: '分析段融从第1章到第5章的心态变化和成长弧光，找出成长感不够明显的关键节点...'
2026-01-26 17:09:38,602 - app.services.agent.execution.task_runner - INFO - [TaskRunner] 调用 ToolExecutor(analyze_content)
2026-01-26 17:09:38,604 - app.services.agent.tools.tool_types - INFO - [analyze_content] 开始执行工具
2026-01-26 17:09:38,611 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 17:09:38,612 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 17:09:38,612 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=3000, temp=0.3, task_type=TaskType.SUMMARIZATION
2026-01-26 17:09:51,719 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 17:10:08,328 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 38 个数据块，总长度: 3635
2026-01-26 17:10:08,332 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 8736 (prompt=6292, completion=2444)
2026-01-26 17:10:08,335 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:10:08,335 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 17:10:08,352 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:10:08,355 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=8736, cost=$0.007998, time=29722ms
2026-01-26 17:10:08,357 - app.services.agent.tools.tool_types - INFO - [analyze_content] 执行成功 (耗时: 29.751s)
2026-01-26 17:10:08,358 - app.services.agent.execution.tool_executor - INFO - [StandardTool] analyze_content 执行成功
2026-01-26 17:10:08,359 - app.services.agent.execution.task_runner - INFO - [TaskRunner] analyze_content 执行成功（ToolExecutor）
2026-01-26 17:10:08,359 - app.api.v1.agent - INFO - [Stream] 任务完成: 分析段融从第1章到第5章的心态变化和成长弧光，找出成长感不够明显的关键节点。 (29.8s)
2026-01-26 17:10:08,359 - app.services.agent.execution.parallel_executor - INFO - [ParallelExecution] 串行就绪任务2完成
2026-01-26 17:10:08,360 - app.services.agent.langgraph_agent - INFO - [Execution] 所有任务执行完成，共2个任务，耗时: 116.19s
2026-01-26 17:10:08,361 - app.services.agent.langgraph_agent - INFO - [Response] 生成最终响应
2026-01-26 17:10:08,362 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-26 17:10:08,362 - app.services.agent.langgraph_agent - INFO - [Response] 2个输出任务（含续写），使用AI整合
2026-01-26 17:10:08,362 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用AI整合任务结果
2026-01-26 17:10:08,363 - app.services.agent.planning.response_builder - INFO - [TaskClassify] 任务分类: 输入型=0, 输出型=2, 展示型=0
2026-01-26 17:10:08,363 - app.services.agent.planning.response_builder - INFO - [Summarization] 上下文处理: 原始=5511字符, 处理后=5584字符
2026-01-26 17:10:08,365 - app.services.agent.planning.response_builder - INFO - [Summarization] 准备发送 summarization_start 事件
2026-01-26 17:10:08,365 - app.services.agent.stream.stream_event_handler - INFO - [StreamEventHandler] emit_summarization_start 被调用, _on_flow_event=True
2026-01-26 17:10:08,366 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_start 事件已发送
2026-01-26 17:10:08,367 - app.services.agent.planning.response_builder - INFO - [Summarization] 使用流式生成（_generate_text_stream）
2026-01-26 17:10:08,367 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 开始流式生成，buffer_size=1
2026-01-26 17:10:08,380 - app.services.agent.model_selector - INFO - [ModelSelector] 任务复杂度: medium
2026-01-26 17:10:08,381 - app.services.ai.http_ai_service - INFO - [ModelSelector] ✅ 智能选择成功: task_type=summarization, complexity=medium, selected_model=gemini-2.5-flash, default_model=gemini-2.5-pro, reason=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.3/$2.5 per 1M tokens)
2026-01-26 17:10:08,382 - app.services.ai.http_ai_service - INFO - 开始调用 AI API: model=gemini-2.5-flash, max_tokens=2000, temp=0.7, task_type=TaskType.SUMMARIZATION
2026-01-26 17:10:12,065 - app.services.ai.http_ai_service - INFO - API 流式响应已建立，开始接收数据...
2026-01-26 17:10:12,067 - app.services.agent.planning.response_builder - INFO - [Summarization] summarization_complete 事件已发送（第一个chunk时）
2026-01-26 17:10:12,069 - app.services.agent.planning.response_builder - INFO - [Summarization] output_ready 事件已发送（第一个chunk时）
2026-01-26 17:10:16,020 - app.services.ai.http_ai_service - INFO - API 响应完成，共接收 18 个数据块，总长度: 1734
2026-01-26 17:10:16,020 - app.services.ai.http_ai_service - INFO - 流式响应Token统计: 10428 (prompt=9321, completion=1107)
2026-01-26 17:10:16,022 - app.services.ai.http_ai_service - INFO - [成本追踪] user_id来源: 上下文, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:10:16,023 - app.services.ai.http_ai_service - INFO - [成本追踪] 记录模型: gemini-2.5-flash (actual_model=gemini-2.5-flash, self.model=gemini-2.5-pro)
2026-01-26 17:10:16,034 - app.services.ai.http_ai_service - INFO - [积分扣除] 管理员 79913e7e-d5cd-4e09-bce6-ca6639bd8456 豁免积分扣除
2026-01-26 17:10:16,035 - app.services.ai.http_ai_service - INFO - [AILogService] API调用已记录到数据库 (来源:上下文): tokens=10428, cost=$0.005564, time=7639ms
2026-01-26 17:10:16,036 - app.services.agent.langgraph_agent - INFO - [_generate_text_stream] 流式生成完成，总长度=1734
2026-01-26 17:10:16,784 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:7414c983-ce5d-4d9e-a503-01ce30ae2b26 | 重要度=0.72
2026-01-26 17:10:17,766 - app.services.context.manager - INFO - ✅ 保存长期记忆 | ID=79913e7e-d5cd-4e09-b... | 隔离=work:7414c983-ce5d-4d9e-a503-01ce30ae2b26 | 重要度=0.77
2026-01-26 17:10:17,785 - app.services.context.store - INFO - [ContextStore] 保存上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:7414c983-ce5d-4d9e-a503-01ce30ae2b26:11ff5b2e-4522-4ffd-a89a-504161817f1a, token=1797
2026-01-26 17:10:17,788 - app.services.context.manager - INFO - [ContextManager] 更新上下文: 79913e7e-d5cd-4e09-bce6-ca6639bd8456:7414c983-ce5d-4d9e-a503-01ce30ae2b26:11ff5b2e-4522-4ffd-a89a-504161817f1a, 消息数=2, 摘要长度=0, Token=1797
2026-01-26 17:10:17,788 - app.services.agent.langgraph_agent - INFO - [Planning] 已保存对话到 ContextManager (session=79913e7e-d5cd-4e09-bce6-ca6639bd8456:7414c983-ce5d-4d9e-a503-01ce30ae2b26:11ff5b2e-4522-4ffd-a89a-504161817f1a)
2026-01-26 17:10:17,789 - app.api.v1.agent - INFO - [Stream] 跳过最终响应（内容已流式发送）
2026-01-26 17:10:17,795 - app.api.v1.agent - INFO - [LangGraph Agent Stream] User 79913e7e-d5cd-4e09-bce6-ca6639bd8456 - Mode: planning, Stream completed
2026-01-26 17:10:29,544 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a
INFO:     127.0.0.1:52198 - "GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a HTTP/1.1" 200 OK
2026-01-26 17:13:58,617 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:65221 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:13:58,688 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:50915 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:13:58,707 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65220 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:13:58,819 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:55957 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:13:59,022 - app.services.chapter_comment_service - INFO - [ChapterCommentService] 章节 19c51863-a5d0-40a9-b891-f6124d9446f0 内容更新，新段落数: 70
2026-01-26 17:13:59,077 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:13:59,079 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:65216 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:13:59,084 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:14:03,202 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:14:03,224 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,225 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, type=<class 'uuid.UUID'>
2026-01-26 17:14:03,229 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:14:03,235 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:14:03,238 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:14:03,239 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:14:03,239 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:14:03,239 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:14:03,268 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:14:03,273 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=60s)
2026-01-26 17:14:03,278 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
INFO:     127.0.0.1:61168 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
2026-01-26 17:14:03,283 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:61167 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:14:03,312 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:14:03,318 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,323 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
INFO:     127.0.0.1:61166 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61169 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
2026-01-26 17:14:03,343 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:14:03,354 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:14:03,356 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
INFO:     127.0.0.1:61170 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
2026-01-26 17:14:03,368 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
2026-01-26 17:14:03,384 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,392 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     127.0.0.1:61442 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
2026-01-26 17:14:03,403 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,409 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
INFO:     127.0.0.1:54333 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
2026-01-26 17:14:03,417 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,418 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:62630 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62628 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:14:03,451 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,476 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
2026-01-26 17:14:03,483 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:59478 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
2026-01-26 17:14:03,498 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:14:03,501 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
2026-01-26 17:14:03,505 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:54986 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
2026-01-26 17:14:03,508 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
INFO:     127.0.0.1:61444 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:14:03,510 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
INFO:     127.0.0.1:53149 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
2026-01-26 17:14:03,539 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,542 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
INFO:     127.0.0.1:63405 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:14:03,594 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:14:03,608 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:14:03,618 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9bd86e66-886f-4e36-bf3d-29a755a8053a
2026-01-26 17:14:03,618 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:14:03,625 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 17:14:03,628 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:64967 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:14:03,645 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:14:03,650 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9bd86e66-886f-4e36-bf3d-29a755a8053a
2026-01-26 17:14:03,651 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:14:03,656 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:53931 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:14:03,808 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a
INFO:     127.0.0.1:51865 - "GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a HTTP/1.1" 200 OK
2026-01-26 17:14:03,843 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
INFO:     127.0.0.1:51867 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 17:14:03,854 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a
INFO:     127.0.0.1:56005 - "GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a HTTP/1.1" 200 OK
2026-01-26 17:14:03,900 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions
INFO:     127.0.0.1:51869 - "GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:14:03,995 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:03,999 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:51868 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:14:04,010 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:14:04,071 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
INFO:     127.0.0.1:64288 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 17:14:07,415 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions
2026-01-26 17:14:07,421 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     127.0.0.1:54651 - "GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:14:07,461 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:14:07,465 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:55351 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:14:07,471 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:14:10,871 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:14:10,892 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:62196 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:14:10,898 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:62197 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:14:10,960 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58530 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:14:10,981 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:52047 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:14:14,130 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:14:14,146 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,147 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, type=<class 'uuid.UUID'>
2026-01-26 17:14:14,150 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 17:14:14,158 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:14:14,158 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:14:14,158 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:14:14,159 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:14:14,175 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:14:14,181 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=60s)
2026-01-26 17:14:14,182 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,186 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 17:14:14,188 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 17:14:14,191 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
INFO:     127.0.0.1:60260 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
INFO:     127.0.0.1:60261 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
2026-01-26 17:14:14,198 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,199 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
2026-01-26 17:14:14,200 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
INFO:     127.0.0.1:60259 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
INFO:     127.0.0.1:60262 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:60263 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
2026-01-26 17:14:14,242 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:14:14,249 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,253 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 17:14:14,257 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=300s)
2026-01-26 17:14:14,262 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,265 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
2026-01-26 17:14:14,266 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
2026-01-26 17:14:14,267 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
2026-01-26 17:14:14,268 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,269 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:59450 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:64870 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:64767 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:59449 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
INFO:     127.0.0.1:59452 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 17:14:14,312 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,319 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
INFO:     127.0.0.1:50300 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
2026-01-26 17:14:14,331 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,335 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,340 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
2026-01-26 17:14:14,343 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,345 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
INFO:     127.0.0.1:60819 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:60821 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
2026-01-26 17:14:14,350 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
INFO:     127.0.0.1:60823 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:14:14,370 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:14:14,380 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:14:14,385 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e43a4f06-f97c-43bf-8801-7b25b8a3f4af
2026-01-26 17:14:14,386 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:14:14,391 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:60427 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:14:14,396 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:14:14,404 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:14:14,409 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e43a4f06-f97c-43bf-8801-7b25b8a3f4af
2026-01-26 17:14:14,409 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:14:14,411 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:62665 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:14:14,607 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26
INFO:     127.0.0.1:58649 - "GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26 HTTP/1.1" 200 OK
2026-01-26 17:14:14,655 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions
2026-01-26 17:14:14,658 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:58653 - "GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:58650 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 17:14:14,728 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26
INFO:     127.0.0.1:56920 - "GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26 HTTP/1.1" 200 OK
2026-01-26 17:14:14,852 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26
INFO:     127.0.0.1:54059 - "GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26 HTTP/1.1" 200 OK
2026-01-26 17:14:14,860 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:54057 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 17:14:14,875 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions
INFO:     127.0.0.1:62409 - "GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:14:14,887 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:14,890 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:58652 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 17:14:14,893 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:14:18,709 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:14:18,759 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:14:18,761 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:56926 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 17:14:18,762 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:14:21,139 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:15:30,050 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:64847 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:15:30,075 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:64849 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:15:30,096 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:53150 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:15:30,126 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:64337 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:15:35,515 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:15:35,522 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,529 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,532 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,533 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, type=<class 'uuid.UUID'>
2026-01-26 17:15:35,538 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,539 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,540 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
2026-01-26 17:15:35,542 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:15:35,543 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:15:35,543 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:15:35,543 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:15:35,560 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:15:35,564 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad (expire=60s)
INFO:     127.0.0.1:49406 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 17:15:35,566 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
INFO:     127.0.0.1:49409 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
2026-01-26 17:15:35,569 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
INFO:     127.0.0.1:49411 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:49410 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
2026-01-26 17:15:35,579 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:49407 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 17:15:35,609 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,616 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,622 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
2026-01-26 17:15:35,627 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
INFO:     127.0.0.1:51156 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:35,631 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:56321 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:35,637 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,640 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:62969 - "GET /api/v1/works/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 17:15:35,644 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters
INFO:     127.0.0.1:58712 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/characters HTTP/1.1" 200 OK
2026-01-26 17:15:35,651 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings
INFO:     127.0.0.1:51307 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/settings HTTP/1.1" 200 OK
2026-01-26 17:15:35,665 - app.api.v1.chapters - INFO - [GET chapters] work_id=b0a47953-7246-42d6-bb24-eba29c2606ad, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:15:35,670 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,674 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,677 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:35,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations
2026-01-26 17:15:35,681 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines
2026-01-26 17:15:35,683 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:62354 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57836 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:35,688 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b0a47953-7246-42d6-bb24-eba29c2606ad
INFO:     127.0.0.1:57835 - "GET /api/v1/chapters/work/b0a47953-7246-42d6-bb24-eba29c2606ad HTTP/1.1" 200 OK
2026-01-26 17:15:35,693 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines
INFO:     127.0.0.1:50194 - "GET /api/v1/worldview/works/b0a47953-7246-42d6-bb24-eba29c2606ad/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:35,707 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:15:35,713 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:15:35,715 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e43a4f06-f97c-43bf-8801-7b25b8a3f4af
2026-01-26 17:15:35,715 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:15:35,719 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:52354 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:15:35,728 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b0a47953-7246-42d6-bb24-eba29c2606ad, chapter_id: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:15:35,733 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 4010049e-6d95-4abe-872d-1eb0c0d756d5
2026-01-26 17:15:35,736 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: e43a4f06-f97c-43bf-8801-7b25b8a3f4af
2026-01-26 17:15:35,736 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:15:35,738 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:51989 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:15:35,905 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26
INFO:     127.0.0.1:53446 - "GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26 HTTP/1.1" 200 OK
2026-01-26 17:15:35,938 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:53448 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 17:15:35,987 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26
2026-01-26 17:15:35,997 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions
INFO:     127.0.0.1:62346 - "GET /api/v1/agent/operations/d25295f3-b024-477c-9990-a00e67178f26 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53449 - "GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:15:36,067 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:36,075 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:53445 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 17:15:36,080 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:15:36,133 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status
INFO:     127.0.0.1:63376 - "GET /api/v1/analysis/works/b0a47953-7246-42d6-bb24-eba29c2606ad/status HTTP/1.1" 404 Not Found
2026-01-26 17:15:38,960 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions
INFO:     127.0.0.1:63377 - "GET /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:15:38,999 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:15:39,017 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b0a47953-7246-42d6-bb24-eba29c2606ad
2026-01-26 17:15:39,018 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5
INFO:     127.0.0.1:56174 - "PUT /api/v1/chapters/4010049e-6d95-4abe-872d-1eb0c0d756d5 HTTP/1.1" 200 OK
2026-01-26 17:15:39,019 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:15:41,939 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:15:42,235 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:60908 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:15:42,252 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:60907 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:15:42,256 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:63079 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:15:42,283 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:53654 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:15:46,722 - app.api.v1.chapters - INFO - [GET chapters] work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:15:46,739 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,739 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, type=<class 'uuid.UUID'>
2026-01-26 17:15:46,754 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:15:46,754 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:15:46,755 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:15:46,755 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:15:46,779 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:15:46,783 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=60s)
2026-01-26 17:15:46,786 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,790 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 17:15:46,793 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 17:15:46,796 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
INFO:     127.0.0.1:58832 - "GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
2026-01-26 17:15:46,802 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,804 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations
2026-01-26 17:15:46,806 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters
2026-01-26 17:15:46,807 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings
INFO:     127.0.0.1:58833 - "GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
INFO:     127.0.0.1:58835 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:58834 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:58837 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings HTTP/1.1" 200 OK
2026-01-26 17:15:46,843 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
2026-01-26 17:15:46,855 - app.api.v1.chapters - INFO - [GET chapters] work_id=53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:15:46,856 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines
2026-01-26 17:15:46,862 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 (expire=300s)
INFO:     127.0.0.1:49219 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:46,871 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,875 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,878 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,879 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines
2026-01-26 17:15:46,883 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
INFO:     127.0.0.1:52116 - "GET /api/v1/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
INFO:     127.0.0.1:60252 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:46,887 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,888 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations
INFO:     127.0.0.1:61968 - "GET /api/v1/chapters/work/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873 HTTP/1.1" 200 OK
INFO:     127.0.0.1:63311 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/locations HTTP/1.1" 200 OK
2026-01-26 17:15:46,899 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters
INFO:     127.0.0.1:63313 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/characters HTTP/1.1" 200 OK
2026-01-26 17:15:46,914 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,920 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings
2026-01-26 17:15:46,924 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:46,927 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
INFO:     127.0.0.1:58693 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/settings HTTP/1.1" 200 OK
2026-01-26 17:15:46,930 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines
2026-01-26 17:15:46,931 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines
INFO:     127.0.0.1:50965 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:50963 - "GET /api/v1/worldview/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/guidelines HTTP/1.1" 200 OK
2026-01-26 17:15:46,959 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 17:15:46,963 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 17:15:46,965 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9e65d7f6-85c9-4bb4-a2f3-6ce886387672
2026-01-26 17:15:46,966 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:15:46,967 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56598 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:15:46,979 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873, chapter_id: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 17:15:46,984 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: cf119734-c397-4025-a3f8-0147da826cdb
2026-01-26 17:15:46,986 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9e65d7f6-85c9-4bb4-a2f3-6ce886387672
2026-01-26 17:15:46,987 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:15:46,989 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:50091 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:15:47,133 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999
INFO:     127.0.0.1:49432 - "GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999 HTTP/1.1" 200 OK
2026-01-26 17:15:47,219 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status
2026-01-26 17:15:47,227 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions
INFO:     127.0.0.1:49434 - "GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:49433 - "GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:15:47,315 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999
INFO:     127.0.0.1:57690 - "GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999 HTTP/1.1" 200 OK
2026-01-26 17:15:47,400 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:47,415 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb
INFO:     127.0.0.1:49431 - "PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb HTTP/1.1" 200 OK
2026-01-26 17:15:47,433 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:15:51,000 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999
2026-01-26 17:15:51,003 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status
INFO:     127.0.0.1:61329 - "GET /api/v1/agent/operations/e8da7500-5304-4bca-98a1-9a53b49e4999 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61326 - "GET /api/v1/analysis/works/53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873/status HTTP/1.1" 404 Not Found
2026-01-26 17:15:51,034 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:15:51,039 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions
INFO:     127.0.0.1:61327 - "GET /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:15:51,107 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:53e5c1cc-8ffe-4a4d-9d82-04b5a9bb6873
2026-01-26 17:15:51,111 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb
INFO:     127.0.0.1:57959 - "PUT /api/v1/chapters/cf119734-c397-4025-a3f8-0147da826cdb HTTP/1.1" 200 OK
2026-01-26 17:15:51,118 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:15:55,276 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:17:37,289 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:58931 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:17:37,302 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:58932 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:17:37,328 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:57933 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:17:37,334 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:57381 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:17:40,970 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:17:40,990 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:40,991 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 17:17:40,997 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 17:17:41,000 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:17:41,000 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:17:41,000 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:17:41,000 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:17:41,021 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:17:41,024 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 17:17:41,026 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,029 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 17:17:41,033 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 17:17:41,034 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:61905 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61906 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
2026-01-26 17:17:41,040 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,043 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:17:41,043 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
INFO:     127.0.0.1:61907 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61908 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:61909 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
2026-01-26 17:17:41,086 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:17:41,092 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 17:17:41,101 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,105 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,109 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,111 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=300s)
2026-01-26 17:17:41,113 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,114 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
2026-01-26 17:17:41,115 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
2026-01-26 17:17:41,116 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,117 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:17:41,117 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:64128 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51132 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:49499 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:64567 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:64569 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:64127 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:17:41,147 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,150 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,153 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:17:41,155 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,157 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:58026 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:59855 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 17:17:41,162 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:59857 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:17:41,196 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:17:41,200 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:17:41,201 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:17:41,202 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:17:41,203 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:56569 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:17:41,210 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:17:41,215 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:17:41,217 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:17:41,217 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:17:41,218 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:55317 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:17:41,312 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:55231 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:17:41,330 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:55232 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 17:17:41,336 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:55234 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:17:41,409 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:62743 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:17:41,530 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:56524 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:17:41,537 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:41,540 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
2026-01-26 17:17:41,542 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:17:41,544 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:55669 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:55230 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:17:41,549 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
INFO:     127.0.0.1:55667 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:17:44,094 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:17:44,129 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:17:44,130 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:49817 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:17:44,133 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:17:46,420 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     connection closed
INFO:     ('127.0.0.1', 54395) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:18:01,421 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     ('127.0.0.1', 55109) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:18:01,441 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection closed
2026-01-26 17:18:02,589 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:18:02,604 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,615 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,624 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,632 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,636 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,644 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,644 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
INFO:     127.0.0.1:58946 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:18:02,657 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:18:02,660 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
2026-01-26 17:18:02,665 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:18:02,670 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:18:02,671 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:18:02,673 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:18:02,675 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:18:02,730 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:18:02,735 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 17:18:02,740 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:58949 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:58951 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:58950 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:58952 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:02,775 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:58948 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:18:02,845 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,864 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,869 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
2026-01-26 17:18:02,877 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,883 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,886 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:62212 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:02,894 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,896 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
INFO:     127.0.0.1:51295 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:18:02,902 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:51298 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
2026-01-26 17:18:02,905 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:18:02,908 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:51300 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:51301 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61134 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:02,933 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:18:02,949 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,958 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,967 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:02,975 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:60743 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:61966 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:03,061 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:03,074 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:03,086 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:18:03,087 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:18:03,096 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58753 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:18:03,103 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:03,112 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:03,116 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:18:03,118 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:18:03,122 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63650 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:18:03,344 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:58323 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:18:03,378 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
2026-01-26 17:18:03,382 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:58327 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:58328 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:18:03,444 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:56093 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:18:03,590 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:59042 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 17:18:03,625 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:53517 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:18:03,656 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:56986 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:18:03,686 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:03,691 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:58329 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:18:03,696 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:18:06,409 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:18:06,462 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:06,464 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:56407 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:18:06,466 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
INFO:     ('127.0.0.1', 52657) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:18:06,472 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-26 17:18:09,321 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 55630) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:18:27,094 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     ('127.0.0.1', 59802) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:18:27,132 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection closed
2026-01-26 17:18:27,877 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:18:27,910 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:27,911 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 17:18:27,916 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:27,918 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:27,922 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:27,927 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:18:27,928 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:18:27,930 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:18:27,931 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:18:27,994 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:18:28,002 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 17:18:28,011 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,016 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:62429 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:18:28,025 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
2026-01-26 17:18:28,029 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
2026-01-26 17:18:28,031 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:18:28,034 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,038 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
INFO:     127.0.0.1:62434 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62432 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:62431 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:62430 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62433 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
2026-01-26 17:18:28,105 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,119 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
2026-01-26 17:18:28,123 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:18:28,134 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:53629 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:28,152 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,156 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,160 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,163 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,165 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:52469 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:18:28,172 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,176 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:52470 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:28,185 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
INFO:     127.0.0.1:59667 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:59664 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:59665 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
2026-01-26 17:18:28,233 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:28,245 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:18:28,251 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:61549 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
2026-01-26 17:18:28,265 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:64222 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:18:28,296 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:28,312 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:28,319 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:28,322 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:18:28,324 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:18:28,333 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:18:28,337 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:57842 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:18:28,348 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:18:28,349 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:18:28,356 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:58874 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:18:28,476 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:64612 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:18:28,522 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:64614 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 17:18:28,552 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:64616 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:18:28,663 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:65208 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:18:28,784 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:52731 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:18:28,820 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
2026-01-26 17:18:28,829 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:54286 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:18:28,839 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
2026-01-26 17:18:28,842 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:52732 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:64613 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:18:28,853 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:18:31,797 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:18:31,819 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:18:31,822 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:57176 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:18:31,823 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
INFO:     ('127.0.0.1', 62208) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:18:34,801 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-26 17:18:34,826 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:20:04,635 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:64786 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:20:04,647 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:64787 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:20:04,685 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
2026-01-26 17:20:04,686 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:65027 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
INFO:     127.0.0.1:51256 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:20:18,282 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:20:18,297 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,298 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 17:20:18,306 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,311 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,316 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,321 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:20:18,323 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:20:18,323 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:20:18,324 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:20:18,356 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:20:18,362 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 17:20:18,372 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:20:18,373 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:20:18,373 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
2026-01-26 17:20:18,374 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:57878 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:57877 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:57879 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:57876 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:18,385 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:57875 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:18,417 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,419 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,423 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,426 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:20:18,429 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,433 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,438 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,440 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
2026-01-26 17:20:18,440 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
2026-01-26 17:20:18,442 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:20:18,443 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
INFO:     127.0.0.1:56953 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51641 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 17:20:18,446 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:56952 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
2026-01-26 17:20:18,448 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:60302 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:60303 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:60305 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:18,479 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,482 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,485 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:18,486 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
2026-01-26 17:20:18,488 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:62569 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:62573 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:62571 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:20:18,561 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:18,570 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:18,571 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:20:18,571 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:20:18,573 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 17:20:18,575 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:58284 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:20:18,583 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:18,587 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:20:18,587 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:20:18,590 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:64804 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:20:18,724 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:65327 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:20:18,774 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
2026-01-26 17:20:18,792 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:65328 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
INFO:     127.0.0.1:65329 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:20:18,990 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:54673 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:20:19,072 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:56844 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:20:19,092 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:61314 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 17:20:19,107 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:19,117 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:65326 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:20:19,124 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:20:21,648 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:20:21,670 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:21,671 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:50732 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:20:21,673 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:20:23,797 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
INFO:     connection closed
INFO:     connection closed
INFO:     ('127.0.0.1', 57208) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:20:41,580 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     ('127.0.0.1', 64700) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:20:41,600 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
INFO:     connection closed
2026-01-26 17:20:42,360 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:20:42,390 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,397 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,400 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=b1456da2-6a55-49e8-ad42-2332dc579363, type=<class 'uuid.UUID'>
2026-01-26 17:20:42,408 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,416 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,422 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:20:42,424 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:20:42,425 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:20:42,427 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:20:42,478 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:20:42,487 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363 (expire=60s)
2026-01-26 17:20:42,491 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:55048 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:42,502 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:20:42,506 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:20:42,514 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
2026-01-26 17:20:42,521 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:55051 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:55050 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
INFO:     127.0.0.1:55053 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
2026-01-26 17:20:42,552 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:55049 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:42,583 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
INFO:     127.0.0.1:55052 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
2026-01-26 17:20:42,641 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,667 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,685 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,692 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,695 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
2026-01-26 17:20:42,699 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations
2026-01-26 17:20:42,700 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:58379 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:20:42,706 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines
INFO:     127.0.0.1:61843 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:61841 - "GET /api/v1/works/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:42,714 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters
2026-01-26 17:20:42,717 - app.api.v1.chapters - INFO - [GET chapters] work_id=b1456da2-6a55-49e8-ad42-2332dc579363, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     127.0.0.1:51575 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/guidelines HTTP/1.1" 200 OK
INFO:     127.0.0.1:51573 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/characters HTTP/1.1" 200 OK
2026-01-26 17:20:42,745 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,767 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363
INFO:     127.0.0.1:50780 - "GET /api/v1/chapters/work/b1456da2-6a55-49e8-ad42-2332dc579363 HTTP/1.1" 200 OK
2026-01-26 17:20:42,802 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,810 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:42,816 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings
2026-01-26 17:20:42,819 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines
INFO:     127.0.0.1:50928 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/settings HTTP/1.1" 200 OK
INFO:     127.0.0.1:52178 - "GET /api/v1/worldview/works/b1456da2-6a55-49e8-ad42-2332dc579363/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:20:42,863 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:42,872 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:42,878 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:20:42,880 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:20:42,885 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:63872 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:20:42,908 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: b1456da2-6a55-49e8-ad42-2332dc579363, chapter_id: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:42,915 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 6903be9b-2bc2-42d0-8b08-75d679ee3591
2026-01-26 17:20:42,917 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: a136312a-0333-4e14-84eb-f856dbb50ad9
2026-01-26 17:20:42,918 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:20:42,922 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:61030 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:20:43,043 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:51705 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:20:43,094 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:51706 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 17:20:43,210 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
INFO:     127.0.0.1:54409 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
2026-01-26 17:20:43,234 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:51708 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:20:43,338 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:43,353 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:51704 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:20:43,378 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:20:43,535 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363
2026-01-26 17:20:43,549 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status
INFO:     127.0.0.1:49712 - "GET /api/v1/agent/operations/a7f7bd35-cd62-4ce0-821b-239b342cb363 HTTP/1.1" 200 OK
INFO:     127.0.0.1:49711 - "GET /api/v1/analysis/works/b1456da2-6a55-49e8-ad42-2332dc579363/status HTTP/1.1" 404 Not Found
2026-01-26 17:20:46,529 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions
INFO:     127.0.0.1:49714 - "GET /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:20:46,562 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:20:46,700 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:b1456da2-6a55-49e8-ad42-2332dc579363
2026-01-26 17:20:46,704 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591
INFO:     127.0.0.1:63551 - "PUT /api/v1/chapters/6903be9b-2bc2-42d0-8b08-75d679ee3591 HTTP/1.1" 200 OK
2026-01-26 17:20:46,711 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
INFO:     ('127.0.0.1', 53005) - "WebSocket /api/v1/ws/notifications/79913e7e-d5cd-4e09-bce6-ca6639bd8456" [accepted]
2026-01-26 17:20:46,726 - app.api.v1.ws - INFO - [WebSocket] 通知连接建立: user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     connection open
2026-01-26 17:20:49,702 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:21:35,997 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:54120 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:21:36,009 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:54119 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:21:36,036 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/notifications/user/notifications
INFO:     127.0.0.1:60187 - "GET /api/v1/notifications/user/notifications?params%5Bpage%5D=1&params%5BpageSize%5D=10 HTTP/1.1" 200 OK
2026-01-26 17:21:36,045 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works
INFO:     127.0.0.1:65157 - "GET /api/v1/works?skip=0&limit=100 HTTP/1.1" 200 OK
2026-01-26 17:21:37,474 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
2026-01-26 17:21:37,487 - app.api.v1.chapters - INFO - ⚠️ [GET chapters] 缓存未命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,488 - app.services.chapter_service - INFO - [ChapterService] Querying chapters for work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, type=<class 'uuid.UUID'>
2026-01-26 17:21:37,499 - app.services.chapter_service - INFO - [ChapterService] Found 5 chapters
2026-01-26 17:21:37,502 - app.services.chapter_service - INFO -   - Chapter: 第1章 吞噬, order=1
2026-01-26 17:21:37,504 - app.services.chapter_service - INFO -   - ... (3 more chapters)
2026-01-26 17:21:37,506 - app.services.chapter_service - INFO -   - Chapter: 第5章 太一门, order=5
2026-01-26 17:21:37,527 - app.api.v1.chapters - INFO - [GET chapters] Returning 5 chapters
2026-01-26 17:21:37,531 - app.api.v1.chapters - INFO - 💾 [GET chapters] 缓存已保存: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=60s)
2026-01-26 17:21:37,539 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:21:37,544 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,548 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
INFO:     127.0.0.1:52886 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:21:37,553 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,556 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
2026-01-26 17:21:37,561 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
INFO:     127.0.0.1:52887 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:21:37,565 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
INFO:     127.0.0.1:52890 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:52888 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
2026-01-26 17:21:37,574 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
INFO:     127.0.0.1:52891 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
2026-01-26 17:21:37,604 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:21:37,614 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
2026-01-26 17:21:37,617 - app.api.v1.worldview - INFO - 💾 [Worldview] 缓存已保存: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26 (expire=300s)
2026-01-26 17:21:37,622 - app.api.v1.chapters - INFO - [GET chapters] work_id=7414c983-ce5d-4d9e-a503-01ce30ae2b26, user_id=79913e7e-d5cd-4e09-bce6-ca6639bd8456
INFO:     127.0.0.1:63806 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
2026-01-26 17:21:37,630 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:locations:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,633 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
2026-01-26 17:21:37,637 - app.api.v1.chapters - INFO - ✅ [GET chapters] 缓存命中: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,643 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:characters:7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:49939 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:21:37,647 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations
2026-01-26 17:21:37,650 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,658 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:52946 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/locations HTTP/1.1" 200 OK
INFO:     127.0.0.1:58626 - "GET /api/v1/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
2026-01-26 17:21:37,669 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters
INFO:     127.0.0.1:52944 - "GET /api/v1/chapters/work/7414c983-ce5d-4d9e-a503-01ce30ae2b26 HTTP/1.1" 200 OK
INFO:     127.0.0.1:56363 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/characters HTTP/1.1" 200 OK
2026-01-26 17:21:37,710 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:settings:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,734 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:37,738 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings
INFO:     127.0.0.1:52774 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/settings HTTP/1.1" 200 OK
2026-01-26 17:21:37,763 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines
2026-01-26 17:21:37,777 - app.api.v1.worldview - INFO - ✅ [Worldview] 缓存命中: worldview:ai-guidelines:7414c983-ce5d-4d9e-a503-01ce30ae2b26
INFO:     127.0.0.1:50328 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/guidelines HTTP/1.1" 200 OK
2026-01-26 17:21:37,797 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines
INFO:     127.0.0.1:56484 - "GET /api/v1/worldview/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/ai-guidelines HTTP/1.1" 200 OK
2026-01-26 17:21:37,825 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:21:37,841 - app.api.v1.ai - INFO - [预加载元数据] 用户: 文枢AI管理者(79913e7e-d5cd-4e09-bce6-ca6639bd8456), work_id: 7414c983-ce5d-4d9e-a503-01ce30ae2b26, chapter_id: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:21:37,866 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:21:37,873 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9bd86e66-886f-4e36-bf3d-29a755a8053a
2026-01-26 17:21:37,877 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
2026-01-26 17:21:37,890 - app.api.v1.ai - INFO - [预加载] 当前章节已加载: 19c51863-a5d0-40a9-b891-f6124d9446f0
2026-01-26 17:21:37,899 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
2026-01-26 17:21:37,903 - app.api.v1.ai - INFO - [预加载] 前一章节已加载: 9bd86e66-886f-4e36-bf3d-29a755a8053a
2026-01-26 17:21:37,908 - app.api.v1.ai - INFO - [预加载] 完成: {'guidelines': False, 'current_chapter': True, 'previous_chapter': True}
INFO:     127.0.0.1:62717 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:21:37,930 - app.api.middleware.monitoring_middleware - INFO - API请求完成: POST /api/v1/ai/preload-metadata
INFO:     127.0.0.1:59611 - "POST /api/v1/ai/preload-metadata HTTP/1.1" 200 OK
2026-01-26 17:21:38,127 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a
INFO:     127.0.0.1:59598 - "GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a HTTP/1.1" 200 OK
2026-01-26 17:21:38,196 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
INFO:     127.0.0.1:59599 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 17:21:38,331 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions
2026-01-26 17:21:38,341 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a
INFO:     127.0.0.1:59600 - "GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions?status=pending HTTP/1.1" 200 OK
INFO:     127.0.0.1:51774 - "GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a HTTP/1.1" 200 OK
2026-01-26 17:21:38,422 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status
INFO:     127.0.0.1:58171 - "GET /api/v1/analysis/works/7414c983-ce5d-4d9e-a503-01ce30ae2b26/status HTTP/1.1" 404 Not Found
2026-01-26 17:21:38,536 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:38,541 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a
2026-01-26 17:21:38,543 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:54133 - "GET /api/v1/agent/operations/11ff5b2e-4522-4ffd-a89a-504161817f1a HTTP/1.1" 200 OK
INFO:     127.0.0.1:59595 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:21:38,551 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:21:38,555 - app.api.middleware.monitoring_middleware - INFO - API请求完成: GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions
INFO:     127.0.0.1:60694 - "GET /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0/revisions?status=pending HTTP/1.1" 200 OK
2026-01-26 17:21:41,579 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)
2026-01-26 17:21:41,638 - app.api.v1.chapters - INFO - 🗑️ [Chapters] 缓存已失效: chapters:work:7414c983-ce5d-4d9e-a503-01ce30ae2b26
2026-01-26 17:21:41,640 - app.api.middleware.monitoring_middleware - INFO - API请求完成: PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0
INFO:     127.0.0.1:49563 - "PUT /api/v1/chapters/19c51863-a5d0-40a9-b891-f6124d9446f0 HTTP/1.1" 200 OK
2026-01-26 17:21:41,642 - app.services.chapter_vector_service - INFO - Vectorizing chapter: 第5章 太一门 (order=5)
2026-01-26 17:21:44,245 - app.services.chapter_vector_service - INFO - Stored chapter vectors: 第5章 太一门 (70 paragraphs)