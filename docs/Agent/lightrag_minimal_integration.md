# LightRAG 单后端接入说明（FactRetrievalGateway）

## 1. 目标

`retrieve_facts` 检索链路固定为 **LightRAG**，不再保留旧词法后端与任何回退分支。

## 2. 代码变更点

- `backend/app/services/agent/retrieval/fact_retrieval_gateway.py`
  - 删除旧后端执行与回退逻辑
  - 固定分发到 `lightrag`
  - 保留统一响应字段：`backend`、`backend_fallback_reason`
- `backend/app/core/config.py`
  - `FACT_RETRIEVAL_BACKEND` 默认值改为 `lightrag`
  - 删除 `FACT_RETRIEVAL_BACKEND_FALLBACK`、`FACT_RETRIEVAL_EXTERNAL_FALLBACK_ENABLED`

## 3. 配置项

```env
# 事实检索后端（固定）
FACT_RETRIEVAL_BACKEND=lightrag

# LightRAG
LIGHTRAG_BASE_URL=http://127.0.0.1:9621
LIGHTRAG_QUERY_PATH=/query
LIGHTRAG_API_KEY=
LIGHTRAG_TIMEOUT_SECONDS=20
LIGHTRAG_MODE=mix
LIGHTRAG_TOP_K=20
```

## 4. 验收口径（最小）

1. 单测通过

```bash
pytest -q backend/tests/unit/fact_retrieval_gateway_spec.py
```

2. 关键日志可观测

- 分发日志：`[FactRetrieval] dispatch backend=lightrag ...`
- 命中日志：`[FactRetrieval] backend=lightrag endpoint=... hits=...`

3. 响应字段可观测

- `backend`: `lightrag`
- `backend_fallback_reason`: 始终为空字符串（无回退机制）

## 5. 当前限制（已知）

- LightRAG 结果不一定总带 `chapter_order/paragraph_index`，网关会尽量从元数据或文本猜测定位。
- 若需要稳定段落级定位，建议后续补充“离线事实表 + 稳定 locator 映射”。
- 若 LLM 网关不支持 `/embeddings`，LightRAG 文档入库会失败（常见日志：`openai.NotFoundError: 404 page not found`）。
