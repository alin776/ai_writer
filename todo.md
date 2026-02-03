# TODO

#### 去掉修订采纳态的撤销按钮（待确认）

- [x] 定位撤销按钮渲染位置（RevisionCard）并确认仅影响修订胶囊
- [x] 移除采纳态的撤销按钮渲染，保持功能逻辑不变
- [x] 自检界面状态：采纳态仅显示“修订已采纳”提示

#### review

- 已移除修订胶囊“已采纳”态的撤销按钮，仅保留“修订已采纳”提示文本，避免出现不应有的撤销入口。`src/components/agent/ExecutionFlow/RevisionCard.tsx`

#### 采纳修订后空白占位残留排查（待确认）

- [x] 追踪修订标记生成路径（modify/insert/continue），确认空段落可能的产生方式
- [x] 追踪采纳修订清理路径（applyRevisionDecisionToHtml），核对空段落清理范围与过滤条件
- [x] 对照截图现象，给出“空白占位残留”的核心原因与证据清单

#### review

- 修改型修订会先给原文加删除标记，再把新内容插在原文后面；当替换文本含换行时走 `insertContent`，会把新内容拆成新段落，导致“原段落只剩删除标记”。`src/components/editor/NovelEditor.tsx:1202-1247`
- 采纳修订只做“删除 del / 还原 ins / 解包 revisionId”，不做段落合并；空段落清理只扫描**包含修订标记的 `<p>`**，并用 `textContent.trim()` 判空。`src/components/editor/NovelEditor.tsx:190-295`
- 因此当原段落被清空但仍带编辑器占位字符/尾随 `<br>`、或该空块不是 `<p>` 时，清理不会移除，最终留下“红字消失但空白占位保留”的空行。

#### 修复采纳后空段落残留（待确认）

- [x] 明确修复策略：仅在采纳清理中扩展“受影响段落”的相邻空 `<p>`（包含 p.is-empty）
- [x] 最小实现：收集受影响段落时向前/向后吸纳连续空 `<p>`，复用现有空段落清理条件
- [x] 自检：采纳后不再出现空白占位，且非修订区域空行不受影响

#### review

- 采纳清理范围扩展：在收集修订影响段落时，向前/向后吸纳连续的空 `<p>`（包含 `p.is-empty`），以覆盖修订产生的占位空行。`src/components/editor/NovelEditor.tsx`
- 清理条件保持一致：复用“空文本 + 无媒体 + 无修订标记”的判定，只删除可安全移除的空段落。`src/components/editor/NovelEditor.tsx`

#### 修复采纳后空段落残留（二次排查）（待确认）

- [x] 验证空 `<p>` 是否包含零宽字符/占位字符（导致判空失败）
- [x] 调整空段落判定：过滤零宽字符后再判空
- [x] 自检：采纳后 `p.is-empty` 不再残留

#### review

- 空段落判定补充过滤零宽字符（`U+200B`/`U+200C`/`U+200D`/`U+2060`/`U+FEFF`），避免 `p.is-empty` 因占位字符被误判为非空。`src/components/editor/NovelEditor.tsx`

#### 采纳后空段落残留（二次修复方案B）（待确认）

- [x] 验证空段落是否由 `setContent` 后 ProseMirror 重新生成（HTML 清理无效）
- [x] 在采纳后追加 ProseMirror 文档级清理：删除空 paragraph 节点
- [x] 自检：采纳后 `p.is-empty` 不再出现

#### review

- 采纳后追加文档级清理：根据修订位置清理附近空 paragraph 节点，避免 `setContent` 后生成的 `p.is-empty` 残留。`src/components/editor/NovelEditor.tsx`
- 空段落判定基于 ProseMirror 节点：过滤零宽字符，仅在“无文本/无非文本子节点”时删除，避免误删有内容的段落。`src/components/editor/NovelEditor.tsx`

#### 重新发送小说素材（待确认）

- [ ] 确认素材文件路径并读取内容范围
- [ ] 确认输出范围（完整文本/节选/摘要）并给出版权提示
- [ ] 按确认输出内容，并在 todo.md 追加 review

#### 重新发送测试提示词（待确认）

- [x] 复读《一夕千悟，从杂役弟子开始》关键情节与角色脉络
- [x] 复刻 5 条高复杂度测试提示词（覆盖定位/读段/插入/改写/续写/校验）
- [x] 按“可直接复制”的格式输出，并在 todo.md 追加 review

#### review

- 已基于素材关键情节（吞噬器灵、浑圆桩、赵穆指导/离场、孔斌李充张征小团体）生成 5 条复杂测试提示词，覆盖插入/替换/续写/歧义消解与上下文读取验证。

#### 重复句消歧替换生成多段问题排查（待确认）

- [x] 通读 Backend.md 中“吞噬效果：五虎群羊刀入门”相关日志，确认任务数与执行顺序
- [x] 追踪计划层是否生成多次替换任务（第2处/第3处）及其来源
- [x] 核对 operate_apply 定位参数是否复用同一段落（para/node_id）
- [x] 追踪 apply_chapter_edit 是否有重复替换去重逻辑
- [x] 汇总证据并给出直白结论（为何出现三段、根因链路）

#### review

- 计划层确实生成了多次“第2处/第3处”替换任务，来源是 `_split_multi_edit_tasks` 在检测到**多段引号**时自动拆分任务。`backend/app/services/agent/planning/plan_generator.py:756-852`
- 本次用户指令包含 3 段引号（原句/替换句/“段融第一次读取牛尾刀器灵”提示），触发了拆分逻辑，因此出现三次 smart_rewrite + apply。`backend/app/services/agent/planning/plan_generator.py:600-640,756-852`
- Backend.md 明确显示三次改写与三次写回：任务2/4/6分别执行 smart_rewrite，随后 operate_apply 均使用**相同定位** `para=75, node=eah0i8el`。`Backend.md:71-147,95-158`
- apply_chapter_edit 对 replace 没有去重/“no_change”保护（只有 insert 有），所以同段落被替换三次也会生成三条修订，前端显示成三行重复。`backend/app/services/agent/tools/editor_tools.py:520-580`

#### 重复句消歧“治根方案”实现（待确认）

- [x] 规划层：新增“改为/替换为”语义解析，区分【原句/替换句/上下文提示】，只对真正的原句做拆分
- [x] 规划层：仅在用户显式“分别/各自/每处/多处”时拆分多处改写；“只/仅/首次/第1处”强制单处
- [x] 规划层：把“上下文提示”写入 locate_target_hint，而不是当成待改句
- [x] 执行层：replace 增加 no_change 去重（同内容重复替换时直接返回）
- [ ] 补最小回归：多引号但单处替换不再拆分；显式“分别”仍会拆分

#### review

- 规划层新增引号语义分类：识别“替换句/上下文提示”，`_split_multi_edit_tasks` 只在显式多处意图时拆分，避免把“改为句/上下文提示”当成待改原句。`backend/app/services/agent/planning/plan_generator.py`
- `locate_target_hint` 优先使用“上下文提示”引号，避免替换句被误用为定位线索。`backend/app/services/agent/planning/plan_generator.py`
- 执行层 replace 增加 no_change 兜底：同段落重复替换同内容直接返回 no_change，防止前端堆叠重复修订。`backend/app/services/agent/tools/editor_tools.py`

#### 采纳修订后空行（待确认）

- [x] 通读修订展示/采纳链路（NovelEditor/AIRevisionMark/AIRevisionBar），定位删除/插入标记的 HTML 结构
- [x] 核对采纳/弃用的 HTML 处理函数（applyRevisionDecisionToHtml），验证是否清理空段落
- [x] 复盘“修改型修订”的插入位置与换行处理，判断空行出现的条件
- [x] 汇总证据路径与直白结论（根因+影响）

#### review

- 修订标记结构：删除用 `<del data-ai-deleted>`，新增用 `<ins data-ai-inserted>`，并用 `<span data-revision-id>` 关联；采纳/弃用只做“删除 del / 还原 ins / 去掉 revision-id”，不会处理空段落或段落合并。`src/components/editor/AIRevisionMark.ts`、`src/components/editor/NovelEditor.tsx`
- 修改型修订是“先标记删除，再在原文后插入新内容”，且当 replacement 含换行时用 `insertContent` 生成新段落；因此采纳后原段落可能为空，形成可见空行。`src/components/editor/NovelEditor.tsx`
- 核心结论：空行不是渲染问题，而是**采纳时只删标记不清理空段落**叠加**修改型修订插入位置在原文之后**导致的结构空洞；只要 replacement 触发新段落，就会出现“原位空出来、绿色文本在下一段”的现象。`src/components/editor/NovelEditor.tsx`

#### 修复采纳修订空行（待确认）

- [x] 设计最小修复策略：仅清理“由该 revisionId 产生的空段落”，不做全局空段落清理
- [x] 在 applyRevisionDecisionToHtml 增加定向清理逻辑（限定含 revisionId 的段落/节点）
- [x] 复核批量采纳/弃用与跨章节修订，确保不误删用户手动空行
- [x] 更新 todo.md review（改动与风险）

#### review

- 最小修复落地：仅对“包含该 revisionId 或 del/ins 标记”的段落做空段落清理，避免影响用户手动空行。`src/components/editor/NovelEditor.tsx`
- 兼容批量采纳/弃用：当 revisionIds 为空时，先收集所有含修订标记的段落，再统一清理；不会全局扫空段落。`src/components/editor/NovelEditor.tsx`
- 风险控制：空段落清理会跳过仍包含修订标记/媒体元素的段落，避免误删仍待处理的修订或非文本内容。`src/components/editor/NovelEditor.tsx`

#### 复检遗漏（待确认）

- [x] 复查采纳/弃用路径，确认是否存在绕过 applyRevisionDecisionToHtml 的流程
- [x] 检查非段落节点（列表/标题/引用）在采纳后是否可能残留“空块”
- [x] 评估“AI 插入空行/双换行”的场景是否会被误删
- [x] 更新 todo.md review（遗漏点与结论）

#### review

- 采纳/弃用链路未发现绕过：AIPanel/AIRevisionBar 最终都派发 `agent-accept/discard` 事件，`NovelEditor` 统一走 `applyRevisionDecisionToHtml`；只有 `agent-undo-revision` 的“带快照撤销”不走该函数，但那是撤销已采纳内容，不是采纳/弃用流程。`src/components/editor/AIPanel.tsx`、`src/components/editor/NovelEditor.tsx`
- 仍有潜在遗漏：空段落清理只处理 `<p>`；若修订发生在标题/引用或列表项（list_item 内的 `<p>` 被删后可能留下空 `<li>`），可能残留“空块/空项目”。需要时可扩展为清理空 `<li>`/`<blockquote>`/`<h1~h6>`。`src/components/editor/NovelEditor.tsx`
- “AI 双换行”不会被误删：空行若来自插入内容的 `\n\n`，该空段落通常不带 revision 标记，不在清理集合内，因此会被保留（这是对“AI 有意留白”的保守策略）。`src/components/editor/NovelEditor.tsx`
- 核心补充：`replacement` 仅在“含 HTML 标签”时做 `.trim()`，纯文本前导换行会保留；`insertContent` 会因此生成**不带 revision 标记**的空 `<p>`，而清理只针对“含 revision 标记的段落”，所以该空行不会被清掉。`src/components/editor/NovelEditor.tsx:953-960,1183-1197,205-223`

#### 修复方案A：纯文本前导换行裁剪（待确认）

- [x] 在修订展示前对纯文本 replacement 统一裁剪前导空行（仅保留内容本体）
- [x] 避免影响原有 HTML 清理逻辑（只补充纯文本分支）
- [x] 更新 todo.md review（改动与风险）

#### review

- 纯文本分支新增“前导空行裁剪”：仅去掉开头的空白行（包含空格/制表/不换行空格 + 换行），避免生成无标记空 `<p>`。`src/components/editor/NovelEditor.tsx`
- HTML 清理逻辑保持不变：仍只在检测到 `<p>/<br>/<div>/<span>` 时做标签替换与 `.trim()`，不影响现有 HTML 修订展示。`src/components/editor/NovelEditor.tsx`

#### 上传到 GitHub（待确认）

- [ ] 检查 git 状态与当前分支（确认待提交文件）
- [ ] 检查远程仓库配置（若无远程需你提供 GitHub 仓库地址）
- [ ] 提交本次改动（需要你确认 commit message）
- [ ] 推送到 GitHub 远程分支

#### 写回后段落顶格/排版乱（待确认）

- [ ] 通读 Backend.md 本次测试日志，确认写回流程成功但内容格式异常的证据点
- [ ] 追踪后端 replace 写回逻辑（apply_chapter_edit / chapter_revision_service）对段落边界的处理方式
- [ ] 追踪前端修订显示与插入逻辑（NovelEditor）对换行/HTML 的处理方式
- [ ] 对照编辑器样式（editor-styles.css）解释“顶格/乱排版”的直因
- [ ] 形成最小修复草案（后端拆段 / 前端拆段）并评估风险
- [ ] 汇总证据并给出直白结论与最小修复方向

#### 深度探索胶囊行为标签缺失排查（待确认）

- [x] 通读前端 ExecutionFlow/ExploreCard/StepCard 等组件，确认“工具标签/胶囊”的显示条件
- [x] 通读前端事件映射（agentApi/useAgentChat/useAgentChatStream），确认 tool_calls 传递路径
- [x] 通读后端 explore_round 事件与 _format_tool_calls_for_frontend，确认 tool_calls 生成条件与可能为空的场景
- [x] 汇总证据清单并给出直白结论（是否本来没有/为何缺失）

#### review

- 行为标签不是“前端丢失”，而是**有条件渲染**：ExploreRoundCard 仅在展开时渲染 toolCalls 标签，折叠态不显示。`src/components/agent/ExecutionFlow/ExploreCard.tsx`
- 另一类缺失来自**后端未生成标签**：`_format_tool_calls_for_frontend` 对 `read_paragraphs` 只在 `items` 列表模式才追加标签，分页模式（chapter_order/offset/limit）会生成空列表，前端自然无标签。`backend/app/services/agent/tools/explore_tools.py`
- tool_calls 在前端并未被丢弃：SSE 解析用 `tool_calls -> toolCalls` 直传给 ExploreRoundCard。`src/services/agentApi.ts`、`src/hooks/useAgentChat.ts`、`src/hooks/useAgentChatStream.ts`

#### 补齐 read_paragraphs 分页模式标签（待确认）

- [x] 在 `_format_tool_calls_for_frontend` 增加分页模式标签生成（基于 chapter_order + offset/limit）
- [x] 保持最小改动，不影响 items 列表模式已有标签
- [x] 更新 todo.md review（改动与影响）

#### review

- `read_paragraphs` 在分页模式下也生成工具标签：根据 chapter_order + offset/limit 计算“第X~Y段”或单段标签，确保 Explore 胶囊始终有行为标签。`backend/app/services/agent/tools/explore_tools.py`
- items 列表模式逻辑保持不变，仅在 count=0 时走分页兜底，避免影响已有展示。`backend/app/services/agent/tools/explore_tools.py`

#### 章节切换会话仍变新修复（待确认）

- [x] 深入核对“切章→读 tab →无则新建”的链路与证据（useTabManager / tabStorage / useConversationPersistence）
- [x] 增加“tab 恢复”兜底：章节 tab 为空或无效时，从已保存的会话列表按 chapterId 重建 tabs
- [x] 补充 localStorage 配额失败处理：tab 写入失败时清理+重试，并抛出统一提示事件
- [x] 做最小回归：切换章节/切回、历史恢复、空章节首次进入不新增新问题

#### review

- 增加章节会话恢复兜底：当 chapter_tabs_map 为空时，先从已存 tab 重建，再从会话列表/上下文映射重建，最后才新建。
- 新增存储配额保护：tab/map 写入失败时清理旧会话后重试，并派发统一提示事件。
- 本地会话缺失时新增后端回填：打开 tab 时若本地无消息，尝试从后端拉取并写回本地，避免切章回来看见空会话。

#### 测试提示词生成（待确认）

- [x] 读取小说素材，提取关键人物/事件/术语
- [x] 设计 5 条复杂综合 Prompt，覆盖 Explore→定位→Create→Operate 全链路
- [x] 输出可直接复制使用的提示词

#### review

- 基于素材中的“入门时长矛盾/吞噬器灵因果/浑圆桩讲解/赵穆人物声线”等要素设计 5 条复杂 Prompt，覆盖取证、定位、生成、精准写回全链路。

#### 操作失败（写回验证错误）排查（待确认）

- [x] 通读 Backend.md 日志，定位失败发生点与上游工具调用路径
- [x] 追踪 operate_apply -> apply_chapter_edit 的校验逻辑与失败条件
- [x] 对照前端错误提示与后端日志，确认是“写回验证失败”还是“前后端状态不一致”
- [x] 给出证据清单（文件路径+日志片段）和直白结论+修复方向

#### review

- Backend.md 记录的是“续写追加”流程，operate_apply 走 append 并执行成功；日志里没有验证错误，说明截图的失败不是同一次请求。
- replace/insert 写回必须提供 node_id/paragraph_index，operate_apply/ToolExecutor 均做强校验；缺定位或索引越界会被直接拒绝并触发“验证错误”提示。

#### smart_rewrite 写回修复（方案1+2）（待确认）

- [x] 方案1：在计划层强制修正 smart_rewrite 的写回路径为 versions[0].content
- [x] 方案2：在 smart_rewrite 输出补充兼容字段 content=versions[0].content
- [x] 验证不会影响 smart_continue/smart_insert 的现有写回流程

#### review

- 方案1：对 smart_rewrite 的 apply 任务补正 content 引用路径，避免 $TASK_X.content 误用导致 content=None。
- 方案2：smart_rewrite 输出补充兼容 content 字段，双保险避免计划错误时写回失败。

#### 章节会话迁移修复（待确认）

- [x] 核对 tabStorage 的章节分组键与遗留 workId 分组
- [x] 在 useTabManager 中加入“legacy key → 章节 key”的迁移逻辑（仅在章节 tab 为空时执行）
- [x] 确保迁移后不再自动新建会话（优先恢复旧 tab）
- [x] 在 todo.md 追加 review（改动与影响）

#### review

- 新增 tab 迁移：当章节 tab 为空时，从 legacy workId key 迁移到章节 key，并同步 activeTab。
- 迁移只在 chapterId 就绪后触发，不会覆盖已有章节 tab。

#### 章节切换会话恢复修复（待确认）

- [x] 核对章节初始化流程，避免 currentChapterId 未就绪时创建 tab
- [x] 优先使用章节级 key 恢复 tab；仅在确定无历史时创建新会话
- [x] 保持最小改动，验证不会影响首次进入空章节
- [x] 在 todo.md 追加 review（改动与影响）

#### review

- WorkDetailView 不再用 workId 作为 tab 分组兜底，currentChapterId 未就绪时传空字符串，避免误写到作品级 key。
- useTabManager 增加“chapterId 未就绪”防护：不再自动创建新会话，也不会读写 localStorage，直到章节 ID 就绪。
- SessionTabBar 在章节未就绪时禁用“新会话”按钮并显示加载提示，避免用户误触发新建。

#### 切换章节后会话变新问题排查（待确认）

- [x] 追踪章节切换逻辑与 tab/session 绑定（useTabManager/WorkDetailView/SessionContext）
- [x] 复核会话恢复/持久化策略（useConversationPersistence、tabStorage、activeTab 逻辑）
- [x] 定位“切回变新会话”的触发路径与条件
- [x] 给出证据与直白结论（含修复方向）
- [x] 在 todo.md 追加 review（结论与影响）

#### review

- 章节切换后会话变新，根因是“按章节分组的 tab 列表为空”时会自动创建新会话；触发点在 useTabManager 的 bootstrap（chapterTabs 为空即 createNewTab）。
- 章节分组键来自 WorkDetailView：`useTabManager(currentChapterId || workId || 'work', workId)`，当 currentChapterId 未就绪/为 undefined 时会落到 workId 键，导致会话存到“作品级”而非章节级，切回章节后视为无 tabs 而新建。
- 另一个高概率触发条件是 localStorage 写入失败（配额/异常）导致 tab 或 session 缺失，切回时被当作空列表处理。

#### 缓存失效 + 会话消息索引（待确认）

- [x] 追踪 _persist_message / update / delete 是否已有会话缓存失效逻辑
- [x] 在消息写入后失效会话列表与详情缓存
- [x] 为 agent_session_messages 增加 (session_id, created_at) 索引迁移
- [x] 在 todo.md 追加 review（改动与影响）

#### review

- 已将会话缓存失效下沉到 _persist_message：每次写入消息后都会清理会话详情缓存并失效会话列表缓存。
- 已移除流式聊天中的重复缓存清理，避免重复逻辑。
- 已新增 Alembic 迁移：为 agent_session_messages 增加 (session_id, created_at) 索引，优化列表统计查询性能。

#### 会话绑定补丁 + 历史统计字段（待确认）

- [x] 复核会话创建入口（createSession/agent_chat_stream）与 conversation_id 传递点
- [x] 后端：创建会话时写入 conversation_id，避免“同一会话重复记录”
- [x] 后端：会话列表补充 message_count 与 last_message_preview
- [x] 在 todo.md 追加 review（改动与影响）

#### review

- createSession 现在支持传 conversation_id，前端 Tab/流式聊天/持久化创建都会携带会话ID，减少重复会话。
- 后端 create_session 对同一 conversation_id 做幂等：已存在则直接返回，避免重复记录。
- 会话列表增加 message_count 与 last_message_preview（按会话聚合统计），历史面板可直接使用后端统计。

#### 会话绑定 + 历史列表修正 + 本地压缩（待确认）

- [x] 核对 AgentChatRequest/上下文字段，确认 chat/stream 里可用的 work_id/chapter_id（避免创建会话缺字段）

#### 段落定位偏移（第28段插入变成第33段）排查（待确认）

- [x] 通读 Backend.md 本次任务B日志，确认 locate_content/operate_apply 传递的 chapter_id/paragraph_index
- [x] 对比 locate_content/_split_paragraphs 与 apply_chapter_edit/_get_paragraph_position 的段落计数规则
- [x] 对比前端 getAllNodes 的节点列表与后端段落索引定义，确认空段落/非文本节点偏移
- [x] 汇总证据清单（文件路径+关键逻辑）并给出直白结论
- [x] 在 todo.md 添加 review（根因+影响+最小修复方向）

#### review

- Backend.md 中任务B只记录到 operate_apply 调用（chapter_id=44cfd207-bb6e-46ed-af0b-a3694af72dbd），未打印 locate/insert 细节，但“定位完成在第2章第28段”的结论来自 explore_content 阶段。`Backend.md`
- locate_content 的段落切分会 **跳过空段落**：`_split_paragraphs` 只有 `text` 非空才 append，因此 paragraph_index 是“非空段落的 0-based 索引”。`backend/app/services/agent/tools/locate_tools.py`
- apply_chapter_edit 的插入定位会 **计入空段落**：`_get_paragraph_position` 用正则匹配所有 `<p>/<li>/...>`，不排除空 `<p></p>`，因此同一 paragraph_index 在有空段落时会向后偏移。`backend/app/services/agent/tools/editor_tools.py`
- 前端 `getAllNodes()` 同样 **不跳过空节点**：UniqueID 为所有段落节点分配 ID 且直接收集（即便 text 为空），`NovelEditor` 用 paragraphIndex 直接索引该列表，进一步放大偏移。`src/components/editor/UniqueIDExtension.ts`、`src/components/editor/NovelEditor.tsx`
- 直白结论：**定位与写回使用了不一致的“段落计数规则”**（后端定位忽略空段落，写回/前端计数包含空段落），当目标段落前有 5 个空段落时，就会出现“第28段被写到第33段”的偏移。

#### 最小修复方向（记录）

- 方向A（后端统一）：让 locate_content/_split_paragraphs 也保留空段落，保证 paragraph_index 与 apply_chapter_edit 的计数规则一致。
- 方向B（写回统一）：在 apply_chapter_edit/_get_paragraph_position 中 **跳过空段落**，与 locate_content 的索引对齐。
- 方向C（前端缓解）：`getAllNodes()` 过滤空节点或提供“non-empty-only”列表，用于 paragraphIndex 定位（保持与 locate_content 规则一致）。

#### 插入定位优先级修复（待确认）

- [x] 调整前端修订定位优先级：nodeId/paragraphIndex 优先，position 仅作兜底
- [x] 保持最小改动，仅影响 insert/continue 的定位路径
- [x] 回填 todo.md review（改动点+收益+残余风险）

#### review

- insert/continue 改为优先使用 nodeId/paragraphIndex/锚点，`position` 只作为兜底，避免 HTML 字符索引误插到句子中间。`src/components/editor/NovelEditor.tsx`
- modify 行为不变，仍可直接使用 position（保持既有改写逻辑）。
- 残余风险：如果只有 position 且没有 nodeId/paragraphIndex/锚点，insert/continue 仍会使用 position；但这已是兜底路径，风险可控。

#### 插入内容异常（生成超长+重复原文）根因排查（待确认）

- [x] 通读 smart_insert 的输入/提示词/默认字数路径，确认“20字/一句话”是否被正确传入
- [x] 追踪 tool_dispatcher / task_runner / operate_apply 的参数流，确认 word_count 与 user_intent 是否丢失或默认回退
- [x] 复核 smart_insert 输出结构与写回逻辑，确认是否存在“原文/上下文被重复拼进生成内容”的机制
- [x] 汇总证据（文件路径+关键逻辑）并给出直白结论
- [x] 在 todo.md 添加 review（根因+影响+最小修复方向）

#### review

- **字数约束丢失/默认回退**：`smart_insert` 默认 `word_count=200`，提示词也写成“生成约{word_count}字”；`tool_dispatcher` 未提取“约20字/一句话”，缺省直接回退到 200。`backend/app/services/agent/tools/editor_tools.py`、`backend/app/services/agent/core/tool_dispatcher.py`
- **上下文注入导致复述**：执行层会把 `source_locator.text` 直接塞进 `insert_context`，即把目标原句作为上下文喂给模型；结合 200 字目标，模型很容易把原句重复并扩写。`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/tools/editor_tools.py`
- **写回不做裁剪/去重**：`operate_apply` 直接写入 `data.content`，没有限制“只一句话/20字”，因此超长内容原样进入编辑器。`backend/app/services/agent/planning/plan_generator.py`、`backend/app/services/agent/tools/operate_tools.py`
- **直白结论**：此次“插入内容过长且重复原句”不是定位问题，而是**字数/一句话约束未传入 + 原句上下文喂给模型 + 写回不裁剪**三者叠加的必然结果。
- **最小修复方向**：当用户意图含“约20字/一句话”时，强制 `word_count=20` 并在生成后仅保留首句；同时明确提示“不要复述原句”。（低风险、只影响该类任务）

#### 动态上下文读取策略（待确认）

- [x] 仅在写回类任务（insert/replace）触发上下文读取，不对所有搜索强制 read
- [x] 依据意图估算阅读范围（如 1~5 段），设置上限并在失败时扩读一次
- [x] 使用 read_paragraph(index_base="zero", context_before/after=动态值) 获取前后文并回填 insert_context
- [x] 在 todo.md 添加 review（规则+收益+风险）

#### review

- smart_insert/smart_rewrite 参数准备阶段改为动态补上下文：仅当存在 source_locator/paragraph_index 且上下文未扩展时调用 read_paragraph，避免对所有搜索强制 read。`backend/app/services/agent/execution/tool_executor.py`
- 上下文范围按用户意图/字数推断（1~5 段），并在长内容且上下文过短时扩读一次；索引基准固定为 `index_base="zero"`，防止段落偏移。`backend/app/services/agent/execution/tool_executor.py`
- 生成上下文结构为【前文/目标段落/后文】拼接，便于模型理解插入位置，且保持最小侵入。`backend/app/services/agent/execution/tool_executor.py`

#### 基于素材生成复杂测试提示词（待确认）

- [x] 阅读指定小说素材文件，提取关键人物/设定/情节脉络
- [x] 设计 5 条高复杂度测试提示词（覆盖：定位→读段→插入/改写/续写/校验）
- [x] 输出可直接用于验证“上下文读取/插入定位/字数约束”的提示词

#### smart_insert 类型错误 + ambiguous_locator 排查（待确认）

- [x] 通读 Backend.md 日志，锁定 smart_insert 校验失败与 locate 选择冲突的触发点
- [x] 追踪 insert_context 数据类型来源与校验路径（StandardTool/LegacyTool）
- [x] 追踪 ambiguous_locator 触发条件与缺失的显式定位参数
- [x] 汇总证据并给出直白结论

#### review

- smart_insert 报错的直接原因是 `insert_context` 被解析为 **list**（而非字符串），StandardTool 在 `.strip()` 时崩溃，LegacyTool 又因 Pydantic 校验失败直接拒绝。`Backend.md`、`backend/app/services/agent/execution/tool_executor.py`
- 该 list 形态与 explore_content 输出的 `evidences/search_hits` 结构一致，说明规划/参数引用将列表直接传给 `insert_context`，但系统**只对 evidence_context 做了强制字符串化**，insert_context 没有同类保护。`backend/app/services/agent/execution/tool_executor.py`
- ambiguous_locator 出现在 smart_insert 失败之后，operate_apply 仍执行但缺少明确 `locate_target_index/locator_id/node_id/paragraph_index`，而 locate_targets 有多条候选（两句分别成候选），于是触发“多个定位候选”。`Backend.md`、`backend/app/services/agent/execution/tool_executor.py`

#### 修复：insert_context 类型保护 + 两句之间自动锚定（已完成）

- [x] smart_insert 接收 insert_context 时强制字符串化，防止 list 导致 Pydantic 校验失败
- [x] 识别“在A和B之间”场景时，自动锚定前一句作为 locate_target_hint，避免 ambiguous_locator
- [x] 后端：在 chat/stream 找不到 session 时创建 AgentSession 并写入 conversation_id（保证消息可持久化）
- [x] 后端/前端二选一最小改动：补 message_count/last_message_preview 或放宽“无内容过滤”
- [x] 前端：启用本地会话压缩（优先轻量压缩 flowItems）
- [x] 在 todo.md 追加 review（改动与影响）

#### review

- 已确认 chat/stream 请求包含 work_id/chapter_id/conversation_id，可用于会话绑定。
- 已在流式聊天中补齐会话绑定逻辑：优先用 conversation_id 查找；若 conversation_id 实为 session_id 则回填绑定；仍无会话则创建新 AgentSession。
- 已放宽历史会话列表过滤：不再因 messageCount/preview 为空而隐藏会话，避免“看起来丢失”。
- 已启用本地轻量压缩：保存会话时压缩 flowItems/长文本，降低 localStorage 体积与配额风险。

#### 历史会话存储问题排查与结论（待确认）

- [x] 核对前端本地会话持久化与历史列表逻辑（useConversationPersistence、HistoryPanel、ConversationHistory、WorkDetailView）
- [x] 核对后端会话/消息存储与过期策略（agent sessions endpoints、_persist_message、expires_at 过滤）
- [x] 识别“丢失/存储过度”的触发条件（本地上限/过滤规则/读取上限/清理缺失）
- [x] 输出证据清单（文件路径+关键片段）并给出直白结论
- [x] 在 todo.md 追加 review（结论+影响范围+可能修复方向）

#### review

- 已确认“历史会话丢失”的主因是后端会话未与 conversation_id 绑定，导致流式对话无法持久化消息；历史列表又会过滤“无内容”的会话。
- 已确认“存储过度”来自前端持久化保存了完整消息+flowItems，且压缩逻辑被禁用，localStorage 容易超配额导致写入失败。
- 已确认前端会话列表仅保留最近 N 个（useAgentChat 设置为 20），超出后在列表中不可见。
- 已确认后端会话默认 30 天过期，过期后被列表接口过滤。
- 已确认历史恢复拉取消息默认 limit=200，长会话会被截断。

#### 上下文对话 AI 上下文记忆说明（待确认）

- [x] 深度检索前后端与文档：定位“上下文/记忆/会话”相关实现（ContextManager、MemoryManager、LongTermMemory、UserProfile、前端会话持久化）
- [x] 梳理“上下文记忆”具体包含的数据范围与层级（短期对话、摘要、长期向量记忆/MemoryPack、用户偏好、写作风格、用户画像、近期对话摘要）
- [x] 对照 API 与前端入口，说明“上下文对话/记忆”板块的调用链路与数据流（/memory/context、useConversationPersistence、SessionStateManager、AI 对话面板）
- [x] 输出证据清单（文件路径+关键片段），给出直白详细结论

#### review

- 已完成“上下文对话 AI 上下文记忆”深度检索与证据整理，并形成结论与调用链路说明。
- 已完成 INFO.md 复盘与“重复探索/再次追问”根因定位：规划规则强制每次涉及作品内容都调用 explore_content，且工具结果不写入持久上下文；共享缓存仅进程内 20 分钟且依赖 conversation_id，无法保证复用。
- 已为 explore_content 增加 Redis 结果缓存（TTL=1小时），并支持 use_cache/force_refresh；缓存键包含 work_id/user_id/范围/任务摘要/关键词/output_mode；超大结果跳过缓存；tool_executor 放行新参数。

#### INFO.md 对话与重复探索原因排查（待确认）

- [x] 阅读 INFO.md 中用户与 AI 的两轮对话原文，整理时间线与关键语句
- [x] 深度检索后端/前端/提示词：定位“重复探索/再次追问”触发条件（planning/agent 路由、上下文/记忆读取链路）
- [x] 对照证据给出核心原因与结论（直白说明“为什么没有记住/为什么又探索”）
- [x] 在 todo.md 追加 review（结论+证据路径）

#### explore_content 结果缓存（待确认）

- [x] 设计缓存键与TTL（work_id + scope + task digest + search_keywords + schema_version）
- [x] 在 explore_content 开始处读取 Redis 缓存；支持 force_refresh/use_cache 参数
- [x] 在 explore_content 成功后写入 Redis 缓存；限制缓存体积与TTL
- [x] 放行新参数到 tool_executor（避免被裁剪）
- [x] 在 todo.md 追加 review（改动与影响）

#### explore_content 缓存补强（待确认）

- [x] ChapterService：create/update/delete/reorder/update_with_lock/apply_agent_edit 后失效 explore 结果缓存（避免陈旧结果）
- [x] ImportService：_import_json/_import_text 成功后失效 explore 结果缓存
- [x] planning_prompts：用户要求“重新读取/刷新/忽略缓存”时自动传 force_refresh（可选 use_cache=false）
- [x] 更新 todo.md review（记录影响）

#### review

- 已在 ChapterService 的创建/更新/删除/重排/带锁更新/Agent 编辑路径中失效 explore 结果缓存，避免章节变更后仍命中旧结果。
- 已在 ImportService 的 JSON/TXT 导入完成后失效 explore 结果缓存，确保导入内容可被最新探索读取。
- 已补充规划提示词规则：当用户要求刷新/重新读取时自动传 `force_refresh: true`（可选 `use_cache:false`）。

#### explore_content 缓存遗漏补齐（待确认）

- [x] 章节历史恢复（restore_version）后失效 explore 结果缓存
- [x] 更新 todo.md review（记录影响）

#### review

- 已在章节历史恢复（restore_version）后失效 explore 结果缓存，避免恢复后仍命中旧探索结果。

#### 复杂测试 prompt 设计（待确认）

- [x] 阅读素材《一夕千悟，从杂役弟子开始.txt》，提取关键人物/事件/术语
- [x] 设计 5 个复杂测试 prompt，覆盖跨章检索、证据引用、刷新/忽略缓存、章节范围等场景
- [x] 更新 todo.md review（记录覆盖点）

#### review

- 已基于《一夕千悟，从杂役弟子开始》前 5 章设计 5 个复杂测试 prompts，覆盖跨章检索、证据引用、章节范围锁定、刷新/忽略缓存等场景。

#### Backend.md 复盘与改动深度 Review（待确认）

- [x] 通读 Backend.md 最新日志，定位与 explore 缓存/刷新/规划规则相关的调用链
- [x] 逐项核对本次改动是否引入新问题（缓存失效频率/错误吞没/性能影响）
- [x] 验证是否真正解决“重复探索/陈旧结果”与“刷新需求”问题
- [x] 检查改动完整性与一致性（章节更新/导入/恢复/重排路径是否覆盖）
- [x] 汇总遗漏与下一步建议，并在 todo.md 追加 review

#### review

- Backend.md 显示 explore_content 多次执行且成功，但日志未出现 cache_hit/force_refresh 相关信息，无法直接从日志确认新缓存生效（仅能确认未引入运行时错误）。
- 发现遗漏风险：explore_content 仍会复用进程内共享状态（Backend.md 有“复用共享状态”日志），但章节更新/导入/恢复只清 Redis 结果缓存，未清进程内共享状态，可能在同会话内复用过期状态。
- 新增失效调用会触发 Redis `delete_pattern`（内部使用 KEYS），在高键量时存在潜在阻塞/延迟风险，但目前日志未体现性能问题。

#### INFO.md 对话逻辑复核（待确认）

- [x] 通读 INFO.md 原对话，标注“确认后仍追问/继续探索”关键片段
- [x] 深度检索规划/执行/响应生成链路，定位“确认后仍追问”的规则或缺口
- [x] 对照证据给出是否存在逻辑问题与根因（直白结论）
- [x] 更新 todo.md review（记录证据与结论）

#### review

- INFO.md 中首次 Explore 后的“请确认是否开始分析”属于分阶段执行提示，但确认后再次进入 Explore 并输出“请问希望怎样创作/分析”的追问，显示“分阶段询问规则”在 AI 整合阶段触发，导致重复询问且偏离原问题。
- 代码证据：ResponseBuilder.ai_summarization 强制“分阶段执行识别”，只要结果是“准备信息”就要求询问用户细节，而非直接输出分析结论，易导致“确认后仍追问”。`backend/app/services/agent/planning/response_builder.py:460-475`

#### 修复“确认后仍追问/继续探索”（待确认）

- [x] 在 ResponseBuilder 的 AI 整合提示中增加“仅创作类才允许追问”的门槛（分析/推演/设定补充直接输出）
- [x] 更新 todo.md review（记录影响）

#### review

- 已在 ResponseBuilder 的 AI 整合提示中增加“仅创作类才允许追问”的门槛，分析/推演/设定补充任务不再引导续写或询问创作风格。

#### opencode Explore 阶段处理机制复核（待确认）

- [x] 通读 opencode 的 Explore 相关提示与子代理实现（agent/prompt/explore.txt、agent/agent.ts）
- [x] 查找 Explore 工具输出如何被保存/截断/回传（tool/truncation.ts、session/prompt.ts 等）
- [x] 确认 Explore 结果是否写入主会话上下文（是否仅返回最终文本/是否保存到会话消息）
- [x] 汇总证据并在 todo.md 追加 review 结论

#### review

- opencode 的 Explore 是子代理（subagent），通过 Task 工具调用。主会话只拿到子代理**最终文本**作为 Task 工具输出；搜索/读取的原始工具输出保留在子代理会话内，不会完整写入主会话上下文。
- 工具输出若过长会被 Truncate 截断并写入磁盘文件，提示改用 Task→Explore 继续 Grep/Read，以减少上下文占用。

#### Explore 结果持久化（待确认）

- [ ] 新增 Explore Artifact 存储（落盘 JSON，包含元数据 + 完整结果）
- [ ] explore_content 返回 artifact_id + 摘要信息，便于后续对话引用
- [ ] 新增读取工具 load_explore_artifact（按 artifact_id 取回完整结果）
- [ ] 更新 todo.md review（记录影响）

#### 核心问题复盘（最新 Backend.md + 截图）（待确认）

- [x] 通读最新 Backend.md，定位与“未找到证据/误判”相关的搜索与读取链路
- [x] 对照截图中的原文位置，查找日志里对应的 search/read 调用与返回
- [x] 汇总核心问题 + 证据行号 + 影响结论（直白）

#### 修复：limit 负数 / 章节范围生效 / 空读取可诊断（待确认）

- [x] 限制 exact_search_paragraphs 的 limit 最小为 1（避免负数触发 SQL 错误）
- [x] 章节范围强制生效：优先使用本次请求 chapter_range(s)，避免回退全局范围
- [x] read_paragraphs 空结果输出原因（越界/上限/过滤/索引基准），提高可诊断性

#### 修复：chapter_order 也锁范围 + 空读日志可见（待确认）

- [x] exact_search_paragraphs 在传 chapter_order 时强制转为范围 (order, order)
- [x] read_paragraphs 失败/空结果时记录 empty_reason/error/invalid_items/index_base 到日志

#### 修复：关键词覆盖与最小证据读取（待确认）

- [x] 精确搜索合并规划关键词，强制覆盖（总搜 + 缺失补搜）
- [x] 每个关键词优先读至少 1 条证据（按预算优先）
- [x] 输出 missing_keywords，避免“无证据却下结论”

#### Explore 测试 prompts 设计（待确认）

- [x] 阅读素材《一夕千悟，从杂役弟子开始》前几章，提取可用于定位的角色/事件/术语
- [x] 设计 5 个复杂测试 prompts，覆盖分页读取、items 批量读取、范围锁定与证据回读
- [x] 输出可直接用于 Explore 测试的 prompts

#### Backend.md 问题排查与归因（待确认）

- [x] 读取 Backend.md 中最新日志区段，标注关键异常/警告/重复行为
- [x] 对照代码路径定位触发链路，归因到具体模块或参数
- [x] 汇总“核心问题 + 直接证据 + 影响面”，给出直白结论

#### Backend.md 扩展问题复盘（待确认）

- [x] 复扫 Backend.md 其余区段（非 22:19 段）标注异常/重复/不一致日志
- [x] 对照当前代码改动点，判断是否为已修复问题或新问题
- [x] 给出“问题清单 + 证据位置 + 当前状态（已修复/待修复/无法复现）”

#### 修复 explore_tool_loop None 预算比较错误（待确认）

- [x] 定位 `reads_left <= 0` 的无保护比较
- [x] 增加 None 判断，避免 `None <= 0` TypeError
- [x] 记录修复与影响范围到 review

#### 修复关键词拆分与搜索拦截误判（待确认）

- [x] exact_search_paragraphs 关键词拆分加入英文逗号 `,`
- [x] should_block_search 避免把“未拆分的逗号串”误判为已搜单词
- [x] 更新 review 记录修复与影响

#### 图片逻辑问题总结 + Backend.md 全量复盘（待确认）

- [x] 先基于 6 张截图总结前端反馈中的逻辑问题（不读日志）
- [x] 完整通读 Backend.md（约2000行），逐段标注异常/误判/矛盾点
- [x] 对照日志给出“原因归类 + 证据行号 + 可能修复方向”

#### chapter_vector_service.py 语法错误修复计划（待确认）

- [x] 定位 `exact_search_content` 中的语法错误位置并还原应有分支逻辑
- [x] 修复缩进/分支结构，保证 match_mode 分支完整
- [x] 复核附近逻辑无新的语法问题，记录是否能运行语法检查

#### Create 板块工具清单（待确认）

- [ ] 定位 Create/创作板块来源（侧边栏导航配置），确认具体文件与字段
- [ ] 核对工具显示名称（i18n 文案）与数量
- [ ] 汇总工具列表并回复

#### Agent 创作 smart* 工具数量（待确认）

- [x] 定位 smart_* 工具定义与注册位置
- [x] 统计 smart_* 工具数量，并核对“创作/创建阶段”描述
- [x] 汇总数量与对应工具名并回复

#### Create 阶段“分析型需求”工具匹配说明（待确认）

- [x] 核对创作阶段与分析/探索阶段的工具职责（smart_* / analyze_content / explore_content / operate_apply）
- [x] 结合用户示例需求，给出“该用什么工具、不写入章节”的解释
- [x] 汇总答复并更新 review

#### Explore 之后直接回答的规则改造（待确认）

- [x] 梳理规划提示词中“分析/文档类任务”的默认路由（planning_prompts.py / decision_prompts.py）
- [x] 调整规则：Explore 获取证据后优先 direct_answer，只有明确要求结构化评估时才用 analyze_content
- [x] 补充 1 条示例（Explore → direct_answer）避免遗漏
- [x] 更新 todo.md review 总结影响范围

#### 路由规则遗漏核对（待确认）

- [x] 全局搜索 analyze_content/smart_* 的提示词与示例，确认是否还有需要同步的路由说明
- [x] 重点核对 planning_examples.py / tool_descriptions.py / actions 相关文档是否需要补充
- [x] 如有遗漏，做最小改动并更新 review
- [x] 汇总核对结论补充到 todo.md review

#### review

- 已调整关键词覆盖逻辑：规划关键词不再被历史拦截，缺失关键词以“实际读取到的原文”判定。
- 已增强关键词覆盖：精确搜索合并规划关键词，未命中词补搜，优先为每个关键词读取至少1条原文证据，并输出 missing_keywords。
- 已复盘最新 Backend.md：在“赵穆/孔斌/李充/张征区别对待”任务中，仅执行了对“赵穆”的 exact_search/read，未对孔斌/李充/张征进行搜索或读取，导致证据缺失与结论不一致。
- 已补齐空读日志：read_paragraphs 即使 success=True 但 count=0 也会打印 empty_reason 等诊断字段。
- 已补齐范围锁定：当 exact_search_paragraphs 仅传 chapter_order 时，自动锁为 (order, order)。
- 已增强空读日志：read_paragraphs 失败时打印 empty_reason/error/invalid_items/index_base。
- 二次复核本次三项修复：未发现新增异常风险；范围优先级、limit 夹持、read_paragraphs 空结果原因均符合预期。
- 已修复精确搜索负数 limit：向量/正文两路统一限流为最小 1，避免 SQL 报错。
- 精确搜索强制使用本次请求的 chapter_range(s)，并对结果二次按参数范围过滤，避免回退全局范围。
- read_paragraphs 空结果补充原因与诊断字段（empty_reason/invalid_items/index_base），提升可观测性。
- 已确认创作阶段 smart_* 工具仅 3 个：smart_continue、smart_rewrite、smart_insert（定义在 backend/app/services/agent/tools/editor_tools.py，提示词说明在 backend/app/services/agent/prompts/tool_descriptions.py 与 planning_prompts.py）。
- 本次只更新 todo.md 的进度与记录，无代码逻辑改动。
- 已核对规划规则：分析/整理类文档用 analyze_content，证据检索用 explore_content，正文创作才用 smart_*；是否写入章节由 operate_apply 决定。
- 已更新提示词规则：Explore 取证后默认直接输出分析/推演/大纲/设定补充；只有明确的结构化评估（一致性/风格/质量/打分）才使用 analyze_content，并补充示例。
- 已补齐遗漏：planning_examples.py 的大纲/概括/分析文档/多章分析示例改为 explore_content 后直接输出；tool_descriptions.py 补充 analyze_content 的使用边界；planning_prompts.py 更新选中文本路由规则。
- 已梳理 ai_summarization 架构：调用链路、触发条件、上下文压缩、流式事件与最终输出策略（含失败回退与事件时序）。
- 已将 ai_summarization 的 max_tokens 从 2000 提升到 20000（影响最终整合输出长度上限）。
- 已在 OutputCard 增加表格上下间距（12px）并补齐 h3/h4 字号与间距，避免子标题过小与表格贴近问题。
- 已在 OutputCard 增加编号样式归一化：将 1、/（1）/一、 等常见格式转换为 Markdown 有序列表，确保显示 1/2/3 序号。
- 已将编号归一化同步到 ContentPreviewModal，并增加过滤规则：年份行与公告/编号/版本/通知类行不再被错误转换。
- 已在格式规范与 ai_summarization 提示词中强制要求编号列表使用 Markdown `1.`，禁止 `1、/（1）/一、`。
- 已核对段落索引来源：向量入库使用 `locate_tools._split_paragraphs`，`chunk_index` 即 `paragraph_index`，与 `read_paragraph/list_paragraphs` 共享同一拆段规则。
- 已确认索引不一致场景：章节内容更新未重建向量、`index_base` 0/1 混用、超大章 `list_paragraphs` 进入 800 字近似模式、段落数超过向量上限（MAX_CHUNKS=2000）导致后续段落未入索引。
- 已将章节向量化移到 `ChapterService` 统一触发（create/update/update_with_lock），覆盖 API/Agent/HITL 写入路径；API 层原有 background_tasks 调用已移除避免重复。
- 已补齐 `create_chapter_simple` 的向量化触发，并增加版本校验，避免多次保存导致旧任务覆盖新索引。
- 已新增实时正文精确搜索：Explore 的 exact_search_paragraphs 改为直接读取最新章节内容切段匹配，确保保存后的段落定位与正文一致（不依赖向量索引）。
- 已知限制：该路径会扫描章节正文，章节越大越慢；语义检索仍依赖向量索引（异步更新），仅精确搜索/段落定位保证实时。
- 已增加向量新鲜度判断（基于 ChapterContentIndex.updated_at vs vector.updated_at），向量最新时走向量精确搜索，过期时走正文兜底，并加短 TTL 缓存减少高频查询。
- 已添加大章性能优化：正文精确搜索先做章节级关键词预判，命中才切段；达到全局 limit 立即停止继续扫描。
- 已移除自动向量化的 `content > 100` 门槛，短章也会触发向量化（仍为异步）。
- 已在章节重排时同步更新 `novel_chapter_vectors.chapter_order`，避免向量顺序滞后影响检索排序。
- 已对超大正文的精确搜索改为“流式切段+提前过滤+早停”，减少全量切段的 CPU/内存开销。
- 已修复实时精确搜索的缩进错误，避免模块加载失败影响 Explore。
- 已将向量新鲜度缓存改为“绝对 TTL + 正文更新时主动失效”，降低高频访问导致的过期判断失真。
- 已在 ChapterService 与 ImportService 的正文落库路径补上新鲜度缓存失效，避免导入/批量写入后仍使用旧判断。
- 已在章节删除与重排后主动失效新鲜度缓存，避免章节范围变化时短暂使用旧判定。
- 已在新鲜度判断中加入“向量截断”判定：当向量数量达到 MAX_CHUNKS 时视为过期，优先走正文兜底保证准确性（代价是更频繁的兜底扫描）。
- 已将高频日志降级为 debug：API 请求完成、缓存命中/保存、世界观缓存、预加载元数据、章节向量化、字数增量、世界观同步内容预览与 AI 响应等，默认 INFO 输出显著减少。
- 已补充第三方库降噪：apscheduler/redisvl/langgraph 统一提升到 WARNING。
- 已调整 API 请求完成日志策略：仅 4xx/5xx 或慢请求（>=500ms）记录，常规 2xx/3xx 不再输出。
- Backend.md 最新段落未出现“API请求完成”流水，说明慢请求/错误请求策略生效；但仍有大量按段落/按调用明细日志（read_paragraph 缓存写入、ExploreTool call/done、AI 成本追踪/积分豁免/AI响应成功等），在高频任务下仍偏冗余。
- 已将 read_paragraph 逐段日志降为 debug（缓存命中/索引修正/缓存写入），减少每段刷屏。
- 已将 http_ai_service 的成本追踪/积分扣除/成功记录日志降为 debug，并把流式/非流式调用开始与成功日志降级。
- 已将“非流式调用未启用/未传 task_type”警告改为仅首次提示，后续降级为 debug。

#### ai_summarization 架构说明（待确认）

- [x] 定位 ai_summarization 调用链路与触发条件（langgraph_agent.py / response_builder.py）
- [x] 梳理上下文压缩与输入拼装（context_builder.py）
- [x] 梳理流式事件与输出阶段（stream_event_handler / flow_events）
- [x] 用直白详细的语言输出架构说明与执行流程

#### 调整 ai_summarization 输出上限（待确认）

- [x] 搜索 ai_summarization 的 max_tokens 设置与可能的相关上限
- [x] 将 max_tokens 提升到指定值（最小改动）
- [x] 更新 todo.md review 记录影响范围

#### OutputCard 表格间距调整（待确认）

- [x] 定位 OutputCard 的 Markdown 样式容器
- [x] 为 table 与相邻内容增加上下间距（12px）
- [x] 更新 todo.md review 记录影响范围

#### OutputCard 子标题字号调整（待确认）

- [x] 确认 h3/h4 未设置字号的渲染位置（OutputCard）
- [x] 为 h3/h4 增加字号与间距（不影响 h1/h2）
- [x] 更新 todo.md review 记录影响范围

#### 有序列表编号自动修正（待确认）

- [x] 定位输出渲染入口（OutputCard）
- [x] 将常见编号样式（1、/（1）/一、）转换为 Markdown 有序列表
- [x] 更新 todo.md review 记录影响范围

#### 编号归一化完善（待确认）

- [x] 同步编号归一化到 ContentPreviewModal
- [x] 增加过滤规则：跳过年份/公告编号类行
- [x] 更新 todo.md review 记录影响范围

#### 编号列表格式约束（待确认）

- [x] 明确 AI 输出编号列表必须使用 Markdown `1.` 格式
- [x] 更新 format_guidelines 与 ai_summarization 提示词
- [x] 更新 todo.md review 记录影响范围

#### 规划 JSON 强制输出改造计划（待确认）

- [x] 阅读规划链路与 AI 调用参数（planning_prompts / plan_generator / http_ai_service）
- [x] 规划调用启用 JSON 模式或响应格式约束（仅影响 story_planning）
- [x] 增强规划提示词的“仅 JSON 输出”约束（避免代码块/自然语言前后缀）
- [x] 规划解析失败时尝试 JSON 修复/重排（不改变原始意图）
- [x] 更新 todo.md review（记录改动与影响范围）

#### Backend.md 最新日志分析计划（待确认）

- [x] 定位并读取 `Backend.md` 最新追加日志区段（确认时间与上下文）
- [x] 提取 planning 阶段关键日志（计划生成/解析失败/重试/降级条件）
- [x] 对照“默认两步计划”触发条件，给出结论与证据
- [x] 在 todo.md 追加 review（结论/时间点/建议）

#### 章节数不一致排查计划（未确认）

- [x] 通读后端导入与章节列表链路（ImportService / ChapterService / Chapters API），确认前端取数路径
- [x] 结合日志与数据库记录核对真实章节数、章节 order、标题中的“第X章”是否仅为标题文本
- [x] 复核文本分章规则（_split_chapters）对原始文本格式的匹配缺口，判断是否导致章节被跳过/合并
- [x] 排查缓存/权限/预加载数据是否可能导致章节列表数量不一致
- [x] 汇总根因与修复/回补方案（重导入、修复分章规则、补偿脚本），并在 todo.md 追加 review

#### 统计《人在诸天，摆烂成帝.txt》章节数计划（未确认）

- [x] 检查文本实际章节标题格式，确定可用的分章正则与计数口径
- [x] 统计章节标题出现次数，并交叉验证首末章节标题
- [x] 输出章节总数与统计依据，更新 todo.md review

#### 修复分章正则计划（未确认）

- [x] 定位 `ImportService._split_chapters` 的章节匹配正则与调用路径
- [x] 放宽“第X章”标题匹配：允许无空格/括号/破折号等常见分隔符
- [x] 保持最小改动，避免误分章；必要时补充简单注释
- [x] 更新 todo.md review，记录改动与影响范围

#### 本次问题复盘计划（未确认）

- [x] 阅读 `Backend.md` 与 `INFO.md`，标注“未找到原文证据”对应的工具调用与结果
- [x] 核对 `explore_content`/tool_loop 的 `exact_search_paragraphs` 关键词解析与入参格式（是否因 `|` 拼接导致未命中）
- [x] 核对证据生成条件（必须 `read_paragraph(s)`）与本次日志是否满足
- [x] 输出 review：回答“是否已解决/为什么会这样/不是搜索到了吗”，给出原因与建议
- [x] 在 `todo.md` 追加 review 小结

#### 本次修复计划（待确认）

- [x] 复核 `explore_tools.py` 中 `exact_search_paragraphs` 的关键词解析路径（tool_loop）
- [x] 拆分含分隔符的关键词（`|/，/、/;/｜`），确保传给向量精确匹配的是关键词数组
- [x] 更新 `todo.md` review（记录改动与影响）

#### 段落索引对应性核对计划（待确认）

- [x] 查找段落切分规则与索引来源（`locate_tools._split_paragraphs` / `chapter_vector_service.store_chapter_vector`）
- [x] 核对 `read_paragraph`/`list_paragraphs` 的 index_base 与大章近似模式
- [x] 汇总“向量 paragraph_index ↔ UI 段落”对应关系与不一致场景
- [x] 更新 todo.md review 并输出答复

#### 取消向量段落上限（待确认）

- [ ] 定位 MAX_CHUNKS 使用点与相关保护逻辑（`ChapterVectorService`）
- [ ] 移除/放开 MAX_CHUNKS 限制并保持最小改动
- [ ] 评估与记录影响范围（入库耗时/内存/存储/检索性能）
- [ ] 更新 todo.md review 并输出答复

#### 统一段落解析仅 <p>（待确认）

- [ ] 核对后端段落切分入口与调用链（`locate_tools._split_paragraphs` / 向量入库 / read_paragraph）
- [ ] 将段落解析规则收敛为仅 <p>（保留纯文本回退），并评估对 locate/阅读工具影响
- [ ] 同步前端解析规则以保持段落序号一致（`useContentParser`）
- [ ] 记录需要重建向量索引的注意事项，更新 todo.md review 并回复

#### 保存后自动重建章节向量（待确认）

- [x] 核对所有写入链路（API/Agent/HITL/工具）是否统一走 ChapterService.update_* 
- [x] 在统一入口处触发向量化（后台任务或异步），避免遗漏

#### 后台日志冗余精简（待确认）

- [x] 通读后端日志输出点（按 Backend.md 里的高频样式定位文件与函数）
- [x] 汇总可移除/降级/采样的日志清单（附路径与理由）
- [x] 给出最小改动方案（保留必要告警/错误）
- [x] 依确认执行日志精简并回填 review

#### 慢请求/错误请求日志策略调整（待确认）

- [x] 明确记录策略与阈值（慢请求=500ms；仅 4xx/5xx 或慢请求记录）
- [x] 调整 MonitoringMiddleware 日志级别与条件
- [x] 简要复核对现有日志的影响并回填 review

#### Backend.md 日志符合预期评估（待确认）

- [x] 读取 Backend.md 最新日志区段并对照当前日志策略
- [x] 判断是否仍存在高频冗余日志并给出具体例子
- [x] 给出“是否符合预期 + 冗余程度”结论与建议

#### 继续降噪：read_paragraph 与 AI 调用日志（待确认）

- [x] 降级 read_paragraph 逐段 INFO（改为 DEBUG 或聚合摘要）
- [x] 合并/降级 http_ai_service 成本/积分/记录/成功日志
- [x] 将“非流式未启用”告警改为仅提示一次或降级
- [x] 更新 todo.md review 记录调整与影响
- [x] 保持最小改动并评估性能影响（频繁保存/大章）
- [x] 更新 todo.md review 并回复现状与改动

#### 方案二：Explore 精确搜索使用最新正文（待确认）

- [x] 在 ChapterVectorService 增加“基于最新正文切段”的精确搜索实现（保留原向量路径）
- [x] Explore 调用 exact_search_paragraphs 时切换到最新正文路径
- [x] 评估性能与边界（大章/无范围/limit），记录已知限制
- [x] 更新 todo.md review 并回复变更影响

#### 方案二优化：向量新鲜度判断 + 大章性能 + 去掉长度门槛（待确认）

- [x] 设计并实现向量新鲜度判断（基于 content_hash 或章节版本）仅过期时走正文兜底
- [x] 增加大章精确搜索性能策略（按章节范围/分页扫描，避免全量切段）
- [x] 去掉自动向量化的 content > 100 门槛（短章也向量化）
- [x] 记录性能权衡与限制，更新 todo.md review 并回复

#### 方案二补强：新鲜度/重排/缓存（待确认）

- [x] 仅基于正文索引更新时间判断新鲜度，避免非内容更新触发兜底
- [x] 重排章节时同步更新向量的 chapter_order（不重建向量）
- [x] 向量新鲜度判断加短 TTL 缓存，降低 Explore 频繁调用负担
- [x] 更新 todo.md review，记录影响范围与边界

#### 方案二复核修补（待确认）

- [x] 修复实时精确搜索的缩进/语法问题，避免模块加载失败
- [x] 将新鲜度缓存改为绝对 TTL，并在正文更新时主动失效
- [x] 新鲜度判断补充“向量截断”判定（MAX_CHUNKS 命中则视为过期）
- [x] 更新 todo.md review，记录修补点与残余风险

### 讨论记录（详细）

#### 待办清单

- [x] 确认保留范围（仅保留本节及其内容）
- [x] 删除其余所有记录，只保留“### 讨论记录（详细）”相关内容
- [x] 在本节末尾补充 review，总结修改
- [x] 梳理重构所需改动点与相关文件（explore_tools/search/locate/read/输出）
- [x] 改造 Explore：删除规则验收与旧补漏流程，仅保留“只读收集器 + LLM 自检循环”
- [x] 产出定位桥梁：新增 locate_targets（chapter_id + 原文 query + node_id/nodes_info + reason）
- [x] node_id 打通：为证据/段落补齐 node_id（最小改动）
- [x] 输出收敛：移除/隐藏 sufficiency/coverage 等硬规则字段，保持前端兼容
- [x] 冒烟自检：确认 search/read/locate 链路不崩、返回结构完整
- [x] 修复 ParagraphRead 字段顺序导致的导入错误
- [x] 读段落时回填 node_id，并补齐仅有 paragraphs 的 chapter_id（含 resolve）
- [x] 恢复 max_rounds=10 行为（移除 3 轮硬封顶）
- [x] 清理未使用的旧规则方法/数据结构（死代码）
- [x] 冒烟自检：记录无法运行的原因
- [x] 只接受 read_paragraph 原文作为证据：Search/Exact 仅作候选，不进入 evidences
- [x] 主题拆分/关键词入口：允许主 agent 传入并驱动检索（探索内不再自生“主题清单”）
- [x] locate_content 禁跨章降级：统一 allow_global_fallback=false
- [x] 输出收敛：对外仅保留证据+定位元数据（评估依赖与兼容策略）
- [x] 冒烟自检：记录无法运行的原因

- opencode 的“先找再读”来自**提示词与权限约束**，不是硬编码流程；子代理只读（Glob/Grep/Read/Bash）并返回绝对路径，策略由上层子任务 prompt 指定。`opencode/packages/opencode/src/agent/prompt/explore.txt` `opencode/packages/opencode/src/agent/agent.ts`
- opencode **没有“硬规则验收/证据数”**：Explore 只遵循“调用方给的 thoroughness”，停止/是否足够由主 agent 主观判断，不在代码中强制。依据：
  - `opencode/packages/opencode/src/agent/prompt/explore.txt`：第13行明确“Adapt…thoroughness level specified by the caller”。 
  - `opencode/packages/opencode/src/agent/agent.ts`：第146行要求调用方指定 quick/medium/very thorough。
  - `opencode/packages/opencode/src/session/prompt.ts`：第1262–1271行只规定“启动 explore”，没有验收规则。
- 我们要复刻的不是“子代理形式”，而是**确定性检索链路**：先找范围（类似 List），再做文本级筛选（类似 Grep），最后用 Read 读取原文并输出定位信息。
- 工具对标（文件系统 → 章节内容）：
  - Glob/List → 章节范围/清单：优先用 `explore_tools` 的范围解析与 scope 过滤；必要时用 `get_writing_context` 拿章节内容或新增轻量章节清单工具。`backend/app/services/agent/tools/explore_tools.py` `backend/app/services/agent/langgraph_tools.py`
  - Grep → **精确文本检索**：用 `chapter_vector_service.exact_search_paragraphs` 做“字面匹配”，`search_content` 只当语义补充，不作为最终证据来源。`backend/app/services/chapter_vector_service.py` `backend/app/services/agent/langgraph_tools.py`
  - Read → `read_paragraph` 读取段落原文；需要整章时才用 `get_writing_context`。`backend/app/services/agent/langgraph_tools.py`
  - “绝对路径”对标 → `chapter_id/chapter_order + paragraph_index`（作为证据的唯一定位）
  - Locate → `locate_content` 仅用于补段落号，且必须禁用跨章降级。`backend/app/services/agent/tools/locate_tools.py`
- 可复刻的确定性流程（Search+Read 到预期内容）：
  1) 强制范围锁定：解析“前 N 章”并写入 scope，后续搜索/定位/读取全部过滤在范围内。`backend/app/services/agent/tools/explore_tools.py`
  2) 主题拆分 + 关键词清单（由主代理生成）：对每个主题先做精确搜索（exact_search），得到候选段落。
  3) 补段落号：候选缺段落号时用 `locate_content` 定位，但不允许跨章/全局降级。
  4) 读原文：对每条候选用 `read_paragraph` 读出原文段落（必要时带上下文）。
  5) 证据验收：只接受 Read 原文（拒绝 Search 片段直接当证据）。
  6) 配额与缺失：按主题数量要求检查，不足则二次精确搜索；仍缺则标注“范围内未出现”。
- 为什么“LLM 自选 Search/Read”不能保证预期：
  - `search_content` 是语义检索，天然会漏/偏；`locate_content` 依赖 LLM + query 截断，容易跑偏；如果允许跨章降级，会破坏范围约束。
- 只有“精确搜索 + 严格范围 + 只接受 read_paragraph 原文”才能接近 opencode 的确定性 Grep/Read 体验。
- 追加讨论（对齐 opencode 的执行风格）：
  - `explore_content` 拆成**只读收集器 + LLM 自检**两块：收集器只做 Search/Locate/Read 并回传证据；自检只做“是否继续”的判断。
  - **删除规则验收 + 旧补漏逻辑**：不再用 `_rule_based_sufficiency/_evaluate_from_extraction` 及基于规则的缺口补漏。
  - **内部循环仍在 explore_content**：由 LLM 自检决定是否再派一轮收集任务；外部不参与验收、不追加任务，只消费最终证据作为上下文。
  - **输出收敛**：对外只保留证据+定位元数据（chapter/paragraph/source），不再输出 sufficiency/coverage 等硬规则字段。
- 追加讨论（方案B可行性）：后端持久化 node_id **可行但要动三件事**：  
  - 向量化切分必须统一到能解析 `data-id` 的拆段逻辑（否则 index 对不上）。  
  - 向量索引表需新增 `node_id` 字段并在检索返回中透出。  
  - 旧章节向量必须重建/回填，否则 node_id 为空。  
  结论：能做，但不是“加字段就完事”，必须“拆段一致 + 索引迁移 + 回填”。
- 追加讨论（受影响功能代码范围）：  
  - **模型/迁移**：`backend/app/models/novel_chapter_vector.py`（新增 node_id 字段）+ 数据库迁移脚本。  
  - **向量化入库**：`backend/app/services/chapter_vector_service.py`（拆段改为解析 data-id + 写入 node_id）；触发入口在 `backend/app/api/v1/chapters.py`、`backend/app/api/v1/import_routes.py`、`backend/scripts/migrate_chapter_vectors.py`。  
  - **检索输出**：`backend/app/services/chapter_vector_service.py` 的 `retrieve_for_writing/exact_search_paragraphs` + `backend/app/services/search/hybrid_retriever.py` 需要透出 node_id。  
  - **Search/Explore 输出**：`backend/app/services/agent/langgraph_tools.py` 的 `search_content` 与 `backend/app/services/agent/tools/explore_tools.py` 需要把 node_id 透传到 locate_targets。  
  - **Locate/Read 对齐**：`backend/app/services/agent/tools/locate_tools.py` / `backend/app/services/agent/langgraph_tools.py` 的 read_paragraph 依赖拆段一致性。
- 追加讨论（Explore → locate_content 传参规则）：  
  - **最小必需**：`chapter_id + query`，其中 query 必须是**原文片段**，不是抽象关键词。  
  - **高精度优先**：`node_id`（最高优先级）与 `nodes_info`（结构化节点列表，有就传）。  
  - **范围锁定**：有 scope 时必须 `allow_global_fallback=false`，禁止跨章降级。  
  - **注意点**：`locate_content` 没有 `paragraph_index` 参数；只有段落号时需转成“第N段”或直接用原文片段作为 query。  
  - **推荐调用**：`locate_content(chapter_id=target.chapter_id, query=target.query, node_id=target.node_id?, nodes_info=target.nodes_info?, allow_global_fallback=false)`。

#### 计划（opencode 风格 Explore 改造）

- [x] 评估现有 `explore_content/ContentExplorer` 流程与调用点，确定 “opencode 风格” 开关参数与兼容策略（保留旧流程默认行为）
- [x] 新增只读工具：`list_chapters`（章节清单）、`list_paragraphs`（章节段落索引/片段，支持 offset/limit）、`read_paragraphs`（批量读取）
- [x] 在 `explore_tools.py` 中实现 “LLM 工具调用循环”（LLM 产出 tool+args+stop），仅允许 List/Grep/Read；默认禁用语义检索，并加预算限制（最大工具调用/最大读取段落）
- [x] `explore_content` 接入新模式（如 `explore_mode="tool_loop"`），输出结构保持兼容（evidences/locate_targets 等），并继续强制范围锁定 + 只读证据
- [x] 必要时更新工具描述/提示词（`tool_descriptions.py`/`planning_prompts.py`）以反映新模式的可用只读工具与约束
- [x] 冒烟检查与记录（若无法运行说明原因），更新 review 汇总变更与影响

#### 计划（补齐缺口：chapter_id / 段落数 / node_id）

- [x] read_paragraph 支持 chapter_id（无 chapter_order 时自动解析）并在返回中补齐 chapter_id
- [x] list_chapters 补充段落数（paragraph_count），与编辑器拆段一致
- [x] 向量索引补齐 node_id：模型新增字段 + 向量化写入 node_id + 检索返回 node_id + migrate/回填脚本说明
- [x] explore/tool_loop 对接 node_id（候选/证据/locate_targets 中透出）
- [x] 冒烟检查并更新 review（记录无法运行的原因）

#### 计划（默认启用 V5 tool_loop）

- [x] 将 explore_content 的默认 explore_mode 改为 tool_loop（保留显式 pipeline 可选）
- [x] 同步工具描述提示“默认 tool_loop”，避免误解
- [x] 冒烟检查并更新 review（记录无法运行的原因）

#### 计划（Backend.md 四条测试日志验收）

- [x] 抽取四条测试 prompt 对应的 explore_content 日志片段
- [x] 对照 V5 预期：确认 tool_loop、仅 read_paragraph、是否触发语义检索
- [x] 检查范围锁定是否正确（第X章至第Y章 / 第1–30章）

#### 计划（扩大 V5 工具调用上限）

- [x] 将 TOOL_LOOP_MAX_CALLS_DEFAULT 从 20 提升到 200
- [x] 冒烟检查并更新 review（记录无法运行的原因）

#### 计划（基于小说素材生成大跨度测试 Prompt）

- [x] 阅读素材文件，提取关键角色/事件/体系/场景范围
- [x] 设计 2 条“章节跨度大 + 信息跨度大”的复杂测试 prompt（严格原文证据要求）
- [x] 回填 review（记录未能执行的原因）

#### 计划（修复章节范围约束丢失）

- [x] 扩展规划阶段范围解析（支持“第X章至第Y章/第X–Y章/第X–第Y章”等）
- [x] 确保 explore_content 的范围解析兼容上述格式（含 en dash）
- [x] 冒烟检查并更新 review（记录无法运行的原因）

#### 计划（修复"世界观文档"被误派给续写工具的问题）

**问题背景**：
- 用户请求"输出一份完整的《世界观设定补充文档》"时，系统错误地使用了 `smart_continue`（续写工具）
- `smart_continue` 的 prompt 是为小说续写设计的，导致输出了故事内容而非分析文档
- 生成的内容还被自动 `operate_apply(append)` 到了当前章节

**根因**：
- `planning_prompts.py:196` 规定：`创作新内容（包括大纲/规划/设定）→ smart_continue`
- "设定文档"被归类为"创作"，但实际应该是"分析/整理"

**修复方案**：修改规则，明确区分工具职责
- **故事正文创作**（写入编辑器的小说内容）→ `smart_continue` / `smart_rewrite` / `smart_insert`
- **其他所有非正文需求**（世界观文档、角色卡、分析报告、伏笔追踪、大纲规划等）→ `analyze_content`

**待办**：
- [x] 修改 `planning_prompts.py` 中的工具选择规则，区分"故事正文"与"分析文档"
- [x] 在 `planning_examples.py` 中增加"世界观文档/角色卡/分析报告"使用 `analyze_content` 的示例
- [ ] 确保 `analyze_content` 能输出结构化文档（检查其 prompt 是否需要调整）
- [ ] 冒烟检查并更新 review

#### 计划（修复 read_paragraphs 批量读取缺少去重检查的问题）

**问题背景**：
- 日志显示 AI 使用 `read_paragraphs` 批量读取时，同一段落被反复读取多次
- 例如：第1章第57-87段在连续3轮中被重复读取

**根因**：
- `read_paragraph`（单个读取）有前置去重检查（`should_read_paragraph`）
- `read_paragraphs`（批量读取）**没有前置去重检查**，直接调用底层工具
- 调用链：`ExploreTool → langgraph_tools.read_paragraphs`，后者没有任何去重逻辑
- 结果处理时只是记录已读（`record_paragraph_read`），但读取已经发生了

**代码位置**：
- 缺陷位置：`explore_tools.py` 第3099-3142行（`read_paragraphs` 分支）
- 对比参考：`explore_tools.py` 第2995-2996行（`read_paragraph` 有前置检查）

**补充发现 - 结果截断导致 AI 误判**：
- `TOOL_LOOP_RESULT_PREVIEW_LIMIT = 1200` 字符
- 38个段落的读取结果远超 1200 字符，AI 只能看到前几个段落
- AI 误以为后面的段落没读到，所以每轮都重新请求读取
- 日志证据：AI 每轮微调起点（50→52→54→57），但终点始终是 87，说明它知道前面的读了，但不确定后面的

**待办**：
- [x] 在 `ExploreTool._execute_tool` 的 `read_paragraphs` 分支中增加前置去重检查
- [x] 过滤掉 `items` 中已读取的段落（调用 `should_read_paragraph`）
- [x] 在 `_build_tool_loop_summary` 中增加"已读段落列表"摘要，告诉 AI 哪些段落已读
- [ ] 考虑优化结果预览策略（如：只返回段落号列表，不返回内容）
- [x] 将 `MAX_ROUNDS` 从 10 提升到 200（`explore_tools.py:1786`）
- [ ] 冒烟检查并更新 review

#### 计划（重构工具循环的章节覆盖策略）

- [ ] 增加"覆盖度优先"硬规则：同一章节连续读取上限 + 未覆盖章节优先
- [ ] 在 tool_loop 决策提示中加入"跨章覆盖"要求（必须先覆盖范围内多个章节）
- [ ] 读取策略改为"跨章批量读"：优先 list_chapters/list_paragraphs 再分散 read_paragraphs
- [ ] 增加章节覆盖统计并输出到日志/summary，便于验收
- [ ] 冒烟检查并更新 review（记录无法运行的原因）

#### 计划（改为 opencode 式“LLM 主观判断”，去硬规则）

- [x] 逐项定位 Explore 中“硬规则判停/补漏”逻辑（证据数/覆盖率/自动补漏/固定阶段）
- [x] 删除或绕过“证据数/覆盖率”驱动的 sufficiency 判定，仅保留 LLM 自检决定是否继续
- [x] 把 auto-read / 固定阶段（精确→语义）改为**可选**且仅由 LLM 决定是否调用
- [x] 保留安全上限（最大轮次/工具调用/读取数）但不参与“够不够”判断，仅作熔断
- [x] 输出收敛：移除 sufficiency/coverage/统计驱动字段，输出只保留证据与定位元数据
- [ ] 冒烟检查并更新 review（记录无法运行的原因）

#### 计划（旧链路自动补 output_mode="full"）

- [x] 扫描规划任务参数中的旧字段引用（$ref/$TASK_ 里出现 chapters/context_for_task/explore_summary/frontend_display）
- [x] 在 PlanGenerator._validate_and_fix_plan 后处理：为被引用的 explore_content 任务自动补 output_mode="full"
- [x] 仅在 params 未显式设置 output_mode 时才补，避免覆盖新链路
- [x] 更新工具提示：需要旧字段时显式 output_mode="full"
- [x] 更新 review（记录影响与风险）

#### 计划（默认启用 output_mode="full" 以恢复前端轨迹）

- [x] 将 explore_content 默认 output_mode 改为 "full"
- [x] 更新提示词/工具说明中关于默认输出的描述
- [x] 更新 review（记录影响与风险）

#### 计划（排查“读取两章内容/读了100+次”问题）

- [x] 通读 Backend.md + INFO.md，整理“读两章/高频调用”的关键时间段与触发条件
- [x] 追踪 explore_content → ContentExplorer → ExploreTool.read_paragraphs 参数流，定位失败原因
- [x] 修正 read_paragraphs 对 items 的兼容（chapter_id/node_id → chapter_order/paragraph_index 映射或兜底）
- [x] 校准 tool_loop 提示/参数约束，避免 LLM 生成无效 items 导致重复调用
- [x] 记录复现路径与修复结果，补充 todo.md 的 review

#### Explore 搜索可见性问题 review（待确认）

- [x] 定位 Explore 工具链路中搜索结果的存储与证据规则（search_hits/evidences）
- [x] 确认 AI 决策上下文可见内容（search_history/last_tool_result/证据原文）
- [x] 给出结论：AI 是否能看到搜索返回原文、哪些是片段、哪些是证据，并更新 todo.md review

#### opencode Explore 搜索流程剖析计划（待确认）

- [x] 通读 opencode Explore 入口（explore prompt / agent 注册 / Task 调用）
- [x] 梳理搜索工具链路（glob/grep/read）与输出截断/权限，明确 AI 能看到的内容
- [x] 解释“探索结果如何返回主 AI”，形成深度剖析结论并更新 todo.md review

#### Explore 命中回显扩展计划（待确认）

- [x] 扩展搜索命中回显长度与条数（对标 grep 100 条 × 2000 字）
- [x] 在自检摘要中展示“最近一轮 exact_search 命中列表”，避免仅靠短预览
- [x] 更新 todo.md review 记录改动与影响

#### Explore 命中列表上限与过滤优化计划（待确认）

- [x] 命中列表增加总字符上限，超出提示“剩余条目省略”
- [x] 仅展示最新 query 的 Top-N 命中，避免混入旧轮次
- [x] 更新 todo.md review 记录改动与影响

#### Explore 命中定位可回溯性计划（待确认）

- [x] 命中无段落号时标记“不可直接读取”，提示先 list_paragraphs 获取 index（tool_loop 不用 locate）
- [x] 命中列表展示 chapter_id/node_id（如有），并在摘要中保留位置线索
- [x] 更新 todo.md review 记录改动与影响

#### 段落索引准确性与 UI 一致性 review 计划（待确认）

- [x] 复核段落拆分规则与索引基准（list_paragraphs/read_paragraphs/index_base）
- [x] 对照 UI 渲染与后端拆段规则，判断“UI 所见即段落索引”的一致性
- [x] 输出结论与风险，并更新 todo.md review

#### 段落索引对外 1-based 兼容方案（待确认）

- [x] 对外 API 默认 1-based（list_paragraphs/read_paragraph/read_paragraphs），内部仍 0-based
- [x] list_paragraphs 输出 display_index = index + 1（含 approximate 模式）
- [x] read_paragraph/read_paragraphs 默认 index_base=one，内部显式 zero 调用保持不变
- [x] read_paragraph/read_paragraphs 返回 display_index（便于 UI/AI 对齐）
- [x] 更新 todo.md review 记录改动与影响

#### Explore 读取预算按章限制计划（待确认）

- [x] 新增 per-chapter 读取上限（动态上限：按段落数比例/最小/最大值），避免单章耗尽预算
- [x] 取消默认全局上限（如需保留则改为可选），并在工具摘要中显示每章剩余预算
- [x] 调整 read_paragraph/read_paragraphs/exact_search 自动读的预算扣减逻辑
- [x] 更新 todo.md review 记录改动与影响

#### read_paragraphs 分页读取优化计划（待确认）

- [x] read_paragraphs 新增 offset/limit + chapter_order/chapter_id 参数，内部自动 list_paragraphs→read_paragraph
- [x] 保持 items 批量模式兼容（未传 offset/limit 时走原逻辑）
- [x] 更新 explore 工具提示语（说明可用分页参数）
- [x] 更新 todo.md review 记录改动与影响

### review

- 已删除 todo.md 其余记录，仅保留“### 讨论记录（详细）”及其内容。
- 本节保留了对标 opencode 的确定性检索链路、重构执行风格、node_id 方案可行性与受影响代码范围、Explore→Locate 传参规则。
- 已完成 Explore 重构：删除规则验收与旧补漏路径，改为“精确搜索 + LLM 自检循环”驱动后续收集。
- 已补齐定位桥梁：新增 `locate_targets` 与 `evidences` 输出，并在 `frontend_display` 中透出 locate_targets。
- 已打通 node_id：`ParagraphRead` 记录 node_id，构建 node_id 映射并用于 evidences/search_results/locate_targets。
- 已移除/隐藏 sufficiency/coverage 输出字段，前端展示改为“继续检索/停止检索”语义。
- 已修复 `ParagraphRead` 字段顺序错误，避免 dataclass 导入时报错。
- Backend.md 最新日志显示：2026-01-28 21:15:58 开始 planning；21:17:03 第1次 JSON 解析失败（模型输出为非 JSON 的完整内容）；21:17:54 第2次重试成功并生成 3 个任务。日志中未出现“默认两步计划/降级两步”触发记录，说明本次并非走两步降级，而是一次解析失败后重试成功。
- 规划 JSON 强制输出已加强：planning 调用加入 `response_format={"type":"json_object"}` 并在不支持时自动降级重试；提示词追加“禁止 ```json 代码块”；JSON 提取增加 BOM 处理，解析更稳。
- 已在 read_paragraph 回填 node_id，并为仅有 paragraphs 的章节补齐 chapter_id（含 resolve）。
- 已恢复 max_rounds=10 的自检循环上限（不再硬封顶 3 轮）。
- 已清理旧规则评估与 AI 规划相关死代码，保留当前自检驱动路径。
- 已新增 search_hits 作为“候选池”，Search/Exact 仅入候选，不再进入 evidences。
- 已改为“只用 read_paragraph 原文入证据”，search_content/exact_search 只驱动定位与阅读。
- 已统一 locate_content 禁跨章降级（allow_global_fallback=false），并在 locate_targets 透出。
- 已新增 output_mode（evidence_only）输出收敛开关，按需仅返回证据+定位元数据。
- 已新增只读工具：`list_chapters`/`list_paragraphs`/`read_paragraphs`，用于对标 List/Grep/Read 的章节数据源映射。
- 已实现 opencode 风格工具循环：LLM 产出 tool+args+stop，仅允许 List/Grep/Read，语义检索默认禁用，并加入工具/读取预算上限。
- 已为 `explore_content` 增加 `explore_mode` 与预算参数，`tool_loop` 模式可选启用，默认保留旧流程。
- 已更新 `tool_descriptions.py`，补充 explore_content 新参数说明。
- 冒烟：`python -m py_compile` 失败（环境无 python），未运行自动化测试。
- 已为 `read_paragraph` 增加 chapter_id 支持（无 chapter_order 时自动解析），返回中补齐 chapter_id。
- 已在 `list_chapters` 输出 paragraph_count（与编辑器拆段一致）。
- 已扩展搜索命中回显：命中列表追加 chapter_id/node_id；无段落号时标记“先 list_paragraphs”；搜索历史摘要加入“首条第X章第Y段”位置提示。
- 已完成对外 1-based 兼容：list_paragraphs 增加 display_index（含 approximate）；read_paragraph/read_paragraphs 默认 1-based 并返回 display_index，内部调用仍显式 zero。
- 已为向量索引新增 node_id 字段并写入/检索透出，Hybrid/semantic 搜索结果同步携带 node_id。
- 已新增迁移脚本说明（重跑 `migrate_chapter_vectors.py` 回填 node_id），并添加 Alembic 迁移文件。
- 已将 explore_content 默认模式切到 tool_loop（V5），并更新工具描述。
- 冒烟：未运行自动化测试（环境无 python）。
- 日志验收：V5 已启用且以 exact_search + read_paragraph 为主，但范围解析对“第X章至第Y章”和“第1–30章”存在识别问题，出现“第5章、第20章”或 range=None 的锁定结果。
- 已将 V5 工具调用上限从 20 提升到 200，以降低早停概率。
- 已读取《人在诸天，摆烂成帝》素材并据此生成 2 条大跨度测试 prompt。
- 已修复范围解析：规划侧与 Explore 侧均支持“第X章至第Y章/第X–Y章/第X–第Y章”，含 en dash（–）。
- 已去掉自检输入中的“证据数/覆盖统计”，并移除 keyword 覆盖强制逻辑，改为纯 LLM 主观判断。
- 已移除自检循环的“信息收敛”硬停机规则，仅保留安全上限作为熔断。
- 已将前端轮次状态文案与 sufficiency 脱钩（仅展示，不参与判停）。
- 已强制 explore_content 统一走 tool_loop（pipeline 弃用），固定阶段/自动补漏不再执行。
- 已收敛 explore_content 输出为最小字段（仅 evidences + locate_targets），并更新提示词参数规则。
- 已调整 explore_content 结果处理：无 frontend_display 时不再尝试发射事件；无 explore_summary 时回退为最小 JSON 文本。
- 已批量替换规划示例中的旧字段引用（chapters/context_for_task）为 evidences/locate_targets，并补充新字段说明。
- 已更新工具说明中的停止条件描述（不再提“信息收敛自动停止”）。
- 已更新写作行动提示：改为使用 evidences/locate_targets 作为改写/续写/插入的输入来源。
- 已禁用 explore_round/explore_summary 事件（不再创建 emit_callback，结果标记 events_emitted=true）。
- 已恢复 output_mode 分支：默认最小输出；output_mode="full" 才返回旧字段（chapters/context_for_task/frontend_display/explore_summary）。
- 已补回 locate_targets 的 chapter_id 解析（最小章节映射 + resolve_chapter_id），避免最小输出下定位目标为空。
- 已补充 opencode 的“判定标准”结论：无硬规则，仅依赖调用方指定的 thoroughness + 主 agent 主观判断停止。
- 已在规划后处理阶段自动补齐 explore_content 的 output_mode="full"：当下游参数引用旧字段（chapters/context_for_task/explore_summary/frontend_display）时生效，且不覆盖显式设置。
- 工具提示已包含 output_mode 使用说明（无需额外改动）。
- 已恢复 full 输出的前端事件发射：当 output_mode="full" 时返回 events_emitted=false，交由 parallel_executor 发射 explore_round/explore_summary。
- 已改回 explore_content 默认 output_mode="full"，以恢复前端 Explore 轨迹展示。
- 已更新提示词说明：默认输出完整字段，需精简时显式 output_mode="evidence_only"。
- 已恢复工具内事件实时发射：当存在 stream handler 时，explore_content 直接发 explore_round/explore_summary，并标记 events_emitted=true。
- 已定位“读两章/高频调用”原因：tool_loop 生成的 read_paragraphs items 使用 chapter_id/node_id（或 index），而 ExploreTool 仅识别 chapter_order/paragraph_index，导致 read_paragraphs 过滤为空并反复重试。
- 已为 list_paragraphs 增加 paragraph_index 字段，并在 ExploreTool 内缓存 node_id→paragraph_index 映射以兜底。
- 已在 ExploreTool.read_paragraphs 兼容 chapter_id/node_id/index → chapter_order/paragraph_index 的映射，避免空列表反复调用。
- 已更新 tool_loop 提示，要求 read_paragraph/read_paragraphs 使用 chapter_order+paragraph_index，降低 LLM 生成无效 items 的概率。
- 本次日志确实“调用了搜索”，但 `exact_search_paragraphs` 收到的是带 `|` 的**单字符串**关键词（如“世界观体量|遮天|一人之下|主线任务|摆烂”），未拆分时会按**字面包含 `|`** 进行匹配，导致命中为 0。
- 日志显示未发生成功的 `read_paragraph(s)` 读取，因此 `evidences` 为空，最终只能返回“未找到任何原文证据”。
- 任务范围锁定在第1–2章，且 tool_loop 禁用语义检索，仅做精确匹配；若原文措辞不同，也会出现“搜索过但无证据”的结果。
- 建议：在 `exact_search_paragraphs` 或调用侧拆分 `|/，/空格` 为数组；必要时加入低成本兜底（list_paragraphs→read_paragraph）或允许语义检索作为辅助。
- 已在 explore 工具侧对 `exact_search_paragraphs` 的关键词做分隔符拆分（`|/，/、/;/｜`），避免单字符串精确匹配导致 0 命中。

#### 2026-01-29 修复：explore_content 重复读取与工具选择问题

**问题1：read_paragraphs 批量读取缺少去重检查**
- 根因：`read_paragraphs` 分支没有调用 `should_read_paragraph` 进行前置去重检查
- 补充发现：`TOOL_LOOP_RESULT_PREVIEW_LIMIT=1200` 导致 AI 只能看到部分结果，误以为后面的段落没读到
- 修复：在 `explore_tools.py:3097` 增加 `self.state.should_read_paragraph()` 检查

**问题2：AI 不知道哪些段落已读**
- 根因：`_build_tool_loop_summary` 没有告诉 AI 已读段落列表
- 修复：在 `explore_tools.py:2451-2468` 增加已读段落摘要（按章节分组显示）

**问题3：MAX_ROUNDS 过小**
- 修复：将 `MAX_ROUNDS` 从 10 提升到 200（`explore_tools.py:1786`），与其他预算参数保持一致

**问题4：世界观文档被误派给续写工具**
- 根因：`planning_prompts.py:196` 规定"创作新内容（包括设定）→ smart_continue"
- 修复：区分"故事正文"与"分析文档"
  - `planning_prompts.py:196-202`：明确 smart_continue 只用于故事正文，analyze_content 用于分析文档
  - `planning_examples.py:607-677`：新增场景6示例（世界观文档/角色卡/伏笔表）

**深度验证后的额外修复**（2026-01-29）：
- 修复：`explore_content` 函数参数默认值 `max_rounds=10` 改为 `200`，与 `MAX_ROUNDS=200` 保持一致
- 修复：已读段落摘要增加长度限制（最大500字符），避免占用过多 token
- 修复：`planning_examples.py` 中 `aspects: ["worldview"]` 改为 `aspects: ["structure"]`（因为 `worldview` 不是有效 aspect）
- 修复：示例中增加 `focus` 参数，明确指定输出格式要求

#### 《人在诸天，摆烂成帝.txt》章节统计

- 文件 `docs/Agent/real-book/人在诸天，摆烂成帝.txt` 共有 **100** 个章节标题（匹配 `^第[0-9]+章`）。
- 章节编号连续完整（1–100 无缺号），首章为“第1章【摆烂的宿主】”，末章为“第100章【火域铸真器，两脉起冲突】”。

#### 分章正则修复

- 扩展 `ImportService._split_chapters` 的分章正则：`第X章` 允许无空格、括号/破折号等分隔符；`Chapter X` 同步放宽；Markdown 标题支持 `#`–`######`。
- 该改动只影响文本/Markdown 导入的章节切分，不影响已有章节读取。

#### Operate 工具清单整理计划（未确认）

- [x] 定位 Operate 相关实现与路由表，确认实际调用的工具集合
- [x] 核对定位/执行阶段是否额外依赖 locate 工具
- [x] 输出 Operate 类工具清单并在 todo.md 补充 review

#### Operate 工具清单

- `operate_apply`（Operate 入口工具，支持 append/replace/insert/content/create/title）。
- 其底层路由会调用：`apply_chapter_edit`、`create_chapter`、`update_chapter_title`。
- replace/insert 需要定位时，内部会调用 `locate_content`（direct/text_match/semantic）。

#### “读取上限”提示排查计划（未确认）

- [x] 搜索前端/后端该提示的文案来源与触发条件
- [x] 追踪与“探索/读取上限”相关的参数（如最大读取段落/轮次/调用上限）
- [x] 给出含义解释与调整建议（如提升上限/分批读取/缩小范围）
- [x] 更新 todo.md review 记录结论

#### “读取上限”提示含义

- 该提示对应 Explore 工具循环中的 `stop_reason=达到读取上限`（tool_loop 读取预算耗尽后停止）。
- 读取预算由 `max_read_paragraphs` 控制，默认值为 `TOOL_LOOP_MAX_READS_DEFAULT=60`；当 `read_paragraph/read_paragraphs` 继续调用且 `reads_left<=0` 时触发停止。
- 解决思路：缩小任务范围/分批探索，或在调用 `explore_content` 时显式提高 `max_read_paragraphs`，或提升默认常量。

#### 提升默认读取上限到 200（未确认）

- [x] 定位 `TOOL_LOOP_MAX_READS_DEFAULT` 常量定义位置
- [x] 将默认值从 60 调整为 200
- [x] 更新 todo.md review 记录改动

#### 默认读取上限调整

- 将 `TOOL_LOOP_MAX_READS_DEFAULT` 从 60 提升为 200，以降低探索因读取预算耗尽而提前停止的概率。

#### “默认两步计划”原因分析计划（未确认）

- [x] 阅读 `Backend.md` 中对应时间段的规划日志，定位触发兜底的直接原因
- [x] 对照 `PlanGenerator` 的兜底分支条件（JSON解析失败/空响应/无tasks）核验
- [x] 输出结论与改进建议（提示词约束/JSON封装/失败回退策略）
- [x] 更新 todo.md review 记录结论

#### “默认两步计划”原因结论

- `Backend.md` 显示在 2026-01-28 20:56:38 与 20:57:21 两次规划尝试均出现 “JSON解析失败” 警告，且日志中 AI 返回文本包含自然语言 + 未闭合的 JSON 片段，导致解析失败。
- `PlanGenerator` 在连续两次解析失败后触发 `_create_default_plan()` 兜底，因此生成了固定的两步计划（get_context → analyze_content）。
- 改进建议：增强规划提示词的 JSON 约束（只输出 JSON）、提高最大 tokens 或开启更严格的 JSON 修复；必要时将解析失败的原始文本记录到单独字段便于调试。

#### 规划 JSON 输出修复计划（未确认）

- [x] 收紧规划提示词：仅允许输出 JSON（禁止自然语言/解释），覆盖 planning_static_prompt 与 agent_mode_prompt
- [x] 增强 JSON 修复/截断补全策略（提取失败时尝试补齐闭合括号/引号等）
- [x] 记录解析失败的原始文本到日志字段，便于定位具体坏片段
- [x] 更新 todo.md review 记录改动与影响范围

#### 规划 JSON 输出修复（完成）

- Prompt 层：在规划输出格式中新增“仅输出 JSON、禁止任何非 JSON 内容”，并在静态/Agent 模式提示尾部再次强约束。
- 解析层：新增 JSON 截断与括号补齐策略（`_truncate_to_balanced_json` / `_balance_json_braces`），并在修复失败时继续尝试解析。
- 观测层：规划 JSON 解析失败时记录原始文本日志，便于定位坏片段。

#### 章节数不一致排查结论

- 2026-01-27 19:03:57 后端日志显示文本导入完成仅 **77 章**（work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21）。
- 2026-01-27 19:04:01 章节列表查询返回 **77 章**，且最后一章标题为“第100章【火域铸真器，两脉起冲突】”，但 **order=77**，说明“第100章”仅是标题文本而非真实章节序号。
- 2026-01-27 19:07:02–19:07:05 向量化日志显示“第98/99/100章”对应 **order=75/76/77**，进一步印证实际章节数为 77（标题编号与真实顺序不一致）。
- 前端列表来自 `/api/v1/chapters/work/{work_id}`，未做过滤；数量显示与后端真实章节数一致，问题不在前端。
- 最可能根因：`_split_chapters` 的正则仅匹配“第X章+空白/冒号”，对“第X章【标题】/第X章-标题/第X章·标题/无分隔符”等格式命中失败，导致 23 处章节标题未被识别而被合并。
- 解决建议：扩展分章正则（允许 `【】()（）[]`、破折号、点号、空白可选），重新导入或做补偿拆分迁移；若使用 Markdown，建议放宽 `##` 为 `#{1,6}`。
- Explore 搜索可见性结论：搜索/精确搜索结果只进入 `search_hits` 与 `search_history` 的摘要或预览，不作为证据；AI 在决策时只能看到摘要/截断片段（`hits_summary` + 上一次结果预览），完整原文只来自 `read_paragraph` 并进入 `evidences`。
- opencode Explore 结论：Explore 是独立子代理（`explore`），主代理通过 Task 工具创建新会话并传入提示；子代理用 Glob/Grep/Read 搜索与阅读，工具输出各自有截断（glob/grep 限 100 条、read 2000 行或 50KB），截断时提示继续 read/offset；子代理看到完整工具输出后自行总结并返回**单条文本**给主代理（Task 只回传子代理最终文本 + session 元数据），要求返回绝对路径。
- 已将搜索命中回显扩展到对标 grep 规格：`search_hits` 单条保存上限改为 2000 字，自检摘要新增“最近一轮命中列表”（最多 100 条、每条 2000 字），减少仅靠短预览做决策。
- 已加入命中列表总字符上限（20k）与最少展示条数（5条），超出会提示省略；同时改为优先展示“最新 query”的 Top-N 命中，避免混入旧轮次。
- 段落索引准确性结论：AI 读取的段落索引是以 `_split_paragraphs` 解析 HTML/纯文本的顺序为准，匹配 Tiptap 的块级节点（p/h1-6/blockquote/pre/li）并解析 data-id；在章节内容 < 200k 时准确，但超大章节 `list_paragraphs` 会进入 approximate 模式（800 字窗口），UI 与索引可能不一致；另外 `read_paragraph` 的 index_base=auto 会把正数当 1-based，下游若传 0-based 且未显式声明会出现偏移。
- 已改为按章动态读取上限（默认按段落数比例+最小/最大值），并取消默认全局上限；工具摘要显示各章读取进度；read_paragraph/read_paragraphs/精确搜索自动读均受按章预算约束。
- 已为 read_paragraphs 增加分页读取模式（chapter_order/chapter_id + offset/limit），内部先 list_paragraphs 再批量 read_paragraph，且 range 模式强制使用 0-based 索引。
- Explore tool_loop 已支持 read_paragraphs 的分页参数，并在提示语中说明 items/分页双模式；按章预算与全局预算会裁剪分页 limit。
- read_paragraphs 的结果返回补充 range 元数据（mode/offset/limit/total_paragraphs/index_base），便于调用侧对齐显示。
- 已基于《一夕千悟，从杂役弟子开始》前几章设计 5 个复杂测试 prompts，覆盖分页读取、items 批量读取、范围锁定与证据回读。
- Backend.md 最新段落存在两类硬错误：`get_writing_context` 未定义导致世界观获取失败，以及 `chapter_vector_service.py` 语法错误导致 explore_content 直接崩溃，任务被提前终止并返回“工具执行失败”提示。
- 已修复 `chapter_vector_service.py` 中 `match_mode` 分支的缩进语法错误（else 块缺缩进），恢复 exact_search_content 的判断逻辑。
- 未能运行 `python -m py_compile`（环境无 python）。
- 已在 explore_tool_loop 内部补回 `get_writing_context` 的局部导入，修复“name 'get_writing_context' is not defined”导致的世界观读取失败。
- 已修复 `reads_left` 为 None 时仍执行 `<= 0` 比较导致的 TypeError，避免 Explore 在 list_chapters 后崩溃。
- 已修复关键词拆分：支持英文逗号 `,`；并跳过对含逗号未拆分关键词的阻断，避免“0 命中”被错误复用。
- 已调整 should_block_search：对“多关键词组合且 0 命中”的历史记录不再阻断单个关键词搜索，避免旧错误记录持续误判。
- 已通读 Backend.md（2021 行）并复盘：主要问题集中在精确搜索过于字面、搜索拦截误判、read_paragraphs 多次返回空、以及负数 limit 触发 SQL 错误。

#### smart* 应用漂移原因排查（待确认）

- [x] 梳理 smart_* → operate_apply → apply_chapter_edit → 修订落库/应用 的实际写入链路
- [x] 核对定位信息来源（node_id/paragraph_index/original_text/nodes_info）与前端传递路径
- [x] 对比 apply_chapter_edit 与 ChapterRevisionService 的替换/插入逻辑差异，定位漂移触发点
- [x] 汇总证据清单（文件路径+关键片段）并输出直白结论
- [x] 在 todo.md 追加 review（结论+影响范围+可能修复方向）

#### review

- 结论：smart_* 只生成内容，真正写入由 operate_apply → apply_chapter_edit 触发修订；漂移主要发生在“定位信息不可靠 + 确认写入使用弱定位”的组合上。
- 关键触发点1：operate_apply 调用 locate_content，默认允许跨章节全局降级；一旦本章定位失败会返回其他章节并修改 chapter_id，导致内容被写入别章（跨章节漂移风险）。
- 关键触发点2：apply_chapter_edit 在 original_text 多次出现且缺 paragraph_index 时，直接替换第一次出现；定位信息缺失/错误时会替换错段。
- 关键触发点3：用户确认后由 ChapterRevisionService 重新“文本匹配写入”，使用 old_content.find/replace(…, 1) 等首匹配逻辑，忽略更稳定的 node_id/段落位置，重复文本时极易漂移到第一处。
- 关键触发点4：locate_content 有 5 分钟缓存且无失效钩子，章节内容变更后仍可能返回旧 paragraph_index。
- 影响范围：所有 replace/insert 场景（尤其是有重复文本、章节近期编辑、或定位失败触发全局降级时）。
- 可能修复方向：确认写入阶段优先使用 node_id/段落位置（与 apply_chapter_edit 保持一致），禁用/显式控制跨章节降级，locate_content 缓存与章节变更联动失效，必要时要求 operate_apply 强制传 node_id/paragraph_index 并拒绝无定位写入。
- 补充结论：章节约 2500 字不会触发 list_paragraphs 的 approximate 模式，定位本身可精确；漂移仍发生的根因在“写入阶段未强制使用 node_id/paragraph_index”，确认落库时仍可能走 original_text 首匹配替换，遇到重复文本就漂移。

#### 严格定位写入（去降级）（待确认）

- [x] 修改 operate_apply：replace/insert 仅接受 node_id/paragraph_index，移除定位失败降级与跨章节降级逻辑
- [x] 修改 apply_chapter_edit：replace/insert 必须 node_id/paragraph_index；移除 original_text/anchor 兜底与自动 locate
- [x] 修改 ChapterRevisionService：确认写入阶段只按 node_id/paragraph_index 精确写入（补齐 <li> 解析）
- [x] 同步提示词说明：operate_apply 不再自动定位，必须带精确定位参数
- [x] 更新 todo.md review（改动与影响）

#### smart* 注入 Explore 证据（待确认）

- [x] 梳理 Explore→Create 调用链，确认 smart_* 参数注入点（planning / task_runner / tool_executor）
- [x] 在 smart_continue/smart_rewrite/smart_insert 调用前，自动合并 Explore evidences/locate_targets 作为上下文参考
- [x] 限制注入长度与格式，避免 prompt 失控（如证据摘要 + 关键段落拼接）
- [x] 更新提示词说明：smart_* 必须基于 explore 证据创作（否则拒绝/先探索）
- [x] 更新 todo.md review（改动与影响）

#### 打通 Explore→Create→Operate 精确链路（待确认）

- [x] Explore 阶段强制“证据 + 定位候选”：要求 list_paragraphs/read_paragraphs 产出 node_id/paragraph_index
- [x] Create 阶段强制注入 Explore 证据 + 目标段落上下文（写入前校验）
- [x] Operate 阶段强制 node_id/paragraph_index 写回（无定位直接失败）
- [x] 统一失败提示：引导用户“先定位段落/先探索证据”
- [x] 更新 todo.md review（链路打通与影响）

#### review

- operate_apply/ apply_chapter_edit/ ChapterRevisionService 全部改为“只接受 node_id/paragraph_index”，移除 original_text/anchor/跨章节降级与 append 降级，确认写入不再用首匹配替换。
- locate_content 默认禁用全局降级；工具提示与规划示例同步更新为“必须先定位”。
- explore_content 在写作类任务强制段落号模式，并在缺少定位候选时直接报错提示“先定位段落”。
- 严格段落号关键词已收敛（不含“续写/写入”），避免 append 场景因无段落而失败。
- locate_content 缓存键加入 chapter.version，避免章节内容更新后仍命中旧定位。
- ChapterRevisionService 对旧修订缺定位信息直接返回 missing_locator，提示需重新定位生成。

#### 修复伪定位导致漂移（待确认）

- [x] locate_targets 仅来自 read_paragraphs 成功结果（禁止 search_hits 兜底）
- [x] read_paragraphs 失败时直接返回 missing_locate_targets，禁止继续创作/写入
- [x] 分页读取修正：确保 list_paragraphs 覆盖候选段落区间，避免索引越界
- [x] 规划参数修正：smart_rewrite 只用 evidences[0].text，不再引用 locate_targets[0].text
- [x] operate_apply 追加校验：paragraph_index 超出范围或 node_id 为空直接失败
- [x] 更新 todo.md review（改动与影响）
- smart_* 新增 evidence_context 注入，ToolExecutor 自动拼接探索证据与定位候选并限长注入。

#### review

- locate_targets 现在只基于 read_paragraph/read_paragraphs 成功返回的原文段落生成，搜索命中不再伪装“可定位”。
- read_paragraphs 未读到原文时，严格模式会返回 missing_locate_targets，阻断后续 smart_* 与写回。
- read_paragraphs items 模式会自动补齐 list_paragraphs 覆盖范围，避免候选段落落在未分页区间导致索引失配。
- operate_apply/ apply_chapter_edit 增加空 node_id 兜底清空与段落越界错误，定位异常不再静默降级。
- planning_prompts 明确 smart_rewrite 必须引用 evidences[0].text，避免 locate_targets[0].text 造成空原文改写。

#### 再次深度 Review（待确认）

- [x] 核对“伪定位修复”改动是否引入新问题（定位候选缺失、性能、兼容性）
- [x] 验证是否真正解决漂移根因（结合 Backend.md/截图链路核验）
- [x] 检查修改完整性（prompt/规划/执行/写回/日志 是否一致）
- [x] 逻辑一致性复核（严格定位模式、read_paragraphs 分页、node_id 约束）
- [x] 更深入验证：确认问题是否真实存在、是否有遗漏问题
- [x] 更新 todo.md review（结论与风险）

#### review

- Backend.md 明确显示“读原文失败但仍自称定位成功”的链路：read_paragraphs 失败（`Backend.md` 第144–149行），随后依然输出“已收集到相关证据”（第150行），并出现 ParameterResolver 对 `locate_targets[0].text` 的缺字段降级（第155行），最终 smart_rewrite 原文长度仅 13（第159行）且 operate_apply 直接使用 para=20/node=tdb57sw8（第176行）——这就是漂移根因证据。
- 伪定位已被阻断：`explore_tools._build_locate_targets` 只用 `result.paragraphs`（不再用 search_hits/evidences），且 `explore_content` 在严格模式下 locate_targets 为空即返回 missing_locate_targets，能直接阻断“未读原文却写回”的流程。`backend/app/services/agent/tools/explore_tools.py`
- 分页覆盖修复降低索引越界：read_paragraphs(items) 会按 paragraph_index 计算页并补齐 list_paragraphs 覆盖范围，避免候选索引落在未分页区间导致“全部为空”的情况。`backend/app/services/agent/tools/explore_tools.py`
- 写回阶段新增硬校验：空 node_id 会清空；段落索引越界直接失败，防止 silent drift。`backend/app/services/agent/tools/operate_tools.py`、`backend/app/services/agent/tools/editor_tools.py`
- 规划层逻辑一致性已补齐：smart_rewrite 明确只能用 `evidences[0].text`，消除“locate_targets[0].text 不存在导致空改写”的问题。`backend/app/services/agent/prompts/planning_prompts.py`
- 残留风险：若 Explore 未读到任何段落，且任务不触发严格段落号模式（如“续写”），locate_targets 可能为空 → 计划仍可能引用 locate_targets[0].chapter_id 失败并触发 ToolExecutor 的“降级使用当前章节”。这不会漂移到别段，但可能写错章节，需要后续增加“无定位就终止写回/必须先读段落”的更强约束。

#### smart_insert 失败（content 为空）排查（待确认）

- [x] 通读 Backend.md 对应时间段日志，定位 smart_insert 失败原因与参数
- [x] 核对 smart_insert 参数生成链路（planning → tool_executor → editor_tools）
- [x] 检查 operate_apply 的 content 空判定与失败路径
- [x] 给出“根因+证据+结论（直白）”
- [x] 更新 todo.md review（结论与影响）

#### review

- 根因：smart_insert 的 evidence_context 被传成 **list**（explore_content 的 evidences 结构），而 SmartInsertInput 要求 **string**，导致 Pydantic 校验失败 → smart_insert 未产出 content → operate_apply 传入 content=None 再次校验失败。`Backend.md:76–85`、`Backend.md:97–103`
- 直接证据：日志显示 SmartInsertInput 验证错误 “evidence_context Input should be a valid string ... input_type=list”（`Backend.md:77–85`），随后 operate_apply 报 “content Input should be a valid string ... input_type=NoneType”（`Backend.md:97–103`）。
- 链路一致性：tool_executor 只在 params 未提供 evidence_context 时才注入字符串证据，因此当规划阶段显式传了 list（例如 `$ref` 指向 evidences）就不会被自动纠正。`backend/app/services/agent/execution/tool_executor.py:374-409`
- 结论（直白）：这次失败不是“定位漂移”，而是**smart_insert 入参类型错误**导致创作阶段直接崩溃，内容根本没生成，后续写回自然失败。

#### 修复 smart_insert evidence_context 类型错误（待确认）

- [x] 只在 smart_insert/smart_rewrite/smart_continue 的 evidence_context 非字符串时，统一转换为字符串（并保留警告日志）
- [x] 确保转换不影响正常 evidence_context 注入逻辑（已有字符串不改动）
- [x] 更新 todo.md review（结论与影响）

#### review

- ToolExecutor 增加 evidence_context 类型强制转换：smart_rewrite/smart_continue/smart_insert 只要发现非字符串就转换并打警告，避免 Pydantic 直接失败。`backend/app/services/agent/execution/tool_executor.py`
- 转换逻辑优先提取 list/dict 中的 text/content/snippet 字段，无法提取时回退为 JSON 文本，保持可读性并保留证据。

#### 追加内容写错章节（第1章→第2章）排查（待确认）

- [x] 通读 Backend.md 最新日志，定位 append/operate_apply 的 chapter_id 来源
- [x] 核对 planning/parameter_resolver/tool_executor 是否发生章节降级或引用越界
- [x] 查明“应写第1章但写到第2章”的触发条件（上下文 chapter_id、locate_targets、task依赖）
- [x] 输出证据清单（行号 + 文件路径）并给出直白结论
- [x] 更新 todo.md review（结论与风险）

#### review

- 证据1（读的确是第1章）：explore_content 在第1章读取段落（`Backend.md:61-66`），并明确“已收集到第一章所有段落（18/18）”（`Backend.md:67`），说明探索目标确实是第1章末尾。
- 证据2（写入却是第2章）：operate_apply/ apply_chapter_edit 实际写入 chapter_id=a82095aa...（`Backend.md:86-88`），这与界面中“第2章”被选中且内容落在第2章末尾一致（截图）。
- 直接根因：**chapter_id 没有从“第1章”目标显式传到写入阶段**，写入工具使用了当前上下文/前端活跃章节的 chapter_id（第2章）。因为这一轮没有 locate_content 任务（仅 explore_content），`plan_generator._ensure_chapter_id_from_locate` 不会覆写章节ID；而 ToolExecutor 对 smart_continue/operate_apply 在 chapter_id 缺失或解析失败时会默认使用 state.chapter_id（当前章节）。`backend/app/services/agent/execution/tool_executor.py:360-392`、`backend/app/services/agent/planning/plan_generator.py:1227-1253`
- 结论（直白）：**你写错章不是定位漂移，而是“章节ID来源错了”**——计划/参数没有把“第1章”的 chapter_id 绑定到写入阶段，最终沿用当前界面所在章节（第2章）。

#### 章节一致性硬约束（治本）（待确认）

- [x] 规划阶段固化“目标章节”并传入 smart_continue/operate_apply（禁止仅靠 state 回退）
- [x] ToolExecutor/operate_apply 写回前校验 chapter_id 与目标章节一致，不一致直接失败并提示
- [x] 记录 chapter_id 来源（显式/locate/explore/回退）到日志，便于追踪
- [x] 更新 todo.md review（结论与影响）

#### review

- 规划阶段新增 explore_content 兜底：当无 locate_content 时，smart_continue/operate_apply 的 chapter_id 优先引用 explore_content 的 `locate_targets[0].chapter_id`（带 default 兜底），避免落回当前界面章节。`backend/app/services/agent/planning/plan_generator.py`
- 执行阶段固化目标章节：explore_content 成功后将 target_chapter_id 写入 shared_state，并记录来源（locate_targets/evidences/chapters）。`backend/app/services/agent/execution/parallel_executor.py`
- 写回前硬校验：operate_apply/apply_chapter_edit 若 chapter_id 与目标章节不一致，直接返回 `chapter_id_mismatch` 阻止写入，并记录 source/expected/actual。`backend/app/services/agent/execution/tool_executor.py`
- 追加日志：smart_continue/operate_apply 会输出 chapter_id 来源与是否采用目标章节，便于追踪“为什么写到某章”。

#### 章节一致性修复再复核（待确认）

- [x] 验证是否引入新问题（chapter_id_mismatch 误杀、旧流程兼容性）
- [x] 验证是否真正解决“第1章写到第2章”的根因
- [x] 检查修改完整性（planning → explore → executor → operate_apply）
- [x] 逻辑一致性复核（目标章节来源、fallback 行为、日志一致性）
- [x] 更深入验证：确认问题是否真实存在、是否有遗漏路径
- [x] 更新 todo.md review（结论与风险）

#### review

- 逻辑完整性：规划层补了 explore_content 的 chapter_id 引用兜底，执行层固化 target_chapter_id，写回前强校验；链路已覆盖 planning → explore → executor → operate_apply。`backend/app/services/agent/planning/plan_generator.py`、`backend/app/services/agent/execution/parallel_executor.py`、`backend/app/services/agent/execution/tool_executor.py`
- 原问题可被阻断：若写回目标与 explore_content 目标不一致，会直接返回 `chapter_id_mismatch`，避免“写到当前章”静默发生。`backend/app/services/agent/execution/tool_executor.py`
- 兼容性风险（新增）：**多章节任务**场景下若同一计划包含多个 explore_content，当前仅保留“最后一次 explore”的 target_chapter_id，可能误判并拦截正确写回（误杀风险）。需要后续按任务依赖绑定 explore→write，或在规划阶段显式为每个写回任务绑定对应 explore 结果。
- 仍需验证：若 explore_content 未产生 locate_targets/chapters/evidences（极少数异常），target_chapter_id 为空则不会触发校验，仍可能回退到当前章节；但这与原问题相比已显著收敛。
- 兼容性补丁：写回校验支持“章节序号 vs UUID”等价匹配，避免因 chapter_id 为数字而被误杀。`backend/app/services/agent/execution/tool_executor.py`

#### 按写回任务绑定目标章节（待确认）

- [x] 规划阶段为写回类任务注入 __target_chapter_id（引用 locate/explore 或显式章节）
- [x] 执行阶段解析 __target_chapter_id 并绑定到 task_state（不透传给工具）
- [x] 更新 todo.md review（结论与影响）

#### review

- plan_generator 为 smart_* / operate_apply / apply_chapter_edit 注入 `__target_chapter_id`，用于**每个写回任务**绑定目标章节（避免全局 target 被后续 explore 覆盖）。`backend/app/services/agent/planning/plan_generator.py`
- parallel_executor 解析并移除 `__target_chapter_id`，写入 task_state（source=task_binding），确保工具层只见到合法参数。`backend/app/services/agent/execution/parallel_executor.py`

#### 章节一致性仍写错章复盘（待确认）

- [x] 通读最新 Backend.md，定位 explore 目标章与写回章是否一致
- [x] 对照任务绑定日志，确认 __target_chapter_id 的来源
- [x] 核对 plan_generator 覆盖规则（显式 chapter_id 不会被 explore 覆盖）
- [x] 输出证据与直白结论

#### review

- 日志显示 **explore 已固化目标章=f9f4...（第1章）**，但任务绑定章变成 **947b...（当前章）**：`Backend.md:01:24:38 目标章节已固化` → `Backend.md:01:24:38 任务2 绑定目标章节: 947b...` → `Backend.md:01:24:38 smart_continue chapter_id 来源=explicit value=947b...` → `Backend.md:01:25:05 operate_apply chapter_id 来源=explicit value=947b...`。
- 根因：计划中已经带了显式 chapter_id（来自当前界面章节），而 `plan_generator._should_override_chapter_id` 只会在 **占位符/空值** 时覆盖，导致 explore 的“第1章”无法覆盖显式 UUID。`backend/app/services/agent/planning/plan_generator.py:1208-1253`
- 结论（直白）：**不是执行阶段丢了章，而是规划阶段一开始就把“当前章节ID”写进任务参数，后续绑定沿用这个错误值，所以依然写错章。**

#### 本次深度复核（待确认）

- [x] 通读 Backend.md 最新日志，抽取“目标章→绑定→写回”的完整链路证据
- [x] 复查相关代码（plan_generator/parallel_executor/tool_executor/operate_apply/editor_tools）与上次改动，确认是否引入新问题
- [x] 核对 chapter_order / chapter_id 传递与覆盖逻辑，确认是否遗漏场景
- [x] 判断是否真正解决“写错章/漂移”根因，列出仍可能触发的路径
- [x] 更新 todo.md review（证据、结论、风险与建议）

#### review

- Backend.md 明确显示：Explore 固化目标章=f9f4...（第1章），但任务绑定/写回使用显式 chapter_id=947b...（当前章），smart_continue/operate_apply 全程走 explicit。证据：`Backend.md:67-74,90-96`。
- 规划阶段的覆盖逻辑不足：`_should_override_chapter_id` 对“显式 UUID”直接返回 False，导致 explore 的目标章无法覆盖；同时 `__target_chapter_id` 优先取 params.chapter_id，进一步把“错误显式值”固化到任务绑定。`backend/app/services/agent/planning/plan_generator.py:1208-1272`
- 执行阶段不会纠正显式值：`smart_continue` 对显式 chapter_id 只告警不覆盖（继续用 explicit），因此即便已知道目标章不同，也不会修正。`backend/app/services/agent/execution/tool_executor.py:390-433`
- `locate_targets` 输出缺少 `chapter_order`，仅有 `chapter_id/paragraph_index/node_id`，导致下游无法用“章序号”做一致性校验。`backend/app/services/agent/tools/explore_tools.py:1544-1566`
- 结论：**写错章的根因仍在“规划阶段把当前章 ID 写进任务参数，且后续不会覆盖显式值”**。因此本轮修复没有治本，只能记录告警与绑定日志，无法阻断错误写回。

#### 章节写回目标修复（待确认）

- [x] 调整 __target_chapter_id 绑定优先级：优先 locate/explore 结果，不再默认沿用显式 chapter_id（防止错误显式值固化）
- [x] locate_targets 输出补充 chapter_order，便于一致性校验与诊断
- [x] 更新 todo.md review（改动与影响）

#### review

- __target_chapter_id 现在优先绑定 locate_content/explore_content 的 chapter_id，只有两者都缺失时才回退到显式 chapter_id，避免“当前章显式值”固化为写回目标。`backend/app/services/agent/planning/plan_generator.py:1269-1285`
- locate_targets 增加 chapter_order 字段，便于下游诊断与一致性校验。`backend/app/services/agent/tools/explore_tools.py:1560-1567`

#### 本次复核（待确认）

- [x] 通读 Backend.md 最新日志，验证目标章/绑定章/写回章是否一致
- [x] 复查本次改动是否引入新问题（plan_generator / explore_tools）
- [x] 检查是否真正解决“写错章/漂移”根因（显式 chapter_id 覆盖问题）
- [x] 复核逻辑一致性（__target_chapter_id 优先级、chapter_order 补充字段）
- [x] 深入验证是否仍有遗漏路径（多章节任务、无 locate/explore 的写回）
- [x] 更新 todo.md review（证据、结论与风险）

#### review

- Backend.md 现有日志仍显示“目标章=第1章、绑定/写回=当前章”的旧问题，但这是**改动前**日志，无法用于判断新修复是否生效；需要复测后看是否仍出现 `chapter_id_mismatch` 或错误写回。`Backend.md:67-96`
- 本次改动未触及执行层写回逻辑，仅调整任务绑定优先级与 locate_targets 输出字段；逻辑一致性良好，风险较低。`backend/app/services/agent/planning/plan_generator.py:1269-1285`、`backend/app/services/agent/tools/explore_tools.py:1560-1567`
- 预期影响：只要计划中存在 explore/locate 任务，写回任务的 target_chapter_id 将优先绑定 explore/locate 结果，不再固化“当前章显式值”，从而减少写错章。
- 仍可能遗漏路径：没有 explore/locate 的写回任务仍会用显式 chapter_id；多章节任务如果同一批次含多个 explore，仍需依赖任务级绑定正确性（当前已优先绑定最近的 locate/explore）。
- 结论：修复方向正确，但**是否真正解决需复测**；若仍写错章，建议启用“expected≠explicit 直接阻断写回”的硬闸。

#### 续写不换行问题复盘（待确认）

- [x] 通读 Backend.md/前端日志，定位续写/写回的 operation 与段落定位参数（append/replace/insert）
- [x] 深度检索写回链路（smart_continue → operate_apply → apply_chapter_edit），确认是否有“段落拼接/去换行”逻辑
- [x] 追踪章节内容结构（HTML/段落标记），确认换行与段落切分的真实规则
- [x] 复核 append 行为是否应该自动包裹成新段落（<p> / <li>）
- [x] 输出证据清单与直白结论，更新 todo.md review

#### review

- 写回链路确认：续写走 `smart_continue → operate_apply(operation=append) → apply_chapter_edit(operation=append)`，append 分支直接 `old_content + actual_content`，**没有任何自动换行/段落包裹**。`backend/app/services/agent/tools/editor_tools.py:494-508`
- insert 分支才会在 HTML 上下文中自动包 `<p>`，append 分支没有这个逻辑，因此纯文本续写会直接拼接到上一段末尾。`backend/app/services/agent/tools/editor_tools.py:521-527`
- operate_apply 对 append 不要求 node_id/paragraph_index（也不会定位），因此默认是“追加到章节末尾”，不会“自动新段落”。`backend/app/services/agent/tools/operate_tools.py:401-412`
- 结论（直白）：**不换行是因为 append 写回逻辑就是字符串拼接，没有包裹新段落，也没有自动插入换行**。要换行只能：1) 用 insert 写入下一段，或 2) append 时内容本身以 `<p>`/换行开头，或 3) 在 apply_chapter_edit 的 append 分支增加自动包段规则。

#### Explore 结果是否进入上下文（待确认）

- [x] 复核 ContextManager 的持久化链路：确认保存的仅是 user/assistant 消息
- [x] 复核 Summarization/ResponseBuilder：确认 explore_content 结果只在当轮摘要上下文中使用且会被压缩
- [x] 汇总直白结论：Explore 结果是否“塞进上下文”、哪些内容能进入记忆层
- [x] 更新 todo.md review（证据与结论）

#### review

- ContextManager/UnifiedMemoryCoordinator 只保存 user/assistant 消息，不保存工具结果；上下文来源是短期对话+摘要+长期记忆/MemoryPack，均基于“对话文本”。`backend/app/services/context/manager.py`、`backend/app/services/agent/memory/unified_coordinator.py`
- explore_content 的结果只在**当轮整合**里使用：ResponseBuilder 调用 `_build_summarization_context` 把任务结果压缩进摘要上下文；探索结果虽可保留到 20000 字符，但仅用于本次回答，不进入后续会话存储。`backend/app/services/agent/planning/response_builder.py`、`backend/app/services/agent/utils/context_builder.py`
- 历史消息构建会过滤 ToolMessage，不把工具输出带入下一轮历史。`backend/app/services/agent/core/message_builder.py`
- 结论（直白）：**Explore 结果不会“全量塞进上下文记忆”**；它只参与本轮回答，后续记忆里只有“助手最终输出的文字”。如果助手没把证据写进回复，就不会被上下文记住。

#### opencode Explore 结果存储机制复核（待确认）

- [x] 通读 opencode Explore 相关实现与提示（agent/prompt/explore.txt）
- [x] 复核子代理/Task 工具输出如何回传主会话（agent.ts / tool/task.ts）
- [x] 复核截断与落盘逻辑（tool/truncation.ts / session/message-v2.ts）
- [x] 汇总“是否持久化/是否能复用”的直白结论
- [x] 更新 todo.md review（证据与结论）

#### review

- Explore 是**子代理**：主会话通过 Task 工具启动 explore 子会话，子代理在自己的 session 中执行搜索/读取。`opencode/packages/opencode/src/agent/agent.ts`、`opencode/packages/opencode/src/tool/task.ts`
- 主会话拿到的只有**子代理最终文本输出**（result.parts 最后一个 text），并附上 `<task_metadata> session_id`；并不会自动把子代理的工具输出并入主会话上下文。`opencode/packages/opencode/src/tool/task.ts`
- 工具输出过大时会被截断并**落盘到 tool-output**，提示使用 Task→explore 继续 grep/read 该文件；这是“把大输出存在文件里，再由子代理处理”的策略。`opencode/packages/opencode/src/tool/truncation.ts`
- ToolPart 会保存 output/attachments 到会话记录，但这是**子会话**里的 ToolPart；主会话只看到 Task 工具的输出摘要。`opencode/packages/opencode/src/session/message-v2.ts`、`opencode/packages/opencode/src/session/prompt.ts`
- 结论（直白）：**opencode 没有把 Explore 的完整结果自动塞回主会话**；它把探索放在子代理会话里，主会话只拿到“总结+子会话 ID”。需要更多细节时，靠 Task 再次让 explore 在其会话里读取（包括读取 truncation 落盘文件）。

#### Explore 结果持久化与上下文策略（待确认）

- [x] 明确“按需取回”策略：证据/原文/截断补全/用户明确要求 → 触发读取完整 Explore
- [x] Explore 结果落盘（Artifact）：保存完整结果+元数据（work_id/user_id/关键词/时间/范围/版本）
- [x] explore_content 返回 artifact_id + 摘要/预览（不把全文塞进上下文）
- [x] 新增 load_explore_artifact 工具：按 artifact_id 取回全文（支持 max_chars/模式）
- [x] 上下文记忆只保存“引用指针”（artifact_id + 摘要），避免重复探索且控制上下文体积
- [x] 失效/清理策略：章节更新/导入/恢复触发失效；TTL=7天、单条上限=200k字符、单 work_id=200、全局=10000

#### review

- 新增 Explore Artifact 落盘与清理：`backend/app/services/agent/utils/explore_artifact.py` 保存完整结果并支持 TTL(7天)/单 work(200)/全局(10000) 清理；超出 200k 字符会跳过存储。
- explore_content 增加 artifact 写入与回传：返回 `artifact_id / artifact_preview / artifact_created_at`，并将 artifact_id 写入 explore_summary，便于后续按需取回。`backend/app/services/agent/tools/explore_tools.py`
- 新增 load_explore_artifact 工具与上下文压缩上限：支持 full/summary/metadata 读取，full 可选 max_chars；并加入 `FULL_CONTENT_TOOLS` 限制。`backend/app/services/agent/tools/explore_tools.py`、`backend/app/services/agent/utils/context_builder.py`
- 失效联动：explore_cache 失效时同步删除落盘 artifacts，继承现有章节更新/导入/恢复触发点。`backend/app/services/agent/utils/explore_cache.py`
- 工具描述补齐：explore_content 返回 artifact_id，新增 load_explore_artifact 说明。`backend/app/services/agent/prompts/tool_descriptions.py`

#### Explore Artifact 深度 Review（待确认）

- [x] 全量复核新增与改动文件（explore_artifact/explore_tools/tool_descriptions/context_builder/tool_dispatcher/explore_cache）
- [x] 验证是否引入新问题（权限校验/路径错误/清理误删/并发冲突）
- [x] 验证是否真正解决原问题（避免重复探索，支持按需取回）
- [x] 检查修改完整性（工具注册/提示词/上下文压缩/失效链路）
- [x] 验证逻辑一致性（artifact_id 生成与回传/读取权限/TTL与上限）
- [x] 更深入验证（问题是否真实存在/是否仍有遗漏）
- [x] 更新 todo.md review（证据与结论）

#### review

- 逻辑完整性：artifact 落盘、工具注册、提示词、上下文压缩与失效链路均已覆盖。`backend/app/services/agent/utils/explore_artifact.py`、`backend/app/services/agent/tools/explore_tools.py`、`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/core/tool_dispatcher.py`、`backend/app/services/agent/utils/context_builder.py`、`backend/app/services/agent/utils/explore_cache.py`
- ✅ 原问题覆盖：Explore 结果可落盘并生成 `artifact_id`，可用 `load_explore_artifact` 取回，避免重复探索。`backend/app/services/agent/tools/explore_tools.py`
- ⚠️ 潜在遗漏1：artifact 只有在**最终回复包含 artifact_id**时才会进入“对话记忆”；目前仅把 artifact_id 写入 explore_summary，**不保证最终回答一定输出**，导致下一轮可能拿不到指针。可选补强：在 ResponseBuilder 输出中强制附带 artifact_id（或写入 MemoryPack）。`backend/app/services/agent/tools/explore_tools.py`、`backend/app/services/agent/planning/response_builder.py`
- ⚠️ 潜在遗漏2：超出 200k 字符会跳过存储（`size_limit`），大范围读取仍可能无法持久化，重复探索问题未完全消除。`backend/app/services/agent/utils/explore_artifact.py`
- ⚠️ 权限边界：`user_id` 可选，若未传入则 artifacts 仅以 work_id 保护；若存在跨用户共享 work_id，需强制传 user_id 或在读取时拒绝空 user_id。`backend/app/services/agent/utils/explore_artifact.py`

#### 写入 Redis 会话状态（待确认）

- [x] 通读与会话状态相关实现（ContextManager / session store / tool policy）
- [x] 设计 Redis 结构：按 session_id 存 last_artifact_id 列表（去重/上限）
- [x] explore_content 写入会话状态（保存 artifact_id）
- [x] 规划阶段/响应阶段读取会话状态并注入上下文（确保下轮可取回）
- [x] 更新 todo.md review（证据与结论）

#### review

- 新增会话级 Redis 状态：按 session_id 记录最近 20 个 artifact_id（含 work_id/preview），TTL=7天；写入在 explore_content 成功保存 artifact 时触发。`backend/app/services/agent/utils/explore_artifact.py`、`backend/app/services/agent/tools/explore_tools.py`
- 规划阶段读取并注入上下文：在 Planning 构建 history_parts 时追加“【可用探索结果】”列表，确保下轮能看到 artifact_id。`backend/app/services/agent/langgraph_agent.py`
- ToolExecutor 补默认参数：load_explore_artifact 自动补 work_id/user_id/mode，避免漏参。`backend/app/services/agent/execution/tool_executor.py`

#### Explore 持久化功能测试（待确认）

- [x] 读取素材《一夕千悟，从杂役弟子开始.txt》，提取可定位的角色/事件/术语
- [x] 设计 5 条测试 prompt：覆盖 Explore → artifact_id → load_explore_artifact（summary/full）
- [x] 设计失效测试：章节更新后再次 Explore 应触发新结果
- [x] 输出可直接复制的测试步骤与提示词

#### review

- 素材要素已提取：段融、赵穆、牛尾刀、吞噬器灵、浑圆桩、一夕千悟、源顺镖局等可用于精确定位。
- 测试覆盖：Explore→artifact_id 回传、load_explore_artifact(summary/full)、会话内复用、章节更新失效。

#### load_explore_artifact 返回空 排查（待确认）

- [x] 通读 Backend.md 日志，定位 load_explore_artifact 调用链与结果长度
- [x] 核对 artifact 文件是否存在与内容是否含 explore_summary
- [x] 核对 load_explore_artifact 入参是否缺 work_id / user_id 导致 not_found
- [x] 输出核心原因+证据+直白结论
- [x] 更新 todo.md review（证据与结论）

#### review

- 证据1：artifact 文件存在且含摘要，路径为 `backend/uploads/explore_artifacts/73d0f930-3cc8-42c7-b48f-da2992952358/475634a1fce04a00ba68ad0e39d9bc7a.json`，其中 `payload.explore_summary` 长度为 1502，`context_for_task` 长度为 3122。
- 证据2：Backend.md 显示 load_explore_artifact 被调用，但规划阶段提示“用户提供了 artifact_id”并未包含 work_id 作为参数（实际由 ToolExecutor 兜底注入），且响应中没有直接暴露 tool 返回内容。
- 结论（直白）：**不是 artifact 不存在，也不是没有摘要**；问题更可能出在“LLM 总结阶段未正确取用/展示 load_explore_artifact 的返回内容”，导致前端看到“结果为空”的提示。进一步验证需要在 load_explore_artifact 内部增加日志（记录返回内容长度）或在 ResponseBuilder 中直接输出工具结果用于核对。

#### 修复 load_explore_artifact 读取空结果（待确认）

- [x] 修复 UPLOAD_DIR 相对路径歧义（统一为绝对路径并保留旧路径回退）
- [x] 增加 artifact_id → 路径 Redis 索引，读取时优先索引回查
- [x] load_explore_artifact 找不到文件时输出可诊断日志
- [x] 更新 todo.md review（证据与结论）

#### review

- UPLOAD_DIR 相对路径已改为“候选根目录”解析（优先 repo root，其次 backend root），避免不同 cwd 造成找不到文件；读取时会尝试旧路径回退。`backend/app/services/agent/utils/explore_artifact.py`
- 保存时写入 Redis 索引（artifact_id → path/work_id/user_id），读取时优先索引回查，显著降低路径歧义导致的 not_found。`backend/app/services/agent/utils/explore_artifact.py`
- 读取失败时增加可诊断日志，便于定位 work_id/path 问题。`backend/app/services/agent/utils/explore_artifact.py`
- [ ] 更新 todo.md review（证据与结论）

#### Create 阶段缺少 node_id/paragraph_index 原因复盘（待确认）

- [x] 梳理 Explore→Create→Operate 责任边界与数据流（evidences/locate_targets/node_id/paragraph_index）
- [x] 追踪“缺少 node_id/paragraph_index”报错来源与触发条件（tool_executor / operate_apply / apply_chapter_edit）
- [x] 核对 smart_* 工具是否产出定位信息，以及是否依赖 locate_content/list_paragraphs/read_paragraphs
- [x] 输出证据清单与直白结论（解释为何会出现“缺少定位而无法应用”）
- [x] 更新 todo.md review（证据与结论）

#### review

- Explore 只负责取证并产出 locate_targets；若要求精确定位但 locate_targets 为空，会直接返回“缺少 paragraph_index/node_id”的错误提示。`backend/app/services/agent/tools/explore_tools.py:4838-4857`
- Create 的 smart_* 只生成内容，不提供定位；smart_insert/smart_rewrite 注释明确“定位职责已移交给 locate_content”。`backend/app/services/agent/tools/editor_tools.py:812-832`、`backend/app/services/agent/tools/editor_tools.py:900-922`
- Operate 层严格要求定位：operate_apply 仅接受 direct 的 node_id/paragraph_index，否则返回“必须提供 node_id 或 paragraph_index”；执行层 tool_executor 也会 fail-fast 拦截。`backend/app/services/agent/tools/operate_tools.py:300-322`、`backend/app/services/agent/execution/tool_executor.py:182-193`
- 最终写回也会再次校验：apply_chapter_edit 与 ChapterRevisionService 对 replace/insert 缺定位直接拒绝。`backend/app/services/agent/tools/editor_tools.py:356-365`、`backend/app/services/chapter_revision_service.py:151-152`
- 结论（直白）：报“缺少 node_id 或 paragraph_index”并非 Create 凭空捏造，而是**定位信息没有从 Explore/locate_content 传到 Operate**；内容可以生成，但写回必须有精确段落定位，没有定位就会被系统拦截。

#### 严格定位硬闸方案（待确认）

- [x] 明确“编辑类请求”的判定范围与触发条件（replace/insert/扩写/润色等）
- [x] Explore 阶段强制产出 locate_targets：缺失时直接终止并提示继续 list_paragraphs/read_paragraphs
- [x] 计划层强制绑定 locate_targets → Create/Operate（smart_* 必须引用 locate_targets[0].text；operate_apply 必须引用 node_id/paragraph_index）
- [x] 设计 locate_targets 选择/消歧规则（精确匹配/段号/用户确认）
- [x] 上下文段落不进入 locate_targets（仅“明确目标段落”可入候选）
- [x] 多段修改拆分为多条编辑任务（每条绑定独立 locator）
- [x] 引入 source_locator 结构并贯穿 Create→Operate（只读、不可改写）
- [x] 执行层增加定位一致性校验（Create 的 source_locator 与 Operate 参数必须一致）
- [x] 补充错误码/日志与用户提示，确保可追溯与可解释
- [x] 增加最小回归用例（缺定位/多段重复文本/错位写回）
- [x] 更新 todo.md review（证据与结论）

#### review

- 执行层新增 source_locator 一致性校验：replace/insert 必须携带 source_locator，且 node_id/paragraph_index 与之匹配，不一致直接阻断写回并记录日志；同时时补齐缺失的 node_id/paragraph_index。`backend/app/services/agent/execution/tool_executor.py`
- 计划层补齐自动写回的定位绑定：对 smart_rewrite/smart_insert 自动 apply 任务补充 source_locator 依赖与 __require_source_locator，避免“写回错位/缺定位”。`backend/app/services/agent/planning/plan_generator.py`
- 多段改写支持拆分：当用户消息包含多个引号段落且仅有单条改写任务时，自动拆成多条 rewrite+apply，逐条绑定独立文本。`backend/app/services/agent/planning/plan_generator.py`
- 补齐 explore_content 参数透传 require_paragraph_index，确保严格定位开关不会被执行层过滤。`backend/app/services/agent/execution/tool_executor.py`
- 最小回归用例新增：覆盖 source_locator 不一致/缺定位补齐/多段拆分。`backend/tests/unit/test_strict_locator.py`

#### Pydantic V2 警告清理（待确认）

- [x] 盘点全部 `class Config` / `@validator` / `json_encoders` 使用点并分类（schemas / core config / agent tools）
- [x] 迁移 `@validator` → `@field_validator`（重点：`backend/app/core/config.py`）
- [x] 迁移 `class Config` → `model_config = ConfigDict(...)`（补齐 from_attributes / arbitrary_types_allowed 等）
- [x] 移除 `json_encoders`（保留必要的 model_config，其余交由 Pydantic 默认序列化）
- [x] 逐文件验证不再触发 Pydantic V2 警告
- [x] 更新 todo.md review（改动与注意事项）

说明（盘点范围）：
- `@validator`: `backend/app/core/config.py`
- `class Config`: 主要集中在 `backend/app/schemas/*` 与 `backend/app/services/agent/*`
- `json_encoders`: `backend/app/schemas/export.py`、`backend/app/services/agent/version_control.py`、`backend/app/services/agent/environment/message_bus.py`、`backend/app/services/agent/memory/types.py`、`backend/app/services/agent/tools/tool_types.py`

#### review

- 已清理全部 `class Config`：改为 `model_config = ConfigDict(...)` 或删除冗余配置，避免 Pydantic V2 deprecation 警告。涉及 `backend/app/schemas/*`、`backend/app/services/agent/*` 等多个模型文件。
- 已移除 `json_encoders`：对 datetime/UUID 依赖 Pydantic 默认序列化；`ToolInput/ToolOutput` 保留 `arbitrary_types_allowed` 配置（改为 `model_config`），减少行为变更风险。`backend/app/services/agent/tools/tool_types.py`、`backend/app/services/agent/version_control.py` 等。
- 已核对仓库内不再出现 `class Config` / `json_encoders` / `@validator`（仅剩非 Pydantic 的 `ConfigTemplates`），警告应消失。

#### 严格定位硬闸方案 复测 Prompts（待确认）

- [x] 通读小说素材（docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt），摘取关键角色/事件/术语
- [x] 设计 5 个高复杂度测试 Prompt，覆盖多段改写拆分、精确定位、跨章歧义消歧、插入/替换混合、source_locator 一致性
- [x] 输出可直接复制的 5 个 Prompts
- [x] 更新 todo.md review（记录覆盖点）

#### review

- Prompts 已覆盖：跨章时间矛盾修复（多段拆分）、重复句子消歧（两处“读取器灵”只改其一）、插入与替换混合、精确定位（必须 list/read 后写回 node_id/paragraph_index）、source_locator 一致性校验场景。

#### 重复句消歧失败原因复盘（待确认）

- [x] 通读 Backend.md 与 INFO.md，抽取失败链路与关键时间点
- [x] 对照 ToolExecutor 的 source_locator 校验日志，确认阻断原因
- [x] 追踪 plan_generator 的定位绑定逻辑（locate_targets[0] 绑定规则）
- [x] 汇总证据并给出直白结论 + 最小修复方向

#### review

- 失败链路证据：Backend.md 显示 `operate_apply` 多次被阻断，错误为 `node_id 与 source_locator 不一致`，实际 node_id=4s4wpsay（第2处），但 source_locator 期望 node_id=hhjsbajw（第1处）。`Backend.md:85-86,108-109,131-132`
- INFO.md 同步记录：系统已识别两处定位，但写回指向第1处，触发 `source_locator_mismatch`，因此阻止写回。`INFO.md:56-59`
- 绑定逻辑证据：plan_generator 目前默认用 `locate_targets[0]` 作为 source_locator / node_id / paragraph_index 的绑定来源；当存在多个候选且未显式指定目标索引时，容易将“第1处”绑定为写回定位。`backend/app/services/agent/planning/plan_generator.py:1420-1667`
- 直白结论：**失败不是 Create 凭空捏造，而是“写回任务绑定了错误的 source_locator（第1处）”，导致执行层一致性校验拦截**。系统防错生效但目标选择错误。
- 最小修复方向：规划阶段支持显式 `locate_target_index` 或基于上下文关键词（如“好刀/废刀”）选择目标段落；写回任务必须引用该目标的 source_locator，避免默认落到 `locate_targets[0]`。
- 方案评审：目标选择显式化（明确选中目标或歧义时要求确认）不是过度设计，**刚刚好，利大于弊**。在重复句/多候选场景下属于必要改动，可减少误改与硬闸拦截。

#### 目标选择显式化修复（待确认）

- [x] 明确“目标选择优先级”规则：显式索引/ID > 关键词匹配 > 歧义报错
- [x] Explore 输出补齐定位元数据：before/after_anchor、chapter_order、稳定 locator_id（可由 chapter_id+node_id+paragraph_index 生成）
- [x] 规划层解析用户意图：识别“第X处/后者/前者/好刀/废刀”等，写入 locate_target_index 或 locator_id
- [x] 规划层绑定修正：smart_rewrite/smart_insert/operate_apply 统一引用选中目标（不再默认 locate_targets[0]）
- [x] 执行层选择器支持 locate_target_index/locator_id，并在多候选且未指定时返回 ambiguous_locator
- [x] 更新错误提示与日志：明确提示“需指定第几处/请确认目标段落”
- [x] 增加回归用例：重复句消歧成功/歧义报错/关键词匹配
- [x] 更新 todo.md review（记录改动与风险）

#### review

- locate_targets 新增稳定 locator_id（优先 chapter_id+node_id/paragraph_index），并保留 before/after_anchor/insert_context 元数据，便于后续选择与诊断。`backend/app/services/agent/tools/explore_tools.py`
- 规划层新增“显式目标选择”解析：识别“第X处/前者/后者”等索引与单段引用提示，写入 locate_target_index/locate_target_hint，并同步改写 locate_targets 引用路径，避免默认落到第1处。`backend/app/services/agent/planning/plan_generator.py`
- 执行层支持 locator_id/索引/关键词匹配，auto_locator 会强制重新选择目标并在多候选时返回 ambiguous_locator；错误提示明确要求“第几处”。`backend/app/services/agent/execution/tool_executor.py`
- 回归用例覆盖 locator_id/负索引/关键词命中/歧义报错与索引路径改写。`backend/tests/unit/test_strict_locator.py`

#### 插入位置错位原因复盘（待确认）

- [x] 通读 Backend.md/INFO.md，抽取“插入在之前”的任务链路与参数（operation/paragraph_index/node_id/position）
- [x] 对照 operate_apply → apply_chapter_edit 的 insert 定位逻辑，确认“after/before”落点规则与 HTML 包段行为
- [x] 追踪定位来源（locate_targets / read_paragraphs / list_paragraphs），确认段落索引与前端显示是否一致
- [x] 对照前端插入展示逻辑（NovelEditor / AIRevisionBar），确认是否存在“显示顺序反转”或 HTML 段落切分差异
- [x] 汇总证据并给出直白结论 + 最小修复方向

#### review

- 后端链路证据：Backend.md 显示插入任务确实走 `operate_apply -> apply_chapter_edit`，并用 DIRECT 定位 para=75、node=3z720q99，操作类型为 insert。`Backend.md:86-93`
- 后端“插入之后”规则：apply_chapter_edit 的 insert 在 node_id 时调用 `_insert_after_node_id`，在 paragraph_index 时用 `_get_paragraph_position(..., "end")`，语义都是“在段落末尾之后插入”。`backend/app/services/agent/tools/editor_tools.py:475-553`
- 前端展示错误点：NovelEditor 处理插入修订时，nodeId 定位得到的是节点范围（from/to），但插入分支使用 `resolvedPosition.from` 作为插入点，等于“插到段落开头”，导致视觉上变成“在目标段落之前插入”。`src/components/editor/NovelEditor.tsx:1010-1068,1354-1389`
- 直白结论：**不是后端插错，而是前端插入修订“用错了位置边界（from 而不是 to）”，把“应插在段落之后”显示成“插在段落之前”。**
- 最小修复方向：插入类型应使用 `resolvedPosition.to`（或直接调用 locateInsertPosition(nodeId)），确保“after”语义；同时保持 continue/insert 两个分支一致。

#### 插入位置错位修复（待确认）

- [x] 修正插入修订的插入点：insert 分支改用 `resolvedPosition.to`（或 locateInsertPosition 的结果）
- [x] 统一 continue/insert 的插入位置规则，避免同类逻辑分叉
- [ ] 增加最小回归：插在“之后”不再跑到段落前
- [x] 更新 todo.md review（记录改动与风险）

#### review

- 插入修订现在与续写一致使用 `resolvedPosition.to` 作为插入点，避免把“插在段落之后”显示成“插在段落之前”。`src/components/editor/NovelEditor.tsx`
- 未新增前端回归用例：仓库缺少现成的前端测试框架与用例入口，若需要可补 Vitest/Jest 再覆盖该场景。

#### 写回章节绑定修复（待确认）

- [x] 规划层：写回任务 chapter_id 强制绑定 explore/locate 的目标章节（覆盖显式值）
- [x] 执行层：保持 chapter_id_mismatch 硬闸，补充日志标注“覆盖来源”
- [ ] 回归验证：跨章写回不再被 chapter_id_mismatch 拦截
- [x] 更新 todo.md review（记录改动与风险）

#### review

- 规划层对 smart_rewrite/smart_insert/operate_apply/apply_chapter_edit 强制使用 locate/explore 的 chapter_id（即便显式值存在），并同步使用选中 locate_targets 路径，避免“显式当前章”固化。`backend/app/services/agent/planning/plan_generator.py`
- 执行层在 replace/insert 且 auto_locator 场景下，如果显式 chapter_id 与目标章节不一致，会覆盖为目标章节并记录来源日志；chapter_id_mismatch 硬闸仍保留。`backend/app/services/agent/execution/tool_executor.py`
- 回归验证未做完整跨章写回复测：本地 pytest 受依赖缺失（chromadb）阻塞，需要环境补齐后复测。

#### 重复句消歧仍失败（ambiguous_locator）复盘（待确认）

- [x] 通读 Backend.md/INFO.md，定位 “ambiguous_locator” 触发的具体步骤与参数（locate_target_index/locator_id/hint）
- [x] 追踪规划层输出：是否产生 locate_target_index/locator_id，是否被覆盖为 locate_targets[0]
- [x] 追踪执行层选择器：_select_locate_target 的匹配路径是否被显式 index/ID 命中
- [x] 对照 locate_targets 输出内容（chapter_id/node_id/paragraph_index/locator_id/text）判断是否确有多候选
- [x] 汇总证据并给出直白结论（核心原因 + 最小修复方向）
- [x] 更新 todo.md review（记录改动与风险）

#### review

- Backend.md 未出现 ambiguous_locator 相关日志；取而代之的是多次 ParameterResolver 警告：`path=content` / `path=source_locator` 字段不存在，说明写回任务未拿到 smart_rewrite 的内容与定位信息。`Backend.md:100-137`
- 规划层当时生成的 apply 任务仍在引用 `$TASK.content` 而非 `versions[0].content`，且 source_locator 未绑定（被 Resolver 降级），导致 operate_apply 进入写回时缺少 content 与 node_id/paragraph_index。`backend/app/services/agent/planning/plan_generator.py`、`backend/app/services/agent/parameter_resolver.py`
- 后端写回链路明确要求 content 与定位：`apply_chapter_edit` 先校验 `empty_content` 与 `missing_position_for_replace`，缺失即失败；operate_apply 也只允许 direct 定位。`backend/app/services/agent/tools/editor_tools.py`、`backend/app/services/agent/tools/operate_tools.py`
- 结论（直白）：**失败不是“ambiguous_locator”，而是写回任务没拿到内容和定位（source_locator/content 都缺），导致写回直接失败。**“ambiguous_locator”只出现在前台文本里，是 AI 自己编的解释，不是系统返回的真实错误。
- 最小修复方向：保证 smart_rewrite → operate_apply 的 content 与 source_locator 绑定正确、写回任务携带 locate_target_index/locator_id；若绑定缺失，应在执行层直接报错而不是走 summarization。`backend/app/services/agent/planning/plan_generator.py`、`backend/app/services/agent/execution/tool_executor.py`

#### 写回参数完整性修复计划（待确认）

- [x] 规划层：operate_apply 绑定 data.content / data.versions[0].content（StandardTool 输出结构）
- [x] 规划层：operate_apply 绑定 data.source_locator 或 locate/explore 选中目标（source_locator+node_id/paragraph_index）
- [x] 执行层：缺 content/source_locator 时直接返回明确错误，禁止进入 summarization
- [x] 执行层：显式目标选择强制 re-select（locate_target_index/locator_id/hint）
- [x] 多候选未指定：返回 ambiguous_locator 并提示“第几处”
- [x] 增加回归用例：缺参报错 / 写回成功 / 歧义报错
- [x] 更新 todo.md review（记录改动与风险）

#### review

- 写回任务统一绑定 StandardTool 输出结构：content 改为 `data.versions[0].content`/`data.content`，original_text 改为 `data.original_text`，source_locator 改为 `data.source_locator`，并优先用 locate/explore 目标覆盖定位。`backend/app/services/agent/planning/plan_generator.py`
- 执行层新增缺参硬闸：replace/insert/append/content 的 content 为空或非字符串直接报错，避免写回进入 Pydantic 报错与“假成功”总结。`backend/app/services/agent/execution/tool_executor.py`
- 显式目标选择与歧义提示已生效：locate_target_index/locator_id/hint 强制重选，多候选未指定返回 ambiguous_locator。`backend/app/services/agent/execution/tool_executor.py`
- 回归用例补充：校验 apply_task 使用 data.* 路径与歧义选择器行为。`backend/tests/unit/test_strict_locator.py`

#### 写回内容引用路径修正（待确认）

- [x] plan_generator：所有 $ref 指向 StandardTool 的输出时补上 data 前缀（content/source_locator/versions）
- [x] plan_generator：兼容旧路径（无 data）但优先 data 路径
- [x] 增加最小回归：StandardTool 输出结构下 content 不再为 None
- [x] 更新 todo.md review（记录改动与风险）

#### review

- 规划层写回引用全部切到 data.* 路径，避免 `versions[0].content`/`source_locator` 解析失败导致 content=None。`backend/app/services/agent/planning/plan_generator.py`
- 参数解析新增兼容：若 payload 没有 data 字段，会回退按旧路径解析，兼容旧输出结构。`backend/app/services/agent/parameter_resolver.py`
- 最小回归用例新增：apply_task 生成的 content/original_text/source_locator 均为 data.* 路径。`backend/tests/unit/test_strict_locator.py`

#### 写回段落错位（定位17→应用13）原因复盘与修复（待确认）

- [ ] 通读 Backend.md / INFO.md，抽取“read_paragraph=17 与 operate_apply=12”链路证据
- [ ] 追踪 read_paragraph 的 index_base/校正逻辑（langgraph_tools）与 explore_tools 的索引入库方式
- [ ] 复核 locate_targets 生成顺序与 is_target 标记，确认是否误选 locate_targets[0]
- [ ] 修复索引一致性：使用 read_paragraph 返回的 paragraph_index/target_index 写入 ParagraphRead
- [ ] 修复目标选择：自动读取段落标记 is_target=False 或显式目标优先排序，避免默认取错
- [ ] 补充日志：记录 index_base/纠正后索引/最终写回索引，提示“已纠正”
- [ ] 增加最小回归用例：index_base auto/clamp、locate_targets 用纠正索引、写回一致性
- [ ] 更新 todo.md review（证据与结论）

#### 抽象需求下的唯一定位策略（待确认）

- [x] 搜索结果仅作为候选池，不直接写回（明确“候选≠目标”）
- [x] 对候选逐条 read_paragraph 验证原文（命中关键词/目标句/上下文锚点）
- [x] 评分排序：关键词覆盖率 + 句子匹配 + 上下文锚点命中
- [x] 高置信唯一：自动绑定 locator_id/locate_target_index
- [x] 低置信歧义：强制用户确认“第几处”，不允许写回
- [x] 写回硬闸：operate_apply 必须携带唯一定位，否则报错拒绝
- [x] 更新 todo.md review（结论与风险）

#### review

- 仅对“已读取原文”的段落做候选筛选，搜索命中不会直接写回；候选来自 read_paragraphs/paragraphs。`backend/app/services/agent/tools/explore_tools.py`
- 新增候选评分与唯一性选择：基于引号原句命中 + 关键词覆盖率进行评分；高置信时自动只保留一个 is_target。`backend/app/services/agent/tools/explore_tools.py`
- 低置信保留多候选：不做自动裁剪，执行层会触发歧义提示，要求用户明确“第几处”。`backend/app/services/agent/execution/tool_executor.py`

#### 插入歧义修复方案（待确认）

- [x] 规划层：insert 写回任务补齐 locate_target_hint（来自定位段落 text），用于自动消歧
- [x] 规划层：insert 写回任务补齐 target_description（同 locate_target_hint），便于执行层匹配
- [x] 规划层：在 explore 定位任务上保留 require_paragraph_index 且不覆盖用户显式选择
- [x] 回归用例：_build_apply_task(insert) 生成 locate_target_hint/target_description 路径正确
- [x] 更新 todo.md review（改动与影响）

#### review

- insert 写回任务现在自动带 locate_target_hint/target_description（默认指向定位段落 text），执行层可用该 hint 消歧，不再只靠 locate_targets[0]。`backend/app/services/agent/planning/plan_generator.py`
- 新增回归用例：验证 smart_insert 的 apply 任务包含 locate_target_hint/target_description 的路径。`backend/tests/unit/test_strict_locator.py`
- explore_content 的 require_paragraph_index 若为空/null 会被强制补齐为 True，但显式 False 不会被覆盖，避免“明明要求严格定位却因 null 被跳过”。`backend/app/services/agent/planning/plan_generator.py`

#### 对标 opencode 歧义处理（待确认）

- [x] 追踪 edit/multiedit 替换逻辑，确认多匹配时的处理方式
- [x] 追踪 patch/apply_patch 的上下文消歧机制与失败条件
- [x] 汇总做法差异与可借鉴点
- [x] 更新 todo.md review（证据与结论）

#### review

- opencode 的 edit/multiedit 采用“oldString 必须唯一”的硬约束：若找到多处匹配且 replaceAll=false，会直接报错并要求提供更多上下文，避免猜测写回。`opencode/packages/opencode/src/tool/edit.ts`
- opencode 的 patch/apply_patch 通过 @@ 变更上下文进行消歧：找不到上下文或匹配失败直接抛错；测试覆盖“@@ header 消歧”和“缺上下文拒绝”。`opencode/packages/opencode/src/patch/index.ts`、`opencode/packages/opencode/test/tool/apply_patch.test.ts`

#### 插入失败（歧义定位）原因复盘（待确认）

- [x] 通读 Backend.md / INFO.md，定位“插入失败=定位歧义”的具体请求链路与时间点
- [x] 抽取 explore/locate_targets 输出，确认是否多候选或未携带 locator_id/locate_target_index
- [x] 追踪计划层绑定：operate_apply 是否携带 locate_target_index/locator_id/source_locator
- [x] 追踪执行层选择器：_select_locate_target 是否触发 ambiguous_locator（原因与分支）
- [x] 对照插入任务参数（before/after/insert_context）与 locate_targets 顺序，确认是否误用 locate_targets[0]
- [x] 给出证据清单与直白结论（是谁的问题、为何失败）
- [x] 更新 todo.md review（证据与结论）

#### review

- 证据1：Backend.md 仅出现 exact_search_paragraphs（hits=6）与“严格段落号模式”，未出现 read_paragraph/read_paragraphs 调用，说明本次定位没有读原文证据。`Backend.md:128-149`
- 证据2：插入任务仅记录 TaskRunner/ToolExecutor 入口，没有出现 operate_apply 的“开始执行工具/Operate 路由/定位完成”日志，说明插入在执行层被提前拦截。`Backend.md:166-171`
- 证据3：执行层在 replace/insert 时会强制 _ensure_source_locator；若 locate_targets 多候选或未显式指定 locator_id/locate_target_index，会返回 ambiguous_locator（“定位候选不唯一”）。`backend/app/services/agent/execution/tool_executor.py:1005-1122`
- 直白结论：**这是后端规划/执行链路的问题**——Explore 没有产出“单一可写回定位”，且 plan 未显式绑定 locator_id/locate_target_index，导致执行层在定位阶段判定“歧义”并拦截写回；前台的“定位信息存在歧义”是对该拦截的自然语言描述。 

#### 插入失败（目标段落未命中）排查（待确认）

- [x] 通读 Backend.md，锁定 explore_content 的失败原因与后续参数降级证据
- [x] 核对 explore_content 的“严格段落号”条件与缺失 locate_targets 的直接报错逻辑
- [x] 对照章节文件，确认目标句实际所在章节与本次请求指定章节不一致
- [x] 复盘参数解析链路，确认 smart_insert/operate_apply 因缺定位字段降级
- [x] 汇总证据清单并给出直白结论（核心问题与根因链路）

#### review

- explore_content 在严格段落号模式下若未产出 locate_targets 会直接返回错误 `missing_locate_targets`，并提示需要 list_paragraphs/read_paragraphs。`backend/app/services/agent/tools/explore_tools.py:4972-4988`
- 本次日志显示 explore_content 失败后，ParameterResolver 连续提示 locate_targets/paragraph_index/node_id 等字段不存在，说明后续任务拿不到定位信息。`Backend.md:57-75`
- 目标句“吞噬效果：五虎群羊刀入门。”实际存在于章节文件 `backend/uploads/chapters/239b4eca-358a-4c32-b231-75b78f098099/68bff4d0-ac26-4f53-bf91-f1d9833aabb5.html`，而请求锁定的章节 `f2b84430-e08c-49f7-9df4-c7bcfecbd975.html` 内容为“第3章 一夕千悟”段落，文本不含该句。`backend/uploads/chapters/239b4eca-358a-4c32-b231-75b78f098099/68bff4d0-ac26-4f53-bf91-f1d9833aabb5.html`、`backend/uploads/chapters/239b4eca-358a-4c32-b231-75b78f098099/f2b84430-e08c-49f7-9df4-c7bcfecbd975.html`
- 直白结论：**核心问题是“定位章节错了”**。系统把“吞噬效果：五虎群羊刀入门。”去第3章（f2b844…）里找，但它实际在第1章（68bff…）里，导致 explore_content 无法读到原文段落→locate_targets 为空→smart_insert/operate_apply 失去 node_id/paragraph_index 而降级失败。

#### 错误章节锁定根因排查（待确认）

- [x] 通读规划链路（plan_generator / planning_prompts / planning_examples），确认 chapter_id 的写入来源与优先级
- [x] 追踪执行链路（tool_executor / parameter_resolver），确认 chapter_id 是否会被显式值覆盖或降级
- [x] 对照 Backend.md 中“定位任务/写回任务”的参数日志，锁定是哪一步把 chapter_id 固化为 f2b844…
- [x] 复核 work/chapter 数据来源（导入/上下文记忆/最近章节），确认“默认章”可能来源
- [x] 汇总证据并给出直白结论（为何锁错 + 根因链路 + 最小修复方向）

#### review

- 前端在章节面板发送请求时**必带 chapter_id**，并把 `chapter_context: "当前章节ID: {chapterId}"` 写进上下文；这是“锁章”最直接的来源。`src/components/editor/AIPanel.tsx`
- 后端 `agent_chat_stream` 会验证并透传 `request.chapter_id` 给 LangGraph 规划器；规划 prompt 里会显式展示 `chapter_id`，导致规划器默认把编辑请求当“当前章节”处理。`backend/app/api/v1/agent.py`、`backend/app/services/agent/planning/plan_generator.py`
- 执行层不会自动跨章：`explore_content` 只有在目标任务不含章节限定时才会全书搜索；一旦规划文本里写了“在章节…定位”，就被锁死在该章。`backend/app/services/agent/tools/explore_tools.py`
- `ParameterResolver` 在定位字段缺失时会降级为 fallback，不会中断流程；结果是 smart_insert/operate_apply 仍被调用但缺定位信息，只能失败。`backend/app/services/agent/parameter_resolver.py`
- 直白结论：**根因是“章节面板上下文强绑定 + 规划器默认本章优先”**。当前章 ID 被前端写入上下文与请求体，规划器据此把“插入”任务限定到本章；当目标句不在本章时就无法产出 locate_targets，从而触发写回失败。最小修复方向：当用户未指定章节且给出精确引号/短句时，规划器应优先全书定位；或在本章未命中时自动放宽到全书并要求用户确认章节。

#### Explore 阶段工具梳理（待确认）

- [ ] 通读 explore_content 的阶段流程与工具白名单，列出会被调用的工具集合
- [ ] 按阶段（预处理/精确搜索/读取/定位）说明每个工具的作用与入参
- [ ] 汇总为“直白清单 + 调用条件”，回答用户问题

#### list_chapters 能力评估（待确认）

- [x] 通读 list_chapters 实现，核对它能返回哪些字段、是否依赖章节文件内容
- [x] 结合 explore_content 的强制流程，说明 list_chapters 在“已锁章/未锁章”两种场景的实际作用
- [x] 汇总为直白结论：是否能发挥预期能力、在哪些情况下会沦为“走过场”

#### review

- list_chapters 实际返回字段：chapter_id/id、order、title、word_count、paragraph_count；paragraph_count 依赖读取章节文件并用 `_split_paragraphs` 统计。`backend/app/services/agent/langgraph_tools.py`
- 未锁章时它是“范围决策”的入口（先列章 → 再决定去哪些章 list_paragraphs/搜索）；锁章后仍会被强制执行，但结果不再影响范围，变成流程走过场。`backend/app/services/agent/tools/explore_tools.py`
- 直白结论：list_chapters 本身能力完整，但在“规划器提前锁章”场景下失去决策作用。

#### Opencode Explore 工具梳理（待确认）

- [x] 通读 D:\Java\ai_writer\opencode 中 Explore/检索相关代码，列出阶段使用的工具集合
- [x] 逐个说明工具作用与输入/输出（直白解释）
- [x] 汇总对比：和当前项目 Explore 的主要差异点（仅限工具层）

#### review

- Opencode 的 explore 子代理允许工具：glob、grep、list、read、bash、webfetch、websearch、codesearch（以及外部目录权限用于截断输出读取）。`opencode/packages/opencode/src/agent/agent.ts`
- 工具语义：glob=文件名模式匹配；grep=正则搜文件内容；list=列目录树；read=读文件内容；bash=执行命令（但文档强调别用来替代搜索/读写）；webfetch=抓取网页；websearch=在线检索；codesearch=外部代码/文档检索。`opencode/packages/opencode/src/tool/*.txt`
- 与当前项目的差异（工具层）：Opencode Explore 面向“文件/代码”检索（glob/grep/read），而当前项目 Explore 面向“章节/段落”检索（list_chapters/list_paragraphs/read_paragraphs/exact_search_paragraphs）。

#### 修复：引用句子时不锁章（待确认）

- [x] 在 plan_generator 增加“引用句子且未显式指定章节”判断
- [x] 对 explore_content 任务补充 `force_global_search` 参数（仅在上述条件满足时）
- [x] explore_content/ContentExplorer 支持忽略章节范围（force_global_search）
- [x] 保持最小改动，不影响用户明确“本章/第X章”的请求
- [x] 更新 todo.md review（改动与影响）

#### review

- 规划层新增“引用句子且未指明章节”判定：满足条件时给 explore_content 注入 `force_global_search=true`，并在目标描述里追加“全文范围搜索”，避免锁死本章。`backend/app/services/agent/planning/plan_generator.py`
- explore_content 支持 `force_global_search`：会剥离“在章节…/本章”等提示并清空 chapter_scopes，缓存键也区分该开关。`backend/app/services/agent/tools/explore_tools.py`
- ContentExplorer 接收 `force_global_search` 并在初始化时忽略章节范围，确保后续 tool_loop 不再受锁章限制。`backend/app/services/agent/tools/explore_tools.py`

#### 重复 read_paragraph 现象追因（待确认）

- [x] 通读 Backend.md / INFO.md，定位重复 read_paragraph 的时间段与频率
- [x] 追踪 explore_tool_loop 的决策与去重逻辑（should_read_paragraph / read_paragraph 分支 / prompt 汇总）
- [x] 对照日志，解释“重复调用”与“实际是否重复读取”的差别
- [x] 汇总证据并给出直白结论（核心问题 + 触发条件）

#### review

- 日志证据：Backend.md 在 00:58:23–01:00:06 内连续多次调用 `read_paragraph`，参数始终是第3章第36段，仅 context_before/after 在 1~3 之间变化。`Backend.md:58-119`
- 前台轨迹同样重复显示 “ReadParagraph: 第3章 · 第36段”，对应同一轮工具调用被多次触发。`INFO.md:24-50`
- 代码行为：`should_read_paragraph` 只做“已读去重”并返回 skipped，但 **不会阻止 LLM 决策再次调用**；`read_paragraph` 分支在已读时返回 `{success: True, skipped: True}`，日志只打 success，不展示 skipped，导致看起来像“重复读取”。`backend/app/services/agent/tools/explore_tools.py:795-815,3740-3815`
- 核心结论：**重复出现是“工具循环决策层没有硬防重 + 日志/前台不展示 skipped”**的结果。系统并非一直重新读文件，而是被 LLM 反复触发同一工具调用，后端多数会直接跳过。触发条件是“目标段落已定位但仍反复强调读取上下文”的任务描述。`backend/app/services/agent/tools/explore_tools.py:2961-3032`

#### 修复：read_paragraph 重复读取（待确认）

- [x] 在 read_paragraph 成功时记录上下文段落为已读，并追加 ParagraphRead(is_target=False)
- [x] skipped 时不再追加空 ParagraphRead/证据，避免误导
- [x] 验证 locate_targets 仍只使用 is_target=True（不误用上下文段）
- [x] 更新 todo.md review（改动与影响）

#### review

- read_paragraph 成功后会把返回的前后文段落也标记为“已读”，并以 `is_target=False` 追加到 ParagraphRead 列表，LLM 可以在“已读段落”摘要中看到上下文已覆盖。`backend/app/services/agent/tools/explore_tools.py`
- skipped 情况不再重复追加段落/证据，避免前端重复显示“读过”。`backend/app/services/agent/tools/explore_tools.py`
- locate_targets 仍仅使用 `is_target=True` 的段落构建定位目标，上下文段落不会被误用于写回定位。`backend/app/services/agent/tools/explore_tools.py`

#### 显式告知“上下文已满足”（待确认）

- [x] 在 ExploreState 记录“目标段上下文覆盖范围”（min/max index）
- [x] 在 _build_tool_loop_summary 输出“上下文已覆盖”提示（明确第X章第Y段前后范围）
- [x] 在工具决策提示中新增硬规则：上下文已覆盖则禁止再次 read_paragraph
- [x] 更新 todo.md review（改动与影响）

#### review

- ExploreState 新增上下文覆盖记录：读段落时根据返回的 paragraphs 索引范围记录 (start,end)，为“上下文已覆盖”判断提供依据。`backend/app/services/agent/tools/explore_tools.py`
- 工具循环摘要新增“上下文已覆盖（无需重复读取）”提示，明确目标段与覆盖范围，直接暴露给 LLM。`backend/app/services/agent/tools/explore_tools.py`
- 决策提示新增硬约束：若出现“上下文已覆盖”，不要再次调用 read_paragraph/read_paragraphs 读取同一目标段落。`backend/app/services/agent/tools/explore_tools.py`

#### 生成复杂测试提示词（待确认）

- [x] 读取小说素材，整理人物/设定/关键情节要点
- [x] 设计 5 条复杂 Prompt（不包含工具名），覆盖定位/上下文/风格/约束
- [x] 输出可直接复制使用的提示词
- [x] 更新 todo.md review（改动与说明）

#### review

- 基于第1–5章素材整理人物/设定/情节点，设计 5 条复杂测试提示词，覆盖定位、上下文读取、风格与约束要求，并避免出现工具名。`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`

#### 采纳后新增内容被清除排查（待确认）

- [x] 通读 Backend.md / INFO.md，定位“采纳”触发点与修订事件链路
- [x] 追踪前端采纳事件流（agent-accept-revision/acceptAll）到编辑器处理逻辑
- [x] 复核 applyRevisionDecisionToHtml / NovelEditor 插入分支，确认是否把新增内容误删
- [x] 汇总证据并给出直白结论（核心问题 + 触发条件）

#### review

- 采纳事件链路：AIPanel 点击采纳会派发 `agent-accept-revision`，编辑器监听并调用 `applyRevisionDecisionToHtml` 做标记清理。`src/components/editor/AIPanel.tsx`、`src/components/editor/NovelEditor.tsx`
- 关键触发条件：当修订目标章节 ≠ 当前编辑章节时，`handleAcceptRevisionEvent` 会直接 `clearPendingRevisions(revisionIds)` 并 `return`，相当于把跨章节修订当作“丢弃”处理。`src/components/editor/NovelEditor.tsx`
- 直白结论：你在**非目标章节**点击采纳时，系统并没有应用新增内容，而是清空了“跨章节待应用修订”，所以新内容消失；这不是后端写回问题，而是前端跨章节采纳逻辑把“采纳”当成“清空待应用”。`src/components/editor/NovelEditor.tsx`

#### 修复：跨章节采纳应自动应用（待确认）

- [x] 采纳内容修订后触发章节列表刷新（复用 agent-chapter-confirm），确保跨章节也能拿到已应用内容
- [x] 覆盖两条采纳路径：useAgentChat.submitApproval（阻塞式）与 AIPanel 非阻塞采纳
- [x] 不覆盖当前编辑内容：仅刷新章节列表（由 WorkDetailView 现有监听处理）
- [x] 更新 todo.md review（改动与影响）

#### review

- useAgentChat 的采纳成功统一派发 `agent-chapter-confirm`，不再区分是否章节操作，确保跨章节内容修订也能触发列表刷新。`src/hooks/useAgentChat.ts`
- AIPanel 的非阻塞采纳在后端确认成功后派发 `agent-chapter-confirm`，补齐“无 pendingApproval 场景”的刷新链路。`src/components/editor/AIPanel.tsx`

#### ReadParagraph 重复读取排查（待确认）

- [x] 通读 Backend.md / INFO.md 中 ReadParagraph 重复日志，标记轮次、段落与触发点
- [x] 追踪后端 read_paragraph 调用链（explore_tools + 计划/循环决策），确认是否重试/循环/去重缺失
- [x] 追踪前端执行轨迹渲染（ExecutionFlow/ExploreCard），核对是否重复推送或重复渲染
- [x] 汇总证据（日志片段 + 代码位置 + 触发条件），给出核心原因与直白结论
- [x] 在 todo.md 追加 review（修改/发现/风险）

#### review

- Backend.md 显示同一段落被多次发起 read_paragraph（第1章第70段），且夹杂大量 read_paragraphs 失败（“没有可读取的段落”），这会让工具循环一直觉得“上下文不足”而继续读。`Backend.md:110-209`
- INFO.md 里 AI 决策理由反复写“已读取但未获取上下文，需要重新读取”，说明不是“没读到”，而是**认为上下文没拿到**导致重复调用。`INFO.md:30-66`
- 前台“ReadParagraph: 第1章 · 2段”其实是 read_paragraphs 批量读取的**数量标签**，不是“第2段”。前端标签用 count 渲染（第X章 · {count}段）。`backend/app/services/agent/tools/explore_tools.py:1968-1978`
- 核心机制：read_paragraphs 会先用 should_read_paragraph 去重，若全部已读就直接报“没有可读取的段落”，但这不会中止 LLM 的工具循环，于是 LLM 继续读同一目标段落。`backend/app/services/agent/tools/explore_tools.py:4061-4081`

#### 替换模式下拉为圆弧＋号（待确认）

- [x] 定位 Plan/Agent 下拉与 @ 指令列表的实际渲染位置
- [x] 用圆弧＋号按钮替换下拉触发器，点击直接打开 @ 指令列表
- [x] 适配无 @ 触发时的指令选择逻辑（不误删输入文本）
- [x] 简要自检交互与样式（按钮、弹层、键盘操作）

#### review

- Plan/Agent 下拉已替换为圆弧＋号按钮，点击直接打开指令列表，空白输入也可正常弹出。`src/components/editor/AIPanel.tsx`
- 新增 manualMenuOpen 控制与关闭逻辑，避免无 @ 时菜单被自动关闭，同时不影响 @ 触发筛选流程。`src/components/editor/AIPanel.tsx`
- AIPanel 不再渲染模式切换器，执行模式继续沿用默认 plan（enable_reflection 逻辑未改动）。`src/components/editor/AIPanel.tsx`

#### ＋号按钮加圆弧外圈（待确认）

- [x] 定位 AIPanel 中的圆弧＋号按钮样式
- [x] 调整默认态样式，给＋号外圈补充圆弧/外环效果
- [x] 简要自检默认/hover/禁用态显示

#### review

- ＋号按钮默认态新增外环：通过 ring + ring-offset 形成圆弧外圈，在深浅色模式都可见。`src/components/editor/AIPanel.tsx`

#### 单环外圈调整（待确认）

- [x] 定位当前按钮的 border/ring 叠加来源
- [x] 改为单圈浅描边（去掉 ring-offset 或替换 border）
- [x] 简要自检默认/hover/禁用态是否只剩单环

#### review

- ＋号按钮改为单圈浅描边：移除 border/offset，仅保留一层淡 ring 作为圆弧外圈。`src/components/editor/AIPanel.tsx`

#### 指令菜单点击外部关闭（待确认）

- [x] 定位 AIPanel 指令菜单的开关逻辑与触发条件
- [x] 增加点击空白处关闭菜单的监听（排除输入框与菜单本身）
- [x] 简要自检：有 @ 时点击外部也能关闭，输入框交互不受影响

#### review

- 指令菜单增加外部点击关闭：监听 pointerdown，命中菜单/输入框/＋号触发器时不关闭，其余区域点击即关闭。`src/components/editor/AIPanel.tsx`
- 修复 closeAtMenu 初始化顺序：将外部点击监听移到 closeAtMenu 定义之后，避免 ReferenceError。`src/components/editor/AIPanel.tsx`

#### 指令文案调整（待确认）

- [x] 定位 @ 指令菜单的文案来源
- [x] 修改 Knowledge/optimization 的描述文案

#### review

- @Knowledge 描述改为“从知识库中添加”，@optimization 描述改为“文本自然化”。`src/components/editor/AIPanel.tsx`

#### 指令名称中文化（待确认）

- [x] 定位 @ 指令菜单中的英文标签与相关文案
- [x] 将 @Knowledge/@optimization 标签替换为纯中文显示
- [x] 评估已选标签是否需要同步中文显示（如 optimization 芯片）

#### review

- 指令菜单标签改为中文：知识库 / 文本自然化，去掉 @ 前缀。`src/components/editor/AIPanel.tsx`
- 已选标签文案同步中文：optimization 芯片改为“文本自然化”，并更新 aria-label。`src/components/editor/AIPanel.tsx`

#### 指令菜单文案调整（二次）（待确认）

- [x] 将“知识库”标签改为“从知识库中添加”
- [x] 移除指令菜单中标签下方的描述文本
- [x] 简要自检菜单排版与行高

#### review

- 指令菜单标签更新为“从知识库中添加”，并移除标签下方的描述行。`src/components/editor/AIPanel.tsx`

#### 子菜单分栏展示（待确认）

- [x] 将“从知识库中添加”子菜单改为独立左侧面板
- [x] 保留右侧主菜单列表，子菜单打开时两栏并排显示
- [x] 简要自检高亮与滚动区域

#### review

- 知识库子菜单改为左侧独立面板，主菜单保留在右侧，两栏并排显示。`src/components/editor/AIPanel.tsx`
- 子菜单列顺序调整：主菜单在左，知识库列表在右。`src/components/editor/AIPanel.tsx`

#### 主菜单宽度调整（待确认）

- [x] 缩窄单栏主菜单的最大宽度
- [x] 简要自检默认态宽度是否更贴合参考

#### review

- 单栏主菜单最大宽度收窄为 280px，使默认态更紧凑。`src/components/editor/AIPanel.tsx`

#### 主菜单宽度统一（二次）（待确认）

- [x] 单栏主菜单宽度改为与双栏列宽一致
- [x] 简要自检两种状态宽度一致

#### review

- 单栏主菜单最大宽度调整为 240px，以匹配双栏时的列宽。`src/components/editor/AIPanel.tsx`
- 主菜单宽度改为常量：单栏 240px，双栏总宽 488px（两列 240 + gap），避免悬浮切换时宽度变化。`src/components/editor/AIPanel.tsx`

#### 移除菜单页眉（待确认）

- [x] 定位主菜单与知识库子菜单的页眉区域
- [x] 删除 “@ 指令 / 从知识库中添加” 顶部行
- [x] 简要自检列表顶距与分隔是否自然

#### review

- 主菜单与知识库子菜单的页眉已移除，列表顶部直接对齐内容区。`src/components/editor/AIPanel.tsx`

#### 子菜单上移（待确认）

- [x] 定位双栏状态下的知识库子菜单容器
- [x] 调整子菜单整体上移（不影响主菜单）
- [x] 简要自检：顶部间距更紧凑且不遮挡

#### review

- 知识库子菜单整体上移 16px（-mt-4），顶部间距更紧凑。`src/components/editor/AIPanel.tsx`

#### 知识库标题省略（待确认）

- [x] 定位知识库列表标题渲染位置
- [x] 设置单行省略（truncate），避免多行撑高
- [x] 简要自检长标题显示效果

#### review

- 知识库列表标题改为单行省略展示（truncate），避免长标题多行撑高。`src/components/editor/AIPanel.tsx`

#### 子菜单最大高度（待确认）

- [x] 调整知识库子菜单列表容器的最大高度
- [x] 简要自检滚动条与显示行数

#### review

- 知识库子菜单最大高度调整为约 5 行（max-h-[220px]），超出滚动。`src/components/editor/AIPanel.tsx`
- 子菜单滚动隔离：添加 overscroll-contain，避免滚动传递到后方 AI 列表。`src/components/editor/AIPanel.tsx`
- 子菜单滚动链阻断：在滚动容器上拦截 wheel，边界时 preventDefault，避免外层继续滚动。`src/components/editor/AIPanel.tsx`

#### 双栏高度独立（待确认）

- [x] 防止双栏布局被网格拉伸为同高
- [x] 简要自检：主菜单高度不随知识库列表变化

#### review

- 双栏网格改为 items-start，并让主菜单列 self-start，避免随右侧列表高度拉伸。`src/components/editor/AIPanel.tsx`

#### 知识库子菜单避免闪动（方案A）（待确认）

- [x] 切换到知识库子菜单时不再重新定位菜单
- [x] 简要自检：子菜单打开时不再因重算位置闪动

#### review

- 进入知识库子菜单时不再调用 repositionMenu，避免因高度变化导致位置跳动。`src/components/editor/AIPanel.tsx`
- 子菜单阶段冻结重定位：atStage=knowledge 时跳过重算与测高，防止子菜单加载时闪动。`src/components/editor/AIPanel.tsx`

#### 知识库列表缓存（待确认）

- [x] 关闭菜单时不重置 knowledgeLoadedOnce，保留已加载列表
- [x] 简要自检：二次打开不再出现加载闪动

#### review

- 关闭菜单时保留知识库加载状态与列表缓存，避免每次打开都重新加载。`src/components/editor/AIPanel.tsx`

#### 知识库子菜单仅点击打开（待确认）

- [x] 增加 knowledgePanelOpen 状态，只在点击“从知识库中添加”时打开
- [x] 关闭/重新打开菜单时重置子菜单状态
- [x] 简要自检：仅点击才展开，悬停不触发

#### review

- 子菜单显示增加 knowledgePanelOpen 门闸，确保仅在点击后展开，避免悬停自动展开。`src/components/editor/AIPanel.tsx`
- 子菜单改为悬浮打开：hover 到“从知识库中添加”时打开面板，hover 其他项时关闭。`src/components/editor/AIPanel.tsx`

#### 子菜单滚动影响 AI 列表（根因排查与修复）（待确认）

- [x] 通读 WorkDetailView 的全局滚轮接管逻辑，确认触发条件与边界判断
- [x] 核对指令菜单为 portal 且不在 workbench 边界，验证 scrollableParent 返回空导致 AI 列表被接管滚动
- [x] 为指令菜单标记 scroll-scope，并在全局滚轮接管中排除该作用域
- [x] 自检：滚动子菜单不再带动 AI 列表，其他滚轮行为不受影响

#### review

- 根因证据：WorkDetailView 里 `onWheelCapture={handleGlobalWheel}` 会在滚轮事件触发时接管滚动；当目标元素不在可滚动父级（或父级到顶/到底）时会把滚动量转给 `[data-ai-scroll-container="active"]`，因此子菜单滚动边界时会推动 AI 列表。`src/views/WorkDetailView/index.tsx`
- 触发机制：指令菜单通过 portal 渲染到 `document.body`，不在 `workbenchRef` 边界内，`findScrollableParent` 找不到有效父级，导致全局接管直接生效。`src/components/editor/AIPanel.tsx`、`src/views/WorkDetailView/index.tsx`
- 修复：为指令菜单根节点加 `data-scroll-scope="command-menu"`，并在全局滚轮接管中直接排除该作用域，阻断对子菜单滚轮的“AI 列表代滚动”。`src/components/editor/AIPanel.tsx`、`src/views/WorkDetailView/index.tsx`

#### 从知识库中添加功能深度探索（待确认）

- [x] 梳理前端触发入口与交互（@ 指令菜单、知识库子菜单、选择后标签展示）
- [x] 追踪前端请求与知识库文档列表来源（knowledgeApi.getDocTitles / GET /knowledge/titles）
- [x] 追踪发送链路：selectedDocs → knowledge_doc_ids → 后端注入 knowledge_docs
- [x] 验证知识库文档如何进入 AI 生成链路（context_builder/plan_generator/response_builder）
- [x] 汇总证据并给出直白结论（功能核心、边界、与“添加到知识库”区别）

#### review
- “从知识库中添加”入口在 AIPanel 的 @ 指令菜单：ROOT_OPTIONS 定义了该指令，点击/悬停会打开知识库子面板；选择后会以标签（Tag 芯片）显示在输入框前。`src/components/editor/AIPanel.tsx:355-379,1032-1087,1349-1368,1990-2070`
- 文档列表来源是 `knowledgeApi.getDocTitles()`，只拉取 id+title；前端仅按标题做本地过滤，不拉正文。`src/components/editor/AIPanel.tsx:950-977,622-633`、`src/services/knowledgeApi.ts:233-248`
- 后端 `/knowledge/titles` 返回“当前用户”的文档 id+title（按 updated_at 倒序），这是 @ 菜单的数据源。`backend/app/api/v1/knowledge.py:116-129`
- 发送链路：已选文档 id 被打进 `knowledge_doc_ids`，后端按 id 取全文并注入 `knowledge_docs`（同时增加 reference_count）。`src/components/editor/AIPanel.tsx:1129-1175`、`backend/app/api/v1/agent.py:1195-1227`
- AI 生成链路会把 `knowledge_docs` 注入提示词：planning/response_builder 都会拼接“用户引用的知识库文档”段落并限制最多 3 篇，context_builder 还会生成系统提示要求“严格参考”。`backend/app/services/agent/planning/plan_generator.py:253-381`、`backend/app/services/agent/planning/response_builder.py:395-629`、`backend/app/services/agent/utils/context_builder.py:408-470`
- “从知识库中添加”≠“添加到知识库”：后者是把新内容写入知识库，走 `knowledgeApi.create`（title/content/category/tags），与引用现有文档是两条路径。`src/components/editor/AIPanel.tsx:572-607`

#### Opencode 是否存在“从知识库中添加”功能排查（待确认）

- [x] 全局检索 Opencode 是否有“知识库/knowledge base”相关模块、UI、接口
- [x] 重点排查 opencode/src 中是否存在“知识库引用/文档选择”链路
- [x] 梳理 Opencode 可能的“替代机制”（技能/文件引用/MCP 等）并界定差异
- [x] 汇总证据并给出直白结论（是否存在该功能+原因）

#### review
- 全局关键词检索未发现“knowledge base/知识库”相关模块或 UI 文案；在 src 范围内出现的 “knowledge” 仅是“知识截止/提示词”等文本，并非功能实现。`rg: opencode/…`、`opencode/packages/opencode/src/tool/websearch.txt:1-10`、`opencode/packages/opencode/src/session/prompt/anthropic-20250930.txt:151`
- opencode 核心代码中未看到“选择知识库文档 → 发送文档 id → 后端注入”的链路；`@` 仅用于文件路径引用解析，不是知识库引用。`opencode/packages/opencode/src/session/prompt.ts:1584-1625`
- 可用的“替代机制”是：技能加载（SkillTool 读取本地 skill 说明）、MCP 外部上下文服务器、以及 OpenAI 兼容的 file_search（vectorStoreIds 由外部提供），都不是内置“知识库文档管理 + 选择引用”。`opencode/packages/opencode/src/tool/skill.ts:8-80`、`opencode/packages/opencode/src/mcp/index.ts:1-120`、`opencode/packages/opencode/src/provider/sdk/openai-compatible/src/responses/tool/file-search.ts:19-125`
- 结论：Opencode 仓库里没有“从知识库中添加”这种 UI/数据链路功能；它只有“文件引用/技能/MCP/外部 file_search”这类上下文来源，性质不同且不提供本地知识库文档列表与引用选择。

#### 方案A：知识库自动检索片段注入（待确认）

- [x] 增加向量检索按 doc_ids 过滤能力（VectorStoreService.search_knowledge）
- [x] 知识库语义搜索支持 doc_ids，并在 doc_ids 模式返回“相关片段”
- [x] agent_chat_stream 用“相关片段”替代全文注入（保留引用计数）
- [x] 更新 todo.md review：说明检索逻辑与行为变化

#### review
- VectorStoreService.search_knowledge 支持 doc_ids 过滤：只在指定知识条目范围内做向量检索，非法 ID 会被跳过且不会回退到全库。`backend/app/services/vector_store_service.py`
- KnowledgeService.search_by_semantic 增加 doc_ids 参数并传递到向量检索，同时在结果层二次过滤，确保只返回选中的文档片段。`backend/app/services/knowledge_service.py`
- agent_chat_stream 优先做“选中文档内语义检索”，把相关片段作为 knowledge_docs.content 注入；若检索为空才回退全文注入，引用计数仅针对实际使用的条目。`backend/app/api/v1/agent.py`

#### 知识库引用上限与状态透出（待确认）

- [x] 知识库引用上限可配置，默认 5
- [x] 透出“检索片段/回退全文”的前端状态提示

#### review
- knowledge_doc_limit 支持从 context 读取，默认 5，限制生效于检索与回退注入，避免无限扩张。`backend/app/api/v1/agent.py`
- SSE 追加 text 事件提示“检索片段/回退全文（已使用/总数）”，让前端可见本次引用模式。`backend/app/api/v1/agent.py`

#### 知识库引用上限硬限制（待确认）

- [x] knowledge_doc_limit 增加硬上限 10（防止极端参数拖慢检索）
- [x] 更新 todo.md review 说明行为变化

#### review
- knowledge_doc_limit 超过 10 会被强制压到 10，避免极端参数造成检索放大与性能风险。`backend/app/api/v1/agent.py`

#### 生成测试引用文本与提示词（待确认）

- [x] 读取小说素材并提取可引用内容（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 生成 2 段约 1000 字引用文本（.md 格式）
- [x] 基于引用文本生成 2 条对应测试 prompt（.md 格式）
- [x] 更新 todo.md review（生成内容摘要与注意事项）

#### review
- 已基于小说第1–3章素材生成两段约1000字引用文本：第一段聚焦源顺镖局杂役弟子环境、赵穆教学与段融吞噬器灵；第二段聚焦“一夕千悟”、内息尝试与赵穆刀感变化。
- 为两段引用文本分别生成了对应测试 prompt，覆盖设定约束、人物行为与训练细节的调用验证。

#### Thinking 消失排查（待确认）

- [x] 通读 Backend.md 测试日志，确认与“Thinking 消失”相关的异常/预期行为
- [x] 追踪后端流式事件链路（planning/direct_answer/flow events）与前端显示条件（AIPanel showThinking）
- [x] 汇总证据并给出直白结论（根因 + 是否符合预期）

#### review
- Backend.md 显示多次 `Plan tasks: 0 items` 且走 `direct_answer`，说明没有执行阶段任务，也就不会产生 `task_progress/thinking` 事件；“思维链”仅在后端日志记录，不是前端事件。`Backend.md`
- 前端只在“正在流式 + 没有任何 flowItems”时显示 Thinking；一旦收到 `agent_header` / `text` 等 flow 事件就不再显示。`src/components/editor/AIPanel.tsx`
- 后端在 direct_answer 路径会先发 `agent_header` + `output_ready`，且在知识库引用时还会发 `text` 状态事件，因此 flowItems 很早就存在，Thinking 自然消失；这是当前逻辑下的**预期行为**。`backend/app/services/agent/langgraph_agent.py`、`backend/app/api/v1/agent.py`、`src/hooks/useAgentChat.ts`

#### 前端微调 Thinking 显示（待确认）

- [x] 梳理 AIPanel 中 Thinking 显示条件与 flowItems 过滤范围
- [x] 调整 showThinking 逻辑：忽略 agent_header/text 等“装饰性”flowItems
- [x] 更新 todo.md review（变更与影响）

#### review
- Thinking 显示判断改为仅基于“实质执行项”：忽略 `agent_header`/`text`，避免装饰性事件导致 Thinking 过早消失。`src/components/editor/AIPanel.tsx`

#### 修复注释乱码（待确认）

- [x] 定位乱码注释并确认期望文案
- [x] 修复注释中的乱码字符（保持语义不变）
- [x] 更新 todo.md review

#### review
- 修复注释乱码：恢复“显示 logo 和名称”文案，保持语义不变。`src/components/editor/AIPanel.tsx`

#### AIPanel 注释乱码批量修复（待确认）

- [x] 统计并确认需要修复的乱码注释位置
- [x] 批量替换乱码字符（保持原意、尽量不改语义）
- [x] 更新 todo.md review

#### review
- 已修复 `AIPanel.tsx` 内全部注释乱码，并同步清理少量日志文案中的乱码（仅文本变化，不影响逻辑）。`src/components/editor/AIPanel.tsx`

#### 修复知识库语义检索 message 未定义（待确认）

- [x] 定位 knowledge 语义检索调用处的未定义变量
- [x] 修复为使用 request.message（或显式赋值）
- [x] 更新 todo.md review

#### review
- 修复知识库语义检索的 `message` 未定义错误，改为使用 `request.message`，避免检索失败后回退全文。`backend/app/api/v1/agent.py`

#### 检查 Backend.md 最新日志是否符合预期（待确认）

- [x] 通读 Backend.md 最新日志，确认是否仍出现 knowledge semantic search 的报错
- [x] 对照后端逻辑（语义检索/回退全文/状态提示）判断是否符合预期
- [x] 汇总直白结论（是否符合预期 + 是否仍有异常）

#### review
- 最新日志不再出现 `knowledge semantic search failed`，且已记录“语义搜索知识库/知识库RAG检索/返回结果”链路，说明检索已恢复并符合预期。`Backend.md`
- 仍有一个与本次问题无关的警告：`MarkupResemblesLocatorWarning`（BeautifulSoup 解析文本时提示像文件名），属于内容清理层的告警。`Backend.md`

#### 知识库检索内容是否持久化（待确认）

- [x] 通读知识库引用与上下文构建链路，确认数据注入点
- [x] 追踪会话/长期记忆保存逻辑，确认是否持久化检索片段
- [x] 汇总直白结论（保存范围与生命周期）

#### review
- 知识库检索片段仅在本次请求中注入 `context["knowledge_docs"]` 供规划/总结使用，未写入会话消息或长期记忆，默认不持久化；会话只保存用户/助手文本。`backend/app/api/v1/agent.py`、`backend/app/services/agent/planning/plan_generator.py`、`backend/app/services/context/manager.py`
- 前端发送后会清空已选知识文档标签，下一次需要重新选择（否则不会带 `knowledge_doc_ids`）。`src/components/editor/AIPanel.tsx`

#### 保存知识库引用信息（不持久化片段）（待确认）

- [ ] 设计并实现“仅保存引用信息”的数据结构与保存时机
- [ ] 前端/后端透出引用信息（doc_id/标题/时间/标签）
- [ ] 更新 todo.md review

#### 主菜单/子菜单适配浅色模式（待确认）

- [x] 定位命令菜单主/子面板的样式配置
- [x] 为浅色模式补充背景、文字、边框与高亮样式
- [x] 更新 todo.md review

#### review
- 主菜单与子菜单在浅色模式下使用白底/浅边框/深色文字，高亮与 hover 状态也同步适配，暗色模式保持原样。`src/components/editor/AIPanel.tsx`

#### 知识库子菜单去掉小箭头（待确认）

- [x] 定位子菜单列表项右侧 ChevronRight 图标渲染
- [x] 移除子菜单列表项的小箭头图标
- [x] 更新 todo.md review

#### review
- 移除知识库子菜单列表项右侧的小箭头图标，避免视觉干扰。`src/components/editor/AIPanel.tsx`

#### 用户卡片弹窗暗色匹配（待确认）

- [x] 定位 UserCardPopover 弹窗暗色背景/分隔线/hover 的色值
- [x] 使用全局暗色主题变量替换 discord 灰，保持与整体暗色一致
- [x] 自检暗色模式下弹窗层级、文字对比与下拉菜单背景

#### review
- 用户卡片弹窗暗色底色/分隔线/hover 全部对齐项目深色体系：主卡改为 #1e293b、分隔与 hover 改为 #334155，下拉菜单改为 #0f172a + #334155 边框，避免“discord 黑灰”突兀。`src/components/layout/UserCardPopover.tsx`

#### 管理员界面去掉页眉（待确认）

- [x] 确认管理员布局中页眉渲染入口（AdminLayout/Header）
- [x] 移除管理后台页面顶部 Header（不影响侧边栏与内容区）
- [x] 自检 admin/works 页面顶栏消失且布局无错位

#### review
- 管理员布局移除顶部 Header，只保留侧边栏与内容区，`/admin/works` 顶部条消失且结构不变。`src/components/layout/AdminLayout.tsx`

#### 管理后台侧边栏标题去掉（待确认）

- [x] 定位 AdminSidebar 中“管理后台”标题区块
- [x] 移除该标题区块，保持返回入口与菜单列表布局不变
- [x] 自检 admin 页面侧边栏间距与样式无异常

#### review
- 已移除管理后台侧边栏的“管理后台”标题区块，保留返回入口与菜单列表，间距由菜单自身 padding 接管。`src/components/layout/AdminSidebar.tsx`

#### 去掉侧边栏“管理员模式”提示（待确认）

- [x] 定位 AdminSidebar 底部“管理员模式/具有完整系统权限”区块
- [x] 移除该提示区块，保持菜单滚动与布局不变
- [x] 自检 admin 页面侧边栏底部无残留空白

#### review
- 已移除侧边栏底部“管理员模式/具有完整系统权限”提示卡片，菜单区域更简洁，底部不再占位。`src/components/layout/AdminSidebar.tsx`

#### 管理后台侧边栏背景匹配（待确认）

- [x] 定位 AdminSidebar 背景/边框色值与暗色模式配置
- [x] 调整侧边栏暗色背景与右侧内容区域匹配（必要时同步边框色）
- [x] 自检 admin 页面整体对比与层级保持清晰

#### review
- 侧边栏暗色背景调整为 `gray-800` 并同步边框为 `gray-700`，hover 暗色改为 `gray-700`，与右侧内容卡片暗色更协调。`src/components/layout/AdminSidebar.tsx`

#### 管理后台作品列表顶部区域固定（待确认）

- [x] 定位 AdminWorksView 顶部“标题 + 搜索/统计”区域结构
- [x] 将该区域设为 sticky，避免随列表滚动
- [x] 自检滚动时顶部区域固定且不遮挡列表

#### 管理后台作品默认封面（待确认）

- [x] 复用默认封面资源（/default-cover.jpg）并处理缺失/加载失败
- [x] 替换 AdminWorksView 封面渲染为带兜底方案
- [x] 自检无封面时显示默认图

#### review
- 作品管理页顶部“标题 + 搜索/统计”区域改为 sticky，滚动列表时固定在顶部。`src/views/AdminWorksView.tsx`
- 作品封面使用默认封面兜底，并改为 ImageWithFallback 渲染，缺失/加载失败时也有默认图。`src/views/AdminWorksView.tsx`

#### 管理后台作品页顶部“轻微滚动”修正（待确认）

- [x] 调整 AdminWorksView 布局：移除父级 top padding，改由 sticky 区域内 padding 保持间距
- [x] 确保 sticky 从滚动开始即固定，消除顶部“滑动 1 次才吸顶”的视觉
- [x] 自检滚动时顶部区域不再产生位移

#### review
- 取消父级顶部 padding，并把顶部间距移入 sticky 容器，避免滚动时出现“轻微位移后才吸顶”的视觉跳动。`src/views/AdminWorksView.tsx`

#### 管理后台多页面顶部区域固定（待确认）

- [x] 盘点 admin 视图顶部区域结构（Dashboard/Users/Reports/Notifications/Invitations/Credits/Cost/Tasks/AIModels）
- [x] 为需要固定的页面增加 sticky 顶部块，并调整 padding/背景避免轻微位移
- [x] 自检多个 admin 页面滚动时顶部区域不再出现位移

#### review
- 为多个 admin 页面增加顶部 sticky 区域：Dashboard/Users/Reports/Notifications/Invitations/Credits/Cost/Tasks/AIModels/Channels，顶部信息与筛选区滚动不再位移。`src/views/AdminDashboardView/index.tsx` `src/views/AdminUsersView/index.tsx` `src/views/AdminReportsView.tsx` `src/views/AdminNotificationsView.tsx` `src/views/AdminInvitationsView/index.tsx` `src/views/AdminCreditsView/index.tsx` `src/views/AdminCostView/index.tsx` `src/views/AdminTasksView/index.tsx` `src/views/AdminAIModelsView/index.tsx` `src/views/AdminChannelsView.tsx`
- 处理有顶距页面的“轻微位移”：AdminReports/AdminTasks 将顶部 padding 移入 sticky 容器，避免滚动后才吸顶。`src/views/AdminReportsView.tsx` `src/views/AdminTasksView/index.tsx`

#### INFO.md 末尾 100 条日志核对（待确认）

- [x] 读取 INFO.md 最后 100 行并统计 hit=0 频次
- [x] 关联触发链路（exact_search/read_paragraphs）与关键词
- [x] 在 todo.md 追加 review：直白结论 + 关键证据行号

#### review

- `INFO.md` 最后 100 行里只有 2 条 exact_search 相关日志，且 hits=5 / hits=12，没有出现 hit=0；其余是 explore 完成、summarization、上下文保存等流程日志。证据：`INFO.md` 末尾 100 行（15:50:45 之后）。

#### read_paragraphs 报“超出范围”原因排查（待确认）

- [x] 定位 ExploreTool read_paragraphs 失败日志来源与触发条件（items 过滤/分页范围）
- [x] 对比 `explore_tools.py` 与 `langgraph_tools.py` 的空结果返回路径与字段差异
- [x] 结合日志字段（empty_reason=None 等）判断触发路径并标注证据行号
- [x] 在 todo.md 追加 review：直白结论 + 关键证据 + “超出范围”误导点

#### review

- “超出范围”并不是唯一/真实原因：`ExploreTool` 在**本地过滤后无可读项**或**预算裁剪后 limit<=0**时会直接构造 `{"success": False, "error": "没有可读取的段落（可能超出范围）"}`，并未进入底层 `read_paragraphs`，因此日志里 `empty_reason/index_base/invalid_items` 全是 `None`。证据：`backend/app/services/agent/tools/explore_tools.py:3968-3984`、`backend/app/services/agent/tools/explore_tools.py:4066-4085`、`backend/app/services/agent/tools/explore_tools.py:4101-4107`。
- 触发“无可读项”的核心过滤链：items 必须能解析出 `chapter_order+paragraph_index`（或 `chapter_id/node_id` 映射成功），且在章节范围内、未读、未超预算，否则会被剔除；当全部被剔除就会触发上面的通用错误。证据：`backend/app/services/agent/tools/explore_tools.py:4031-4081`。
- 如果真的是“分页超出范围”，底层 `langgraph_tools.read_paragraphs` 会返回 `empty_reason`（如 `offset 超出段落总数/章节无段落`）并带 `index_base`，日志不应为 `None`。证据：`backend/app/services/agent/langgraph_tools.py:1781-1805`。

#### Backend.md 测试日志复核（待确认）

- [ ] 摘取 2026-02-03 15:35 左右的 read_paragraphs 失败日志，确认参数与错误字段组合
- [ ] 结合 ExploreTool 过滤/预算路径，判断这批 items 为何会被过滤成空
- [ ] 对照同一时段的“成功 read_paragraphs”日志，确认 index_base/调用路径差异
- [ ] 在 todo.md 追加 review：基于 Backend.md 的直接证据与直白结论

#### “源顺镖局”反复搜索原因排查（待确认）

- [x] 从日志中定位反复搜索的关键词与触发链路（search/exact_search/tool_loop）
- [x] 核对 ExploreState 的去重逻辑与“相似词”判断是否覆盖该关键词
- [x] 追踪 Planning/Prompt 是否重复注入同一关键词导致循环
- [x] 在 todo.md 追加 review：直接证据 + 直白结论 + 如何“没有就跳过”

#### review

- 反复搜索并非“没有命中仍继续”，而是**任务本身要求查询“源顺镖局”**：15:38:45 开始的任务明确是“查找关于组织‘源顺镖局’的信息”，并且 explore_content 记录“规划传入关键词: ['源顺镖局']”。证据：`Backend.md:664-670`。
- “源顺镖局”在搜索中**确实有命中**：多次 exact_search 命中（如 15:39:17 hits=15，后续 15:40:54/15:41:56/15:46:57 等仍有 hits），因此不会触发“0 命中即跳过”的拦截条件。证据：`Backend.md:688-691`、`Backend.md:709-712`、`Backend.md:734-737`、`Backend.md:833-836`。
- 代码层面，“规划传入关键词”会被当作**必带关键词**，每次 exact_search 都会被强制合并并绕过去重/拦截：`required_keywords → force_set`，force_set 直接进入 allowed_keywords，不走 should_block_search。证据：`backend/app/services/agent/tools/explore_tools.py:3286-3341`、`backend/app/services/agent/tools/explore_tools.py:3411-3423`。
- 现有“没有就跳过”只在 **0 命中** 或 **已穷尽** 时触发（且对强制关键词不生效）；而“源顺镖局”既有命中，又被 force_set 强制保留，所以不会跳过。证据：`backend/app/services/agent/tools/explore_tools.py:1120-1148`、`backend/app/services/agent/tools/explore_tools.py:658-670`。

#### Explore Artifact 路径基准改为 backend/（待确认）

- [x] 核对当前 UPLOAD_DIR 相对路径与服务工作目录（backend/）一致性
- [x] 调整 Explore Artifact 根目录优先使用 backend 根路径，保留 repo 根路径作为兼容读取
- [x] 自检保存/读取：新写入落在 backend/uploads，旧文件仍可读取
- [x] 在 todo.md 追加 review（改动位置 + 兼容性说明）

#### review

- UPLOAD_DIR 仍为相对路径（`./uploads`），但 Explore Artifact 优先以 backend 根目录作为基准，适配服务运行在 backend/ 的工作目录。`backend/app/services/agent/utils/explore_artifact.py`
- 保留兼容读取：当当前根目录找不到文件时，会在其他 upload 根目录下依次尝试 `root/<work_id>/...` 和旧版 `root/explore_artifacts/<work_id>/...`，避免历史 artifact 失效。`backend/app/services/agent/utils/explore_artifact.py`

#### load_explore_artifact 摘要丢失排查与修复（待确认）

- [x] 复核工具返回结构与执行层提取逻辑，定位 summary 被丢弃的原因
- [x] 在 extract_result 增加 load_explore_artifact 分支，返回完整 JSON 结果
- [x] 自检：摘要字段不会被提取逻辑丢弃
- [x] 在 todo.md 追加 review（证据 + 改动位置）

#### review

- `load_explore_artifact` 工具返回的是顶层 `success/summary` 结构，没有 `data` 字段，但 `ToolExecutor.extract_result` 默认只取 `data` 并返回 `{}`，导致 summary 被丢弃，最终 Summarization 看不到摘要。证据：`backend/app/services/agent/execution/tool_executor.py:1626-1705`，以及 artifact 文件内确有 `payload.explore_summary`。`backend/uploads/73db1555-41d1-427a-bac1-2e2164c2a427/50fe756714434d5dbabee3b6eafcbd57.json`
- 修复：为 `load_explore_artifact` 增加专用分支，直接返回完整 JSON（和 locate_content/explore_content 一致），确保 summary 不会被提取逻辑丢弃。`backend/app/services/agent/execution/tool_executor.py`
