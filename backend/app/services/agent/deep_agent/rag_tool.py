"""
RAG 混合搜索 Tool

基于 ChromaDB 向量检索 + BM25 关键词检索的混合语义搜索工具。
使用 RRF (Reciprocal Rank Fusion) 算法融合两路检索结果。

功能：
1. create_semantic_search_tool — 创建可注入 Agent 的混合检索工具
2. update_chapter_vectors    — 章节变更后更新向量索引
3. update_knowledge_vectors  — 知识库文件变更后更新向量索引
4. remove_chapter_vectors    — 删除指定路径的向量
"""

import logging
import re
import threading
import time
from collections import defaultdict
from typing import Any, List, Optional

import chromadb
import jieba
from langchain_chroma import Chroma
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.retrievers import BaseRetriever
from langchain_core.tools import BaseTool
from langchain_core.tools.retriever import create_retriever_tool
from rank_bm25 import BM25Okapi

logger = logging.getLogger(__name__)

# ─── Embedding 适配器 ───


class SharedEmbeddingAdapter(Embeddings):
    """将共享 SentenceTransformer 单例包装为 LangChain Embeddings 接口。"""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        from app.services.embedding import get_model
        model = get_model()
        return model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        from app.services.embedding import get_model
        model = get_model()
        return model.encode([text], normalize_embeddings=True)[0].tolist()


# ─── 全局 Embedding 实例 ───

_embedding = SharedEmbeddingAdapter()

# ─── BM25 缓存管理 ───

_BM25_TTL_SECONDS = 1800  # 30 分钟未访问则淘汰


class _BM25Store:
    """内存中的 BM25 索引，从 ChromaDB 懒加载构建。"""

    __slots__ = ("docs", "bm25", "last_accessed")

    def __init__(self, docs: List[Document], bm25: Optional[BM25Okapi]):
        self.docs = docs
        self.bm25 = bm25  # None when collection is empty
        self.last_accessed = time.time()

    def query(self, text: str, k: int = 10) -> List[Document]:
        self.last_accessed = time.time()
        if self.bm25 is None or not self.docs:
            return []
        tokens = _jieba_tokenize(text)
        if not tokens:
            return []
        scores = self.bm25.get_scores(tokens)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.docs[i] for i in top_indices if scores[i] > 0]


_bm25_stores: dict[str, _BM25Store] = {}
_bm25_lock = threading.Lock()


_CHINESE_CHAR_RE = re.compile(r'[\u4e00-\u9fff]')


def _jieba_tokenize(text: str) -> List[str]:
    """jieba 分词，过滤纯符号和空白，但保留单个汉字。"""
    return [
        w for w in jieba.cut(text)
        if w.strip() and (len(w) > 1 or _CHINESE_CHAR_RE.match(w))
    ]


def _get_or_build_bm25_store(work_id: str, vectorstore: Chroma) -> _BM25Store:
    """获取或构建 BM25 索引（从 ChromaDB 懒加载）。"""
    with _bm25_lock:
        store = _bm25_stores.get(work_id)
        if store is not None:
            store.last_accessed = time.time()
            return store

    # 从 ChromaDB 读取全部文档（在锁外执行，避免阻塞）
    try:
        collection = vectorstore._collection
        result = collection.get(include=["documents", "metadatas"])
        docs = [
            Document(page_content=text, metadata=meta or {})
            for text, meta in zip(result["documents"] or [], result["metadatas"] or [])
            if text and text.strip()
        ]
    except Exception as e:
        logger.warning("Failed to load documents from ChromaDB for BM25: %s", e)
        docs = []

    # 构建 BM25 索引
    if docs:
        tokenized = [_jieba_tokenize(d.page_content) for d in docs]
        bm25 = BM25Okapi(tokenized)
    else:
        bm25 = None

    store = _BM25Store(docs=docs, bm25=bm25)

    with _bm25_lock:
        _bm25_stores[work_id] = store
        # LRU 清理：淘汰过期缓存
        now = time.time()
        expired = [k for k, v in _bm25_stores.items() if now - v.last_accessed > _BM25_TTL_SECONDS]
        for k in expired:
            del _bm25_stores[k]

    return store


def _invalidate_bm25_store(work_id: str) -> None:
    """向量更新后失效 BM25 缓存，下次查询时自动重建。"""
    with _bm25_lock:
        _bm25_stores.pop(work_id, None)


# ─── RRF 融合 ───


def _rrf_fuse(
    doc_lists: List[List[Document]],
    weights: List[float],
    rrf_k: int = 60,
) -> List[Document]:
    """加权 Reciprocal Rank Fusion。

    Args:
        doc_lists: 每个 retriever 返回的文档列表
        weights: 每个 retriever 的权重
        rrf_k: RRF 常数（默认 60）
    """
    scores: dict[str, float] = defaultdict(float)
    doc_map: dict[str, Document] = {}

    for doc_list, weight in zip(doc_lists, weights):
        for rank, doc in enumerate(doc_list, start=1):
            key = f"{doc.metadata.get('source', '')}:{doc.page_content}"
            scores[key] += weight / (rank + rrf_k)
            if key not in doc_map:
                doc_map[key] = doc

    sorted_keys = sorted(scores, key=lambda x: scores[x], reverse=True)
    return [doc_map[k] for k in sorted_keys]


# ─── 混合检索器 ───


from pydantic import ConfigDict


class HybridRetriever(BaseRetriever):
    """BM25 + ChromaDB 向量混合检索，RRF 融合。"""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    work_id: str
    vectorstore: Any  # Chroma instance
    k: int = 8
    vector_weight: float = 0.7
    bm25_weight: float = 0.3

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: Optional[CallbackManagerForRetrieverRun] = None,
    ) -> List[Document]:
        # 1. 向量检索 top-10
        try:
            vector_docs = self.vectorstore.as_retriever(
                search_kwargs={"k": 10}
            ).invoke(query)
        except Exception as e:
            logger.warning("Vector retrieval failed: %s", e)
            vector_docs = []

        # 2. BM25 检索 top-10
        try:
            bm25_store = _get_or_build_bm25_store(self.work_id, self.vectorstore)
            bm25_docs = bm25_store.query(query, k=10)
        except Exception as e:
            logger.warning("BM25 retrieval failed: %s", e)
            bm25_docs = []

        # 3. RRF 融合
        if not vector_docs and not bm25_docs:
            return []

        fused = _rrf_fuse(
            [vector_docs, bm25_docs],
            [self.vector_weight, self.bm25_weight],
        )

        return fused[:self.k]


# ─── 创建检索工具 ───


def create_semantic_search_tool(
    work_id: str,
    persist_dir: str = "./data/chroma_db",
) -> BaseTool:
    """创建混合语义搜索 Tool，可注入 DeepAgents。

    内部同时执行向量语义检索和 BM25 关键词检索，RRF 融合返回最佳结果。

    Args:
        work_id: 作品 ID（用作 ChromaDB collection 名）
        persist_dir: ChromaDB 持久化目录

    Returns:
        LangChain BaseTool 实例
    """
    client = chromadb.PersistentClient(path=persist_dir)
    collection_name = f"work_{work_id.replace('-', '_')}"

    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=_embedding,
    )

    retriever = HybridRetriever(work_id=work_id, vectorstore=vectorstore)

    return create_retriever_tool(
        retriever,
        name="semantic_search",
        description=(
            "在全书章节和知识库（outline/characters/worldview/refs/*）中做混合搜索。"
            "输入一段描述或关键词（如'主角的武器是什么'、'力量体系规则'、'时间线 永历三年'），"
            "返回最相关的文本片段。支持语义匹配和关键词精确匹配，"
            "用于一致性检查、前文回顾、设定查证等场景。"
        ),
    )


# ─── 更新向量索引 ───


def _update_vectors(
    work_id: str,
    path: str,
    content: str,
    doc_type: str,
    persist_dir: str = "./data/chroma_db",
) -> None:
    """内部统一函数：更新指定路径的向量索引。

    先删除该路径的旧文档，再切块后重新入库。

    Args:
        work_id: 作品 ID
        path: 文件路径（如 /chapters/01-考核之日.md 或 /knowledge/outline.md）
        content: 文件正文内容
        doc_type: 文档类型（"chapter" 或 "knowledge"）
        persist_dir: ChromaDB 持久化目录
    """
    client = chromadb.PersistentClient(path=persist_dir)
    collection_name = f"work_{work_id.replace('-', '_')}"

    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=_embedding,
    )

    # 删除旧文档
    try:
        collection = client.get_or_create_collection(collection_name)
        existing = collection.get(where={"source": path})
        if existing["ids"]:
            collection.delete(ids=existing["ids"])
    except Exception as e:
        logger.warning("Failed to delete old vectors for %s: %s", path, e)

    # 切块：500 字 / 50 字重叠 / 中文标点分隔
    chunks = _split_chinese_text(content, chunk_size=500, overlap=50)
    if not chunks:
        return

    docs = [
        Document(
            page_content=chunk,
            metadata={"source": path, "chunk_index": i, "doc_type": doc_type},
        )
        for i, chunk in enumerate(chunks)
    ]

    vectorstore.add_documents(docs)
    logger.info("Updated %d %s chunks for %s in work %s", len(docs), doc_type, path, work_id)

    # 失效 BM25 缓存
    _invalidate_bm25_store(work_id)


def update_chapter_vectors(
    work_id: str,
    path: str,
    content: str,
    persist_dir: str = "./data/chroma_db",
) -> None:
    """章节变更后更新向量索引。

    Args:
        work_id: 作品 ID
        path: 章节文件路径（如 /chapters/01-考核之日.md）
        content: 章节正文内容（不含 frontmatter）
        persist_dir: ChromaDB 持久化目录
    """
    _update_vectors(work_id, path, content, doc_type="chapter", persist_dir=persist_dir)


def update_knowledge_vectors(
    work_id: str,
    path: str,
    content: str,
    persist_dir: str = "./data/chroma_db",
) -> None:
    """知识库文件变更后更新向量索引。

    Args:
        work_id: 作品 ID
        path: 知识库文件路径（如 /knowledge/outline.md）
        content: 文件内容（纯文本，无 frontmatter）
        persist_dir: ChromaDB 持久化目录
    """
    _update_vectors(work_id, path, content, doc_type="knowledge", persist_dir=persist_dir)


def remove_chapter_vectors(
    work_id: str,
    path: str,
    persist_dir: str = "./data/chroma_db",
) -> None:
    """Remove all vector chunks for a given path (chapter or knowledge)."""
    client = chromadb.PersistentClient(path=persist_dir)
    collection_name = f"work_{work_id.replace('-', '_')}"
    try:
        collection = client.get_or_create_collection(collection_name)
        existing = collection.get(where={"source": path})
        ids = existing.get("ids") or []
        if ids:
            collection.delete(ids=ids)
            logger.info("Removed %d vector chunks for %s in work %s", len(ids), path, work_id)
    except Exception as e:
        logger.warning("Failed to remove vectors for %s: %s", path, e)

    _invalidate_bm25_store(work_id)


def _split_chinese_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> List[str]:
    """按中文标点和字数切分文本。"""
    # 按中文句号/问号/叹号/换行分句
    sentences = re.split(r'(?<=[。！？\n])', text)
    sentences = [s for s in sentences if s.strip()]

    chunks = []
    current = ""

    for sent in sentences:
        if len(current) + len(sent) > chunk_size and current:
            chunks.append(current)
            # 保留重叠
            current = current[-overlap:] + sent if overlap > 0 else sent
        else:
            current += sent

    if current.strip():
        chunks.append(current)

    return chunks
