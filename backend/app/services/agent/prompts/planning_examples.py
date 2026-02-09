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
    "step3_process": "⚠️ 创作类→操作类：读取→分析→续写500字→operate_apply应用"
  },
  "user_intent": "执行之前讨论的续写计划",
  "output_title": "续写内容",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "续写第5章战斗场景，获取第5章内容和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "分析战斗风格", "tool": "analyze_content", "params": {"content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}, "aspects": ["style"], "depth": "normal"}, "depends_on": [1]},
    {"task_id": 3, "description": "续写500字战斗场景", "tool": "smart_continue", "params": {"chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}, "user_requirement": "续写战斗场景，保持现有风格", "word_count": 500}, "depends_on": [1]},
    {"task_id": 4, "description": "应用到编辑器", "tool": "operate_apply", "params": {"operation": "append", "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "content": {"$ref": {"task_id": 3, "path": "content"}}}, "depends_on": [1, 3]}
  ]
}

用户: "可以，直接写1000字"
{
  "thinking": {
    "step1_output": "用户确认了计划并调整了字数要求，可以直接执行并应用到编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "⚠️ 创作类→操作类：获取→续写1000字→operate_apply应用"
  },
  "user_intent": "续写1000字战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "续写第5章战斗场景，获取第5章内容和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "续写1000字战斗场景", "tool": "smart_continue", "params": {"chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}, "user_requirement": "续写战斗场景", "word_count": 1000}, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {"operation": "append", "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "content": {"$ref": {"task_id": 2, "path": "content"}}}, "depends_on": [1, 2]}
  ]
}

用户: "不用分析，直接续写"
{
  "thinking": {
    "step1_output": "用户确认了计划，但跳过分析步骤，直接续写并应用到编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "⚠️ 创作类→操作类：获取→续写→operate_apply应用"
  },
  "user_intent": "直接续写第5章战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "续写第5章战斗场景，获取第5章内容和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "续写战斗场景", "tool": "smart_continue", "params": {"chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}, "user_requirement": "续写战斗场景", "word_count": 500}, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {"operation": "append", "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "content": {"$ref": {"task_id": 2, "path": "content"}}}, "depends_on": [1, 2]}
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
    "step3_process": "第一阶段：获取现有内容后直接规划大纲，征求用户确认后再续写"
  },
  "user_intent": "续写后5章（分阶段执行）",
  "tasks": [
    {"task_id": 1, "description": "获取最近章节和世界观", "tool": "explore_content", "params": {"target_task": "续写后5章准备，获取最近3章内容和世界观设定"}, "depends_on": []}
  ]
}
⚠️ 注意：这个任务只生成取证阶段，执行完成后 AI 会在响应中直接给出后5章大纲并征求确认。

用户: "可以，先写第6章"
{
  "thinking": {
    "step1_output": "用户确认了大纲方向，现在开始续写第6章并应用到编辑器",
    "step2_material": "需要之前的分析结果（在对话历史中）",
    "step3_process": "⚠️ 创作类→操作类：获取→续写→operate_apply应用"
  },
  "user_intent": "续写第6章",
  "tasks": [
    {"task_id": 1, "description": "获取第5章上下文", "tool": "explore_content", "params": {"target_task": "续写第6章准备，获取第5章内容和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "续写第6章", "tool": "smart_continue", "params": {"chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}, "user_requirement": "基于之前规划的大纲续写第6章", "word_count": 3000}, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {"operation": "append", "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}}, "content": {"$ref": {"task_id": 2, "path": "content"}}}, "depends_on": [1, 2]}
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
    "step2_material": "⚠️ 使用 explore_content 一次性获取世界观和已有章节",
    "step3_process": "第一阶段：获取上下文，然后基于已有内容询问创作细节"
  },
  "user_intent": "创作第一章（分阶段）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "创作第一章准备，获取世界观和已有章节"}, "depends_on": []}
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
    {"task_id": 1, "description": "创作第一章", "tool": "smart_continue", "params": {"chapter_id": "$CHAPTER_ID$", "chapter_content": "", "user_requirement": "创作第一章，3000字，激昂风格，重点介绍主角", "word_count": 3000}, "depends_on": []},
    {"task_id": 2, "description": "应用到编辑器", "tool": "operate_apply", "params": {"operation": "append", "chapter_id": "$CHAPTER_ID$", "content": {"$ref": {"task_id": 1, "path": "content"}}}, "depends_on": [1]}
  ]
}

用户: "续写第二章"
{
  "thinking": {
    "step1_output": "用户要续写第二章，这是创作请求，应该分阶段执行",
    "step2_material": "⚠️ 使用 explore_content 一次性获取世界观和相关章节",
    "step3_process": "第一阶段：获取上下文，然后基于已有内容询问续写方向"
  },
  "user_intent": "续写第二章（分阶段执行）",
  "direct_answer": "好的，我先了解一下作品的世界观和已有内容...",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "续写第二章准备，获取第1-2章内容和世界观"}, "depends_on": []}
  ]
}

用户: "第三章讲了什么"
{
  "thinking": {
    "step1_output": "用户想看到概括性文字，了解第三章主要内容，不是要原文",
    "step2_material": "需要第三章原文",
    "step3_process": "获取后直接概括总结"
  },
  "user_intent": "概括第三章内容",
  "tasks": [
    {"task_id": 1, "description": "获取第三章", "tool": "explore_content", "params": {"target_task": "获取第三章内容用于概括"}, "depends_on": []}
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
    {"task_id": 1, "description": "获取第三章", "tool": "explore_content", "params": {"target_task": "获取第三章原文"}, "depends_on": []}
  ]
}

用户: "第五章的标题是什么"
{
  "thinking": {
    "step1_output": "用户想知道第五章的标题（元数据查询）",
    "step2_material": "需要第五章的元数据",
    "step3_process": "explore_content 返回的数据已包含 title 字段，直接返回即可"
  },
  "user_intent": "查询第五章标题",
  "response_hint": "title",
  "tasks": [
    {"task_id": 1, "description": "获取第五章信息", "tool": "explore_content", "params": {"target_task": "获取第五章标题信息"}, "depends_on": []}
  ]
}

用户: "根据前四章写后5章的大纲"
{
  "thinking": {
    "step1_output": "用户想看到第5-9章的大纲规划（章节标题+主要剧情），不是正文",
    "step2_material": "需要前四章内容作为参考",
    "step3_process": "获取前文后直接输出大纲结构（不写入编辑器）"
  },
  "user_intent": "创作第5-9章大纲",
  "tasks": [
    {"task_id": 1, "description": "批量获取前四章", "tool": "explore_content", "params": {"target_task": "创作大纲准备，获取前四章内容和世界观"}, "depends_on": []}
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
    "step3_process": "locate_content 定位 → smart_rewrite 改写 → operate_apply 应用"
  },
  "user_intent": "优化吞噬器灵场景描写",
  "tasks": [
    {"task_id": 1, "description": "定位吞噬器灵场景", "tool": "locate_content", "params": {"chapter_id": "$CHAPTER_ID$", "query": "吞噬器灵"}, "depends_on": []},
    {"task_id": 2, "description": "改写场景描写", "tool": "smart_rewrite", "params": {"chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}}, "text_to_rewrite": {"$ref": {"task_id": 1, "path": "text"}}, "user_requirement": "优化场景描写，增强画面感"}, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {"chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}}, "operation": "replace", "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}}, "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}}, "node_id": {"$ref": {"task_id": 1, "path": "node_id"}}}, "depends_on": [1, 2]}
  ]
}
⚠️ 关键：用户要**修改**内容时，必须用 locate_content 定位；检索信息统一用 explore_content！
⚠️ 章节必须明确：locate_content 不跨章节，chapter_id 必须来自明确章节或用户指定！

用户: "找一下主角觉醒的描写"
{
  "thinking": {
    "step1_output": "用户想找到主角觉醒的相关描写",
    "step2_material": "统一用 explore_content 获取相关描写",
    "step3_process": "explore_content 搜索并返回相关片段"
  },
  "user_intent": "搜索主角觉醒描写",
  "tasks": [
    {"task_id": 1, "description": "获取觉醒相关描写", "tool": "explore_content", "params": {"target_task": "找出主角觉醒的描写"}, "depends_on": []}
  ]
}

用户: "赵穆和段融的对话在哪"
{
  "thinking": {
    "step1_output": "用户想找两个人物的对话场景",
    "step2_material": "统一用 explore_content 搜索对话描写",
    "step3_process": "explore_content 搜索并返回相关片段"
  },
  "user_intent": "搜索赵穆和段融的对话",
  "tasks": [
    {"task_id": 1, "description": "获取赵穆和段融对话描写", "tool": "explore_content", "params": {"target_task": "找出赵穆和段融的对话描写"}, "depends_on": []}
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
    "step3_process": "⚠️ locate_content 定位 → smart_rewrite 生成 → operate_apply 应用"
  },
  "user_intent": "润色吞噬器灵场景",
  "tasks": [
    {"task_id": 1, "description": "定位吞噬器灵场景", "tool": "locate_content", "params": {"chapter_id": "$CHAPTER_ID$", "query": "吞噬器灵"}, "depends_on": []},
    {"task_id": 2, "description": "润色场景", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "text"}},
      "user_requirement": "优化心理描写、扩写感官体验、使节奏更紧凑"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}},
      "node_id": {"$ref": {"task_id": 1, "path": "node_id"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ 关键：用 locate_content 定位，然后把 paragraph_index 和 node_id 传给 operate_apply！

用户: "把这段话改得更有画面感：天色未明，青冥中尚悬着几颗残星。"
{
  "thinking": {
    "step1_output": "用户指定了要改写的文本，使用 smart_rewrite 并应用到编辑器",
    "step2_material": "用户已提供文本",
    "step3_process": "⚠️ 创作类→操作类：smart_rewrite 生成 → locate_content 定位 → operate_apply 应用"
  },
  "user_intent": "改写指定文本使其更有画面感",
  "tasks": [
    {"task_id": 1, "description": "改写指定文本", "tool": "smart_rewrite", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "text_to_rewrite": "天色未明，青冥中尚悬着几颗残星。",
      "user_requirement": "更有画面感"
    }, "depends_on": []},
    {"task_id": 2, "description": "定位原文位置", "tool": "locate_content", "params": {"chapter_id": "$CHAPTER_ID$", "query": "天色未明，青冥中尚悬着几颗残星。"}, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "operation": "replace",
      "content": {"$ref": {"task_id": 1, "path": "versions[0].content"}},
      "paragraph_index": {"$ref": {"task_id": 2, "path": "paragraph_index"}},
      "node_id": {"$ref": {"task_id": 2, "path": "node_id"}}
    }, "depends_on": [1, 2]}
  ]
}

用户: "扩写第3章的战斗场景"
{
  "thinking": {
    "step1_output": "用户说'扩写'，这是改写场景，不是续写！需要应用到编辑器",
    "step2_material": "需要获取第3章内容",
    "step3_process": "⚠️ 创作类→操作类：获取章节 → smart_rewrite 生成 → operate_apply 应用"
  },
  "user_intent": "扩写战斗场景（改写场景）",
  "tasks": [
    {"task_id": 1, "description": "获取第3章", "tool": "explore_content", "params": {"target_task": "扩写第3章战斗场景，获取第3章内容"}, "depends_on": []},
    {"task_id": 2, "description": "扩写战斗场景", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "user_requirement": "扩写战斗场景，增加细节描写，使其更丰富"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "locate_targets[0].paragraph_index"}},
      "node_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].node_id"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ 关键：扩写/润色/优化 都用 smart_rewrite → operate_apply（必须传 node_id/paragraph_index）！
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
    "step3_process": "先 explore_content 读章节，再 analyze_content 分析并给出建议"
  },
  "user_intent": "润色选中的文本，使其更丰富",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "explore_content", "params": {"target_task": "润色文本准备，获取章节 abc-123 的内容和上下文"}, "depends_on": []},
    {"task_id": 2, "description": "分析并给出更丰富的改写建议", "tool": "analyze_content", "params": {"content": "天色未明，青冥中尚悬着几颗残星。", "aspects": ["style"], "context": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}}, "depends_on": [1]}
  ]
}

用户选中文本: "他走进房间，看到了她。"
用户指令: "更有文采一些"
chapter_id: "def-456"
{
  "thinking": {
    "step1_output": "用户选中了一句话，希望改写得更有文采",
    "step2_material": "需要读取本章内容了解场景和情绪",
    "step3_process": "先 explore_content 读章节，再 analyze_content 分析并给出改写建议"
  },
  "user_intent": "改写选中的文本，使其更有文采",
  "tasks": [
    {"task_id": 1, "description": "读取章节内容", "tool": "explore_content", "params": {"target_task": "改写文本准备，获取章节 def-456 的内容和上下文"}, "depends_on": []},
    {"task_id": 2, "description": "分析并给出更有文采的改写建议", "tool": "analyze_content", "params": {"content": "他走进房间，看到了她。", "aspects": ["style"], "context": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}}, "depends_on": [1]}
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
    "step3_process": "使用 explore_content 一次性读取多个章节，然后直接输出对比分析"
  },
  "user_intent": "对比分析多个章节的心理变化",
  "tasks": [
    {"task_id": 1, "description": "批量读取第3章和第7章", "tool": "explore_content", "params": {"target_task": "对比分析第3章和第7章主角心理变化"}, "depends_on": []}
  ]
}
"""


def get_explore_content_examples() -> str:
    """explore_content 深度探索工具示例（2026-01-18 更新：统一信息获取入口）"""
    return """【explore_content 统一信息获取示例】🔴 所有信息获取任务都用 explore_content

🔴🔴🔴 **重要：explore_content 是统一的信息获取入口！**
⚠️ **默认返回完整字段**（含 frontend_display/explore_summary）；如需最小输出，仅保留 `evidences` / `locate_targets`，请显式 output_mode="evidence_only"。

explore_content 会自动判断任务复杂度：
- 简单任务 → 首轮即返回（与单次读取一致）
- 复杂任务 → 自动多轮探索

⚠️ **不要再使用以下工具**（这些是 explore_content 内部调用的）:
- ❌ search_content
- ❌ get_chapter_by_order

---
【场景1：简单续写】

用户: "续写第5章"
{
  "thinking": {
    "step1_output": "用户要续写第5章",
    "step2_material": "⚠️ 统一用 explore_content 获取上下文",
    "step3_process": "explore_content → smart_continue → operate_apply"
  },
  "user_intent": "续写第5章",
  "tasks": [
    {"task_id": 1, "description": "获取续写上下文", "tool": "explore_content", "params": {
      "target_task": "续写第5章，获取第4-5章内容和世界观"
    }, "depends_on": []},
    {"task_id": 2, "description": "续写内容", "tool": "smart_continue", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "user_requirement": "续写",
      "word_count": 2000
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "operation": "append",
      "content": {"$ref": {"task_id": 2, "path": "content"}}
    }, "depends_on": [1, 2]}
  ]
}
✅ 简单任务 explore_content 首轮即返回，效率与单次读取一致

---
【场景2：复杂续写 - 需要深入理解人物】

用户: "续写第6章，需要深入理解段融的性格变化"
{
  "thinking": {
    "step1_output": "用户要续写，且需要深入理解人物性格变化，这是复杂任务",
    "step2_material": "⚠️ explore_content 会自动多轮探索收集段融相关信息",
    "step3_process": "explore_content 深度探索 → smart_continue 续写 → operate_apply 应用"
  },
  "user_intent": "深入理解人物后续写第6章",
  "tasks": [
    {"task_id": 1, "description": "深度探索段融性格变化", "tool": "explore_content", "params": {
      "target_task": "续写第6章，需要深入理解段融的性格变化，包括他在前几章的行为、心理描写、与其他角色的互动"
    }, "depends_on": []},
    {"task_id": 2, "description": "基于探索结果续写", "tool": "smart_continue", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "user_requirement": "续写第6章，延续段融的性格特点",
      "word_count": 2000
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 2, "path": "chapter_id"}},
      "operation": "append",
      "content": {"$ref": {"task_id": 2, "path": "content"}}
    }, "depends_on": [2]}
  ]
}
✅ 复杂任务 explore_content 会自动多轮探索

---
【场景3：多章节关联分析】

用户: "分析主角与师兄的关系在1-5章的发展"
{
  "thinking": {
    "step1_output": "用户要分析跨多章节的人物关系发展",
    "step2_material": "⚠️ explore_content 会自动收集多章节中的相关描写",
    "step3_process": "explore_content 深度探索 → 直接输出分析"
  },
  "user_intent": "分析多章节中的人物关系发展",
  "tasks": [
    {"task_id": 1, "description": "深度探索主角与师兄关系", "tool": "explore_content", "params": {
      "target_task": "分析主角与师兄的关系，包括：首次见面、互动场景、情感变化、关键转折点"
    }, "depends_on": []}
  ]
}

---
【场景4：搜索并验证上下文】

用户: "找出所有提到'灵气'的地方，并分析其在不同章节的含义"
{
  "thinking": {
    "step1_output": "用户要找多个位置并分析，需要验证上下文",
    "step2_material": "⚠️ explore_content 会自动搜索+读取原文验证",
    "step3_process": "explore_content 深度探索"
  },
  "user_intent": "搜索并分析灵气在各章节的含义",
  "tasks": [
    {"task_id": 1, "description": "深度探索灵气相关内容", "tool": "explore_content", "params": {
      "target_task": "找出所有提到'灵气'的地方，读取完整上下文，分析其在不同章节的具体含义和用法"
    }, "depends_on": []}
  ]
}
✅ explore_content 会自动：搜索 → 定位 → 读取原文 → 验证上下文

---
【场景5：获取世界观】

用户: "这个作品有哪些角色？"
{
  "thinking": {
    "step1_output": "用户想了解角色信息",
    "step2_material": "⚠️ 统一用 explore_content",
    "step3_process": "explore_content 获取世界观"
  },
  "user_intent": "查询角色信息",
  "tasks": [
    {"task_id": 1, "description": "获取世界观", "tool": "explore_content", "params": {
      "target_task": "获取作品的世界观和角色设定"
    }, "depends_on": []}
  ]
}
✅ 简单查询 explore_content 首轮即返回

---
【场景6：生成分析文档（世界观/角色卡/伏笔表）】⚠️ 取证后直接输出，不用 smart_continue/analyze_content

用户: "输出一份完整的世界观设定文档"
{
  "thinking": {
    "step1_output": "用户需要结构化的世界观设定文档，不是故事正文",
    "step2_material": "需要从作品中收集世界观相关信息",
    "step3_process": "收集证据后直接输出设定文档"
  },
  "user_intent": "生成世界观设定文档",
  "output_title": "世界观设定",
  "tasks": [
    {"task_id": 1, "description": "收集世界观相关内容", "tool": "explore_content", "params": {
      "target_task": "收集作品的世界观设定：包括世界背景、修炼体系、势力分布、地理环境等"
    }, "depends_on": []}
  ]
}
⚠️ 注意：世界观文档、角色卡、伏笔表等分析类文档：explore_content 取证后**直接输出**，不写入编辑器！

用户: "帮我生成主角的角色卡"
{
  "thinking": {
    "step1_output": "用户需要角色卡文档，不是故事正文",
    "step2_material": "需要收集主角相关描写",
    "step3_process": "收集证据后直接输出角色卡"
  },
  "user_intent": "生成主角角色卡",
  "output_title": "角色卡",
  "tasks": [
    {"task_id": 1, "description": "收集主角相关描写", "tool": "explore_content", "params": {
      "target_task": "收集主角的外貌、性格、能力、背景、人际关系等描写"
    }, "depends_on": []}
  ]
}

用户: "整理前5章的伏笔追踪表"
{
  "thinking": {
    "step1_output": "用户需要伏笔追踪表，不是故事正文",
    "step2_material": "需要读取前5章内容",
    "step3_process": "收集证据后直接输出伏笔追踪表"
  },
  "user_intent": "生成伏笔追踪表",
  "output_title": "伏笔追踪",
  "tasks": [
    {"task_id": 1, "description": "读取前5章内容", "tool": "explore_content", "params": {
      "target_task": "读取第1-5章，收集所有伏笔和悬念"
    }, "depends_on": []}
  ]
}
❌ 错误做法：用 smart_continue 生成世界观文档（会输出故事内容而非分析文档）
✅ 正确做法：explore_content 取证后直接输出（按指定格式整理）
"""


def get_agent_mode_examples() -> str:
    """Agent 模式示例（带 checkpoint 字段）"""
    return """
## 📝 Agent 模式示例（必须包含 checkpoint 字段）

示例1 - 简单查询（无checkpoint）：
用户: "叶凡是什么体质？"
{
  "thinking": {"step1_output": "描述体质", "step2_material": "统一用 explore_content 获取相关内容", "step3_process": "explore_content → 直接输出"},
  "user_intent": "查询叶凡体质",
  "tasks": [
    {"task_id": 1, "description": "获取叶凡体质相关描写", "tool": "explore_content",
     "params": {"target_task": "查询叶凡体质相关描写"}, "checkpoint": false, "depends_on": []}
  ]
}

示例2 - 多章节分析（使用批量读取）：
用户: "分析前5章的情节发展"
{
  "thinking": {"step1_output": "分析报告", "step2_material": "5个章节内容", "step3_process": "批量读取后直接输出分析"},
  "user_intent": "分析前5章情节",
  "output_title": "分析结果",
  "tasks": [
    {"task_id": 1, "description": "获取前5章内容", "tool": "explore_content", "params": {"target_task": "分析前5章情节发展，获取第1-5章内容"}, "checkpoint": false, "depends_on": []}
  ]
}

示例3 - 单任务（无checkpoint）：
用户: "第3章讲了什么"
{
  "thinking": {"step1_output": "概括", "step2_material": "第3章", "step3_process": "读取后直接概括"},
  "user_intent": "概括第3章",
  "output_title": "章节概括",
  "tasks": [
    {"task_id": 1, "description": "获取第3章内容", "tool": "explore_content", "params": {"target_task": "概括第3章内容"}, "checkpoint": false, "depends_on": []}
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
    "step3_process": "调用 operate_apply(create) 创建章节"
  },
  "user_intent": "创建新章节",
  "tasks": [
    {"task_id": 1, "description": "创建新章节", "tool": "operate_apply", "params": {"operation": "create", "work_id": "$WORK_ID$", "title": "第四章 器灵之秘", "content": ""}, "depends_on": []}
  ]
}

用户: "把第二章标题改成觉醒"
{
  "thinking": {
    "step1_output": "用户要修改章节标题",
    "step2_material": "用户指定了第二章，可以直接使用章节序号",
    "step3_process": "直接调用 operate_apply(title)，传入章节序号"
  },
  "user_intent": "修改章节标题",
  "tasks": [
    {"task_id": 1, "description": "修改第二章标题", "tool": "operate_apply", "params": {"operation": "title", "chapter_id": "2", "title": "觉醒"}, "depends_on": []}
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
    {"task_id": 1, "description": "删除第三章", "tool": "delete_chapter", "params": {"chapter_id": "3"}, "depends_on": []}
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
    {"task_id": 1, "description": "修改第1章标题", "tool": "update_chapter_title", "params": {"chapter_id": "1", "new_title": "觉醒"}, "depends_on": []},
    {"task_id": 2, "description": "修改第2章标题", "tool": "update_chapter_title", "params": {"chapter_id": "2", "new_title": "修炼"}, "depends_on": []},
    {"task_id": 3, "description": "修改第3章标题", "tool": "update_chapter_title", "params": {"chapter_id": "3", "new_title": "突破"}, "depends_on": []}
  ]
}
"""


def get_editor_workflow_examples() -> str:
    """编辑器工作流示例（创作类 → 操作类）"""
    return """【编辑器工作流示例】⚠️ 创作类工具 + 操作类工具的正确用法

⚠️ 核心规则：
- 创作类工具（smart_continue, smart_insert, smart_rewrite）只生成内容，不写入编辑器
- 操作类工具 operate_apply 负责将内容写入编辑器
- **创作类 → 操作类的对应关系**：
  - smart_continue → operate_apply(operation="append")
  - smart_insert → operate_apply(operation="insert")
  - smart_rewrite → operate_apply(operation="replace")

⚠️⚠️⚠️ 极其重要 - 参数类型规则 ⚠️⚠️⚠️
- chapter_content 参数必须是字符串，不能是列表！
- ✅ 正确: "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}（单个章节的内容字符串）
- ❌ 错误: "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}}（这是列表，会报错！）
- ❌ 错误: "chapter_content": {"$ref": {"task_id": 1}}（这是完整对象，会报错！）

- **什么时候需要操作类工具？**
  - 用户说"续写"、"插入"、"改写"、"润色" → 需要！
  - 用户说"帮我写一段XX"、"生成一个大纲" → 不需要！

⚠️ **具体示例请参考【operate_apply 统一入口示例】**

---
【只创作，不应用到编辑器】

用户: "帮我写一段主角觉醒的场景"
{
  "thinking": {
    "step1_output": "用户只是想看内容，不需要写入编辑器",
    "step2_material": "可能需要参考现有内容",
    "step3_process": "生成内容返回给用户，不调用 operate_apply"
  },
  "user_intent": "生成一段觉醒场景（只看不写入）",
  "tasks": [
    {"task_id": 1, "description": "生成觉醒场景", "tool": "smart_continue", "params": {
      "chapter_content": "",
      "user_requirement": "写一段主角觉醒的场景",
      "word_count": 500
    }, "depends_on": []}
  ]
}
⚠️ 注意：没有 operate_apply，内容只返回给用户看，不写入编辑器
"""


def get_operate_apply_examples() -> str:
    """operate_apply 统一入口示例（🆕 推荐使用）"""
    return """【operate_apply 统一入口示例】🆕 推荐使用 operate_apply 统一入口

⚠️⚠️⚠️ **极其重要 - operate_apply 不再自动定位！** ⚠️⚠️⚠️

必须先用 locate_content 获取 node_id/paragraph_index（检索证据统一走 explore_content）。

✅ 正确流程：先定位 → smart_rewrite → operate_apply(operation="replace", paragraph_index=..., node_id=...)

⚠️ operate_apply 支持 6 种操作：
| operation | 说明 | 使用场景 |
|-----------|------|---------|
| append | 续写 | smart_continue 后追加到章节末尾 |
| replace | 改写 | smart_rewrite 后替换指定段落（需精确定位） |
| insert | 插入 | smart_insert 后在指定位置插入（需精确定位） |
| content | 整章替换 | 重写整章内容 |
| create | 创建章节 | 写新章节（需要 work_id 和 title） |
| title | 修改标题 | 改进章节标题 |

---
【场景1：续写 - 使用 operate_apply】

用户: "续写第5章500字"
{
  "thinking": {
    "step1_output": "用户要续写，内容需要写入编辑器",
    "step2_material": "需要第5章内容",
    "step3_process": "获取章节 → smart_continue 生成 → operate_apply(append) 应用"
  },
  "user_intent": "续写第5章",
  "tasks": [
    {"task_id": 1, "description": "获取第5章上下文", "tool": "explore_content", "params": {"target_task": "续写第5章准备，获取第5章内容和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "生成续写内容", "tool": "smart_continue", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "user_requirement": "续写",
      "word_count": 500
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "operation": "append",
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "content": {"$ref": {"task_id": 2, "path": "content"}}
    }, "depends_on": [1, 2]}
  ]
}

---
【场景2：改写 - 使用 operate_apply（精确定位）】

用户: "润色第3章的战斗场景"
{
  "thinking": {
    "step1_output": "用户要润色/改写，内容需要写入编辑器",
    "step2_material": "需要第3章内容",
    "step3_process": "获取章节 → smart_rewrite 生成 → operate_apply(replace) 应用（精确定位）"
  },
  "user_intent": "润色战斗场景",
  "tasks": [
    {"task_id": 1, "description": "获取第3章内容", "tool": "explore_content", "params": {"target_task": "润色第3章战斗场景，获取第3章内容"}, "depends_on": []},
    {"task_id": 2, "description": "生成改写内容", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "user_requirement": "润色战斗场景，增加画面感"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "operation": "replace",
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "locate_targets[0].paragraph_index"}},
      "node_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].node_id"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ replace 操作必须传 node_id/paragraph_index

---
【场景3：插入 - 使用 operate_apply（精确定位）】

用户: "在战斗结束后加一段心理描写"
{
  "thinking": {
    "step1_output": "用户要在特定位置插入内容",
    "step2_material": "需要章节内容",
    "step3_process": "获取章节 → smart_insert 生成 → operate_apply(insert) 应用（精确定位）"
  },
  "user_intent": "在战斗结束后插入心理描写",
  "tasks": [
    {"task_id": 1, "description": "获取章节内容", "tool": "explore_content", "params": {"target_task": "获取当前章节内容"}, "depends_on": []},
    {"task_id": 2, "description": "生成心理描写", "tool": "smart_insert", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "user_intent": "在战斗结束后插入心理描写",
      "insert_context": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "word_count": 200
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "operation": "insert",
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "content": {"$ref": {"task_id": 2, "path": "content"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "locate_targets[0].paragraph_index"}},
      "node_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].node_id"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ insert 操作必须传 node_id/paragraph_index（不允许降级）

---
【场景4：整章替换 - 使用 rewrite_chapter_content + operate_apply(content)】

用户: "重写第2章"
{
  "thinking": {
    "step1_output": "用户要重写整章内容",
    "step2_material": "需要世界观和大纲",
    "step3_process": "获取上下文 → rewrite_chapter_content 生成整章 → operate_apply(content) 整章替换"
  },
  "user_intent": "重写第2章",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "重写第2章准备，获取第1-2章和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "重写第2章", "tool": "rewrite_chapter_content", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapters[0].chapter_id"}},
      "user_requirement": "基于世界观和第1章，重写第2章"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "整章替换", "tool": "operate_apply", "params": {
      "operation": "content",
      "chapter_id": {"$ref": {"task_id": 2, "path": "chapter_id"}},
      "content": {"$ref": {"task_id": 2, "path": "content"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ operation="content" 会整章替换（映射到 replace_all），无需定位

---
【场景5：创建新章节 - 使用 operate_apply(create)】

用户: "帮我写一个新章节，主角开始修炼"
{
  "thinking": {
    "step1_output": "用户要创建新章节并写内容",
    "step2_material": "需要世界观和前文",
    "step3_process": "获取上下文 → smart_continue 生成 → operate_apply(create) 创建章节"
  },
  "user_intent": "创建新章节",
  "tasks": [
    {"task_id": 1, "description": "获取创作上下文", "tool": "explore_content", "params": {"target_task": "创建新章节准备，获取最新章节和世界观"}, "depends_on": []},
    {"task_id": 2, "description": "创作章节内容", "tool": "smart_continue", "params": {
      "chapter_content": {"$ref": {"task_id": 1, "path": "evidences[0].text"}},
      "user_requirement": "写主角开始修炼的章节",
      "word_count": 3000
    }, "depends_on": [1]},
    {"task_id": 3, "description": "创建新章节", "tool": "operate_apply", "params": {
      "operation": "create",
      "work_id": "$WORK_ID$",
      "title": "修炼初始",
      "content": {"$ref": {"task_id": 2, "path": "content"}}
    }, "depends_on": [2]}
  ]
}
⚠️ operation="create" 需要 work_id 和 title

---
【场景6：修改标题 - 使用 operate_apply(title)】

用户: "把第2章标题改成觉醒"
{
  "thinking": {
    "step1_output": "用户要直接修改标题",
    "step2_material": "不需要读取内容",
    "step3_process": "直接调用 operate_apply(title)"
  },
  "user_intent": "修改第2章标题",
  "tasks": [
    {"task_id": 1, "description": "修改标题", "tool": "operate_apply", "params": {
      "operation": "title",
      "chapter_id": "2",
      "title": "觉醒"
    }, "depends_on": []}
  ]
}
⚠️ operation="title" 需要 chapter_id 和 title，支持直接使用章节序号
"""


def get_new_tools_examples() -> str:
    """新聚合工具示例（2026-01-18 更新：已废弃，请使用 explore_content）"""
    return """【⚠️ 重要提示 - 工具已升级】

🔴🔴🔴 **旧的信息获取工具已整合到 explore_content！**

请参考【explore_content 统一信息获取示例】部分的示例。

explore_content 会自动判断任务复杂度：
- 简单任务 → 首轮即返回
- 复杂任务 → 自动多轮探索

⚠️ **不要再使用以下工具**（这些是 explore_content 内部调用的）:
- ❌ search_content
- ❌ get_chapter_by_order

✅ **统一使用 explore_content**
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
⚠️ nodes_info 仅来自前端/上下文；explore_content 不返回 nodes，禁止引用旧的 chapters[*].nodes。请改用 locate_targets[*].node_id。

⚠️ locate_content 输出字段在顶层：chapter_id / paragraph_index / node_id / text / before_anchor / after_anchor
❌ 禁止引用 results / found_paragraphs / frontend_display.locations（默认不返回 frontend_display）

⚠️ insert 降级已禁用（不允许 append fallback）

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
    "step3_process": "locate_content 定位 → smart_rewrite 生成 → operate_apply 应用（传递定位参数）"
  },
  "user_intent": "改写第三段使其更生动",
  "tasks": [
    {"task_id": 1, "description": "定位第三段", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "第三段"
    }, "depends_on": []},
    {"task_id": 2, "description": "改写内容", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "text"}},
      "user_requirement": "更生动，增加画面感"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "node_id": {"$ref": {"task_id": 1, "path": "node_id"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ 关键：locate_content 返回的 node_id、paragraph_index 必须传给 operate_apply！

---
【场景2：定位开头/结尾】

用户: "修改开头部分，让它更吸引人"
{
  "thinking": {
    "step1_output": "用户说'开头'，是模糊位置，需要先定位",
    "step2_material": "用 locate_content 定位开头",
    "step3_process": "locate_content → smart_rewrite → operate_apply"
  },
  "user_intent": "改写开头",
  "tasks": [
    {"task_id": 1, "description": "定位开头", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "开头"
    }, "depends_on": []},
    {"task_id": 2, "description": "改写开头", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "text"}},
      "user_requirement": "更吸引人，开篇即引人入胜"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "node_id": {"$ref": {"task_id": 1, "path": "node_id"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}}
    }, "depends_on": [1, 2]}
  ]
}

---
【场景3：定位 + 插入】

用户: "在第二段后面加一段心理描写"
{
  "thinking": {
    "step1_output": "用户说'第二段后面'，需要先定位第二段，然后在其后插入",
    "step2_material": "用 locate_content 定位第二段",
    "step3_process": "locate_content → smart_insert → operate_apply"
  },
  "user_intent": "在第二段后插入心理描写",
  "tasks": [
    {"task_id": 1, "description": "定位第二段", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "第二段"
    }, "depends_on": []},
    {"task_id": 2, "description": "生成心理描写", "tool": "smart_insert", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "user_intent": "在第二段后插入心理描写",
      "insert_context": {"$ref": {"task_id": 1, "path": "text"}},
      "word_count": 200
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "operation": "insert",
      "content": {"$ref": {"task_id": 2, "path": "content"}},
      "node_id": {"$ref": {"task_id": 1, "path": "node_id"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ 注意：smart_insert 不再接收锚点参数，operate_apply 只接受 node_id/paragraph_index

---
【场景4：定位特定内容】

用户: "改一下主角出场的地方"
{
  "thinking": {
    "step1_output": "用户说'主角出场的地方'，是语义描述，需要先定位",
    "step2_material": "用 locate_content 搜索主角出场相关内容",
    "step3_process": "locate_content → smart_rewrite → operate_apply"
  },
  "user_intent": "改写主角出场部分",
  "tasks": [
    {"task_id": 1, "description": "定位主角出场", "tool": "locate_content", "params": {
      "chapter_id": "$CHAPTER_ID$",
      "query": "主角出场"
    }, "depends_on": []},
    {"task_id": 2, "description": "改写出场描写", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "text"}},
      "user_requirement": "让主角出场更有气势"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "node_id": {"$ref": {"task_id": 1, "path": "node_id"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}}
    }, "depends_on": [1, 2]}
  ]
}
⚠️ locate_content 支持语义搜索，可以定位"主角出场"、"战斗场景"等描述性内容
⚠️ locate_content 不跨章节，请确保 chapter_id 正确

---
【场景4.5：未指定章节的修改】⚠️ 用户描述内容但没有章节信息

用户: "把'吞噬器灵'那段改得更紧凑"
{
  "thinking": {
    "step1_output": "用户要修改但未说明章节，需要先检索找到目标章节",
    "step2_material": "先用 explore_content 找到相关章节并获取上下文，再用 locate_content 精确定位",
    "step3_process": "explore_content → locate_content → smart_rewrite → operate_apply"
  },
  "user_intent": "修改吞噬器灵相关段落",
  "tasks": [
    {"task_id": 1, "description": "检索吞噬器灵场景并获取章节", "tool": "explore_content", "params": {"target_task": "检索吞噬器灵场景，找到对应章节并获取章节内容"}, "depends_on": []},
    {"task_id": 2, "description": "定位吞噬器灵段落", "tool": "locate_content", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "query": "吞噬器灵"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "改写段落", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 2, "path": "chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 2, "path": "text"}},
      "user_requirement": "压缩冗余，节奏更紧凑"
    }, "depends_on": [2]},
    {"task_id": 4, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 2, "path": "chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 3, "path": "versions[0].content"}},
      "node_id": {"$ref": {"task_id": 2, "path": "node_id"}},
      "paragraph_index": {"$ref": {"task_id": 2, "path": "paragraph_index"}}
    }, "depends_on": [2, 3]}
  ]
}

---
【场景5：跨章节定位 + 修改】⚠️ 用户在A章节，要修改B章节的内容

用户: "我在第4章，想修改第2章中'羚羊献食'那段"
{
  "thinking": {
    "step1_output": "用户要跨章节修改，需要先获取第2章ID，再定位",
    "step2_material": "先用 explore_content 获取第2章，再用 locate_content 定位",
    "step3_process": "explore_content → locate_content → smart_rewrite → operate_apply"
  },
  "user_intent": "跨章节修改第2章内容",
  "tasks": [
    {"task_id": 1, "description": "获取第2章内容", "tool": "explore_content", "params": {"target_task": "修改第2章准备，获取第2章内容"}, "depends_on": []},
    {"task_id": 2, "description": "定位羚羊献食场景", "tool": "locate_content", "params": {
      "chapter_id": {"$ref": {"task_id": 1, "path": "locate_targets[0].chapter_id"}},
      "query": "羚羊献食"
    }, "depends_on": [1]},
    {"task_id": 3, "description": "改写场景", "tool": "smart_rewrite", "params": {
      "chapter_id": {"$ref": {"task_id": 2, "path": "chapter_id"}},
      "text_to_rewrite": {"$ref": {"task_id": 2, "path": "text"}},
      "user_requirement": "润色这段描写"
    }, "depends_on": [2]},
    {"task_id": 4, "description": "应用到编辑器", "tool": "operate_apply", "params": {
      "chapter_id": {"$ref": {"task_id": 2, "path": "chapter_id"}},
      "operation": "replace",
      "content": {"$ref": {"task_id": 3, "path": "versions[0].content"}},
      "node_id": {"$ref": {"task_id": 2, "path": "node_id"}},
      "paragraph_index": {"$ref": {"task_id": 2, "path": "paragraph_index"}}
    }, "depends_on": [2, 3]}
  ]
}
⚠️ 跨章节关键：先用 explore_content 获取目标章节ID，再传给 locate_content！
"""


def get_all_planning_examples() -> str:
    """获取所有规划示例（用于基础 Planning Prompt）"""
    return (
        get_explore_content_examples() +  # 🔴🔴🔴 P0优先级：统一信息获取入口，放在最前面！
        get_new_tools_examples() +  # 工具升级提示（已废弃旧工具）
        get_operate_apply_examples() +  # 🆕 operate_apply 统一入口示例（P0优先级！）
        get_direct_answer_examples() +
        get_user_confirmation_examples() +
        get_staged_execution_examples() +
        get_creation_request_examples() +
        get_selected_text_examples() +
        get_multi_chapter_examples() +
        get_operation_tools_examples() +
        get_editor_workflow_examples()
        # ⚠️ 以下已移除（2026-01-23）：与 operate_apply 流程冲突
        # get_locate_content_examples()  - operate_apply 不再自动定位
        # get_search_examples()  - 搜索+修改场景已在 operate_apply 示例中覆盖
        # get_smart_rewrite_examples()  - 改写场景已在 operate_apply 示例中覆盖
    )


# 导出
__all__ = [
    "get_new_tools_examples",  # 新增：聚合工具示例
    "get_explore_content_examples",  # 新增：深度探索示例（2026-01-17）
    "get_operate_apply_examples",  # 🆕 新增：operate_apply 统一入口示例（2026-01-23）
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
