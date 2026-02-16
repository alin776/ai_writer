"""
RAG 语义搜索 Tool

基于 ChromaDB + BGE-small-zh-v1.5 的语义检索工具。
提供两个功能：
1. create_semantic_search_tool — 创建可注入 Agent 的检索工具
2. update_chapter_vectors — 章节变更后更新向量索引
"""

import logging
import re
from typing import List

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.tools import BaseTool
from langchain_core.tools.retriever import create_retriever_tool

logger = logging.getLogger(__name__)

# ─── Embedding 适配器 ───


class ChromaEmbeddingAdapter(Embeddings):
    """将 SentenceTransformer 包装为 LangChain Embeddings 接口。"""

    _models: dict[str, "SentenceTransformer"] = {}  # 按模型名缓存

    def __init__(self, model_name: str = "BAAI/bge-small-zh-v1.5"):
        self._model_name = model_name

    def _get_model(self):
        if self._model_name not in ChromaEmbeddingAdapter._models:
            from sentence_transformers import SentenceTransformer
            ChromaEmbeddingAdapter._models[self._model_name] = SentenceTransformer(self._model_name)
            logger.info("Loaded embedding model: %s", self._model_name)
        return ChromaEmbeddingAdapter._models[self._model_name]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        model = self._get_model()
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        model = self._get_model()
        embedding = model.encode([text], normalize_embeddings=True)
        return embedding[0].tolist()


# ─── 全局 Embedding 实例 ───

_embedding = ChromaEmbeddingAdapter()


# ─── 创建检索工具 ───


def create_semantic_search_tool(
    work_id: str,
    persist_dir: str = "./data/chroma_db",
) -> BaseTool:
    """创建语义搜索 Tool，可注入 DeepAgents。

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

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    return create_retriever_tool(
        retriever,
        name="semantic_search",
        description=(
            "在全书已有章节中做语义搜索。"
            "输入一段描述（如'主角的武器是什么'、'第一次出现反派的场景'），"
            "返回最相关的文本片段。用于一致性检查、前文回顾等场景。"
        ),
    )


# ─── 更新向量索引 ───


def update_chapter_vectors(
    work_id: str,
    path: str,
    content: str,
    persist_dir: str = "./data/chroma_db",
) -> None:
    """章节变更后更新向量索引。

    先删除该路径的旧文档，再切块后重新入库。

    Args:
        work_id: 作品 ID
        path: 章节文件路径（如 /chapters/01-考核之日.md）
        content: 章节正文内容（不含 frontmatter）
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
            metadata={"source": path, "chunk_index": i},
        )
        for i, chunk in enumerate(chunks)
    ]

    vectorstore.add_documents(docs)
    logger.info("Updated %d chunks for %s in work %s", len(docs), path, work_id)


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
