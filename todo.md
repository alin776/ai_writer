# TODO

---

## Explore V6 执行流程优化

### 问题 1：查询高度重叠，67% 浪费

**现状**：AI 分解出 3 条查询，各返回 ~11 条 chunk，合计 33 条，去重后只剩 11 条。2/3 的 LightRAG 调用是浪费的。

**方案**：只用 1 条查询，去掉分解、并行、去重逻辑，大幅减少 token 消耗和 LightRAG 调用次数。

- [x] `explore_v6.py`：`decompose_queries` 改为 `generate_query` 生成 1 条短查询，删除 `execute_parallel` 并行/去重逻辑，改为 `execute_query` 单次调用

### 问题 2+3：KG 数据丢弃 + mix 模式白等 60s

**现状**：`mode="mix"` 触发 LightRAG 内部 LLM 做 KG 推理（60s），但 `_parse_context_chunks` 只提取 Document Chunks，KG 实体数据全部丢弃。等于花 60s 换来一堆不用的东西。

**分析**：本地数据库已有完整结构化元数据（characters/locations/settings/guidelines/glossary/relationships/timeline 共 7 张表），且 Explore V6 已通过 `get_worldview_pack` 在使用。LightRAG KG 与本地 DB 高度重复，解析不可靠，不值得为它多花 55s。

**方案**：`mode` 从 `mix` 改为 `hybrid`（向量 + 关键词，无内部 LLM），响应从 60s 降到 <5s。

- [x] `config.py`：`LIGHTRAG_MODE` 默认值从 `"mix"` 改为 `"hybrid"`
- [x] `fact_retrieval_gateway.py`：所有 fallback 默认值也改为 `"hybrid"`

### 问题 4：子串定位脆弱 + LightRAG 未接入导入流程

**现状**：LightRAG 数据是外部手动导入的，没有 chapter_id 元数据。查询返回的 chunk 只有纯文本，`locate_chunks` 被迫用前 80 字符做 `str.find()` 遍历所有章节定位，实测 1/11 失败率。

**方案**：插入时 `file_source="chapter_{chapter_id}"`，查询时 `include_references=True`，从 `references[].file_path` 提取 `chapter_id`。

- [x] `config.py`：新增 `LIGHTRAG_INSERT_PATH` 配置
- [x] `fact_retrieval_gateway.py`：新增 `insert_document()` 方法 + `_build_ref_chapter_map()` + 查询添加 `include_references=True`
- [x] `_parse_context_chunks`：同时提取 `reference_id` 和 `content`
- [x] `import_service.py`：后处理链新增 `_insert_chapters_to_lightrag()` 步骤
- [x] `explore_v6.py`：删除 `locate_chunks` / `_load_chapter_cache`，新增 `enrich_chunks()` 用 chapter_id 补全元数据

### 问题 5：每次新建 Gateway 实例

**现状**：`execute_parallel` 每次 `FactRetrievalGateway()`，重复解析 10+ 次 `os.getenv()`。

**方案**：改为模块级单例。

- [x] `fact_retrieval_gateway.py`：新增 `get_gateway()` 单例函数
- [x] `explore_v6.py`：调用 `get_gateway()` 替代 `FactRetrievalGateway()`

---

## 执行计划

### 阶段 1：Gateway 基础改造（问题 5 + 2+3）✅

1. `fact_retrieval_gateway.py`：新增 `get_gateway()` 单例
2. `config.py`：`LIGHTRAG_MODE` 默认值 `"mix"` → `"hybrid"`

### 阶段 2：查询简化（问题 1）✅

3. `explore_v6.py`：`decompose_queries` → `generate_query`（单条短查询）
4. `explore_v6.py`：`execute_parallel` → `execute_query`（单次调用，用 `get_gateway()` 单例）

### 阶段 3：LightRAG 导入集成（问题 4）✅

5. `config.py`：新增 `LIGHTRAG_INSERT_PATH`
6. `fact_retrieval_gateway.py`：新增 `insert_document()` + 查询加 `include_references` + `_build_ref_chapter_map()`
7. `import_service.py`：后处理链新增 `_insert_chapters_to_lightrag()`
8. `_parse_context_chunks`：返回 `{reference_id, content}` 结构
9. `explore_v6.py`：删除 `locate_chunks` / `_load_chapter_cache`，新增 `enrich_chunks()`

---

## Review

### 修改的文件（6 个）

| 文件 | 改动 |
|------|------|
| `config.py` | `LIGHTRAG_MODE` 默认值 `mix` → `hybrid`；新增 `LIGHTRAG_INSERT_PATH`；删除死配置 `EXPLORE_V6_MAX_QUERIES` |
| `fact_retrieval_gateway.py` | 新增 `get_gateway()` 单例；新增 `insert_document()` + `_build_ref_chapter_map()`；`query_lightrag_raw` 添加 `include_references=True`，从 references 提取 chapter_id；`_parse_context_chunks` 返回含 reference_id 的 dict 列表；清理未使用的 `field` import |
| `explore_v6.py` | `decompose_queries` → `generate_query`（单条 10-30 字短查询）；`execute_parallel` → `execute_query`（单次调用）；删除 `locate_chunks` + `_load_chapter_cache`（~70 行），新增 `enrich_chunks()`（~20 行）；清理 `must_have` 残留引用；更新 docstring；清理未使用的 `field`/`asyncio` import |
| `import_service.py` | `_import_json` 和 `_import_text` 后处理链新增 LightRAG 插入步骤；新增 `_insert_chapters_to_lightrag()` 方法 |
| `evidence_store.py` | `has("locate_targets")` 判断条件从 `chapter_id + (paragraph_index or node_id)` 简化为仅需 `chapter_id`（适配 V6 不再返回段落级定位） |
| `explore_v6_spec.py` | 重写全部测试：`decompose_queries` → `generate_query`，`execute_parallel` → 删除，新增 `enrich_chunks` 测试，新增源码方法存在性断言 |

### 数据流变化

**之前**：
```
AI 分解 → 3 条长查询 → 并行 LightRAG(mix, 60s×3) → 合并去重(33→11) → 子串匹配定位(1/11 失败)
```

**之后**：
```
AI 生成 → 1 条短查询 → 单次 LightRAG(hybrid, <5s) → references 提取 chapter_id → 直接定位(100%)
```
