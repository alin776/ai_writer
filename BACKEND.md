INFO:     127.0.0.1:62183 - "OPTIONS /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:52:30 app.services.ai.prompts INFO   Prompts loaded successfully from D:\Java\ai_writer\backend\app\services\ai\prompts\default.json
09:52:30 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:52:30 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:52:30 app.services.agent.cost_tracker INFO   CostTracker 初始化完成, 持久化: False
09:52:30 app.services.ai.http_ai_service INFO   CostTracker 已启用
09:52:32 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:52:32 app.api.v1.agent INFO   [Chat Stream] Mode: planning
09:52:32 app.api.middleware.monitoring_middleware INFO   API请求完成: POST /api/v1/agent/chat/stream
INFO:     127.0.0.1:62183 - "POST /api/v1/agent/chat/stream HTTP/1.1" 200 OK
09:52:53 app.core.redis INFO   ✅ Redis connected: redis://localhost:6379/0
09:52:53 app.api.v1.agent INFO   [Session] 创建新会话归属: e2749af6-6c3d-405d-9d49-4045ffb5b7b3 -> 602f5147-846a-4cde-95d3-405fa75f133f
09:52:53 app.api.v1.agent INFO   [LangGraph Agent Stream] ⏱️ 请求开始 - User: 602f5147-846a-4cde-95d3-405fa75f133f, Mode: planning, Message: 小说的第 28章讲了什么？有什么亮点？...
09:52:53 app.services.agent.model_selector INFO   ModelSelector 初始化完成, 成本优化: True, 模型层级: 3
09:52:53 app.services.ai.http_ai_service INFO   ModelSelector 已启用
09:52:53 app.services.ai.http_ai_service INFO   CostTracker 已启用
09:52:54 app.services.ai.http_ai_service INFO   HTTP AI Service 初始化成功，Base URL: https://204992.xyz/v1, Model: gemini-2.5-pro, Timeout: 120s, HTTP/2: Enabled (多路复用), ModelSelector: True, CostTracking: True
09:52:54 chromadb.telemetry.product.posthog INFO   Anonymized telemetry enabled. See                     https://docs.trychroma.com/telemetry for more information.
09:52:54 sentence_transformers.SentenceTransformer INFO   Load pretrained SentenceTransformer: paraphrase-multilingual-MiniLM-L12-v2
09:53:01 app.services.context.vector_memory_store INFO   ✅ VectorMemoryStore初始化成功 | 目录=./data/chroma_db | 模型=paraphrase-multilingual-MiniLM-L12-v2 | 集合=user_memories
09:53:01 app.services.context.manager INFO   ✅ VectorMemoryStore 已初始化
09:53:01 app.services.context.manager INFO   ✅ ContextManager: 长期记忆已启用 (user_id=None)
09:53:01 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ ContextManager已初始化（长期记忆已启用）
成功加载模板: intent_classifier (版本 2.0.0)
成功加载模板: writing_agent (版本 2.0.0)
成功加载模板: planning_agent (版本 2.0.0)
成功加载模板: tool_agent (版本 2.0.0)
成功加载模板: query_agent (版本 2.0.0)
09:53:02 app.services.agent.langgraph_agent INFO   [LangGraph] ✅ PromptManager已初始化
09:53:02 app.services.agent.langgraph_agent INFO   [LangGraph] 使用 ChatOpenAI 模式（原生工具调用）
09:53:03 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] 已初始化
09:53:03 app.services.agent.langgraph_agent INFO   [LangGraph] 已创建MonitoringCallbackHandler
09:53:24 app.services.agent.langgraph_agent INFO   [LangGraph] OK 使用 AsyncRedisSaver（redis://localhost:6379/0，TTL=7天）
09:53:24 app.api.v1.agent INFO   [Global Agent] 创建全局Agent实例，MemorySaver将在请求间共享
09:53:45 app.services.agent.langgraph_agent INFO   [Planning] 开始规划: 小说的第 28章讲了什么？有什么亮点？...
09:54:02 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/1.1 200 OK"
09:54:02 app.api.callbacks.monitoring_callback INFO   [MonitoringCallback] LLM调用成功: run_id=3e56c572-3f53-4d13-bc7d-19f0302ec368, model=gemini-2.5-pro, duration=16.12s, tokens=2695 (prompt=2394, completion=301)
09:54:02 app.services.agent.langgraph_agent INFO   [_generate_text] 使用ChatOpenAI生成文本，tokens=2695
09:54:02 app.services.agent.langgraph_agent INFO   [JSON解析] 方法2成功: 从```json块提取
09:54:02 app.services.agent.langgraph_agent INFO   [Planning] 规划生成成功，共3个任务，耗时: 16.12s
09:54:02 app.api.v1.agent INFO   [Stream] 规划生成: 3 个任务
09:54:02 app.services.agent.langgraph_agent INFO   [Execution] 开始智能并行执行任务
09:54:02 app.services.agent.parameter_resolver INFO   [ParameterResolver] 初始化完成, 严格模式: False
09:54:02 app.services.agent.langgraph_agent INFO   [ParameterResolver] 参数解析器已启用
09:54:02 app.services.agent.langgraph_agent INFO   [ParallelExecution] 任务分组: 并行=1, 串行=2
09:54:02 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始并行执行1个任务
09:54:02 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1开始: 根据用户请求，使用工具获取第28章的章节内容
09:54:02 app.api.v1.agent INFO   [Stream] 任务开始: 根据用户请求，使用工具获取第28章的章节内容
09:54:02 app.services.agent.langgraph_agent INFO   [get_chapter_by_order_tool] 找到第28章: 第28章 九州八宗
09:54:02 app.services.agent.langgraph_agent INFO   [ParallelExecution] 并行任务1完成
09:54:02 app.api.v1.agent INFO   [Stream] 任务完成: 根据用户请求，使用工具获取第28章的章节内容 (0.0s)
09:54:02 app.services.agent.langgraph_agent INFO   [ParallelExecution] 开始串行执行2个任务
09:54:02 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2开始: 分析第28章的故事情节，生成内容总结
09:54:02 app.api.v1.agent INFO   [Stream] 任务开始: 分析第28章的故事情节，生成内容总结
D:\Java\ai_writer\backend\venv\Lib\site-packages\jieba\_compat.py:18: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  import pkg_resources
09:54:02 app.prompts.constraint_manager INFO   ✅ 已加载模板: analyze_text (v2.0.0)
09:54:02 app.prompts.constraint_manager INFO   ✅ 已加载模板: intent_classifier (v2.0.0)
09:54:02 app.prompts.constraint_manager INFO   ✅ 已加载模板: planning_agent (v2.0.0)
09:54:02 app.prompts.constraint_manager INFO   ✅ 已加载模板: query_agent (v2.0.0)
09:54:02 app.prompts.constraint_manager INFO   ✅ 已加载模板: tool_agent (v2.0.0)
09:54:02 app.prompts.constraint_manager INFO   ✅ 已加载模板: writing_agent (v2.0.0)
09:54:02 app.prompts.constraint_manager INFO   ✅ 约束提示词管理器已初始化: 加载6个模板, 注册3个验证器
09:54:02 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:54:02 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
09:54:02 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.1, task_type=TaskType.SUMMARIZATION
09:54:05 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
09:54:05 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:54:34 app.services.ai.http_ai_service INFO   API 响应完成，共接收 53 个数据块，总长度: 3726
09:54:34 app.services.ai.http_ai_service INFO   流式响应Token统计: 9775 (prompt=7213, completion=2562)
09:54:34 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 7213+2562=9775, cost: $0.000524
09:54:34 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=7213+2562, cost=$0.000524, time=32.21s
Building prefix dict from the default dictionary ...
09:54:34 jieba DEBUG   Building prefix dict from the default dictionary ...
Loading model from cache D:\Temp\jieba.cache
09:54:34 jieba DEBUG   Loading model from cache D:\Temp\jieba.cache
Loading model cost 0.596 seconds.
09:54:35 jieba DEBUG   Loading model cost 0.596 seconds.
Prefix dict has been built successfully.
09:54:35 jieba DEBUG   Prefix dict has been built successfully.
09:54:35 app.services.agent.langgraph_agent WARNING   ⚠️ AI输出验证失败: [{'constraint': '只能分析提供的文本内容，不得添加任何文本中不存在的信息', 'validation_func': 'validate_entities', 'result': {'valid': False, 'error': 'AI可能编造了以下实体', 'fabricated_entities': ['三天修炼', '三趟套路', '世界观', '两州之地', '了解此界', '以及次日', '众抽出刀', '但作为小', '修炼内功', '内功突破', '内息操控', '内息配合', '力滋养下', '勤奋刻苦', '原主', '发萧宗庭', '同时', '和书本中', '和对世界', '咳嗽不止', '围绕段融', '在萧宗庭', '埋下伏笔', '基于提供', '基本格局', '夜间', '套路', '宗门格局', '容分析报', '察力敏锐', '对世界', '对武', '对萧宗庭', '小高潮', '局演武场', '并在次日', '并对武技', '并被段融', '异于常人', '强了阅读', '得了显著', '惊人成就', '感到震惊', '戏剧性', '所处世界', '晚饭后', '智慧', '有了全新', '有所提升', '本分析报', '本段文本', '杀人', '核心理念', '桩一整天', '武侠', '武侠世界', '武道', '武道修炼', '武道理念', '段融一天', '深刻理解', '热气如雾', '特殊药材', '现了主角', '的书籍', '的刀法', '的困难', '的宗门', '的格局', '的武', '的真谛', '的设定', '的身份', '的辅助', '的阅读', '看出孔斌', '眼神', '策略博弈', '继续训练', '考核表现', '联系起来', '自己所在', '般的武', '认知展开', '说片段', '逐渐壮大', '通过段融', '速度极快', '造了主角', '道天赋', '间内取得', '隐藏实力', '高潮'], 'source_entities': ['一上手', '一个僻静', '一个周天', '一个时辰', '一动未动', '一天桩功', '一定境界', '一家独大', '一气贯通', '一眼孔斌'], 'output_entities': ['一上手', '一个僻静', '一个周天', '一气贯通', '三天修炼', '三日后', '三趟套路', '上品', '不如段融', '世界观'], 'confidence': 0.43, 'recommendation': '重新生成或人工审查'}}, {'constraint': '不得编造角色、情节、对话或任何文本中未出现的内容', 'validation_func': 'validate_fabrication', 'result': {'valid': False, 'error': 'AI可能编造了以下实体', 'fabricated_entities': ['三天修炼', '三趟套路', '世界观', '两州之地', '了解此界', '以及次日', '众抽出刀', '但作为小', '修炼内功', '内功突破', '内息操控', '内息配合', '力滋养下', '勤奋刻苦', '原主', '发萧宗庭', '同时', '和书本中', '和对世界', '咳嗽不止', '围绕段融', '在萧宗庭', '埋下伏笔', '基于提供', '基本格局', '夜间', '套路', '宗门格局', '容分析报', '察力敏锐', '对世界', '对武', '对萧宗庭', '小高潮', '局演武场', '并在次日', '并对武技', '并被段融', '异于常人', '强了阅读', '得了显著', '惊人成就', '感到震惊', '戏剧性', '所处世界', '晚饭后', '智慧', '有了全新', '有所提升', '本分析报', '本段文本', '杀人', '核心理念', '桩一整天', '武侠', '武侠世界', '武道', '武道修炼', '武道理念', '段融一天', '深刻理解', '热气如雾', '特殊药材', '现了主角', '的书籍', '的刀法', '的困难', '的宗门', '的格局', '的武', '的真谛', '的设定', '的身份', '的辅助', '的阅读', '看出孔斌', '眼神', '策略博弈', '继续训练', '考核表现', '联系起来', '自己所在', '般的武', '认知展开', '说片段', '逐渐壮大', '通过段融', '速度极快', '造了主角', '道天赋', '间内取得', '隐藏实力', '高潮'], 'source_entities': ['一上手', '一个僻静', '一个周天', '一个时辰', '一动未动', '一天桩功', '一定境界', '一家独大', '一气贯通', '一眼孔斌'], 'output_entities': ['一上手', '一个僻静', '一个周天', '一气贯通', '三天修炼', '三日后', '三趟套路', '上品', '不如段融', '世界观'], 'confidence': 0.43, 'recommendation': '重新生成或人工审查'}}, {'constraint': '分析时必须引用原文作为证据支持', 'validation_func': 'validate_citations', 'result': {'valid': False, 'error': 'AI输出缺少原文引用', 'recommendation': '要求AI在分析时引用原文', 'citations_found': 0}}]
09:54:35 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务2完成
09:54:35 app.api.v1.agent INFO   [Stream] 任务完成: 分析第28章的故事情节，生成内容总结 (0.0s)
09:54:35 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3开始: 在情节总结的基础上，提炼并分析第28章的亮点
09:54:35 app.api.v1.agent INFO   [Stream] 任务开始: 在情节总结的基础上，提炼并分析第28章的亮点
09:54:35 app.services.agent.model_selector INFO   [ModelSelector] 任务复杂度: medium
09:54:35 app.services.ai.http_ai_service INFO   [ModelSelector] 任务=summarization, 模型=gemini-2.5-flash, 原因=任务复杂度为 medium; 任务类型: summarization; 选择 Gemini 2.5 Flash (质量评分: 8.0/10, 成本: $0.075/$0.3 per 1M tokens)
09:54:35 app.services.ai.http_ai_service INFO   开始调用 AI API: model=gemini-2.5-flash, max_tokens=1500, temp=0.1, task_type=TaskType.SUMMARIZATION
09:54:37 httpx INFO   HTTP Request: POST https://204992.xyz/v1/chat/completions "HTTP/2 200 OK"
09:54:37 app.services.ai.http_ai_service INFO   API 流式响应已建立，开始接收数据...
09:54:48 app.services.ai.http_ai_service INFO   API 响应完成，共接收 27 个数据块，总长度: 2517
09:54:48 app.services.ai.http_ai_service INFO   流式响应Token统计: 4684 (prompt=2958, completion=1726)
09:54:48 app.services.agent.cost_tracker INFO   [CostTracker] 记录API调用: gemini-2.5-pro, tokens: 2958+1726=4684, cost: $0.000296
09:54:48 app.services.ai.http_ai_service INFO   [CostTracker] API调用已记录: tokens=2958+1726, cost=$0.000296, time=13.23s
09:54:49 app.services.agent.langgraph_agent WARNING   ⚠️ AI输出验证失败: [{'constraint': '只能分析提供的文本内容，不得添加任何文本中不存在的信息', 'validation_func': 'validate_entities', 'result': {'valid': False, 'error': 'AI可能编造了以下实体', 'fabricated_entities': ['一种高明', '为小', '争霸模式', '人事件后', '以更积极', '修炼内功', '入门', '其中包含', '内功修炼', '内息发力', '内息贯通', '前世国术', '功修炼上', '勤奋刻苦', '升了文本', '半时间内', '受萧宗庭', '同于常见', '同时', '吸引读者', '和复杂性', '在萧宗庭', '在镖局内', '基于提供', '天赋', '天赋异禀', '宗门格局', '容分析报', '对段融', '建了清晰', '张扬', '强了阅读', '得到提升', '心理素质', '快速入门', '息发力时', '所处世界', '招式内涵', '招式存在', '提供了小', '文本内容', '是青阳门', '智慧', '更加立体', '有更惊人', '本报', '武学中', '武学体系', '武学修炼', '武学本质', '武打描写', '求知欲强', '深度', '添了独特', '独特', '现出惊人', '用血鹿茸', '的刀法', '的困难', '的天赋', '的意义', '的成果', '的理解', '的画面感', '的考究中', '的联想', '的解释', '的设定', '相辅相成', '种心理上', '精妙设计', '素质强大', '索与主角', '练习刀法', '细节描写', '经验丰富', '结合内息', '自身天赋', '解力深刻', '说内', '越了简单', '辅助修炼', '迅速壮大', '运转内息', '这一现实', '这些生动', '通过段融', '重要亮点', '长和转变', '阅读书籍', '隐藏锋芒', '霸主地位', '非花架子', '面对未来', '高明'], 'source_entities': ['一上手', '一个僻静', '一个周天', '一个时辰', '一动未动', '一天桩功', '一定境界', '一家独大', '一气贯通', '一眼孔斌'], 'output_entities': ['一上手', '一个周天', '一种高明', '两个时辰', '个演武场', '中喷出一', '为小', '为花架子', '九州', '九州八宗'], 'confidence': 0.58, 'recommendation': '重新生成或人工审查'}}, {'constraint': '不得编造角色、情节、对话或任何文本中未出现的内容', 'validation_func': 'validate_fabrication', 'result': {'valid': False, 'error': 'AI可能编造了以下实体', 'fabricated_entities': ['一种高明', '为小', '争霸模式', '人事件后', '以更积极', '修炼内功', '入门', '其中包含', '内功修炼', '内息发力', '内息贯通', '前世国术', '功修炼上', '勤奋刻苦', '升了文本', '半时间内', '受萧宗庭', '同于常见', '同时', '吸引读者', '和复杂性', '在萧宗庭', '在镖局内', '基于提供', '天赋', '天赋异禀', '宗门格局', '容分析报', '对段融', '建了清晰', '张扬', '强了阅读', '得到提升', '心理素质', '快速入门', '息发力时', '所处世界', '招式内涵', '招式存在', '提供了小', '文本内容', '是青阳门', '智慧', '更加立体', '有更惊人', '本报', '武学中', '武学体系', '武学修炼', '武学本质', '武打描写', '求知欲强', '深度', '添了独特', '独特', '现出惊人', '用血鹿茸', '的刀法', '的困难', '的天赋', '的意义', '的成果', '的理解', '的画面感', '的考究中', '的联想', '的解释', '的设定', '相辅相成', '种心理上', '精妙设计', '素质强大', '索与主角', '练习刀法', '细节描写', '经验丰富', '结合内息', '自身天赋', '解力深刻', '说内', '越了简单', '辅助修炼', '迅速壮大', '运转内息', '这一现实', '这些生动', '通过段融', '重要亮点', '长和转变', '阅读书籍', '隐藏锋芒', '霸主地位', '非花架子', '面对未来', '高明'], 'source_entities': ['一上手', '一个僻静', '一个周天', '一个时辰', '一动未动', '一天桩功', '一定境界', '一家独大', '一气贯通', '一眼孔斌'], 'output_entities': ['一上手', '一个周天', '一种高明', '两个时辰', '个演武场', '中喷出一', '为小', '为花架子', '九州', '九州八宗'], 'confidence': 0.58, 'recommendation': '重新生成或人工审查'}}, {'constraint': '分析时必须引用原文作为证据支持', 'validation_func': 'validate_citations', 'result': {'valid': False, 'error': 'AI输出缺少原文引用', 'recommendation': '要求AI在分析时引用原文', 'citations_found': 0}}]
09:54:49 app.services.agent.langgraph_agent INFO   [ParallelExecution] 串行任务3完成
09:54:49 app.api.v1.agent INFO   [Stream] 任务完成: 在情节总结的基础上，提炼并分析第28章的亮点 (0.0s)
09:54:49 app.services.agent.langgraph_agent INFO   [Execution] 所有任务执行完成，共3个任务，耗时: 47.20s
09:54:49 app.services.agent.langgraph_agent INFO   [Response] 生成最终响应
09:54:49 app.services.agent.langgraph_agent INFO   [TaskClassify] 任务分类: 输入型=1, 输出型=2
09:54:49 app.services.agent.langgraph_agent INFO   [Response] 2个输出任务，简单拼接
09:54:49 app.api.v1.agent INFO   [LangGraph Agent Stream] User 602f5147-846a-4cde-95d3-405fa75f133f - Mode: planning, Stream completed
