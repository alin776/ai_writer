• 我排查了，问题主要有两条链路在“定位信息”上断了，所以前端最后只能走“默认末尾”：

  - 规划执行链路里 request.context 没传进工具执行层，locate_content 拿不到 nodes_info，很难返回 node_id，后续 apply_chapter_edit 就缺
    定位。
  - HITL 构造 editor_action 时只塞了 type/position，把 node_id / paragraph_index / before_anchor / after_anchor / original_text 丢了；
    前端只认 editor_action，所以定位信息丢失后必然落到末尾。

  我已经在下面文件里补上了这两块信息传递（你现在再测，应该不再“跑到结尾”）：

  - 让 planning 的任务执行链路携带结构化 context：backend/app/services/agent/langgraph_agent.py、backend/app/services/agent/execution/

  nodes_info 是什么？

  - 它是编辑器当前文档的“节点 id 列表”（只发 id），用于把“第 N 段”精确映射到 node_id。locate_content 可以用它把段落索引转成 node_id；
    前端再用 node_id 定位到准确位置。

  这种方法科学吗？

  - 是目前最稳的路线：node_id 是结构化定位，稳定性远高于纯文本匹配。再以锚点/原文兜底，是“工程上最可靠”的组合。

  为什么 Cursor 能那么精准？

  - 它拿的是结构化信息（AST/符号表/编辑器真实位置），不是纯文本猜测。我们这边的等价路线就是：node_id > position > anchor > fuzzy。

  要更精准，还可以做什么？

  - 强制：只要没有 node_id/anchor/original_text 就拒绝 apply（返回“定位失败，需要你确认位置”），不要默认 append。
  - 选区优先：用户有选区时直接使用选区对应 node_id/position。
  - 位置校验：apply 前用 original_text + anchor 在当前文档做校验，失败就不落地。

  现在你可以这样验证是否真在用新代码

  1. 前端控制台看 agent-show-revision 事件是否带 nodeId/paragraphIndex。
  2. 后端日志看 locate_content 是否打印收到 nodes_info、是否返回 node_id。
  3. 如果仍然跑末尾，基本就是“老构建未生效/后端未重启”。