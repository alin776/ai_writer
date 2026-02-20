# TODO

---

## 第二轮修复（2026-02-12 深度诊断）

### 三个根因

1. **Insert 插入错位**：`explore_v6.py` 的 `_match_paragraph()` 返回 chunk 中**第一个**子串匹配段落 → 长 chunk 覆盖多个段落时，第一个匹配不一定是用户指定的段落。改为返回**最长匹配**（最具体的段落）。
2. **Continue 不触发新建章节**：`_maybe_upgrade_append_to_create` 只识别"续写**第X章**"，但用户说的是"续写**下去**"（无章节号）→ 正则不匹配 → 一致性检查阻止 append。fix: ① `_extract_continue_target_chapter_order` 新增回退：从 explore 查询中提取章节号（AI 查询生成器已识别出"第六章"）；② append 操作一致性检查降级为 WARNING + 覆盖（双保险）。
3. **Rewrite 0秒失败**：`_ensure_source_locator` 返回 ambiguous_locator → 存入 `__locator_error` → line 244 拦截**所有工具**（包括 smart_rewrite）→ smart_rewrite 根本没执行。fix: `__locator_error` 只拦截 operate_apply，不拦截创作工具。

### 待办清单

- [x] `explore_v6.py`：`_match_paragraph` 改为最长匹配（best match）
- [x] `tool_executor.py`：`_extract_continue_target_chapter_order` 新增 explore 查询回退（从 `stats.query` 提取"第X章"）
- [x] `tool_executor.py`：`operation=="append"` 一致性检查降级为 WARNING + 自动覆盖 chapter_id（双保险）
- [x] `tool_executor.py`：`__locator_error` 检查仅对 operate_apply/apply_chapter_edit 生效
- [x] `explore_v6_spec.py`：更新 `test_locate_in_chapters` 期望值（匹配策略改变）
- [x] 运行测试：63 passed, 1 failed（已有问题 test_strict_locator.py，与本次无关）
- [x] 在本文件追加 review 小结

---

## Explore V6 执行流程优化

### 问题 1：查询高度重叠，67% 浪费

**现状**：AI 分解出 3 条查询，各返回 ~11 条 chunk，合计 33 条，去重后只剩 11 条。2/3 的 LightRAG 调用是浪费的。

**方案**：只用 1 条查询，去掉分解、并行、去重逻辑，大幅减少 token 消耗和 LightRAG 调用次数。

- [x] `explore_v6.py`：`decompose_queries` 改为 `generate_query` 生成 1 条短查询，删除 `execute_parallel` 并行/去重逻辑，改为 `execute_query` 单次调用

### 问题 2+3：KG 数据丢弃 + mix 模式白等 60s

**现状**：`mode="mix"` 触发 LightRAG 内部 LLM 做 KG 推理（60s），但 `_parse_context_chunks` 只提取 Document Chunks，KG 实体数据全部丢弃。等于花 60s 换来一堆不用的东西。

**方案**：`mode` 从 `mix` 改为 `hybrid`（向量 + 关键词，无内部 LLM），响应从 60s 降到 <5s。

- [x] `config.py`：`LIGHTRAG_MODE` 默认值从 `"mix"` 改为 `"hybrid"`
- [x] `fact_retrieval_gateway.py`：所有 fallback 默认值也改为 `"hybrid"`

### 问题 4：子串定位脆弱 + LightRAG 未接入导入流程

**现状**：LightRAG 数据是外部手动导入的，没有 chapter_id 元数据。查询返回的 chunk 只有纯文本，`locate_chunks` 被迫用前 80 字符做 `str.find()` 遍历所有章节定位，实测 1/11 失败率。

**方案**：插入时 `file_source="chapter_{chapter_id}"`，查询时 `include_references=True`，从 `references[].file_path` 提取 `chapter_id`。

- [x] `config.py`：新增 `LIGHTRAG_INSERT_PATH` 配置
- [x] `fact_retrieval_gateway.py`：新增 `insert_document()` + `_build_ref_chapter_map()` + 查询添加 `include_references=True`
- [x] `_parse_context_chunks`：同时提取 `reference_id` 和 `content`
- [x] `import_service.py`：后处理链新增 `_insert_chapters_to_lightrag()` 步骤
- [x] `explore_v6.py`：删除 `locate_chunks` / `_load_chapter_cache`，新增 `enrich_chunks()` 用 chapter_id 补全元数据

### 问题 5：每次新建 Gateway 实例

**方案**：改为模块级单例。

- [x] `fact_retrieval_gateway.py`：新增 `get_gateway()` 单例函数
- [x] `explore_v6.py`：调用 `get_gateway()` 替代 `FactRetrievalGateway()`

---

## 问题 6：段落级定位缺失（写入链路断裂）

### 问题

Explore V6 的 `locate_targets` 只包含 `chapter_id` + `chapter_order`，缺少 `paragraph_index`、`node_id`、`text`、`before_anchor`、`after_anchor`。下游 `_validate_source_locator()` 检查 `node_id` 或 `paragraph_index` 不存在时直接阻止写回，导致 `smart_rewrite` / `smart_insert` → `operate_apply` 整条写入链路断裂。

### 根因

LightRAG 按 token 数（~1200）切块，每个 chunk 跨越 30-50 个段落，不返回段落偏移/位置信息。LightRAG 没有现成的段落级定位功能（社区 Issue #468 请求中）。

### 额外发现

`_insert_chapters_to_lightrag()` 直接把 HTML 内容发给 LightRAG，LightRAG 内部处理 HTML 标签的行为不可控，导致返回的 chunk 格式可能不干净。

### 方案

1. **插入时 HTML → 纯文本**：`_insert_chapters_to_lightrag()` 插入前用 `_html_to_plain_text()` 把 HTML 转为每行一个段落的纯文本
2. **查询后段落匹配**：新增 `locate_in_chapters()` 方法，用 `_split_paragraphs()` 解析章节 HTML，chunk 文本与段落做子串匹配
3. **补全 locate_targets**：`_build_result()` 中 `locate_targets` 改为 `(chapter_id, paragraph_index)` 去重，包含 `paragraph_index`、`node_id`、`text`、`before_anchor`、`after_anchor`
4. **恢复 evidence_store 检查**：`has("locate_targets")` 恢复要求 `chapter_id AND (paragraph_index OR node_id)`

### 完成项

- [x] `import_service.py`：新增 `_html_to_plain_text()` 静态方法；`_insert_chapters_to_lightrag()` 插入前转纯文本
- [x] `explore_v6.py`：新增 `locate_in_chapters()` + `_match_paragraph()` + `_load_chapter_content()`；`run()` 新增步骤 3b；`_build_result()` 补全段落级字段；evidences 传递段落字段
- [x] `evidence_store.py`：`has("locate_targets")` 恢复 `chapter_id AND (paragraph_index OR node_id)` 检查
- [x] `explore_v6_spec.py`：新增 `_match_paragraph` 测试（3 个）、`locate_in_chapters` 测试、`_build_result` 段落字段测试（2 个）、源码方法存在性断言更新

---

## Review

### 修改的文件（4 个）

| 文件 | 改动 |
|------|------|
| `import_service.py` | 新增 `_html_to_plain_text()` 静态方法（HTML → 纯文本，每个 `<p>` 一行）；`_insert_chapters_to_lightrag()` 插入前调用转纯文本，确保 LightRAG 存储干净文本 |
| `explore_v6.py` | 新增 `locate_in_chapters()` 段落级定位方法（按 chapter_id 分组 → 加载章节 HTML → `_split_paragraphs()` 解析 → 子串匹配找 paragraph_index）；新增 `_match_paragraph()` 归一化匹配（去空白 + 跳过<6字符短段落）；新增 `_load_chapter_content()`；`run()` 新增步骤 3b；`_build_result()` locate_targets 改为 `(chapter_id, paragraph_index)` 去重，包含 `paragraph_index`/`node_id`/`text`/`before_anchor`/`after_anchor`；evidences 新增段落级字段；docstring 更新 |
| `evidence_store.py` | `has("locate_targets")` 恢复原始检查：`chapter_id AND (paragraph_index is not None OR node_id)`，确保下游写入链路只在有段落级定位时放行 |
| `explore_v6_spec.py` | 新增 6 个测试：`_match_paragraph` 首个完整匹配/无匹配/跳过短段落、`locate_in_chapters` 补全验证、`_build_result` 段落字段 + 去重；源码方法存在性断言新增 `locate_in_chapters`/`_match_paragraph`/`_load_chapter_content` |

### 数据流变化

**之前**：
```
LightRAG chunk(chapter_id only) → locate_targets(chapter_id only) → _validate_source_locator() → ❌ 阻止写回
```

**之后**：
```
LightRAG chunk(chapter_id + text)
  → locate_in_chapters(): 加载章节 HTML → _split_paragraphs() → 子串匹配
  → locate_targets(chapter_id + paragraph_index + node_id + text + anchors)
  → _validate_source_locator() → ✓ 通过
  → smart_rewrite / smart_insert → operate_apply → 写入成功
```

### 本轮修复（2026-02-12）

#### 1) `smart_insert/smart_rewrite` 定位歧义与错位风险

- 文件：`backend/app/services/agent/execution/tool_executor.py`
- 修改：
  - `source_locator` 在 `force` 模式下新增保护：
    - 若无显式选择（无 `locate_target_index/hint/id`）且已有有效 `source_locator`，优先沿用，不再强制重选。
    - 自动重选失败（如“定位候选不唯一”）时，回退到已有 `source_locator`，避免直接失败。
  - `node_id/paragraph_index` 的读取优先级改为：参数显式值 > 已有 `source_locator` > context。
- 目的：降低“定位候选不唯一/多个段落匹配”误报，减少插入与改写定位漂移。

#### 2) “续写第X章”自动新建章节（Create）

- 文件：`backend/app/services/agent/execution/tool_executor.py`
- 修改：
  - 新增 `append -> create` 运行时升级逻辑：
    - 当 `operate_apply(operation=append)` 且用户消息匹配“续写第X章”时，先解析目标章序号；
    - 若目标章存在，自动将 `chapter_id` 对齐到目标章；
    - 若目标章不存在，自动切换 `operation=create`，并设置标题 `第X章`。
- 目的：避免把“续写第6章”误追加到旧章节。

#### 3) `smart_rewrite -> operate_apply` 内容引用路径稳定性

- 文件：`backend/app/services/agent/planning/plan_generator.py`
- 修改：
  - 在 `_normalize_plan_schema()` 之后，再执行一次 `_ensure_replace_original_text()`。
- 目的：防止占位符后置转换导致的 `content` 路径漏修，确保 replace 写回使用 `data.versions[0].content`。

#### 4) 单元测试

- 新增：
  - `backend/tests/unit/tool_executor_continue_create_spec.py`
  - `backend/tests/unit/plan_generator_rewrite_apply_ref_spec.py`
- 结果：
  - 执行 `pytest -q tests/unit/tool_executor_continue_create_spec.py tests/unit/plan_generator_rewrite_apply_ref_spec.py tests/unit/tool_executor_retrieval_intent_spec.py tests/unit/plan_generator_retrieval_intent_spec.py`
  - `7 passed in 0.79s`

#### 5) 仍需你在线验证

- 建议用你给的 3 组 prompt 再走一轮前端联调，重点确认：
  - 插入段落是否稳定落在"第2章指定语句后"；
  - "续写第6章"是否产生 `operation=create` 的审批请求；
  - 改写是否不再出现"定位候选不唯一/多个段落匹配"提示。

---

### 第二轮 Review（2026-02-12 深度诊断后修复）

#### 修改的文件（3 个）

| 文件 | 改动 |
|------|------|
| `explore_v6.py` | `_match_paragraph()` 从"返回第一个子串匹配"改为"返回最长子串匹配"（遍历所有段落，记录最长匹配而非立即 return）。长 chunk 覆盖多段时，最长段落 = 最具体的匹配 = 最可能是用户指定的段落。 |
| `tool_executor.py` | ① `_extract_continue_target_chapter_order` 新增 explore 查询回退：用户消息无章节号时，从 `state.last_explore_result.stats.query` 提取"第X章"（AI 查询生成器已能识别目标章节）。② 一致性检查 `operation=="append"` 降级为 WARNING + 自动覆盖 chapter_id（双保险：即使 explore 查询也没有章节号，append 也不会被阻止）。③ `__locator_error` 只对 operate_apply/apply_chapter_edit 返回 error，创作工具改为 WARNING 跳过。 |
| `explore_v6_spec.py` | `test_locate_in_chapters` 期望值更新：paragraph_index 从 1→2（匹配策略从首个改为最长）。 |

#### 预期行为变化

| 场景 | 之前 | 之后 |
|------|------|------|
| Insert: 长 chunk 含多段 | 返回第一个匹配段落（可能是不相关的早期段落） | 返回最长匹配段落（最具体、最可能是目标段落） |
| Continue: "续写下去"无章节号 | explore 查询"第六章 当前内容" → 但 `_extract_continue_target_chapter_order` 只看用户消息 → 提取不到 → 一致性检查 ERROR → 阻止写回 | 从 explore 查询提取"第六章" → `resolve_chapter_id` 发现第6章不存在 → `operation` 升级为 `create` → 直接创建新章节 |
| Rewrite: 多 locate_targets 歧义 | `__locator_error` 拦截 smart_rewrite → 0秒失败 → 无内容 | smart_rewrite 正常执行（跳过拦截）→ 生成内容 → 定位由后续 operate_apply 负责 |

---

## 第三轮清理（2026-02-12 删除 OpenSearch 精确检索残留）

### 待办清单

- [x] 删除 `exact_search_paragraphs` 方法及其残留引用
- [x] 删除 `search_content` 工具定义与执行入口（含 StandardTool）
- [x] 删除执行链里对 `search_content` 的分支与别名映射
- [x] 清理缓存/流式事件/上下文预算中的 `search_content` 残留键
- [x] 全库检索确认：`backend/app` 下不再出现 `exact_search_paragraphs` / `search_content` 标识
- [x] 追加 review 总结与风险说明

### Review

#### 修改文件

- `backend/app/services/chapter_vector_service.py`：删除 `exact_search_paragraphs` 方法，去掉 `Tuple` 类型依赖。
- `backend/app/services/agent/langgraph_tools.py`：删除 `search_content` 工具与对应 StandardTool（`SearchContentInput/Output`、`search_content_executor`、`search_content_tool_st`），同步清理 `__all__` 与注释残留。
- `backend/app/services/agent/tools/__init__.py`：删除 `search_content_tool_st` 的懒加载导入、`__getattr__` 暴露、`__all__` 导出和自动注册。
- `backend/app/services/agent/execution/tool_executor.py`：删除 `search_content` 映射/分支；`locate_content` 自动补全改走 `search_analysis_fragments`；`_extract_first_chapter_id` 支持 `data.fragments`；删除 legacy 调用中的 `search_content`。
- `backend/app/services/agent/execution/task_runner.py`：删除 `search_content` 导入、映射、参数构造和 `ainvoke` 分支。
- `backend/app/services/agent/execution/parallel_executor.py`：并行安全工具集合中移除 `search_content`。
- `backend/app/services/agent/planning/response_builder.py`：`INPUT_TOOLS` 中移除 `search_content`。
- `backend/app/services/agent/langgraph_agent.py`：工具事件解析中移除 `search_content` 分支。
- `backend/app/services/agent/stream/flow_events.py`：工具图标映射中移除 `search_content`。
- `backend/app/services/agent/stream/event_parser.py`：显示配置/名称映射/描述生成中移除 `search_content`。
- `backend/app/services/agent/utils/context_builder.py`：工具上下文预算中移除 `search_content`。
- `backend/app/services/agent/utils/tool_cache.py`：工具缓存白名单与 TTL 中移除 `search_content`。
- `backend/app/core/config.py`：工具缓存默认配置中移除 `search_content`。
- `backend/app/services/agent/prompts/planning_prompts.py`、`backend/app/services/agent/prompts/planning_examples.py`：清理提示词里 `search_content` 文案残留。
- `backend/scripts/explore_replay_metrics.py`：日志匹配规则移除 `exact_search*` 旧关键字，改为 `search_analysis_fragments`。

#### 验证结果

- 全量检索：`rg -n "exact_search_paragraphs|search_content" backend/app backend/scripts -g"*.py" -g"*.md"` 无命中。
- 语法校验：`python3 -m py_compile ...`（本轮改动的 Python 文件）全部通过。
- 单测回归：`python3 -m pytest -q backend/tests/unit/tool_executor_continue_create_spec.py backend/tests/unit/plan_generator_rewrite_apply_ref_spec.py` → `3 passed in 1.45s`。

#### 风险说明

- 删除后历史会话或外部调用若仍显式请求 `search_content`，会走“未知工具”路径；当前提示词与执行映射已同步清理，正常新会话不会再生成该工具。

---

## 第四轮清理（2026-02-12 彻底停用 OpenSearch 同步链）

### 待办清单

- [x] `main.py`：删除启动阶段 OpenSearch 重建与同步审计调用（避免启动触发 `_search/_count`）
- [x] `chapter_vector_service.py`：删除向量化后的 OpenSearch upsert/delete 与同步状态更新调用
- [x] `chapter_vector_service.py`：删除章节删除时 OpenSearch delete 与同步状态更新调用
- [x] `chapter_vector_service.py`：移除 `OpenSearchChapterSearchService` 导入，确保运行链路不再实例化客户端
- [x] 全库检索确认：`backend/app` 运行主链不再有 `OpenSearchChapterSearchService(` 实例化点
- [x] 运行语法/定向测试并追加 review 结论

### Review

#### 修改文件

- `backend/app/main.py`：删除启动阶段 OpenSearch 重建与一致性审计调用块，改为“已停用”注释。
- `backend/app/services/chapter_vector_service.py`：删除 `OpenSearchChapterSearchService` 导入；删除 `store_chapter_vector()` 内所有 OpenSearch upsert/delete 与 sync status 更新调用；删除 `delete_chapter_vectors()` 内 OpenSearch delete 与 sync status 更新调用。

#### 验证结果

- 运行链实例化检查：`rg -n "OpenSearchChapterSearchService\\(" backend/app -g"*.py"` 无命中。
- 语法检查：`python3 -m py_compile backend/app/main.py backend/app/services/chapter_vector_service.py` 通过。
- 定向单测：`python3 -m pytest -q backend/tests/unit/tool_executor_continue_create_spec.py backend/tests/unit/plan_generator_rewrite_apply_ref_spec.py` → `3 passed in 0.77s`。

#### 结果说明

- 现在章节向量化/删除只操作 Postgres `novel_chapter_vectors`，不再触发 OpenSearch `_bulk/_count/_delete_by_query`。

---

## 新增 smart_create 工具：新建章节创作专用

### 待办清单

- [x] 步骤 1：`editor_tools.py` — 新增 `smart_create` 函数 + StandardTool 包装
- [x] 步骤 2：`__init__.py` — 导出 `smart_create` / `smart_create_tool`
- [x] 步骤 3：`explore_v6.py` — 路由增加 `smart_create` → `_run_create`
- [x] 步骤 4：`task_runner.py` — 添加参数准备和回退执行
- [x] 步骤 5：`tool_descriptions.py` — 添加工具描述
- [x] 步骤 6：`planning_prompts.py` — 更新创作类工具列表
- [x] 运行测试验证 + 追加 review

### Review

#### 修改的文件（6 个 → 深度审查后扩展至 13 个）

| 文件 | 改动 |
|------|------|
| `editor_tools.py` | 新增 `smart_create` @tool 函数（仿照 `smart_continue`，参数改为 `work_id`，prompt 侧重"从上下文创作全新章节"，`action_type` 返回 `"create"`）；新增 `SmartCreateInput/Output` + `smart_create_tool` StandardTool 包装 |
| `tools/__init__.py` | 导出 `smart_create` / `smart_create_tool`；`__all__` 添加对应条目；`_register_standard_tools()` 注册 `smart_create_tool` |
| `explore_v6.py` | `run()` 路由新增 `smart_create` → `_run_create` 显式分支 |
| `task_runner.py` | `TOOL_NAME_MAPPING` 添加 `smart_create`；`_prepare_tool_params()` 添加 `smart_create` 参数构造；`_fallback_legacy_execute()` 添加 `smart_create` 回退分支 |
| `tool_descriptions.py` | 创作类工具列表新增 `smart_create`；推荐对应关系新增 `smart_create → operate_apply(operation="create")`；新增 `smart_create` 工具描述（参数、触发词、与 smart_continue 的区别） |
| `planning_prompts.py` | 创作类工具列表新增 `smart_create`；operate_apply 表格中 create 行更新为"smart_create 后写新章节"；推荐流程新增 `smart_create → operate_apply(operation="create")`；单结果规则新增 `smart_create` |
| `tool_executor.py` | `TOOL_NAME_MAPPING` 添加 `smart_create`；worldview_hard_constraints 注入集合新增；一致性校验/extract_result/attach_consistency_report 集合新增；新增 `smart_create` 参数处理分支（work_id + evidence_context + worldview_context 注入）；LEGACY_TOOLS 导入和映射新增 |
| `response_builder.py` | `OUTPUT_TOOLS` 新增 `smart_create`；单任务直接返回/has_writing/拼接逻辑的工具集合新增 |
| `flow_events.py` | `TOOL_ICONS` 新增 `smart_create` 图标映射 |
| `event_parser.py` | `TOOL_DISPLAY_CONFIG` 新增 `smart_create`；`TOOL_DISPLAY_NAMES` 新增；`_build_tool_description` 新增描述生成 |
| `langgraph_agent.py` | `CONTENT_GENERATION_TOOLS` 新增 `smart_create`；`has_writing` 判断集合新增 |
| `langgraph_tools.py` | 导入 `smart_create`；`LANGGRAPH_TOOLS` 列表新增 |
| `plan_generator.py` | `_has_edit_tasks` 集合新增；`_ensure_replace_original_text` 创作工具集合新增；locator override 集合新增；operate_apply 依赖识别集合新增；`_build_apply_task` 新增 `smart_create` 分支（operation="create" + work_id + title）；不携带定位字段的排除集合新增 |

#### 验证结果

- 语法检查：13 个文件 `py_compile` 全部通过
- 单测回归：15 passed（explore_v6_spec 12 + plan_generator_rewrite_apply_ref_spec 1 + tool_executor_continue_create_spec 2）
- 全局同步检查：`rg '"smart_continue".*"smart_rewrite".*"smart_insert"'` 所有命中处均已同步添加 `smart_create`

#### 深度审查发现与修复

| # | 严重度 | 遗漏位置 | 修复内容 |
|---|--------|---------|---------|
| 1 | **严重** | `tool_executor.py` 缺少参数处理分支 | 新增 smart_create 分支：work_id + evidence_context + worldview_context 自动注入 |
| 2 | **严重** | `plan_generator.py` `_build_apply_task` 无 smart_create 分支 | 新增 smart_create → operate_apply(operation="create", work_id, title, content) |
| 3 | **严重** | `langgraph_tools.py` 未注册 smart_create | 导入 + LANGGRAPH_TOOLS 列表添加 |
| 4 | 高 | `langgraph_agent.py` CONTENT_GENERATION_TOOLS 缺失 | 集合新增 smart_create |
| 5 | 高 | `response_builder.py` OUTPUT_TOOLS + 3 处判断集合缺失 | 全部同步新增 |
| 6 | 高 | `plan_generator.py` 5 处工具集合缺失 | 全部同步新增 |
| 7 | 中 | `tool_executor.py` 5 处工具集合缺失 | 全部同步新增（TOOL_NAME_MAPPING、worldview 注入、一致性校验、extract_result、LEGACY_TOOLS） |
| 8 | 低 | `flow_events.py` / `event_parser.py` UI 显示缺失 | 图标/标题/描述生成全部新增 |
| 9 | 高 | `planning_examples.py` 场景5"创建新章节"示例仍使用 smart_continue | 改为 smart_create + 更新 $ref 路径和 operate_apply 参数 |
| 10 | 中 | `planning_examples.py` 创作类工具列表/推荐对应关系/operate_apply 表格缺 smart_create | 全部同步新增 |

#### 真实环境日志验证修复（2026-02-13 app.log 分析）

| # | 严重度 | 日志行 | 问题 | 修复 |
|---|--------|-------|------|------|
| 11 | **严重** | 23099 | `_ensure_replace_original_text` 检查 `chapter_id` 而 smart_create 用 `work_id` → `_build_apply_task` 的 smart_create 分支永远不执行 | 单独判断：smart_create 检查 `work_id`，其他检查 `chapter_id` |
| 12 | **严重** | 23099,23117 | AI 规划器生成错误 $ref 路径 `locate_targets[0].chapter_id`，但 `_run_create` 不返回 locate_targets → 解析越界返回 None | 新增 `_fix_smart_create_apply_params()` 方法：即使 AI 已生成 apply task，也强制覆盖为正确路径 `data.work_id/title/content` |
| 13 | 中 | 23122 | operate_apply(create) 收到现有章节 chapter_id 而非 work_id，靠 `setdefault("work_id", state.work_id)` 兜底 | 同上：修正后不再传错误的 chapter_id |

---

## 为 LightRAG 启用本地 Rerank（bge-reranker-base）

### 已完成

- [x] 修复 Docker Desktop（服务 Stopped → 重启就绪）
- [x] 修复 reranker 容器（`--device cuda` 无 GPU 卡死 → 改为本地 Python 进程 CPU 运行）
- [x] 创建 `backend/scripts/reranker_server.py`：本地 FastAPI reranker 服务（BAAI/bge-reranker-base + CrossEncoder）
- [x] 重新创建 LightRAG 容器：`RERANK_BINDING=cohere`，`RERANK_BINDING_HOST=http://host.docker.internal:7997`
- [x] LightRAG 数据卷持久化（`lightrag_data` 命名卷，不再随容器删除丢数据）
- [x] `docker-compose.yml`：新增 LightRAG 服务定义（与实际容器配置一致）
- [x] `fact_retrieval_gateway.py`：新增 `lightrag_enable_rerank` 字段 + 查询 payload 传递 `enable_rerank`
- [x] `backend/.env` + `.env.example`：新增 `LIGHTRAG_ENABLE_RERANK=true`
- [x] 验证：LightRAG health 返回 `enable_rerank=True, rerank_binding=cohere`

### 待办

- [ ] 将 `MIN_RERANK_SCORE` 从 0.0 改为 0.3（让 rerank 真正过滤低分 chunk）
- [ ] 重新导入小说数据到 LightRAG（旧索引随容器删除已丢失）

---

## Explore → Create 架构重设计（核心问题）

### 根本问题

**Explore 阶段和 Create 阶段是割裂的。**

Explore 不知道下游工具是谁，盲目做一次通用 LightRAG 检索，返回散乱 chunk。三种创作工具各自需要完全不同的上下文，但拿到的是同一堆无差别的检索结果。真正有用的上下文全靠后面的 `_augment_*` 补救函数从 DB 二次读取。

**现状数据流**：
```
plan_generator（不传下游工具）
  → explore_content（通用 LightRAG 检索，返回散乱 chunk）
    → smart_insert / smart_continue / smart_rewrite（拿到同一堆 chunk）
      → _augment_*（二次补救，从 DB 读真正需要的上下文）
```

### 三种创作操作的上下文需求（纯写作逻辑）

#### 1. 插入内容（局部操作——一个点的前后文）

| 必须知道 | 为什么 |
|---------|--------|
| 插入点前面 2-3 段原文 | 衔接上文语境、情绪、节奏 |
| 插入点后面 2-3 段原文 | 插入内容要自然过渡到下文 |
| 用户意图 | 插入什么——心理描写、场景补充、对话？ |
| 涉及的角色设定 | 角色在此刻的状态、性格、说话风格 |

- **不需要**跨章节检索，不需要远距离 chunk
- chapter_id + paragraph_index 已知 → **直接从 DB 读前后段落即可**

#### 2. 章节续写（半局部操作——一条线的末端）

| 必须知道 | 为什么 |
|---------|--------|
| 当前章节末尾 1000-2000 字 | 续写的直接衔接点，语气、节奏、场景、情绪 |
| 前 1-2 章的关键情节摘要 | 防止续写和前文矛盾，保持剧情连贯 |
| 用户要求 | 续写方向——推进战斗？展开对话？转场？ |
| 涉及角色的当前状态 | 经过前面章节，角色的位置、情感、能力 |
| 世界观设定 | 力量体系、地点描述、特殊规则 |

- chapter_id 已知 → **直接从 DB 读章节末尾**
- 前文摘要可能需要 LightRAG 或 DB 读前几章

#### 3. 新建章节（全局操作——整张网的全貌）

| 必须知道 | 为什么 |
|---------|--------|
| 上一章结尾 1000-2000 字 | 新章节要和上一章自然衔接 |
| 全书到此为止的剧情脉络 | 整体走向、伏笔回收、主线进度 |
| 用户对新章节的要求 | 本章写什么、重点场景、冲突、转折 |
| 主要角色的累积状态 | 经过所有前章，角色现在是什么状态 |
| 世界观设定 | 同上 |

- 这是唯一真正需要跨章节检索（LightRAG）的场景
- 需要全局视野：前文剧情线 + 角色弧光 + 世界观

#### 对比

| 维度 | 插入 | 续写 | 新建章节 |
|------|------|------|---------|
| 核心上下文 | 插入点前后 2-3 段 | 章节末尾 1000-2000 字 | 上一章结尾 + 全书脉络 |
| 操作范围 | 局部（一个点） | 半局部（章节尾部） | 全局（跨章节） |
| 需要 LightRAG 吗 | 不需要 | 少量（前章摘要） | 需要（全书脉络） |
| 世界观权重 | 低 | 中 | 高 |

**一句话**：插入要的是一个点的前后文，续写要的是一条线的末端，新建章节要的是整张网的全貌。

### 正确的设计方向

Explore 应该感知下游工具，**按需获取上下文**：

| 下游工具 | Explore 应该做什么 |
|---------|------------------|
| 插入 | 已知 chapter_id + paragraph_index → 直接读插入点前后几段（DB） |
| 续写 | 已知 chapter_id → 直接读章节末尾 + 前 1-2 章摘要 |
| 新建章节 | 读上一章结尾 + 全书剧情脉络 + 角色状态（LightRAG + DB） |

前两种甚至不需要走 LightRAG。只有新建章节可能真正需要 LightRAG 做跨章节检索。

### 当前代码中的证据

| 环节 | 证据 |
|------|------|
| plan_generator | `_build_retrieval_intent_payload()` 无 `downstream_tool` 字段 |
| explore_v6 | `generate_query()` 不知道下游工具，生成通用查询 |
| tool_executor | `_build_evidence_context()` 对三种工具完全相同逻辑 |
| 二次补救 | insert 有 `_augment_insert_context()`，rewrite 有 `_augment_rewrite_context()`，continue **无补救** |
| 实际有用上下文 | 全部来自 DB 直读，不来自 explore 的 LightRAG chunk |

### 实施方案：语义段落定位（插入 + 改写 共用）

#### 核心思路

用户描述的是语义位置（"林风进入密林之后"），不是结构位置（"第15段"）。
需要把语义描述翻译为精确的 paragraph_index。

**两个场景，同一套定位逻辑**：

| 场景 | 用户说 | reranker 找到 | 该段角色 | 下游操作 |
|------|--------|--------------|---------|---------|
| 改写 | "把林风进入密林那段改写得更有画面感" | 第14段 | **目标段落**（改写它） | smart_rewrite |
| 插入 | "在林风进入密林之后插入一段环境描写" | 第14段 | **锚点段落**（在它之后插入） | smart_insert |

#### 技术方案：Embedding 召回 + Cross-Encoder 精排

**已有基础设施**：
- bge-m3（Ollama, port 11434）— embedding 模型
- bge-reranker-base（本地 reranker_server.py, port 7997）— cross-encoder 精排模型

**两步定位**：

```
第一步：定位章节（从全书找到目标章节）
  用户描述 → bge-m3 embedding
  每章内容 → bge-m3 embedding
  余弦相似度 → 缩到 2-3 章候选
  bge-reranker 精排 → 确定第3章

第二步：定位段落（从章节内找到目标段落）
  加载第3章 → _split_paragraphs() 拆成段落（30-80段）
  用户描述 vs 每段 → bge-reranker 逐段打分
  → 第14段得分最高（核心句）
```

- 0 次 LLM 调用，全靠 embedding + reranker（本地 CPU 推理）
- cross-encoder 做 token 级交叉注意力，能区分"走向密林"和"踏入密林"的语义差异

#### 定位后的分叉

```
reranker 定位 → 第14段（核心句）

改写场景：
  target = 第14段（改写它）
  context = 第12-13段（前文）+ 第15-16段（后文）
  → 交给 smart_rewrite

插入场景：
  anchor = 第14段
  insert_position = "之后"（由用户描述中的"之后/之前"决定）
  context = 第13-14段（前文）+ 第15-16段（后文）
  → 交给 smart_insert
```

#### 相关开源项目（构建模块）

- [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding)（11.2k stars）— BGE 系列，中文最强
- [text2vec](https://github.com/shibing624/text2vec)（4.9k stars）— 中文语义匹配，有 sentence-to-paragraph 模型
- [BCEmbedding](https://github.com/netease-youdao/BCEmbedding)（1.8k stars）— 网易有道，中文优化 reranker
- [rerankers](https://github.com/AnswerDotAI/rerankers)（1.6k stars）— 统一 rerank 接口

#### 特殊情况处理

- 用户直接指定了章节（"第3章"）→ 跳过第一步，直接进入段落定位
- 用户在编辑器中选中了文本 → 前端已传 chapter_id + 选中内容，跳过两步定位
- 章节标题足够明确（规划 AI 能推断）→ 第一步可简化

---

### 实施方案：续写（smart_continue）

#### 核心特征

续写永远从章节末尾开始，**不需要定位段落**，不需要 reranker，不需要 LightRAG。
Explore 在续写场景的本质就是 **两次 DB 读取**。

#### 所需上下文

```
续写第5章

① 第5章末尾 1000-2000 字     ← 最重要，续写的衔接点（语气、节奏、场景、情绪）
② 第4章末尾 500 字           ← 前章过渡，防止断裂
③ 角色设定 + 世界观           ← 已有的 worldview 小包
④ 用户要求                    ← 续写方向（推进战斗？展开对话？转场？）
```

#### 与插入/改写的对比

| 维度 | 插入/改写 | 续写 |
|------|----------|------|
| 需要定位段落 | 是（reranker） | 否（永远是章节末尾） |
| 需要定位章节 | 可能（用户未指定时） | 通常已知 |
| 需要 LightRAG | 否 | 否 |
| 需要 reranker | 是 | 否 |
| Explore 本质 | embedding + reranker 定位 | DB 直读 |

#### 流程

```
用户："续写第5章"

第一步：DB 读当前章末尾
  加载第5章内容 → 取最后 1000-2000 字 → 作为续写衔接上下文

第二步：DB 读前一章末尾
  加载第4章内容 → 取最后 500 字 → 作为前文过渡参考

第三步：worldview 小包（已有逻辑）
  获取角色设定 + 世界观 → 作为约束

→ 全部交给 smart_continue
```

0 次 LLM 调用，0 次搜索，纯 DB 读取。

---

### 实施方案：新建章节（create_chapter）

#### 核心特征

新建章节是三个场景中最复杂的，需要**全局视野**——跨章节的剧情脉络、角色关系、世界观。
这是 LightRAG **知识图谱能力**真正该发挥作用的场景。

#### 现状问题

当前所有场景统一用 `mode=hybrid` + `only_need_context=True`：
- 跳过了 LightRAG 内部 LLM 的知识图谱推理
- 只返回原始 Document Chunks（散乱文本片段）
- `_parse_context_chunks()` 把 Entities 和 Relationships 全丢弃了
- 等于把知识图谱引擎当成笨重的向量搜索器用

#### 所需上下文

```
新建第6章：林风在密林中遭遇张三的伏击

① 上一章（第5章）末尾 1000-2000 字   ← 衔接过渡
② 全书剧情脉络                        ← 主线进度、伏笔、冲突走向
③ 角色关系与状态                       ← 林风和张三的关系、各自实力、动机
④ 世界观设定                           ← 密林的环境、力量体系规则
⑤ 用户对新章节的要求                   ← 写什么、重点场景、冲突设计
```

#### 技术方案：LightRAG mix 模式 + DB 直读

```
用户："新建第6章，林风在密林中遭遇张三的伏击"

第一步：DB 读上一章末尾
  加载第5章 → 取最后 1000-2000 字 → 衔接过渡上下文

第二步：LightRAG 知识图谱查询
  payload = {
    "query": "林风 张三 密林 伏击 当前剧情线索",
    "mode": "mix",                # 向量 + 关键词 + 知识图谱推理
    "only_need_context": False,   # 不跳过内部 LLM，让 KG 推理生效
  }
  返回：
    - Entities：林风（修仙者）、张三（敌对势力）、玄清道人（师父）...
    - Relationships：林风→师从→玄清、林风→敌对→张三、密林→位于→南荒禁地...
    - 综合分析：LightRAG 内部 LLM 综合知识图谱后的文本
  → 解析全部内容（Entities + Relationships + 文本），不再丢弃

第三步：worldview 小包（已有逻辑）
  角色设定 + 世界观 → 作为约束

→ 全部交给 smart_continue（生成新章节内容）
```

#### 与其他场景的对比

| 维度 | 插入/改写 | 续写 | 新建章节 |
|------|----------|------|---------|
| 需要定位段落 | 是（reranker） | 否 | 否 |
| 需要 LightRAG | 否 | 否 | **是（mix 模式 + KG 推理）** |
| Explore 本质 | reranker 定位 | DB 直读 | **LightRAG KG + DB 直读** |
| LLM 调用 | 0 次 | 0 次 | LightRAG 内部 1 次 |
| 耗时预期 | 快（本地推理） | 快（纯 DB） | 较慢（~60s，KG 推理）|

#### 为什么新建章节值得等 60 秒

- 新建章节本身就是重操作（生成几千字内容）
- 多等几十秒换来结构化的角色关系 + 剧情脉络，值得
- 插入/改写/续写不需要这个开销，所以不走 LightRAG

#### 需要改动的代码（预估）

- `fact_retrieval_gateway.py`：新增解析 Entities + Relationships 的逻辑（当前 `_parse_context_chunks` 只解析 Document Chunks）
- `explore_v6.py`：根据下游工具类型选择不同的查询策略（mix vs hybrid，only_need_context 开关）
- `plan_generator.py`：在 `retrieval_intent` 中传递 `downstream_tool` 字段

---

## Explore → Create 架构重设计实施（按下游工具分路获取上下文）

### 待办清单

- [x] 步骤 1：`plan_generator.py` — 新增 `_infer_downstream_tool()` 方法，在 `_rewrite_internal_explore_tasks()` 中将 `downstream_tool` 注入 `retrieval_intent`
- [x] 步骤 2：`explore_v6.py` — `run()` 方法按 `downstream_tool` 分路（locate / continue / create）+ 新增 `_resolve_target_chapter()` 辅助方法
- [x] 步骤 3：`explore_v6.py` — 实现 `_run_continue()`（纯 DB 读取续写上下文）
- [x] 步骤 4：`explore_v6.py` — 实现 `_run_locate()`（reranker 定位段落 + 前后文）+ `_rerank()` 方法
- [x] 步骤 5a：`fact_retrieval_gateway.py` — `query_lightrag_raw()` 支持 `only_need_context` 参数
- [x] 步骤 5b：`explore_v6.py` — 实现 `_run_create()`（LightRAG KG + 上一章末尾）
- [x] 步骤 6：运行测试验证 + 追加 review

### Review

#### 修改的文件（3 个）

| 文件 | 改动 |
|------|------|
| `plan_generator.py` | 新增 `_infer_downstream_tool()` 静态方法：从任务列表的 `depends_on` 依赖关系推断当前 explore 任务的下游工具名（如 `smart_insert`、`smart_continue`）。在 `_rewrite_internal_explore_tasks()` 中将推断结果注入 `retrieval_intent["downstream_tool"]` |
| `explore_v6.py` | `run()` 从单一流程改为按 `downstream_tool` 分三路：`_run_locate()`（插入/改写，reranker 精确定位段落 + 前后文）、`_run_continue()`（续写，纯 DB 读章节末尾）、`_run_create()`（新建章节，LightRAG KG mix 模式 + 上一章末尾）。新增 `_resolve_target_chapter()`、`_rerank()` 辅助方法 |
| `fact_retrieval_gateway.py` | `query_lightrag_raw()` 新增 `only_need_context` 参数（默认 True 向后兼容） |

#### 数据流变化

**之前**：
```
plan_generator（不传下游工具）
  → explore_content（统一 LightRAG hybrid 检索）
    → 三种工具拿到同一堆散乱 chunk
      → _augment_* 二次补救从 DB 读真正需要的上下文
```

**之后**：
```
plan_generator（推断 downstream_tool，注入 retrieval_intent）
  → explore_content.run() 按 downstream_tool 分路：
    ├─ smart_insert/smart_rewrite → _run_locate()
    │    reranker 精确定位段落 + 前后 3 段上下文（0 次 LLM）
    ├─ smart_continue → _run_continue()
    │    DB 直读当前章末尾 2000 字 + 前章末尾 500 字（0 次 LLM，0 次搜索）
    └─ 新建章节/未知 → _run_create()
         LightRAG mix 模式 KG 推理 + 上一章末尾 2000 字
```

#### 兼容性

- 三条路径都返回 `_build_result()` 相同结构，下游代码无需改动
- `downstream_tool` 为空或未知时走 `_run_create()`（兼容旧计划）
- 现有 12 个单测 + 3 个相关单测全部通过

#### 验证结果

- 语法检查：3 个文件 `py_compile` 全部通过
- 单测回归：`pytest -q explore_v6_spec.py` → 12 passed
- 相关单测：`pytest -q plan_generator_rewrite_apply_ref_spec.py tool_executor_continue_create_spec.py` → 3 passed

#### 深度审查修复（Review 后二次修复）

| # | 严重度 | 问题 | 修复 |
|---|--------|------|------|
| 1 | 严重 | `_run_locate` reranker 宕机时返回空 evidences，比旧逻辑更差 | 新增回退：reranker 无结果时走旧的 LightRAG + enrich_chunks + locate_in_chapters 流程 |
| 2 | 严重 | 上下文段落设了 `paragraph_index`，`_build_result` 为每个都创建 locate_target（7+ 个），可能触发"定位候选不唯一" | 上下文段落不再设 `paragraph_index`/`node_id`，只有主定位段落进入 locate_targets |
| 3 | 中等 | `_run_create` 跳过 `enrich_chunks()`，KG chunks 缺少 chapter_order/title | KG 查询结果补调 `enrich_chunks(chapters)` |
| 4 | 低 | `_parse_kg_sections()` 是死代码，没有调用方 | 已删除。`only_need_context=False` 时由 `_parse_context_chunks` 策略 3 兜底 |

修复后验证：语法 3 文件 py_compile 通过，15 passed（12 + 3）

#### 第三轮审查修复（端到端追踪 + _select_locate_target 交互验证）

| # | 严重度 | 问题 | 修复 |
|---|--------|------|------|
| 5 | **严重** | `_build_result` 为无 `paragraph_index` 的 evidence 也创建 locate_target → `_run_locate` reranker 成功时产生 2 个 locate_targets → `_select_locate_target()` 行 1620-1626 触发 `ambiguous_locator` 报错（上几轮专门修复的旧 bug 复活） | `_build_result` 新增过滤：`paragraph_index is None and not node_id` 的 evidence 不进入 locate_targets |
| 6 | 中等 | `_run_locate` 中 `_resolve_target_chapter` 失败后步骤 3 调用 `generate_query()` + `execute_query()` 找章节，reranker 再失败后步骤 4 回退又调用一次，浪费 1 次 LLM + 1 次 LightRAG | 步骤 3 的 LightRAG 查询结果缓存为 `_cached_lightrag_chunks`，步骤 4 回退时优先复用缓存 |

各路径 locate_targets 验证：
- `_run_locate` reranker 成功：1 个主定位 locate_target（有 paragraph_index），上下文证据被过滤 → 不触发 ambiguous ✓
- `_run_locate` 回退：与旧逻辑行为一致 ✓
- `_run_continue`：locate_targets=[]，smart_continue 不检查 locate_targets ✓
- `_run_create`：locate_targets=[]，新建章节不需要 ✓

修复后验证：语法通过，15 passed（12 + 3）

---

## 任务：在 WSL 的 Docker 中启动 Redis

### 待办清单

- [x] 步骤 1：检查项目内 Docker Compose 配置并确认 Redis 服务名
- [ ] 步骤 2：执行 Redis 启动命令（仅启动 Redis 服务）
- [ ] 步骤 3：检查容器运行状态与健康状态
- [ ] 步骤 4：在 `todo.md` 添加 review 总结

### Review

- 待完成

---

## Skills 页面重构 + 用户自定义 Skill 规划

### 已完成：SkillEditor 从 Tiptap 编辑器迁移到 react-markdown 渲染器

**改动文件**：
- `src/components/editor/SkillEditor.tsx`：整体重写。Tiptap WYSIWYG 编辑器 → react-markdown + react-syntax-highlighter 只读渲染组件
  - 代码块：语言标签头部（大写）+ 复制按钮（✓ 反馈）+ Prism 语法高亮（oneDark/oneLight 双主题）
  - 修复 `react-markdown` v10 的 block/inline 代码混淆：`pre` 组件统一处理块级代码，`code` 只处理行内
  - 修复无语言标记的代码块（如决策树 `├└`）不渲染问题：fallback 到 `language="text"`
  - 修复暗色模式"薄膜"问题：`codeTagProps={{ style: { background: 'transparent' } }}` 清除 oneDark 主题内层 `<code>` 自带背景
  - 添加 `remark-breaks` 插件：解决 SKILL.md 中单换行被合并为空格的问题（Markdown 标准 vs Tiptap 宽松处理）
  - 完整排版：h1-h3、p、ul/ol、blockquote、hr、strong、a、table（th/td）全部自定义渲染 + 深浅模式
  - `useDarkMode()` hook：MutationObserver 监听 `<html class="dark">` 变化

**清理**：
- `src/styles/globals.css`：删除 104 行 `.skill-tiptap-body` 相关样式（1117-1220 行）
- `package.json`：移除 5 个 Tiptap 包（`@tiptap/react`、`@tiptap/starter-kit`、`@tiptap/extension-placeholder`、`@tiptap/pm`、`tiptap-markdown`）
- 新增依赖：`remark-breaks`

**页面调整**：
- `src/views/SkillsView/index.tsx`：移除顶部页眉栏（"AI 技能" 标题 + "新建技能" 按钮）；复制按钮去掉文字只留图标

### 讨论结论：文件存储与部署持久化

**现状**：
- 章节内容以 .md 文件存储在 `data/users/{user_id}/works/{work_id}/chapters/`，数据库只存元数据
- 内置 Skill 以 SKILL.md 文件存储在 `backend/app/services/agent/skills/` 下
- `docker-compose.yml` 中 `data/` 目录**没有挂载为 Docker Volume**，容器重建会丢失所有用户章节数据

**结论**：
- 用户 Skill 采用文件系统存储（不用数据库），路径：`backend/data/user-skills/{user_id}/{skill-name}/SKILL.md`
- 格式与内置 Skill 完全一致（YAML frontmatter + Markdown 正文），编辑体验是编辑完整 .md 文件
- 多用户隔离靠目录名（user_id UUID）
- **必须修复**：`docker-compose.yml` 添加 `./data:/app/data` volume 挂载，同时保护现有章节数据和未来用户 Skill 数据
- 存储容量评估：500 用户 × 2000 章 × 2000 字 ≈ 6GB 磁盘空间，Docker Volume 完全够用，当前阶段无需对象存储（OSS/S3）

### 待实施：用户自定义 Skill 功能

详细计划见 `.claude/plans/modular-questing-flask.md`，核心要点：

**后端**（修改 `backend/app/api/v1/agent.py`）：
- 提取 `_load_builtin_skills()` + 新增 `_load_user_skills(user_id)`
- `GET /skills` 合并返回内置（`builtin: true`）+ 用户（`builtin: false, full_markdown: "..."`）
- 新增 `POST /skills`（创建 .md 文件）、`PUT /skills/{name}`（覆盖写入）、`DELETE /skills/{name}`（删除目录）
- 零数据库改动，纯文件操作

**前端**（修改 `src/views/SkillsView/index.tsx` + `src/services/agentApi.ts`）：
- 列表区分内置（⚡ Zap 图标）vs 用户（✏️ Pencil 图标）
- 用户 Skill 编辑模式：右侧面板切换为等宽字体 textarea，编辑完整 .md 文件（含 frontmatter）
- 创建 Dialog → 生成模板 .md → 自动进入编辑模式
- AlertDialog 二次确认删除

### 讨论结论：AI 辅助 Skill 创建 — skill-creator 系统提示词

**用户创建 Skill 的途径**：
1. ~~用户手动上传~~（保留意见，暂不实施）
2. **AI 辅助创建**：用户点击"使用文枢AI构建" → 跳转到 AI 对话 → Agent 引导用户通过对话构建 SKILL.md

**参考来源**：Manus 的 `tasks/deepagents/skill-creator_prod/SKILL.md`（元技能——教 AI 如何创建 Skill）

**Manus skill-creator vs 文枢 AI 的差异**：

| 维度 | Manus | 文枢 AI |
|------|-------|---------|
| 范围 | 通用，任何领域 | 小说写作领域 |
| Skill 结构 | SKILL.md + scripts/ + references/ + templates/ | 仅 SKILL.md（纯文本） |
| 初始化 | `init_skill.py` 脚本 | 通过 API 创建文件 |
| 验证 | `quick_validate.py` 脚本 | 后端做简单 frontmatter 校验 |
| 交付 | `message` tool 发送 .skill 文件 | 直接保存到用户目录 |
| 加载层级 | 3 级（metadata → body → resources） | 1 级（仅 SKILL.md） |

**文枢 AI Skill 的五段式范式**（从 7 个内置 Skill 提炼）：

```
---
name: xxx
description: "中文描述 + Use when: (...) Keywords: ..."
allowed-tools: [...]
---

# 标题

## 心智模型 (Mental Model)
   → "Before xxx, ask yourself:" 三问引导

## 核心方法论 (Expert Rules / Decision Framework)
   → 表格、决策树、分级标准等

## NEVER 规则
   → 5-6 条"绝对不要"

## 边界情况
   → 4-5 种特殊场景的处理方式

## 输出格式
   → 固定输出模板
```

**方案选择：方案 B — 独立系统提示词**

- 放置路径：`backend/app/services/agent/prompts/skill-creator.md`（或类似路径）
- 当用户发起"构建 Skill"对话时，后端把此提示词注入到 AI 对话的 system message 中
- **不作为内置 Skill**，因为它不是给"写小说的 AI"用的，而是给"帮用户构建 Skill 的 AI"用的
- 调用现有 `OpenAIService`（`backend/app/services/ai/openai_service.py`），不需要新建 AI 服务

**skill-creator 提示词需要包含的内容**：
1. 文枢 SKILL.md 的完整格式规范（YAML frontmatter 字段 + 五段式结构）
2. 1-2 个精简的内置 Skill 示例片段（作为 few-shot example）
3. 对话引导流程：理解需求（2-3 轮）→ 确认范围 → 生成完整 SKILL.md
4. 小说写作领域的特定约束（角色、世界观、情节、伏笔等维度）

**两个待解决的架构问题**：
1. **对话作用域**：AI 聊天当前绑定 work_id（作品），但 Skill 构建是全局的 → `agent_sessions.work_id` 已支持 nullable，数据层无问题，需要前端/路由层支持
2. **结果回填**：AI 生成 SKILL.md 后如何回填到 Skills 详情页 → 需设计"对话完成 → 自动保存到用户 Skill 目录 → 跳转/通知 Skills 页面"的流程
