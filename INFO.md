● 我已了解小说内容。这是一本关于段融魂穿异界、获得吞噬器灵能力的修仙武侠小说。他是源顺镖局的杂役弟子，正在学习五虎群羊刀。

  🧪 5条全方位测试 Prompt

  测试1：意图分类 + 一般对话 (IntentClassifier)

  这本小说的主角叫什么名字？他有什么特殊能力？
  测试点：
  - IntentClassifier 规则分类
  - handlers/handle_general() 委托
  - 简单问答响应

  ---
  测试2：Planning 模式 + 多任务执行 (PlanGenerator, ParallelExecutor)

  帮我分析段融这个角色的性格特点，并基于第1章的内容续写200字，展现他吞噬器灵后的内心活动
  测试点：
  - PlanGenerator.generate_plan()
  - ParallelExecutor.execute_tasks()
  - ResponseBuilder.build_final_response()
  - 多任务分解和执行

  ---
  测试3：写作场景 + 二次工具调用 (SecondaryToolHandler)

  续写第3章"一夕千悟"的结尾，描写段融成功感知到内息的那一刻，要求500字以上
  测试点：
  - SecondaryToolHandler.needs_secondary_tool_call()
  - SecondaryToolHandler.build_task_instruction()
  - handlers/handle_writing()
  - 创作类任务的直接返回

  ---
  测试4：分析场景 + AI整合 (ResponseBuilder.ai_summarization)

  从文学角度分析这本小说的写作技巧，包括：1.叙事手法 2.人物塑造 3.世界观构建 4.金手指设定的合理性
  测试点：
  - IntentClassifier 识别为 analysis 意图
  - ResponseBuilder.ai_summarization()
  - handlers/handle_analysis()
  - 流式响应生成

  ---
  测试5：卡文场景测试 (handle_stuck)

  我在写类似的修仙小说，主角刚获得金手指能力，但我不知道接下来怎么安排剧情让他成长，你能给我一些创作建议吗？
  测试点：
  - IntentClassifier 识别为 stuck 意图
  - handlers/handle_stuck()
  - 创作建议生成

  ---
  📋 测试覆盖矩阵

  | 测试 | Intent | Handlers    | Planning | Execution | Response  | Secondary |
  |------|--------|-------------|----------|-----------|-----------|-----------|
  | 1    | ✅     | ✅ general  | -        | -         | ✅        | -         |
  | 2    | ✅     | ✅ planning | ✅       | ✅        | ✅        | -         |
  | 3    | ✅     | ✅ writing  | -        | ✅        | ✅        | ✅        |
  | 4    | ✅     | ✅ analysis | -        | -         | ✅ AI整合 | -         |
  | 5    | ✅     | ✅ stuck    | -        | -         | ✅        | -         |

  ---
  请依次在你的应用中测试这5条 prompt，观察是否有报错。我会根据测试结果帮你进一步排查问题。