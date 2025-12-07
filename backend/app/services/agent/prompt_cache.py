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
    """
    return """生成任务清单JSON。

【核心规则 - 任务类型识别】
⚠️ 最重要：先识别任务类型，再决定如何规划！

1. 写作类任务 → 使用 multi_agent_writing（单个任务）
   关键词：续写、写、创作、扩写、重写、生成章节、写第X章
   规则：不要分解成「获取章节」「分析」等子任务，Multi-Agent 内部会自动处理

2. 查询类任务 → 使用对应工具
   关键词：获取、查看、读取、列出

3. 分析类任务 → 使用 analyze_text_tool
   关键词：分析、总结、归纳（不涉及写作时）

4. 编辑类任务 → 使用 smart_rewrite 等
   关键词：修改、润色、改写某段

【可用工具】
查询工具:
- get_chapter_by_order_tool: 按序号获取章节 (参数: chapter_order)
- read_chapter_tool: 按ID读取章节 (参数: chapter_id)
- get_context_tool: 获取作品上下文 (无参数)

分析工具:
- analyze_text_tool: 分析文本 (参数: text, focus)

写作工具（仅用于非章节级写作）:
- polish_text_tool: 润色 (参数: text, style)

⚠️ 特殊类型 - multi_agent_writing:
- 用于：续写章节、创作新章节、扩写内容
- 不需要指定 tool 字段，使用 type: "multi_agent_writing"
- params 包含: chapters_needed(数组), target_chapter(数字), requirements(字符串)

【示例】

✅ 写作类 - 使用 multi_agent_writing（正确）
用户: "分析前三章，续写第四章"
{
  "user_intent": "基于前三章续写第四章",
  "tasks": [
    {
      "task_id": 1,
      "type": "multi_agent_writing",
      "description": "基于前三章续写第四章",
      "params": {
        "chapters_needed": [1, 2, 3],
        "target_chapter": 4,
        "requirements": "分析前三章的角色、剧情、伏笔，续写第四章"
      }
    }
  ]
}

✅ 写作类 - 简单续写
用户: "续写第五章"
{
  "user_intent": "续写第五章",
  "tasks": [
    {
      "task_id": 1,
      "type": "multi_agent_writing",
      "description": "续写第五章",
      "params": {
        "chapters_needed": [4],
        "target_chapter": 5,
        "requirements": "承接上一章内容续写"
      }
    }
  ]
}

✅ 查询类 - 使用工具
用户: "获取第二章内容"
{
  "user_intent": "获取第二章",
  "tasks": [
    {"task_id": 1, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}}
  ]
}

✅ 分析类 - 不涉及写作
用户: "分析第一章的人物关系"
{
  "user_intent": "分析第一章人物关系",
  "tasks": [
    {"task_id": 1, "description": "获取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 2, "description": "分析人物关系", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "人物关系"}}
  ]
}

✅ 混合类 - 先分析再写作
用户: "帮我分析一下前两章写得怎么样，然后续写第三章"
{
  "user_intent": "分析前两章并续写第三章",
  "tasks": [
    {"task_id": 1, "description": "获取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 2, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}},
    {"task_id": 3, "description": "分析前两章质量", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$\n\n$TASK_2.content$", "focus": "写作质量评估"}},
    {
      "task_id": 4,
      "type": "multi_agent_writing",
      "description": "续写第三章",
      "params": {
        "chapters_needed": [1, 2],
        "target_chapter": 3,
        "requirements": "基于前两章续写第三章"
      }
    }
  ]
}

返回纯JSON:"""
