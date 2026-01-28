# TODO

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

#### 计划（重构工具循环的章节覆盖策略）

- [ ] 增加“覆盖度优先”硬规则：同一章节连续读取上限 + 未覆盖章节优先
- [ ] 在 tool_loop 决策提示中加入“跨章覆盖”要求（必须先覆盖范围内多个章节）
- [ ] 读取策略改为“跨章批量读”：优先 list_chapters/list_paragraphs 再分散 read_paragraphs
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

### review

- 已删除 todo.md 其余记录，仅保留“### 讨论记录（详细）”及其内容。
- 本节保留了对标 opencode 的确定性检索链路、重构执行风格、node_id 方案可行性与受影响代码范围、Explore→Locate 传参规则。
- 已完成 Explore 重构：删除规则验收与旧补漏路径，改为“精确搜索 + LLM 自检循环”驱动后续收集。
- 已补齐定位桥梁：新增 `locate_targets` 与 `evidences` 输出，并在 `frontend_display` 中透出 locate_targets。
- 已打通 node_id：`ParagraphRead` 记录 node_id，构建 node_id 映射并用于 evidences/search_results/locate_targets。
- 已移除/隐藏 sufficiency/coverage 输出字段，前端展示改为“继续检索/停止检索”语义。
- 已修复 `ParagraphRead` 字段顺序错误，避免 dataclass 导入时报错。
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

#### 章节数不一致排查结论

- 2026-01-27 19:03:57 后端日志显示文本导入完成仅 **77 章**（work_id=5fe6c67d-8a1b-48c1-ad56-a5281eb22e21）。
- 2026-01-27 19:04:01 章节列表查询返回 **77 章**，且最后一章标题为“第100章【火域铸真器，两脉起冲突】”，但 **order=77**，说明“第100章”仅是标题文本而非真实章节序号。
- 2026-01-27 19:07:02–19:07:05 向量化日志显示“第98/99/100章”对应 **order=75/76/77**，进一步印证实际章节数为 77（标题编号与真实顺序不一致）。
- 前端列表来自 `/api/v1/chapters/work/{work_id}`，未做过滤；数量显示与后端真实章节数一致，问题不在前端。
- 最可能根因：`_split_chapters` 的正则仅匹配“第X章+空白/冒号”，对“第X章【标题】/第X章-标题/第X章·标题/无分隔符”等格式命中失败，导致 23 处章节标题未被识别而被合并。
- 解决建议：扩展分章正则（允许 `【】()（）[]`、破折号、点号、空白可选），重新导入或做补偿拆分迁移；若使用 Markdown，建议放宽 `##` 为 `#{1,6}`。
