  ---
  10个复杂测试Prompt

  Prompt 1 - 搜索+改写+情感展示

  帮我找到段融第一次吞噬器灵的场景，然后用"展示而非告诉"的手法改写他内心的兴奋和紧张，让读者能感受到他发现自己能力可用时的激动心情。
  预期触发工具: search_analysis_fragments_tool → smart_rewrite → show_emotion_tool

  ---
  Prompt 2 - 读取+续写+场景增强

  读取第3章"一夕千悟"的内容，然后帮我续写500字，描写段融在月光下练刀的场景，要增强环境描写的感官细节，让画面更有氛围感。
  预期触发工具: get_chapter_by_order_tool → smart_continue → enhance_scene_tool

  ---
  Prompt 3 - 风格学习+风格分析+风格指导

  分析这部小说前三章的写作风格特点，学习作者的文风，然后给我一份风格指导，告诉我如何保持与原作一致的写作风格来续写后续章节。
  预期触发工具: analyze_style_tool → learn_style_tool → get_style_guidance_tool

  ---
  Prompt 4 - 世界观查询+一致性检查

  查看这部小说的世界观设定，包括器灵等阶系统、精神力等级、源顺镖局的人物关系，然后检查前三章是否存在设定矛盾或逻辑漏洞。
  预期触发工具: get_worldview_summary → check_story_consistency_tool

  ---
  Prompt 5 - 搜索+分析+改写

  搜索赵穆出现的所有场景，分析他的人物形象塑造是否立体，然后帮我改写第1章中赵穆第一次出场的描写，让他的性格特点更加鲜明。
  预期触发工具: search_analysis_fragments_tool → analyze_text_tool → smart_rewrite

  ---
  Prompt 6 - 创建章节+插入内容

  帮我创建第4章，标题叫"初露锋芒"，然后在章节开头插入一段承上启下的过渡内容，衔接第3章段融练刀的情节，描写他第二天早上醒来的状态。
  预期触发工具: create_chapter → smart_insert

  ---
  Prompt 7 - 获取上下文+续写+应用编辑

  获取当前作品的完整上下文，然后帮我续写一段段融在考核中展示五虎群羊刀法的精彩打斗场面，写完后直接应用到编辑器中。
  预期触发工具: get_context_tool → smart_continue → apply_chapter_edit

  ---
  Prompt 8 - 读取多章+分析+更新标题

  读取第1章到第3章的内容，分析每章的核心情节，然后帮我把第2章的标题从"浑圆桩"改成更能体现章节内容的标题。
  预期触发工具: get_chapter_by_order_tool(范围读取) → analyze_text_tool → update_chapter_title

  ---
  Prompt 9 - 搜索+情感展示+场景增强+改写

  找到段融被其他杂役弟子嫌弃"一身马粪味"的场景，用展示手法重写他内心的窃喜情绪，同时增强马厩环境的感官描写（气味、声音、光线），让这个场景更加生动立体。
  预期触发工具: search_analysis_fragments_tool → show_emotion_tool → enhance_scene_tool → smart_rewrite

  ---
  Prompt 10 - 全流程测试（查询+分析+创作+操作）

  先查看世界观中关于器灵等阶的设定，然后分析第1章中段融读取器灵数据的描写风格，学习这种"系统面板"的写作手法，最后帮我创建一个新章节，写段融吞噬一件更高阶器物时的系统提示和他的反应，要保持风格一致，写完后更新到章节内容中。
  预期触发工具: get_worldview_summary → search_analysis_fragments_tool → analyze_style_tool → learn_style_tool → create_chapter → update_chapter_content

  ---
  工具覆盖矩阵
  Prompt: 1
  覆盖的工具: search_analysis_fragments_tool, smart_rewrite, show_emotion_tool
  ────────────────────────────────────────
  Prompt: 2
  覆盖的工具: get_chapter_by_order_tool, smart_continue, enhance_scene_tool
  ────────────────────────────────────────
  Prompt: 3
  覆盖的工具: analyze_style_tool, learn_style_tool, get_style_guidance_tool
  ────────────────────────────────────────
  Prompt: 4
  覆盖的工具: get_worldview_summary, check_story_consistency_tool
  ────────────────────────────────────────
  Prompt: 5
  覆盖的工具: search_analysis_fragments_tool, analyze_text_tool, smart_rewrite
  ────────────────────────────────────────
  Prompt: 6
  覆盖的工具: create_chapter, smart_insert
  ────────────────────────────────────────
  Prompt: 7
  覆盖的工具: get_context_tool, smart_continue, apply_chapter_edit
  ────────────────────────────────────────
  Prompt: 8
  覆盖的工具: get_chapter_by_order_tool, analyze_text_tool, update_chapter_title
  ────────────────────────────────────────
  Prompt: 9
  覆盖的工具: search_analysis_fragments_tool, show_emotion_tool, enhance_scene_tool, smart_rewrite
  ────────────────────────────────────────
  Prompt: 10
  覆盖的工具: get_worldview_summary, search_analysis_fragments_tool, analyze_style_tool, learn_style_tool, create_chapter,
    update_chapter_content
  未直接覆盖的工具:
  - read_chapter_tool - 可在Prompt 2/7中替代 get_chapter_by_order_tool
  - delete_chapter - 危险操作，建议单独测试："删除第4章"

  这10个prompt设计为复杂的多步骤任务，能够测试工具的组合调用能力和参数传递是否正确。