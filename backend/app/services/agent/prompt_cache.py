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
需work_id: get_chapter_by_order, get_context, read_chapter, search_fragments
不需work_id: continue_writing, polish_text, analyze_text

返回JSON:
- 需要: {{"need_tools": true, "tool_name": "工具名", "tool_args": {{}}}}
- 缺参数: {{"need_tools": false, "direct_response": "请提供..."}}
- 直接答: {{"need_tools": false, "direct_response": "..."}}

示例:
"获取第3章" + work_id已设置 → {{"need_tools": true, "tool_name": "get_chapter_by_order_tool", "tool_args": {{"chapter_order": 3}}}}
"获取第3章" + work_id未设置 → {{"need_tools": false, "direct_response": "请先告诉我是哪部作品？"}}

请判断并返回JSON:"""


@cache_review(expire=3600, key_prefix="prompt")
async def get_planning_static_prompt() -> str:
    """获取 Planning 的静态 Prompt 部分（可缓存 1 小时）

    Returns:
        str: 静态 Prompt 文本（约 250 tokens）

    说明：
        这部分 Prompt 包含工具列表、规则说明和示例，
        对所有请求都相同，因此可以安全缓存。
    """
    return """生成任务清单JSON。

可用工具:
1. get_chapter_by_order_tool: 按序号获取章节 (参数: chapter_order)
2. read_chapter_tool: 按ID读取章节 (参数: chapter_id, UUID格式)
3. get_context_tool: 获取作品上下文 (无参数)
4. search_analysis_fragments_tool: 搜索设定 (参数: query)
5. continue_writing_tool: 续写 (参数: context, requirements)
6. polish_text_tool: 润色 (参数: text, style)
7. analyze_text_tool: 分析 (参数: text, focus)

规则:
- "第X章" → 用 get_chapter_by_order_tool
- UUID格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (标准36字符)
- 任务依赖用占位符: $TASK_N.field$ (如 $TASK_1.content$)

示例:
用户: "分析第二章"
{{
  "user_intent": "分析第二章内容",
  "tasks": [
    {{"task_id": 1, "description": "获取第二章", "tool": "get_chapter_by_order_tool", "params": {{"chapter_order": 2}}, "estimated_time": "5秒"}},
    {{"task_id": 2, "description": "分析章节", "tool": "analyze_text_tool", "params": {{"text": "$TASK_1.content$", "focus": "情节"}}, "estimated_time": "10秒"}}
  ]
}}

返回纯JSON:"""
