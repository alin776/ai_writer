"""
向量存储服务
负责微观分析结果的向量化存储和检索（RAG）
"""
import json
import logging
import math
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

# 提前配置 HuggingFace 端点与缓存目录，避免导入 sentence_transformers 时锁定为默认的 huggingface.co
_default_hf_endpoint = os.getenv("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_ENDPOINT", _default_hf_endpoint)
_hf_cache_dir = Path(__file__).resolve().parents[2] / "data" / "hf_cache"
_hf_cache_dir.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("HF_HOME", str(_hf_cache_dir))
os.environ.setdefault("HF_HUB_CACHE", str(_hf_cache_dir))

from sentence_transformers import SentenceTransformer
import numpy as np

from app.models.novel_analysis_vector import NovelAnalysisVector

logger = logging.getLogger(__name__)


class VectorStoreService:
    """向量存储服务"""

    # 使用轻量级多语言模型（支持中文）
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    VECTOR_DIM = 384  # 模型输出维度
    CACHE_DIR = _hf_cache_dir  # 统一缓存目录，避免重复下载

    # 类级别的模型缓存（所有实例共享）
    _global_model: Optional[SentenceTransformer] = None
    _model_loading = False

    def __init__(self, db: AsyncSession):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db

    @classmethod
    def preload_model(cls):
        """
        预加载embedding模型 (在应用启动时调用)

        优化点: 避免首次使用时加载模型的7秒延迟
        """
        if cls._global_model is None and not cls._model_loading:
            cls._model_loading = True
            logger.info(f"🔄 预加载Embedding模型: {cls.MODEL_NAME}")
            try:
                import time

                start_time = time.time()
                cls._global_model = SentenceTransformer(
                    cls.MODEL_NAME, cache_folder=str(cls.CACHE_DIR)
                )
                load_time = time.time() - start_time
                logger.info(f"✅ Embedding模型预加载成功，耗时: {load_time:.2f}秒")
            except Exception as e:
                logger.error(f"❌ 预加载Embedding模型失败: {e}", exc_info=True)
                cls._model_loading = False
                raise
            finally:
                cls._model_loading = False

    def _get_model(self) -> SentenceTransformer:
        """
        获取或初始化Embedding模型（懒加载）

        Returns:
            SentenceTransformer: 模型实例
        """
        if self._global_model is None:
            logger.info(f"正在加载Embedding模型: {self.MODEL_NAME}")
            try:
                self._global_model = SentenceTransformer(
                    self.MODEL_NAME, cache_folder=str(self.CACHE_DIR)
                )
                logger.info("Embedding模型加载成功")
            except Exception as e:
                logger.error(f"加载Embedding模型失败: {e}", exc_info=True)
                raise
        return self._global_model
    
    def _convert_micro_data_to_text(self, micro_data: Dict[str, Any]) -> str:
        """
        将微观分析JSON转换为可向量化的文本
        
        Args:
            micro_data: 微观分析JSON数据
            
        Returns:
            str: 文本表示
        """
        text_parts = []
        
        # 添加章节主题
        if 'chapter_theme' in micro_data:
            text_parts.append(f"主题: {micro_data['chapter_theme']}")
        
        # 添加详细事件
        if 'detailed_events' in micro_data:
            for event in micro_data['detailed_events']:
                # 时间上下文
                if 'time_context' in event:
                    text_parts.append(f"时间: {event['time_context']}")
                
                # 动作摘要
                if 'action_summary' in event:
                    text_parts.append(f"事件: {event['action_summary']}")
                
                # 涉及的实体
                if 'entities_involved' in event:
                    for entity in event['entities_involved']:
                        entity_type = entity.get('type', '未知')
                        entity_name = entity.get('name', '未知')
                        entity_desc = entity.get('description', '')
                        text_parts.append(f"{entity_type}: {entity_name} - {entity_desc}")
        
        # 合并所有部分
        combined_text = " | ".join(text_parts)
        logger.debug(f"转换文本长度: {len(combined_text)} 字符")
        return combined_text
    
    async def store_micro_analysis_vector(
        self,
        work_id: str,
        chapter_id: str,
        analysis_id: str,
        micro_data: Dict[str, Any],
        chunk_index: int = 0
    ) -> NovelAnalysisVector:
        """
        存储微观分析的向量表示
        
        Args:
            work_id: 作品ID
            chapter_id: 章节ID
            analysis_id: 分析任务ID
            micro_data: 微观分析JSON数据
            chunk_index: 块索引（一章可能分多块）
            
        Returns:
            NovelAnalysisVector: 创建的向量记录
            
        Raises:
            Exception: 存储失败
        """
        try:
            logger.info(f"开始向量化章节 {chapter_id} 的微观分析数据")
            
            # 1. 转换为文本
            content_text = self._convert_micro_data_to_text(micro_data)
            
            # 2. 向量化
            model = self._get_model()
            embedding = model.encode(content_text, normalize_embeddings=True)
            
            # 转换为列表（PostgreSQL pgvector需要）
            embedding_list = embedding.tolist()
            
            logger.info(f"生成向量维度: {len(embedding_list)}")
            
            # 3. 存储到数据库
            from uuid import UUID
            
            # 确保所有ID都是UUID类型
            if isinstance(work_id, str):
                work_id = UUID(work_id)
            if isinstance(chapter_id, str):
                chapter_id = UUID(chapter_id)
            if isinstance(analysis_id, str):
                analysis_id = UUID(analysis_id)
            
            vector_record = NovelAnalysisVector(
                work_id=work_id,
                chapter_id=chapter_id,
                analysis_id=analysis_id,
                embedding=embedding_list,
                content_text=content_text,
                micro_data=micro_data,
                chunk_index=chunk_index
            )
            
            self.db.add(vector_record)
            
            try:
                await self.db.commit()
                await self.db.refresh(vector_record)
                logger.info(f"向量存储成功: vector_id={vector_record.id}")
                return vector_record
            except Exception as commit_error:
                await self.db.rollback()
                # 检查是否是外键约束错误
                error_msg = str(commit_error)
                if "ForeignKeyViolationError" in error_msg or "analysis_id_fkey" in error_msg:
                    logger.warning(f"向量存储失败：主分析记录不可见（可能是事务隔离问题）")
                    logger.warning(f"  analysis_id={analysis_id} 在当前Session中不可见")
                    logger.warning(f"  这不影响分析主流程，向量可以稍后重新生成")
                    raise ValueError(f"Analysis record not visible: {analysis_id}")
                else:
                    logger.error(f"向量存储失败: {commit_error}", exc_info=True)
                    raise
            
        except ValueError as ve:
            # 外键问题，向上传递但标记为非致命
            raise
        except Exception as e:
            logger.error(f"向量化失败: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def retrieve_relevant_analysis(
        self,
        work_id: str,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.3  # P2修复: 统一阈值为0.3（原为0.5）
    ) -> List[Dict[str, Any]]:
        """
        检索与查询相关的微观分析（RAG）

        Args:
            work_id: 作品ID
            query: 查询文本
            top_k: 返回前K个最相关的结果
            similarity_threshold: 相似度阈值（0-1），默认0.3

        Returns:
            List[Dict]: 相关的分析结果列表，每项包含：
                - chapter_id: 章节ID
                - micro_data: 微观分析JSON
                - content_text: 文本内容
                - similarity: 相似度分数
        """
        try:
            logger.info(f"RAG检索: work_id={work_id}, query={query[:50]}...")

            # 1. 向量化查询
            model = self._get_model()
            query_embedding = model.encode(query, normalize_embeddings=True)
            query_embedding_list = query_embedding.tolist()

            # 2. 执行相似度搜索（使用余弦距离）
            # pgvector的<=>操作符计算余弦距离（值越小越相似）
            # 余弦相似度 = 1 - 余弦距离
            stmt = (
                select(
                    NovelAnalysisVector,
                    # 计算余弦相似度
                    (1 - NovelAnalysisVector.embedding.cosine_distance(query_embedding_list)).label('similarity')
                )
                .where(NovelAnalysisVector.work_id == work_id)
                .order_by(NovelAnalysisVector.embedding.cosine_distance(query_embedding_list))
                .limit(top_k)
            )

            result = await self.db.execute(stmt)
            rows = result.all()

            # P2修复: 添加调试日志
            if not rows:
                logger.warning(f"RAG检索: 向量表为空或无匹配数据 (work_id={work_id})")

            # 3. 过滤和格式化结果
            relevant_results = []
            filtered_count = 0
            for vector_record, similarity in rows:
                # 只返回超过阈值的结果
                if similarity >= similarity_threshold:
                    relevant_results.append({
                        'chapter_id': str(vector_record.chapter_id),
                        'micro_data': vector_record.micro_data,
                        'content_text': vector_record.content_text,
                        'similarity': float(similarity),
                        'chunk_index': vector_record.chunk_index
                    })
                else:
                    filtered_count += 1
                    # P2修复: 记录被过滤的低相似度结果
                    logger.debug(f"RAG过滤: similarity={similarity:.3f} < threshold={similarity_threshold}")

            # P2修复: 增强日志
            if filtered_count > 0 and len(relevant_results) == 0:
                logger.warning(
                    f"RAG检索: 所有 {filtered_count} 个结果都被阈值({similarity_threshold})过滤，"
                    f"考虑降低阈值"
                )

            logger.info(f"检索到 {len(relevant_results)} 个相关结果（阈值={similarity_threshold}）")

            # 打印前3个结果的相似度
            for i, result in enumerate(relevant_results[:3]):
                logger.debug(f"结果 {i+1}: 相似度={result['similarity']:.3f}, 章节={result['chapter_id']}")

            return relevant_results

        except Exception as e:
            logger.error(f"RAG检索失败: {e}", exc_info=True)
            return []
    
    async def delete_work_vectors(self, work_id: str) -> int:
        """
        删除作品的所有向量数据
        
        Args:
            work_id: 作品ID
            
        Returns:
            int: 删除的记录数
        """
        try:
            from sqlalchemy import delete as sql_delete
            
            stmt = sql_delete(NovelAnalysisVector).where(
                NovelAnalysisVector.work_id == work_id
            )
            result = await self.db.execute(stmt)
            await self.db.commit()
            
            deleted_count = result.rowcount
            logger.info(f"删除作品 {work_id} 的 {deleted_count} 条向量记录")
            return deleted_count
            
        except Exception as e:
            logger.error(f"删除向量数据失败: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def get_vector_stats(self, work_id: str) -> Dict[str, Any]:
        """
        获取作品的向量数据统计
        
        Args:
            work_id: 作品ID
            
        Returns:
            Dict: 统计信息
        """
        try:
            stmt = select(
                func.count(NovelAnalysisVector.id).label('total_vectors'),
                func.count(func.distinct(NovelAnalysisVector.chapter_id)).label('total_chapters')
            ).where(NovelAnalysisVector.work_id == work_id)
            
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

    # ==================== 知识库向量方法 ====================

    async def add_knowledge_batch(self, knowledge_items: List, cache_service=None) -> List[NovelAnalysisVector]:
        """
        批量添加知识条目到向量库 (优化版本 + 缓存)

        优化点:
        1. 批量生成embedding,比逐个生成快3倍
        2. Redis缓存,避免重复向量化相同内容

        Args:
            knowledge_items: KnowledgeItem模型实例列表
            cache_service: Redis缓存服务(可选)

        Returns:
            List[NovelAnalysisVector]: 向量记录列表
        """
        if not knowledge_items:
            return []

        try:
            logger.info(f"🚀 开始批量向量化 {len(knowledge_items)} 个知识条目")
            import time
            start_time = time.time()

            # 1. 批量生成文本表示
            texts = []
            for item in knowledge_items:
                text_parts = [item.title, item.content]
                if item.tags:
                    text_parts.append(f"标签: {', '.join(item.tags)}")
                texts.append(" | ".join(text_parts))

            # 2. 尝试从缓存获取向量
            cached_embeddings = None
            if cache_service:
                cached_embeddings = await cache_service.get_cached_vectors(texts)

            # 3. 处理缓存结果
            embeddings = []
            texts_to_compute = []
            indices_to_compute = []

            if cached_embeddings:
                # 有部分或全部缓存命中
                for i, cached_emb in enumerate(cached_embeddings):
                    if cached_emb is not None:
                        # 使用缓存的向量
                        embeddings.append(cached_emb)
                    else:
                        # 需要计算的文本
                        embeddings.append(None)  # 占位
                        texts_to_compute.append(texts[i])
                        indices_to_compute.append(i)

                # 批量计算未命中的向量
                if texts_to_compute:
                    logger.info(f"⚡ 需要计算 {len(texts_to_compute)}/{len(texts)} 个向量")
                    model = self._get_model()
                    computed_embeddings = model.encode(texts_to_compute, normalize_embeddings=True, batch_size=len(texts_to_compute))

                    # 填充计算结果
                    for idx, computed_emb in zip(indices_to_compute, computed_embeddings):
                        embeddings[idx] = computed_emb.tolist()

                    # 缓存新计算的向量
                    if cache_service:
                        await cache_service.cache_vectors(texts_to_compute, [emb.tolist() for emb in computed_embeddings])
                else:
                    logger.info("⚡ 100%缓存命中,跳过所有向量计算")
            else:
                # 完全未命中,批量计算所有向量
                logger.info(f"🔄 缓存未命中,计算全部 {len(texts)} 个向量")
                model = self._get_model()
                embeddings_array = model.encode(texts, normalize_embeddings=True, batch_size=len(texts))
                embeddings = [emb.tolist() for emb in embeddings_array]

                # 缓存所有向量
                if cache_service:
                    await cache_service.cache_vectors(texts, embeddings)

            # 4. 批量创建向量记录
            from uuid import UUID
            vector_records = []

            for i, (item, embedding) in enumerate(zip(knowledge_items, embeddings)):
                user_id = item.user_id if isinstance(item.user_id, UUID) else UUID(str(item.user_id))
                item_id = item.id if isinstance(item.id, UUID) else UUID(str(item.id))

                vector_record = NovelAnalysisVector(
                    user_id=user_id,
                    source_type="knowledge",
                    source_id=item_id,
                    embedding=embedding,  # 已经是list了
                    content_text=texts[i],
                    micro_data=None,
                    chunk_index=0
                )
                vector_records.append(vector_record)
                self.db.add(vector_record)

            # 5. 批量提交
            await self.db.commit()

            # 6. 批量刷新
            for record in vector_records:
                await self.db.refresh(record)

            elapsed = time.time() - start_time
            logger.info(f"✅ 批量向量化完成: {len(vector_records)}个条目, 耗时: {elapsed:.2f}秒")

            return vector_records

        except Exception as e:
            logger.error(f"❌ 批量向量化失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def add_knowledge(self, knowledge_item) -> NovelAnalysisVector:
        """
        添加知识条目到向量库

        Args:
            knowledge_item: KnowledgeItem模型实例

        Returns:
            NovelAnalysisVector: 向量记录
        """
        try:
            logger.info(f"开始向量化知识条目: {knowledge_item.id}")

            from uuid import UUID

            # 生成基础文本片段 (标题 + 内容 + 标签)
            tag_text = f"标签: {', '.join(knowledge_item.tags)}" if knowledge_item.tags else ""
            base_content = knowledge_item.content or ""

            # 简单分块，避免超长文本只生成一个向量
            chunks, chunk_meta = self._chunk_text(base_content)
            if not chunks:
                chunks = [""]

            model = self._get_model()

            user_id = knowledge_item.user_id if isinstance(knowledge_item.user_id, UUID) else UUID(str(knowledge_item.user_id))
            item_id = knowledge_item.id if isinstance(knowledge_item.id, UUID) else UUID(str(knowledge_item.id))

            # 批量编码，降低单次上传的时延
            chunk_texts: List[str] = []
            for chunk in chunks:
                chunk_text_parts = [knowledge_item.title, chunk]
                if tag_text:
                    chunk_text_parts.append(tag_text)
                chunk_texts.append(" | ".join([part for part in chunk_text_parts if part]))

            embeddings = model.encode(
                chunk_texts,
                normalize_embeddings=True,
                batch_size=self._get_encode_batch_size(len(chunk_texts)),
                show_progress_bar=False
            )

            vector_records = []
            for idx, (chunk_text, embedding) in enumerate(zip(chunk_texts, embeddings)):
                vector_record = NovelAnalysisVector(
                    user_id=user_id,
                    source_type="knowledge",
                    source_id=item_id,
                    embedding=embedding.tolist(),
                    content_text=chunk_text,
                    micro_data=None,
                    chunk_index=idx
                )
                self.db.add(vector_record)
                vector_records.append(vector_record)

            await self.db.commit()
            # 返回首个记录以保持向后兼容
            first_record = vector_records[0]
            await self.db.refresh(first_record)

            # 将分块信息写入元数据，避免静默截断
            try:
                meta = knowledge_item.extra_data or {}
                meta.update({
                    "vector_chunk_count": len(chunk_texts),
                    "vector_chunk_size": chunk_meta["chunk_size"],
                    "vector_chunk_overlap": chunk_meta["overlap"]
                })
                if chunk_meta.get("truncated"):
                    meta["vectorization_warning"] = "文本过长，已按上限截断部分内容，请拆分或减少文件大小"
                elif chunk_meta.get("scaled"):
                    meta["vectorization_warning"] = "文本较长，已动态增大分块以控制向量数量，可能影响检索精度"
                knowledge_item.extra_data = meta
                await self.db.commit()
            except Exception as meta_err:
                logger.warning(f"写入分块元数据失败: {meta_err}")

            logger.info(f"知识库向量存储成功: item_id={item_id}, chunks={len(vector_records)}")
            return first_record

        except Exception as e:
            logger.error(f"知识库向量化失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    def _get_encode_batch_size(self, total_chunks: int) -> int:
        """
        根据分块数量选择合适的批大小，避免一次性占用过多显存/CPU
        """
        if total_chunks >= 128:
            return 8
        if total_chunks >= 64:
            return 12
        return 16

    def _chunk_text(
        self,
        text: str,
        chunk_size: int = 800,
        overlap: int = 200,
        max_chunks: int = 200
    ) -> Tuple[List[str], Dict[str, Any]]:
        """
        按字符长度切分长文本，带简单重叠，并对块数量做上限防护，
        同时在超过上限时动态放宽块大小，避免无声截断。
        """
        if not text:
            return [], {"chunk_size": chunk_size, "overlap": overlap, "truncated": False, "scaled": False}

        cleaned = text.replace("\r", "")
        if len(cleaned) <= chunk_size:
            return [cleaned], {"chunk_size": chunk_size, "overlap": overlap, "truncated": False, "scaled": False}

        # 预估当前分块数量
        def estimate_chunks(size: int, ov: int) -> int:
            step = max(1, size - ov)
            return math.ceil(max(len(cleaned) - size, 0) / step) + 1

        used_chunk_size = chunk_size
        used_overlap = overlap
        scaled = False

        approx = estimate_chunks(used_chunk_size, used_overlap)
        if approx > max_chunks:
            # 动态放大分块尺寸，目标控制在上限附近，避免截断
            used_chunk_size = max(chunk_size, math.ceil(len(cleaned) / max_chunks))
            used_overlap = min(overlap, used_chunk_size // 4)
            scaled = True

        chunks: List[str] = []
        start = 0
        length = len(cleaned)

        while start < length and len(chunks) < max_chunks:
            end = min(length, start + used_chunk_size)
            chunk = cleaned[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end == length:
                break

            start = max(0, end - used_overlap)

        truncated = start < length and len(chunks) >= max_chunks
        if truncated:
            logger.warning(
                "知识向量分块达到上限，后续内容未向量化",
                extra={
                    "text_length": length,
                    "max_chunks": max_chunks,
                    "chunk_size": used_chunk_size,
                    "overlap": used_overlap
                }
            )

        meta = {
            "chunk_size": used_chunk_size,
            "overlap": used_overlap,
            "truncated": truncated,
            "scaled": scaled
        }

        return chunks, meta

    async def search_knowledge(
        self,
        query: str,
        user_id: str,
        top_k: int = 10,
        similarity_threshold: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        搜索知识库

        Args:
            query: 查询文本
            user_id: 用户ID
            top_k: 返回前K个最相关的结果
            similarity_threshold: 相似度阈值（0-1）

        Returns:
            List[Dict]: 相关的知识条目，每项包含：
                - source_id: 知识条目ID
                - similarity: 相似度分数
                - text: 文本内容
        """
        try:
            logger.info(f"知识库RAG检索: user_id={user_id}, query={query[:50]}...")

            # 1. 向量化查询
            model = self._get_model()
            query_embedding = model.encode(query, normalize_embeddings=True)
            query_embedding_list = query_embedding.tolist()

            # 2. 执行相似度搜索
            from uuid import UUID
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id

            stmt = (
                select(
                    NovelAnalysisVector,
                    (1 - NovelAnalysisVector.embedding.cosine_distance(query_embedding_list)).label('similarity')
                )
                .where(NovelAnalysisVector.user_id == user_uuid)
                .where(NovelAnalysisVector.source_type == "knowledge")
                .order_by(NovelAnalysisVector.embedding.cosine_distance(query_embedding_list))
                .limit(top_k)
            )

            result = await self.db.execute(stmt)
            rows = result.all()

            # 3. 过滤和格式化结果
            relevant_results = []
            for vector_record, similarity in rows:
                if similarity >= similarity_threshold:
                    relevant_results.append({
                        'source_id': str(vector_record.source_id),
                        'similarity': float(similarity),
                        'text': vector_record.content_text
                    })

            logger.info(f"检索到 {len(relevant_results)} 个相关知识条目（阈值={similarity_threshold}）")

            return relevant_results

        except Exception as e:
            logger.error(f"知识库RAG检索失败: {e}", exc_info=True)
            return []

    async def update_knowledge_vector(self, knowledge_item) -> Optional[NovelAnalysisVector]:
        """
        更新知识条目的向量

        Args:
            knowledge_item: KnowledgeItem模型实例

        Returns:
            NovelAnalysisVector: 更新后的向量记录
        """
        try:
            from uuid import UUID
            from sqlalchemy import delete as sql_delete

            item_id = knowledge_item.id if isinstance(knowledge_item.id, UUID) else UUID(str(knowledge_item.id))

            # 1. 删除旧向量
            stmt = sql_delete(NovelAnalysisVector).where(
                NovelAnalysisVector.source_type == "knowledge",
                NovelAnalysisVector.source_id == item_id
            )
            await self.db.execute(stmt)

            # 2. 创建新向量
            vector_record = await self.add_knowledge(knowledge_item)

            logger.info(f"知识库向量更新成功: item_id={item_id}")
            return vector_record

        except Exception as e:
            logger.error(f"知识库向量更新失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def delete_knowledge_vector(self, item_id: str) -> int:
        """
        删除知识条目的向量

        Args:
            item_id: 知识条目ID

        Returns:
            int: 删除的记录数
        """
        try:
            from sqlalchemy import delete as sql_delete
            from uuid import UUID

            item_uuid = UUID(item_id) if isinstance(item_id, str) else item_id

            stmt = sql_delete(NovelAnalysisVector).where(
                NovelAnalysisVector.source_type == "knowledge",
                NovelAnalysisVector.source_id == item_uuid
            )
            result = await self.db.execute(stmt)
            await self.db.commit()

            deleted_count = result.rowcount
            logger.info(f"删除知识条目 {item_id} 的向量记录: {deleted_count} 条")
            return deleted_count

        except Exception as e:
            logger.error(f"删除知识库向量失败: {e}", exc_info=True)
            await self.db.rollback()
            raise
