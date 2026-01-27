# TODO

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
