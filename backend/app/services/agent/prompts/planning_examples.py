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
    "step1_output": "用户确认了计划，需要立即执行之前讨论的方案并应用到编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "⚠️ 创作类→操作类：读取→分析→续写500字→apply_chapter_edit应用"
  },
  "user_intent": "执行之前讨论的续写计划",
  "output_title": "续写内容",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {"chapter_orders": "5", "include": "chapter,worldview,rag"}},
    {"task_id": 2, "description": "分析战斗风格", "tool": "analyze_content", "params": {"content": "$TASK_1.chapters[0].content$", "aspects": ["style"], "depth": "normal"}},
    {"task_id": 3, "description": "续写500字战斗场景", "tool": "smart_continue", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "chapter_content": "$TASK_1.chapters[0].content$", "user_requirement": "续写战斗场景，保持现有风格", "word_count": 500}},
    {"task_id": 4, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "operation": "append", "content": "$TASK_3.content$"}}
  ]
}

用户: "可以，直接写1000字"
{
  "thinking": {
    "step1_output": "用户确认了计划并调整了字数要求，可以直接执行并应用到编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "⚠️ 创作类→操作类：获取→续写1000字→apply_chapter_edit应用"
  },
  "user_intent": "续写1000字战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {"chapter_orders": "5", "include": "chapter,worldview,rag"}},
    {"task_id": 2, "description": "续写1000字战斗场景", "tool": "smart_continue", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "chapter_content": "$TASK_1.chapters[0].content$", "user_requirement": "续写战斗场景", "word_count": 1000}},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "operation": "append", "content": "$TASK_2.content$"}}
  ]
}

用户: "不用分析，直接续写"
{
  "thinking": {
    "step1_output": "用户确认了计划，但跳过分析步骤，直接续写并应用到编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "⚠️ 创作类→操作类：获取→续写→apply_chapter_edit应用"
  },
  "user_intent": "直接续写第5章战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {"chapter_orders": "5", "include": "chapter,worldview,rag"}},
    {"task_id": 2, "description": "续写战斗场景", "tool": "smart_continue", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "chapter_content": "$TASK_1.chapters[0].content$", "user_requirement": "续写战斗场景", "word_count": 500}},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "operation": "append", "content": "$TASK_2.content$"}}
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
    {"task_id": 1, "description": "获取最近章节和世界观", "tool": "get_writing_context", "params": {"chapter_orders": "-3", "include": "chapter,worldview,rag"}},
    {"task_id": 2, "description": "分析情节走向并规划大纲", "tool": "analyze_content", "params": {"content": "$TASK_1.chapters$", "aspects": ["plot", "structure"], "depth": "deep"}}
  ]
}
⚠️ 注意：这个任务只生成了分析阶段，执行完成后 AI 会在响应中说："我分析了现有内容，这是后5章的大纲规划...你觉得这个方向可以吗？确认后我会开始续写第一章。"

用户: "可以，先写第6章"
{
  "thinking": {
    "step1_output": "用户确认了大纲方向，现在开始续写第6章并应用到编辑器",
    "step2_material": "需要之前的分析结果（在对话历史中）",
    "step3_process": "⚠️ 创作类→操作类：获取→续写→apply_chapter_edit应用"
  },
  "user_intent": "续写第6章",
  "tasks": [
    {"task_id": 1, "description": "获取第5章上下文", "tool": "get_writing_context", "params": {"chapter_orders": "5", "include": "chapter,worldview,rag"}},
    {"task_id": 2, "description": "续写第6章", "tool": "smart_continue", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "chapter_content": "$TASK_1.chapters[0].content$", "user_requirement": "基于之前规划的大纲续写第6章", "word_count": 3000}},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {"chapter_id": "$TASK_1.chapters[0].id$", "operation": "append", "content": "$TASK_2.content$"}}
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
    "step2_material": "⚠️ 使用 get_writing_context 一次性获取世界观和已有章节",
    "step3_process": "第一阶段：获取上下文，然后基于已有内容询问创作细节"
  },
  "user_intent": "创作第一章（分阶段）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {"chapter_orders": "0,1", "include": "work,chapter,worldview"}}
  ]
}

用户: "3000字，激昂风格，重点介绍主角"
{
  "thinking": {
    "step1_output": "用户确认了创作细节，现在可以开始创作",
    "step2_material": "世界观信息（在对话历史中已获取）",
    "step3_process": "生成创作任务 → 应用到编辑器"
  },
  "user_intent": "创作第一章（用户已确认参数）",
  "tasks": [
    {"task_id": 1, "description": "创作第一章", "tool": "smart_continue", "params": {"chapter_id": "$CHAPTER_ID$", "chapter_content": "", "user_requirement": "创作第一章，3000字，激昂风格，重点介绍主角", "word_count": 3000}},
    {"task_id": 2, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {"chapter_id": "$CHAPTER_ID$", "operation": "append", "content": "$TASK_1.content$"}}
  ]
}

用户: "续写第二章"
{
  "thinking": {
    "step1_output": "用户要续写第二章，这是创作请求，应该分阶段执行",
    "step2_material": "⚠️ 使用 get_writing_context 一次性获取世界观和相关章节",
    "step3_process": "第一阶段：获取上下文，然后基于已有内容询问续写方向"
  },
  "user_intent": "续写第二章（分阶段执行）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {"chapter_orders": "1,2", "include": "work,chapter,worldview,rag"}}
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
    {"task_id": 1, "description": "获取第三章", "tool": "get_writing_context", "params": {"chapter_orders": "3", "include": "chapter"}},
    {"task_id": 2, "description": "概括内容", "tool": "analyze_content", "params": {"content": "$TASK_1.chapters[0].content$", "aspects": ["plot"], "depth": "normal"}}
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
    {"task_id": 1, "description": "获取第三章", "tool": "get_writing_context", "params": {"chapter_orders": "3", "include": "chapter"}}
  ]
}

用户: "第五章的标题是什么"
{
  "thinking": {
    "step1_output": "用户想知道第五章的标题（元数据查询）",
    "step2_material": "需要第五章的元数据",
    "step3_process": "get_writing_context 返回的数据已包含 title 字段，直接返回即可"
  },
  "user_intent": "查询第五章标题",
  "response_hint": "title",
  "tasks": [
    {"task_id": 1, "description": "获取第五章信息", "tool": "get_writing_context", "params": {"chapter_orders": "5", "include": "chapter"}}
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
    {"task_id": 1, "description": "批量获取前四章", "tool": "get_writing_context", "params": {"chapter_orders": "1-4", "include": "chapter,worldview"}},
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
    "step1_output": "用户想优化一个特定场景的描写，需要修改内容",
    "step2_material": "需要先用 locate_content 定位'吞噬器灵'场景，获取 paragraph_index",
    "step3_process": "locate_content 定位 → smart_rewrite 改写 → apply_chapter_edit 应用"
  },
  "user_intent": "优化吞噬器灵场景描写",
  "tasks": [
    {"task_id": 1, "description": "定位吞噬器灵场景", "tool": "locate_content", "params": {"chapter_id": "$CHAPTER_ID$", "query": "吞噬器灵"}},
    {"task_id": 2, "description": "改写场景描写", "tool": "smart_rewrite", "params": {"chapter_id": "$TASK_1.chapter_id$", "text_to_rewrite": "$TASK_1.text$", "user_requirement": "优化场景描写，增强画面感"}},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {"chapter_id": "$TASK_1.chapter_id$", "operation": "replace", "content": "$TASK_2.versions[0].content$", "original_text": "$TASK_2.original_text$", "paragraph_index": "$TASK_1.paragraph_index$", "node_id": "$TASK_1.node_id$"}}
  ]
}
⚠️ 关键：用户要**修改**内容时，必须用 locate_content 定位，不要用 search_content！
⚠️ 跨章节支持：smart_rewrite 和 apply_chapter_edit 的 chapter_id 必须使用 $TASK_1.chapter_id$（locate_content 返回的章节ID），支持跨章节修改！

用户: "找一下主角觉醒的描写"
{
  "thinking": {
    "step1_output": "用户想找到主角觉醒的相关描写",
    "step2_material": "需要搜索'觉醒'相关内容",
    "step3_process": "搜索定位相关片段"
  },
  "user_intent": "搜索主角觉醒描写",
  "tasks": [
    {"task_id": 1, "description": "搜索觉醒相关内容", "tool": "search_content", "params": {"query": "觉醒"}}
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
    {"task_id": 1, "description": "搜索赵穆和段融", "tool": "search_content", "params": {"query": "赵穆 段融"}}
  ]
}
"""


def get_smart_rewrite_examples() -> str:
    """smart_rewrite 完整示例（P1级别重要！）"""
    return """【smart_rewrite 完整示例】⚠️ 必须参考！

用户: "帮我润色第1章中段融第一次吞噬器灵的场景"
{
  "thinking": {
    "step1_output": "用户想润色特定场景，需要先定位再改写",
    "step2_material": "需要先用 locate_content 定位吞噬器灵场景",
    "step3_process": "⚠️ locate_content 定位 → smart_rewrite 生成 → apply_chapter_edit 应用"
  },
  "user_intent": "润色吞噬器灵场景",
  "tasks": [
    {"task_id": 1, "description": "定位吞噬器灵场景", "tool": "locate_content", "params": {"chapter_id": "$CHAPTER_ID$", "query": "吞噬器灵"}},
    {"task_id": 2, "description": "润色场景", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "text_to_rewrite": "$TASK_1.text$",
      "user_requirement": "优化心理描写、扩写感官体验、使节奏更紧凑"
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "operation": "replace",
      "content": "$TASK_2.versions[0].content$",
      "original_text": "$TASK_2.original_text$",
      "paragraph_index": "$TASK_1.paragraph_index$",
      "node_id": "$TASK_1.node_id$"
    }}
  ]
}
⚠️ 关键：用 locate_content 定位，然后把 paragraph_index 和 node_id 传给 apply_chapter_edit！

用户: "把这段话改得更有画面感：天色未明，青冥中尚悬着几颗残星。"
{
  "thinking": {
    "step1_output": "用户指定了要改写的文本，使用 smart_rewrite 并应用到编辑器",
    "step2_material": "用户已提供文本",
    "step3_process": "⚠️ 创作类→操作类：smart_rewrite 生成 → apply_chapter_edit 应用（用 original_text 定位）"
  },
  "user_intent": "改写指定文本使其更有画面感",
  "tasks": [
    {"task_id": 1, "description": "改写指定文本", "tool": "smart_rewrite", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "text_to_rewrite": "天色未明，青冥中尚悬着几颗残星。",
      "user_requirement": "更有画面感"
    }},
    {"task_id": 2, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "operation": "replace",
      "content": "$TASK_1.versions[0].content$",
      "original_text": "$TASK_1.original_text$"
    }}
  ]
}

用户: "扩写第3章的战斗场景"
{
  "thinking": {
    "step1_output": "用户说'扩写'，这是改写场景，不是续写！需要应用到编辑器",
    "step2_material": "需要获取第3章内容",
    "step3_process": "⚠️ 创作类→操作类：获取章节 → smart_rewrite 生成 → apply_chapter_edit 应用"
  },
  "user_intent": "扩写战斗场景（改写场景）",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "get_writing_context", "params": {"chapter_orders": "3", "include": "chapter"}},
    {"task_id": 2, "description": "扩写战斗场景", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "text_to_rewrite": "$TASK_1.chapters[0].content$",
      "chapter_content": "$TASK_1.chapters[0].content$",
      "user_requirement": "扩写战斗场景，增加细节描写，使其更丰富"
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "operation": "replace",
      "content": "$TASK_2.versions[0].content$",
      "original_text": "$TASK_2.original_text$"
    }}
  ]
}
⚠️ 关键：扩写/润色/优化 都用 smart_rewrite → apply_chapter_edit（用 original_text 定位）！
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
    "step3_process": "先 get_writing_context 读章节，再 analyze_content 分析并给出建议"
  },
  "user_intent": "润色选中的文本，使其更丰富",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "get_writing_context", "params": {"chapter_id": "abc-123", "include": "chapter"}},
    {"task_id": 2, "description": "分析并给出更丰富的改写建议", "tool": "analyze_content", "params": {"content": "天色未明，青冥中尚悬着几颗残星。", "aspects": ["style"], "context": "$TASK_1.chapters[0].content$"}}
  ]
}

用户选中文本: "他走进房间，看到了她。"
用户指令: "更有文采一些"
chapter_id: "def-456"
{
  "thinking": {
    "step1_output": "用户选中了一句话，希望改写得更有文采",
    "step2_material": "需要读取本章内容了解场景和情绪",
    "step3_process": "先 get_writing_context 读章节，再 analyze_content 分析并给出改写建议"
  },
  "user_intent": "改写选中的文本，使其更有文采",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "get_writing_context", "params": {"chapter_id": "def-456", "include": "chapter"}},
    {"task_id": 2, "description": "分析并给出更有文采的改写建议", "tool": "analyze_content", "params": {"content": "他走进房间，看到了她。", "aspects": ["style"], "context": "$TASK_1.chapters[0].content$"}}
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
    "step3_process": "使用 get_writing_context 一次性读取多个章节，然后用 analyze_content 进行对比分析"
  },
  "user_intent": "对比分析多个章节的心理变化",
  "tasks": [
    {"task_id": 1, "description": "批量读取第3章和第7章", "tool": "get_writing_context", "params": {"chapter_orders": "3,7", "include": "chapter"}},
    {"task_id": 2, "description": "对比分析主角心理变化", "tool": "analyze_content", "params": {"content": "$TASK_1.chapters$", "aspects": ["character"], "depth": "deep"}}
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
    {"task_id": 1, "description": "搜索叶凡体质", "tool": "search_content",
     "params": {"query": "叶凡的体质"}, "checkpoint": false},
    {"task_id": 2, "description": "总结体质特点", "tool": "analyze_content",
     "params": {"content": "$TASK_1$", "aspects": ["character"], "depth": "normal"}, "checkpoint": false}
  ]
}

示例2 - 多章节分析（使用批量读取）：
用户: "分析前5章的情节发展"
{
  "thinking": {"step1_output": "分析报告", "step2_material": "5个章节内容", "step3_process": "批量读取后汇总分析"},
  "user_intent": "分析前5章情节",
  "output_title": "分析结果",
  "tasks": [
    {"task_id": 1, "description": "批量读取前5章", "tool": "get_writing_context", "params": {"chapter_orders": "1-5", "include": "chapter"}, "checkpoint": false},
    {"task_id": 2, "description": "汇总分析情节发展", "tool": "analyze_content", "params": {"content": "$TASK_1.chapters$", "aspects": ["plot", "structure"], "depth": "deep"}, "checkpoint": false}
  ]
}

示例3 - 单任务（无checkpoint）：
用户: "第3章讲了什么"
{
  "thinking": {"step1_output": "概括", "step2_material": "第3章", "step3_process": "读取并概括"},
  "user_intent": "概括第3章",
  "output_title": "章节概括",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "get_writing_context", "params": {"chapter_orders": "3", "include": "chapter"}, "checkpoint": false},
    {"task_id": 2, "description": "概括内容", "tool": "analyze_content", "params": {"content": "$TASK_1.chapters[0].content$", "aspects": ["plot"], "depth": "shallow"}, "checkpoint": false}
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


def get_editor_workflow_examples() -> str:
    """编辑器工作流示例（创作类 → 操作类）"""
    return """【编辑器工作流示例】⚠️ 创作类工具 + 操作类工具的正确用法

⚠️ 核心规则：
- 创作类工具（smart_continue, smart_insert, smart_rewrite）只生成内容，不写入编辑器
- 操作类工具（apply_chapter_edit）负责将内容写入编辑器
- **创作类 → 操作类的对应关系**：
  - smart_continue → apply_chapter_edit(operation="append")
  - smart_insert → apply_chapter_edit(operation="insert")
  - smart_rewrite → apply_chapter_edit(operation="replace")

⚠️⚠️⚠️ 极其重要 - 参数类型规则 ⚠️⚠️⚠️
- chapter_content 参数必须是字符串，不能是列表！
- ✅ 正确: "chapter_content": "$TASK_1.content$"（单个章节的内容字符串）
- ❌ 错误: "chapter_content": "$TASK_1.chapters$"（这是列表，会报错！）
- ❌ 错误: "chapter_content": "$TASK_1$"（这是完整对象，会报错！）

- **什么时候需要 apply_chapter_edit？**
  - 用户说"续写"、"插入"、"改写"、"润色" → 需要！
  - 用户说"帮我写一段XX"、"生成一个大纲" → 不需要！

---
【场景1：续写 + 应用到编辑器】

用户: "续写第5章500字"
{
  "thinking": {
    "step1_output": "用户要续写，内容需要写入编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "获取章节 → smart_continue 生成 → apply_chapter_edit 应用"
  },
  "user_intent": "续写第5章",
  "tasks": [
    {"task_id": 1, "description": "获取第5章", "tool": "get_writing_context", "params": {"chapter_orders": "5", "include": "chapter,worldview,rag"}},
    {"task_id": 2, "description": "生成续写内容", "tool": "smart_continue", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "chapter_content": "$TASK_1.chapters[0].content$",
      "user_requirement": "续写",
      "word_count": 500
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "operation": "append",
      "content": "$TASK_2.content$"
    }}
  ]
}

---
【场景2：插入 + 应用到编辑器】

用户: "在他转身离开那里加一段心理描写"
{
  "thinking": {
    "step1_output": "用户要在特定位置插入内容，需要先定位再插入",
    "step2_material": "用 locate_content 定位'他转身离开'的位置",
    "step3_process": "locate_content 定位 → smart_insert 生成 → apply_chapter_edit 应用"
  },
  "user_intent": "在指定位置插入心理描写",
  "tasks": [
    {"task_id": 1, "description": "定位插入位置", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "他转身离开"
    }},
    {"task_id": 2, "description": "生成插入内容", "tool": "smart_insert", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "user_intent": "在他转身离开那里加一段心理描写",
      "insert_context": "$TASK_1.text$",
      "word_count": 200
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "operation": "insert",
      "content": "$TASK_2.content$",
      "node_id": "$TASK_1.node_id$",
      "paragraph_index": "$TASK_1.paragraph_index$",
      "before_anchor": "$TASK_1.after_anchor$"
    }}
  ]
}

---
【场景3：改写 + 应用到编辑器】

用户: "润色第3章的战斗场景"
{
  "thinking": {
    "step1_output": "用户要润色/改写，内容需要写入编辑器",
    "step2_material": "需要第3章内容",
    "step3_process": "获取章节 → smart_rewrite 生成版本 → apply_chapter_edit 应用"
  },
  "user_intent": "润色战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "get_writing_context", "params": {"chapter_orders": "3", "include": "chapter"}},
    {"task_id": 2, "description": "生成改写版本", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "text_to_rewrite": "$TASK_1.chapters[0].content$",
      "chapter_content": "$TASK_1.chapters[0].content$",
      "user_requirement": "润色战斗场景，增加画面感"
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "operation": "replace",
      "content": "$TASK_2.versions[0].content$",
      "original_text": "$TASK_2.original_text$"
    }}
  ]
}
⚠️ 注意：smart_rewrite 返回 versions 和 original_text，用 original_text 让前端定位

---
【场景4：只创作，不应用到编辑器】

用户: "帮我写一段主角觉醒的场景"
{
  "thinking": {
    "step1_output": "用户只是想看内容，不需要写入编辑器",
    "step2_material": "可能需要参考现有内容",
    "step3_process": "生成内容返回给用户，不调用 apply_chapter_edit"
  },
  "user_intent": "生成一段觉醒场景（只看不写入）",
  "tasks": [
    {"task_id": 1, "description": "生成觉醒场景", "tool": "smart_continue", "params": {
      "chapter_content": "",
      "user_requirement": "写一段主角觉醒的场景",
      "word_count": 500
    }}
  ]
}
⚠️ 注意：没有 apply_chapter_edit，内容只返回给用户看，不写入编辑器
"""


def get_new_tools_examples() -> str:
    """新聚合工具示例（get_writing_context 和 analyze_content）"""
    return """【新聚合工具示例】⚠️ 推荐使用！减少工具调用次数

## 🔴 重要：优先使用新聚合工具！

| 旧工具 | 新工具 | 说明 |
|--------|--------|------|
| get_chapter_by_order_tool | get_writing_context | 一站式获取上下文 |
| read_chapter_tool | get_writing_context | 支持批量读取 |
| get_worldview_summary | get_writing_context | include="worldview" |
| analyze_text_tool | analyze_content | 一站式分析 |

---
【场景1：续写前获取完整上下文】⚠️ 推荐用法！

用户: "续写第5章"
{
  "thinking": {
    "step1_output": "用户要续写第5章，需要获取上下文",
    "step2_material": "⚠️ 使用 get_writing_context 一次性获取：章节+世界观+RAG",
    "step3_process": "get_writing_context → smart_continue → apply_chapter_edit"
  },
  "user_intent": "续写第5章",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {
      "chapter_orders": "5",
      "include": "work,chapter,worldview,rag"
    }},
    {"task_id": 2, "description": "续写内容", "tool": "smart_continue", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "chapter_content": "$TASK_1.chapters[0].content$",
      "user_requirement": "续写",
      "word_count": 2000
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "operation": "append",
      "content": "$TASK_2.content$"
    }}
  ]
}
⚠️ 对比旧方式：需要 3 个工具（get_worldview_summary + get_chapter_by_order_tool + get_context_tool）
✅ 新方式：1 个工具搞定！

---
【场景2：批量读取多章节】

用户: "分析前5章的情节发展"
{
  "thinking": {
    "step1_output": "用户要分析多章节，需要批量读取",
    "step2_material": "⚠️ 使用 get_writing_context 批量读取 1-5 章",
    "step3_process": "get_writing_context → analyze_content"
  },
  "user_intent": "分析前5章情节",
  "tasks": [
    {"task_id": 1, "description": "批量读取前5章", "tool": "get_writing_context", "params": {
      "chapter_orders": "1-5",
      "include": "chapter"
    }},
    {"task_id": 2, "description": "分析情节发展", "tool": "analyze_content", "params": {
      "content": "$TASK_1.chapters$",
      "aspects": ["structure", "plot"],
      "depth": "deep"
    }}
  ]
}
⚠️ 支持范围格式："1-5" 表示第1到第5章

---
【场景3：只获取世界观】

用户: "这个作品有哪些角色？"
{
  "thinking": {
    "step1_output": "用户想了解角色信息",
    "step2_material": "⚠️ 使用 get_writing_context 只获取世界观",
    "step3_process": "get_writing_context(include=worldview)"
  },
  "user_intent": "查询角色信息",
  "tasks": [
    {"task_id": 1, "description": "获取世界观", "tool": "get_writing_context", "params": {
      "include": "worldview"
    }}
  ]
}

---
【场景4：内容分析】

用户: "帮我检查这章有什么问题"
{
  "thinking": {
    "step1_output": "用户要检查内容问题",
    "step2_material": "⚠️ 使用 analyze_content 一站式分析",
    "step3_process": "get_writing_context → analyze_content"
  },
  "user_intent": "检查章节问题",
  "tasks": [
    {"task_id": 1, "description": "获取章节内容", "tool": "get_writing_context", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "include": "chapter"
    }},
    {"task_id": 2, "description": "分析内容问题", "tool": "analyze_content", "params": {
      "content": "$TASK_1.chapters[0].content$",
      "aspects": ["grammar", "logic", "style"],
      "depth": "normal"
    }}
  ]
}

---
【场景5：创作第一章（分阶段）】⚠️ 推荐用法！

用户: "帮我写第一章"
{
  "thinking": {
    "step1_output": "用户要创作第一章，应该分阶段执行",
    "step2_material": "⚠️ 使用 get_writing_context 一次性获取世界观和已有章节",
    "step3_process": "第一阶段：获取上下文，询问创作细节"
  },
  "user_intent": "创作第一章（分阶段）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "get_writing_context", "params": {
      "chapter_orders": "0,1",
      "include": "work,chapter,worldview"
    }}
  ]
}
⚠️ 对比旧方式：需要 3 个工具（get_worldview_summary + get_chapter_by_order_tool x2）
✅ 新方式：1 个工具搞定！

"""


def get_locate_content_examples() -> str:
    """locate_content 定位工具示例（定位 → 改写/插入 → 应用）"""
    return """【locate_content 定位工具示例】⚠️ 用户指定模糊位置时，必须先定位！

⚠️⚠️⚠️ 极其重要 - locate_content 参数规则 ⚠️⚠️⚠️
locate_content 只接受以下参数：
- chapter_id: 章节ID（必填）
- query: 定位查询（必填）
- nodes_info: 节点列表（可选）
- node_id: 节点ID（可选）

❌ 绝对禁止传入 work_id 参数！locate_content 不接受 work_id！
✅ 正确: {"chapter_id": "$CHAPTER_ID$", "query": "吞噬器灵"}
❌ 错误: {"work_id": "xxx", "chapter_id": "xxx", "query": "xxx"}

---
【场景1：定位段落 + 改写】

用户: "把第三段改得更生动"
{
  "thinking": {
    "step1_output": "用户指定了'第三段'这个模糊位置，需要先定位",
    "step2_material": "用 locate_content 定位第三段，获取 node_id 和 paragraph_index",
    "step3_process": "locate_content 定位 → smart_rewrite 生成 → apply_chapter_edit 应用（传递定位参数）"
  },
  "user_intent": "改写第三段使其更生动",
  "tasks": [
    {"task_id": 1, "description": "定位第三段", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "第三段"
    }},
    {"task_id": 2, "description": "改写内容", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "text_to_rewrite": "$TASK_1.text$",
      "user_requirement": "更生动，增加画面感"
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "operation": "replace",
      "content": "$TASK_2.versions[0].content$",
      "node_id": "$TASK_1.node_id$",
      "paragraph_index": "$TASK_1.paragraph_index$",
      "before_anchor": "$TASK_1.before_anchor$",
      "after_anchor": "$TASK_1.after_anchor$",
      "original_text": "$TASK_1.text$"
    }}
  ]
}
⚠️ 关键：locate_content 返回的 node_id、paragraph_index 必须传给 apply_chapter_edit！

---
【场景2：定位开头/结尾】

用户: "修改开头部分，让它更吸引人"
{
  "thinking": {
    "step1_output": "用户说'开头'，是模糊位置，需要先定位",
    "step2_material": "用 locate_content 定位开头",
    "step3_process": "locate_content → smart_rewrite → apply_chapter_edit"
  },
  "user_intent": "改写开头",
  "tasks": [
    {"task_id": 1, "description": "定位开头", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "开头"
    }},
    {"task_id": 2, "description": "改写开头", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "text_to_rewrite": "$TASK_1.text$",
      "user_requirement": "更吸引人，开篇即引人入胜"
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "operation": "replace",
      "content": "$TASK_2.versions[0].content$",
      "node_id": "$TASK_1.node_id$",
      "paragraph_index": "$TASK_1.paragraph_index$"
    }}
  ]
}

---
【场景3：定位 + 插入】

用户: "在第二段后面加一段心理描写"
{
  "thinking": {
    "step1_output": "用户说'第二段后面'，需要先定位第二段，然后在其后插入",
    "step2_material": "用 locate_content 定位第二段",
    "step3_process": "locate_content → smart_insert → apply_chapter_edit"
  },
  "user_intent": "在第二段后插入心理描写",
  "tasks": [
    {"task_id": 1, "description": "定位第二段", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "第二段"
    }},
    {"task_id": 2, "description": "生成心理描写", "tool": "smart_insert", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "user_intent": "在第二段后插入心理描写",
      "insert_context": "$TASK_1.text$",
      "word_count": 200
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "operation": "insert",
      "content": "$TASK_2.content$",
      "node_id": "$TASK_1.node_id$",
      "paragraph_index": "$TASK_1.paragraph_index$",
      "before_anchor": "$TASK_1.after_anchor$"
    }}
  ]
}
⚠️ 注意：smart_insert 不再接收锚点参数，定位由 locate_content 完成，锚点传给 apply_chapter_edit

---
【场景4：定位特定内容】

用户: "改一下主角出场的地方"
{
  "thinking": {
    "step1_output": "用户说'主角出场的地方'，是语义描述，需要先定位",
    "step2_material": "用 locate_content 搜索主角出场相关内容",
    "step3_process": "locate_content → smart_rewrite → apply_chapter_edit"
  },
  "user_intent": "改写主角出场部分",
  "tasks": [
    {"task_id": 1, "description": "定位主角出场", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "主角出场"
    }},
    {"task_id": 2, "description": "改写出场描写", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "text_to_rewrite": "$TASK_1.text$",
      "user_requirement": "让主角出场更有气势"
    }},
    {"task_id": 3, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_1.chapter_id$",
      "operation": "replace",
      "content": "$TASK_2.versions[0].content$",
      "node_id": "$TASK_1.node_id$",
      "paragraph_index": "$TASK_1.paragraph_index$",
      "original_text": "$TASK_1.text$"
    }}
  ]
}
⚠️ locate_content 支持语义搜索，可以定位"主角出场"、"战斗场景"等描述性内容
⚠️ 跨章节支持：smart_rewrite 和 apply_chapter_edit 的 chapter_id 必须使用 $TASK_1.chapter_id$（locate_content 返回的章节ID）

---
【场景4.5：未指定章节的修改】⚠️ 用户描述内容但没有章节信息

用户: "把'吞噬器灵'那段改得更紧凑"
{
  "thinking": {
    "step1_output": "用户要修改但未说明章节，需要先检索找到目标章节",
    "step2_material": "search_content 找章 → get_writing_context 读章 → locate_content 精确定位",
    "step3_process": "search_content → get_writing_context → locate_content → smart_rewrite → apply_chapter_edit"
  },
  "user_intent": "修改吞噬器灵相关段落",
  "tasks": [
    {"task_id": 1, "description": "检索吞噬器灵场景", "tool": "search_content", "params": {"query": "吞噬器灵", "top_k": 3}},
    {"task_id": 2, "description": "读取目标章节", "tool": "get_writing_context", "params": {"chapter_id": "$TASK_1.results[0].chapter_id$", "include": "chapter"}},
    {"task_id": 3, "description": "定位吞噬器灵段落", "tool": "locate_content", "params": {
      "chapter_id": "$TASK_2.chapters[0].id$",
      "query": "吞噬器灵"
    }},
    {"task_id": 4, "description": "改写段落", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_3.chapter_id$",
      "text_to_rewrite": "$TASK_3.text$",
      "user_requirement": "压缩冗余，节奏更紧凑"
    }},
    {"task_id": 5, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_3.chapter_id$",
      "operation": "replace",
      "content": "$TASK_4.versions[0].content$",
      "node_id": "$TASK_3.node_id$",
      "paragraph_index": "$TASK_3.paragraph_index$",
      "original_text": "$TASK_3.text$"
    }}
  ]
}

---
【场景5：跨章节定位 + 修改】⚠️ 用户在A章节，要修改B章节的内容

用户: "我在第4章，想修改第2章中'羚羊献食'那段"
{
  "thinking": {
    "step1_output": "用户要跨章节修改，需要先获取第2章ID，再定位",
    "step2_material": "先用 get_writing_context 获取第2章，再用 locate_content 定位",
    "step3_process": "get_writing_context → locate_content → smart_rewrite → apply_chapter_edit"
  },
  "user_intent": "跨章节修改第2章内容",
  "tasks": [
    {"task_id": 1, "description": "获取第2章", "tool": "get_writing_context", "params": {"chapter_orders": "2", "include": "chapter"}},
    {"task_id": 2, "description": "定位羚羊献食场景", "tool": "locate_content", "params": {
      "chapter_id": "$TASK_1.chapters[0].id$",
      "query": "羚羊献食"
    }},
    {"task_id": 3, "description": "改写场景", "tool": "smart_rewrite", "params": {
      "chapter_id": "$TASK_2.chapter_id$",
      "text_to_rewrite": "$TASK_2.text$",
      "user_requirement": "润色这段描写"
    }},
    {"task_id": 4, "description": "应用到编辑器", "tool": "apply_chapter_edit", "params": {
      "chapter_id": "$TASK_2.chapter_id$",
      "operation": "replace",
      "content": "$TASK_3.versions[0].content$",
      "node_id": "$TASK_2.node_id$",
      "paragraph_index": "$TASK_2.paragraph_index$",
      "original_text": "$TASK_2.text$"
    }}
  ]
}
⚠️ 跨章节关键：先用 get_writing_context 获取目标章节ID，再传给 locate_content！
"""


def get_all_planning_examples() -> str:
    """获取所有规划示例（用于基础 Planning Prompt）"""
    return (
        get_new_tools_examples() +  # 🔴 P0优先级：新聚合工具示例放在最前面！
        get_direct_answer_examples() +
        get_user_confirmation_examples() +
        get_locate_content_examples() +
        get_staged_execution_examples() +
        get_creation_request_examples() +
        get_search_examples() +
        get_smart_rewrite_examples() +
        get_selected_text_examples() +
        get_multi_chapter_examples() +
        get_operation_tools_examples() +
        get_editor_workflow_examples()
    )


# 导出
__all__ = [
    "get_new_tools_examples",  # 新增：聚合工具示例
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
    "get_editor_workflow_examples",
    "get_locate_content_examples",
    "get_all_planning_examples",
]
