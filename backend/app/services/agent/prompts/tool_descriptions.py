"""
工具描述模块 - 单一数据源

所有工具的描述集中管理，避免多个 Prompt 不同步。
被 decision_prompts.py 和 planning_prompts.py 共同引用。
"""


def _get_retrieval_tools_section() -> str:
    """检索工具描述"""
    return """
【检索工具 - 内容搜索场景使用】
- search_analysis_fragments_tool: 混合检索（向量+全文）召回作品相关片段
  参数: query(必需), top_k(默认5), work_id(可选), chapter_id(可选)
  → 适用场景:
    - 用户给出具体文字片段但不知道在哪章: "微光如露落雪在哪"
    - 搜索包含某关键词的内容: "哪里提到了XX"、"找一下XX相关的内容"
    - 查找人物/地点/设定相关描述: "赵穆出现在哪"、"关于源顺镖局的描述"
    - ⚠️ 用户提到人物名但未指定章节: "帮我改写赵穆的描写" → 先搜索赵穆出现位置

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
- 用户提到具体文字/关键词但不知位置 → 必须先调用 search_analysis_fragments_tool
- 用户问"XX在哪"/"哪里提到XX" → 必须先调用 search_analysis_fragments_tool
- ⚠️ 用户提到人物名（如"赵穆"）但未说在哪章 → 必须先调用 search_analysis_fragments_tool 定位
- **禁止不检索就直接回答"没有找到"或"不存在"！必须先检索确认！**
- **禁止直接读取"当前章节"然后说"XX未出现"！必须先检索确认XX在哪些章节！**
"""


def _get_editor_tools_section() -> str:
    """编辑器工具描述（直接修改章节内容）"""
    return """
【编辑器工具 - 修改内容时优先使用】
- smart_rewrite: 改写/修改章节内容（生成3个版本供选择）
  参数: chapter_id, text_to_rewrite, user_requirement, base_version
  触发词: "修改"、"改写"、"重写"、"润色"、"优化"、"扩写"
  ⚠️ "扩写"= 把现有内容写得更丰富，属于改写场景，不是续写！
  ⚠️ **参数填充规则**（极其重要！）：
    * 如果用户指定了要改写的文本 → text_to_rewrite 填入该文本
    * 如果用户说"改写第X章" → 先用 get_chapter_by_order_tool 获取章节，再用 $TASK_N.content$ 引用
    * user_requirement 必须从用户消息中提取改写要求！

- smart_continue: 智能续写（根据上下文生成续写内容）
  参数: chapter_id, chapter_content, user_requirement, word_count
  触发词: "续写"、"继续写"、"往后写"
  📌 写入编辑器: 添加 apply_to_editor=true, operation="append"

- smart_insert: 智能插入（根据意图生成插入内容）
  参数: chapter_id, user_intent, chapter_content, insert_context, word_count
  触发词: "插入"、"在...处添加"

- apply_chapter_edit: 直接应用编辑到章节
  参数: chapter_id, operation, content
  ⚠️ 此工具用于将已生成的内容应用到编辑器
"""


def _get_read_tools_section() -> str:
    """读取工具描述"""
    return """
【读取工具】
- get_chapter_by_order_tool: 按序号获取章节（支持批量！）
  参数: chapter_order，支持三种格式：
    - 单个: "1"
    - 多个: "1,2,3,4,5"
    - 范围: "1-5"（一次性读取第1到第5章）
  返回: {title, order, content, word_count}
  ⚠️ 需要读取多章时，用范围格式 "1-5" 一次读取，避免生成多个读取任务！

- read_chapter_tool: 读取指定章节的完整内容
  参数: chapter_id（支持多个，用逗号分隔）
  需要: work_id

- get_context_tool: 获取作品上下文
  参数: work_id
  返回: 作品信息、章节内容、相关分析

- get_worldview_summary: 查询世界观信息
  触发词: "世界观里有什么"、"有哪些角色/地点/设定"
  返回: 角色、地点、设定等世界观信息

- analyze_text_tool: 分析文本（不需要work_id）
  参数: text, focus
  ⚠️ focus 参数必须简洁（15字以内）
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
  参数: chapter_id, new_title
  用途: 修改章节标题
  触发词: "改标题"、"重命名章节"

- update_chapter_content: 更新章节内容
  参数: chapter_id, new_content, operation(replace/append/prepend，默认replace)
  用途: 直接更新章节内容
  ⚠️ 优先使用 smart_rewrite/smart_continue，它们有版本选择功能

- delete_chapter: 删除章节
  参数: chapter_id
  用途: 删除指定章节
  ⚠️ 危险操作！必须先确认用户意图，建议先询问确认
"""


def _get_analysis_tools_section() -> str:
    """分析工具描述（一致性检查、风格分析）"""
    return """
【分析工具】
- check_story_consistency_tool: 故事一致性检查
  参数: work_id, chapters_json(章节JSON，默认"[]"), characters_json(角色JSON，默认"[]"), worldview_json(世界观JSON，默认"{}")
  用途: 检查故事中的逻辑漏洞、人设矛盾、时间线错误
  返回: 一致性问题列表及修复建议
  触发词: "检查一致性"、"有没有矛盾"、"逻辑漏洞"

- analyze_style_tool: 风格分析工具
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
        _get_retrieval_tools_section() +
        _get_editor_tools_section() +
        _get_read_tools_section() +
        _get_creative_tools_section() +
        _get_operation_tools_section() +
        _get_analysis_tools_section()
    )


# 导出
__all__ = [
    "_get_retrieval_tools_section",
    "_get_editor_tools_section",
    "_get_read_tools_section",
    "_get_creative_tools_section",
    "_get_operation_tools_section",
    "_get_analysis_tools_section",
    "get_all_tools_description",
]
