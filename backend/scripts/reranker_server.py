# -*- coding: utf-8 -*-
"""本地 Reranker 服务（CPU）.

用 sentence-transformers CrossEncoder 加载 BAAI/bge-reranker-base，
暴露 Cohere 兼容的 /rerank 端点，供 LightRAG 调用。

启动方式：
    python backend/scripts/reranker_server.py
"""

import logging
import time

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("reranker")

# --------------- 模型加载 ---------------

MODEL_NAME = "BAAI/bge-reranker-base"
_model = None


def get_model():
    global _model
    if _model is None:
        from sentence_transformers import CrossEncoder
        logger.info("加载模型 %s ...", MODEL_NAME)
        t0 = time.time()
        _model = CrossEncoder(MODEL_NAME, max_length=512)
        logger.info("模型加载完成，耗时 %.1fs", time.time() - t0)
    return _model


# --------------- API ---------------

app = FastAPI(title="Local Reranker")


class RerankRequest(BaseModel):
    query: str
    documents: List[str]
    top_n: Optional[int] = None
    model: Optional[str] = None


class RerankResult(BaseModel):
    index: int
    relevance_score: float
    document: Optional[str] = None


class RerankResponse(BaseModel):
    results: List[RerankResult]
    model: str = MODEL_NAME


@app.post("/rerank")
async def rerank(req: RerankRequest) -> RerankResponse:
    model = get_model()
    pairs = [(req.query, doc) for doc in req.documents]
    scores = model.predict(pairs).tolist()

    ranked = sorted(
        [{"index": i, "relevance_score": float(s)} for i, s in enumerate(scores)],
        key=lambda x: x["relevance_score"],
        reverse=True,
    )

    top_n = req.top_n or len(ranked)
    results = [
        RerankResult(index=r["index"], relevance_score=r["relevance_score"])
        for r in ranked[:top_n]
    ]
    logger.info("rerank query=%s docs=%d top=%d best=%.3f",
                req.query[:40], len(req.documents), top_n,
                results[0].relevance_score if results else 0)
    return RerankResponse(results=results)


@app.get("/health")
async def health():
    return {"status": "ok", "model": MODEL_NAME}


if __name__ == "__main__":
    # 启动时预加载模型
    get_model()
    uvicorn.run(app, host="0.0.0.0", port=7997)
