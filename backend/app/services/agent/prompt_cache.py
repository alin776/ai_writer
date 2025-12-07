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
        str: 静态 Prompt 文本（约 250 tokens）

    说明：
        这部分 Prompt 包含工具列表、规则说明和示例，
        对所有请求都相同，因此可以安全缓存。

    🔧 2025-12-02: P3根源修复 - 区分JSON工具和纯文本工具的占位符用法
    🔧 2025-12-06: P1优化 - 增强多章节分析+续写场景的指导
    """
    return """生成任务清单JSON。

可用工具:
【返回JSON的工具 - 支持字段引用 $TASK_N.field$】
1. get_chapter_by_order_tool: 按序号获取章节 (参数: chapter_order) → 返回 {content, title, order}
2. read_chapter_tool: 按ID读取章节 (参数: chapter_id) → 返回 {content, title}
3. get_context_tool: 获取作品上下文 (无参数) → 返回 {work_info, current_chapter}
4. search_analysis_fragments_tool: 搜索设定 (参数: query) → 返回 {fragments}

【返回纯文本的工具 - 只能用完整输出 $TASK_N$】
5. continue_writing_tool: 续写 (参数: context, requirements) → 返回纯文本
6. polish_text_tool: 润色 (参数: text, style) → 返回纯文本
7. analyze_text_tool: 分析 (参数: text, focus) → 返回纯文本

规则:
- "第X章" → 用 get_chapter_by_order_tool
- UUID格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
- JSON工具可用字段引用: $TASK_N.content$, $TASK_N.title$ 等
- 纯文本工具只能用完整输出: $TASK_N$ (不要加.field)
- 写作/生成类任务（continue_writing_tool、polish_text_tool 等）必须串联前序任务：用 $TASK_N$ 或 $TASK_N.content$ 作为输入，禁止直接复述用户原话或空上下文。
- 写作前先获取/分析：先用 read_chapter/get_chapter_by_order/analyze_text 拿到内容，再把 $TASK_N$ 传给写作工具的 params（如 context/text）。
- ⚠️ 多章节分析后续写时：分析任务的 $TASK_N$ 必须传给续写任务的 context 参数，确保角色和剧情延续！

示例:
用户: "分析第二章并润色"
{
  "user_intent": "分析第二章并润色",
  "tasks": [
    {"task_id": 1, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}},
    {"task_id": 2, "description": "分析章节", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "all"}},
    {"task_id": 3, "description": "润色内容", "tool": "polish_text_tool", "params": {"text": "$TASK_2$", "style": "文学"}}
  ]
}

用户: "基于前两章续写第三章"
{
  "user_intent": "基于前两章续写第三章",
  "tasks": [
    {"task_id": 1, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}},
    {"task_id": 2, "description": "分析第二章", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "角色+剧情"}},
    {"task_id": 3, "description": "续写第三章", "tool": "continue_writing_tool", "params": {"context": "$TASK_2$", "requirements": "承接角色关系与冲突"}}
  ]
}

用户: "分析前三章，续写第四章"
{
  "user_intent": "分析前三章，续写第四章",
  "tasks": [
    {"task_id": 1, "description": "获取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 2, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}},
    {"task_id": 3, "description": "获取第三章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}},
    {"task_id": 4, "description": "分析前三章", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$\n\n$TASK_2.content$\n\n$TASK_3.content$", "focus": "角色+剧情+伏笔"}},
    {"task_id": 5, "description": "续写第四章", "tool": "continue_writing_tool", "params": {"context": "$TASK_4$", "requirements": "基于分析结果续写，延续角色和故事线"}}
  ]
}

返回纯JSON:"""
