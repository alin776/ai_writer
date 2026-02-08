"""
工具描述模块 - 单一数据源

所有工具的描述集中管理，避免多个 Prompt 不同步。
被 decision_prompts.py 和 planning_prompts.py 共同引用。
"""


def _get_new_aggregated_tools_section() -> str:
    """新聚合工具描述（2026-01-18 更新：explore_content 为统一入口）"""
    return """
🔴🔴🔴 【统一信息获取入口 - 最高优先级！】 🔴🔴🔴

⚠️ **重要：所有信息获取都使用 explore_content，它会自动判断需要的深度！**

- explore_content: **统一信息获取工具**
  参数:
    - work_id: 作品ID（必需）
    - target_task: 目标任务描述（必需，描述需要什么信息）
    - max_rounds: 最大探索轮数（默认100，简单任务1轮即返回）
    - max_tool_calls: 工具调用上限（仅 tool_loop 生效）
    - max_read_paragraphs: 读取段落上限（仅 tool_loop 生效）
  返回: {
    evidences,        # 证据原文列表（只读结果）
    locate_targets    # 定位目标（chapter_id + query + node_id 等）
  }
  🆕 返回字段包含 artifact_id / artifact_preview（用于后续按需取回完整结果）
  ⚠️ 默认返回完整字段（含 frontend_display/explore_summary）；如需精简，仅返回 evidences/locate_targets 时设置 output_mode="evidence_only"
  ⚠️ 后续工具参数只允许引用 evidences / locate_targets；旧字段仅用于兼容
  ⚠️ 整章改写例外：rewrite_chapter_content 可引用 chapters[0].chapter_id / chapters[0].content

- load_explore_artifact: **按需取回探索结果**
  参数:
    - artifact_id: 探索结果ID（必需）
    - work_id: 作品ID（必需）
    - user_id: 用户ID（可选）
    - mode: "full" | "summary" | "metadata"
    - max_chars: 最大字符数（可选，full 模式下可用）
  返回: {success, payload/summary/metadata}

  ✅ **所有信息获取场景都用这个工具**:
    - 续写/改写前获取上下文 → explore_content(target_task="续写第5章，需要第4-5章内容和世界观")
    - 分析人物/情节 → explore_content(target_task="分析主角性格特点，收集相关描写")（取证后直接回答，不用 analyze_content）
    - 搜索/查找内容 → explore_content(target_task="找出所有关于XX的描写")
    - 获取世界观设定 → explore_content(target_task="获取世界观和角色设定")
    - 批量读取章节 → explore_content(target_task="读取第1-5章内容")

  ⚠️ **工作原理**（你不需要关心，explore_content 自动处理）:
    - 简单查询 → 首轮即返回
    - 复杂查询 → 自动多轮探索
    - LLM 自行决定停止或达到安全上限

  ⚠️ **禁止直接使用以下工具**（这些是内部工具）:
    - ❌ list_chapters（已整合到 explore_content）
    - ❌ list_paragraphs（已整合到 explore_content）
    - ❌ exact_search_paragraphs（已整合到 explore_content）
    - ❌ read_paragraph/read_paragraphs（已整合到 explore_content）

---

- analyze_content: 🔴 结构化评估/报告专用
  参数:
    - content: 待分析文本（必需）
    - analysis_types: 分析类型列表（可选）
      * "text" - 文本分析
      * "style" - 风格分析
      * "consistency" - 一致性检查
      * "quality" - 质量评估
    - aspects: 分析维度列表，可选值：
      * "grammar" - 语法检查
      * "logic" - 逻辑分析
      * "style" - 风格分析
      * "structure" - 结构分析
      * "character" - 人物分析
      * "plot" - 情节分析
    - depth: 分析深度 "shallow" / "normal" / "deep"
    - focus: 分析重点（可选）
    - context: 上下文信息（可选）
  返回: {analysis, summary, scores, issues[], suggestions[]}

  ⚠️ **使用边界**：
    - 仅用于**明确的结构化评估/报告**（一致性/风格/质量/打分）
    - 其余“概括/分析/推演/大纲/设定补充/伏笔整理”等 → explore_content 取证后**直接输出**

  ✅ 使用示例：
    - 一致性检查: analyze_content(content="...", analysis_types=["consistency"])
    - 质量评估: analyze_content(content="...", analysis_types=["quality"])
    - 风格分析: analyze_content(content="...", analysis_types=["style"])
"""


def _get_retrieval_tools_section() -> str:
    """检索工具描述（内部工具，由 explore_content 调用）"""
    return """
【内部检索工具 - ⚠️ 禁止直接使用！】

以下工具已整合到 explore_content，请使用 explore_content 代替：

- list_chapters: ❌ 内部工具（由 explore_content 自动调用）
- list_paragraphs: ❌ 内部工具（由 explore_content 自动调用）
- exact_search_paragraphs: ❌ 内部工具（由 explore_content 自动调用）
- read_paragraph / read_paragraphs: ❌ 内部工具（由 explore_content 自动调用）

✅ **正确做法**：使用 explore_content(target_task="你的查询需求")
"""


def _get_editor_tools_section() -> str:
    """编辑器工具描述（直接修改章节内容）"""
    return """
【编辑器工具 - 修改内容时优先使用】

⚠️ **核心规则：创作类 vs 操作类**
- 创作类工具（smart_continue, smart_insert, smart_rewrite）：只生成内容，不写入编辑器
- 操作类工具（operate_apply）：将内容写入编辑器

🆕 **推荐：使用 operate_apply 统一入口**
- operate_apply 是 Create 工具输出的统一接收者，支持 6 种操作
- operate_apply 只负责写入，不再自动定位（replace/insert 必须传 node_id/paragraph_index）

⚠️ **什么时候需要调用操作类工具？**
- 用户说"续写"、"插入"、"改写"、"润色" → 需要！（内容要写入编辑器）
- 用户说"帮我写一段XX"、"生成一个大纲" → 不需要！（只是看内容，不写入编辑器）

⚠️ **创作类工具 → 操作类工具的推荐对应关系**
- smart_continue → operate_apply(operation="append")
- smart_insert → operate_apply(operation="insert")
- smart_rewrite → operate_apply(operation="replace")（段落级改写）
- rewrite_chapter_content → operate_apply(operation="content")（整章改写）

---

- smart_rewrite: 段落级改写/修改章节内容（只生成1个改写结果）
  参数: chapter_id, text_to_rewrite, user_requirement, evidence_context
  触发词: "修改"、"改写"、"重写"、"润色"、"优化"、"扩写"
  ⚠️ "扩写"= 把现有内容写得更丰富，属于改写场景，不是续写！
  ⚠️ **整章重写禁止使用 smart_rewrite**，必须使用 rewrite_chapter_content
  ⚠️ 如果用户想把改写内容写入编辑器 → 后续调用 operate_apply(operation="replace")
  ⚠️ **参数填充规则**（极其重要！）：
    * 如果用户指定了要改写的文本 → text_to_rewrite 填入该文本
    * 如果用户说"改写第X章"（但未说明整章） → 先用 explore_content 定位证据，再用 {"$ref": {"task_id": N, "path": "evidences[0].text"}} 引用
    * user_requirement 必须从用户消息中提取改写要求！
  ⚠️ 输出只允许单段内容，不要编号/版本列表
  ⚠️ 即使用户要求多版本/多候选，也只生成一条

- rewrite_chapter_content: 整章改写工具（只生成，不写入编辑器）
  参数: chapter_id, user_requirement, chapter_content(可选), evidence_context(可选)
  触发词: "整章重写"、"全文改写"、"全章改写"
  ⚠️ 不需要 paragraph_index/node_id（只用于整章）
  ⚠️ 输出是整章内容，必须用 operate_apply(operation="content") 写入

- smart_continue: 智能续写（只生成内容）
  参数: chapter_id, chapter_content, user_requirement, evidence_context, word_count
  触发词: "续写"、"继续写"、"往后写"
  ⚠️ 如果用户想把续写内容写入编辑器 → 后续调用 operate_apply(operation="append")

- smart_insert: 智能插入（只生成内容）
  参数: chapter_id, user_intent, chapter_content, insert_context, evidence_context, word_count
  触发词: "插入"、"在...处添加"、"在...后面加"
  ⚠️ 如果用户想把插入内容写入编辑器 → 后续调用 operate_apply(operation="insert")
  ⚠️ **定位规则**：先用 locate_content/list_paragraphs/read_paragraphs 获取 node_id/paragraph_index
  ⚠️ insert_context 可用于风格参考，从 explore_content 返回的章节内容中获取
  ⚠️ 输出只允许单段内容，不要编号/版本列表
  ⚠️ 即使用户要求多版本/多候选，也只生成一条

---

🆕 **operate_apply: 统一应用 AI 生成的内容（推荐使用！）**
  参数:
    - operation: 操作类型（必需）
      * "append" - 续写（追加到章节末尾）
      * "replace" - 改写（替换指定段落）
      * "insert" - 插入（在指定位置插入）
      * "content" - 整章替换（替换整个章节内容）
      * "create" - 创建新章节（需要 work_id 和 title）
      * "title" - 修改标题（需要 chapter_id 和 title）
    - chapter_id: 章节ID（create 时不需要）
    - work_id: 作品ID（create 时必需）
    - content: AI生成的内容
    - title: AI生成的标题（create/title 时使用）
    - original_text: 原文（仅用于描述，不参与定位）
    - target_description: 目标位置描述（仅用于描述，不参与定位）
    - paragraph_index: 段落索引（优先级最高的定位方式）
    - node_id: 节点ID（优先级最高的定位方式）
    - allow_append_fallback: 已禁用（不再允许降级追加）

  ✅ **推荐使用场景**：
    * smart_continue 后续写 → operate_apply(operation="append", chapter_id=..., content=...)
    * smart_rewrite 后替换 → operate_apply(operation="replace", chapter_id=..., content=..., paragraph_index=..., node_id=...)
    * smart_insert 后插入 → operate_apply(operation="insert", chapter_id=..., content=..., paragraph_index=..., node_id=...)
    * 重写整章 → operate_apply(operation="content", chapter_id=..., content=...)
    * 创建新章节 → operate_apply(operation="create", work_id=..., title=..., content=...)
    * 修改标题 → operate_apply(operation="title", chapter_id=..., title=...)

  ⚠️ **定位要求**：
    * replace/insert 必须提供 node_id 或 paragraph_index

---

- apply_chapter_edit: ⚠️ **底层操作工具（由 operate_apply 内部调用，推荐使用 operate_apply 代替！）**
  参数: chapter_id, operation, content, paragraph_index(整数), node_id, before_anchor, after_anchor, original_text
  operation: "append"(续写) | "insert"(插入) | "replace"(替换)
  ⚠️ 推荐使用 operate_apply 代替直接调用此工具
  ⚠️ operate_apply 不会自动定位，必须传 node_id/paragraph_index

- locate_content: ⚠️ **内部定位工具（不会被 operate_apply 自动调用）**
  参数: chapter_id, query, nodes_info(可选)
  ⚠️ **重要：需要先调用 locate_content 或 list_paragraphs/read_paragraphs 获取 node_id/paragraph_index**
  ⚠️ 跨章节降级已禁用（allow_global_fallback=false）
  ⚠️ **唯一例外**：如果用户未指定章节，需要先用 explore_content 找到章节，再传给 operate_apply
"""


def _get_read_tools_section() -> str:
    """读取工具描述（内部工具，由 explore_content 调用）"""
    return """
【内部读取工具 - ⚠️ 禁止直接使用！】

以下工具已整合到 explore_content：
- get_chapter_by_order_tool → 使用 explore_content
- read_chapter_tool → 使用 explore_content
- get_context_tool → 使用 explore_content
- get_worldview_summary → 使用 explore_content

✅ **正确做法**：使用 explore_content(target_task="你的读取需求")
"""


def _get_creative_tools_section() -> str:
    """创作增强工具描述（情感、场景、风格）"""
    return """
【创作增强工具】
- show_emotion_tool: 情感展示工具（Show Don't Tell）
  参数: emotion(目标情感，如"生气"/"高兴"/"悲伤"/"害怕"), intensity(强度1-5，默认3)
  用途: 将抽象情绪转换为具体的感官描写
  示例: emotion="生气" → 返回愤怒的具体表现（动作、神态、环境）

- enhance_scene_tool: 场景增强工具
  参数: description(原始场景描述)
  用途: 增强场景描写的感官细节和画面感
  示例: 增加环境描写、感官细节、氛围渲染

- learn_style_tool: 风格学习工具
  参数: user_id(用户ID), text(样本文本), profile_name(档案名称，默认"default")
  用途: 从样本中学习写作风格特征
  返回: 风格特征分析报告
"""


def _get_operation_tools_section() -> str:
    """章节操作工具描述（创建、更新、删除）"""
    return """
【章节操作工具】⚠️ 这些操作会修改数据，需谨慎使用
- create_chapter: 创建新章节
  参数: work_id, title, content(可选), order(可选)
  用途: 在作品中创建新章节
  ⚠️ 创建前应确认用户意图，避免误创建

- update_chapter_title: 更新章节标题
  参数: chapter_id（支持章节序号如"1"、"2"，或UUID）, new_title
  用途: 修改章节标题
  触发词: "改标题"、"重命名章节"
  ⚠️ 可以直接使用章节序号，无需先获取章节信息

- update_chapter_content: 更新章节内容
  参数: chapter_id（支持章节序号如"1"、"2"，或UUID）, new_content, operation(replace/append/insert，默认replace)
  用途: 直接更新章节内容
  ⚠️ 优先使用 smart_rewrite/smart_continue，它们会生成稳定的单版本内容

- delete_chapter: 删除章节
  参数: chapter_id（支持章节序号如"1"、"2"，或UUID）
  用途: 删除指定章节
  ⚠️ 危险操作！必须先确认用户意图，建议先询问确认
"""


def _get_analysis_tools_section() -> str:
    """分析工具描述（一致性检查、风格分析）"""
    return """
【分析工具】⚠️ 已有聚合工具，请优先使用 analyze_content（仅用于一致性/风格/质量/打分等结构化评估）
- check_story_consistency_tool: 故事一致性检查（兼容）
  参数: work_id, chapters_json(章节JSON，默认"[]"), characters_json(角色JSON，默认"[]"), worldview_json(世界观JSON，默认"{}")
  用途: 检查故事中的逻辑漏洞、人设矛盾、时间线错误
  返回: 一致性问题列表及修复建议
  触发词: "检查一致性"、"有没有矛盾"、"逻辑漏洞"

- analyze_style_tool: 风格分析工具（兼容）
  参数: text(待分析文本)
  用途: 分析文本的写作风格特征
  返回: 句式特点、用词偏好、节奏分析、风格标签
  触发词: "分析风格"、"写作特点"

- get_style_guidance_tool: 获取风格指导
  参数: user_id(用户ID), profile_name(档案名称，默认"default")
  用途: 基于用户已学习的风格档案，给出写作指导建议
  返回: 风格指南、用词建议、句式参考
  触发词: "风格指导"、"怎么保持风格一致"
"""


def _get_explore_tools_section() -> str:
    """探索工具描述（2026-01-18 更新：已在聚合工具部分详细描述）"""
    return """
【探索工具 - 参见顶部统一入口说明】

explore_content 的详细说明已在顶部【统一信息获取入口】部分。

- read_paragraph: 精确读取段落原文（explore_content 内部使用，通常不需要直接调用）
"""


def get_all_tools_description() -> str:
    """获取所有工具的完整描述"""
    return (
        _get_new_aggregated_tools_section() +  # 🔴 新聚合工具放在最前面！
        _get_retrieval_tools_section() +
        _get_editor_tools_section() +
        _get_explore_tools_section() +  # 探索工具（2026-01-17 新增）
        _get_read_tools_section() +
        _get_creative_tools_section() +
        _get_operation_tools_section() +
        _get_analysis_tools_section()
    )


# 导出
__all__ = [
    "_get_new_aggregated_tools_section",  # 新增
    "_get_retrieval_tools_section",
    "_get_editor_tools_section",
    "_get_explore_tools_section",  # 探索工具（2026-01-17 新增）
    "_get_read_tools_section",
    "_get_creative_tools_section",
    "_get_operation_tools_section",
    "_get_analysis_tools_section",
    "get_all_tools_description",
]
