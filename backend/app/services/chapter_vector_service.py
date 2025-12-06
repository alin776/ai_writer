"""
章节向量服务
专门用于RAG续写上下文检索，与分析系统解耦
"""
import logging
import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete

# 确保在导入 sentence_transformers 前设置好镜像与缓存目录，避免访问 huggingface.co 超时
_default_hf_endpoint = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_ENDPOINT", _default_hf_endpoint)
_hf_cache_dir = Path(__file__).resolve().parents[2] / "data" / "hf_cache"
_hf_cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(_hf_cache_dir))
os.environ.setdefault("HF_HUB_CACHE", str(_hf_cache_dir))

from sentence_transformers import SentenceTransformer
import numpy as np

from app.models.novel_chapter_vector import NovelChapterVector

logger = logging.getLogger(__name__)


class ChapterVectorService:
    """章节向量服务 - 专门用于RAG续写"""

    # 使用与VectorStoreService相同的模型（保持一致性）
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    VECTOR_DIM = 384
    MAX_CHUNKS = 2000  # 保护性上限，防止超大文本生成过多向量

    def __init__(self, db: AsyncSession):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db

    def _get_model(self) -> SentenceTransformer:
        """
        获取Embedding模型（复用全局预加载的模型）

        Returns:
            SentenceTransformer: 模型实例
        """
        from app.services.vector_store_service import VectorStoreService

        # 复用VectorStoreService的全局模型
        if VectorStoreService._global_model is None:
            logger.info(f"正在加载Embedding模型: {self.MODEL_NAME}")
            VectorStoreService._global_model = SentenceTransformer(
                self.MODEL_NAME, cache_folder=str(VectorStoreService.CACHE_DIR)
            )
            logger.info("Embedding模型加载成功")

        return VectorStoreService._global_model

    def _split_content(self, content: str, chunk_size: int = 500, max_chunks: Optional[int] = None) -> List[str]:
        """
        内容分段（按句子边界切分）

        Args:
            content: 章节内容
            chunk_size: 每段最大字符数
            max_chunks: 分块数量上限（超过则截断并记录告警）

        Returns:
            List[str]: 分段后的文本列表
        """
        # 按中文句子边界分割
        sentences = re.split(r'([。！？\n])', content)

        chunks = []
        current_chunk = ""

        for i in range(0, len(sentences), 2):
            sentence = sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else "")

            if len(current_chunk) + len(sentence) > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        # 过滤过短的段落（<50字符）
        chunks = [c for c in chunks if len(c) >= 50]

        if max_chunks is not None and len(chunks) > max_chunks:
            logger.warning(
                f"章节分块数量 {len(chunks)} 超过上限 {max_chunks}，将截断多余分块"
            )
            chunks = chunks[:max_chunks]

        return chunks

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        计算余弦相似度

        Args:
            a: 向量A
            b: 向量B

        Returns:
            float: 相似度（0-1）
        """
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    async def store_chapter_vector(
        self,
        work_id: str,
        chapter_id: str,
        chapter_order: int,
        chapter_title: str,
        content: str,
        chunk_size: int = 500,
        max_chunks: Optional[int] = None
    ) -> int:
        """
        存储章节内容向量（幂等操作）

        Args:
            work_id: 作品ID
            chapter_id: 章节ID
            chapter_order: 章节顺序
            chapter_title: 章节标题
            content: 章节内容
            chunk_size: 分块大小（默认500字符）
            max_chunks: 分块上限，防止超大文本占用过多资源

        Returns:
            int: 存储的向量数量

        Raises:
            Exception: 存储失败
        """
        try:
            logger.info(f"开始向量化章节: {chapter_title} (order={chapter_order})")

            # 1. 删除该章节的旧向量（幂等性）
            stmt = sql_delete(NovelChapterVector).where(
                NovelChapterVector.chapter_id == chapter_id
            )
            await self.db.execute(stmt)
            await self.db.flush()

            # 2. 内容分段
            chunks = self._split_content(
                content,
                chunk_size=chunk_size,
                max_chunks=max_chunks or self.MAX_CHUNKS,
            )

            if len(chunks) == 0:
                logger.warning(f"⚠️ 章节内容过短，跳过向量化: {chapter_title}")
                await self.db.commit()
                return 0

            # 3. 批量生成embedding
            model = self._get_model()
            embeddings = model.encode(chunks, normalize_embeddings=True)

            # 4. 批量存储
            from uuid import UUID
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id
            chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

            vectors = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                vector = NovelChapterVector(
                    work_id=work_uuid,
                    chapter_id=chapter_uuid,
                    chapter_order=chapter_order,
                    chapter_title=chapter_title,
                    chunk_index=idx,
                    chunk_text=chunk,
                    embedding=embedding.tolist()
                )
                vectors.append(vector)

            self.db.add_all(vectors)
            await self.db.commit()

            logger.info(f"✅ 章节向量存储完成: {chapter_title} ({len(chunks)}段)")
            return len(chunks)

        except Exception as e:
            logger.error(f"❌ 章节向量存储失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def retrieve_for_writing(
        self,
        work_id: str,
        current_chapter_order: int,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        检索续写上下文（关键：只检索当前章节之前的章节）

        Args:
            work_id: 作品ID
            current_chapter_order: 当前章节顺序
            query: 查询文本
            top_k: 返回前K个结果
            similarity_threshold: 相似度阈值

        Returns:
            List[Dict]: 相关的段落列表，每项包含：
                - chapter_title: 章节标题
                - chapter_order: 章节顺序
                - chunk_text: 段落文本
                - similarity: 相似度分数
        """
        try:
            logger.info(
                f"RAG检索: work_id={work_id}, "
                f"current_order={current_chapter_order}, "
                f"query={query[:50]}..."
            )

            # 1. 向量化查询
            model = self._get_model()
            query_embedding = model.encode([query], normalize_embeddings=True)[0]

            # 2. 获取所有前文章节的向量（🔑 关键：时序过滤）
            from uuid import UUID
            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            stmt = select(NovelChapterVector).where(
                NovelChapterVector.work_id == work_uuid,
                NovelChapterVector.chapter_order < current_chapter_order  # 🔑 只检索前文
            )
            result = await self.db.execute(stmt)
            vectors = result.scalars().all()

            if len(vectors) == 0:
                logger.warning(
                    f"⚠️ 作品 {work_id} 前{current_chapter_order - 1}章暂无向量数据"
                )
                return []

            # 3. 计算相似度
            results = []
            for vector in vectors:
                embedding = np.array(vector.embedding)
                similarity = self._cosine_similarity(query_embedding, embedding)

                if similarity >= similarity_threshold:
                    results.append({
                        'chapter_title': vector.chapter_title,
                        'chapter_order': vector.chapter_order,
                        'chunk_text': vector.chunk_text,
                        'similarity': float(similarity)
                    })

            # 4. 按相似度排序，返回top_k
            results.sort(key=lambda x: x['similarity'], reverse=True)
            results = results[:top_k]

            logger.info(
                f"✅ RAG检索成功: work={work_id}, "
                f"前{current_chapter_order - 1}章, "
                f"检索到{len(results)}个相关段落"
            )

            return results

        except Exception as e:
            logger.error(f"❌ RAG检索失败: {e}", exc_info=True)
            return []

    async def delete_chapter_vectors(self, chapter_id: str) -> int:
        """
        删除章节的向量数据

        Args:
            chapter_id: 章节ID

        Returns:
            int: 删除的记录数
        """
        try:
            from uuid import UUID
            chapter_uuid = UUID(chapter_id) if isinstance(chapter_id, str) else chapter_id

            stmt = sql_delete(NovelChapterVector).where(
                NovelChapterVector.chapter_id == chapter_uuid
            )
            result = await self.db.execute(stmt)
            await self.db.commit()

            deleted_count = result.rowcount
            logger.info(f"删除章节 {chapter_id} 的 {deleted_count} 条向量记录")
            return deleted_count

        except Exception as e:
            logger.error(f"删除章节向量失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def get_stats(self, work_id: str) -> Dict[str, Any]:
        """
        获取作品的向量统计

        Args:
            work_id: 作品ID

        Returns:
            Dict: 统计信息
        """
        try:
            from uuid import UUID
            from sqlalchemy import func

            work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id

            stmt = select(
                func.count(NovelChapterVector.id).label('total_vectors'),
                func.count(func.distinct(NovelChapterVector.chapter_id)).label('total_chapters')
            ).where(NovelChapterVector.work_id == work_uuid)

            result = await self.db.execute(stmt)
            row = result.first()

            return {
                'total_vectors': row.total_vectors if row else 0,
                'total_chapters': row.total_chapters if row else 0,
                'vector_dimension': self.VECTOR_DIM,
                'model_name': self.MODEL_NAME
            }

        except Exception as e:
            logger.error(f"获取向量统计失败: {e}", exc_info=True)
            return {
                'total_vectors': 0,
                'total_chapters': 0,
                'vector_dimension': self.VECTOR_DIM,
                'model_name': self.MODEL_NAME
            }
