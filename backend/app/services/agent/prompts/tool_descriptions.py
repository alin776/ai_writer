"""
工具描述模块 - 单一数据源

所有工具的描述集中管理，避免多个 Prompt 不同步。
被 decision_prompts.py 和 planning_prompts.py 共同引用。
"""


def _get_new_aggregated_tools_section() -> str:
    """新聚合工具描述（优先使用！）"""
    return """
【🔴 新聚合工具 - 优先使用！】

⚠️ **重要：优先使用新聚合工具，减少工具调用次数！**

| 旧工具 | 新工具 | 说明 |
|--------|--------|------|
| get_chapter_by_order_tool | get_writing_context | 一站式获取上下文 |
| read_chapter_tool | get_writing_context | 支持批量读取 |
| get_worldview_summary | get_writing_context | include="worldview" |
| get_context_tool | get_writing_context | include="work,rag" |
| analyze_text_tool | analyze_content | 一站式分析 |

---

- get_writing_context: 🔴 一站式获取创作上下文（推荐！）
  参数:
    - chapter_orders: 章节序号，支持 "5" / "1,2,3" / "1-5"
    - chapter_id: 章节UUID（与 chapter_orders 二选一）
    - include: 包含内容类型，逗号分隔
      * "work" - 作品信息
      * "chapter" - 章节内容
      * "worldview" - 世界观（角色、地点、设定）
      * "rag" - RAG检索相关内容
      * "style" - 风格指导
    - rag_query: RAG查询（可选）
    - rag_top_k: RAG返回数量（默认5）
  返回: {work_info, chapters[], worldview, rag_context[], style_guidance}

  ✅ 使用示例：
    - 续写前获取上下文: get_writing_context(chapter_orders="5", include="work,chapter,worldview,rag")
    - 批量读取章节: get_writing_context(chapter_orders="1-5", include="chapter")
    - 只获取世界观: get_writing_context(include="worldview")

  ⚠️ 对比旧方式：
    - 旧：get_worldview_summary + get_chapter_by_order_tool + get_context_tool（3次调用）
    - 新：get_writing_context（1次调用）

---

- analyze_content: 🔴 一站式内容分析（推荐！）
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

  ✅ 使用示例：
    - 检查问题: analyze_content(content="...", aspects=["grammar", "logic"])
    - 深度分析: analyze_content(content="...", aspects=["style", "structure"], depth="deep")
    - 风格分析: analyze_content(content="...", analysis_types=["style"])
"""


def _get_retrieval_tools_section() -> str:
    """检索工具描述"""
    return """
【检索工具 - 纯搜索/查询场景使用】
- search_content: 混合检索（向量+全文）召回作品相关片段（返回snippet）
  参数: work_id(必需), query(必需), top_k(默认10, ≤50), chapter_id(可选), look_ahead(默认0=不限制)
  → 适用场景（仅用于查询，不用于修改！）:
    - 用户只是想**查找/搜索**内容: "哪里提到了XX"、"找一下XX相关的内容"
    - 用户想**了解**某内容在哪: "赵穆出现在哪"、"关于源顺镖局的描述"
  ⚠️ **禁止场景**（不要用此工具！）:
    - 用户要**修改/改写/润色**某内容 → 用 locate_content！
    - 用户要**插入/续写**内容 → 用 locate_content！
    - 任何需要返回 paragraph_index 的场景 → 用 locate_content！
  ✅ **符合场景时的三步链路**：
    - 用户要修改/插入但**未说明章节** → search_content 找章 → get_writing_context 读章 → locate_content 精确定位

⚠️ 【搜索 query 提取规则 - 极其重要！】
提取用户描述中的**核心动作/事件/专有名词**作为搜索词，保持完整性！

✅ 正确提取示例：
- "段融第一次吞噬器灵的场景" → query: "吞噬器灵" 或 "段融 吞噬器灵"
- "主角觉醒的描写" → query: "觉醒"
- "赵穆和段融的对话" → query: "赵穆 段融"
- "描写战斗的片段" → query: "战斗"
- "关于源顺镖局的描述" → query: "源顺镖局"

❌ 错误提取示例（绝对禁止！）：
- "段融第一次吞噬器灵的场景" → query: "灵的场景" ❌ (拆分了专有名词"吞噬器灵")
- "主角觉醒的描写" → query: "的描写" ❌ (丢失了核心词"觉醒")

**关键原则**：
1. 专有名词/动作词组必须保持完整（如"吞噬器灵"、"源顺镖局"、"金丹期"）
2. 优先提取动词+宾语组合（如"吞噬器灵"而非"器灵"）
3. 人物名+动作组合效果更好（如"段融 吞噬器灵"）
4. 不要只提取"的场景"、"的描写"等无意义后缀
5. **提取技巧**：找到用户描述中"第一次/首次/开始"后面紧跟的动作词组，这通常是核心搜索词
   - "第一次吞噬器灵" → 提取 "吞噬器灵"
   - "首次突破金丹" → 提取 "突破金丹"

⚠️ 【检索规则 - 强制执行】
- 用户只是想**查询/搜索**内容位置 → 用 search_content
- 用户要**修改/改写/插入**内容 → 用 locate_content（返回 paragraph_index）
- **禁止不检索就直接回答"没有找到"或"不存在"！必须先检索确认！**
"""


def _get_editor_tools_section() -> str:
    """编辑器工具描述（直接修改章节内容）"""
    return """
【编辑器工具 - 修改内容时优先使用】

⚠️ **核心规则：创作类 vs 操作类**
- 创作类工具（smart_continue, smart_insert, smart_rewrite）：只生成内容，不写入编辑器
- 操作类工具（apply_chapter_edit）：将内容写入编辑器

⚠️ **什么时候需要调用 apply_chapter_edit？**
- 用户说"续写"、"插入"、"改写"、"润色" → 需要！（内容要写入编辑器）
- 用户说"帮我写一段XX"、"生成一个大纲" → 不需要！（只是看内容，不写入编辑器）

⚠️ **创作类工具 → 操作类工具的对应关系**
- smart_continue → apply_chapter_edit(operation="append")
- smart_insert → apply_chapter_edit(operation="insert")
- smart_rewrite → apply_chapter_edit(operation="replace")

---

- smart_rewrite: 改写/修改章节内容（生成3个版本供选择）
  参数: chapter_id, text_to_rewrite, user_requirement, base_version
  触发词: "修改"、"改写"、"重写"、"润色"、"优化"、"扩写"
  ⚠️ "扩写"= 把现有内容写得更丰富，属于改写场景，不是续写！
  ⚠️ 如果用户想把改写内容写入编辑器 → 后续调用 apply_chapter_edit(operation="replace")
  ⚠️ **参数填充规则**（极其重要！）：
    * 如果用户指定了要改写的文本 → text_to_rewrite 填入该文本
    * 如果用户说"改写第X章" → 先用 get_writing_context 获取章节，再用 {"$ref": {"task_id": N, "path": "chapters[0].content"}} 引用
    * user_requirement 必须从用户消息中提取改写要求！

- smart_continue: 智能续写（只生成内容）
  参数: chapter_id, chapter_content, user_requirement, word_count
  触发词: "续写"、"继续写"、"往后写"
  ⚠️ 如果用户想把续写内容写入编辑器 → 后续调用 apply_chapter_edit(operation="append")

- smart_insert: 智能插入（只生成内容）
  参数: chapter_id, user_intent, chapter_content, insert_context, word_count
  触发词: "插入"、"在...处添加"、"在...后面加"
  ⚠️ 如果用户想把插入内容写入编辑器 → 后续调用 apply_chapter_edit(operation="insert")
  ⚠️ **定位规则**：插入位置由 locate_content 工具确定，smart_insert 只负责生成内容
  ⚠️ insert_context 可以从 locate_content 返回的 text 获取，用于风格参考

- apply_chapter_edit: 将已生成的内容应用到编辑器（操作类工具）
  参数: chapter_id, operation, content, paragraph_index(整数), node_id, before_anchor, after_anchor, original_text
  operation: "append"(续写) | "insert"(插入) | "replace"(替换)
  ⚠️ 此工具用于将创作类工具生成的内容写入编辑器
  ⚠️ **必须在创作类工具之后调用**：先创作，后应用！

  ⚠️ **参数类型约束（必须严格遵守！）**：
    * paragraph_index: 【必须是整数】如 0、1、2。从 locate_content 获取
    * node_id: 【字符串】节点ID，从 locate_content 获取
    * before_anchor/after_anchor: 【文本】锚点字符串

  ❌ **错误示例（绝对禁止！）**：
    * position="before" ❌ 错误！不要传 position 参数！
    * position="after" ❌ 错误！
    * paragraph_index="第三段" ❌ 错误！必须是整数如 2

  ✅ **正确做法**：
    * 插入/替换操作 → 先调用 locate_content 获取 paragraph_index 和 node_id
    * 然后将 locate_content 返回的整数 paragraph_index 传入此工具
    * 示例：locate_content 返回 paragraph_index=2 → apply_chapter_edit(paragraph_index=2)

- locate_content: 定位章节中的内容位置（**修改前必须调用！**）
  参数: chapter_id, query, nodes_info(可选)
  query: "第三段"、"开头"、"结尾"、"段融吞噬器灵的场景"、具体文本片段
  返回: chapter_id, paragraph_index, text_preview, before_anchor, after_anchor, node_id, text, cross_chapter
  ⚠️ nodes_info 仅来自前端/上下文；get_writing_context 不返回 nodes，禁止引用 chapters[*].nodes。
  ⚠️ **核心用途**：为 apply_chapter_edit 提供定位信息（paragraph_index, node_id）
  ⚠️ **跨章节定位**：如果内容不在当前章节，会自动全局搜索并返回目标章节的 chapter_id
    * 返回的 chapter_id 可能与传入的不同（cross_chapter=true）
    * **必须使用返回的 chapter_id 调用 smart_rewrite 和 apply_chapter_edit**
  ⚠️ **必须使用场景**：
    * 用户要**改写/润色/修改**某内容 → 先用 locate_content 定位！
    * 用户要**插入**内容到某位置 → 先用 locate_content 定位！
    * 用户说"找到XX场景，改写它" → 先用 locate_content 定位！
    * 用户指定模糊位置（如"第三段"、"开头"）→ 先用 locate_content 定位！
  ⚠️ **工作流程**：locate_content → smart_rewrite/smart_insert → apply_chapter_edit
  ⚠️ **参数传递**：locate_content 返回的 chapter_id、paragraph_index 和 node_id 必须传给后续工具
    * 示例：smart_rewrite(chapter_id={"$ref": {"task_id": 1, "path": "chapter_id"}}, ...)
    * 示例：apply_chapter_edit(chapter_id={"$ref": {"task_id": 1, "path": "chapter_id"}}, paragraph_index={"$ref": {"task_id": 1, "path": "paragraph_index"}}, ...)
"""


def _get_read_tools_section() -> str:
    """读取工具描述（已废弃，请使用 get_writing_context）"""
    return """
【读取工具】⚠️ 已废弃，请优先使用 get_writing_context！

以下工具已被 get_writing_context 替代，仅保留向后兼容：
- get_chapter_by_order_tool → 请用 get_writing_context(chapter_orders="1-5", include="chapter")
- read_chapter_tool → 请用 get_writing_context(chapter_id="xxx", include="chapter")
- get_context_tool → 请用 get_writing_context(include="work,rag")
- get_worldview_summary → 请用 get_writing_context(include="worldview")
- analyze_text_tool → 请用 analyze_content(content="...", aspects=["style"])
- search_analysis_fragments_tool → 请用 search_content(query="...", top_k=10)
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
  ⚠️ 优先使用 smart_rewrite/smart_continue，它们有版本选择功能

- delete_chapter: 删除章节
  参数: chapter_id（支持章节序号如"1"、"2"，或UUID）
  用途: 删除指定章节
  ⚠️ 危险操作！必须先确认用户意图，建议先询问确认
"""


def _get_analysis_tools_section() -> str:
    """分析工具描述（一致性检查、风格分析）"""
    return """
【分析工具】⚠️ 已有聚合工具，请优先使用 analyze_content
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


def get_all_tools_description() -> str:
    """获取所有工具的完整描述"""
    return (
        _get_new_aggregated_tools_section() +  # 🔴 新聚合工具放在最前面！
        _get_retrieval_tools_section() +
        _get_editor_tools_section() +
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
    "_get_read_tools_section",
    "_get_creative_tools_section",
    "_get_operation_tools_section",
    "_get_analysis_tools_section",
    "get_all_tools_description",
]
