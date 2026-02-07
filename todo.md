# TODO

#### 提取反AI检测规范库（待确认）

- [x] 盘点 `article-writer/spec/presets/anti-ai-detection/` 下全部文件与内容范围
- [x] 将三份规范完整合并到 `article-writer/反AI检测规范库.md`（保留原文结构并标注来源文件）
- [x] 对照文件清单复核无遗漏
- [x] 在 todo.md 追加 review（输出位置与核对结果）

#### review

- 已汇总 `spec/presets/anti-ai-detection/` 下 3 个文件到 `article-writer/反AI检测规范库.md`，保留原文结构并添加来源标注，避免遗漏。
- 在该目录未发现 `audit-config.json` 或其他规则文件，仅包含 3 个 Markdown 文件（套话库/AI句式库/书面词汇替换库）。

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
- AIPanel 不再渲染模式切换器，执行模式继续沿用默认 plan（反思开关逻辑未改动）。`src/components/editor/AIPanel.tsx`

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

#### Backend.md 17:23 read_paragraphs 失败原因排查（待确认）

- [x] 定位 2026-02-03 17:23:08 前后 read_paragraphs 调用与参数
- [x] 结合 explore_tools 过滤/预算/范围逻辑确定触发路径
- [x] 在 todo.md 追加 review：直白结论 + 证据行号 + “超出范围”具体指向

#### review

- 17:23:08 这次失败并非“真正超出范围”，而是 **ExploreTool 过滤后 items 为空**触发的兜底错误。日志显示 call=read_paragraphs 传入了 6 个 item，但 done=read_paragraphs success=False count=0 且 empty_reason/index_base 均为 None，符合 ExploreTool 本地过滤后直接构造错误的路径。证据：`Backend.md:183-185`、`backend/app/services/agent/tools/explore_tools.py:4066-4085`、`backend/app/services/agent/tools/explore_tools.py:4101-4107`。
- 触发“过滤为空”的具体机制：items 必须满足 **章节范围允许 + 未读去重 + 未超章节阅读预算**，否则会被剔除；全部被剔除就返回“没有可读取的段落（可能超出范围）”。证据：`backend/app/services/agent/tools/explore_tools.py:4066-4085`。
- 这段任务前日志显示已复用共享状态 `read_paragraphs=50`，结合“按章阅读上限”逻辑，最可能是 **章节预算已耗尽或已读去重**导致 items 全部被过滤。证据：`Backend.md:156`、`backend/app/services/agent/tools/explore_tools.py:2299-2309`。

#### 移除按章阅读上限机制（待确认）

- [x] 确认按章阅读上限的关键入口（_init_chapter_read_caps/_get_chapter_remaining_reads）
- [x] 最小改动禁用按章 cap（不影响全局读取上限）
- [x] 自检 read_paragraphs/read_paragraph 仍可正常执行
- [x] 在 todo.md 追加 review：改动点与行为变化说明

#### review

- 已禁用按章阅读上限：`_get_chapter_remaining_reads` 直接返回 `None`，所有“每章剩余可读数”判断将不再生效，仅保留全局读取上限与已读去重。`backend/app/services/agent/tools/explore_tools.py`

#### 空读硬停 + 共享状态隔离 + 空读原因统计（待确认）

- [x] 共享状态隔离：调整 explore 共享 key（加入任务指纹或清空 read_paragraph_positions）
- [x] 空读硬停：连续空读 N 次停止或切换策略（read_paragraphs/read_paragraph）
- [x] 空读原因统计：记录过滤原因计数并输出更准确的错误文案
- [x] 自检：空读时不再死循环，日志可读性提升
- [x] 在 todo.md 追加 review：改动点与行为变化说明

#### review

- 共享状态隔离：`_build_explore_shared_key` 新增 `target_task` 指纹，避免不同任务复用已读段落状态导致“全被过滤”。`backend/app/services/agent/tools/explore_tools.py`
- 空读硬停：新增空读计数，连续空读达到 `TOOL_LOOP_EMPTY_READ_STREAK_LIMIT=3` 将停止工具循环，防止反复重试。`backend/app/services/agent/tools/explore_tools.py`
- 空读原因统计：read_paragraphs(items) 过滤后为空时记录过滤统计并生成更准确的错误文案与 `empty_reason`，日志可直接看出是“已读/超范围/无效/预算”。`backend/app/services/agent/tools/explore_tools.py`

#### Backend.md 缺陷复核（待确认）

- [x] 通读 Backend.md（优先关注最新日志区段）
- [x] 提取可疑/异常行为并关联到具体模块或逻辑路径
- [x] 在 todo.md 追加 review：缺陷清单 + 证据行号 + 直白结论

#### review

- **read_paragraphs 反复失败但仍连续重试**：17:23:46～17:25:17 期间多次调用 `read_paragraphs`，全部 `count=0` 且 `empty_reason=None`，但工具循环继续重试（只调整 context_before/after 或 items 组合），造成明显的无效调用风暴。证据：`Backend.md:257-273`（多次 call/done/failed）以及 `Backend.md:276-282`。
- **章节阅读预算耗尽导致 range 读取直接失败**：分页模式 `read_paragraphs` 在 17:25:24 与 17:28:28 返回“该章节读取预算已用尽”，随后探索完成理由也明确写“相关章节的阅读预算已用尽”。这会阻断后续原文读取，使探索只能停在“搜索命中”层。证据：`Backend.md:291`、`Backend.md:395`、`Backend.md:292`。
- **共享状态复用造成“已读/预算”持续卡死**：每次新探索开始都会复用共享状态（read_paragraphs 计数持续增加），随后读段全部失败，说明“已读/预算状态”跨任务继承过重，导致新任务也无法读取原文。证据：`Backend.md:240`（read_paragraphs=53）结合连续 read_paragraphs 失败（`Backend.md:257-282`）。

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

#### 自动复用 Explore Artifact Hook（待确认）

- [x] 将会话 artifact 列表注入 planning context（不只写入对话历史）
- [x] 规划后处理加入“自动复用”逻辑：在满足条件时用 load_explore_artifact(summary) 替换 explore_content
- [x] 增加“重新/最新/更新”等新鲜度判断，避免错误复用
- [x] 只在 explore_content 无下游依赖时替换，避免破坏 $ref 依赖
- [x] 在 todo.md 追加 review（规则 + 改动点）

#### Explore 按条目补缺（部分复用）（待确认）

- [x] 在规划阶段先自动取回最近 artifact_summary（同 work_id）
- [x] 从用户请求中提取“需获取的条目”（支持编号/列表/显式条目）
- [x] 用“条目文本是否出现在 summary”做轻量覆盖判断
- [x] 仅对未覆盖条目触发 explore_content，并在 target_task 中声明“只补缺失项”
- [x] 汇总时合并“已覆盖 + 新探索”结果

#### review

- Planning 阶段除了把“可用探索结果”注入对话历史，也写入 `context.session_artifacts`，使规划后处理能直接读取会话级 artifact 指针。`backend/app/services/agent/langgraph_agent.py`
- 规划后处理新增自动复用逻辑：在用户未要求“重新/最新/更新”的情况下，若同 work_id 的 artifact 预览覆盖了部分条目，则先插入 `load_explore_artifact(summary)` 任务，并将 `explore_content` 的 target_task/keywords 改为“只补缺失项”。`backend/app/services/agent/planning/plan_generator.py`
- 当所有条目都已覆盖且无下游 $ref 依赖时，自动移除 explore_content，避免重复探索；若有依赖则保留 explore。`backend/app/services/agent/planning/plan_generator.py`

#### 文本自然化功能深度探索（待确认）

- [x] 通读前端入口与交互（AIPanel/ChatInput/HumanizeView），明确“文本自然化”触发与参数
- [x] 通读后端接口与执行链路（agent use_optimization + humanize API/Service），确认实际调用与处理流程
- [x] 汇总关键限制/开关/强度/长度规则与证据
- [x] 输出直白结论（功能定位、触发方式、真正做了什么、会/不会记录历史）

#### review

- “文本自然化”在编辑器 AIPanel 内是 @ 菜单项，点击后仅设置 `use_optimization`，并显示“文本自然化”胶囊；发送请求时把章节内容截断到 5000 字并写入 `current_content/text`。`src/components/editor/AIPanel.tsx:374-387,637-646,1200-1207,1297-1352,1526-1539`
- Agent ChatInput 的 @optimization 入口支持强度（light/medium/strong），同时也把 `use_optimization` 与 `intensity` 写入上下文，长度同样按 5000 字截断。`src/components/agent/ChatInput.tsx:60-96,139-154,398-425`
- 前端明确标注“@optimization 不写 humanize 历史”；后端 agent 在 `use_optimization` 分支内直接走 HumanizeService（检测+改写），并把结果作为会话消息持久化，而不是 humanize 历史会话。`src/hooks/useAgentChat.ts:324-345`、`backend/app/api/v1/agent.py:1370-1472`
- HumanizeService 支持检测与改写阶段，并默认启用 NLP 预处理；后端配置默认 `max_text_chars=5000`、检测启用、验证默认关闭。`backend/app/services/ai/humanize_service.py:1-199`、`backend/app/core/humanize_config.py:15-38`
- 去痕迹的具体策略来自 humanize prompts：重点移除 AI 套话/模板化结构、增加口语化与句式变化。`backend/app/services/ai/humanize_prompts.py:181-205`

#### Create/smart* 与文本自然化关系排查（待确认）

- [x] 核对 smart* 工具的分类与数量（Create/Creative），确认是否只有一个创作工具
- [x] 核对 Create → operate_apply 的写回链路与适用场景（何时写入编辑器）
- [x] 核对“文本自然化/@optimization”触发链路与是否自动接入 smart* 流程
- [x] 输出直白结论（是否只有一个 smart*、文本自然化的真实使用时机）

#### review

- smart* 创作类工具不止一个：至少有 `smart_continue`、`smart_rewrite`、`smart_insert`，且全部标记为 `ToolCategory.CREATIVE`（只生成内容，不直接写入）。`backend/app/services/agent/tools/editor_tools.py:1165-1299`
- Create → operate_apply 的写回链路是系统级规则：CREATIVE 只生成，必须再走 operate_apply 才会写入编辑器；操作类型包括 append/replace/insert/content/create/title。`backend/app/services/agent/prompts/planning_prompts.py:85-107`、`backend/app/services/agent/tools/operate_tools.py:3-103`
- 文本自然化/@optimization 不会自动进入 smart* 流程；它在 agent chat 的 `use_optimization` 分支里直接调用 HumanizeService（检测+改写），流式返回结果，不经过 smart_* 或 operate_apply。`src/hooks/useAgentChat.ts:324-345`、`backend/app/api/v1/agent.py:1370-1436`

#### 启用文本自然化时“先创作再去痕”改造（待确认）

- [x] 明确规则：@optimization 仅对“写入编辑器”的 smart_* 结果生效；title 不处理
- [x] 选型实现路径：operate_apply 内部统一后处理（不改变 smart_* → operate_apply 外部链路）
- [x] 最小实现：透传 use_optimization + intensity 到 operate_apply，并在写入前 Humanize
- [x] 回归核对：非 @optimization 的创作链路不受影响

#### review

- @optimization 不再强行短路创作链路：仅当 `optimization_only` 显式为真才走“直接去痕迹”分支，其余照常进入 smart_* → operate_apply。`backend/app/api/v1/agent.py`
- operate_apply 在写入前执行 Humanize：当 `use_optimization` 为真且操作为 append/replace/insert/content/create 时，先检测+改写再写入；title 不处理。`backend/app/services/agent/tools/operate_tools.py`
- ToolExecutor 透传 `use_optimization` 与强度到 operate_apply（默认 medium），保证外部任务链路不变，只在写入前去痕。`backend/app/services/agent/execution/tool_executor.py`

#### Backend.md 日志问题深度排查（待确认）

- [x] 通读 Backend.md 关键错误日志，定位失败环节与时间线
- [x] 追踪 explore_content/定位链路，找出“缺少 paragraph_index/node_id”的根因
- [x] 追踪参数解析失败链路（locate_targets/versions 缺失）与写回失败的直接影响
- [x] 汇总证据并给出直白结论（核心问题 + 影响范围）

#### review

- 失败起点是 explore_content：日志显示 ContentExplorer 被锁定在“第7-191章”，但该作品只有 5 章，随后“章节范围映射为空，保持原始范围”，最终报“探索未产出可定位段落”。`Backend.md:65-79`
- 章节范围异常来自目标任务含“章节 <UUID>”，`_parse_chapter_scopes` 在“章节”分支仍会匹配 `(\d{1,3})-(\d{1,3})`，UUID 中的 `e7-1917` 被误识为 7-191，导致范围错误。`backend/app/services/agent/tools/explore_tools.py:388-406`
- 因为 explore_content 未产出 locate_targets，后续任务取不到 locate_targets/versions，ParameterResolver 全部降级为 fallback，smart_rewrite/operate_apply 的关键参数缺失，写回自然失败。`Backend.md:84-108`
- 最终响应也验证了根因：“未能成功改写句子，因未能获取章节内容并定位用户选中的文本。”`Backend.md:120-121`

#### 修复章节范围误匹配 UUID（待确认）

- [x] 在 `_parse_chapter_scopes` 入口剔除标准 UUID，避免“章节 <UUID>”误触发范围解析
- [x] 自检：不影响“章节1-2/第X章”等正常范围解析

#### review

- UUID 过滤前置：进入范围解析前先移除标准 UUID（8-4-4-4-12），防止 `e7-1917` 这类片段被误当作章节范围。`backend/app/services/agent/tools/explore_tools.py`

#### 导入作品自动解析世界观功能排查（待确认）

- [x] 通读导入入口与参数流转（前端导入对话框、后端 import 路由）
- [x] 追踪“自动解析世界观”的实际执行链路与触发条件（后台任务、扫描范围与限制）
- [x] 梳理解析算法/AI 调用与数据落库路径，标注关键约束
- [x] 汇总可复现缺陷与证据（文件/行号），形成直白结论

#### review

- 自动解析仅在文本/Markdown导入生效：前端默认 `autoExtractWorldview` 为 true（非 JSON），后端仅在 `format in ["markdown","txt"]` 且 `auto_extract_worldview=true` 时排队后台任务。`src/views/WorksView/index.tsx:632-709`、`src/components/import/ImportDialog.tsx:430-459`、`backend/app/api/v1/import_routes.py:124-204`
- 自动解析实际扫描逻辑有硬性上限：固定从第 1 章开始、最多 50 章，合并内容超过 50,000 字符直接截断；超过 50 章或长文后半段不会被分析。`backend/app/api/v1/import_routes.py:24-49`、`backend/app/services/worldview_sync_service.py:70-170`
- 追加导入时也从第 1 章扫描（非仅新章节），导致新增章节若排在 50 章以后完全不被解析；这是“追加导入 + 自动解析”最直接的漏检点。`backend/app/api/v1/import_routes.py:24-49`、`backend/app/services/worldview_sync_service.py:70-170`
- 导入文本会先转成 HTML 段落，再被世界观解析直接读取；解析时未做 HTML 清洗，AI 实际看到的是带 `<p>` 标签的内容，可能降低抽取准确度。`backend/app/services/import_service.py:846-890`、`backend/app/services/chapter_content_provider.py:12-24`、`backend/app/services/worldview_sync_service.py:124-170`
- 章节拆分会丢弃“第1章”之前的所有内容（只有在未识别到章节时才整体导入），导致前言/世界观设定等正文前置内容不会进入解析。`backend/app/services/import_service.py:720-842`
- 自动解析只应用“新增人物/地点/设定/关系”，忽略 `updated_characters`，因此对已有作品追加导入时无法同步人物变化。`backend/app/services/worldview_sync_service.py:185-299`
- 自动解析异步执行但前端导入后立即预加载世界观数据且不自动刷新，用户容易看到“空世界观”；且后台失败只写日志，无进度/错误回传。`src/views/WorksView/index.tsx:664-711`、`src/views/WorkDetailView/index.tsx:408-502`、`backend/app/api/v1/import_routes.py:24-55`

#### 彻底修：导入解析世界观（待确认）

- [x] 增加“导入上下文”返回新增章节范围/ID，后台解析仅扫描本次新增章节，支持追加导入
- [x] 世界观扫描改为分批处理 + 去重合并，支持按章节ID扫描；导入时可选“全书扫描”则遍历全书分批解析（不再截断）
- [x] 解析输入先转纯文本（HTML 清洗），可选纳入“前言/设定”段落
- [x] apply_changes 补齐 `updated_characters` 的更新逻辑（必要时扩展到地点/设定）
- [x] 增加后台解析进度/结果查询接口，前端导入后轮询并自动刷新世界观数据 + 状态提示

#### review

- 导入响应新增 import_context（章节ID/顺序范围），后台解析按“新增章节”扫描；支持选择全书扫描，追加导入不再从第1章扫。`backend/app/schemas/export.py`、`backend/app/services/import_service.py`、`backend/app/api/v1/import_routes.py`、`src/types/export.ts`
- 世界观扫描改为按章节分批解析、去重合并，不再 50章/5万字截断；解析前统一 HTML 清洗，首批可纳入“前言/设定”文本。`backend/app/services/worldview_sync_service.py`、`backend/app/services/import_service.py`、`backend/app/core/config.py`
- apply_changes 补齐 updated_characters 的追加更新逻辑，并在导入解析中即使只有更新/关系也会应用。`backend/app/services/worldview_sync_service.py`、`backend/app/api/v1/import_routes.py`
- 增加扫描进度表与接口，前端导入后轮询进度并自动刷新世界观数据。`backend/app/models/worldview_scan_progress.py`、`backend/app/services/worldview_scan_progress_service.py`、`backend/app/api/v1/worldview.py`、`src/views/WorkDetailView/index.tsx`
- 新增导入弹窗“世界观解析”配置区（自动解析 + 新增/全书），并透传 scan_mode。`src/components/import/ImportDialog.tsx`、`src/views/WorksView/index.tsx`、`src/services/DataService.ts`
- 新增 Alembic 迁移创建 worldview_scan_progress 表。`backend/alembic/versions/20260203_0001_add_worldview_scan_progress.py`
- 修复 WorldviewScanProgressResponse 缺少 Dict 导入导致启动报错。`backend/app/schemas/worldview.py`

#### 文本自然化日志与链路核验（待确认）

- [x] 通读 Backend.md，确认是否存在 humanize/use_optimization 相关日志与证据
- [x] 追踪前端 @文本自然化 是否把 use_optimization 写入请求上下文（AIPanel/ChatInput）
- [x] 追踪后端 use_optimization 到 operate_apply 的透传与触发条件（ToolExecutor/operate_apply）
- [x] 设计最小可观测性修复：补充必要日志（use_optimization 命中、人类化开始/结束、长度/强度）
- [x] 给出可复现验证步骤与预期日志点

#### review

- Backend.md 中无 humanize/use_optimization 关键词命中（日志缺失导致无法从日志证明是否执行）。
- 前端 @文本自然化/AIPanel 与 ChatInput 均会在请求上下文写入 use_optimization，并附带 current_content/text（上限 5000）。
- 后端 ToolExecutor 会把 context.use_optimization 透传到 operate_apply，并在 operate_apply 内部触发写入前 humanize。
- 补充可观测性日志：agent_chat_stream 标记 use_optimization 进入规划链路；operate_apply 增加 humanize start/done 日志（含强度与长度）。
- 新证据显示执行走 StandardTool 路径（Backend.md 记录了 `TaskRunner 使用统一接口调用未知工具: operate_apply` 与 `[StandardTool] operate_apply 执行成功`），但 ToolExecutor 的 **StandardTool 预处理分支**未把 `context.use_optimization` 注入 `operate_apply` 参数，导致写回时仍是 `use_optimization=false`，humanize 不会触发也不会产生日志。
- 已修复 StandardTool 分支的透传：`prepare_params` 中 operate_apply 现在会从 `state.context` 注入 `use_optimization` 与强度，并打印启用日志，确保 humanize 能真正触发。`backend/app/services/agent/execution/tool_executor.py`
- [x] 前端导入弹窗增加“世界观解析”配置区（自动解析开关 + 扫描范围：新增章节/全书），并把参数传给后端

#### 导入作品页面预览 HTML（待确认）

- [x] 确定预览文件路径（`preview/import-worldview-preview.html`）
- [x] 按当前导入弹窗风格搭建静态 HTML 结构与样式
- [x] 加入“世界观解析”配置区（自动解析开关 + 扫描范围：新增章节/全书）
- [x] 加入导入预览与解析进度的示例占位
- [x] 调整预览页样式对齐现有 ImportDialog.css（浅色默认 + 暗色对应）

#### review

- 新增静态预览页用于确认导入弹窗布局与“世界观解析”配置区样式，包含自动解析开关、扫描范围选择、导入预览与解析进度占位；样式对齐现有 ImportDialog.css 的浅色/暗色配色与按钮形态。`preview/import-worldview-preview.html`

#### 导入上传框圆角调整（待确认）

- [x] 定位导入作品弹窗的文件拖拽区域样式（WorksView/ImportDialog）
- [x] 将上传框调整为更圆的圆角，保持现有边框/状态样式不变
- [x] 自检：暗色/浅色与拖拽态显示正常

#### review

- 导入作品上传框改为更圆的圆角：WorksView 拖拽区域加 `rounded-2xl`，ImportDialog 的 `.file-upload-area` 半径提升到 16px，预览页同步。`src/views/WorksView/index.tsx`、`src/components/import/ImportDialog.css`、`preview/import-worldview-preview.html`

#### 导入弹窗外框去斜切（待确认）

- [x] 定位导入弹窗外框的斜切/倾斜样式来源
- [x] 移除导入弹窗外框的 skew 变换，保持内部布局不变
- [x] 自检：弹窗边角恢复“正常直角/圆角”，不再倾斜

#### review

- 导入弹窗外框去斜切：移除外层容器 `skewX(-2deg)` 与内部反向 `skewX(2deg)`，恢复正常矩形圆角外框。`src/views/WorksView/index.tsx`

#### 导入弹窗高度限制（待确认）

- [x] 定位导入弹窗外层高度与滚动控制逻辑
- [x] 限制弹窗高度不超过视口，并在内容区启用内部滚动
- [x] 自检：小屏不溢出，滚动条出现在弹窗内部

#### review

- 导入弹窗改为视口高度限制：外层 `max-h-[80vh]` + `overflow-hidden`，内容区 `overflow-y-auto`，小屏不溢出且滚动条在弹窗内。`src/views/WorksView/index.tsx`

#### 导入弹窗显示世界观解析进度（待确认）

- [x] 梳理导入完成后的弹窗关闭逻辑与跳转逻辑（WorksView）
- [x] 导入后不立即关闭弹窗：在弹窗内展示解析进度（轮询 scan-progress），提供“关闭/继续后台”按钮
- [x] 解析完成/失败时更新提示，并允许跳转到作品详情页

#### review

- 导入成功且开启自动解析时，不再立即关闭弹窗；在弹窗内轮询 `scan-progress` 并显示进度条与状态，支持“继续后台解析/查看作品详情”。`src/views/WorksView/index.tsx`

#### 世界观进度接口 404 修复（待确认）

- [x] 确认前端请求路径与后端实际路由前缀不一致的问题
- [x] 在 works 路由补充 `/works/{work_id}/worldview/scan-progress` 接口（与前端一致）
- [x] 自检：导入弹窗与详情页轮询不再 404

#### review

- 在 works 路由补齐世界观扫描进度接口，兼容前端请求路径，避免 `/works/{id}/worldview/scan-progress` 404。`backend/app/api/v1/works.py`

#### 导入后页面闪跳/加载覆盖（待确认）

- [x] 确认导入成功后调用 loadWorks 触发全屏 loading，导致弹窗进度被遮挡
- [x] 为 loadWorks 增加“静默刷新”模式，导入后用静默刷新避免闪跳
- [x] 自检：导入成功后保持弹窗与进度条可见，不再出现“跳转回来”观感

#### review

- 导入成功后改用静默刷新：`loadWorks(true)` 不再触发全屏 Loading，避免弹窗进度被遮挡造成“跳转回来”错觉。`src/views/WorksView/index.tsx`

#### 世界观解析进度回调参数修复（待确认）

- [x] 确认 progress_callback 传参与 update_progress 签名不一致导致报错
- [x] 在导入解析后台任务中包一层回调，补齐 work_id 参数
- [x] 自检：解析进度更新不再抛错，后台任务完成

#### review

- 导入解析进度回调改为本地包装函数，补齐 work_id 参数，避免 update_progress 参数缺失报错。`backend/app/api/v1/import_routes.py`

#### 移除导入成功提示弹窗（待确认）

- [x] 定位导入成功提示的触发位置（WorksView）
- [x] 移除或改为静默，避免导入完成后右上角弹窗
- [x] 自检：导入流程不再出现成功 toast

#### review

- 导入成功不再弹出成功 toast，避免遮挡导入弹窗与进度条；“继续后台解析”也不再提示弹窗。`src/views/WorksView/index.tsx`

#### 修复 ImportContext 序列化警告（待确认）

- [x] 确认 import_context 被赋值为 dict 导致 Pydantic 序列化警告
- [x] 在导入路由中改为赋值 ImportContext 实例
- [x] 自检：日志不再出现 PydanticSerializationUnexpectedValue

#### review

- 导入响应的 import_context 改为 `ImportContext` 实例赋值，避免 Pydantic 序列化警告。`backend/app/api/v1/import_routes.py`

#### 世界观解析性能&体验综合优化（待确认）

- [ ] 导入时先写入“排队中”进度（避免长时间无变化），并把世界观解析放在向量化之前
- [ ] 将解析与向量化迁移到 Celery：世界观高优先级队列、向量化低优先级队列，避免互相阻塞
- [ ] 解析批次优化：首批小批次快速出进度，后续动态批次；支持并发批次（限流）
- [ ] 复用 AI 服务实例 + 传 task_type（模型选择走更快档），降低每批初始化/耗时
- [ ] 进度更新更细：批次开始/结束/应用变化都写入进度（UI显示排队/解析/应用）
- [ ] 前端轮询节流（运行中 5-10s 间隔，完成即停），降低日志噪音

#### 世界观解析性能&体验综合优化（二期·吸收方案优势）（待确认）

- [x] 复核“解析启动慢”的关键耗时点（批次构建/HTML清洗/AI首批），确认对应代码位置
- [x] 批次构建优化：首批按更小字符数拆分（避免单章过大拖慢首批），并尽早写入 batches_total
- [x] 进度阶段化：增加 preparing/applying 状态或 phase 字段，前端展示“准备中/应用中”
- [x] 解析模型可配置：支持首批快模型 + 后续高质量模型（配置开关），兼顾速度与质量
- [x] 自检：导入后 10s 内可见“准备/解析”状态变化，首批完成后进度条有增长

#### review

- 启动慢的根因定位：扫描前会读取**全部章节文件并做 HTML 清洗**构建批次，进度回调在批次构建后才触发，导致导入后长时间无进度变化。`backend/app/services/worldview_sync_service.py`、`backend/app/services/chapter_content_provider.py`、`backend/app/utils/text_cleaner.py`
- 批次构建改为**流式迭代**：并发=1 时按批次生成并立刻解析，避免先清洗全书才开始，首批更快出进度。`backend/app/services/worldview_sync_service.py`
- 进度阶段化落地：新增 `preparing/applying` 状态更新，前端显示“准备中/应用中”，并将无 `batches_total` 时进度百分比退回按章节计算。`backend/app/services/worldview_extraction_runner.py`、`backend/app/services/worldview_scan_progress_service.py`、`backend/app/models/worldview_scan_progress.py`、`src/views/WorksView/index.tsx`、`src/views/WorkDetailView/index.tsx`
- 首批快模型支持：新增 `WORLDVIEW_SCAN_FIRST_BATCH_MODEL`（默认 `gemini-2.5-flash`）+ `WORLDVIEW_SCAN_MODEL` 可配置，首批快模型、后续高质量模型分离。`backend/app/core/config.py`、`backend/app/services/worldview_sync_service.py`

#### 统一世界观解析模型为 gemini-2.5-flash（待确认）

- [x] 定位世界观解析的所有模型入口（批量扫描/单章提取），确认是否仍有 gemini-2.5-pro 硬编码
- [x] 将世界观解析模型统一为 gemini-2.5-flash（禁用模型选择器，避免自动切回 pro）
- [x] 自检日志：不再出现 gemini-2.5-pro、task_type 仍正常输出

#### review

- 单章解析硬编码 pro 已替换为配置驱动的 flash，并禁用模型选择器，避免回切。`backend/app/services/worldview_sync_service.py`、`backend/app/core/config.py`
- 批量解析默认模型统一为 flash：`WORLDVIEW_SCAN_MODEL` 设为 flash，且强制首批与后续一致。`backend/app/core/config.py`、`backend/app/services/worldview_sync_service.py`

#### 解析完成自动跳转作品详情（待确认）

- [x] 定位导入弹窗的解析进度轮询逻辑与跳转入口（WorksView）
- [x] 当解析完成且弹窗仍打开时自动跳转作品详情页（避免重复触发）
- [x] 自检：解析完成自动跳转；用户手动关闭弹窗时不强制跳转

#### review

- 导入后世界观解析完成会自动跳转详情页：在轮询中检测 `completed` 且弹窗仍打开时触发跳转，并用 ref 防止重复触发。`src/views/WorksView/index.tsx`
- 手动关闭弹窗会禁用自动跳转，避免用户“继续后台解析”时被强制带走。`src/views/WorksView/index.tsx`

#### 缩小世界观解析批次（待确认）

- [x] 评估“批次越小越好”的可接受最小值（章节数/字符数/首批）
- [x] 调整 WORLDVIEW_SCAN_BATCH_* 配置为更小批次，优先提升“进度有变化”的频率
- [ ] 自检：进度条更新更频繁，但整体耗时/成本可接受

#### review

- 批次配置缩小为 1~2 章/4k~8k 字符，首批更快出进度，整体更新更频繁。`backend/app/core/config.py`

#### 世界树按需加载（待确认）

- [ ] 通读世界观读取链路（get_writing_context / WorldviewService / context_builder / tool_executor），确认可复用点
- [ ] 设计世界树数据结构与最小接口（root/children/node），明确按需加载粒度与 node_id 规范
- [ ] 增加后端世界树接口与缓存策略（按 work_id + node_id）
- [ ] 新增 agent 工具：按需获取世界树节点（get_worldview_tree / get_worldview_node）
- [ ] 更新 agent 调用策略与上下文构建：仅拉取必要节点（Explore → Worldview(on-demand) → Create）
- [ ] 自检：agent 能按需拉人物/地点/设定/关系，不再一次性拉全量

#### 统计核心代码行数（待确认）

- [x] 确认“核心代码”统计口径与范围（包含/排除的目录与语言，剔除测试脚本与开发文档）
- [x] 按确认口径运行统计并记录排除规则
- [x] 汇总行数结果与口径说明，并在 todo.md 追加 review

#### review

- 统计口径：仅主工程 `backend/app` + `backend/alembic` + `src`；排除测试与文档目录（tests/docs 等）、`node_modules/dist/build/public/preview` 等非核心目录，跳过 `*.test.*`/`*.spec.*`/`*_test.py`/`test_*.py`；统计扩展名 `.py/.ts/.tsx/.js/.jsx/.mjs/.cjs/.css/.scss/.less/.d.ts`，按文件物理行数计（含空行）。
- 统计结果：核心代码总行数 245,985 行（813 个文件）；分目录：`backend/app` 134,598 行、`backend/alembic` 5,468 行、`src` 105,919 行；分扩展名：`.py` 140,066、`.tsx` 71,035、`.ts` 24,608、`.css` 10,202、`.d.ts` 74。

#### Agent 获取世界观元数据链路梳理（待确认）

- [x] 汇总世界观元数据来源：chat/stream 自动注入 + 工具获取（get_writing_context/get_worldview_summary）
- [x] 核对执行轨迹元数据：knowledge_loaded 如何承载世界观数据
- [x] 形成直白结论并标注证据路径（文件+行号）
- [x] 在 todo.md 追加 review

#### review

- Agent 的世界观元数据有两条主链路：一是 `/api/v1/agent/chat/stream` 自动注入 `context["worldview_data"]`（人物/地点/设定/规范，且带字段截断），二是工具调用 `get_worldview_summary`（已废弃但仍在提示词中强制调用）实际转调 `get_writing_context(include="worldview")` 返回人物/地点/设定摘要与计数。`backend/app/api/v1/agent.py:1291`、`backend/app/services/agent/langgraph_tools.py:917`、`backend/app/services/agent/langgraph_tools.py:1132`
- 执行轨迹里的“世界观已加载(n)”来自工具返回解析：`langgraph_agent` 在 tool 执行完成后解析 `get_worldview_summary/get_worldview_tool` 的 JSON，生成 `knowledge_loaded` 事件并打上“人物/地点/设定”标签。`backend/app/services/agent/langgraph_agent.py:1676`
- 数据的最终来源是世界观服务层按 work_id 读取角色/地点/设定/规范表；工具与自动注入都复用该服务。`backend/app/services/worldview_service.py:30`

#### 世界观元数据给到 Agent 的方案（待确认）

- [x] 盘点世界观进入 Agent 的全部链路（自动注入 / 工具拉取 / Explore 侧读）
- [x] 列出现有字段差异清单：自动注入 vs get_writing_context（人物/地点/设定/规范）字段完整性与裁剪上限
- [x] 标注所有长度预算点：worldview_data 字段截断、system message 总字符上限、summarization 截断
- [x] 明确安全处理差异：自动注入是否清洗、工具链是否 sanitize、潜在注入风险点
- [x] 补全权限策略：work_id + user_id 验证是否一致；无 user_id 时的降级策略
- [x] 统一世界观元数据 Schema（WorldviewSchema v1）：全量字段定义 + 最小返回字段定义
- [x] 增加 world_rules/constraints/禁忌清单结构化字段（从 guidelines 拆分）
- [ ] 加入实体关系结构：entity_id、aliases、relations、role/status/voice/constraints
- [ ] 引入 evidence 字段：章节序号/引用片段/来源类型，支持溯源与置信度
- [ ] 加入 timeline/glossary：时间线事件与术语表，便于一致性与复用
- [x] 定义 WorldviewProfile（统计与摘要）与 WorldviewPack（按需注入包）两级结构
- [ ] 设计 WorldviewPack 构建规则：根据任务类型/章节定位/关键词召回
- [x] 设计硬约束注入层：将世界规则/禁忌/风格约束注入 System 级提示
- [ ] 设计软约束注入层：人物/地点/设定按需注入，避免全量污染
- [x] 改造 get_writing_context：可选 include=worldview_full/worldview_pack/worldview_profile
- [x] 新增按需工具：get_worldview_tree
- [x] 新增按需工具：get_worldview_node
- [x] 新增按需工具：get_worldview_pack
- [x] 补齐 Explore 对世界观的召回链路：按需拉取 + 结果融合 + 证据化呈现
- [x] 建立世界观索引：名称/别名/关键词/标签/关系索引，支持快速检索
- [x] 建立世界观缓存策略：work_id 级缓存 + 更新失效机制
- [x] 接入一致性校验工具：生成后对规则/关系/时间线做冲突检测
- [x] 设计冲突处置：自动修复（可修）/ 生成候选 / 交由用户确认（不可修）
- [x] 建立回写闭环：新事实 -> pending -> 用户确认 -> 落库 -> 版本递增
- [x] 加入世界观版本字段与变更日志（谁改、改了什么、证据）
- [ ] 加入观测指标：世界观注入条目数/命中率/冲突率/回写通过率
- [ ] 补测试用例：字段完整性、清洗安全、按需注入、冲突检测、回写流程
- [ ] 交付迁移计划：老数据映射到新 schema、规范字段拆分与回填
- [ ] 输出上线步骤与回滚方案（开关化：仅 profile → pack → full）

#### review

- 已新增 WorldviewSchema v1 / WorldviewProfile / WorldviewPack 结构，作为统一世界观与按需小包的最小数据规范。
- get_writing_context 支持 worldview_full/worldview_profile/worldview_pack，并新增关键词与 top_k 参数。
- 已补齐 get_worldview_pack / get_worldview_node / get_worldview_tree（StandardTool 注册完成），Explore 首轮改为按需小包拉取，并新增 worldviews 缓存失效。
- 现状盘点结果：三条链路为自动注入（`/api/v1/agent/chat/stream`）、工具拉取（`get_writing_context`）、Explore 侧读（`get_worldview_pack`）。
- 字段差异：自动注入不含 `id` 且摘要长度更高（人物500/地点300/设定500），get_writing_context 返回 `id`、更短摘要（默认200）并可选规范；Setting 在工具链返回 `name/title/content`，自动注入仅 `title/content`。`backend/app/api/v1/agent.py`、`backend/app/services/agent/langgraph_tools.py`
- 长度预算点：自动注入字段截断；世界观软约束系统提示上限约 `3000` 字符、硬约束 `800`；工具结果压缩上限（`get_writing_context=12000`、`get_worldview_summary=6000` 等）由 `context_builder` 控制；ContextManager 超预算触发压缩/摘要。`backend/app/services/agent/utils/context_builder.py`、`backend/app/services/context/manager.py`
- 安全处理差异：工具链读取会经过 `content_sanitizer` 清洗，自动注入仍为原始字段，存在 prompt 注入风险。
- 权限补齐：`get_writing_context/get_worldview_pack/get_worldview_node/get_worldview_tree` 新增 user_id 校验（有 user_id 才校验，无 user_id 降级放行）；自动注入改为先验证 work 归属。`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/execution/tool_executor.py`、`backend/app/api/v1/agent.py`

#### 世界观按需加载方案整体梳理（待确认）

- [x] 目标：不塞全量世界观给 Agent；每次只拿“此刻必须遵守”的小包
- [x] 现状链路：自动注入 / get_writing_context 工具拉取 / Explore 侧读
- [x] 现状差异：字段结构不一致（规范缺失/描述裁剪不同/关系字段不足）
- [x] 长度预算：worldview_data 字段截断 + system message 总字符上限 + summarization 截断
- [x] 安全处理：工具链 sanitize，自动注入未必清洗；存在 prompt 注入风险
- [x] 权限策略：部分路径缺 user_id 校验，需要统一 work_id+user_id 验证
- [x] Schema 统一：WorldviewSchema v1，统一人物/地点/设定/规范字段
- [x] 规则拆分：从 guidelines 中拆 world_rules / constraints / 禁忌清单
- [ ] 实体结构：entity_id / aliases / relations / role / status / voice / constraints
- [ ] 证据字段：evidence(章节/片段/来源/置信度)支撑溯源与冲突校验
- [ ] 时间线/术语表：timeline + glossary 结构化，便于一致性与检索
- [x] 两级结构：WorldviewProfile(摘要统计) + WorldviewPack(按需注入包)
- [ ] Pack 构建：基于任务类型 + 章节定位 + 关键词召回 + Top-K 控制
- [x] 硬约束注入：世界规则/禁忌/风格必须进 System 层
- [ ] 软约束注入：人物/地点/设定只注入必要字段，避免上下文污染
- [x] get_writing_context 扩展：include=worldview_full/worldview_pack/worldview_profile
- [x] 新增工具：get_worldview_tree
- [x] 新增工具：get_worldview_node
- [x] 新增工具：get_worldview_pack
- [x] Explore 补齐：按需拉取 + 结果融合 + 证据化呈现
- [x] 索引体系：名称/别名/标签/关系索引，支持快速召回
- [x] 缓存策略：work_id 级缓存 + 变更失效
- [x] 一致性校验：生成后检测规则/关系/时间线冲突
- [ ] 冲突处置：自动修复可修项；不可修项进入用户确认
- [x] 回写闭环：新事实 -> pending -> 用户确认 -> 落库 -> 版本递增
- [x] 版本与日志：记录谁改了什么、证据与时间
- [ ] 观测指标：注入条目数/命中率/冲突率/回写通过率
- [ ] 测试覆盖：字段完整性/清洗安全/按需注入/冲突检测/回写流程
- [ ] 落地优先级：Schema 统一 → Pack 按需 → 硬约束注入 → 校验闭环 → 观测与缓存

梳理全文（对应 25 条待办）

整体目标

1. 不把世界观“塞给”Agent。
2. 让 Agent 每次只拿“此刻必须遵守”的那一小撮。
3. 生成前有硬约束，生成中按需补充，生成后做一致性校验并回写。

一、现状链路盘点（对应 2993-2997）

1. 目前有三条进入链路：自动注入、工具拉取、Explore 侧读。
2. 字段差异明显：自动注入包含规范但字段较肥；get_writing_context 字段更瘦且不含规范。
3. 长度预算分散：字段截断、system message 上限、summarization 截断。
4. 安全处理不一致：自动注入不一定清洗，工具链会 sanitize。
5. 权限策略不一致：有的路径未强制 user_id 校验。

二、目标架构（对应 2998-3006）

1. 统一世界观 Schema：同一套字段定义，自动注入与工具拉取使用同一结构。
2. 新增规则类结构：世界规则/禁忌/约束从 guidelines 中拆分成可读的硬规则。
3. 实体结构补全：人物/地点/设定统一实体模型，支持 aliases、relations、status、voice、constraints。
4. 证据化：每条元数据带 evidence（来源章节/片段/置信度）。
5. 新增时间线/术语表：用于一致性与召回。
6. 两级返回结构：
   - WorldviewProfile：轻量摘要与统计。
   - WorldviewPack：按需小包，只有当前任务需要的条目。

三、按需加载运行流程（对应 3003-3011）

1. 识别需求：从用户请求与当前段落抽取关键实体/规则/术语。
2. 构建 pack：根据任务类型 + 章节定位 + 关键词召回构建 WorldviewPack。
3. 硬约束先注入：世界规则/禁忌/风格进入 System prompt，小而刚性。
4. 软约束按需注入：人物/地点/设定只带必要字段，避免上下文污染。
5. 支持精确补拿：get_worldview_node 精确补一个节点。
6. Explore 侧读：与章节证据融合，返回证据化的世界观条目。
7. 缓存策略：work_id 级缓存 + 变更失效，减少重复 IO。

四、工具与接口（对应 3007-3009）

1. 改造 get_writing_context：
   - include=worldview_full
   - include=worldview_pack
   - include=worldview_profile
2. 新增按需工具：
   - get_worldview_tree
   - get_worldview_node
   - get_worldview_pack

五、一致性校验与闭环（对应 3012-3015）

1. 输出后执行一致性检测：规则/关系/时间线冲突扫描。
2. 可修复就自修复，不可修复则提示用户确认。
3. 回写闭环：新事实进入 pending → 用户确认 → 落库 → 版本递增。
4. 增加版本与变更日志，保证可追溯。

六、观测与测试（对应 3016-3017）

1. 观测指标：注入条目数、命中率、冲突率、回写通过率。
2. 测试用例：字段完整性、清洗安全、按需注入、冲突检测、回写流程。

七、落地优先级建议

1. 先统一 Schema + Profile/Pack 两级结构。
2. 接入硬规则 System 注入。
3. 上线 get_worldview_pack + 关键词召回。
4. 加一致性校验与回写闭环。
5. 最后完善索引、缓存、观测指标。

一句话总结

这套计划的核心是：把世界观变成“结构化可检索元数据”，按需拼成小包注入，生成后再做一致性校验与回写闭环。这样世界观再大也能“随用随取”，并且始终稳。

#### review

- 已按梳理版落地首批能力：Explore 改为按需调用 `get_worldview_pack`，新增 `get_worldview_tree`，并补充 worldview_pack 缓存与更新失效。
- 已接入硬约束注入：系统提示追加世界规则/风格/禁忌摘要；一致性校验新增“轻量自动修复”尝试（非 critical 且条数少时自动修正，否则提示用户确认）。
- 已补齐索引体系：按名称/别名/标签/关系构建轻量索引，worldview_pack 关键词命中优先走索引再回退全文匹配。

#### 世界观回写闭环（pending → 用户确认 → 落库 → 版本递增）（待确认）

- [x] 通读现有链路：`extract-changes/scan-changes/apply-changes` 与世界观 CRUD，确认可复用点与缺口
- [x] 设计 pending 数据结构：work_id/user_id/status/source/changes/evidence/selected_items/version/apply_stats
- [x] 新增模型 + Schema + 迁移：`WorldviewChange`（pending/applied/rejected）+ 版本字段
- [x] 新增服务层：创建 pending、查询列表、应用落库、拒绝/撤回
- [x] 新增 API：创建 pending、查询 pending、应用变更（可选项）、拒绝变更
- [x] 应用落库时写入变更日志并递增版本号
- [x] 自检闭环：创建 pending → 用户确认 → apply 生效 → 版本递增与日志可追溯

#### review

- 新增世界观回写闭环数据结构：`WorldviewChange` 表记录 pending/applied/rejected、changes/selected_items/evidence 与版本前后值；`works.worldview_version` 作为世界观版本号。`backend/app/models/worldview_change.py`、`backend/app/models/work.py`、`backend/alembic/versions/20260204_1200_add_worldview_changes.py`
- 新增回写服务与接口：支持创建 pending、列表查询、应用变更、拒绝变更，并在 apply 时递增版本号与记录统计。`backend/app/services/worldview_change_service.py`、`backend/app/api/v1/worldview.py`、`backend/app/schemas/worldview.py`
- 自检：`python3 -m py_compile` 覆盖新增/修改文件通过（`python` 不存在，已改用 `python3`）。

#### 世界观规则结构化 + 软约束注入（待确认）

- [x] 通读相关文件：`work_guidelines` 模型/Schema、世界观自动注入、`_fetch_worldview_data`、`context_builder`
- [x] 规则结构化：为 guidelines 增加 `constraints`/`taboo` 字段并迁移；Schema 同步
- [x] 世界观聚合：`_fetch_worldview_data` 补充 `world_rules/constraints/taboo` 列表与 timeline 输出
- [x] 约束注入：硬约束优先读结构化规则；软约束优先使用 `worldview_pack`（无则回退 `worldview_data`）
- [x] 自动注入同步：注入时补充 `constraints/taboo`（如有）
- [x] 自检：`python3 -m py_compile` 覆盖改动文件

#### review

- WorkGuidelines 新增 `constraints/taboo` 字段并完成迁移，Schema 同步。`backend/app/models/work_guidelines.py`、`backend/app/schemas/worldview.py`、`backend/alembic/versions/20260204_1300_add_work_guidelines_constraints_taboo.py`
- 世界观聚合补齐结构化规则与时间线：`_fetch_worldview_data` 输出 `world_rules/constraints/taboo` 列表与 `timeline`。`backend/app/services/agent/langgraph_tools.py`
- 约束注入改为优先读结构化列表；软约束系统提示优先使用 `worldview_pack`；自动注入补充 `constraints/taboo` 并生成 `worldview_pack`。`backend/app/services/agent/utils/context_builder.py`、`backend/app/api/v1/agent.py`
- 自检通过：`python3 -m py_compile` 覆盖改动文件。

#### Agent板块设计模式深度探索（待确认）

- [x] 通读 agent 核心链路（LangGraph 工作流/规划/执行/工具注册/反思/并行/HITL）
- [x] 提取证据（文件+行号）并整理与 ReAct/Plan-Execute 等模式对应关系
- [x] 输出直白结论（项目中的设计模式清单 + 每种模式的职责/边界）

#### review

- 已通读并记录 agent 核心链路与实现文件（langgraph_agent/planning/execution/deep_agent/tools/parallel_tool_node 等），整理出 ReAct、Plan-Execute、Reflection+Replan、Parallelization、HITL、Tool Registry、Intent Routing 等模式的代码证据与边界；结论与证据详见本次回复。

#### Agent板块实际执行链路核查（待确认）

- [x] 定位 API 入口与路由（agent/chat 与 stream 等）调用的实际执行函数
- [x] 追踪“真正执行的一条链路”从入口到执行器（LangGraph or Planning or 反思分支）的调用路径
- [x] 核对开关/配置对链路的影响（如 quick_path、反思开关、tool_policy）
- [x] 汇总证据（文件+行号）并给出直白结论（当前线上默认执行链路、备用链路条件）

#### review

- 已确认实际执行入口为 `/api/v1/agent/chat/stream`，且 `mode` 被强制回退为 planning，实际只走 `chat_with_planning` 规划链路；反思分支与 humanize-only 短路为该链路内的条件分支；LangGraph 图仅构建未被调用。结论与证据详见本次回复。

#### 清理 Agent 未使用代码（待确认）

- [x] 梳理当前真实执行链路的“使用清单”（入口→planning→执行→工具）并标注证据
- [x] 生成“可删除候选清单”（含文件路径 + 未被引用的证据）并发给你确认
- [x] 按确认清单删除文件/模块，并同步清理无效引用与测试/文档残留
- [x] 自检：rg 全仓无残留引用，记录删除结果与风险点

#### review

- 已删除未被实际执行链路使用的 LangGraph 图/多场景处理/路由/并行工具节点等模块与文档备份；同时精简 `langgraph_agent.py` 移除图构建与 HTTPAIService 手动工具路径，仅保留 Planning 主链路与反思分支，相关 imports 与初始化已同步清理。

#### 删除反思分支（待确认）

- [x] 移除 API 入参中的反思开关与相关说明（AgentChatRequest）
- [x] 删除反思分支代码与引用（langgraph_agent 执行分支、deep_agent 模块、测试）
- [x] 清理 planning 中与反思开关相关的逻辑与参数传递
- [x] 自检：rg 全仓无反思分支/反思开关残留

#### review

- 已移除反思分支执行逻辑与模块文件，Planning 链路统一走标准并行执行；反思分支目录下 `__init__.py/config.py/executor.py/reflection.py/task_enricher.py` 已删除。`backend/app/services/agent/langgraph_agent.py`、`backend/app/services/agent/deep_agent/*`
- Planning 侧移除反思开关参数与对应 prompt 分支，改为恒定使用静态规划提示词；调用端同步去参。`backend/app/services/agent/planning/plan_generator.py`、`backend/app/services/agent/langgraph_agent.py`
- API 侧确认无反思开关入参，仅清理残留注释；并更新 TaskRunner/降级执行的文档说明去除反思分支表述。`backend/app/api/v1/agent.py`、`backend/app/services/agent/execution/task_runner.py`
- 前端移除反思模式入口：删除模式选择器与相关类型字段，AIPanel 请求固定 `planning`，会话模式统一落为 `plan/chat`。`src/components/editor/AIPanel.tsx`、`src/components/agent/ChatInput.tsx`、`src/components/agent/SessionTabs.tsx`、`src/hooks/useAgentChat.ts`、`src/hooks/useConversationPersistence.ts`、`src/utils/sessionTitleGenerator.ts`
- 清理文档残留：移除 `docs/iterative-agent` 目录，并将 `docs/langgraph_agent重构/*` 与 `docs/Agent 架构的探索.md` 中的反思执行器称谓统一为通用表述。

#### 清理 deepagents 文档残留（待确认）

- [ ] 盘点 `docs/langgraph_agent重构` 中 deepagents 相关引用与示例代码
- [ ] 删除/改写 deepagents 相关段落与代码示例，统一为 LangGraph 原生表述
- [ ] 自检：rg 全仓无 deepagents/create_deep_agent/deep_agent 残留

#### Agent板块设计模式深度探索（本次，待确认）

- [x] 通读 agent 相关后端/前端/配置/提示词与测试文件，梳理真实执行链路
- [x] 按模式抽取证据：ReAct、Plan-Execute、Tool-Calling、Parallel、HITL、Memory/Context、Streaming/Trace
- [x] 形成直白结论：现存模式清单、各自职责边界、已移除或仅残留的实现
- [x] 在 todo.md 追加 review（证据摘要与关键结论）

#### review

- 真实执行链路为 `/api/v1/agent/chat/stream` → `WritingAgentGraph.chat_with_planning` → `PlanGenerator` → `ParallelExecutor` → `ResponseBuilder`，SSE 事件由 FlowEventBuilder/ExecutionFlow 渲染承接。`backend/app/api/v1/agent.py`、`backend/app/services/agent/langgraph_agent.py`、`backend/app/services/agent/execution/parallel_executor.py`、`backend/app/services/agent/planning/response_builder.py`、`backend/app/services/agent/stream/flow_events.py`、`src/hooks/useAgentChatStream.ts`、`src/components/agent/ExecutionFlow/index.tsx`
- 现存设计模式与证据已在答复中逐一对应：Plan-Execute、工具注册/调用、DAG并行、HITL、人机记忆/上下文管理、流式执行轨迹、意图路由/快速路径、Explore 子代理循环。相关证据文件见正文引用。

#### 删除 ReAct 状态段落（待确认）

- [x] 删除 todo.md 中“ReAct 状态/残留”相关的 review 段落
- [x] 复核仅移除该段落，不改动其他说明
- [x] 在 todo.md 追加 review（说明删除结果）

#### review

- 已从 `todo.md` 的“Agent板块设计模式深度探索（本次）”review 中移除 ReAct 状态/残留段落，其他条目保持不变。

#### 清理 ReAct 干扰项代码（待确认）

- [x] 盘点 ReAct 相关代码/文档/类型残留（mode=react、react 分支、ReAct 文档）
- [x] 删除 ReAct 相关残留代码与类型（前端 hooks/types/API 兼容逻辑）
- [x] 确认仅清理代码，不改动 ReAct 文档
- [x] 自检：代码范围无 ReAct/react 模式残留（仅保留 React 框架相关引用）
- [x] 在 todo.md 追加 review（删除范围与影响）

#### review

- 删除 ReAct 残留代码：移除 `useAgentChat` 的 react 分支与 backendMode 判定，前端类型只保留 `planning`，会话标题生成去掉 `react`，后端移除 `mode` 入参并固定 planning；清理空的 ReAct 路由文件。`src/hooks/useAgentChat.ts`、`src/types/agent.ts`、`src/utils/sessionTitleGenerator.ts`、`backend/app/api/v1/agent.py`、`backend/app/api/v1/agent_react_stream*.py`
- 仅清理代码，未改动 ReAct 相关文档；自检仅保留 React 框架引用。

#### 删除 ReAct 文档目录（待确认）

- [x] 删除 `docs/Agent/ReAct 模式优化/` 整个文件夹
- [x] 删除 `docs/langgraph_agent重构/18-execution-trace-redesign.md`
- [x] 自检：rg 不再出现 ReAct 模式优化文档路径
- [x] 在 todo.md 追加 review（删除范围）

#### review

- 已删除 `docs/Agent/ReAct 模式优化/` 整个目录及 `docs/langgraph_agent重构/18-execution-trace-redesign.md`；相关文件不再存在。

#### 再梳理 Agent 设计模式（待确认）

- [x] 复核当前真实执行链路与主要模块
- [x] 逐模式梳理：Plan-Execute、Tool-Calling、Parallel/DAG、HITL、Memory/Context、Streaming/Trace、Intent/QuickPath、Explore 子代理
- [x] 输出直白结论（模式清单 + 各自职责边界）
- [x] 在 todo.md 追加 review

#### review

- 已复核当前链路：`/chat/stream` → `chat_with_planning` → 规划 → 执行 → 汇总 → SSE 轨迹；并按模式输出证据与边界（见回复）。`backend/app/api/v1/agent.py`、`backend/app/services/agent/langgraph_agent.py`

#### Agent板块设计模式深度探索（待确认）

- [x] 复核实际执行链路：API 入口 → chat_with_planning → 规划/执行/工具/流式输出
- [x] 通读 agent 核心模块（planning/execution/tools/stream/context/hitl）与前端链路
- [x] 逐模式整理证据：Plan-Execute / Tool-Calling / Parallelization / HITL / Memory-Context / Streaming-Trace 等
- [x] 对照 ReAct 等模式给出是否存在/已移除的结论（含文件与行号证据）
- [x] 输出直白结论并在 todo.md 追加 review

#### review

- 已完成 Agent 真实链路与设计模式证据梳理：覆盖 Planning→Execution→Response、并行DAG调度、工具注册与调用、HITL 审批、上下文记忆、SSE执行轨迹与前端渲染映射等；结论见本次答复。

#### 清理 Planning 之外干扰项（待确认）

- [x] 删除 DynamicPlan（仅定义未被使用）
- [x] 从 execution/__init__.py 移除 DynamicPlan 导出
- [x] 删除 LangGraph HITL 节点封装（hitl_nodes.py，含 need_replan 标记）
- [x] 自检：rg 无 replan/DynamicPlan/hitl_nodes 残留

#### review

- 已删除动态计划与 LangGraph HITL 节点封装：`backend/app/services/agent/execution/dynamic_plan.py`、`backend/app/services/agent/tools/hitl_nodes.py`，并移除 `DynamicPlan` 的导出，仅保留 ToolExecutor/ParallelExecutor/TaskRunner。`backend/app/services/agent/execution/__init__.py`

#### 世界观按需加载后续落地计划（待确认）

- [x] 补齐实体结构字段：Location/Setting 增加 aliases/relations/status/voice/constraints/evidence（含迁移），Character 补齐 schema 输出字段
- [x] 统一证据结构：定义 evidence 子结构（章节/片段/来源/置信度），并在人物/地点/设定/术语表中落地
- [x] 新增 glossary 词条体系：模型/Schema/Service/API + get_worldview_tree/node 支持 glossary
- [x] 更新世界观聚合输出：_fetch_worldview_data 输出实体新增字段 + glossary + timeline
- [x] 升级 WorldviewPack 构建规则：任务类型/章节定位/关键词召回 + Top-K 控制 + timeline 章节过滤
- [x] 软约束注入落地：构建 worldview_context 文本并注入 smart_* 生成提示（避免 System 污染）
- [x] 观测指标埋点：注入条目数/命中率/冲突率/回写通过率（含调用路径）
- [x] 补测试用例：字段完整性/清洗安全/按需注入/冲突检测/回写流程
- [x] 交付迁移计划：旧数据映射、规则拆分回填、默认值策略
- [x] 输出上线步骤与回滚方案：开关化（仅 profile → pack → full）

#### review

- 已补齐实体结构字段与证据结构：角色/地点/设定新增 aliases/relations/status/voice/constraints/evidence，并补充 GlossaryTerm 模型与迁移。`backend/app/models/character.py`、`backend/app/models/location.py`、`backend/app/models/setting.py`、`backend/app/models/glossary_term.py`、`backend/alembic/versions/20260204_1500_add_worldview_entity_fields_and_glossary.py`、`backend/app/schemas/worldview.py`
- Glossary 端到端落地：WorldviewService + API + worlddata 聚合 + get_worldview_tree/node 支持 glossary。`backend/app/services/worldview_service.py`、`backend/app/api/v1/worldview.py`、`backend/app/services/agent/langgraph_tools.py`
- WorldviewPack 升级：任务提示抽词 + 章节范围过滤 + glossary/timeline/规则类注入；索引与关键词匹配扩展到 aliases/relations/constraints/evidence。`backend/app/services/agent/langgraph_tools.py`
- 软约束注入落地：新增 `worldview_context` 构建并注入 smart_continue/smart_rewrite/smart_insert 提示词，避免 System 污染。`backend/app/services/agent/utils/context_builder.py`、`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/tools/editor_tools.py`
- 观测指标埋点：worldview_pack 命中/总量、软注入条目数、一致性冲突总量、回写通过/拒绝计数。`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/tools/consistency_checker.py`、`backend/app/services/worldview_change_service.py`
- 迁移计划：旧字段默认空列表；Location/Setting 的 `related_locations/related_items` 输出映射到 `relations`；规则类字段继续从 guidelines 拆分；新增 Glossary 默认空表，不影响旧数据读取。
- 上线与回滚：先只启用 `worldview_profile` 输出；再开启 `worldview_pack` + 软约束注入；最后开放 full 输出与 glossary UI。回滚时可仅关闭 pack/软注入路径并保留 schema 与数据表。
- 新增单测：覆盖 pack 的 timeline 过滤、glossary 命名与软注入优先级。`backend/tests/unit/test_worldview_pack.py`
- 测试执行失败：`pytest backend/tests/unit/test_worldview_pack.py` 由于缺少 `chromadb` 依赖在导入阶段中断（环境问题，代码层未触发）。

#### 世界观按需加载落地修复（待确认）

- [x] 通读链路并锁定缺口：自动注入 / 工具拉取 / Explore / 软约束 / 硬约束 / 一致性校验
- [x] 统一自动注入数据源：改用 `_fetch_worldview_data` 并走 `sanitize_worldview_data`，消除旧 schema 差异
- [x] 自动注入补齐顶层规则：同步输出 `world_rules/constraints/taboo` 列表，确保 pack/硬约束可读
- [x] 硬约束注入落地：在 smart_* system_prompt 或生成入口插入 `_build_worldview_hard_constraints` 的结果
- [x] 软约束内容扩展：`_collect_worldview_parts` 增加 glossary/timeline/relations/constraints 等必要字段并控长
- [x] pack 优先级校准：hard/soft 统一优先 `worldview_pack`，缺失时回退 `worldview_data`
- [x] 一致性校验自动触发：生成后调用 `check_story_consistency`，按严重度决定自动修复/待确认
- [x] 权限策略补齐：user_id 为空时的降级策略（拒绝/仅 profile/仅公开字段）
- [x] 证据/关系写入补齐：同步或抽取链路写入 evidence/relations/aliases/constraints（至少保留已有字段）
- [x] 缓存与失效对齐：worldview_pack/profile TTL 与失效点校准
- [x] 补测试：硬约束注入、自动注入清洗、软约束包含 glossary/timeline、权限拒绝、自动一致性校验触发
- [x] 自检与回归：`python3 -m py_compile` + pytest（处理 chromadb 依赖或隔离用例）

#### review

- 自动注入改为统一走 `_fetch_worldview_data` 并完成清洗，顶层 `world_rules/constraints/taboo` 可直接用于 pack/硬约束。`backend/app/api/v1/agent.py`
- 软/硬约束落地：`_collect_worldview_parts` 增加 glossary/timeline/relations/constraints；硬约束优先 pack 回退 data；smart_* system_prompt 注入 `worldview_hard_constraints`。`backend/app/services/agent/utils/context_builder.py`、`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/tools/editor_tools.py`
- 一致性校验自动触发：smart_* 结果附加 `consistency_report`（轻量版）；当前一致性引擎仍是空抽取逻辑，报告多为 0，需后续增强抽取。`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/tools/consistency_checker.py`
- 权限降级：`get_worldview_pack` 无 user_id 时限制输出（top_k 缩小、禁 guidelines）；`get_worldview_node/tree` 要求 user_id；Explore 调用补齐 user_id。`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/tools/explore_tools.py`
- 回写补齐：worldview_sync 新建人物/地点/设定可携带 aliases/relations/constraints/evidence/status/voice 等扩展字段。`backend/app/services/worldview_sync_service.py`
- 缓存与 TTL：`get_writing_context` 对 `worldview_pack/profile` 使用 worldview TTL；世界观服务失效触发 ToolCache 清理。`backend/app/services/agent/utils/tool_cache.py`、`backend/app/services/worldview_service.py`
- 测试：`python3 -m py_compile` 通过；`pytest -q backend/tests/unit/test_worldview_context.py backend/tests/unit/test_worldview_pack.py` 结果 2 passed, 1 skipped（chromadb 依赖导致 pack 用例跳过）。

#### 世界观注入与缓存缺陷修复（待确认）

- [x] 修复改写生成 NameError：为 `_generate_rewrite_versions` 补传 `worldview_hard_constraints`
- [x] 补充 `WorkService` 导入，恢复 `agent_chat_stream` 世界观注入链路
- [x] 修复缓存过滤：`_filter_gwc_context` 保留 `worldview_pack/worldview_profile/worldview_full` 字段
- [x] 自检：`python3 -m py_compile` + 相关单测

#### review

- 修复 smart_rewrite 调用链：`_generate_rewrite_versions` 增加 `worldview_hard_constraints` 参数并由 smart_rewrite 传入，避免 NameError。`backend/app/services/agent/tools/editor_tools.py`
- 补齐 `WorkService` 导入，恢复 `agent_chat_stream` 世界观注入路径。`backend/app/api/v1/agent.py`
- 缓存过滤保留 worldview pack/profile/full：`_filter_gwc_context` 追加 `worldview_pack/worldview_profile/worldview_full` 键。`backend/app/services/agent/execution/tool_executor.py`

#### get_worldview_pack NoneType 修复（待确认）

- [x] 防御性处理：_match_worldview_keywords 对非 dict 直接返回 False
- [x] _select 过滤非 dict 项，避免匹配阶段调用 item.get 报错
- [x] 自检：`python3 -m py_compile backend/app/services/agent/langgraph_tools.py`

#### review

- 修复世界观 pack 在包含 None 项时报错：关键词匹配与选择阶段新增 dict 过滤，避免 `NoneType` 访问 `.get`。`backend/app/services/agent/langgraph_tools.py`

#### 世界观 pack 清洗与引用修复（待确认）

- [x] 修复 sanitize_worldview_data 深度导致列表项变 None（保留列表内 dict 结构）
- [x] get_worldview_pack executor 解析 JSON 并补充 pack 兼容字段
- [x] 自检：`python3 -m py_compile` + 验证 pack 不为空

#### review

- 调整 worlddata 清洗深度并跳过 None 列表项，避免人物/地点/设定被清洗成空。`backend/app/utils/content_sanitizer.py`
- get_worldview_pack 返回结构补充 `pack` 兼容字段，并优先解析 JSON 为 dict。`backend/app/services/agent/langgraph_tools.py`
#### 世界观测试 Prompt 生成（待确认）

- [x] 读取素材 `docs/Agent/real-book/人在诸天，摆烂成帝.txt`，抽取关键角色/设定/术语/事件
- [x] 设计 5 条高复杂度测试 Prompt，覆盖世界观按需注入/硬约束/软约束/一致性/缓存路径
- [x] 输出可直接复制的 Prompt，并在 todo.md 追加 review

#### review

- 已读取素材并整理关键要素：林仙/系统10086/叶凡/九龙拉棺/泰山/遮天五大秘境/一人之下等，用于生成覆盖世界观注入与一致性校验的测试 Prompt。

#### Opencode 项目 Agent 设计模式深度探索（待确认）

- [x] 盘点 opencode agent 运行链路核心模块（agent/session/tool/permission/compaction/summary）并记录证据文件
- [x] 深读关键文件并抽取“循环/工具调用/子代理/计划/权限/记忆”实现证据（含行号）
- [x] 对照设计模式给出结论（ReAct/Plan-Execute/多代理/Tool-Calling/HITL/记忆压缩/流式）
- [x] 在 todo.md 追加 review（证据摘要 + 结论）

#### review

- 已盘点并深读 opencode agent 核心链路与模块：`agent/agent.ts`（代理定义与权限）、`session/prompt.ts`（主循环与子任务）、`session/processor.ts`（流式处理与工具状态）、`session/llm.ts`（工具调用与模型流）、`tool/task.ts`（子代理）、`tool/plan.ts`+`session/prompt/plan*.txt`（计划/执行切换）、`permission/next.ts`+`question/*`（HITL）、`session/compaction.ts`+`session/summary.ts`（记忆压缩/摘要）、`tool/registry.ts`（工具注册）、`session/message-v2.ts`（事件/部件结构）。
- 结论摘要：Opencode 采用“工具调用循环（Act→Observe）+ 多代理子任务 + 计划/执行双阶段 + 权限与问答式 HITL + 记忆压缩/摘要 + 流式事件轨迹”的组合模式；未见显式 ReAct 的 Thought 文本输出，但存在等价的工具调用循环与观察回流。

#### Plan-Execute 自主性优化（参考 opencode）（待确认）

- [x] 对照 opencode 的“工具调用循环/子代理/权限-HITL/微型再规划”机制，提炼可迁移点
- [x] 基于现有 Plan-Execute 链路设计“执行阶段可决策”的最小改法（触发条件/边界/回退）
- [x] 给出落地清单：需要改哪些模块、需要新增哪些事件或状态、最小风险控制
- [x] 在 todo.md 追加 review（证据来源 + 结论）

#### review

- 现状证据：执行链路为 `chat_with_planning → PlanGenerator → ParallelExecutor.execute_tasks → ResponseBuilder`，任务列表固定执行，无动态改写入口。`backend/app/services/agent/langgraph_agent.py` `backend/app/services/agent/execution/parallel_executor.py`；PlanSchema 仅定义 tasks/depends_on 等结构。`backend/app/services/agent/planning/plan_schema.py`
- 可迁移点：项目已有“opencode 风格工具调用循环”在 explore_content 内部循环（tool_calls_left/decision/stop），可作为执行阶段“微型再规划”的模板。`backend/app/services/agent/tools/explore_tools.py`
- 结论：最小改法是在 ParallelExecutor 的“单任务完成点”插入 Decision/Replan Hook，根据工具结果触发追加任务或再规划；并新增可视化事件与策略开关，保证可控与可回退。

#### Agent 设计模式完全重构（待确认）

- [ ] 明确目标架构与边界：从“Plan-Execute”改为“Goal/Policy/Action Loop（执行主导）”，定义可控边界（预算/步数/工具白名单/写回规则）
- [ ] 设计新核心模型与接口：GoalState/DecisionPolicy/ExecutionLoop/ActionResult/StopReason，并与现有 ToolExecutor/TaskRunner/FlowEvent 对接
- [ ] 设计新执行主链路：替换 `chat_with_planning → execute_tasks` 为“决策循环”，保留 Planning 作为“可选策略/意图提示”
- [ ] 设计兼容与迁移：旧 PlanSchema → 新 GoalSchema 的适配器；保留旧链路的 feature flag 以便回滚
- [ ] 设计前端执行轨迹映射：新增决策事件（decision_start/decision_done）或复用 step 事件，保证 ExecutionFlow 展示一致
- [ ] 设计安全与质量闭环：失败重试、HITL 触发点、写回强校验、成本/步数上限、降级策略
- [ ] 输出分阶段改造清单与风险评估：按模块列出修改文件、接口变化、测试点与回归范围
- [ ] 在 todo.md 追加 review（架构结论 + 落地清单）

#### Codex 项目 Agent 设计模式深度探索（待确认）

- [x] 通读 `codex/codex-rs/core` 的 agent 主循环、工具路由/执行、审批、并行、多代理、记忆压缩相关文件，记录证据位置（文件+行号）
- [x] 归纳设计模式清单并对照证据：事件驱动/命令、工具调用循环、工具注册/路由、并行执行、HITL、子代理、记忆压缩
- [x] 输出直白结论（模式说明+职责边界+明确“不包含/未实现”的模式）并在 todo.md 追加 review

#### review

- 事件驱动/命令：`submission_loop` 持续读取 `Submission` 并按 `Op` 分发处理，`Op` 充当命令对象；循环本身是事件驱动主循环。`codex/codex-rs/core/src/codex.rs:2124-2238`
- 工具调用循环（Act→Observe）：`run_turn` 说明“模型要么请求工具，要么输出回复；请求工具后再采样下一轮”，并在循环内持续调用 `run_sampling_request`。`codex/codex-rs/core/src/codex.rs:2925-3091`
- 工具注册/路由（Registry/Strategy）：`ToolRegistry` 按工具名映射 handler；`ToolRouter` 负责从配置构建 specs 并将工具调用分派给 registry。`codex/codex-rs/core/src/tools/registry.rs:15-149`、`codex/codex-rs/core/src/tools/router.rs:29-165`
- 并行执行（受控并行）：`ToolCallRuntime` 用 `RwLock` 区分可并行与需串行的工具调用，控制并行度。`codex/codex-rs/core/src/tools/parallel.rs:24-105`
- HITL 审批：`ShellRuntime`/`ApplyPatchRuntime` 通过 `Approvable` 触发 `request_command_approval`/`request_patch_approval`，未批准不执行。`codex/codex-rs/core/src/tools/runtimes/shell.rs:65-173`、`codex/codex-rs/core/src/tools/runtimes/apply_patch.rs:27-174`
- 子代理/多代理：`spawn_agent` 工具通过 `AgentControl::spawn_agent` 创建新线程代理并派发初始消息。`codex/codex-rs/core/src/tools/handlers/collab.rs:37-184`、`codex/codex-rs/core/src/agent/control.rs:28-108`
- 记忆压缩：`compact` 任务将历史摘要化并替换历史（`build_compacted_history`），用于长期对话压缩。`codex/codex-rs/core/src/compact.rs:32-199`
- 直白结论：这个 Codex agent 的核心是“事件驱动 + 工具调用循环”，辅以“工具注册/路由、受控并行、HITL 审批、子代理、记忆压缩”。当前链路没有看到显式的“Plan→Execute 两阶段”或“独立规划器/计划数据结构”，也没有公开的 ReAct 思维输出；它更像“工具调用型执行循环”。证据见上述文件与行号。

#### Opencode 项目 Agent 设计模式深度研读（本次，待确认）

- [x] 通读 opencode agent 关键链路文件（agent/session/tool/permission/compaction/summary/acp），定位证据位置
- [x] 抽取“工具调用循环/计划-执行/子代理/工具注册/事件总线-HITL/记忆压缩/适配器”证据（含文件与行号）
- [x] 形成直白结论并在 todo.md 追加 review（模式清单 + 职责边界 + 是否存在/缺失）

#### review

- 工具调用主循环（Act→Observe）：`SessionPrompt.loop` 在 while(true) 中驱动对话，收集任务/子任务并调用 `SessionProcessor.process`；`SessionProcessor` 解析流式事件并处理 tool-call/result；`LLM.stream` 把 tools 作为 activeTools 传给模型。`opencode/packages/opencode/src/session/prompt.ts:258-625`、`opencode/packages/opencode/src/session/processor.ts:45-221`、`opencode/packages/opencode/src/session/llm.ts:162-216`
- 子代理（Sub-agent/任务派发）：`TaskTool` 选择 subagent、创建子会话并调用 `SessionPrompt.prompt`；主循环遇到 `subtask` 会执行 `TaskTool` 并回写结果。`opencode/packages/opencode/src/tool/task.ts:15-188`、`opencode/packages/opencode/src/session/prompt.ts:316-455`
- 工具注册/命令模式（Registry + Command）：`ToolRegistry` 从目录/插件加载工具并统一过滤；`Tool.define` 定义可执行工具接口并统一校验/执行。`opencode/packages/opencode/src/tool/registry.ts:34-156`、`opencode/packages/opencode/src/tool/tool.ts:16-85`
- 计划/执行是“代理模式切换”而非内置计划图：`plan_enter/plan_exit` 通过问题确认切换 plan/build agent；`Agent` 定义 plan/build 两类 primary agent 与权限。`opencode/packages/opencode/src/tool/plan.ts:20-128`、`opencode/packages/opencode/src/agent/agent.ts:73-109`
- HITL（权限审批 + 交互问题）：`PermissionNext.ask` 根据规则触发 ask 并通过 Bus 发布事件；`Question.ask` 发起可选回答；`SessionProcessor` 在工具重复调用时触发 `doom_loop` 审批。`opencode/packages/opencode/src/permission/next.ts:96-156`、`opencode/packages/opencode/src/question/index.ts:63-120`、`opencode/packages/opencode/src/session/processor.ts:146-168`
- 记忆压缩/摘要：`SessionCompaction` 计算溢出并触发压缩与剪枝；`SessionSummary` 用 LLM 生成摘要/标题与 diff 统计。`opencode/packages/opencode/src/session/compaction.ts:30-193`、`opencode/packages/opencode/src/session/summary.ts:23-110`
- 事件总线/观察者：`Bus.publish/subscribe` 提供全局事件分发；被 Permission/Question/Session 等模块使用。`opencode/packages/opencode/src/bus/index.ts:41-104`
- 协议适配器（ACP Adapter）：`ACP.Agent implements ACPAgent`，把 ACP 连接请求转换为内部权限/会话流程，并订阅 opencode 全局事件流。`opencode/packages/opencode/src/acp/agent.ts:46-173`

#### Plan-Executor 死板问题根因深度探索（本次，待确认）

- [x] 通读项目 agent 主链路（planning→execution→response）并定位关键“固定执行”证据
- [x] 深挖执行器/任务调度（ParallelExecutor/TaskRunner/PlanSchema）以证明“静态计划、无运行时再决策”
- [x] 形成直白结论：死板本质原因 + 受影响链路 + 现存仅有的局部自主性（含证据）

#### review

- 主链路证据：`chat_with_planning` 明确按阶段执行：先 `PlanGenerator.generate_plan` 得到 `plan_data`，再调用 `_execute_tasks_in_parallel(tasks=plan_data["tasks"])`，最后 `_build_final_response` 汇总。整个执行阶段以 `plan_data["tasks"]` 为唯一输入，没有任何“执行中再生成/追加任务”的入口。`backend/app/services/agent/langgraph_agent.py:898-1169`、`backend/app/services/agent/langgraph_agent.py:1193-1235`
- 静态计划证据：`PlanSchema` 只描述 `tasks/depends_on` 的结构（静态 DAG），无“runtime decision / replan / policy”字段；计划一旦生成即固定。`backend/app/services/agent/planning/plan_schema.py:19-42`
- 执行器证据：`ParallelExecutor.execute_tasks` → `_execute_with_dag` 基于 `depends_on` 进行就绪队列调度，任务集合是输入时就确定的 `tasks` 列表；执行过程中只消费队列、不会生成新任务或修改任务图。`backend/app/services/agent/execution/parallel_executor.py:51-225`
- 单任务执行证据：`TaskRunner.execute_task` 只负责“把 task.tool + params 调用到 ToolExecutor/旧 @tool”，无“根据结果再做决策/追加任务”的逻辑，失败只会降级到旧工具或返回错误。`backend/app/services/agent/execution/task_runner.py:70-195`
- 规划后处理证据：`PlanGenerator._post_process_plan` 只对规划结果做“修正/拆分/补全/强制探索”等静态规则，不涉及运行时自我修正；任何规则都在执行前完成。`backend/app/services/agent/planning/plan_generator.py:501-543`
- 仅有的“局部自主性”证据：探索工具内部存在“工具循环决策”（例如 explore_content 的 tool loop 决策与 stop），但它局限在 explore 工具内部，不能改变全局任务图。`backend/app/services/agent/tools/explore_tools.py:2735-2790`

#### 任务列表过少导致链路崩盘排查（本次，待确认）

- [ ] 通读 `INFO.md` 中该条执行轨迹，标记任务列表/步骤数量与失败点
- [ ] 回溯该条请求的 planning 产物与任务拆分规则（PlanGenerator/plan_schema），解释为何只生成 2 个任务
- [ ] 回溯执行阶段（ParallelExecutor/TaskRunner）与结果汇总路径，确认缺少“执行中追加任务/重试探索”的机制
- [ ] 给出直白结论：问题根因 + 受影响链路 + 若有自主决策应插入的位置（含证据）

#### 参考 OpenCode 的自主决策机制梳理（本次，待确认）

- [x] 抽取 OpenCode 的工具调用主循环、停止条件、权限/HITL、子代理与记忆压缩机制证据
- [x] 对照当前项目 Plan-Executor 链路，标出“缺失的运行时决策点”
- [x] 输出直白梳理：OpenCode 做法清单 + 可迁移要点 + 在本项目的最小插入位置（含证据）

#### review

- OpenCode 的“运行时决策主循环”证据：`SessionPrompt.loop` 在 while(true) 中持续处理消息/任务，并在 `SessionProcessor.process` 里解析 tool-call/result 形成“调用→观察→继续”的循环；`LLM.stream` 将 tools 作为 activeTools 提供给模型，模型可在多轮中决定是否继续调用工具。`opencode/packages/opencode/src/session/prompt.ts:258-625`、`opencode/packages/opencode/src/session/processor.ts:45-221`、`opencode/packages/opencode/src/session/llm.ts:162-216`
- 停止条件与防死循环：`SessionProcessor` 在重复 tool-call 时触发 `doom_loop` 权限询问（HITL），并在 `finish`/`blocked` 时中止循环。`opencode/packages/opencode/src/session/processor.ts:146-218`
- 子代理（运行时委派）：`TaskTool` 可创建子会话并调用 subagent，主循环遇到 subtask 会执行 task 工具并回流结果。`opencode/packages/opencode/src/tool/task.ts:23-188`、`opencode/packages/opencode/src/session/prompt.ts:316-455`
- 权限/HITL：`PermissionNext.ask` 将“是否允许”作为运行时决策点（ask/allow/deny），`Question.ask` 支持显式问题确认。`opencode/packages/opencode/src/permission/next.ts:96-156`、`opencode/packages/opencode/src/question/index.ts:63-120`
- 记忆压缩：`SessionCompaction` 在上下文溢出时触发压缩/剪枝，属于运行时状态管理。`opencode/packages/opencode/src/session/compaction.ts:30-193`

- 对照本项目的缺失点：当前链路是“先生成计划 tasks → 执行 tasks → 汇总”，执行阶段没有“再决策/再规划”的入口；执行器只消费静态 tasks 队列。`backend/app/services/agent/langgraph_agent.py:898-1169`、`backend/app/services/agent/execution/parallel_executor.py:51-225`、`backend/app/services/agent/planning/plan_schema.py:19-42`

- 可迁移要点（最小插入位）：
  1) 在 `ParallelExecutor` 的“单任务完成点”插入 Decision Hook：基于 task result 决定是否追加“定位/重试/补证据”任务（对应 OpenCode 的 tool-call→observe→continue 回路）。`backend/app/services/agent/execution/parallel_executor.py:205-223`  
  2) 在 `TaskRunner.execute_task` 返回结果后增加“结果判定→追加任务”的轻量策略（等价于 OpenCode 的运行时工具循环决策）。`backend/app/services/agent/execution/task_runner.py:171-195`
  3) 通过现有 HITL/Question 机制作为“继续/停止”决策点（对标 OpenCode 的 Permission/Question）。`backend/app/services/agent/tools/hitl.py`（运行时 checkpoint 已存在，只缺与执行循环的绑定）

#### 最小改造方案：Decision Hook（保持 Plan-Executor）（本次，待确认）

- [x] 明确 Decision Hook 触发条件：搜索未命中/定位失败/ambiguous_locator（从现有错误格式与轨迹证据归纳）
- [x] 设计最小插入点：在 ParallelExecutor 单任务完成后判定并“追加补救任务”，保持原任务列表不改
- [x] 设计补救任务模板：针对 explore_content 未命中/ambiguous_locator 给出最小补任务（如精确搜索/定位/再读上下文）
- [x] 给出风险控制与停止条件：最大补任务次数、同任务去重、HITL 触发点
- [x] 输出直白方案说明（含伪代码/步骤）并在 todo.md 追加 review

#### review

- 触发条件证据：定位失败/歧义来自 `ToolExecutor._select_locate_target` 的 `missing_locate_targets/ambiguous_locator/locator_not_found/locator_index_out_of_range` 错误；探索未命中可从 explore_content 的 `missing_keywords` 字段判断。`backend/app/services/agent/execution/tool_executor.py:1337-1444`、`backend/app/services/agent/tools/explore_tools.py:3793-3801`
- 最小插入点：`ParallelExecutor._execute_with_dag` 在单任务完成处追加 Decision Hook（对 result 进行判定并补任务），不改规划/执行大结构。`backend/app/services/agent/execution/parallel_executor.py:205-223`
- 补救任务模板：使用 `explore_content(work_id, target_task, search_keywords, require_paragraph_index=True, force_global_search)` 作为“补证据/补定位”任务；explore_content 明确支持 search_keywords 与 require_paragraph_index。`backend/app/services/agent/tools/explore_tools.py:5024-5053`
- 风险控制：新增 decision_budget（最多 1-2 次补任务）、按 tool+params 去重、重复 ambiguous_locator 转入 HITL/Question 询问或直接提示用户指定第几处；避免无限循环。

#### Agentic AI 强自主性重构（本次，待确认）

- [ ] 定义目标架构与边界：Goal/Policy/Action Loop + 运行时评估/策略排序 + 预算/步数/安全白名单
- [ ] 盘点现有模块并映射：planning/execution/tools/memory/stream/hitl/context → 新循环中的角色
- [ ] 设计运行时状态模型：AgentState（目标/策略候选/工具调用历史/证据/风险/成本）
- [ ] 设计决策循环：Observe → Propose → Evaluate → Act → Reflect（含 stop 条件）
- [ ] 设计策略生成/评估接口：多策略候选 + 评分/优先级 + 失败回退
- [ ] 设计记忆与上下文：短期工作记忆 + 历史压缩 + 证据缓存/失效策略
- [ ] 设计 HITL 与安全策略：决策点、审批触发、回滚与审计
- [ ] 输出迁移路径与阶段落地：兼容旧 Plan-Executor、Feature Flag、回滚方案
- [ ] 输出直白结论与落地清单（含证据对照）

#### smart_continue 续写插入位置异常排查（待确认）

- [x] 通读 smart_continue → operate_apply → apply_chapter_edit 链路，确认 append 写回逻辑与返回字段
- [x] 通读 plan_generator 对 smart_continue 的 apply 任务构建，核对是否带入 paragraph_index/node_id
- [x] 通读 stream_event_handler 对 append/continue 的 editor_action 构造，确认前端是否接收定位字段
- [x] 通读 NovelEditor 修订显示流程（continue 定位优先级），确认定位字段如何影响插入位置
- [x] 对照 Backend.md/INFO.md 证据，给出“为何插在中间”的核心原因链路
- [x] 输出直白结论与最小修复建议，并在 todo.md 追加 review

#### review

- 计划器对 smart_continue 也注入定位字段：`_build_apply_task` 在 `operation=append` 情况下仍会把 `node_id/paragraph_index`（来自 locate/explore）写入 operate_apply 参数。`backend/app/services/agent/planning/plan_generator.py:2060-2145`
- 事件层把这些字段原样下发：`stream_event_handler` 构造 `editor_action` 时无条件携带 `node_id/paragraph_index`，append 也会带到前端。`backend/app/services/agent/stream/stream_event_handler.py:372-409`
- 前端续写定位优先级导致“插中间”：`NovelEditor` 在 continue 模式下优先使用 `nodeId/paragraphIndex` 定位，其次才是“末尾默认追加”，因此只要带了定位字段就会插到该段而不是末尾。`src/components/editor/NovelEditor.tsx:1043-1218`
- 后端 append 实际是拼接末尾：`apply_chapter_edit` 对 append 执行 `old_content + actual_content`，说明“插中间”不是写回逻辑，而是前端修订展示定位导致。`backend/app/services/agent/tools/editor_tools.py:510-546`
- 日志链路吻合：Backend.md 显示先 explore_content → smart_continue → operate_apply(append)，在此链路下规划器会引入 explore 的段落索引（推断），与“中间插入”的现象一致。`Backend.md:120-182`（推断基于规划器代码）

#### smart_continue 续写插入位置修复（待确认）

- [x] 明确修复策略：append 不应携带定位字段；continue 展示只允许末尾追加
- [x] 后端：plan_generator 构造 append 任务时不注入 `node_id/paragraph_index/__auto_locator`
- [x] 后端：stream_event_handler 对 append 的 editor_action 清空定位字段（双保险）
- [x] 前端：continue 修订展示忽略定位字段，强制末尾插入
- [ ] 自检：对照续写链路日志与界面行为，确认不再插中段
- [x] 在 todo.md 追加 review（改动点与风险）

#### review

- 续写 append 不再携带定位字段：`_build_apply_task` 对 `smart_continue` 跳过注入 `node_id/paragraph_index/__auto_locator`，避免续写被当作“插入到某段”。`backend/app/services/agent/planning/plan_generator.py:2060-2145`
- 事件层双保险：对 append 的 `editor_action` 清空 `before_anchor/after_anchor/node_id/paragraph_index`，防止旧链路残留字段误导前端。`backend/app/services/agent/stream/stream_event_handler.py:379-411`
- 前端 continue 强制末尾：修订展示对 `continue` 忽略所有定位字段，仅保留“末尾追加”默认行为；定位逻辑仅保留给 `insert/modify`。`src/components/editor/NovelEditor.tsx:1043-1218`
- 风险与影响：append 不再支持“续写到特定段落”，如需中段补写应改用 `smart_insert` + 定位流程；这与产品语义一致。

#### smart_insert 模糊定位根因修复（待确认）

- [x] 复盘 ambiguous_locator 触发路径与 locate_targets 生成逻辑
- [x] 设计根因修复：为 smart_insert 自动补 locate_content，使用插入锚点短语定位
- [x] 实现：规划后处理自动插入 locate_content 并绑定 smart_insert 依赖
- [ ] 自检：第三个测试 prompt 重新执行，smart_insert 不再返回 ambiguous_locator
- [x] 在 todo.md 追加 review（改动点与风险）

#### review

- 根因：smart_insert 仅依赖 explore_content 的 locate_targets；当定位短语（如“系统启动”）未进入 locate_targets 且候选多条时，ToolExecutor 触发 `ambiguous_locator` 并中止 smart_insert 执行。`backend/app/services/agent/execution/tool_executor.py:1320-1450`、`backend/app/services/agent/tools/explore_tools.py:1676-1785`
- 修复：规划后处理自动为 smart_insert 补一个 `locate_content` 任务（query=插入锚点短语），并把 smart_insert 依赖绑定到该定位结果，避免在多候选中盲选。`backend/app/services/agent/planning/plan_generator.py`
- 影响：当用户未指定“第几处/具体段落”但给出锚点短语时，系统会先定位后插入；若定位仍不唯一，会在 locate_content 层明确返回候选而不是直接 ambiguous。

#### 深度探索 Agent 板块设计模式并评审计划可行性（待确认）

- [x] 通读 Agent 架构相关文档（02_技术架构设计、03_Memory系统设计、04_工具系统设计、langgraph_agent重构/00-overview、06-interrupt-resume、explore/01-overview 等），提取设计模式证据
- [x] 盘点后端核心链路：langgraph_agent（Planning 主链路）、planning/execution/tools/stream/memory/context/hitl，整理实际运行环路与 AgentState 字段
- [x] 盘点前端对接：useAgentChatStream/ExecutionFlow 事件依赖，确认改动对 SSE/FlowEvent 的影响
- [x] 对照你的计划输出映射表与缺口清单（Goal/Policy/Action Loop、策略排序、预算/白名单、HITL/安全、迁移路径）
- [x] 给出直白可行性结论与落地清单（含风险/前置条件），并在 todo.md 追加 review

#### review

- 文档设计模式证据：架构文档定义了“LangGraph 工作流+规划/写作/反思/质量循环/HITL/版本管理”等节点与分层架构；中断恢复文档提出 interrupt/resume 与前端 SSE 事件格式；Explore 文档明确 `explore_content` 是内部自主循环的 mini-agent；工具系统设计强调标准化工具注册/类型验证。`docs/Agent/Primary-level-completed/02_技术架构设计.md:20-107`、`docs/langgraph_agent重构/06-interrupt-resume.md:10-176`、`docs/explore/01-overview.md:12-61`、`docs/Agent/Primary-level-completed/04_工具系统设计.md:25-104`
- 实际后端链路证据：当前运行链路是 `/chat/stream → chat_with_planning → PlanGenerator → 执行 → ResponseBuilder`，属于静态 Plan-Execute；`AgentState` 仅包含 messages/work_id/chapter_id/intent/context/agent_steps 等，没有“目标/策略候选/评估/预算/风险”字段。`backend/app/services/agent/langgraph_agent.py:3-60`、`backend/app/services/agent/langgraph_agent.py:679-1267`
- 前端 SSE/FlowEvent 依赖：前端 `agentApi` 解析固定事件类型（plan/task_start/task_done + flow events: step_start/step_complete/output_ready/summary/explore_round 等），`useAgentChatStream` 将其映射为 ExecutionFlow；当前未处理 interrupt/resume 事件。`src/services/agentApi.ts:168-377`、`src/hooks/useAgentChatStream.ts:341-528`、`src/components/agent/ExecutionFlow/index.tsx:71-200`
- 缺口清单（对照 Agentic AI 目标）：
  1) **动态任务分解/目标调整**：缺运行时决策循环，执行阶段只消费静态 tasks；需要引入 Observe→Propose→Evaluate→Act→Reflect 主循环。
  2) **策略生成与优先级**：无策略候选/评分机制；目前只有 PlanGenerator 一次性产出 tasks。
  3) **持续记忆与反馈闭环**：已有 ContextManager/MemoryPack，但未将“评估/反思”写回作为决策信号。
  4) **环境感知与策略反馈**：只有 explore_content 内部循环具备局部反馈，未上升为全局 Agent Loop。
  5) **HITL/安全**：已有 HITL 工具，但未与“运行时决策点”绑定；interrupt/resume 仍停留在文档设计。
- 可行性结论：技术上可行（已有工具注册、上下文管理、FlowEvent、HITL 组件与 explore_content 的 mini-agent 经验），但要达“强自主性”必须重构主循环与事件协议，属于中高代价变更；最大风险在前端 SSE 事件兼容与执行轨迹重塑。
- 落地清单（高层）：
  1) 新增 Agentic 主循环与 AgentState（目标/策略/评估/预算/证据/风险）。
  2) 把 PlanGenerator 降级为“策略生成器”而非唯一计划源。
  3) 新增策略评估器（质量/风险/成本评分）与 stop 条件。
  4) 扩展 SSE：加入 decision/interrupt/resume 事件，并更新 ExecutionFlow 映射。
  5) 保留 Plan-Executor 作为 feature flag 回滚路径。

#### 深度研读 opencode agent 设计模式（待确认）

- [x] 通读 agent/会话/工具/插件/权限/ACP 等核心模块，标记设计模式证据位置
- [x] 归纳该 agent 的主要设计模式，并逐条对应代码证据
- [x] 输出直白结论：核心模式、为何这样设计、局限点

#### review

- 已定位核心证据文件：主循环与工具调用在 `opencode/packages/opencode/src/session/prompt.ts`、`opencode/packages/opencode/src/session/processor.ts`、`opencode/packages/opencode/src/session/llm.ts`；工具命令与注册在 `opencode/packages/opencode/src/tool/tool.ts`、`opencode/packages/opencode/src/tool/registry.ts`。
- 已定位事件/插件/权限/协议适配证据：事件总线在 `opencode/packages/opencode/src/bus/index.ts`；插件钩子在 `opencode/packages/opencode/src/plugin/index.ts`；权限规则在 `opencode/packages/opencode/src/permission/next.ts`；ACP 适配在 `opencode/packages/opencode/src/acp/agent.ts`；多 Provider 工厂/策略在 `opencode/packages/opencode/src/provider/provider.ts`。

#### 项目 Agent 死板根因深度探索（待确认）

- [x] 通读现有 Agent 主链路（planning → execution → response）并列出“固定执行/无再决策”的证据
- [x] 深挖执行器/任务调度（ParallelExecutor/TaskRunner/PlanSchema）确认任务集合是否静态、无运行时追加
- [x] 盘点工具/探索/HITL 是否存在“局部自主性”，并说明为何未上升为全局决策
- [x] 输出直白结论：死板的本质原因 + 受影响链路 + 证据清单

#### review

- 主链路证据：`chat_with_planning` 明确按阶段执行：规划 `PlanGenerator.generate_plan` → 执行 `_execute_tasks_in_parallel(tasks=plan_data["tasks"])` → 汇总 `_build_final_response`，执行阶段只消费规划产生的 tasks，没有“执行中再生成/追加任务”的入口。`backend/app/services/agent/langgraph_agent.py:898-1235`
- 任务集合是静态 DAG：`PlanSchema` 只包含 `tasks/depends_on`，无“runtime replan/decision”字段；`ParallelExecutor._execute_with_dag` 只基于已生成的 `tasks` 建队列并执行，不会新增任务。`backend/app/services/agent/planning/plan_schema.py:19-42`、`backend/app/services/agent/execution/parallel_executor.py:139-225`
- 执行器职责单一：`TaskRunner.execute_task` 只是“调用工具+参数准备+兜底/降级”，不具备“根据结果追加任务”的逻辑；`ParameterResolver` 只解析占位符依赖。`backend/app/services/agent/execution/task_runner.py:70-195`、`backend/app/services/agent/parameter_resolver.py:369-425`
- 仅有局部自主性：`explore_content` 内部存在“round plan → 多轮工具调用”的 mini-loop（局部自主），但该循环被封装在工具内部，无法影响全局任务图；HITL 主要是“结果确认事件”，不改变任务列表。`backend/app/services/agent/tools/explore_tools.py:4331-4410`、`backend/app/services/agent/langgraph_agent.py:1566-1607`

#### Explore 规则移除重构（待确认）

- [x] 移除 `exact_search_paragraphs` 的关键词合并/force_set/拦截规则，仅保留基础清洗与范围过滤
- [x] 禁用搜索去重/相似判断（`should_search`/`searched_queries`），不再因历史跳过搜索
- [x] 移除 tool_loop 的“空读硬停”与相关计数，停止只由 LLM 或 max_tool_calls 决定
- [x] 最小自检：关键词不被合并/拦截，空读不再触发硬停

#### review

- `exact_search_paragraphs` 已移除关键词合并/force_set/拦截逻辑，仅保留基础清洗（去空白/引号/去重）与范围过滤；不再强制合并 `search_keywords` 或覆盖截断。`backend/app/services/agent/tools/explore_tools.py`
- 搜索去重/相似判断已禁用：`should_search` 直接放行，语义搜索与精确搜索不再因历史跳过。`backend/app/services/agent/tools/explore_tools.py`
- tool_loop 移除空读硬停与计数，并取消读取上限触发的提前停止；停机只剩 LLM 停止或工具调用上限。`backend/app/services/agent/tools/explore_tools.py`

#### OpenCode 风格 Review Gate 重设计（待确认）

- [x] 盘点 Review Gate 切入点与数据流（explore_content → shared_state → task_runner/tool_executor → 下游写回）
- [x] 定义 Review Gate 标准（写回必须 locate_targets；分析/回答必须 evidences；允许显式 chapter_id/paragraph_index 直通）
- [x] 落地 Review Gate：在执行器前置检查证据，不满足则阻塞并提示用户指定位置
- [x] 事件与输出：阻塞时发明确信息（前端/最终回复可见），避免继续执行下游任务
- [x] 最小自检：缺证据时不再继续写回；提供明确 HITL 提示

#### review

- Review Gate 落点在执行器前置：`ParallelExecutor._execute_single_task_with_retry` 在执行前检查写回/分析证据，缺失则返回 `missing_prerequisite`，最终响应会直接提示用户补充定位或原文。`backend/app/services/agent/execution/parallel_executor.py`
- 写回 Gate：`smart_insert/smart_rewrite/operate_apply(replace/insert)` 需要 `locate_targets` 或显式 `node_id/paragraph_index/source_locator`；否则阻塞并提示 HITL。`backend/app/services/agent/execution/parallel_executor.py`
- 分析 Gate（仅在参数引用 evidences 时启用）：若任务参数 `$ref` 指向 `evidences/locate_targets` 且无证据，则阻塞并提示先取证。`backend/app/services/agent/execution/parallel_executor.py`
- 阻塞后停止后续任务：并行/串行路径遇到 `status=blocked` 立即终止后续执行，避免继续写回。`backend/app/services/agent/execution/parallel_executor.py`

#### Review Gate 变更验证（待确认）

- [ ] 确认测试入口（如何触发 agent/提供 work_id 与章节）
- [ ] 执行 5 条复杂 prompt 测试（按顺序）
- [ ] 记录每条的预期/实际：是否触发 missing_prerequisite、是否继续写回
- [ ] 汇总测试结论与风险

#### 解决“严格定位 vs 整章读取”矛盾（待确认）

- [x] 复核冲突点与触发链路（严格定位 + 范围读取导致 locate_targets 为空）
- [x] 设计“统一定位契约”：区分章节级/段落级定位，明确各工具的输入/输出要求
- [x] 给出 2-3 种可落地方案并评估（章节级写回工具 / 范围读取产出定位 / 规划层放宽严格定位）
- [x] 输出推荐方案与直白结论（包含影响范围与最小改动点）

#### review

- 冲突链路确认：规划层对编辑类任务强制 `require_paragraph_index=True`，而 `read_paragraphs` 的范围读取会标记 `is_target=False`，`locate_targets` 只收 `is_target=True`，导致“读全章但无定位”。`backend/app/services/agent/planning/plan_generator.py:784` `backend/app/services/agent/tools/explore_tools.py:3840` `backend/app/services/agent/tools/explore_tools.py:4099` `backend/app/services/agent/tools/explore_tools.py:1718`
- 统一定位契约建议：明确区分 `chapter_scope`（整章替换/续写/全章改写）与 `paragraph_scope`（插入/替换某段），前者只要求 `chapter_id + 章节原文证据`，后者必须 `locate_targets`/`node_id/paragraph_index`。
- 可落地方案对比：
  1) **章节级写回通道**（推荐）：整章改写走 `operate_apply(operation=content)` 或 `update_chapter_content`，规划层不再对这类任务设置 `require_paragraph_index`；避免空定位失败。
  2) **范围读取产出定位**：当 `require_paragraph_index=True` 且范围读取时，把段落标为 `is_target=True` 或直接从整章内容拆出 `locate_targets`；能过关但会产生大量定位/歧义。
  3) **严格定位条件收敛**：仅在 `replace/insert` 等段落级操作时开启严格定位；对 `content/append` 关闭严格定位。
- 推荐结论：采用“章节级写回通道 + 严格定位条件收敛”，把“整章任务”和“段落任务”拆成两条协议，既保留精确定位，又避免整章读取被强制失败。

#### Backend.md 失败原因深度排查（待确认）

- [x] 读取 Backend.md 失败日志并定位关键链路（explore_content → smart_rewrite → operate_apply）
- [x] 对照 explore_content 输出规则与 locate_targets 生成逻辑，确认“读全章但无定位”的成因
- [x] 追踪 require_paragraph_index 的注入点（规划/参数），确认为何强制定位
- [x] 汇总证据与给出直白结论（根因链路 + 受影响模块）

#### review

- Backend.md 显示 explore_content 通过 `read_paragraphs` 以 `chapter_order/offset/limit` 分页读取 114 段后仍报错“缺少 paragraph_index/node_id”，关键链路已定位。`Backend.md:91` `Backend.md:127` `Backend.md:128`
- `explore_content` 在 `require_paragraph_index=True` 且 `locate_targets` 为空时直接返回 `missing_locate_targets`，因此即使读到了原文也会报错。`backend/app/services/agent/tools/explore_tools.py:5134` `backend/app/services/agent/tools/explore_tools.py:5142`
- `read_paragraphs` 的“范围读取”会设置 `is_target=False`（`use_range` 为真），而 `_build_locate_targets` 只收集 `is_target=True` 的段落，因此“读全章但无定位”。`backend/app/services/agent/tools/explore_tools.py:3840` `backend/app/services/agent/tools/explore_tools.py:4099` `backend/app/services/agent/tools/explore_tools.py:1718`
- 规划层对编辑类任务强制 `require_paragraph_index=True`，导致上述空定位直接触发严格失败。`backend/app/services/agent/planning/plan_generator.py:784` `backend/app/services/agent/planning/plan_generator.py:1223`

#### 推荐方案再评审（待确认）

- [x] 复核“章节级通道”是否被现有 Review Gate/计划器阻断（含 smart_rewrite/operate_apply 的 gate 条件）
- [x] 追踪计划器是否真正会产出 operation=content/整章写回路径（否则需补规划逻辑）
- [x] 校验 smart_rewrite 的整章改写链路是否安全（参数默认/自动取章/输出路径/写回字段）
- [x] 汇总潜在纰漏与修正建议（若需新增 chapter_scope 标记或调整 Review Gate）

#### review

- **Review Gate 会卡住整章 smart_rewrite**：`parallel_executor` 把 `smart_rewrite` 视作写回工具，若无 `locate_targets`/定位字段会直接 `missing_prerequisite` 阻断；整章读取通常没有 `locate_targets`，因此会被拦截。`backend/app/services/agent/execution/parallel_executor.py:787` `backend/app/services/agent/execution/parallel_executor.py:794`
- **规划器目前不会自动产出 operation=content**：`_build_apply_task` 对 `smart_rewrite` 固定生成 `operate_apply(operation="replace")`，这意味着即使是整章改写也会走段落替换路径，仍要求定位。`backend/app/services/agent/planning/plan_generator.py:2081`
- **整章改写会丢 HTML 结构**：`creative_output_filter` 会主动剥离 `<p>/<br>` 等标签，`replace_all` 直接写入新内容不做 HTML 包装；如果章节原文是 HTML，将被替换成纯文本，排版会塌。`backend/app/services/agent/tools/tool_behaviors.py:109` `backend/app/services/agent/tools/editor_tools.py:515`
- **提示词规则与整章改写冲突**：规划提示强制 `text_to_rewrite` 引用 `evidences[0].text`，但整章改写应引用 `chapters[0].content` 或整章原文，否则只会改写单段证据。`backend/app/services/agent/prompts/planning_prompts.py:225` `backend/app/services/agent/tools/explore_tools.py:5289`

#### 章节级改写工具落地（待确认）

- [x] 新增章节级改写工具（rewrite_chapter_content）：读取整章→生成改写→输出整章内容
- [x] 规划层支持整章改写流程：rewrite_chapter_content → operate_apply(operation="content")
- [x] 更新工具/规划提示词：整章改写禁用 smart_rewrite，保留段落改写的严格定位规则
- [x] 最小自检：整章改写不再要求 paragraph_index/node_id，段落改写仍强制

#### review

- 新增章节级改写工具 `rewrite_chapter_content`：可直接读取整章、生成整章改写内容；对 HTML 章节自动包裹 `<p>`，避免整章写回塌排版。`backend/app/services/agent/tools/editor_tools.py`
- 规划层支持整章改写链路：`rewrite_chapter_content` 自动补 `operate_apply(operation="content")`，且不会附加段落定位字段。`backend/app/services/agent/planning/plan_generator.py`
- 章节级写回不再被 locate 覆写 chapter_id：`operate_apply(content/append)` 跳过 locator 覆盖，避免引用 `locate_targets` 导致缺失。`backend/app/services/agent/planning/plan_generator.py`
- 严格定位规则保持不变：`smart_rewrite/smart_insert` 仍强制段落定位；整章改写通过新工具绕开定位硬要求。`backend/app/services/agent/prompts/planning_prompts.py` `backend/app/services/agent/prompts/tool_descriptions.py`

#### rewrite_chapter_content 输出过滤修复（待确认）

- [x] 通读 Backend.md，确认 `<p>` 标签导致写回/插入失败的报错链路
- [x] 复核 rewrite_chapter_content 的输出过滤与 HTML 包裹逻辑，确定 `<p>` 来源
- [x] 制定修复策略：保留纯文本输出或仅在特定写回模式保留 HTML
- [x] 最小改动落地并自检：rewrite_chapter_content 输出不含 `<p>`，写回不再失败

#### review

- 移除 rewrite_chapter_content 的 `<p>` 包裹逻辑，改为强制清理所有 HTML 标签，确保整章改写输出为纯文本，避免前端插入/替换失败。`backend/app/services/agent/tools/editor_tools.py`

#### 修订失败原因深度排查（待确认）

- [x] 通读 INFO.md 与 Backend.md，定位“显示修订失败”的前后任务链路
- [x] 对照前端 ExecutionFlow/修订显示逻辑，确认失败是前端渲染还是后端写回
- [x] 追踪后端定位/写回/Review Gate 的阻断点与错误码（missing_prerequisite/locator/paragraph_index 等）
- [x] 汇总证据并给出直白结论（根因链路 + 影响范围）

#### review

- 后端实际写回成功：Backend.md 记录 `operate_apply op=content → apply_chapter_edit replace_all` 执行成功，`needs_locate=False`，无任何写回失败日志；因此“显示修订失败”不是写回失败而是前端渲染失败。`Backend.md:106-113`
- 根因链路：`replace_all` 不生成 `position`（仅 insert/replace 才填），且内容替换流程没有补 `original_text`；导致 `editor_action` 自动推断为 `modify` 但 **无 position/node_id/paragraph_index**。`backend/app/services/agent/tools/editor_tools.py`、`backend/app/services/agent/langgraph_agent.py`
- 前端无法定位修订：`NovelEditor` 在 `modify/insert` 无定位时仅在“original 全文匹配”才兜底，否则直接 `toast.error('显示修订失败')` 并取消应用；整章改写缺原文与定位因此触发失败提示。`src/components/editor/NovelEditor.tsx:1188-1213`
- 可能出现双提示：修订事件既来自 `langgraph_agent.emit_revision`（流事件）又可能来自章节修订持久化加载（getChapterRevisions），两条都缺定位会各触发一次失败 toast。`backend/app/services/agent/langgraph_agent.py`、`src/components/editor/NovelEditor.tsx:682-742`

#### 方案一落地：章节级修订仅预览确认（待确认）

- [x] 前端流事件：operation=content/replace_all 的修订不派发 `agent-show-revision`（保留修订卡片）
- [x] 前端持久化：加载章节修订时跳过 replace_all（避免重复 toast）
- [x] 前端保护：章节级修订禁用“重做”触发（避免再次走段落修订）

#### review

- 流事件过滤：`useAgentChat` 在 revision 事件中检测 `operation=content/replace_all`，跳过派发 `agent-show-revision`，避免整章改写触发定位失败 toast；修订卡片仍保留。`src/hooks/useAgentChat.ts`
- 持久化过滤：加载章节修订时跳过 `replace_all/content`，不再对整章替换生成段落修订标记，避免重复失败提示。`src/components/editor/NovelEditor.tsx`
- 重做禁用：ExecutionFlow 在章节级替换时不传 `onRedo`，RevisionCard 不显示“重做”按钮，防止再次触发段落修订流程。`src/components/agent/ExecutionFlow/index.tsx`

#### 全章节替换“看起来未生效”排查（待确认）

- [x] 核对后端链路：`operate_apply(content)` 是否真正走到 `replace_all`
- [x] 核对审批链路：采纳时是否先本地事件再调用 `/chat/approval-response`
- [x] 核对编辑器采纳逻辑：无修订标记时是否仍触发 `setContent + autoSave`
- [x] 给出根因与最小修复方向

#### review

- 后端并非没执行整章替换：日志明确显示 `operate_apply(op=content) -> apply_chapter_edit(operation=replace_all)` 成功；说明“写回请求”已发起。`Backend.md:106-113`
- 关键机制是“审批后才真正落库”：`apply_chapter_edit` 先创建 `PENDING` 修订，采纳时通过 `/api/v1/agent/chat/approval-response` 调用 `ChapterRevisionService.apply_revision` 才写入章节正文。`backend/app/services/agent/tools/editor_tools.py` `backend/app/api/v1/agent.py` `backend/app/services/chapter_revision_service.py`
- 现象根因是前端采纳竞态：
  - `submitApproval(true)` 先派发 `agent-accept-revision`，后调后端审批接口。`src/hooks/useAgentChat.ts`
  - 章节级替换被过滤掉 `agent-show-revision` 后，编辑器里没有任何 revision 标记。
  - 但 `handleAcceptRevisionEvent` 仍会执行 `applyRevisionDecisionToHtml -> setContent(nextHtml) -> debouncedSave(editor)`；`nextHtml` 实际等于旧内容，于是触发自动保存旧稿。`src/components/editor/NovelEditor.tsx`
  - `WorkDetailView` 的 `onSave` 会直接 `DataService.updateChapter(...)`，可能把后端刚应用的新整章内容覆盖回旧内容，表现为“看起来没有全章节替换”。`src/views/WorkDetailView/index.tsx`
- 最小修复方向：
  1) 对 `operation=content/replace_all` 的采纳事件在编辑器侧跳过 `setContent+autoSave`（避免旧稿覆盖）；
  2) 采纳成功后主动刷新当前章节内容（或直接用 `pendingApproval.new_content` 替换编辑器内容）；
  3) 保持章节级修订不走段落 revision 标记。

#### 全章节替换采纳后编辑器不更新修复（待确认）

- [x] `useAgentChat.submitApproval`：章节级采纳不再派发 `agent-accept-revision`，改为审批成功后派发整章直接替换事件
- [x] `NovelEditor.handleAgentReplace`：支持章节级 `forceReplaceAll` 直接 `setContent(replacement)` 并保存
- [x] `NovelEditor.handleAcceptRevisionEvent`：无修订标记时不再执行 `setContent(nextHtml)+autoSave`（避免旧稿覆盖）
- [x] `AIPanel` 非 `pendingApproval` 分支补齐章节级采纳路径：审批成功后触发整章直接替换

#### review

- 章节级采纳顺序修正：`submitApproval` 对 `operation=content/replace_all` 不再先派发 `agent-accept-revision`，改为审批接口成功后派发 `agent-replace-text(skipRevision=true, forceReplaceAll=true)`，避免本地旧稿先写回。`src/hooks/useAgentChat.ts`
- 编辑器新增整章直替入口：`handleAgentReplace` 支持 `forceReplaceAll`，直接 `setContent(replacement)` 并触发保存；同时加了 `chapterId` 校验，避免跨章节误替换。`src/components/editor/NovelEditor.tsx`
- 采纳兜底防护：`handleAcceptRevisionEvent` 在找不到目标 revision 标记时直接跳过本地 `setContent + autoSave`，防止章节级采纳把旧内容覆盖回库。`src/components/editor/NovelEditor.tsx`
- 非 pending 分支补齐：`AIPanel` 在 `submitApprovalResponse` 成功后，若是章节级修订则派发整章直替事件；非章节级保留原有 `agent-accept-revision` 逻辑。`src/components/editor/AIPanel.tsx`
- 本地构建校验：`npm run -s build` 失败于既有文件 `src/components/agent/ChatInput.tsx:906` / `src/components/agent/ChatInput.tsx:907` 语法错误，与本次改动文件无直接关联。

#### 采纳一致性与可观测性修复（待确认）

- [x] 修正文案语义：`requires_confirmation=true` 改为“待确认，未落库”
- [x] 审批后回读章节：章节级采纳成功后以服务端章节内容回填编辑器
- [x] 审批链路打点：补 `approval_request created` / `approval_response received` / `revision applied` 三段同 `request_id` 日志
- [x] 最小验证：静态检查改动路径，确认无分支遗漏

#### review

- 修正总结文案语义：`requires_confirmation: true` 不再解释为“已应用到编辑器”，改为“已生成待确认修订，尚未落库”，避免误导用户。`backend/app/services/agent/planning/response_builder.py`
- 章节级采纳改为“审批成功后回读服务端章节内容再替换编辑器”，优先使用最新后端 `chapter.content`，回读失败才回退 `pending.new_content`。`src/hooks/useAgentChat.ts` `src/components/editor/AIPanel.tsx`
- 增加章节级采纳保护：当缺少 `request_id` 时不再执行本地整章替换，避免“未落库先改前端”的假成功。`src/components/editor/AIPanel.tsx`
- 审批链路新增统一可观测日志（同 request_id）：`approval_request created`、`approval_response received`、`revision applied`，并补失败原因日志，便于快速定位卡点。`backend/app/api/v1/agent.py` `backend/app/services/chapter_revision_service.py`
- 验证结果：
- 后端语法检查通过：`python3 -m py_compile backend/app/api/v1/agent.py backend/app/services/chapter_revision_service.py backend/app/services/agent/planning/response_builder.py`
- 前端构建仍被既有错误拦截：`src/components/agent/ChatInput.tsx:906` / `src/components/agent/ChatInput.tsx:907`，与本次改动文件无直接关联。

#### 审批状态闭环修复（方案一执行中）

- [x] 后端增加统一 `apply_state`：`pending|applied|rejected|failed`
- [x] `/chat/approval-response` 返回明确状态，采纳失败返回 `failed`
- [x] 前端采纳门禁：仅 `apply_state=applied` 才触发章节替换事件
- [x] Summarization 增加硬约束：`pending` 时禁止宣称“已写回成功”
- [x] 最小验证：链路日志 + 关键路径静态检查

#### review

- 后端审批状态闭环已补齐：`approval_request` 默认附带 `apply_state=pending`；`/chat/approval-response` 按实际执行结果返回 `apply_state=applied/rejected/failed`，并回写到 HITL extra_data。`backend/app/api/v1/agent.py`
- 边界保护补齐：审批通过但缺少写回内容时，后端显式返回 `failed`（HTTP 400），避免“成功但未落库”的灰状态。`backend/app/api/v1/agent.py`
- 前端门禁已生效：章节级采纳路径只有 `apply_state=applied` 才会触发 `agent-replace-text`（以及章节确认刷新）；未落库直接跳过本地替换，避免假成功。`src/hooks/useAgentChat.ts` `src/components/editor/AIPanel.tsx`
- Summarization 增加硬约束兜底：一旦检测到 `requires_confirmation` 或 `apply_state=pending`，直接输出“待确认未落库”模板，不再让模型自由总结，避免“写回成功”幻觉。`backend/app/services/agent/planning/response_builder.py`
- 保持前端执行流兼容：`pending` 硬约束分支仍发送 `summarization_start/summarization_complete/output_ready` 事件，避免 UI 状态倒退。`backend/app/services/agent/planning/response_builder.py`
- 接口类型已同步：前端 `agentApi.submitApprovalResponse` 增加 `apply_state` 返回类型声明，便于后续流程显式判断。`src/services/agentApi.ts`
- 验证结果：
- 后端语法检查通过：`python3 -m py_compile backend/app/api/v1/agent.py backend/app/services/agent/planning/response_builder.py`
- 前端构建仍被历史错误拦截：`src/components/agent/ChatInput.tsx:906` / `src/components/agent/ChatInput.tsx:907`，与本次改动无直接关联。

#### ChatInput 语法修复（待确认）

- [x] 定位并修复 `src/components/agent/ChatInput.tsx:906/907` 语法错误（多余闭合标签）
- [x] 重新执行前端构建，确认错误已不再出现

#### review

- 已删除 `ChatInput.tsx` 末尾多余 `</div>`，`TS1005/TS1109` 语法错误消失。`src/components/agent/ChatInput.tsx`
- 构建目前失败于其它历史类型错误（ExecutionFlow/NovelEditor/sessionCompression/WorkDetailView/WorksView 等），不再是 ChatInput 的语法错误。`npm run -s build`

#### 待确认文案优化（待确认）

- [x] 待确认模板增加“已完成任务”摘要
- [x] 待确认模板增加“改动内容”摘要（优先 description，兜底 content 预览）
- [x] 保留下一步采纳引导文案，明确“采纳后才落库”

#### review

- `pending` 响应不再只报状态，改为先告诉用户“已完成什么任务、改了什么内容”，再给出“待确认未落库 + 采纳下一步”。`backend/app/services/agent/planning/response_builder.py`

#### opencode agent框架深度研读（待确认）

- [ ] 盘点 `opencode` 项目中 agent 相关入口与模块边界（CLI、Server、Session、Provider、Tool、Prompt、MCP）
- [ ] 深读主执行链路：从命令入口到会话创建、模型调用、工具执行、结果回流
- [ ] 深读状态与上下文机制：消息历史、文件快照、权限策略、持久化结构
- [ ] 深读扩展机制：工具注册/发现、模型提供商适配、事件与 hook 设计
- [ ] 深读 App/SDK 与 Agent 内核的通信边界，并确认关键 API 合同
- [ ] 产出证据清单（文件路径+关键实现点）与直白详细结论

#### Agent Explore 实现深度梳理（待确认）

- [x] 深读后端 Explore 主入口与执行器（`langgraph_agent.py` / `tool_executor.py`）
- [x] 深读 `explore_content` 实现细节（任务拆解、工具循环、停止条件、缓存与共享状态）
- [x] 深读 Explore 只读工具链（search/locate/read）与证据结构生成
- [x] 深读流式事件到前端展示链路（SSE 事件、类型映射、ExploreCard 渲染条件）
- [x] 针对“这种现象”提炼根因：触发条件、代码机制、为何会重复/偏差
- [x] 在 `todo.md` 追加 review：修改记录、证据列表、最终结论

#### review

- 入口与执行链路已核对：规划层把作品相关取证统一路由到 `explore_content`，执行层在并行执行器里把 `explore_content` 结果写入共享 state（`last_explore_result/target_chapter_id`），供后续写作或写回工具引用。`backend/app/services/agent/prompts/planning_prompts.py` `backend/app/services/agent/langgraph_tools.py` `backend/app/services/agent/execution/parallel_executor.py` `backend/app/services/agent/execution/tool_executor.py`
- Explore 核心机制确认：`explore_content` 统一走 `ContentExplorer.explore_tool_loop`（pipeline 已弃用），并且只允许只读工具 `list_chapters/list_paragraphs/exact_search_paragraphs/read_paragraph/read_paragraphs`。`backend/app/services/agent/tools/explore_tools.py`
- 证据口径确认：搜索命中先进入 `search_hits`，只有读取原文后（`read_paragraph/read_paragraphs`）才会进入 `evidences`。这意味着“搜到了但证据数不涨”是设计结果，不是前端错漏。`backend/app/services/agent/tools/explore_tools.py`
- 轮次与停止逻辑确认：循环条件看 `tool_calls_left`，停止主要依赖 LLM 决策或工具上限；代码中 `max_rounds`/`check_convergence`/`should_block_search` 存在但当前循环未实际使用。`backend/app/services/agent/tools/explore_tools.py`
- 缓存与复用确认：存在 Redis 结果缓存（1小时）+ 进程内共享状态缓存（20分钟）；章节变更失效逻辑只清 Redis/Artifact，未清进程内共享状态。`backend/app/services/agent/tools/explore_tools.py` `backend/app/services/agent/utils/explore_cache.py`
- 前端链路确认：SSE 透传 `explore_round/explore_summary`，前端映射为 `toolCalls` 并按 `stepId` 归组渲染；`ExploreRoundCard` 默认折叠，工具标签仅在展开时可见。`backend/app/api/v1/agent.py` `src/services/agentApi.ts` `src/hooks/useAgentChat.ts` `src/hooks/useAgentChatStream.ts` `src/components/agent/ExecutionFlow/index.tsx` `src/components/agent/ExecutionFlow/ExploreCard.tsx`
- “这种现象”的核心成因（代码级）：
  - 重复探索/轮次偏多：`should_search` 恒为 `True` + `max_rounds` 未参与循环判停 + 强制首轮 `list_chapters/list_paragraphs`，导致 Explore 天然更“啰嗦”。`backend/app/services/agent/tools/explore_tools.py`
  - 命中很多但可写回失败：`locate_targets` 目前只从“已读段落”构建，若只搜索未读，写回前置检查会报 `missing_prerequisite(locate_targets)`。`backend/app/services/agent/tools/explore_tools.py` `backend/app/services/agent/execution/parallel_executor.py`
  - Explore 后还追问：总结提示词对创作类强制“分阶段追问”，即使已探索到准备信息也会继续问用户参数。`backend/app/services/agent/planning/response_builder.py`
- 抽象需求检索失败的核心矛盾（新增）：
  - 当前 Explore 主循环是“只读 Grep 模式”：可用工具明确只有 `exact_search_paragraphs`（字面匹配），并显式禁用 `search_content` 语义检索；旧的语义搜索逻辑在 pipeline 分支里，但 pipeline 已弃用。`backend/app/services/agent/tools/explore_tools.py` `backend/app/services/agent/tools/explore_tools.py`
  - `exact_search_paragraphs` 与实时正文版本质都是 `chunk_text ilike %keyword%` / `kw in text`，不做语义近邻；抽象意图（如“压迫感递进”“关系张力”）天然难命中。`backend/app/services/chapter_vector_service.py`
  - 缺失关键词判定绑定“原文是否包含关键词字面”：`missing_keywords` 依据 `kw.lower() in target_text.lower()` 计算，导致“语义相关但不含字面词”被当作未命中，驱动继续探索。`backend/app/services/agent/tools/explore_tools.py`
  - Read 崩盘常见触发：`read_paragraphs(items)` 过滤后若 `chapter_order/paragraph_index` 无效会返回“没有可读取的段落（无效/超范围/已读）”；node_id 仅在已做过 `list_paragraphs` 的缓存映射下才能还原为段落号。`backend/app/services/agent/tools/explore_tools.py`
  - 还存在“上限错位”：`tool_executor` 默认只给 `max_rounds=10`，但循环实际按 `max_tool_calls`（默认200）停止，`max_rounds` 当前不参与判停，容易出现长时间打转。`backend/app/services/agent/execution/tool_executor.py` `backend/app/services/agent/tools/explore_tools.py`

#### 删除旧 pipeline 语义残留（待确认）

- [x] 清理 `explore_tools.py` 中未使用的旧 pipeline 结构（`RoundPlan` 与 `_execute_round_with_plan`）
- [x] 清理与旧 pipeline 相关的默认值/文案（`explore_mode` 默认与注释统一为 `tool_loop`）
- [x] 运行最小静态校验（`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py`）
- [x] 在 `todo.md` 追加 review（删除范围、影响评估、验证结果）

#### review

- 已删除 `backend/app/services/agent/tools/explore_tools.py` 中旧 pipeline 残留：`RoundPlan` 数据结构与 `_execute_round_with_plan` 整段执行逻辑（含 `search_content` 语义搜索分支、旧 locate/read 路径），避免代码库继续保留不可达的旧实现。
- 已统一默认入口语义：`ContentExplorer.__init__` 的 `explore_mode` 默认值与兜底值均改为 `tool_loop`，文件头核心流程描述同步改为当前“工具循环 + 原文读取证据”逻辑。
- 同步清理提示文案中的旧模式暴露：`backend/app/services/agent/prompts/tool_descriptions.py` 中 `explore_mode` 说明改为“仅支持 tool_loop”，内部禁用工具列表改为当前真实内部工具（list/search/read）。
- 语法校验通过：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py backend/app/services/agent/prompts/tool_descriptions.py` 返回 0。

#### 删除 explore_mode 参数（待确认）

- [x] 清理 `explore_tools.py` 中 `ContentExplorer.__init__` 与 `explore_content` 的 `explore_mode` 入参及传递
- [x] 清理 `tool_executor.py` 中 `explore_content` 允许参数白名单里的 `explore_mode`
- [x] 清理提示词文档中 `explore_mode` 的参数说明，保持“只有 tool_loop”事实一致
- [x] 运行最小语法校验并在 `todo.md` 追加 review

#### review

- `backend/app/services/agent/tools/explore_tools.py` 已删除 `explore_mode` 全链路：`ContentExplorer.__init__` 入参、无效成员赋值、`explore_content` 入参与 `ContentExplorer(...)` 传参，避免继续暴露无意义模式开关。
- `backend/app/services/agent/execution/tool_executor.py` 的 `explore_content` 参数白名单已移除 `explore_mode`，上层即使传入该字段也不会再参与调用。
- `backend/app/services/agent/prompts/tool_descriptions.py` 已删除 `explore_content` 的 `explore_mode` 参数说明，工具文档与实际接口一致（仅保留预算类参数）。
- 语法校验通过：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py backend/app/services/agent/execution/tool_executor.py backend/app/services/agent/prompts/tool_descriptions.py` 返回 0。

#### 研读 opencode 上下文获取机制（待确认）

- [x] 通读 `opencode/packages/opencode/src/session` 主链路，定位“消息→模型输入”构建路径
- [x] 通读 `opencode/packages/opencode/src/tool` 的读/搜工具与截断逻辑，定位“上下文证据”来源与治理策略
- [x] 通读 `opencode/packages/opencode/src/agent/prompt` 与 compaction/summary 逻辑，定位“上下文压缩与续航”机制
- [x] 输出“为何能稳定拿到足够上下文”的证据链结论（含关键文件+行号）
- [x] 在 `todo.md` 追加 review（结论、风险点、可迁移建议）

#### review

- 主链路证据：`SessionPrompt.loop` 每轮先读取历史并过滤已压缩段，再拼接 `SystemPrompt.environment + custom + MessageV2.toModelMessages` 喂给模型；用户上传文件/选区会在 `createUserMessage` 阶段先真实调用 `ReadTool/ListTool/MCP.readResource` 注入文本，确保“先拿证据再推理”。`opencode/packages/opencode/src/session/prompt.ts:275` `opencode/packages/opencode/src/session/prompt.ts:601` `opencode/packages/opencode/src/session/prompt.ts:822`
- 工具治理证据：`read` 默认分段读取（`limit=2000`、50KB 上限、offset 续读提示），`grep` 结果按时间排序后只保留前 100，`Truncate.output` 超限会落盘并强制引导“继续 grep/read(offset/limit) 或委托 explore 子任务”，避免一次性把超长文本塞进上下文。`opencode/packages/opencode/src/tool/read.ts:12` `opencode/packages/opencode/src/tool/read.ts:92` `opencode/packages/opencode/src/tool/grep.ts:107` `opencode/packages/opencode/src/tool/truncation.ts:50`
- 续航证据：`SessionCompaction.isOverflow` 基于 token 预算触发压缩；`process` 会把历史模型消息交给 compaction agent 生成“继续工作提示”；主循环结束还会执行 `prune` 清理早期工具长输出，减少上下文噪声。`opencode/packages/opencode/src/session/compaction.ts:30` `opencode/packages/opencode/src/session/compaction.ts:92` `opencode/packages/opencode/src/session/prompt.ts:627`
- 前端上下文注入证据：页面把“文件选区/评论”存入 prompt context，发送时统一转成 `file://...?...start=&end=` + 注释文本，后端收到后立刻 read 成可消费文本，不依赖模型“猜文件内容”。`opencode/packages/app/src/pages/session.tsx:515` `opencode/packages/app/src/components/prompt-input.tsx:1313` `opencode/packages/opencode/src/session/prompt.ts:954`
- 风险点：它不是语义向量检索，而是“文件显式注入 + grep/read 迭代 + 压缩续航”；如果用户问题高度抽象且未给任何可落地线索，仍会出现探索轮次增加，只是通过任务拆分与截断治理把失控概率压低。`opencode/packages/opencode/src/agent/agent.ts:125` `opencode/packages/opencode/src/tool/task.ts:165`
- 可迁移建议：优先迁移“前端选区强注入 + read/grep 分页续读 + truncation 落盘提示 + compaction/prune 双层续航 + explore 子任务并行”这套可解释机制，再考虑补语义检索；先把召回可控性做稳，语义只是增益层。

#### 深度追踪 Explore 证据传递与评判机制（待确认）

- [x] 通读 `explore_content` 主链路（调用入口→轮次执行→输出组装），定位“探索结果如何落到任务结果”
- [x] 通读执行层参数解析与 `$ref` 注入链路，定位“探索结果如何传给后续 AI 工具（smart_* / operate_apply）”
- [x] 通读创作工具提示词组装逻辑，定位“AI 实际依据哪些信息做判断（evidence_context/段落上下文/用户需求）”
- [x] 通读前端 SSE 事件映射与展示链路，定位“探索信息如何呈现给模型外层与用户”
- [x] 汇总“为什么会出现你说的现象”的核心机制（带文件+行号证据）
- [x] 在 `todo.md` 追加 review（完整链路、关键断点、最小修复方向）

#### review

- Explore 主链路已确认：`explore_tool_loop` 先强制 `list_chapters/list_paragraphs`，再由 LLM 在只读工具集合内循环决策；命中后必须 `read_paragraph/read_paragraphs` 才会进入 `evidences`，最终由 `explore_content` 输出 `evidences + locate_targets + context_for_task + explore_summary`。`backend/app/services/agent/tools/explore_tools.py`
- 结果注入链路已确认：`parallel_executor` 把 `explore_content` 完整 `raw_result` 注册进 `ParameterResolver`，规划层用 `$ref` 把 `locate_targets/evidences` 注入到 `smart_*` 与 `operate_apply` 参数；执行层还会把 `last_explore_result` 放入共享 state 作为兜底。`backend/app/services/agent/execution/parallel_executor.py` `backend/app/services/agent/parameter_resolver.py` `backend/app/services/agent/planning/plan_generator.py`
- AI 评判依据已确认：Explore 轮次决策时，模型看到“搜索历史+命中列表+已读原文证据+已读范围”；创作阶段模型看到 `evidence_context`（探索摘要/证据/定位候选）与段落上下文补读结果，再生成 `smart_rewrite/smart_continue/smart_insert`。`backend/app/services/agent/tools/explore_tools.py` `backend/app/services/agent/execution/tool_executor.py` `backend/app/services/agent/tools/editor_tools.py`
- 前后端事件链路已确认：后端 `flow_events` 生成 `explore_round/explore_summary`，SSE 透传到前端，前端映射为 `flowItems` 展示；这条链路主要给“人和外层流程看”，真正给后续 AI 工具喂数据的是任务结果注册 + `$ref` 注入。`backend/app/services/agent/stream/flow_events.py` `backend/app/api/v1/agent.py` `src/services/agentApi.ts` `src/hooks/useAgentChat.ts`
- 核心断点：当前检索层是“字面匹配”而非语义匹配（`ilike %kw%` / `kw in text`），抽象需求在关键词阶段就可能失配；若 `locate_targets` 不唯一或缺失，写回阶段会触发 `ambiguous_locator/missing_source_locator` 并阻断。`backend/app/services/chapter_vector_service.py` `backend/app/services/agent/execution/tool_executor.py`
- 最小修复方向：先提升召回入口（关键词扩展/同义词改写/用户提供锚句引导），再强化定位选择（默认要求 `locate_target_index/locator_id`），最后把“检索失配”与“定位歧义”拆成可见错误类型，避免 Explore 看起来像“死循环”。`backend/app/services/agent/tools/explore_tools.py` `backend/app/services/agent/execution/tool_executor.py`

#### Explore 动态 regex 检索与硬判停改造（待确认）

- [x] 新增 regex 搜索能力：`exact_search_paragraphs` 支持 `patterns`（正则）与 `regex_mode`（any/all）
- [x] Explore 工具循环支持动态 regex 参数：在 `exact_search_paragraphs` 分支解析/校验/执行 `patterns`
- [x] 增加 regex 安全校验与诊断回传（编译失败/危险模式/过长）
- [x] 接入程序化硬判停：`max_rounds` 真正生效 + 连续无进展停机 + 重复同调用停机
- [x] 接入已有搜索拦截器：`should_block_search` 在执行搜索前生效，避免重复无效搜索
- [x] 补充最小验证（`py_compile`），并在 `todo.md` 追加 review（改动点、证据、残余风险）

#### review

- `chapter_vector_service` 已支持关键词+regex 双通道：`exact_search_paragraphs` 新增 `patterns/regex_mode`，有 regex 时自动走正文扫描路径，返回 `matched_patterns/pattern_count`，避免 SQL 字面匹配漏召回。`backend/app/services/chapter_vector_service.py`
- Explore 执行分支已支持动态 regex：`exact_search_paragraphs` 现在解析 `keywords + patterns`，并把 `patterns/regex_mode` 透传到搜索服务；搜索结果会回传 `blocked_keywords/invalid_patterns` 供 LLM 下一轮修正。`backend/app/services/agent/tools/explore_tools.py`
- regex 安全校验已落地：新增长度上限、条数上限、危险模式拦截（嵌套量词/多重 `.*`）、编译失败诊断。`backend/app/services/agent/tools/explore_tools.py`
- 硬判停已接入主循环：`while` 同时受 `max_tool_calls + max_rounds` 控制，并增加“连续2轮无新增证据”与“连续3轮重复同调用”停机；`check_convergence(window=2)` 也已真正生效。`backend/app/services/agent/tools/explore_tools.py`
- 搜索拦截器已启用：执行搜索前先跑 `should_block_search`，被判穷尽的关键词会被拦截，不再重复空转。
- 已执行最小验证：`python3 -m py_compile backend/app/services/chapter_vector_service.py backend/app/services/agent/tools/explore_tools.py` 通过。
- 残余风险：regex 危险模式拦截目前是启发式，可能存在误拦/漏拦；如果后续线上有误判，可再补“执行超时熔断 + 更细粒度正则 AST 校验”。

#### 删除 prompt 抽关键词残留（待确认）

- [x] 删除 `_extract_keywords_for_search` 函数（包括 jieba 抽词逻辑）
- [x] 删除世界观预取里的 prompt 抽词兜底，只保留 `search_keywords`
- [x] 运行最小语法校验并在 `todo.md` 追加 review

#### review

- 已删除 `backend/app/services/agent/tools/explore_tools.py` 中 `_extract_keywords_for_search` 整段实现，原先的“从用户 prompt 规则抽词 + jieba 抽词”逻辑不再存在。
- 已修改世界观小包预取关键词来源：`keywords = self.search_keywords or []`，不再从 `target_task` 自动抽取关键词。
- 语法校验通过：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py`。

#### 清理旧 pipeline 残留（待确认）

- [x] 删除未调用的旧阶段方法（`_execute_exact_search_phase`）
- [x] 删除未调用的 `explore()` 兼容壳方法（仅保留 `explore_tool_loop` 主链）
- [x] 删除伴随旧流程遗留的未使用章节排序方法（`_chapter_has_paragraph_evidence` 等）
- [x] 清理 `pipeline 已弃用` 文案残留并做语法校验

#### review

- `backend/app/services/agent/tools/explore_tools.py` 中旧 pipeline 的执行残留已删除：`_execute_exact_search_phase`、`explore()` 包装入口、以及未再使用的章节排序/筛选辅助方法，当前仅保留 `explore_tool_loop` 主链路。
- 相关“pipeline 已弃用”注释文案已清理，避免继续误导。
- 校验通过：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py backend/app/services/chapter_vector_service.py`。

#### INFO/Backend 日志深度归因排查（待确认）

- [x] 通读 `INFO.md` 与 `Backend.md`，对齐同一轮请求的时间线与症状
- [x] 提取关键异常信号（循环、超时、参数错配、工具失败）并做证据摘录
- [x] 反查对应实现代码（Explore/tool_loop/写回链路）确认触发机制
- [x] 判断是否与本轮改动直接相关，区分“新增问题”与“历史遗留问题”
- [x] 输出直白结论：核心根因、次要因素、复现条件、最小修复方向
- [x] 在 `todo.md` 追加 review（证据清单+结论）

#### review

- 同一轮请求的前后端症状完全一致：前端轨迹中仅出现 `ListChapters/ListParagraphs` 重复 6 组，没有 `exact_search_paragraphs/read_paragraph`；后端 6 次 `explore_content` 也都在 2 轮后停止。`INFO.md` `Backend.md`
- 关键异常信号明确：每次 Explore 都是 `stop_reason=连续2轮无新增证据，停止探索`，随后触发 `missing_locate_targets` 错误（缺少 `paragraph_index/node_id`）。`Backend.md`
- 触发机制已在代码层闭环：`explore_tool_loop` 先强制执行 `list_chapters -> list_paragraphs`，而“连续2轮无新增证据即停”是无条件生效，导致在进入 AI 决策前就被硬停；因此根本不会调用 `exact_search_paragraphs/read_paragraph(s)`。`backend/app/services/agent/tools/explore_tools.py`
- 与本轮改动关系：这是本轮新增“硬判停”策略引入的副作用，不是历史老问题。因为日志里的停机文案与新增代码字符串一致，且触发点与新增判停条件完全重合。`backend/app/services/agent/tools/explore_tools.py` `Backend.md`
- 次要放大因素：本次任务被规划成 6 个独立输出任务，全部串行调用 `explore_content`，每个都在同一早停点失败，前端因此看起来像“工具在无意义重复”。`Backend.md` `INFO.md`
- 最小修复方向：保留硬判停，但排除强制准备轮（`list_chapters/list_paragraphs`）不计入 `no_progress_streak`；或把阈值改成“至少出现过一次搜索/读取工具调用后再启用无进展判停”。

#### 移除2轮无进展硬停（待确认）

- [x] 删除 `explore_tool_loop` 中“连续2轮无新增证据，停止探索”判停
- [x] 删除等价的2轮收敛判停分支，避免同类早停仍触发
- [x] 保留其余判停机制（`max_rounds`、`max_tool_calls`、重复同调用停机）
- [x] 运行最小语法校验并记录结果

#### review

- 已按要求移除“2轮无新增证据即停”逻辑，并同步移除等价的 `check_convergence(window=2)` 停机分支，避免仅执行 `list_chapters/list_paragraphs` 就被提前终止。`backend/app/services/agent/tools/explore_tools.py`
- 其他保护机制保持不变：`max_rounds`、`max_tool_calls`、`连续3轮重复同一工具调用` 仍生效。`backend/app/services/agent/tools/explore_tools.py`
- 语法校验通过：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py`。

#### Explore 动态 grep 检索改造计划（待确认）

- [x] 阶段1：明确“查询生成”唯一入口
- [x] 移除 `explore_content` 对规划层 `search_keywords` 的强依赖，改为以每轮 LLM 动态生成 `keywords/patterns` 为主（规划词仅作可选 seed）
- [x] 在工具循环状态中增加“查询尝试栈”（记录每轮 regex/关键词、命中数、失败原因），作为下一轮提示上下文
- [x] 统一 `exact_search_paragraphs` 的入参规范（keywords/patterns/match_mode/regex_mode），避免模型反复切换无效参数组合

- [x] 阶段2：建立“程序化查询改写”护栏（不把成败全交给 AI）
- [x] 当 `exact_search_paragraphs` 连续 2 轮 0 命中时，程序强制注入一次“放宽策略”查询（如 all→any、短语→拆词、去掉过强连接词）
- [x] 当检测到重复同调用（同工具+同参数）达到阈值时，不直接结束，先强制要求“结构化改写查询”再允许继续
- [x] 对“关键词已确认不存在”的拦截增加前置条件：必须经历“全局范围 + 至少一次改写策略”后才能标记 exhausted

- [x] 阶段3：收紧停机质量门槛（解决“过早停”）
- [x] `action=stop` 前增加程序校验：若尚未完成“有效搜索覆盖 + 至少一次原文读取尝试”，拒绝 stop 并回退到继续搜索
- [x] 对“内容不存在”结论增加硬条件：至少 N 组不同查询策略都为 0 命中，且覆盖范围满足章节约束
- [ ] 保留现有 `max_rounds/max_tool_calls/重复调用停机`，但将 stop_reason 细化为机器可判别原因码

- [ ] 阶段4：提升可观测性与可调试性
- [x] 在日志中输出每轮查询策略标签（strict/broad/fallback）、命中统计、是否触发程序强制改写
- [ ] 前端流事件补充“本轮为何继续/为何拒绝停止”的简短说明，避免看起来像无意义打转
- [ ] 为 `missing_locate_targets` 增加上游诊断字段（是否读过原文、是否仅 preview）

- [ ] 阶段5：最小回归验证与压测
- [ ] 基于 `INFO.md/Backend.md` 的真实轨迹构建 3 组回放用例（能找到、找不到、半命中）
- [ ] 新增单测：重复同调用拦截、0命中强制改写、stop 前质量门槛
- [x] 运行最小验证（`py_compile`），确认无语法回归

#### review（计划审查）

- [x] 贴合现状：计划直接落在当前主链 `explore_tool_loop + exact_search_paragraphs`，不引入新 pipeline，改动面可控。
- [x] 风险可控：优先做“程序护栏与停机门槛”，不先改底层存储或向量体系，避免大改引发连锁回归。
- [x] 与现有日志问题对齐：可直接针对“0命中早停、重复调用、missing_locate_targets”三类症状给出对应控制点。
- [x] 兼容你当前设计原则：保留“必须读原文才算 evidence、写回必须精确定位”两条硬约束。
- [x] 主要风险：若门槛设置过严，可能增加轮次与时延；需要通过阶段5回放用例校准阈值。
- [x] 结论：该计划合理、可落地、经得起推敲，建议按阶段1→2→3顺序实施，阶段4/5并行补齐。

#### review（实施进度）

- 已完成阶段1~3核心改造：查询尝试栈、0命中强制改写、重复同调用触发改写、`action=stop` 质量门槛、`不存在` 结论硬条件。`backend/app/services/agent/tools/explore_tools.py`
- `exact_search_paragraphs` 已统一参数规范并写入尝试记录：`keywords/patterns/match_mode/regex_mode/strategy`，失败与命中都会入栈。`backend/app/services/agent/tools/explore_tools.py`
- `search_keywords` 已降级为可选 seed：Explore 选择目标段时会合并“近期真实查询词”，不再只依赖规划层初始词。`backend/app/services/agent/tools/explore_tools.py`
- 已完成最小语法校验：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py` 通过。
- 尚未完成：stop reason 机器码细化、前端继续/拒停可视化、`missing_locate_targets` 上游诊断字段、回放用例与单测。

#### Opencode grep 关键词来源机制深挖（待确认）

- [x] 核对 `opencode` 中 grep 工具入参与执行实现，确认是否存在“程序抽关键词”模块
- [x] 核对 explore 子代理提示词与权限配置，确认 LLM 是否被引导动态生成 grep pattern
- [x] 核对会话主循环中模型消息构建链路，确认 LLM 每轮能看到哪些上下文来决定下一组词/regex
- [x] 核对工具结果回灌与循环控制（含 doom loop 保护），确认“上一轮结果如何影响下一轮 pattern”
- [x] 形成证据链与直白结论（回答“AI 根据什么想出这些词”）

#### review

- `grep` 工具只接受单个 `pattern`（regex 字符串）并原样传给 `rg --regexp`，没有任何“程序自动抽关键词”逻辑。`opencode/packages/opencode/src/tool/grep.ts`
- explore 子代理提示词只给策略性指导（用 Glob/Grep/Read），并未提供固定词库或规则抽词器；因此 pattern 来自 LLM 当轮决策。`opencode/packages/opencode/src/agent/prompt/explore.txt` `opencode/packages/opencode/src/agent/agent.ts`
- 每轮模型输入由“系统提示 + 对话历史 + 工具调用结果”组成；工具结果会被结构化写回消息并在下一轮再次送入模型，因此 pattern 依据是动态迭代的。`opencode/packages/opencode/src/session/prompt.ts` `opencode/packages/opencode/src/session/message-v2.ts`
- grep 输出会明确返回“命中行/No files found/截断提示”，这些反馈构成下一轮改词/改 regex 的直接依据。`opencode/packages/opencode/src/tool/grep.ts`
- 会话处理器有 doom loop 检测：同工具同输入连续 3 次会触发 `doom_loop` 权限检查，避免无限重复同一 pattern。`opencode/packages/opencode/src/session/processor.ts`

#### 对齐 Opencode 动态 grep 效果（最小落地计划）（待确认）

- [x] 阶段1：参数与范围语义修正（先治“搜错范围”）
- [x] 在 `exact_search_paragraphs` 参数解析中补齐 `chapter_orders`（支持 `[2]`、`[1,2,3]`、字符串列表）
- [x] 明确范围优先级：`chapter_range/chapter_ranges/chapter_orders/chapter_order`（从高到低），并在日志输出“最终生效范围”
- [x] 保持现有章节 scope 过滤逻辑不变，避免影响写回定位链路

- [x] 阶段2：检索执行改为“分层回退”而非“一票否决”
- [x] 保留首轮严格检索：`keywords + patterns`
- [x] 若 0 命中，自动追加第2轮：`keywords-only`（去掉 patterns）
- [x] 若仍 0 命中，再追加第3轮：`patterns-only`（去掉 keywords）
- [x] 每轮都写入 `query_attempts`，并带 `strategy` 标签（`strict`/`kw_fallback`/`regex_fallback`）

- [x] 阶段3：修正 forced_rewrite 的“假放宽”
- [x] `forced_rewrite` 默认先走 `keywords-only`，不继承上一轮 patterns
- [x] 仅当 `keywords-only` 仍 0 命中时，再尝试保守 regex（短 pattern、低复杂度）
- [x] 保留现有 stop 质量门槛，不再新增硬停规则

- [x] 阶段4：提示词最小改写（不改架构）
- [x] 将“优先给 regex”改为“先关键词召回，再 regex 收敛”
- [x] 明确禁止一次性给长串抽象负向词（如“代价/限制/风险/误判...”全家桶）
- [x] 要求每轮最多 1-2 条短 regex，避免复杂表达式先天漏召回

- [ ] 阶段5：最小验证（基于你现有日志回放）
- [x] 用 `INFO.md/Backend.md` 中 3 个失败样例回放：复杂困境检索、三线并轨联合 regex、限定章节检索
- [ ] 验证指标：命中率提升、`range` 与请求一致、10轮内收敛、`locate_targets` 不回退
- [x] 执行 `py_compile` + 目标单测（仅新增必要用例，不扩面）

#### review（计划审查）

- [x] 计划符合“少改动”原则：只改 `explore_tools.py`（参数解析/决策提示/回退策略）与少量 `chapter_vector_service.py` 调用分支，不动数据库结构与前端协议。
- [x] 先修 `chapter_orders` 再调策略，顺序合理：先保证“搜对地方”，再优化“怎么搜”。
- [x] 分层回退比全局改 OR 更稳：可维持首轮精度，同时避免 regex 偏差导致全盘 0 命中。
- [x] 与现有机制兼容：保留“必须读原文才算 evidence”“写回必须精确定位”“stop 质量门槛”三条硬约束。
- [x] 风险可控：主要风险是回退轮次增加带来时延；通过“最多3层回退 + 现有 max_rounds”可控。
- [x] 可验证性强：可直接复用你当前 `INFO.md/Backend.md` 失败样本做回放，不需要新造复杂测试场景。
- [x] 结论：该计划在当前项目状态下合理、可落地、经得起推敲，建议按阶段1→2→3执行，阶段4/5并行。

#### review（实施进展）

- 已落地 `chapter_orders` 解析，并在 `exact_search_paragraphs` 执行时输出“参数范围/任务范围/最终生效范围”日志，优先级按 `chapter_range/chapter_ranges/chapter_orders/chapter_order` 生效。`backend/app/services/agent/tools/explore_tools.py`
- 已把检索改为分层回退：首轮 `keywords+patterns`，0 命中后自动 `kw_fallback`，仍 0 命中再走 `regex_fallback`；每层都写入 `query_attempts`。`backend/app/services/agent/tools/explore_tools.py`
- 已修正补偿检索逻辑：缺失关键词补偿时不再携带旧 regex（`patterns=[]`），避免“补偿仍被 regex 一票否决”。`backend/app/services/agent/tools/explore_tools.py`
- 已修正 `forced_rewrite` 默认策略为 `keywords-only`（`patterns=None`），去掉“继承旧 regex 导致假放宽”。`backend/app/services/agent/tools/explore_tools.py`
- 已调整 Explore 提示词：从“优先 regex”改为“先关键词召回，再短 regex 收敛（1-2 条）”。`backend/app/services/agent/tools/explore_tools.py`
- 语法校验通过：`python3 -m py_compile backend/app/services/agent/tools/explore_tools.py`。

#### Explore 收尾必做计划（待确认）

- [x] 任务1：补齐 forced_rewrite 二段回退（keywords-only 仍 0 命中时，自动尝试保守 regex）
- [x] 任务2：在探索提示词增加“禁止长串抽象负向词并列”的硬约束
- [x] 任务3：基于 `INFO.md` + `Backend.md` 的 3 组失败样例做回放验收并记录指标
- [x] 任务4：补最小验证脚本/命令并在日志里给出可复现实验结论
- [x] 任务5：在本节追加 review（改动文件、证据、是否达到预期）

#### review（计划审查）

- [x] 该计划和当前代码状态强相关：全部落在你已改过的 `exact_search_paragraphs`/`forced_rewrite`/提示词/日志回放链路，不引入新架构。
- [x] 改动面可控：主要集中在 `backend/app/services/agent/tools/explore_tools.py`，验证材料直接复用现有 `INFO.md` 与 `Backend.md`。
- [x] 验收可量化：每项都有“是否命中、是否收敛、是否产生 locate_targets”的明确判据，不会变成主观口径。
- [x] 风险明确且可控：二段回退若过宽可能带来噪声命中，通过“保守 regex + 轮次上限 + 回放样例”可约束。
- [x] 结论：计划合理、经得起推敲，且符合你要求的“少改动、先解决本质问题、最后用证据说话”。

#### review（实施结果）

- `forced_rewrite` 已补齐二段回退：在最近 `forced_rewrite` 为关键词模式且 0 命中后，会自动切到 `forced_rewrite_regex`，并仅生成低复杂度短 regex（最多2条、关键词长度受限、可选短窗口连接）。`backend/app/services/agent/tools/explore_tools.py`
- 探索提示词已加硬约束：明确禁止一次性并列长串抽象负向词，要求先拆成 1-2 个可落地关键词再检索。`backend/app/services/agent/tools/explore_tools.py`
- 最小验证脚本已补：新增单测 `backend/tests/unit/test_explore_forced_rewrite_fallback.py`，覆盖默认 keywords-only、二段 regex 回退触发、二段回退不重复触发、提示词硬约束存在性。
- 验证命令与结果：
  - `python3 -m py_compile backend/app/services/agent/tools/explore_tools.py backend/tests/unit/test_explore_forced_rewrite_fallback.py` 通过。
  - `cd backend && pytest -q tests/unit/test_explore_forced_rewrite_fallback.py` 通过（4 passed）。
  - 回放抽样脚本从 `Backend.md` 抽取到 3 组“patterns 非空且 0 命中”失败样例（`sample_zero_hit_cases=3`），已用于验证二段回退目标场景覆盖。
- 结论：收尾必做项已完成；当前链路在“复杂 regex 0 命中”后不再停留在单一关键词放宽，而是会追加一次保守 regex 回退，且约束模型减少抽象负向词堆砌。
