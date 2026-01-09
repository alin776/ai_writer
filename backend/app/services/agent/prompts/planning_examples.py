"""
规划示例模块

包含所有 Planning Prompt 的 JSON 示例：
- 直接回答示例（知识问答、问候）
- 用户确认后执行示例
- 分阶段执行示例
- 创作请求示例
- 搜索示例
- 选中文本示例
- 多章节读取示例
- Agent 模式示例
"""


def get_direct_answer_examples() -> str:
    """直接回答示例（不需要工具的情况）"""
    return """【直接回答示例】⚠️ 不需要工具的情况

用户: "怎样写好人物对话？"
{
  "thinking": {
    "step1_output": "用户在问写作技巧，期望得到建议和方法",
    "step2_material": "不需要，这是知识问答",
    "step3_process": "直接回答写作技巧"
  },
  "user_intent": "咨询人物对话写作技巧",
  "output_title": "写作建议",
  "direct_answer": "💡 **写好人物对话的关键技巧**：\\n\\n| 技巧 | 说明 |\\n|-----|-----|\\n| ✅ 符合人设 | 每个角色说话方式应该不同，反映其性格、背景 |\\n| ✅ 推动剧情 | 对话不是闲聊，要传递信息或推动故事发展 |\\n| ✅ 留白与潜台词 | 不要把所有意思都说出来，让读者去体会 |\\n| ✅ 节奏控制 | 长短句交替，紧张时用短句，舒缓时可以稍长 |\\n\\n> 📌 **核心要点**：避免让角色像在念课文，要自然！",
  "tasks": []
}

用户: "你是谁？"
{
  "thinking": {
    "step1_output": "用户在问我的身份，是简单问答",
    "step2_material": "不需要",
    "step3_process": "直接回答"
  },
  "user_intent": "询问身份",
  "direct_answer": "👋 我是 **AI 写作助手**，可以帮助你：\\n\\n- ✍️ 小说创作与续写\\n- 📊 内容分析与诊断\\n- 📝 大纲规划与设计\\n- 🔧 文本润色与改写\\n\\n有什么可以帮你的？",
  "tasks": []
}

用户: "谢谢你的帮助"
{
  "thinking": {
    "step1_output": "用户在表示感谢，是礼貌性回应",
    "step2_material": "不需要",
    "step3_process": "直接回答"
  },
  "user_intent": "表示感谢",
  "direct_answer": "😊 不客气！如果还有其他需要帮助的地方，随时告诉我~",
  "tasks": []
}

【计划确认示例】🤝 意图不明确时先询问

用户: "帮我改写一下这段"
{
  "thinking": {
    "step1_output": "用户想改写，但没说改写哪段、怎么改，意图不明确",
    "step2_material": "需要确认目标文本和改写方向",
    "step3_process": "询问用户补充信息"
  },
  "user_intent": "改写文本（待确认）",
  "direct_answer": "好的，我来帮你改写。请问：\\n\\n1. 你想改写的是哪一段文字？（可以直接选中文本，或告诉我在第几章）\\n2. 你希望怎样改写？（比如：更有画面感、更简洁、更有文采等）",
  "tasks": []
}
"""


def get_user_confirmation_examples() -> str:
    """用户确认后执行示例"""
    return """【用户确认后执行示例】⚠️ 用户说"可以"/"好的"/"开始"时，必须生成 tasks

对话历史（实际格式）:
【对话历史】
用户: 帮我续写第5章的战斗场景
助手: 我理解你想续写第5章的战斗场景。我打算这样做：1. 读取第5章内容 2. 分析现有的战斗风格 3. 续写约500字的战斗场景。你觉得这个计划可以吗？

用户: "好的，开始吧"
{
  "thinking": {
    "step1_output": "用户确认了计划，需要立即执行之前讨论的方案",
    "step2_material": "需要第5章内容",
    "step3_process": "执行之前讨论的计划：读取→分析→续写500字"
  },
  "user_intent": "执行之前讨论的续写计划",
  "output_title": "续写内容",
  "tasks": [
    {"task_id": 1, "description": "获取第5章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 5}},
    {"task_id": 2, "description": "分析战斗风格", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "战斗风格分析"}},
    {"task_id": 3, "description": "续写500字战斗场景", "tool": "smart_continue", "params": {"chapter_content": "$TASK_1.content$", "user_requirement": "续写战斗场景，保持现有风格", "word_count": 500}}
  ]
}

用户: "可以，直接写1000字"
{
  "thinking": {
    "step1_output": "用户确认了计划并调整了字数要求，可以直接执行",
    "step2_material": "需要第5章内容",
    "step3_process": "按用户调整后的方案执行，1000字"
  },
  "user_intent": "续写1000字战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取第5章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 5}},
    {"task_id": 2, "description": "续写1000字战斗场景", "tool": "smart_continue", "params": {"chapter_content": "$TASK_1.content$", "user_requirement": "续写战斗场景", "word_count": 1000}}
  ]
}

用户: "不用分析，直接续写"
{
  "thinking": {
    "step1_output": "用户确认了计划，但跳过分析步骤，直接续写",
    "step2_material": "需要第5章内容",
    "step3_process": "按用户调整后的方案执行，跳过分析"
  },
  "user_intent": "直接续写第5章战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取第5章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 5}},
    {"task_id": 2, "description": "续写战斗场景", "tool": "smart_continue", "params": {"chapter_content": "$TASK_1.content$", "user_requirement": "续写战斗场景", "word_count": 500}}
  ]
}
"""


def get_staged_execution_examples() -> str:
    """分阶段执行示例"""
    return """【分阶段执行示例】📊 复杂任务分阶段，关键节点征求反馈

用户: "帮我续写后面5个章节"
{
  "thinking": {
    "step1_output": "用户想续写5个章节，这是大型创作任务，应该分阶段执行",
    "step2_material": "需要先读取现有内容",
    "step3_process": "第一阶段：分析现有内容并规划大纲，征求用户确认后再续写"
  },
  "user_intent": "续写后5章（分阶段执行）",
  "tasks": [
    {"task_id": 1, "description": "获取最近章节", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": "-3"}},
    {"task_id": 2, "description": "分析情节走向并规划大纲", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.chapters$", "focus": "情节走向分析"}}
  ]
}
⚠️ 注意：这个任务只生成了分析阶段，执行完成后 AI 会在响应中说："我分析了现有内容，这是后5章的大纲规划...你觉得这个方向可以吗？确认后我会开始续写第一章。"

用户: "可以，先写第6章"
{
  "thinking": {
    "step1_output": "用户确认了大纲方向，现在开始续写第6章",
    "step2_material": "需要之前的分析结果（在对话历史中）",
    "step3_process": "续写第6章"
  },
  "user_intent": "续写第6章",
  "tasks": [
    {"task_id": 1, "description": "获取第5章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 5}},
    {"task_id": 2, "description": "续写第6章", "tool": "smart_continue", "params": {"chapter_content": "$TASK_1.content$", "user_requirement": "基于之前规划的大纲续写第6章", "word_count": 3000}}
  ]
}

用户: "大纲不太对，第6章应该是主角觉醒的情节"
{
  "thinking": {
    "step1_output": "用户对大纲有调整意见，需要重新规划",
    "step2_material": "用户的调整意见",
    "step3_process": "在 direct_answer 中确认调整后的方向"
  },
  "user_intent": "调整大纲方向",
  "direct_answer": "好的，我理解了。调整后的规划：\\n\\n**第6章**：主角觉醒，发现自己的隐藏能力\\n**第7章**：...\\n\\n这样的方向可以吗？确认后我开始续写。",
  "tasks": []
}
"""


def get_creation_request_examples() -> str:
    """创作请求示例（分阶段执行）"""
    return """【需要工具的示例】⚠️ 创作类请求 - 分阶段执行

用户: "帮我写第一章"
{
  "thinking": {
    "step1_output": "用户要创作第一章，这是创作请求，应该分阶段执行",
    "step2_material": "⚠️ 统一策略：获取[世界观 + 前一章 + 目标章节]三个。第一章：第0章+第1章（可能都为空）",
    "step3_process": "第一阶段：同时获取世界观、第0章、第1章，然后基于已有内容询问创作细节"
  },
  "user_intent": "创作第一章（分阶段）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取作品世界观", "tool": "get_worldview_summary", "params": {"work_id": ""}},
    {"task_id": 2, "description": "读取第0章（如果存在）", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 0}},
    {"task_id": 3, "description": "读取第1章（如果存在）", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}}
  ]
}

用户: "3000字，激昂风格，重点介绍主角"
{
  "thinking": {
    "step1_output": "用户确认了创作细节，现在可以开始创作",
    "step2_material": "世界观信息（在对话历史中已获取）",
    "step3_process": "生成创作任务，使用用户提供的参数"
  },
  "user_intent": "创作第一章（用户已确认参数）",
  "tasks": [
    {"task_id": 1, "description": "创作第一章", "tool": "smart_continue", "params": {"context": "世界观：主角陈羽，青云宗等场景，力量体系为境界修炼", "requirements": "创作第一章，3000字，激昂风格，重点介绍主角", "target_words": 3000}}
  ]
}

用户: "续写第二章"
{
  "thinking": {
    "step1_output": "用户要续写第二章，这是创作请求，应该分阶段执行",
    "step2_material": "⚠️ 统一策略：获取[世界观 + 前一章 + 目标章节]三个。第二章：第1章+第2章",
    "step3_process": "第一阶段：同时获取世界观、第1章、第2章，然后基于已有内容询问续写方向"
  },
  "user_intent": "续写第二章（分阶段执行）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取作品世界观", "tool": "get_worldview_summary", "params": {"work_id": ""}},
    {"task_id": 2, "description": "读取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 3, "description": "读取第二章（如果存在）", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 2}}
  ]
}

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
    {"task_id": 2, "description": "概括内容", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "内容概括"}}
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

用户: "根据前四章写后5章的大纲"
{
  "thinking": {
    "step1_output": "用户想看到第5-9章的大纲规划（章节标题+主要剧情），不是正文",
    "step2_material": "需要前四章内容作为参考",
    "step3_process": "获取前文后创作大纲结构（大纲是创作！）"
  },
  "user_intent": "创作第5-9章大纲",
  "tasks": [
    {"task_id": 1, "description": "批量获取前四章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": "1-4"}},
    {"task_id": 2, "description": "创作大纲", "tool": "smart_continue", "params": {"context": "$TASK_1.chapters$", "requirements": "基于前四章的人物、情节、伏笔，为第5-9章设计详细大纲：章节标题、主要剧情、涉及角色、伏笔设置", "target_words": 1500}}
  ]
}
"""


def get_search_examples() -> str:
    """搜索示例"""
    return """【搜索示例】⚠️ 搜索关键词提取规则 - 极其重要！

用户: "优化第一章中段融第一次吞噬器灵的场景描写"
{
  "thinking": {
    "step1_output": "用户想优化一个特定场景的描写",
    "step2_material": "需要先搜索'吞噬器灵'相关内容，找到具体位置",
    "step3_process": "搜索定位 → 读取章节 → 分析并给出优化建议"
  },
  "user_intent": "优化吞噬器灵场景描写",
  "tasks": [
    {"task_id": 1, "description": "搜索吞噬器灵场景", "tool": "search_analysis_fragments_tool", "params": {"query": "吞噬器灵"}},
    {"task_id": 2, "description": "读取第一章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 3, "description": "分析并优化场景描写", "tool": "analyze_text_tool", "params": {"text": "$TASK_2.content$", "focus": "场景描写优化"}}
  ]
}
⚠️ 关键：query 参数提取"吞噬器灵"（核心动作词组），而不是"灵的场景"（错误拆分）！

用户: "找一下主角觉醒的描写"
{
  "thinking": {
    "step1_output": "用户想找到主角觉醒的相关描写",
    "step2_material": "需要搜索'觉醒'相关内容",
    "step3_process": "搜索定位相关片段"
  },
  "user_intent": "搜索主角觉醒描写",
  "tasks": [
    {"task_id": 1, "description": "搜索觉醒相关内容", "tool": "search_analysis_fragments_tool", "params": {"query": "觉醒"}}
  ]
}

用户: "赵穆和段融的对话在哪"
{
  "thinking": {
    "step1_output": "用户想找两个人物的对话场景",
    "step2_material": "需要搜索两个人物名",
    "step3_process": "搜索定位"
  },
  "user_intent": "搜索赵穆和段融的对话",
  "tasks": [
    {"task_id": 1, "description": "搜索赵穆和段融", "tool": "search_analysis_fragments_tool", "params": {"query": "赵穆 段融"}}
  ]
}
"""


def get_smart_rewrite_examples() -> str:
    """smart_rewrite 完整示例（P1级别重要！）"""
    return """【smart_rewrite 完整示例】⚠️ 必须参考！

用户: "帮我润色第1章中段融第一次吞噬器灵的场景"
{
  "thinking": {
    "step1_output": "用户想润色特定场景，需要使用 smart_rewrite",
    "step2_material": "需要先获取第1章内容",
    "step3_process": "获取章节 → 调用 smart_rewrite 生成改写版本"
  },
  "user_intent": "润色吞噬器灵场景",
  "tasks": [
    {"task_id": 1, "description": "获取第1章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 1}},
    {"task_id": 2, "description": "润色吞噬器灵场景", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "text_to_rewrite": "$TASK_1.content$",
      "chapter_content": "$TASK_1.content$",
      "user_requirement": "优化心理描写、扩写感官体验、使节奏更紧凑"
    }}
  ]
}

用户: "把这段话改得更有画面感：天色未明，青冥中尚悬着几颗残星。"
{
  "thinking": {
    "step1_output": "用户指定了要改写的文本，直接使用 smart_rewrite",
    "step2_material": "用户已提供文本",
    "step3_process": "直接调用 smart_rewrite"
  },
  "user_intent": "改写指定文本使其更有画面感",
  "tasks": [
    {"task_id": 1, "description": "改写指定文本", "tool": "smart_rewrite", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "text_to_rewrite": "天色未明，青冥中尚悬着几颗残星。",
      "chapter_content": "",
      "user_requirement": "更有画面感"
    }}
  ]
}

用户: "扩写第3章的战斗场景"
{
  "thinking": {
    "step1_output": "用户说'扩写'，这是改写场景，不是续写！",
    "step2_material": "需要获取第3章内容",
    "step3_process": "获取章节 → 调用 smart_rewrite（扩写=改写）"
  },
  "user_intent": "扩写战斗场景（改写场景）",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}},
    {"task_id": 2, "description": "扩写战斗场景", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "text_to_rewrite": "$TASK_1.content$",
      "chapter_content": "$TASK_1.content$",
      "user_requirement": "扩写战斗场景，增加细节描写，使其更丰富"
    }}
  ]
}
⚠️ 关键：扩写/润色/优化 都用 smart_rewrite，不是 smart_continue！
"""


def get_selected_text_examples() -> str:
    """选中文本示例"""
    return """【选中文本示例】⚠️ 当 Prompt 包含【用户选中的文本】时

用户选中文本: "天色未明，青冥中尚悬着几颗残星。"
用户指令: "帮我把这一句话修改得更加丰富！"
chapter_id: "abc-123"
{
  "thinking": {
    "step1_output": "用户选中了一句话，希望润色/丰富这段文字",
    "step2_material": "需要读取本章内容了解上下文，然后基于上下文给出改写建议",
    "step3_process": "先 read_chapter_tool 读章节，再 analyze_text_tool 分析并给出建议"
  },
  "user_intent": "润色选中的文本，使其更丰富",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "read_chapter_tool", "params": {"work_id": "$WORK_ID$", "chapter_id": "abc-123"}},
    {"task_id": 2, "description": "分析并给出更丰富的改写建议", "tool": "analyze_text_tool", "params": {"text": "天色未明，青冥中尚悬着几颗残星。", "focus": "丰富度改写"}}
  ]
}

用户选中文本: "他走进房间，看到了她。"
用户指令: "更有文采一些"
chapter_id: "def-456"
{
  "thinking": {
    "step1_output": "用户选中了一句话，希望改写得更有文采",
    "step2_material": "需要读取本章内容了解场景和情绪",
    "step3_process": "先 read_chapter_tool 读章节，再 analyze_text_tool 分析并给出改写建议"
  },
  "user_intent": "改写选中的文本，使其更有文采",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "read_chapter_tool", "params": {"work_id": "$WORK_ID$", "chapter_id": "def-456"}},
    {"task_id": 2, "description": "分析并给出更有文采的改写建议", "tool": "analyze_text_tool", "params": {"text": "他走进房间，看到了她。", "focus": "文采润色"}}
  ]
}
"""


def get_multi_chapter_examples() -> str:
    """多章节读取示例"""
    return """【多章节读取示例】⚠️ 涉及多个章节时

用户: "对比分析第3章和第7章中主角的心理变化"
{
  "thinking": {
    "step1_output": "用户需要对比两个章节中的内容",
    "step2_material": "需要同时读取第3章和第7章的内容",
    "step3_process": "使用 read_chapter_tool 一次性读取多个章节，然后用 analyze_text_tool 进行对比分析"
  },
  "user_intent": "对比分析多个章节的心理变化",
  "tasks": [
    {"task_id": 1, "description": "获取第3章的chapter_id", "tool": "get_chapter_by_order_tool", "params": {"work_id": "$WORK_ID$", "chapter_order": 3}},
    {"task_id": 2, "description": "获取第7章的chapter_id", "tool": "get_chapter_by_order_tool", "params": {"work_id": "$WORK_ID$", "chapter_order": 7}},
    {"task_id": 3, "description": "读取第3章和第7章内容", "tool": "read_chapter_tool", "params": {"work_id": "$WORK_ID$", "chapter_id": "$TASK_1.chapter_id$,$TASK_2.chapter_id$"}},
    {"task_id": 4, "description": "对比分析主角心理变化", "tool": "analyze_text_tool", "params": {"text": "$TASK_3$", "focus": "心理变化对比"}}
  ]
}
"""


def get_agent_mode_examples() -> str:
    """Agent 模式示例（带 checkpoint 字段）"""
    return """
## 📝 Agent 模式示例（必须包含 checkpoint 字段）

示例1 - 简单查询（无checkpoint）：
用户: "叶凡是什么体质？"
{
  "thinking": {"step1_output": "描述体质", "step2_material": "搜索相关内容", "step3_process": "总结"},
  "user_intent": "查询叶凡体质",
  "tasks": [
    {"task_id": 1, "description": "搜索叶凡体质", "tool": "search_analysis_fragments_tool",
     "params": {"query": "叶凡的体质"}, "checkpoint": false},
    {"task_id": 2, "description": "总结体质特点", "tool": "analyze_text_tool",
     "params": {"text": "$TASK_1$", "focus": "总结体质特点"}, "checkpoint": false}
  ]
}

示例2 - 多章节分析（使用批量读取）：
用户: "分析前5章的情节发展"
{
  "thinking": {"step1_output": "分析报告", "step2_material": "5个章节内容", "step3_process": "批量读取后汇总分析"},
  "user_intent": "分析前5章情节",
  "output_title": "分析结果",
  "tasks": [
    {"task_id": 1, "description": "批量读取前5章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": "1-5"}, "checkpoint": false},
    {"task_id": 2, "description": "汇总分析情节发展", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.chapters$", "focus": "情节发展分析"}, "checkpoint": false}
  ]
}

示例3 - 单任务（无checkpoint）：
用户: "第3章讲了什么"
{
  "thinking": {"step1_output": "概括", "step2_material": "第3章", "step3_process": "读取并概括"},
  "user_intent": "概括第3章",
  "output_title": "章节概括",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "get_chapter_by_order_tool", "params": {"chapter_order": 3}, "checkpoint": false},
    {"task_id": 2, "description": "概括内容", "tool": "analyze_text_tool", "params": {"text": "$TASK_1.content$", "focus": "概括"}, "checkpoint": false}
  ]
}
"""


def get_operation_tools_examples() -> str:
    """OPERATION 工具示例（章节操作）"""
    return """【OPERATION 工具示例】⚠️ 章节操作（会触发用户确认）

用户: "帮我创建一个新章节，标题叫第四章 器灵之秘"
{
  "thinking": {
    "step1_output": "用户要创建新章节，这是章节操作请求",
    "step2_material": "不需要读取，直接创建",
    "step3_process": "调用 create_chapter 创建章节"
  },
  "user_intent": "创建新章节",
  "tasks": [
    {"task_id": 1, "description": "创建新章节", "tool": "create_chapter", "params": {"title": "第四章 器灵之秘"}}
  ]
}

用户: "把第二章标题改成觉醒"
{
  "thinking": {
    "step1_output": "用户要修改章节标题",
    "step2_material": "用户指定了第二章，可以直接使用章节序号",
    "step3_process": "直接调用 update_chapter_title，传入章节序号"
  },
  "user_intent": "修改章节标题",
  "tasks": [
    {"task_id": 1, "description": "修改第二章标题", "tool": "update_chapter_title", "params": {"chapter_id": "2", "new_title": "觉醒"}}
  ]
}

用户: "删除第三章"
{
  "thinking": {
    "step1_output": "用户要删除章节，这是危险操作",
    "step2_material": "用户指定了第三章，可以直接使用章节序号",
    "step3_process": "直接调用 delete_chapter，传入章节序号"
  },
  "user_intent": "删除章节",
  "tasks": [
    {"task_id": 1, "description": "删除第三章", "tool": "delete_chapter", "params": {"chapter_id": "3"}}
  ]
}

用户: "把第1章到第3章的标题分别改成觉醒、修炼、突破"
{
  "thinking": {
    "step1_output": "用户要批量修改多个章节的标题",
    "step2_material": "用户指定了第1、2、3章，可以直接使用章节序号",
    "step3_process": "为每个章节生成一个 update_chapter_title 任务，直接使用章节序号"
  },
  "user_intent": "批量修改章节标题",
  "tasks": [
    {"task_id": 1, "description": "修改第1章标题", "tool": "update_chapter_title", "params": {"chapter_id": "1", "new_title": "觉醒"}},
    {"task_id": 2, "description": "修改第2章标题", "tool": "update_chapter_title", "params": {"chapter_id": "2", "new_title": "修炼"}},
    {"task_id": 3, "description": "修改第3章标题", "tool": "update_chapter_title", "params": {"chapter_id": "3", "new_title": "突破"}}
  ]
}
"""


def get_all_planning_examples() -> str:
    """获取所有规划示例（用于基础 Planning Prompt）"""
    return (
        get_direct_answer_examples() +
        get_user_confirmation_examples() +
        get_staged_execution_examples() +
        get_creation_request_examples() +
        get_search_examples() +
        get_smart_rewrite_examples() +
        get_selected_text_examples() +
        get_multi_chapter_examples() +
        get_operation_tools_examples()
    )


# 导出
__all__ = [
    "get_direct_answer_examples",
    "get_user_confirmation_examples",
    "get_staged_execution_examples",
    "get_creation_request_examples",
    "get_search_examples",
    "get_smart_rewrite_examples",
    "get_selected_text_examples",
    "get_multi_chapter_examples",
    "get_agent_mode_examples",
    "get_operation_tools_examples",
    "get_all_planning_examples",
]
