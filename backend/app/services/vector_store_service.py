"""
向量存储服务
负责微观分析结果的向量化存储和检索（RAG）
"""
import json
import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sentence_transformers import SentenceTransformer
import numpy as np

from app.models.novel_analysis_vector import NovelAnalysisVector

logger = logging.getLogger(__name__)


class VectorStoreService:
    """向量存储服务"""
    
    # 使用轻量级多语言模型（支持中文）
    MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
    VECTOR_DIM = 384  # 模型输出维度
    
    def __init__(self, db: AsyncSession):
        """
        初始化服务
        
        Args:
            db: 数据库会话
        """
        self.db = db
        self._model = None
    
    def _get_model(self) -> SentenceTransformer:
        """
        获取或初始化Embedding模型（懒加载）
        
        Returns:
            SentenceTransformer: 模型实例
        """
        if self._model is None:
            logger.info(f"正在加载Embedding模型: {self.MODEL_NAME}")
            try:
                self._model = SentenceTransformer(self.MODEL_NAME)
                logger.info("Embedding模型加载成功")
            except Exception as e:
                logger.error(f"加载Embedding模型失败: {e}", exc_info=True)
                raise
        return self._model
    
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
            await self.db.commit()
            await self.db.refresh(vector_record)
            
            logger.info(f"向量存储成功: vector_id={vector_record.id}")
            return vector_record
            
        except Exception as e:
            logger.error(f"向量存储失败: {e}", exc_info=True)
            await self.db.rollback()
            raise
    
    async def retrieve_relevant_analysis(
        self,
        work_id: str,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        检索与查询相关的微观分析（RAG）
        
        Args:
            work_id: 作品ID
            query: 查询文本
            top_k: 返回前K个最相关的结果
            similarity_threshold: 相似度阈值（0-1）
            
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
            
            # 3. 过滤和格式化结果
            relevant_results = []
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
