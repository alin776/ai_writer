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
"""

from app.core.cache import cache_review


@cache_review(expire=3600, key_prefix="prompt")
async def get_tool_decision_static_prompt() -> str:
    """获取工具决策的静态 Prompt 部分（可缓存 1 小时）

    Returns:
        str: 静态 Prompt 文本（约 150 tokens）

    说明：
        这部分 Prompt 包含工具列表、JSON 格式说明和示例，
        对所有请求都相同，因此可以安全缓存。
    """
    return """判断是否需要工具。可用工具:

【编辑器工具 - 修改内容时优先使用】
- smart_rewrite: 改写/修改章节内容
  参数: chapter_id, text_to_rewrite, user_requirement, base_version
- smart_continue: 续写章节 (参数: chapter_id, context)
- smart_insert: 插入内容 (参数: chapter_id, position, content)
- apply_chapter_edit: 直接应用编辑 (参数: chapter_id, operation, content)

【读取工具】
需work_id: get_chapter_by_order_tool, get_context_tool, read_chapter_tool, search_analysis_fragments_tool
不需work_id: continue_writing_tool, polish_text_tool, analyze_text_tool

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
1. 用户说"修改"、"改写"、"重写" → 使用 smart_rewrite
2. 用户说"续写"、"继续写" → 使用 smart_continue
3. 用户说"插入" → 使用 smart_insert
4. 简单问候/寒暄（如"你好"、"在吗"、"谢谢"）→ 不需要工具，直接回复
5. 必须严格返回JSON格式！

返回JSON:
- 需要: {"need_tools": true, "tool_name": "工具名", "tool_args": {}}
- 缺参数: {"need_tools": false, "direct_response": "请提供..."}
- 直接答: {"need_tools": false, "direct_response": "..."}
- 问候: {"need_tools": false, "direct_response": "您好！我是AI写作助手，可以帮您修改、续写章节内容。请问有什么可以帮您的？"}

示例:
"你好" → {"need_tools": false, "direct_response": "您好！我是AI写作助手，可以帮您修改、续写章节内容。请问有什么可以帮您的？"}
"白光退去太平淡" → {"need_tools": true, "tool_name": "smart_rewrite", "tool_args": {"chapter_id": "xxx", "text_to_rewrite": "白光退去...", "user_requirement": "更有画面感"}}
"在第二版基础上更简洁" → {"need_tools": true, "tool_name": "smart_rewrite", "tool_args": {"chapter_id": "xxx", "user_requirement": "更简洁", "base_version": "第二版"}}

⚠️ 请严格返回JSON格式，不要直接回答问题:"""


@cache_review(expire=3600, key_prefix="prompt")
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
    """
    return """你是一个任务规划助手。请使用【三步思维链】来理解用户意图并生成任务。

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
- 概括/分析/规划 → 获取 + analyze_text_tool
- 创作完整章节正文 → multi_agent_writing

【关键判断】

⚠️ multi_agent_writing 使用条件（非常严格）：
- 只有当用户明确要求"续写整个章节"、"写第X章正文"时才使用
- 以下情况绝对不用 multi_agent_writing：
  × 获取/查看章节 → get_chapter_by_order_tool
  × 概括/总结 → analyze_text_tool
  × 写大纲/规划 → analyze_text_tool
  × 分析人物/情节 → analyze_text_tool
  × 润色/修改 → 其他工具

大纲 vs 正文：
- 大纲 = 结构化规划（章节标题、主线、伏笔列表）→ analyze_text_tool
- 正文 = 完整故事叙述（2000-4000字，有对话、描写、情节）→ multi_agent_writing

概括 vs 原文：
- 用户想了解内容（"讲了什么"、"是什么故事"、"主要内容"）→ 需要概括
- 用户想获取内容（"给我"、"获取"、"发给我"、"看一下"）→ 直接返回

复合任务：
- 用户说"先做A再做B" → 分解为独立任务，按顺序排列

【可用工具】

获取原料：
- get_chapter_by_order_tool: 按序号获取章节 (参数: chapter_order)
  ⚠️ 返回数据已包含: {title, order, content, word_count} → 标题/序号等元数据无需再分析！
- get_context_tool: 获取作品上下文

处理原料：
- analyze_text_tool: 概括、分析、规划大纲 (参数: text, focus)
  - 适用于：概括内容、分析人物、分析情节、写大纲、规划章节
  - ⚠️ 不要用于：查询标题/序号等元数据（工具已返回这些字段）

创作内容（重量级，谨慎使用）：
- multi_agent_writing: 创作完整章节正文
  - ⚠️ 仅当用户明确要求"续写章节"、"写第X章"时使用
  - 不要用于：写大纲、概括、分析、获取内容
  - params: chapters_needed, target_chapter, requirements

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
    "step3_process": "分析前文后规划大纲结构"
  },
  "user_intent": "规划第5-9章大纲",
  "tasks": [
    {"task_id": 1, "description": "获取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 2, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}},
    {"task_id": 3, "description": "获取第三章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}},
    {"task_id": 4, "description": "获取第四章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 4}},
    {"task_id": 5, "description": "规划大纲", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$\\n\\n$TASK_2.content$\\n\\n$TASK_3.content$\\n\\n$TASK_4.content$", "focus": "基于前四章的人物、情节、伏笔，为第5-9章设计详细大纲：章节标题、主要剧情、涉及角色、伏笔设置"}}
  ]
}

用户: "续写第五章"
{
  "thinking": {
    "step1_output": "用户想看到完整的第五章正文，是实际的故事叙述",
    "step2_material": "需要前文内容作为续写参考",
    "step3_process": "创作新的章节正文"
  },
  "user_intent": "创作第五章正文",
  "tasks": [
    {"task_id": 1, "type": "multi_agent_writing", "description": "续写第五章", "params": {"chapters_needed": [4], "target_chapter": 5, "requirements": "承接上一章内容续写"}}
  ]
}

用户: "分析前四章，然后写后5章大纲，再续写第五章"
{
  "thinking": {
    "step1_output": "复合任务：1)分析报告 2)大纲规划 3)章节正文",
    "step2_material": "需要前四章内容",
    "step3_process": "分三阶段：分析→规划大纲→创作正文"
  },
  "user_intent": "分析+规划大纲+续写",
  "tasks": [
    {"task_id": 1, "description": "获取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 2, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}},
    {"task_id": 3, "description": "获取第三章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}},
    {"task_id": 4, "description": "获取第四章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 4}},
    {"task_id": 5, "description": "分析前四章", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$\\n\\n$TASK_2.content$\\n\\n$TASK_3.content$\\n\\n$TASK_4.content$", "focus": "分析前四章：主要人物、情节发展、伏笔线索、写作风格"}},
    {"task_id": 6, "description": "规划第5-9章大纲", "tool": "analyze_text_tool", "params": {"text": "$TASK_5$", "focus": "基于分析结果，为第5-9章设计详细大纲"}},
    {"task_id": 7, "type": "multi_agent_writing", "description": "续写第五章", "params": {"chapters_needed": [4], "target_chapter": 5, "requirements": "基于大纲续写第五章正文"}}
  ]
}

返回纯JSON（必须包含thinking字段）:"""


# ════════════════════════════════════════════════════════════════
# Agent 模式增强版 Planning Prompt
# ════════════════════════════════════════════════════════════════

# Agent 模式专用的 checkpoint 说明（追加到基础 prompt）
_AGENT_MODE_CHECKPOINT_SECTION = """

【Agent 模式：检查点标记】

在 Agent 模式下，你可以为关键任务标记 `"checkpoint": true`。
标记检查点的任务完成后，系统会评估执行结果，必要时调整后续计划。

## 什么时候标记 checkpoint？

需要标记 checkpoint 的任务：
- 分析类任务（analyze_text_tool）→ 结果可能影响后续任务
- 规划/设计类任务 → 需要验证规划是否合理
- 复杂的多步骤任务的中间关键节点

不需要标记 checkpoint 的任务：
- 简单获取任务（get_chapter_by_order_tool, get_context_tool）
- 最后一个任务（执行完就结束了）
- 独立的单步骤任务

## 输出格式（Agent 模式）

{
  "thinking": {...},
  "user_intent": "...",
  "tasks": [
    {"task_id": 1, "description": "获取上下文", "tool": "get_context_tool", "checkpoint": false},
    {"task_id": 2, "description": "分析并规划大纲", "tool": "analyze_text_tool", "checkpoint": true, "params": {...}}
  ]
}

## 示例

用户: "根据前面的章节，规划后续5章大纲"
{
  "thinking": {
    "step1_output": "用户想看到后续5章的大纲规划",
    "step2_material": "需要前面章节的内容",
    "step3_process": "获取上下文后进行大纲规划"
  },
  "user_intent": "规划后续章节大纲",
  "tasks": [
    {"task_id": 1, "description": "获取作品上下文", "tool": "get_context_tool", "checkpoint": false},
    {"task_id": 2, "description": "规划后续5章大纲", "tool": "analyze_text_tool", "checkpoint": true, "params": {"text": "$TASK_1$", "focus": "基于已有内容，规划后续5章的大纲"}}
  ]
}

注意：checkpoint 字段是可选的，默认为 false。只有需要在该任务后进行评估时才标记为 true。
"""


@cache_review(expire=3600, key_prefix="prompt")
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


@cache_review(expire=3600, key_prefix="prompt")
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
