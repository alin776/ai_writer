  🎯 核心设计问题清单

  1. 探索触发机制

  ❓ 用户如何触发 explore 模式？
  - A. 专门的命令（如"探索段融的修炼历程"）
  - B. 自动判断（AI 识别用户意图需要深度探索）
  - C. UI 上的开关（勾选"启用探索模式"）
  - D. 混合方式（关键词触发 + UI 开关）

  ❓ explore_content 是独立工具还是流程的一部分？
  - 场景 1：用户直接调用 explore_content("段融修炼历程")
  - 场景 2：规划器判断需要探索，生成 explore_content 任务
  - 场景 3：在 Reflection 节点中自动触发探索

  你更倾向哪种方式？

  ---
  2. Review 评估逻辑（最核心）

  ❓ 如何判断"信息是否足够"？
  # 方案 A：纯 AI 判断
  review = await ai.evaluate(
      query="段融的修炼历程",
      collected_info=[...],
      prompt="判断已收集信息是否足够回答问题"
  )
  # 返回：{ status: "sufficient" | "insufficient", missing: [...] }

  # 方案 B：量化指标
  coverage_score = calculate_coverage(query, evidence)
  if coverage_score > 0.8:
      status = "sufficient"
  else:
      status = "insufficient"

  # 方案 C：混合（AI + 指标）

  ❓ 覆盖度如何计算？
  - 基于关键词匹配？
  - 基于语义相似度？
  - 基于用户问题的拆解覆盖？

  ❓ "缺少：浑圆桩训练"这种缺失项如何识别？
  # 示例：
  用户问题: "段融的修炼历程"
  AI 拆解: ["器灵吞噬", "浑圆桩训练", "一夕千悟", "五虎群羊刀"]

  第 1 轮收集到: ["器灵吞噬", "五虎群羊刀"]
  Review 输出: { missing: ["浑圆桩训练", "一夕千悟"] }

  第 2 轮针对性搜索: "浑圆桩训练"

  这个拆解和对比逻辑如何实现？

  ---
  3. 动态查询生成

  ❓ 每轮的 search_query 如何生成？

  # 第 1 轮
  search_query = "吞噬器灵 羚羊献食"  # 从哪来？

  # 第 2 轮
  search_query = "浑圆桩 训练"  # 如何知道要搜这个？

  # 第 3 轮
  search_query = "五虎群羊刀"  # 为什么是这个？

  可能的策略：
  - A. 从用户原始问题中提取关键词
  - B. 从上一轮的 review missing 中提取
  - C. 从已收集证据中发现新线索（实体抽取）
  - D. AI 生成下一步探索方向

  你觉得哪种更合理？

  ---
  4. 证据片段提取

  ❓ 从 read_result 中如何提取"证据片段"？

  read_result = {
      "chapters": [
          {
              "order": 5,
              "content": "第五章内容，共 3000 字...",
              "paragraphs": [...]
          }
      ]
  }

  # 如何变成这样？
  evidence = [
      {
          "meta": "第5章 · 第7段",
          "content": "赵穆的那柄刀，只有他一个人用过..."  # 50字
      }
  ]

  可能的方法：
  - A. 基于 search_query 的关键词高亮匹配
  - B. 使用 locate_content 定位后提取段落
  - C. AI 摘要提取相关句子
  - D. 混合方式

  ❓ 证据片段的长度如何控制？
  - 固定 50 字？
  - 完整段落？
  - 语义完整的句子？

  ---
  5. 轮次标题生成

  ❓ "初次检索与定位"、"补漏检索与二次定位" 这些标题是？

  round_titles = [
      "初次检索与定位",      // 固定？AI 生成？
      "补漏检索与二次定位",  // 如何知道是"补漏"？
      "交叉验证与收敛"       // 如何知道是"收敛"？
  ]

  方案：
  - A. 固定模板（第1/2/3轮）
  - B. AI 根据本轮行为生成（"本轮补齐了缺失项，标题：补漏检索"）
  - C. 基于 review 状态映射

  ---
  6. 缓存与性能

  ❓ 如何避免重复读取？

  # 场景：
  第 1 轮: search → locate 第5章 → read 第5章
  第 2 轮: search → locate 第2章 → read 第2章
  第 3 轮: search → locate 第5章 → read 第5章 (重复！)

  策略：
  - A. 在 explore_content 内部维护已读章节缓存
  - B. 复用现有的 ToolCache（但需要传递 state）
  - C. 如果检测到重复，跳过 read 直接用缓存

  ❓ 如果用户中断探索（关闭页面），如何处理？
  - 探索进度是否需要持久化？
  - 下次打开能否恢复？

  ---
  7. 与现有流程集成

  ❓ explore_content 和其他工具的协调？

  # 场景 1：用户问"分析段融修炼历程并续写第6章"
  规划器可能生成：
  tasks = [
      { tool: "explore_content", params: { query: "段融修炼历程" } },
      { tool: "smart_continue", params: { chapter: 6 }, depends_on: [1] }
  ]

  # 这样合理吗？
  # explore_content 的输出如何传递给 smart_continue？

  ❓ explore_content 是否应该支持嵌套？
  # 是否允许：
  explore_content("段融修炼历程", scope="chapters:1-10")
    → 内部又调用 explore_content("浑圆桩训练", scope="chapters:2-3")

  ---
  8. 错误处理

  ❓ 如果某轮 search 返回空结果？
  第 2 轮: search("浑圆桩训练")
  结果: []  # 没找到

  应该：
  A. 直接跳过这一轮，继续下一轮
  B. 尝试扩大搜索范围（去掉一些关键词）
  C. 标记为失败，提前结束
  D. 记录 warning 但继续

  ❓ 如何避免死循环？
  # 如果 AI review 一直判断"不足"
  第 1 轮: insufficient
  第 2 轮: insufficient
  第 3 轮: insufficient
  ...
  第 10 轮: insufficient (已到 max_rounds)

  # 这时应该返回什么？
  # - 部分结果 + 警告？
  # - 直接失败？

  ---
  9. 前端交互细节

  ❓ 流式推送时，UI 如何更新？

  // 方式 A：逐个标签出现
  [🔍 Search: 吞噬器灵]  (0.5s 后出现)
  [🔍 Search: 吞噬器灵] [🎯 Locate: ...]  (1s 后出现)
  [🔍 Search: 吞噬器灵] [🎯 Locate: ...] [📄 Read: ...]

  // 方式 B：整轮刷新
  (等本轮全部完成后，一次性显示完整轮次)

  // 哪种更好？

  ❓ 用户能否中途取消探索？
  - 需要 UI 上的"停止"按钮吗？
  - 取消后如何清理资源？

  ❓ 证据片段能否点击跳转？
  <div className="explore-item" onClick={() => jumpToChapter(5, 7)}>
    第5章 · 第7段
    赵穆的那柄刀...
  </div>

  ---
  10. 数据持久化

  ❓ 探索结果是否需要保存到数据库？
  - 作为对话历史的一部分？
  - 作为独立的 exploration_sessions 表？
  - 只在前端内存中？

  ❓ MemoryPack 是否需要包含探索证据？
  MemoryPack = {
      "characters": [...],
      "events": [...],
      "explore_evidence": [  # 新增？
          {
              "query": "段融修炼历程",
              "evidence": [...],
              "timestamp": "2026-01-17"
          }
      ]
  }

  ---
  📝 我的问题

  请告诉我你对以下问题的偏好：

  1. 触发方式：自动判断 vs 用户显式调用？
  2. Review 逻辑：纯 AI vs 量化指标 vs 混合？
  3. 查询生成：从 missing 提取 vs AI 生成下一步方向？
  4. 证据提取：关键词匹配 vs AI 摘要？
  5. 标题生成：固定模板 vs AI 生成？

  以及最关键的：

  6. 你希望 explore_content 是一个"黑盒工具"（内部循环，只返回最终结果），还是"可观测流程"（每轮都推送事件给前端）？

  回答完这些，我们才能设计出真正符合你需求的方案！