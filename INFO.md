🔴 协调性问题分析

  问题1: Checkpoint 标记依赖 AI 规划质量
  # Planning 阶段需要 AI 主动标记 checkpoint
  # 但如果 prompt 不够明确，AI 可能不标记或错误标记
  "tasks": [
    {"task_id": 1, "checkpoint": true},   # AI 需要自己判断
    {"task_id": 2, "checkpoint": false},
  ]

  问题2: 补偿机制可能过于机械
  # config.py 中的兜底策略
  MISSING_CHECKPOINT_INTERVAL: int = 3  # 每 3 个任务反思一次
  # 这种机械式触发可能在不需要反思时浪费时间

  问题3: 反思结果与后续任务的衔接
  # reflection.py 返回的 suggested_tasks 如何融入现有任务流？
  # 当前实现：直接替换 remaining_tasks
  # 风险：可能丢失原有任务的依赖关系

  问题4: 两层 prompt 不一致
  - get_planning_static_prompt() - 标准版（无 checkpoint 概念）
  - get_planning_agent_mode_prompt() - 增强版（有 checkpoint）
  - 如果 AI 在增强版 prompt 下仍不理解 checkpoint 的意义，整个反思机制就失效了

  ---
  🟡 要讨论的方向

  1. 是否需要更强制的 checkpoint 规则？
    - 比如：某些工具调用后必须反思（如 write_chapter_tool）
  2. 反思触发逻辑是否需要重构？
    - 当前：AI标记 + 失败 + 间隔
    - 可选：基于任务复杂度、执行时长、结果质量等
  3. DeepAgent 是否应该更深度集成到 LangGraph 节点中？
    - 当前是 "包装器" 模式
    - 可选改为 LangGraph 原生的 "条件边 + 反思节点"