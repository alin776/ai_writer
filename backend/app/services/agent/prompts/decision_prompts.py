"""
决策类提示词模块

包含：
- 工具决策提示词 (get_tool_decision_static_prompt)
- 复杂度决策提示词 (get_complexity_decision_prompt)
"""

from app.core.cache import cache_review
from .tool_descriptions import (
    _get_retrieval_tools_section,
    _get_operation_tools_section,
    _get_creative_tools_section,
    _get_analysis_tools_section
)

# Prompt 版本号 - 修改 Prompt 时请更新此版本号
PROMPT_VERSION = "v2.42.0"  # 2026-02-13: smart_continue 目标章节不存在时升级为 smart_create


@cache_review(expire=3600, key_prefix=f"prompt:tool_decision:{PROMPT_VERSION}")
async def get_tool_decision_static_prompt() -> str:
    """获取工具决策的静态 Prompt 部分（可缓存 1 小时）

    Returns:
        str: 静态 Prompt 文本（约 150 tokens）

    说明：
        这部分 Prompt 包含工具列表、JSON 格式说明和示例，
        对所有请求都相同，因此可以安全缓存。
    """
    retrieval_tools = _get_retrieval_tools_section()
    operation_tools = _get_operation_tools_section()
    creative_tools = _get_creative_tools_section()
    analysis_tools = _get_analysis_tools_section()

    return f"""⚠️ 核心原则：先判断是否需要操作具体内容，不需要就直接回答

【第一步：判断是否需要工具】

✅ 不需要工具，直接回答的情况（优先判断）：
- 问候、寒暄（你好、在吗、谢谢、再见）
- 关于 AI 的问题（你是谁、你能做什么、介绍一下你自己）
- 知识问答（什么是XX、为什么XX、如何XX）
- 闲聊、聊天、表达感受
- 用户没有明确要求操作章节/文本内容
- 任何不确定的情况 → 选择直接回答

❌ 需要工具的情况（必须同时满足）：
- 用户明确要求操作具体的章节内容（修改、续写、插入、改写、润色）
- 或者用户要搜索/查找具体的文本片段、人物、情节

【第二步：如果需要工具，选择合适的工具】

【编辑器工具 - 修改内容时优先使用】
- smart_rewrite: 段落级改写/修改章节内容（只生成1个改写结果）
  参数: chapter_id, text_to_rewrite, user_requirement, evidence_context
- rewrite_chapter_content: 整章改写（只生成整章内容）
  参数: chapter_id, user_requirement, chapter_content(可选), evidence_context(可选)
- smart_continue: 智能续写（根据上下文生成续写内容）
  参数: chapter_id, chapter_content, user_requirement, evidence_context, word_count
- smart_insert: 智能插入（根据意图生成插入内容）
  参数: chapter_id, user_intent, chapter_content, insert_context, evidence_context, word_count
- operate_apply: 🆕 统一应用内容到编辑器（推荐！）
  参数: operation(append/replace/insert/content/create/title), chapter_id, content, ...
  ⚠️ smart_* 生成内容后，必须用 operate_apply 应用到编辑器
  ⚠️ operate_apply 不会自动定位，replace/insert 必须传 node_id/paragraph_index

【读取工具】⚠️ 优先使用 explore_content 统一入口！
- explore_content: 深度探索工具，自动判断任务复杂度并获取所需信息（推荐！）
- analyze_content: 一站式内容分析（仅用于明确的结构化评估/一致性/风格/质量报告）
{retrieval_tools}
{operation_tools}
{creative_tools}
{analysis_tools}
⚠️ **重要变更**：polish_text_tool 已移除
- 所有润色/修改请求必须提供 chapter_id，使用基于章节上下文的工具
- 如果涉及多个章节，explore_content 支持自动探索获取相关信息

【工具使用规则】

1. 用户提到具体文字但未说章节 → 先用 explore_content 定位章节
2. 用户说"整章重写/全文改写/全章改写" → rewrite_chapter_content → operate_apply(operation="content")
3. 用户说"修改第X章"、"改写第X章" → smart_rewrite → operate_apply(operation="replace")
4. 用户说"续写"、"继续写" → smart_continue → operate_apply(operation="append")
5. 用户说"插入" → smart_insert → operate_apply(operation="insert")
6. 用户说"创建新章节"、"新建章节" → operate_apply(operation="create")
7. 用户说"删除章节" → delete_chapter（⚠️ 危险操作，需确认）
8. 用户说"改标题"、"重命名章节" → operate_apply(operation="title")
9. 用户说"检查一致性"、"有没有矛盾" → 使用 analyze_content（analysis_types=["consistency"]）
10. 用户说"分析风格"、"写作特点" → 使用 analyze_content（analysis_types=["style"]）
11. 用户要"暗线/伏笔/剧情大纲/设定补充/推演方案" → 只用 explore_content（取证据后直接回答，不用 analyze_content）

⚠️ **operate_apply 定位规则**：
- replace/insert 必须传 node_id 或 paragraph_index
- 需要先用 locate_content 定位（检索证据统一走 explore_content）

⚠️ 【搜索兜底规则】：
- 如果用户提供的文字**过于简短**（少于3个字）或是**通用描述**（如"这一章"、"这段话"）
- → **不要调用搜索工具**，直接返回询问更多信息

【返回格式】必须严格返回JSON：

不需要工具时：
{{"need_tools": false, "direct_response": "你的回答内容"}}

需要工具时：
{{"need_tools": true, "tool_name": "工具名", "tool_args": {{参数}}}}

【示例 - 不需要工具的情况】

"你好" → {{"need_tools": false, "direct_response": "..."}}
"你是谁" → {{"need_tools": false, "direct_response": "..."}}
"你能做什么" → {{"need_tools": false, "direct_response": "..."}}
"谢谢" → {{"need_tools": false, "direct_response": "..."}}
"写作有什么技巧" → {{"need_tools": false, "direct_response": "..."}}
"这段话太平淡" → {{"need_tools": false, "direct_response": "请问您指的是哪一章？..."}}

注意：direct_response 的内容由你根据问题自由生成，不要复制示例。

【示例 - 需要工具的情况】

"微光如露落雪太书面化" → {{"need_tools": true, "tool_name": "explore_content", "tool_args": {{"target_task": "定位并获取'微光如露落雪'相关内容"}}}}
"修改第三章，白光退去太平淡" → {{"need_tools": true, "tool_name": "smart_rewrite", "tool_args": {{"chapter_id": "xxx", "text_to_rewrite": "白光退去...", "user_requirement": "更有画面感"}}}}
"续写第五章" → {{"need_tools": true, "tool_name": "smart_continue", "tool_args": {{"chapter_id": "xxx", "user_requirement": "续写", "word_count": 500}}}}
"有没有叫赵穆的人物" → {{"need_tools": true, "tool_name": "explore_content", "tool_args": {{"target_task": "查找赵穆相关信息"}}}}
"段融是谁" → {{"need_tools": true, "tool_name": "explore_content", "tool_args": {{"target_task": "查找段融相关信息"}}}}
"请给出'二十四桥明月夜'的原文出处" → {{"need_tools": true, "tool_name": "explore_content", "tool_args": {{"target_task": "查找'二十四桥明月夜'原文出处"}}}}
"创建一个新章节叫第六章" → {{"need_tools": true, "tool_name": "operate_apply", "tool_args": {{"operation": "create", "work_id": "xxx", "title": "第六章"}}}}
"删除第三章" → {{"need_tools": true, "tool_name": "delete_chapter", "tool_args": {{"chapter_id": "xxx"}}}}
"把第二章标题改成觉醒" → {{"need_tools": true, "tool_name": "operate_apply", "tool_args": {{"operation": "title", "chapter_id": "xxx", "title": "觉醒"}}}}
"检查前五章有没有矛盾" → {{"need_tools": true, "tool_name": "analyze_content", "tool_args": {{"analysis_types": ["consistency"], "work_id": "xxx", "content": "..."}}}}
"分析一下我的写作风格" → {{"need_tools": true, "tool_name": "analyze_content", "tool_args": {{"analysis_types": ["style"], "content": "..."}}}}
"基于原文设计暗线和伏笔" → {{"need_tools": true, "tool_name": "explore_content", "tool_args": {{"target_task": "收集暗线/伏笔相关原文证据，便于推演方案"}}}}

⚠️ 如果不确定用户是否需要工具，选择直接回答。请严格返回JSON格式:"""


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

判断为 simple + direct_answer（直接回答，不需要工具）的条件：
- 问候、寒暄（你好、在吗、谢谢）
- 关于 AI 的问题（你是谁、你能做什么、介绍一下你自己）
- 知识问答、闲聊、表达感受
- 用户没有明确要求操作章节/文本内容
- 任何不确定的情况 → 选择直接回答

判断为 simple + tool（单个工具调用）的条件：
- 只需要 1 个工具调用（如获取标题、字数）
- 没有依赖关系
- 没有多步骤

判断为 complex（需要完整流程）的条件：
- 需要多个工具协作
- 有步骤依赖（先获取A，再用A做B）
- 涉及创作完整章节
- 需要分析后再行动
- 需要概括/总结内容

## 执行方案

直接回答时（优先考虑）：
- direct_answer: 答案内容

工具调用时：
- tool_name: 工具名称
- tool_args: 参数
- response_hint: 返回字段提示（title/content/word_count）

【可用工具速查】

获取类（返回数据，无副作用）：
- explore_content(target_task: str) → 自动探索获取所需信息

注意：概括/总结内容需要分析处理，应判定为 complex

【示例】

"你好" → {{"complexity": "simple", "reason": "问候", "action": {{"direct_answer": "..."}}}}
"你是谁" → {{"complexity": "simple", "reason": "关于AI的问题", "action": {{"direct_answer": "..."}}}}
"第三章标题是什么" → {{"complexity": "simple", "reason": "单个工具调用", "action": {{"tool_name": "explore_content", "tool_args": {{"target_task": "获取第三章标题"}}, "response_hint": "title"}}}}
"分析前五章" → {{"complexity": "complex", "reason": "需要读取多章并分析", "action": {{}}}}

注意：direct_answer 的内容由你根据问题自由生成。

【输出格式】

```json
{{
  "complexity": "simple|complex",
  "reason": "判断依据（简短）",
  "action": {{
    // simple + answer:
    "direct_answer": "直接回答内容"

    // simple + tool:
    "tool_name": "工具名",
    "tool_args": {{}},
    "response_hint": "title|content|word_count"

    // complex: 留空 {{}}
  }}
}}
```

⚠️ 如果不确定，选择直接回答。请分析并返回 JSON:"""


# 导出
__all__ = [
    "PROMPT_VERSION",
    "get_tool_decision_static_prompt",
    "get_complexity_decision_prompt",
]
