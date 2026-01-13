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
- [ ] 核对跨章节修订在切换章节时的触发条件与过期逻辑（`src/components/editor/NovelEditor.tsx`）
- [ ] 核对内容刷新/缓存是否阻止修订重建（`src/components/editor/NovelEditor.tsx`、`src/services/EditorSyncService.ts`）
- [ ] 汇总结论与可行修复建议，并更新 Review

## 计划（跨章节修订测试提示词-二次）
- [x] 复核小说素材章节与关键句（`docs/Agent/real-book/一夕千悟，从杂役弟子开始.txt`）
- [x] 设计一条高复杂度跨章节修改测试 prompt（包含定位锚点、替换+插入、明确“切回目标章节查看修订”的验证步骤）
- [x] 更新 Review

## 计划（跨章节修订测试日志核验）
- [ ] 阅读 `Backend.md` 最新日志，确认跨章节 replace/insert 的定位与 apply_chapter_edit 结果
- [ ] 阅读前端日志 `log/localhost-1768280433702.log` 与前端执行轨迹 `INFO.md`
- [ ] 对照前后端事件链（approval_request/revision/agent-show-revision），核对 chapter_id 与锚点字段
- [ ] 汇总结论与可能原因，并更新 Review

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
