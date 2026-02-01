# TODO

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

- [ ] 明确“按需取回”策略：哪些场景触发读取完整 Explore（证据/原文/截断补全/用户明确要求）
- [ ] Explore 结果落盘（Artifact）：保存完整结果+元数据（work_id/chapter_id/关键词/时间/范围/版本）
- [ ] explore_content 返回 artifact_id + 摘要/预览（不把全文塞进上下文）
- [ ] 新增 load_explore_artifact 工具：按 artifact_id 取回全文或指定片段
- [ ] 上下文记忆只保存“引用指针”（artifact_id + 摘要），避免重复探索且控制上下文体积
- [ ] 失效/清理策略：章节更新/导入/恢复触发失效；保留期与大小上限
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
