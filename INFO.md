🔴 核心问题：工具选择规则仍未生效

  | Prompt        | 预期工具                                | 实际工具              | 结果    |
  |---------------|-----------------------------------------|-----------------------|---------|
  | 1. 改写场景   | smart_rewrite                           | smart_rewrite         | ✅ 正确 |
  | 2. 续写场景   | continue_writing_tool + apply_to_editor | 没有续写任务！        | ❌ 错误 |
  | 3. 混合场景   | smart_rewrite                           | smart_rewrite         | ✅ 正确 |
  | 4. 多章节优化 | smart_rewrite                           | continue_writing_tool | ❌ 错误 |
  | 5. 润色+扩写  | smart_rewrite                           | continue_writing_tool | ❌ 错误 |

  ---
  🔴 问题1：续写场景完全没有生成续写任务（Prompt 2）

  行 318: [Planning] 直接回答模式，答案长度: 86
  行 322: [Planning-Alert] AI 违反协议：同时返回 direct_answer(86字) 和 3 个 tasks
  行 358: 任务分类: 输入型=3, 输出型=0, 展示型=0  ← 全是输入型！

  AI 只规划了"读取第3章、读取第4章、获取世界观"，没有续写任务。

  ---
  🔴 问题2：改写/润色场景错用 continue_writing_tool（Prompt 4、5）

  行 628: [TaskRunner] 调用 registry.call_tool(continue_writing)  ← Prompt 4
  行 770: [TaskRunner] 调用 registry.call_tool(continue_writing)  ← Prompt 5

  用户说"优化"、"润色"、"扩写"，AI 却选择了 continue_writing_tool。

  ---
  🟡 问题3：SmartRewriteInput Pydantic 验证失败

  行 150-159:
  [StandardTool] 'smart_rewrite' 不存在，降级到 @tool:
    3 validation errors for SmartRewriteInput
    - chapter_content: Input should be a valid string (input_value=None)
    - base_version: Input should be a valid string (input_value=None)
    - user_id: Input should be a valid string (input_value=None)

  原因：SmartRewriteInput 的 chapter_content、base_version、user_id 定义为必需参数，但传入了 None。

  ---
  🟡 问题4：Rate Limiter Redis 错误

  行 161, 508:
  Rate limiter error: type object 'RedisClient' has no attribute 'incr'

  ---
  🟡 问题5：数据库连接管理问题

  行 226-253:
  - Exception terminating connection
  - asyncio.exceptions.CancelledError
  - The garbage collector is trying to clean up non-checked-in connection

  ---
  🛠️ 需要修复的优先级

  | 优先级 | 问题                              | 修复方向                                                     |
  |--------|-----------------------------------|--------------------------------------------------------------|
  | P0     | Prompt 4/5 改写场景用错工具       | Planning Prompt 中强化"优化/润色→smart_rewrite"规则          |
  | P0     | Prompt 2 续写场景没有生成续写任务 | 检查 AI 为何跳过续写，可能需要更强的引导                     |
  | P1     | SmartRewriteInput 验证失败        | 将 chapter_content、base_version、user_id 改为 Optional[str] |