# TODO

## 计划
- [x] 确认工具分类依据文档（`docs/agent-tools-refactor/01-overview.md`、`docs/iterative-agent/08-validation-report.md`）
- [x] 在答复中澄清工具分类为 Search/Read/Analyze/Update，并说明 Create/Operate 的语境
- [x] 补充 Review 总结

## 计划（Search/Read 说明）
- [x] 核对 Search 类工具定义与列表（`docs/agent-tools-refactor/02-search-tools.md`）
- [x] 核对 Read 类工具定义与列表（`docs/agent-tools-refactor/03-read-tools.md`）
- [x] 汇总为简洁答复并更新 Review

## 计划（完整上下文获取时机）
- [x] 核对规划提示中 get_writing_context 使用条件（`backend/app/services/agent/prompts/planning_prompts.py`）
- [x] 核对决策提示/示例与快速路径说明（`backend/app/services/agent/prompts/decision_prompts.py`、`backend/app/services/agent/prompts/planning_examples.py`、`backend/app/services/agent/planning/quick_path.py`）
- [x] 核对分析工具是否会自动补齐上下文（`backend/app/services/agent/tools/analysis_tools.py`）
- [x] 汇总为答复并更新 Review

## 计划（复杂测试提示词）
- [x] 阅读小说素材关键章节与人物设定（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计跨章节插入的复杂测试提示词（含明确定位锚点/位置/风格约束）
- [x] 更新 Review

## 计划（后台日志分析）
- [x] 阅读 `Backend.md` 日志并定位失败节点
- [x] 结合代码路径分析原因（参数解析/工具输出）
- [x] 总结问题与可行修复建议，并更新 Review

## 计划（修复 get_writing_context 输出）
- [x] 在 `backend/app/services/agent/execution/tool_executor.py` 中为 `extract_result` 增加 `get_writing_context` 分支
- [x] 更新 Review 记录改动与影响范围

## 计划（最新日志核验）
- [x] 阅读 `Backend.md` 最新日志，确认占位符解析与 locate_content 结果
- [x] 对照修复点验证是否仍有 chapter_id 误传或新错误
- [x] 汇总结论并更新 Review

## 计划（前端修订不显示排查）
- [x] 核对前端修订事件派发与字段（`src/hooks/useAgentChat.ts`）
- [x] 核对编辑器修订展示与跨章节逻辑（`src/components/editor/NovelEditor.tsx`、`src/store/editorStore.ts`、`src/utils/revisionLocator.ts`）
- [x] 对照后端修订事件字段（`backend/app/services/agent/langgraph_agent.py`、`backend/app/services/agent/stream/flow_events.py`）
- [x] 汇总结论与可能原因/修复建议，并更新 Review

## 计划（跨章节切换不显示修订）
- [x] 核对跨章节修订在切换章节时的触发条件与过期逻辑（`src/components/editor/NovelEditor.tsx`）
- [x] 核对内容刷新/缓存是否阻止修订重建（`src/components/editor/NovelEditor.tsx`、`src/services/EditorSyncService.ts`、`src/views/WorkDetailView/index.tsx`、`src/components/editor/AIPanel.tsx`、`src/hooks/useAgentChat.ts`）
- [x] 汇总结论与可行修复建议，并更新 Review

## 计划（跨章节修订测试提示词-二次）
- [x] 复核小说素材章节与关键句（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计一条高复杂度跨章节修改测试 prompt（包含定位锚点、替换+插入、明确“切回目标章节查看修订”的验证步骤）
- [x] 更新 Review

## 计划（跨章节修订测试日志核验）
- [x] 阅读 `Backend.md` 最新日志，确认跨章节 replace/insert 的定位与 apply_chapter_edit 结果
- [x] 阅读前端日志 `log/localhost-1768280433702.log` 与前端执行轨迹 `INFO.md`
- [x] 对照前后端事件链（approval_request/revision/agent-show-revision），核对 chapter_id 与锚点字段
- [x] 汇总结论与可能原因，并更新 Review

## 计划（跨章节修订展示修复）
- [x] 将跨章节修订缓存改为按章节队列，避免后续修订覆盖前一条（`src/store/editorStore.ts`）
- [x] 收到 `agent-show-revision` 时按章节追加待处理修订，并在切换章节时逐条应用（`src/components/editor/NovelEditor.tsx`）
- [x] 调整过期策略（延长或仅在成功展示后清理），避免切回章节时被提前清除（`src/components/editor/NovelEditor.tsx`）
- [x] （可选）跨章节 insert/continue 使用 nodeId/paragraphIndex/锚点计算标记范围，减少“找不到 replacement”概率（`src/components/editor/NovelEditor.tsx`、`src/utils/revisionLocator.ts`）
- [x] 更新 Review 记录变更与验证结果

## 计划（复杂测试提示词-三次）
- [x] 阅读小说素材中第2-5章关键段落（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计 1 条高复杂度跨章节测试 prompt（含明确锚点、替换+插入、位置校验指令）
- [x] 更新 Review

## 计划（修订切换后消失排查）
- [x] 阅读最新 `Backend.md`、前端日志 `log/localhost-1768283679274.log` 与执行轨迹 `INFO.md`
- [x] 对照事件链（approval_request/agent-show-revision/修订标记应用/章节切换）核对是否触发清理或重置
- [x] 检查章节切换时编辑器内容重载与本地缓存是否覆盖修订标记（`src/components/editor/NovelEditor.tsx`、`src/views/WorkDetailView/index.tsx`）
- [x] 检查修订标记是否仅在内存中，未随内容保存导致切换时丢失（`src/components/editor/AIRevisionBar.tsx`、`src/components/editor/AIRevisionMark.tsx`）
- [x] 汇总结论与修复建议，并更新 Review

## 计划（修订标记跨章节持久化）
- [x] 修订入队去重，并在本章显示时标记为“已应用”以避免重复插入（`src/store/editorStore.ts`、`src/components/editor/NovelEditor.tsx`）
- [x] 对当前章节的修订也入队，切章后可重建修订标记（`src/components/editor/NovelEditor.tsx`）
- [x] 采纳/弃用时移除本章待处理修订（批量时清空全部），保证切换后不再重建（`src/components/editor/NovelEditor.tsx`）
- [x] 更新 Review 记录变更与验证建议

## 解决方案
- 工具分类当前为 Search / Read / Analyze / Update 四大类（见 `docs/agent-tools-refactor/01-overview.md`），Update 覆盖创建/修改/删除等操作；Create/Operate 更像是阶段反馈用语，不是工具分类（见 `docs/iterative-agent/08-validation-report.md`）。
- Search 类工具负责定位内容位置，返回位置信息和片段（`search_content`、`locate_content`）；Read 类工具负责获取完整内容并预处理，当前为 `get_writing_context`（见 `docs/agent-tools-refactor/02-search-tools.md`、`docs/agent-tools-refactor/03-read-tools.md`）。
- 获取完整上下文的触发主要来自规划提示：创作请求或需要章节/世界观内容的查询与分析会先调用 `get_writing_context`；用户选中文本需先读章节；一致性分析在未提供 context 时会自动补齐（见 `backend/app/services/agent/prompts/planning_prompts.py`、`backend/app/services/agent/tools/analysis_tools.py`）。
- 跨章节插入准确定位：先用 `locate_content` 获取目标章节的 `chapter_id`、`node_id`、`paragraph_index`、锚点；`apply_chapter_edit` 侧优先用 `node_id`/`paragraph_index`/锚点定位插入，必要时可先 `get_writing_context` 获取章节ID，再定位（见 `docs/agent-tools-refactor/02-search-tools.md`、`backend/app/services/agent/prompts/planning_examples.py`、`backend/app/services/agent/tools/editor_tools.py`）。
- 基于小说素材，提供 1 个多步骤、跨章节定位插入的复杂测试 prompt，明确锚点与约束。
- 日志中的 locate_content 失败与参数解析结果有关，需要核对 `get_writing_context` 输出结构与 ParameterResolver 的字段提取路径。
- 采用方案 1：在 `backend/app/services/agent/execution/tool_executor.py` 的 `extract_result` 中对 `get_writing_context` 返回 `data["context"]`（若为 JSON 字符串则直接透传），保证占位符能解析到 `chapters`。
- 通过最新日志验证修复是否生效，重点检查 locate_content 的 chapter_id 是否为 UUID 而非整段 JSON。
- 前端未展示修订可能与跨章节逻辑（目标章节未打开/超时/内容未刷新）、或修订事件字段缺失（chapterId/originalContent）有关，需结合事件派发与编辑器展示路径核对。
- 跨章节切换未显示修订：需要确认切到目标章节时 content 是否已刷新且包含 replacement；若未包含会等待或 5 分钟过期；另需检查 localStorage 旧内容是否覆盖新内容，导致“看不到修订标记”。
- 基于小说素材提供新的复杂测试 prompt，用于验证跨章节修订在切换章节时是否显示红删绿增。
- 根据最新后台日志核验跨章节替换/插入是否成功以及修订事件字段是否完整。
- 结合前端日志与执行轨迹核对修订事件是否触发/被消费，并定位跨章节切换无标记的断点。
- 前端日志显示跨章节修订在切换章节时被判定为“已过期并清除”，且跨章节修订只保存单条，后续修订会覆盖前一条。

## Review
- 已核对工具分类文档，确认为 Search / Read / Analyze / Update 四大类。
- Create/Operate 出现在阶段反馈语境，不是工具分类；Update 覆盖创建/修改/删除等操作。
- Search：定位内容位置，返回位置与片段，工具为 `search_content`、`locate_content`（`docs/agent-tools-refactor/02-search-tools.md`）。
- Read：获取完整内容并做预处理（选择/压缩/格式化），不做语义推理，工具为 `get_writing_context`（`docs/agent-tools-refactor/03-read-tools.md`）。
- 完整上下文触发点：创作请求或涉及章节/世界观内容的查询与分析时由规划提示生成 `get_writing_context`；用户选中文本要求“先读章”；一致性分析未提供 context 时会自动补齐（`backend/app/services/agent/prompts/planning_prompts.py`、`backend/app/services/agent/prompts/decision_prompts.py`、`backend/app/services/agent/tools/analysis_tools.py`）。
- 快速路径/简单问候不走上下文读取；简单章节信息查询走旧读取工具（`backend/app/services/agent/planning/quick_path.py`）。
- 已完成素材阅读并设计复杂测试 prompt，覆盖跨章节定位、锚点与写入约束。
- 日志失败点：`locate_content` 收到的 `chapter_id` 是整段 JSON（`Backend.md` 12:05:43 左右），导致 UUID 解析失败。
- 根因：`get_writing_context` 标准工具输出为 `{"context": "<json字符串>"}`，`ParameterResolver` 取 `$TASK_1.chapters[0].id$` 时找不到 `chapters` 字段，降级返回完整结果，最终把整段 JSON 当成 `chapter_id`（见 `backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/parameter_resolver.py`）。
- 可行修复：在 `backend/app/services/agent/execution/tool_executor.py` 的 `extract_result` 增加 `get_writing_context` 分支，返回 `data["context"]`（若为 JSON 字符串直接透传），或在 `backend/app/services/agent/langgraph_tools.py` 的 `get_writing_context_executor` 中将 `context` 解析为对象并置顶输出，避免下游路径失配。
- 已采用方案 1：`extract_result` 对 `get_writing_context` 直接返回 `data["context"]`（非字符串则序列化），保证占位符可以解析到 `chapters`。
- 最新日志显示修复生效：`$TASK_1.chapters[0].id$`、`$TASK_1.chapters[1].id$` 正常解析为 UUID，`locate_content` 成功执行且未再出现 chapter_id 误传（`Backend.md` 12:22:20~12:22:44）。
- 前端修订不显示的高概率原因：修订是“跨章节”变更，`agent-show-revision` 事件携带的 `chapterId` 与当前编辑器 `chapterId` 不一致时，NovelEditor 会只存入 `pendingCrossChapterRevision` 并提示“切换查看”，不会在当前章节显示红删绿增（`src/components/editor/NovelEditor.tsx`）。
- 次要原因：修订事件在 apply_chapter_edit 后才触发，编辑器已加载“修改后的正文”，跨章节逻辑需要匹配 replacement 才重建标记；若正文未刷新或 replacement 不在当前 content，修订会延迟/过期（5分钟）而不显示。
- 已补充跨章节修订测试 prompt（含切回目标章节验证步骤）。
- 后台日志显示第2章替换定位为 LLM 辅助第15段（node_id=6nf35ycf），第3章插入定位落在“开头”（paragraph_index=0, node_id=hicij01s），apply_chapter_edit 均执行成功（`Backend.md`）。
- `INFO.md` 执行轨迹与后台一致：第2章 replace 成功，第3章 insert 因 locate_content 未命中目标句而落在开头；AI 总结提示“请切回第2章/第3章查看修订”。
- 前端日志显示切换到第3章时触发“跨章节修订已过期，清除”，说明待处理修订因 5 分钟过期策略被清理，导致红删绿增未展示（`log/localhost-1768280433702.log`）。
- 当前跨章节修订只保留单条（`pendingCrossChapterRevision`），多条跨章节修订会被后续覆盖，早先章节的修订无法在切回时重建（`src/store/editorStore.ts`、`src/components/editor/NovelEditor.tsx`）。
- 前端日志出现多次“刷新章节列表与当前内容”，说明内容刷新链路有触发，但修订展示仍受过期与单条覆盖影响。
- 已将跨章节修订缓存改为队列（数组），避免后续修订覆盖前一条（`src/store/editorStore.ts`）。
- 跨章节修订按章节队列逐条应用，过期窗口延长至 30 分钟；若正文未更新则保留，其他情况（成功/失败）均移除该条（`src/components/editor/NovelEditor.tsx`）。
- 跨章节 insert/continue 复用 nodeId/paragraphIndex 约束搜索范围，并加入 before/after anchor 兜底查找，降低 replacement 命中失败概率（`src/components/editor/NovelEditor.tsx`）。
- 已基于第2-5章内容提供一条高复杂度跨章节测试 prompt（含替换+插入+位置校验指令）。
- 最新日志中第3章定位返回“定位到开头”，但仍执行了 insert（与“找不到就停止”要求不一致），说明执行链未中止该任务（`Backend.md`、`INFO.md`）。
- 切换章节后修订标记消失的根因：修订标记仅存在于编辑器内存；章节切换会重载后端正文（不含 mark 标签），且跨章节修订在显示后被移除，无法再次重建（`src/components/editor/NovelEditor.tsx`、`src/components/editor/AIRevisionMark.ts`、`src/views/WorkDetailView/index.tsx`）。
- 现状下只有在“采纳/弃用”事件触发并保存时才会固化标记或回写正文；否则切章导致标记丢失，与预期不符。

## 计划（/works 与 /login 循环跳转）
- [x] 核对登录页与认证布局的跳转条件，定位循环触发点（`src/views/AuthView/index.tsx`、`src/components/layout/AuthLayout.tsx`、`src/store/authStore.ts`）
- [x] 调整登录页自动跳转条件，与认证布局保持一致，避免 user 未就绪时跳转（`src/views/AuthView/index.tsx`）
- [x] 自查未登录访问 `/works`、已登录访问 `/login`、正常登录流程的跳转行为

## 解决方案（/works 与 /login 循环跳转）
- 根因：登录页自动跳转只判断 `isAuthenticated`，登录流程会先 `login(null, token...)` 使 `isAuthenticated=true` 但 `user=null`，而认证布局要求 `isAuthenticated && user`，导致 `/login` 与 `/works` 反复互跳。
- 修复：登录页自动跳转条件增加 `user` 判断，与认证布局一致，避免 user 未加载完成时跳转。

## Review（/works 与 /login 循环跳转）
- 登录页自动跳转条件改为 `hasHydrated && isAuthenticated && user`，与认证布局一致，避免 user 未就绪时跳转（`src/views/AuthView/index.tsx`）。
- 未做实际运行验证，仅完成逻辑自查；如仍有跳转异常，优先检查登录后 `user` 拉取是否失败以及 401 重定向逻辑。

## 计划（阅读页右侧目录面板高度对齐）
- [x] 定位阅读页右侧面板的定位样式与顶部偏移来源（`src/components/library/NovelReader.tsx`）
- [x] 调整面板顶部偏移，使其与页眉顶部对齐（`src/components/library/NovelReader.tsx`）
- [x] 自查面板展开/收起时与顶部导航栏的遮挡关系

## 解决方案（阅读页右侧目录面板高度对齐）
- 右侧面板使用 `fixed top-11` 造成顶部留空；将其改为 `top-0` 以与页眉顶部对齐。

## Review（阅读页右侧目录面板高度对齐）
- 右侧面板顶部偏移从 `top-11` 调整为 `top-0`，消除页眉上方的空隙（`src/components/library/NovelReader.tsx`）。

## 计划（阅读区背景与两侧一致）
- [x] 核对阅读区背景来源与主题默认值（`src/components/library/NovelReader.tsx`）
- [x] 调整默认主题背景色，使阅读区与两侧背景一致（`src/components/library/NovelReader.tsx`）
- [x] 自查阅读设置切换主题是否仍可用

## 解决方案（阅读区背景与两侧一致）
- 增加一个默认主题，背景色对齐全局侧边栏/主区域（浅色 `#f9fafb`，深色 `#0f172a`），并作为默认选中项。

## Review（阅读区背景与两侧一致）
- 新增“默认”主题并置为默认选中，使阅读区背景与两侧一致（浅色 `#f9fafb`、深色 `#0f172a`）（`src/components/library/NovelReader.tsx`）。

## 计划（左侧导航栏背景一致）
- [x] 核对导航栏背景样式与右侧主区域背景定义（`src/components/layout/Sidebar.tsx`、`src/components/layout/AuthLayout.tsx`）
- [x] 调整左侧导航栏背景色与右侧一致（`src/components/layout/Sidebar.tsx`）
- [x] 自查浅色/深色模式下的对比与边框效果

## 解决方案（左侧导航栏背景一致）
- 将侧边栏背景从 `bg-gray-50 dark:bg-slate-900` 调整为与主区域一致的背景色。

## Review（左侧导航栏背景一致）
- 侧边栏深色背景改为 `dark:bg-gray-900`，与右侧主区域背景一致（`src/components/layout/Sidebar.tsx`）。

## 计划（左侧导航栏浅色背景提亮）
- [x] 核对侧边栏浅色背景定义与页面主背景观感（`src/components/layout/Sidebar.tsx`、`src/components/layout/AuthLayout.tsx`）
- [x] 调整侧边栏浅色背景为纯白，缩小与右侧内容的明度差（`src/components/layout/Sidebar.tsx`）
- [x] 自查浅色模式下边框与悬浮态可读性

## 解决方案（左侧导航栏浅色背景提亮）
- 将侧边栏浅色背景从 `bg-gray-50` 调整为 `bg-white`。

## Review（左侧导航栏浅色背景提亮）
- 侧边栏浅色背景调整为 `bg-white`，提升明度，与右侧内容更一致（`src/components/layout/Sidebar.tsx`）。
- 跨章节修订入队改为按 `revisionId` 去重，避免重复堆积（`src/store/editorStore.ts`）。
- 当前章节修订也入队，并在展示时记录为“已应用”，便于切章后重建修订标记（`src/components/editor/NovelEditor.tsx`）。
- 采纳/弃用事件会清理当前章节待处理修订，批量采纳/弃用清空全部，避免切换后重复展示（`src/components/editor/NovelEditor.tsx`）。
- 未做实际运行验证，建议切换章节并点击采纳/弃用确认标记持久性。

## 计划（作品管理底部空白条）
- [x] 核对作品管理页容器高度与滚动设置（`src/views/WorksView/index.tsx`、`src/components/layout/AuthLayout.tsx`）
- [x] 去掉固定高度并让页面填满父容器，消除底部空白（`src/views/WorksView/index.tsx`）
- [x] 自查作品列表滚动与底部可见性

## 解决方案（作品管理底部空白条）
- 移除 `height: calc(100vh - 44px)`，改用 `h-full`/`min-h-full` 由外层布局控制高度，避免底部空白露出主背景。

## Review（作品管理底部空白条）
- 作品管理页根容器移除固定高度，改为 `h-full min-h-full`，消除底部空白条（`src/views/WorksView/index.tsx`）。

## Review（修订入库持久化）
- 新增 `ChapterRevision` 模型与迁移，支持 pending/accepted/discarded/conflict 并记录定位信息（`backend/app/models/chapter_revision.py`、`backend/alembic/versions/20260113_1800_add_chapter_revisions.py`）。
- `apply_chapter_edit` 改为创建修订记录并返回 `request_id`/`revision_id`，不再直接写正文；HITL 使用工具返回的 `request_id`（`backend/app/services/agent/tools/editor_tools.py`、`backend/app/services/agent/stream/stream_event_handler.py`）。
- `approval-response` 通过修订表应用/弃用并处理冲突，Redis 过期时仍可兜底（`backend/app/api/v1/agent.py`、`backend/app/services/chapter_revision_service.py`）。
- 新增章节修订查询接口与前端加载重建标记，编辑器采纳/弃用时同步后端（`backend/app/api/v1/chapters.py`、`src/services/DataService.ts`、`src/components/editor/NovelEditor.tsx`、`src/hooks/useAgentChat.ts`、`src/types/revision.ts`）。
- 未运行测试；建议验证跨章节修订在切换/刷新后仍显示，且采纳/弃用能正确落库与移除。

## 计划（修订入库持久化）
- [x] 新增章节修订表模型与迁移，记录 pending 修订与定位信息（`backend/app/models`、`backend/alembic/versions`）
- [x] `apply_chapter_edit` 改为写入修订记录并返回 `revision_id`/`request_id`，不直接更新正文（`backend/app/services/agent/tools/editor_tools.py`、`backend/app/services/agent/stream/stream_event_handler.py`）
- [x] `approval-response` 按 `request_id` 读取修订记录并应用/更新状态，Redis 过期时也能兜底（`backend/app/api/v1/agent.py`、`backend/app/services`）
- [x] 新增获取章节 pending 修订接口并前端加载重建标记，采纳/弃用同步后端（`backend/app/api/v1/chapters.py`、`src/services/DataService.ts`、`src/components/editor/NovelEditor.tsx`、`src/store/editorStore.ts`、`src/hooks/useAgentChat.ts`）
- [x] 更新 Review 记录改动与验证建议

## 解决方案（修订入库持久化）
- 新增 `chapter_revisions` 表保存待确认修订（状态、操作类型、原文/新文、定位信息、base_version、request_id）。
- `apply_chapter_edit` 只落库创建 pending 修订并返回 `revision_id`/`request_id`；前端仍按现有修订事件展示红删绿增。
- `submit_approval_response` 优先根据 `request_id` 读取修订记录：采纳时应用或跳过重复应用，弃用仅标记状态；Redis 过期时仍可处理。
- 前端切换章节时拉取 pending 修订并重建标记；修订条目标记为持久化，避免过期清理。

## 计划（通知快捷面板易消失）
- [x] 核对侧边栏通知悬浮面板的 hover 逻辑与渲染方式（`src/components/layout/Sidebar.tsx`）
- [x] 为通知面板关闭加入短暂延迟，避免从图标移到面板时立即隐藏（`src/components/layout/Sidebar.tsx`）
- [x] 自查收起/展开侧边栏时的悬浮行为

## 解决方案（通知快捷面板易消失）
- 使用定时器延迟关闭 hover 状态，面板和触发器进入时清除定时器，确保鼠标移动到面板时不消失。

## 计划（章节定位错章排查）
- [x] 阅读后台/前端日志与执行轨迹，确认工具链顺序与 chapter_id 来源（`Backend.md`、`log/localhost-1768283679274.log`、`INFO.md`）
- [x] 核对 locate_content 在未明确章节时的参数补全逻辑与默认 chapter_id 走向（`backend/app/services/agent/execution/tool_executor.py`、`backend/app/services/agent/execution/task_runner.py`）
- [x] 针对“用户不记得章节”的场景，添加跳过当前章节的最小改动，确保触发 search_content → get_writing_context → locate_content
- [x] 更新 Review 记录原因、改动点与验证建议

## Review（通知快捷面板易消失）
- 通知面板关闭改为延迟 200ms，触发区/面板 hover 时清除定时器，避免移入时消失（`src/components/layout/Sidebar.tsx`）。

## 计划（复杂测试提示词-四次）
- [x] 阅读小说素材第2-5章关键段落（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计一条多章节、多操作的复杂测试提示词（替换+插入+锚点/容错要求）
- [x] 更新 Review 记录提示词与验证要点

## 解决方案（复杂测试提示词-四次）
```text
你现在停留在第5章《太一门》编辑器，但我要你跨章节修改第2章、第3章、第4章。请严格按以下规则执行：
【硬性要求】
1) 每一处修改必须先 locate_content 精确定位，必须命中我给的锚点；若定位到章节开头或锚点不匹配，停止该条并报告“未命中，不应用”。
2) 所有修改只在第2/3/4章进行，不得改动第5章正文和任何章节标题。
3) 叙事视角保持第三人称，语气/节奏/用词风格保持原文一致，不新增人物，不改时间线。
4) replace/insert 的内容必须是单段短改，避免大段改写。

【任务A｜第2章《浑圆桩》替换】
把这一句完整替换为新句：
原句（锚点句）：赵穆看着段融茫然若失的样子，喃喃道：“不会是前几天发烧，给烧傻了吧？”
新句：赵穆看着段融茫然若失的样子，喉头动了动，终究把火气压回去，低声嘀咕：“不会是前几天发烧，给烧坏了吧？”
定位锚点：前一句包含“段融站到了队伍的最后”，后一句以“段融站到了队伍的最后”开头。

【任务B｜第2章《浑圆桩》插入】
在下面这句之后插入一句（只加1句）：
锚点句：他每日指导这些杂役弟子练功的时间，也不过只有半柱香而已。
插入句：余下时辰，全靠他们自己咬牙撑着。
定位锚点：前一句为“他每日指导这些杂役弟子练功的时间，也不过只有半柱香而已。”，后一句以“而赵穆自始至终”开头。

【任务C｜第3章《一夕千悟》插入】
在下面这句之后插入一句（只加1句）：
锚点句：段融陡然停下，随即发现右臂的肌肉，微微发疼！
插入句：酸麻沿着肩臂往下坠，像有人攥住了筋。
定位锚点：前一句为“段融陡然停下，随即发现右臂的肌肉，微微发疼！”，后一句以“幸亏手中的树枝”开头。

【任务D｜第4章《家底》插入】
在下面这句之后插入一句（只加1句）：
锚点句：段融看了看，估计加起来，也就一两多点。
插入句：那点碎银在掌心硌得发凉，他却没再犹豫。
定位锚点：前一句为“段融看了看，估计加起来，也就一两多点。”，后一句为“这就是原身的全部家底了。”

【验收与回报】
1) 给出每条修改的章节、锚点命中结果与 apply_chapter_edit 是否成功。
2) 提醒我：切到第2/3/4章查看红删绿增修订；再切换其他章节后返回，确认修订仍在（未点“采纳/弃用”前不应消失）。
```

## Review（复杂测试提示词-四次）
- 已基于第2-5章内容设计跨章节替换+插入的复杂测试提示词，并要求锚点严格命中与失败即停止。
- 加入切回章节查看修订、切换后再次确认的验证步骤，用于复现修订持久性问题。

## 计划（修订标记再次消失排查）
- [ ] 阅读 `Backend.md`、前端日志 `log/localhost-1768287687561.log` 与 `INFO.md`，确认修订事件链
- [ ] 对照前端日志检查“crossChapterRevisionApplied”后是否触发内容刷新覆盖
- [ ] 核对 `NovelEditor` 内容更新逻辑与修订缓存交互，提出最小修复方案
- [ ] 更新 Review 记录结论与验证要点

## 解决方案（修订标记再次消失排查）
- 后端 `apply_chapter_edit` 全部成功，修订已写入正文（`Backend.md`）。
- 前端日志显示“跨章节修订已显示”后紧跟 `WorkDetailView 保存章节` 与 `NovelEditor 更新编辑器内容`，会用无标记正文覆盖编辑器，导致红删绿增被清掉。
- 当前“已应用”修订只在前端内存，内容刷新后没有触发重建，因此等待几分钟或切章后看不到标记。

## 计划（修订入库持久化）
- [ ] 盘点修订/审批链路与入点（`backend/app/services/agent/tools/editor_tools.py`、`backend/app/api/v1/agent.py`、`backend/app/services/agent/stream/stream_event_handler.py`、`src/hooks/useAgentChat.ts`、`src/components/editor/NovelEditor.tsx`）
- [ ] 新增修订表模型与迁移，并注册到 models（`backend/app/models`、`backend/alembic/versions`）
- [ ] 后端实现修订创建/查询/采纳/弃用，并在工具与审批响应中接入（`backend/app/api`、`backend/app/services`）
- [ ] 前端接入修订加载与展示，采纳/弃用同步后端（`src/services/DataService.ts`、`src/store/editorStore.ts`、`src/components/editor/NovelEditor.tsx`）
- [ ] 更新 Review 记录改动与验证步骤

## 解决方案（修订入库持久化）
- 新增 `chapter_revisions` 表保存待确认修订（状态、锚点、原/新内容、base_version、request_id）。
- `apply_chapter_edit` 不直接写正文，改为创建 pending 修订并返回 revision_id。
- `/chat/approval-response` 采纳时应用 revision 到正文并标记 accepted，弃用标记 discarded；若 Redis 过期则以 revision_id 兜底。
- 前端加载章节时拉取 pending revisions，重建红删绿增；采纳/弃用时调用后端更新状态。

## 计划（通知中心移到社区）
- [x] 核对导航配置与通知面板特殊渲染逻辑（`src/components/layout/Sidebar.tsx`）
- [x] 将通知中心移动到社区列表并放在“我的书架”下，保留未读提示与悬浮面板（`src/components/layout/Sidebar.tsx`）
- [x] 自查折叠/展开状态下的悬浮行为与点击跳转

## 解决方案（通知中心移到社区）
- 将通知中心从底部导航移到社区导航列表，抽离通知渲染逻辑复用到新位置。

## Review（通知中心移到社区）
- 通知中心项从底部导航移到社区列表（在“我的书架”之后），并复用原有未读提示与悬浮面板逻辑（`src/components/layout/Sidebar.tsx`）。

## 计划（后端启动报错 NameError）
- [x] 定位 `ChapterRevisionService` 使用 `datetime` 的位置与缺失导入（`backend/app/services/chapter_revision_service.py`）
- [x] 补充缺失的 `datetime` 导入，恢复服务启动（`backend/app/services/chapter_revision_service.py`）
- [x] 自查是否有类似未导入符号

## 解决方案（后端启动报错 NameError）
- 在 `backend/app/services/chapter_revision_service.py` 补充 `from datetime import datetime`。

## Review（后端启动报错 NameError）
- 补充 `datetime` 导入，修复 `ChapterRevisionService` 的 NameError（`backend/app/services/chapter_revision_service.py`）。

## Review（章节定位错章排查）
- 日志显示只执行 locate_content → smart_rewrite → apply_chapter_edit，且 locate_content 使用当前 chapter_id（第5章），未触发 search_content/get_writing_context（`Backend.md`、`INFO.md`）。
- 在 `backend/app/services/agent/execution/tool_executor.py` 增加“用户不记得章节”识别，locate_content/search_content 在该场景不默认使用当前 chapter_id，允许自动 search_content 补全目标章节。
- 验证建议：用“我记不清第几章/哪一章”复测，检查日志出现 search_content，且 locate_content 的 chapter_id 来自搜索结果。

## 计划（Explore 工具与原文读取）
- [ ] 复核现有检索/定位/读取工具链与标准工具注册方式（`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/tools/__init__.py`）
- [ ] 新增 read_chapter_raw 工具，返回原始章节全文（避免清洗/截断）（`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/tools/__init__.py`、`backend/app/services/agent/execution/tool_executor.py`）
- [ ] 新增 explore_content 工具，按 search → locate → read_raw 循环补漏并输出证据（`backend/app/services/agent/langgraph_tools.py`、`backend/app/services/agent/tools/__init__.py`、`backend/app/services/agent/execution/tool_executor.py`）
- [ ] 更新工具说明与使用建议（`backend/app/services/agent/prompts/tool_descriptions.py`）
- [ ] 更新 Review 记录改动与验证建议

## 计划（Explore 工具预览样式）
- [x] 复核预览页结构与现有样式基线（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 追加 Explore 轨迹区块与分轮展示结构，贴合当前 UI 风格并保持紧凑（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 补充示例数据与折叠交互，保证阅读路径清晰（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（Explore 工具预览样式）
- 新增 Explore 轨迹卡片，分轮展示 Search/Locate/ReadRaw/Review 串联与关键参数（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。
- 增加摘要 pills、证据片段折叠列表与状态提示，维持现有浅色胶囊/卡片风格并对齐执行流结构（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（Explore 轨迹拆分折叠）
- [x] 复核 Explore 轨迹现有结构与样式层级（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 将每轮 Explore 拆成可折叠胶囊，保留摘要 pills 与证据折叠（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 调整交互脚本以支持轮次折叠/展开（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（Explore 轨迹拆分折叠）
- Explore 轮次改为独立胶囊卡片，可折叠展开并保留证据片段折叠（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。
- 增加轮次折叠脚本与样式，视觉上更接近 AI 整合分析的胶囊结构（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（Explore 摘要胶囊化）
- [x] 复核 Explore 轨迹摘要区域的外层容器与胶囊样式（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 去掉摘要外层框体，仅保留独立胶囊并对齐 AI 整合分析风格（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（Explore 摘要胶囊化）
- 移除摘要外层框体，仅保留独立胶囊行，整体更接近 AI 整合分析的胶囊风格（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（移除 Explore 摘要胶囊）
- [x] 复核 Explore 轨迹摘要渲染位置与样式引用（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 移除“轮次/证据/覆盖度/补漏”的胶囊区块及对应样式（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（移除 Explore 摘要胶囊）
- 删除 Explore 摘要胶囊与样式，仅保留分轮折叠结构与证据片段（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（Explore 折叠胶囊收缩）
- [x] 复核 Explore 轮次胶囊收起状态的结构与样式（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 收起时改为紧凑胶囊宽度，仅显示统一图标与简短标题（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新折叠交互脚本，确保展开/收起样式切换（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（Explore 折叠胶囊收缩）
- 收起状态改为紧凑胶囊宽度并统一 scan 图标，折叠时隐藏箭头并缩小标记尺寸（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（移除 Explore 分割线）
- [x] 复核 Explore 轮次分隔样式来源（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 移除轮次之间的分割线样式（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（移除 Explore 分割线）
- 去掉 Explore 轮次之间的虚线分隔，视觉更简洁（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（Explore 展开宽度自适应）
- [x] 复核 Explore 轮次展开态宽度来源与布局影响（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 调整展开态宽度为贴合标签行右边界（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（Explore 展开宽度自适应）
- 展开态改为内容自适应宽度，容器右边界贴合标签行末端，并限制最大宽度避免溢出（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（Explore 卡片风格对齐）
- [x] 复核页面现有胶囊样式的颜色/边框/圆角/图标风格（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 调整 Explore 卡片与标签的背景/描边/圆角/图标尺寸，使其与现有胶囊一致（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（Explore 卡片风格对齐）
- Explore 卡片/标签统一为胶囊基准色与圆角，图标改为纯色无底，整体与其他胶囊一致（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（证据片段胶囊高度压缩）
- [x] 复核证据片段胶囊的内边距/字体/行高设置（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 缩小胶囊高度并保持可读性（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）
- [x] 更新 Review 记录改动与展示建议

## Review（证据片段胶囊高度压缩）
- 缩减证据片段胶囊的内边距与字体尺寸，使高度更紧凑（`/mnt/d/Java/claude-code-skill/agent-writing-preview.html`）。

## 计划（Explore 展示聚合落地）
- [ ] 复核流式事件结构与前端执行流渲染路径（`backend/app/services/agent/stream`、`src/hooks/useAgentChat.ts`、`src/components/agent/ExecutionFlow`）
- [ ] 明确 Explore 为“展示聚合”，设计轮次聚合规则与数据结构（Search → Locate → Read → Review/证据片段）
- [ ] 前端实现聚合与 UI 展示，匹配预览卡片内容（`src/components/agent/ExecutionFlow`、`src/components/agent/ExecutionFlow/StepCard.tsx`）
- [ ] 若字段不足，在后端补充最小 tool_result/trace 事件载荷（`backend/app/services/agent/stream/flow_events.py`、`backend/app/services/agent/langgraph_agent.py`）
- [ ] 更新 Review 记录改动与验证建议

## 计划（复杂测试提示词-五次）
- [x] 阅读小说素材第2-4章关键段落（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计 1 条高复杂度跨章节测试 prompt（含定位锚点/替换+插入/失败即停/切回验证）
- [x] 输出 prompt 并更新 Review 记录

## Review（复杂测试提示词-五次）
- 已基于第2-4章提供跨章节替换+插入的复杂测试提示词，包含 locate_content 必须命中、未命中即停与切回验证步骤（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）。

## 计划（修订服务启动报错）
- [x] 核对错误堆栈与缺失引用位置（`backend/app/services/chapter_revision_service.py`）
- [x] 补充缺失的 `datetime` 引用并保持最小改动（`backend/app/services/chapter_revision_service.py`）
- [x] 更新 Review 记录修复点与验证建议

## Review（修订服务启动报错）
- 补充 `from datetime import datetime`，修复 `ChapterRevisionService.mark_status` 的 NameError（`backend/app/services/chapter_revision_service.py`）。

## 计划（日志核验：跨章节修订持久化）
- [x] 阅读后台日志 `Backend.md` 与前端日志 `log/localhost-1768294156979.log`
- [x] 阅读前端执行轨迹 `INFO.md`，对照事件链与接口返回
- [x] 汇总结论并更新 Review（是否符合预期、可能异常点）

## 解决方案（日志核验：跨章节修订持久化）
- 以日志为准核对“修订落库 → 前端拉取 pending → 修订标记重建 → 采纳/弃用后落库状态更新”的完整链路；若链路缺失，优先定位 request_id/revision_id 是否贯通、/chapters/{id}/revisions 是否请求成功、以及切章时是否触发重建。

## Review（日志核验：跨章节修订持久化）
- 后端日志显示 locate_content 被传入 before_anchor/after_anchor 但工具不接受该参数，导致 unknown_tool，并使后续 apply_chapter_edit 的 chapter_id 变成错误对象（`Backend.md`）。
- INFO 轨迹明确“所有修改未执行”，原因是 locate_content 无法调用，章节引用失效（`INFO.md`）。
- 前端日志未出现修订事件或跨章节重建记录（`log/localhost-1768294156979.log`）。

## 计划（locate_content 参数兼容修复）
- [x] 复核 locate_content 签名与调用参数（`backend/app/services/agent/tools/locate_tools.py`）
- [x] 扩展 locate_content 输入参数以兼容 before_anchor/after_anchor，避免 TypeError（`backend/app/services/agent/tools/locate_tools.py`）
- [x] 更新 Review 记录修复点与验证建议

## 解决方案（locate_content 参数兼容修复）
- 为 locate_content 增加 before_anchor/after_anchor 可选参数（必要时作为空 query 的兜底），避免多余参数导致调用失败与 unknown_tool。

## Review（locate_content 参数兼容修复）
- locate_content 接收 before_anchor/after_anchor 兼容参数，并在 query 为空时使用锚点兜底，避免 unexpected keyword argument 导致 unknown_tool（`backend/app/services/agent/tools/locate_tools.py`）。

## 计划（修订重复写入排查与修复）
- [x] 核对章节切换时修订重建路径与去重逻辑（`src/components/editor/NovelEditor.tsx`）
- [x] 评估修订标记是否被保存到章节内容导致二次插入（`src/components/editor/NovelEditor.tsx`、`src/services/EditorSyncService.ts`）
- [x] 增加重复写入拦截（基于位置/内容检测或 revisionId 标记），并更新 Review（`src/components/editor/NovelEditor.tsx`、`src/components/editor/AIRevisionMark.ts`）

## 解决方案（修订重复写入排查与修复）
- 在应用修订前检测插入位置是否已存在同样的 replacement（或已带 AI 标记），已存在则跳过写入，并保持修订条不重复入队。

## Review（修订重复写入排查与修复）
- 章节切换后会重新触发修订重建，且 pending 修订在正文中已被 aiInserted 标记写入（自动保存/缓存），导致重复插入（`src/components/editor/NovelEditor.tsx`、`src/services/EditorSyncService.ts`）。
- 在应用修订前新增检测：若目标位置已存在同样的 replacement 且带 aiInserted 标记，则跳过重复应用并仅恢复操作栏（`src/components/editor/NovelEditor.tsx`）。

## 计划（复杂测试提示词-六次）
- [x] 阅读小说素材第2-4章关键段落（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计 1 条高复杂度跨章节测试 prompt（含定位锚点/替换+插入/切章回看不重复写入验证）
- [x] 输出 prompt 并更新 Review 记录

## Review（复杂测试提示词-六次）
- 已基于第2-4章内容提供跨章节替换+插入的复杂测试提示词，包含切章回看与重复写入验证步骤（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）。

## 计划（重复修订二次修复）
- [x] 阅读后台日志 `Backend.md`、前端日志 `log/localhost-1768297435810.log` 与轨迹 `INFO.md`，确认重复触发链路
- [x] 核对修订重建与定位逻辑，识别重复插入的触发点（`src/components/editor/NovelEditor.tsx`、`src/utils/revisionLocator.ts`）
- [x] 增加基于 revisionId 的修订去重与标记清理，并更新 Review（`src/components/editor/NovelEditor.tsx`、`src/components/editor/AIRevisionMark.ts`）

## 解决方案（重复修订二次修复）
- 在修订文本上附加 `aiRevisionId` 标记，并在应用前扫描文档是否已存在该 revisionId；若存在则仅恢复操作栏，不再重复插入，同时在采纳/弃用时清理 `data-revision-id` 包裹。

## Review（重复修订二次修复）
- 前端日志未出现有效修订事件链输出，但章节切换会触发修订重建；重复插入仍发生，说明仅靠 aiInserted 文本对比不足（`log/localhost-1768297435810.log`、`src/components/editor/NovelEditor.tsx`）。
- 已为修订内容加 `aiRevisionId` 标记，并在应用前检测文档内是否已存在该 revisionId；若存在则跳过重复插入并恢复操作栏（`src/components/editor/NovelEditor.tsx`）。
- 采纳/弃用时同步清理 `data-revision-id` 包裹，避免残留标记影响后续判断（`src/components/editor/NovelEditor.tsx`）。

## 计划（采纳冲突与 500 错误修复）
- [x] 核对 approval-response 409 冲突的触发条件与版本变化来源（`backend/app/api/v1/agent.py`、`backend/app/services/chapter_revision_service.py`）
- [x] 修复 HTTPException 被吞导致 500 的问题（`backend/app/api/v1/agent.py`）
- [x] 前端在应用修订标记时禁止自动保存，避免 base_version 变化（`src/components/editor/NovelEditor.tsx`）
- [x] 更新 Review 记录修复点与验证建议

## 解决方案（采纳冲突与 500 错误修复）
- 审批接口保留 HTTPException 直接返回，避免 409 被包装为 500；前端在修订标记展示阶段关闭自动保存，避免章节版本提前变化导致冲突。

## Review（采纳冲突与 500 错误修复）
- 采纳接口对 `HTTPException` 直接透传，避免 409 冲突被统一捕获成 500（`backend/app/api/v1/agent.py`）。
- 修订标记展示阶段使用 `suppressAutoSaveRef` 跳过 onUpdate 自动保存，避免 `chapter.version` 在采纳前变化导致冲突（`src/components/editor/NovelEditor.tsx`）。

## 计划（切章重复写入与采纳冲突三次修复）
- [x] 复核章节切换卸载保存/防抖保存是否写入修订标记内容（`src/components/editor/NovelEditor.tsx`、`src/views/WorkDetailView/index.tsx`）
- [x] 调整修订展示期间保存策略：取消未完成的防抖保存、跳过卸载保存与自动保存（`src/components/editor/NovelEditor.tsx`）
- [x] 容错 apply_revision：base_version 不一致时尝试应用，失败才标记冲突（`backend/app/services/chapter_revision_service.py`）
- [x] 更新 Review 记录变更与验证要点

## 解决方案（切章重复写入与采纳冲突三次修复）
- 修订展示期间不写回正文：取消既有防抖保存并在卸载时跳过保存，避免切章后把红删绿增内容持久化导致重复插入。
- 采纳端容错版本差：base_version 不一致仍尝试基于当前正文定位应用，只有定位失败或乐观锁冲突才标记为 conflict。

## Review（切章重复写入与采纳冲突三次修复）
- 修订展示时阻断保存：新增 `revisionSaveBlockedRef`，在显示修订时取消防抖保存并跳过 onUpdate 自动保存与卸载保存，避免红删绿增写回正文（`src/components/editor/NovelEditor.tsx`）。
- 采纳/弃用后解除阻断，允许正常保存（`src/components/editor/NovelEditor.tsx`）。
- 后端改为 base_version 不一致时仍尝试应用修订，仅在定位失败或乐观锁冲突时标记为冲突（`backend/app/services/chapter_revision_service.py`）。
