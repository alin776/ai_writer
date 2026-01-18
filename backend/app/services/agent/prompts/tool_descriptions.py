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
    - max_rounds: 最大探索轮数（默认10，简单任务1轮即返回）
  返回: {
    explore_summary,      # 收集到的信息摘要（供后续工具使用）
    context_for_task,     # 可直接作为 chapter_content 的上下文
    frontend_display,     # 前端展示结构
    chapters,            # 相关章节原文（列表）
    worldview            # 世界观设定
  }

  ✅ **所有信息获取场景都用这个工具**:
    - 续写/改写前获取上下文 → explore_content(target_task="续写第5章，需要第4-5章内容和世界观")
    - 分析人物/情节 → explore_content(target_task="分析主角性格特点，收集相关描写")
    - 搜索/查找内容 → explore_content(target_task="找出所有关于XX的描写")
    - 获取世界观设定 → explore_content(target_task="获取世界观和角色设定")
    - 批量读取章节 → explore_content(target_task="读取第1-5章内容")

  ⚠️ **工作原理**（你不需要关心，explore_content 自动处理）:
    - 简单查询 → 首轮即返回
    - 复杂查询 → 自动多轮探索
    - 信息收敛 → 自动停止

  ⚠️ **禁止直接使用以下工具**（这些是内部工具）:
    - ❌ search_content（已整合到 explore_content）
    - ❌ get_writing_context（已整合到 explore_content）
    - ❌ get_chapter_by_order（已整合到 explore_content）

---

- analyze_content: 🔴 一站式内容分析
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
    """检索工具描述（内部工具，由 explore_content 调用）"""
    return """
【内部检索工具 - ⚠️ 禁止直接使用！】

以下工具已整合到 explore_content，请使用 explore_content 代替：

- search_content: ❌ 内部工具（由 explore_content 自动调用）
- get_writing_context: ❌ 内部工具（由 explore_content 自动调用）

✅ **正确做法**：使用 explore_content(target_task="你的查询需求")
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
