"""
Prompt 缓存模块 - Phase 2.6

功能：
- 缓存静态 Prompt 部分，避免重复构建
- 利用 Redis 实现分布式缓存
- 支持 OpenAI Prompt Caching（如果 API 支持）

收益：
- 减少 Prompt 构建时间（5ms → 0.1ms）
- 节省 Token 费用（如果 API 支持服务端缓存）
- 提升系统响应速度

版本管理：
- 每次修改 Prompt 内容时，请更新 PROMPT_VERSION
- 部署时会自动使用新版本的缓存 key
"""

from app.core.cache import cache_review

# Prompt 版本号 - 修改 Prompt 时请更新此版本号
PROMPT_VERSION = "v2.12.0"  # 2025-12-14: 修正工具选择逻辑 - "设计"/"规划"类任务使用 continue_writing_tool 而非 analyze_text_tool


# ════════════════════════════════════════════════════════════════
# 共享工具描述 - 单一数据源，避免多个 Prompt 不同步
# ════════════════════════════════════════════════════════════════

def _get_retrieval_tools_section() -> str:
    """检索工具描述 - 统一数据源

    被 get_tool_decision_static_prompt 和 get_planning_static_prompt 共同引用，
    确保工具列表和使用场景说明保持同步。

    注意：只描述 LANGGRAPH_TOOLS 中实际存在的工具！
    """
    return """
【检索工具 - 内容搜索场景使用】
- search_analysis_fragments_tool: 混合检索（向量+全文）召回作品相关片段
  参数: query(必需), top_k(默认5), work_id(可选), chapter_id(可选)
  → 适用场景:
    - 用户给出具体文字片段但不知道在哪章: "微光如露落雪在哪"
    - 搜索包含某关键词的内容: "哪里提到了XX"、"找一下XX相关的内容"
    - 查找人物/地点/设定相关描述: "赵穆出现在哪"、"关于源顺镖局的描述"
    - ⚠️ 用户提到人物名但未指定章节: "帮我改写赵穆的描写" → 先搜索赵穆出现位置

⚠️ 【检索规则 - 强制执行】
- 用户提到具体文字/关键词但不知位置 → 必须先调用 search_analysis_fragments_tool
- 用户问"XX在哪"/"哪里提到XX" → 必须先调用 search_analysis_fragments_tool
- ⚠️ 用户提到人物名（如"赵穆"）但未说在哪章 → 必须先调用 search_analysis_fragments_tool 定位
- **禁止不检索就直接回答"没有找到"或"不存在"！必须先检索确认！**
- **禁止直接读取"当前章节"然后说"XX未出现"！必须先检索确认XX在哪些章节！**
"""


@cache_review(expire=3600, key_prefix=f"prompt:tool_decision:{PROMPT_VERSION}")
async def get_tool_decision_static_prompt() -> str:
    """获取工具决策的静态 Prompt 部分（可缓存 1 小时）

    Returns:
        str: 静态 Prompt 文本（约 150 tokens）

    说明：
        这部分 Prompt 包含工具列表、JSON 格式说明和示例，
        对所有请求都相同，因此可以安全缓存。

    🔧 2025-12-12: 引用共享的检索工具描述，确保与规划 Prompt 同步
    """
    retrieval_tools = _get_retrieval_tools_section()

    return f"""判断是否需要工具。可用工具:

【编辑器工具 - 修改内容时优先使用】
- smart_rewrite: 改写/修改章节内容
  参数: chapter_id, text_to_rewrite, user_requirement, base_version
- smart_continue: 续写章节 (参数: chapter_id, context)
- smart_insert: 插入内容 (参数: chapter_id, position, content)
- apply_chapter_edit: 直接应用编辑 (参数: chapter_id, operation, content)

【读取工具】
需work_id: get_chapter_by_order_tool, get_context_tool, read_chapter_tool
不需work_id: continue_writing_tool, analyze_text_tool
{retrieval_tools}
⚠️ **重要变更**：polish_text_tool 已移除
- 所有润色/修改请求必须提供 chapter_id，使用基于章节上下文的工具
- 如果涉及多个章节，read_chapter_tool 支持传递多个 chapter_id（用逗号分隔，如 "id1,id2,id3"）

⚠️ 【关键规则】用户提到具体文字但未说章节时：
- 用户只给了句子（如"微光如露落雪太书面化"），但没说是第几章
- → **必须先调用 search_analysis_fragments_tool 搜索这句话，找到它在第几章**
- → 示例：{{"need_tools": true, "tool_name": "search_analysis_fragments_tool", "tool_args": {{"query": "微光如露落雪"}}}}
- → **禁止直接给出修改建议！必须先定位！**

⚠️ 【搜索兜底规则】：
- 如果用户提供的文字**过于简短**（少于3个字）或是**通用描述**（如"这一章"、"这段话"、"这里"）
- → **不要调用搜索工具**，直接返回：
  {{"need_tools": false, "direct_response": "请问您指的是哪一章？或者能否提供更多原文片段帮助我定位？"}}
- 示例：
  "这段话太平淡" → {{"need_tools": false, "direct_response": "请问您指的是哪一章的哪段话？..."}}
  "这里改改" → {{"need_tools": false, "direct_response": "请问您指的是哪一章？..."}}

⚠️ smart_rewrite 参数提取规则：
1. user_requirement（用户要求）：
   - "加强情感描写" → user_requirement="加强情感描写"
   - "更简洁一些" → user_requirement="更简洁"
   - "太平淡了" → user_requirement="更有画面感"
   - "更有张力" → user_requirement="更有张力"

2. base_version（基准版本）- 用户要在某版本基础上改时：
   - "在第一版基础上改" → base_version="第一版" 或 "版本A" 或 "1"
   - "在第二版基础上改" → base_version="第二版" 或 "版本B" 或 "2"
   - "在第三版基础上改" → base_version="第三版" 或 "版本C" 或 "3"
   注意：系统会智能识别各种版本表达方式，无需使用特定格式

3. 用户直接给出最终版本时（不要再生成）：
   - 用户说"就按这个改"/"直接用这个"并给出内容 → 用apply_chapter_edit直接应用

⚠️ 重要规则：
1. 用户提到具体文字但未说章节 → **先用 search_analysis_fragments_tool 定位**
2. 用户说"修改第X章"、"改写第X章" → 使用 smart_rewrite（已知章节）
3. 用户说"续写"、"继续写" → 使用 smart_continue
4. 用户说"插入" → 使用 smart_insert
5. 简单问候/寒暄（如"你好"、"在吗"、"谢谢"）→ 不需要工具，直接回复
6. 必须严格返回JSON格式！

返回JSON:
- 需要: {{"need_tools": true, "tool_name": "工具名", "tool_args": {{}}}}
- 缺参数: {{"need_tools": false, "direct_response": "请提供..."}}
- 直接答: {{"need_tools": false, "direct_response": "..."}}
- 问候: {{"need_tools": false, "direct_response": "您好！我是AI写作助手，可以帮您修改、续写章节内容。请问有什么可以帮您的？"}}

示例:
"你好" → {{"need_tools": false, "direct_response": "您好！我是AI写作助手..."}}
"微光如露落雪太书面化" → {{"need_tools": true, "tool_name": "search_analysis_fragments_tool", "tool_args": {{"query": "微光如露落雪"}}}}
"白光退去太平淡" → {{"need_tools": true, "tool_name": "search_analysis_fragments_tool", "tool_args": {{"query": "白光退去"}}}}
"修改第三章，白光退去太平淡" → {{"need_tools": true, "tool_name": "smart_rewrite", "tool_args": {{"chapter_id": "xxx", "text_to_rewrite": "白光退去...", "user_requirement": "更有画面感"}}}}
"有没有叫赵穆的人物" → {{"need_tools": true, "tool_name": "search_analysis_fragments_tool", "tool_args": {{"query": "赵穆"}}}}
"哪个章节讲到了浑圆桩" → {{"need_tools": true, "tool_name": "search_analysis_fragments_tool", "tool_args": {{"query": "浑圆桩"}}}}
"段融是谁" → {{"need_tools": true, "tool_name": "search_analysis_fragments_tool", "tool_args": {{"query": "段融"}}}}

⚠️ 请严格返回JSON格式，不要直接回答问题:"""


@cache_review(expire=3600, key_prefix=f"prompt:planning:{PROMPT_VERSION}")
async def get_planning_static_prompt() -> str:
    """获取 Planning 的静态 Prompt 部分（可缓存 1 小时）

    Returns:
        str: 静态 Prompt 文本

    说明：
        这部分 Prompt 包含任务类型识别规则和示例。

    🔧 2025-12-02: P3根源修复 - 区分JSON工具和纯文本工具的占位符用法
    🔧 2025-12-06: P1优化 - 增强多章节分析+续写场景的指导
    🔧 2025-12-07: 架构优化 - 引入意图路由，写作任务直接交给 Multi-Agent
    🔧 2025-12-07: 重构 - Chain-of-Thought 思维链，教 AI 如何思考而非匹配关键词
    🔧 2025-12-12: 引用共享的检索工具描述，确保与工具决策 Prompt 同步
    """
    retrieval_tools = _get_retrieval_tools_section()

    # 使用字符串拼接而非 f-string，避免转义大量 JSON 大括号
    part1 = """你是一个任务规划助手。请使用【三步思维链】来理解用户意图并生成任务。

【三步思维链】- 生成任务前必须完成

## Step 1: 输出形式分析（最重要！）

问自己：用户期望看到什么样的输出？

可能的输出形式：
- 原文内容（直接返回，不加工）
- 概括/摘要（需要阅读后总结提炼）
- 分析报告（需要深度分析某个维度）
- 大纲/规划（需要设计结构，但不是写正文）
- 创作内容（需要写新的正文/章节）

## Step 2: 原料分析

问自己：生成这个输出需要什么原料？

- 需要哪些章节的内容？
- 需要人设/大纲等元数据吗？

## Step 3: 处理方式

问自己：需要对原料做什么处理？

- 直接返回（无处理）→ 只用获取工具
- 概括/分析现有内容 → 获取 + analyze_text_tool
- 创作新内容（包括大纲/规划/设定）→ continue_writing_tool

【关键判断】

大纲 vs 正文：
- 创作大纲/规划 → continue_writing_tool（大纲是创作，需要从零生成内容！）
- 续写正文 → continue_writing_tool
- 分析现有大纲/内容 → analyze_text_tool

概括 vs 原文：
- 用户想了解内容（"讲了什么"、"是什么故事"、"主要内容"）→ 需要概括
- 用户想获取内容（"给我"、"获取"、"发给我"、"看一下"）→ 直接返回

复合任务：
- 用户说"先做A再做B" → 分解为独立任务，按顺序排列

【可用工具】

获取原料：
- get_chapter_by_order_tool: 按序号获取章节（支持批量！）
  参数: chapter_order，支持三种格式：
    - 单个: "1"
    - 多个: "1,2,3,4,5"
    - 范围: "1-5"（一次性读取第1到第5章）
  ⚠️ 返回数据已包含: {title, order, content, word_count} → 标题/序号等元数据无需再分析！
  ⚠️ 需要读取多章时，用范围格式 "1-5" 一次读取，避免生成多个读取任务！
- get_context_tool: 获取作品上下文
"""

    part2 = """处理原料：
- analyze_text_tool: 分析已有文本 (参数: text, focus)
  - 适用于：概括内容、分析人物、分析情节、评估文本质量
  - ⚠️ 只能分析现有内容，不能创作新内容（如大纲、设定等）
  - ⚠️ 不要用于：查询标题/序号等元数据（工具已返回这些字段）

文本润色/改写：
- analyze_text_tool: 分析并给出修改建议 (参数: text, focus)
  - 适用于：用户选中文本后要求修改、润色、分析、改写
  - ⚠️ 当【用户选中的文本】存在时，必须将选中文本作为 text 参数！
  - focus 参数示例："给出润色建议"、"分析问题并改写"、"使其更有画面感"
  - style 可选值: professional, creative, concise, elaborate

创作内容：
- continue_writing_tool: 创作新内容（包括大纲、正文、设定等）
  - 适用于：续写章节、创作正文、生成大纲、设计角色成长、规划情节
  - params: context（上下文）, requirements（要求）
  - ⚠️ "设计"/"规划"/"构思"/"创作"都是创作任务，使用这个工具

【选中文本处理规则】⚠️ 重要！

当 Prompt 中包含【用户选中的文本】时，这表示用户在编辑器中选中了一段文字：
1. **必须先读取章节内容**（如果有 chapter_id）：调用 read_chapter_tool
2. 然后使用 analyze_text_tool 分析选中的文本
3. 将选中的文本作为 analyze_text_tool 的 text 参数
4. 根据用户指令确定 focus 参数：
   - "更丰富/丰富一些" → focus="分析并给出更丰富的改写建议"
   - "更简洁/精简" → focus="分析并给出更简洁的改写建议"
   - "更有文采/更优美" → focus="分析并给出更有文采的改写建议"
   - "有什么问题" → focus="分析文本问题并给出改进建议"

【输出格式】

{
  "thinking": {
    "step1_output": "用户期望的输出形式",
    "step2_material": "需要的原料",
    "step3_process": "处理方式"
  },
  "user_intent": "一句话描述",
  "response_hint": "可选，元数据查询时指定返回字段：title/word_count/title_and_word_count/content",
  "tasks": [...]
}

【示例】

用户: "第三章讲了什么"
{
  "thinking": {
    "step1_output": "用户想看到概括性文字，了解第三章主要内容，不是要原文",
    "step2_material": "需要第三章原文",
    "step3_process": "获取后进行概括总结"
  },
  "user_intent": "概括第三章内容",
  "tasks": [
    {"task_id": 1, "description": "获取第三章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}},
    {"task_id": 2, "description": "概括内容", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "概括这一章的主要内容：核心事件、涉及人物、情节发展"}}
  ]
}

用户: "获取第三章"
{
  "thinking": {
    "step1_output": "用户想直接看到第三章原文",
    "step2_material": "需要第三章原文",
    "step3_process": "直接返回，无需处理"
  },
  "user_intent": "获取第三章原文",
  "tasks": [
    {"task_id": 1, "description": "获取第三章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}}
  ]
}

用户: "第五章的标题是什么"
{
  "thinking": {
    "step1_output": "用户想知道第五章的标题（元数据查询）",
    "step2_material": "需要第五章的元数据",
    "step3_process": "get_chapter_by_order_tool 返回的数据已包含 title 字段，直接返回即可"
  },
  "user_intent": "查询第五章标题",
  "response_hint": "title",
  "tasks": [
    {"task_id": 1, "description": "获取第五章信息", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 5}}
  ]
}

用户: "第三章有多少字"
{
  "thinking": {
    "step1_output": "用户想知道第三章的字数（元数据查询）",
    "step2_material": "需要第三章的元数据",
    "step3_process": "get_chapter_by_order_tool 返回的数据已包含 word_count 字段，直接返回即可"
  },
  "user_intent": "查询第三章字数",
  "response_hint": "word_count",
  "tasks": [
    {"task_id": 1, "description": "获取第三章信息", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}}
  ]
}

用户: "根据前四章写后5章的大纲"
{
  "thinking": {
    "step1_output": "用户想看到第5-9章的大纲规划（章节标题+主要剧情），不是正文",
    "step2_material": "需要前四章内容作为参考",
    "step3_process": "获取前文后创作大纲结构（大纲是创作！）"
  },
  "user_intent": "创作第5-9章大纲",
  "tasks": [
    {"task_id": 1, "description": "批量获取前四章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": "1-4"}},
    {"task_id": 2, "description": "创作大纲", "tool": "continue_writing_tool", "params": {"context": "$TASK_1.chapters$", "requirements": "基于前四章的人物、情节、伏笔，为第5-9章设计详细大纲：章节标题、主要剧情、涉及角色、伏笔设置"}}
  ]
}

用户: "续写第五章"
{
  "thinking": {
    "step1_output": "用户想看到完整的第五章正文，是实际的故事叙述",
    "step2_material": "需要前文内容作为续写参考",
    "step3_process": "获取前文后续写"
  },
  "user_intent": "续写第五章正文",
  "tasks": [
    {"task_id": 1, "description": "获取第四章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 4}},
    {"task_id": 2, "description": "续写第五章", "tool": "continue_writing_tool", "params": {"context": "$TASK_1.content$", "requirements": "承接上一章内容续写第五章"}}
  ]
}

用户: "分析前四章，然后写后5章大纲，再续写第五章"
{
  "thinking": {
    "step1_output": "复合任务：1)分析报告 2)大纲规划 3)章节正文",
    "step2_material": "需要前四章内容",
    "step3_process": "分三阶段：分析现有内容→创作大纲→续写正文"
  },
  "user_intent": "分析+创作大纲+续写",
  "tasks": [
    {"task_id": 1, "description": "批量获取前四章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": "1-4"}},
    {"task_id": 2, "description": "分析前四章", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.chapters$", "focus": "分析前四章：主要人物、情节发展、伏笔线索、写作风格"}},
    {"task_id": 3, "description": "创作第5-9章大纲", "tool": "continue_writing_tool", "params": {"context": "$TASK_2$", "requirements": "基于分析结果，为第5-9章设计详细大纲"}},
    {"task_id": 4, "description": "续写第五章", "tool": "continue_writing_tool", "params": {"context": "$TASK_1.chapters[3].content$\\n\\n大纲：$TASK_3$", "requirements": "基于大纲续写第五章正文"}}
  ]
}

【选中文本示例】⚠️ 当 Prompt 包含【用户选中的文本】时

用户选中文本: "天色未明，青冥中尚悬着几颗残星。"
用户指令: "帮我把这一句话修改得更加丰富！"
chapter_id: "abc-123"
{
  "thinking": {
    "step1_output": "用户选中了一句话，希望润色/丰富这段文字",
    "step2_material": "需要读取本章内容了解上下文，然后基于上下文给出改写建议",
    "step3_process": "先 read_chapter_tool 读章节，再 analyze_text_tool 分析并给出建议"
  },
  "user_intent": "润色选中的文本，使其更丰富",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "read_chapter_tool", "params": {"work_id": "$WORK_ID$", "chapter_id": "abc-123"}},
    {"task_id": 2, "description": "分析并给出更丰富的改写建议", "tool": "analyze_text_tool", "params": {"text": "天色未明，青冥中尚悬着几颗残星。", "focus": "基于章节上下文，给出更丰富的改写建议"}}
  ]
}

用户选中文本: "他走进房间，看到了她。"
用户指令: "更有文采一些"
chapter_id: "def-456"
{
  "thinking": {
    "step1_output": "用户选中了一句话，希望改写得更有文采",
    "step2_material": "需要读取本章内容了解场景和情绪",
    "step3_process": "先 read_chapter_tool 读章节，再 analyze_text_tool 分析并给出改写建议"
  },
  "user_intent": "改写选中的文本，使其更有文采",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "read_chapter_tool", "params": {"work_id": "$WORK_ID$", "chapter_id": "def-456"}},
    {"task_id": 2, "description": "分析并给出更有文采的改写建议", "tool": "analyze_text_tool", "params": {"text": "他走进房间，看到了她。", "focus": "基于章节上下文，给出更有文采的改写建议"}}
  ]
}

【多章节读取示例】⚠️ 涉及多个章节时

用户: "对比分析第3章和第7章中主角的心理变化"
{
  "thinking": {
    "step1_output": "用户需要对比两个章节中的内容",
    "step2_material": "需要同时读取第3章和第7章的内容",
    "step3_process": "使用 read_chapter_tool 一次性读取多个章节，然后用 analyze_text_tool 进行对比分析"
  },
  "user_intent": "对比分析多个章节的心理变化",
  "tasks": [
    {"task_id": 1, "description": "获取第3章的chapter_id", "tool": "get_chapter_by_order_tool", "params": {"work_id": "$WORK_ID$", "chapter_order": 3}},
    {"task_id": 2, "description": "获取第7章的chapter_id", "tool": "get_chapter_by_order_tool", "params": {"work_id": "$WORK_ID$", "chapter_order": 7}},
    {"task_id": 3, "description": "读取第3章和第7章内容", "tool": "read_chapter_tool", "params": {"work_id": "$WORK_ID$", "chapter_id": "$TASK_1.chapter_id$,$TASK_2.chapter_id$"}},
    {"task_id": 4, "description": "对比分析主角心理变化", "tool": "analyze_text_tool", "params": {"text": "$TASK_3$", "focus": "对比第3章和第7章中主角的心理状态、情绪变化、成长轨迹"}}
  ]
}

返回纯JSON（必须包含thinking字段）:"""

    return part1 + retrieval_tools + part2


# ════════════════════════════════════════════════════════════════
# Agent 模式增强版 Planning Prompt
# ════════════════════════════════════════════════════════════════

# Agent 模式专用的 checkpoint 说明（追加到基础 prompt）
_AGENT_MODE_CHECKPOINT_SECTION = """

📌 Agent 模式的反思机制

在 Agent 模式下，你可以给任务标记 `checkpoint: true`。
标记了 checkpoint 的任务完成后会触发反思评估，系统会检查是否需要调整后续计划。

## ⚠️ checkpoint 标记原则（严格遵守）

**重要：大部分任务不需要 checkpoint，只在关键决策点才标记！**

🔴 需要 checkpoint 的情况（仅限以下）：
- 多步骤任务的关键中间验证点（例如：分5个章节分析，可在第2章后设checkpoint）
- 可能失败需要补救的高风险操作（例如：批量修改、复杂改写）
- 需要用户确认才能继续的决策点（极少情况）

✅ 不需要 checkpoint 的情况（占大多数）：
- 简单的读取/搜索任务（read_chapter_tool, get_context_tool, search等）
- 单步就能完成的任务（分析、摘要、问答）
- 常规的改写/续写任务（smart_rewrite, continue_writing_tool）
- 已经是最后一个任务

## 📊 标记频率建议

- 1-2个任务：0个checkpoint
- 3-5个任务：最多1个checkpoint（通常在第2-3个任务）
- 6+个任务：最多2个checkpoint（均匀分布）

**记住：checkpoint越少，执行越快，用户体验越好！默认不标记，只在真正需要时才标记。**

## 📝 Agent 模式示例（必须包含 checkpoint 字段）

示例1 - 简单查询（无checkpoint）：
用户: "叶凡是什么体质？"
{
  "thinking": {"step1_output": "描述体质", "step2_material": "搜索相关内容", "step3_process": "总结"},
  "user_intent": "查询叶凡体质",
  "tasks": [
    {"task_id": 1, "description": "搜索叶凡体质", "tool": "search_analysis_fragments_tool",
     "params": {"query": "叶凡的体质"}, "checkpoint": false},
    {"task_id": 2, "description": "总结体质特点", "tool": "analyze_text_tool",
     "params": {"text": "$TASK_1$", "focus": "总结体质特点"}, "checkpoint": false}
  ]
}

示例2 - 多章节分析（使用批量读取）：
用户: "分析前5章的情节发展"
{
  "thinking": {"step1_output": "分析报告", "step2_material": "5个章节内容", "step3_process": "批量读取后汇总分析"},
  "user_intent": "分析前5章情节",
  "tasks": [
    {"task_id": 1, "description": "批量读取前5章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": "1-5"}, "checkpoint": false},
    {"task_id": 2, "description": "汇总分析情节发展", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.chapters$", "focus": "分析前5章的情节发展、人物成长、伏笔设置"}, "checkpoint": false}
  ]
}

示例3 - 单任务（无checkpoint）：
用户: "第3章讲了什么"
{
  "thinking": {"step1_output": "概括", "step2_material": "第3章", "step3_process": "读取并概括"},
  "user_intent": "概括第3章",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}, "checkpoint": false},
    {"task_id": 2, "description": "概括内容", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "概括"}, "checkpoint": false}
  ]
}

"""


@cache_review(expire=3600, key_prefix=f"prompt:planning_agent:{PROMPT_VERSION}")
async def get_planning_agent_mode_prompt() -> str:
    """获取 Agent 模式的 Planning Prompt（带 checkpoint 标记功能）

    Returns:
        str: Agent 模式专用的 Planning Prompt

    说明：
        Agent 模式与 Plan 模式的区别：
        - 任务可以标记 checkpoint: true
        - checkpoint 任务完成后会触发反思评估
        - 支持动态调整后续任务

    🔧 2025-12-08: 新增 Agent 模式支持，基于 LangChain DeepAgents 设计理念
    """
    base_prompt = await get_planning_static_prompt()
    # 在基础 prompt 的 "返回纯JSON" 之前插入 checkpoint 说明
    return base_prompt.replace(
        "返回纯JSON（必须包含thinking字段）:",
        _AGENT_MODE_CHECKPOINT_SECTION + "\n返回纯JSON（必须包含thinking字段，Agent模式下任务需包含checkpoint字段）:"
    )


@cache_review(expire=3600, key_prefix=f"prompt:complexity:{PROMPT_VERSION}")
async def get_complexity_decision_prompt() -> str:
    """复杂度判断 Prompt（在意图分类后调用）

    用于判断请求复杂度（simple/complex）并确定执行方案：
    - simple + tool: 直接执行单个工具
    - simple + answer: 直接返回答案
    - complex: 交给原有 Agent 流程

    Returns:
        str: Prompt 模板（需要 .format(intent=..., message=...) 填充）
    """
    return """你是执行路径决策器。根据已识别的意图类型和用户请求，判断最优执行路径。

【输入信息】
- 意图类型: {intent} (已由意图分类器识别)
- 用户请求: {message}

【决策规则】

## 复杂度判断
问自己：这个请求需要复杂处理吗？

判断为 simple（可直接执行）的条件：
- 只需要 1 个工具调用（如获取标题、字数）
- 或者可以直接回答（如问候、简单问答）
- 没有依赖关系
- 没有多步骤

判断为 complex（需要完整流程）的条件：
- 需要多个工具协作
- 有步骤依赖（先获取A，再用A做B）
- 涉及创作完整章节
- 需要分析后再行动
- 需要概括/总结内容

## 执行方案
如果是 simple，给出具体方案：

工具调用时：
- tool_name: 工具名称
- tool_args: 参数
- response_hint: 返回字段提示（title/content/word_count）

直接回答时：
- direct_answer: 答案内容

【可用工具速查】

获取类（返回数据，无副作用）：
- get_chapter_by_order_tool(chapter_order: int) → {{title, content, word_count}}
- get_context_tool() → 作品上下文

注意：概括/总结内容需要分析处理，应判定为 complex

【输出格式】

```json
{{
  "complexity": "simple|complex",
  "reason": "判断依据（简短）",
  "action": {{
    // simple + tool:
    "tool_name": "工具名",
    "tool_args": {{}},
    "response_hint": "title|content|word_count"

    // simple + answer:
    "direct_answer": "直接回答内容"

    // complex: 留空 {{}}
  }}
}}
```

请分析并返回 JSON:"""
