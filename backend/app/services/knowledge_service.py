"""
知识库服务
负责知识条目的CRUD操作和语义搜索
"""
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_, bindparam, text
from uuid import UUID

from app.models.knowledge_item import KnowledgeItem, KnowledgeCategory
from app.schemas.knowledge import KnowledgeItemCreate, KnowledgeItemUpdate
from app.services.vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)


class KnowledgeService:
    """知识库服务"""

    def __init__(self, db: AsyncSession):
        """
        初始化服务

        Args:
            db: 数据库会话
        """
        self.db = db
        self.vector_service = VectorStoreService(db)

    async def create_item(
        self,
        user_id: str,
        data: KnowledgeItemCreate,
        skip_vectorization: bool = False
    ) -> KnowledgeItem:
        """
        创建知识条目

        Args:
            user_id: 用户ID
            data: 创建数据
            skip_vectorization: 是否跳过向量化 (用于批量向量化优化)

        Returns:
            KnowledgeItem: 创建的知识条目
        """
        try:
            logger.info(f"创建知识条目: user_id={user_id}, title={data.title}")

            # 1. 创建条目
            item = KnowledgeItem(
                user_id=UUID(user_id) if isinstance(user_id, str) else user_id,
                **data.model_dump()
            )
            self.db.add(item)
            await self.db.flush()

            # 2. 生成并存储向量 (可选跳过用于批量优化)
            if not skip_vectorization:
                try:
                    await self.vector_service.add_knowledge(item)
                    logger.info(f"知识条目向量生成成功: item_id={item.id}")
                except Exception as ve:
                    logger.warning(f"向量生成失败，但条目已创建: {ve}")
                    # 向量生成失败不影响条目创建

            await self.db.commit()
            await self.db.refresh(item)

            logger.info(f"知识条目创建成功: item_id={item.id}")
            return item

        except Exception as e:
            logger.error(f"创建知识条目失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def get_item(self, item_id: str, user_id: str, *, increment_view: bool = False) -> Optional[KnowledgeItem]:
        """
        获取单个知识条目

        Args:
            item_id: 条目ID
            user_id: 用户ID（权限验证）

        Returns:
            KnowledgeItem: 知识条目
        """
        try:
            item_uuid = UUID(item_id) if isinstance(item_id, str) else item_id
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id

            stmt = select(KnowledgeItem).where(
                and_(
                    KnowledgeItem.id == item_uuid,
                    KnowledgeItem.user_id == user_uuid
                )
            )

            result = await self.db.execute(stmt)
            item = result.scalar_one_or_none()

            if item and increment_view:
                # 仅在明确需要统计时才增加查看次数，避免后台内部调用产生噪声
                item.view_count += 1
                from datetime import datetime, timezone
                item.last_accessed_at = datetime.now(timezone.utc)
                await self.db.commit()
                await self.db.refresh(item)  # 刷新以确保所有字段加载

            return item

        except Exception as e:
            logger.error(f"获取知识条目失败: {e}", exc_info=True)
            return None

    async def get_items(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        category: Optional[KnowledgeCategory] = None,
        tags: Optional[List[str]] = None,
        work_id: Optional[str] = None,
        search: Optional[str] = None
    ) -> tuple[List[KnowledgeItem], int]:
        """
        获取知识条目列表（支持过滤/分页/排序）

        Args:
            user_id: 用户ID
            skip: 跳过数量
            limit: 每页大小
            category: 分类过滤（可选）
            tags: 标签过滤（可选）
            work_id: 作品ID过滤（可选）
            search: 搜索关键词（可选）

        Returns:
            tuple: (条目列表, 总数)
        """
        try:
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id

            # 构建查询
            query = select(KnowledgeItem).where(KnowledgeItem.user_id == user_uuid)
            count_query = select(func.count(KnowledgeItem.id)).where(KnowledgeItem.user_id == user_uuid)

            # 分类过滤
            if category:
                query = query.where(KnowledgeItem.category == category)
                count_query = count_query.where(KnowledgeItem.category == category)

            # 标签过滤（支持模糊匹配任意标签：输入任意一段文字，只要有标签包含即可命中）
            if tags:
                tag_conditions = []
                for idx, tag in enumerate(tags):
                    if not tag:
                        continue
                    pattern = f"%{tag}%"
                    clause = text(
                        f"EXISTS (SELECT 1 FROM unnest(knowledge_items.tags) AS t(tag) WHERE t ILIKE :tag_pattern_{idx})"
                    ).bindparams(bindparam(f"tag_pattern_{idx}", pattern))
                    tag_conditions.append(clause)
                if tag_conditions:
                    tag_filter = or_(*tag_conditions)
                    query = query.where(tag_filter)
                    count_query = count_query.where(tag_filter)

            # 作品过滤
            if work_id:
                work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id
                query = query.where(KnowledgeItem.work_id == work_uuid)
                count_query = count_query.where(KnowledgeItem.work_id == work_uuid)

            # 关键词搜索（标题或内容）
            if search:
                search_filter = or_(
                    KnowledgeItem.title.ilike(f"%{search}%"),
                    KnowledgeItem.content.ilike(f"%{search}%")
                )
                query = query.where(search_filter)
                count_query = count_query.where(search_filter)

            # 获取总数
            total_result = await self.db.execute(count_query)
            total = total_result.scalar()

            # 获取列表（按更新时间倒序）
            query = query.offset(skip).limit(limit).order_by(KnowledgeItem.updated_at.desc())
            result = await self.db.execute(query)
            items = result.scalars().all()

            logger.info(f"查询知识条目: user_id={user_id}, total={total}, returned={len(items)}")
            return list(items), total

        except Exception as e:
            logger.error(f"获取知识条目列表失败: {e}", exc_info=True)
            return [], 0

    async def update_item(
        self,
        item_id: str,
        user_id: str,
        data: KnowledgeItemUpdate
    ) -> Optional[KnowledgeItem]:
        """
        更新知识条目

        Args:
            item_id: 条目ID
            user_id: 用户ID（权限验证）
            data: 更新数据

        Returns:
            KnowledgeItem: 更新后的知识条目
        """
        try:
            # 获取条目
            item = await self.get_item(item_id, user_id)
            if not item:
                logger.warning(f"知识条目不存在或无权限: item_id={item_id}, user_id={user_id}")
                return None

            # 更新字段
            update_data = data.model_dump(exclude_unset=True)
            content_changed = False

            for field, value in update_data.items():
                if field in ['title', 'content', 'tags']:
                    content_changed = True
                setattr(item, field, value)

            await self.db.flush()

            # 如果内容改变，更新向量
            if content_changed:
                try:
                    await self.vector_service.update_knowledge_vector(item)
                    logger.info(f"知识条目向量更新成功: item_id={item_id}")
                except Exception as ve:
                    logger.warning(f"向量更新失败: {ve}")

            await self.db.commit()
            await self.db.refresh(item)

            logger.info(f"知识条目更新成功: item_id={item_id}")
            return item

        except Exception as e:
            logger.error(f"更新知识条目失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def delete_item(self, item_id: str, user_id: str) -> bool:
        """
        删除知识条目

        Args:
            item_id: 条目ID
            user_id: 用户ID（权限验证）

        Returns:
            bool: 是否删除成功
        """
        try:
            # 获取条目
            item = await self.get_item(item_id, user_id)
            if not item:
                logger.warning(f"知识条目不存在或无权限: item_id={item_id}, user_id={user_id}")
                return False

            # 删除向量
            try:
                await self.vector_service.delete_knowledge_vector(item_id)
                logger.info(f"知识条目向量删除成功: item_id={item_id}")
            except Exception as ve:
                logger.warning(f"向量删除失败: {ve}")

            # 删除条目
            await self.db.delete(item)
            await self.db.commit()

            logger.info(f"知识条目删除成功: item_id={item_id}")
            return True

        except Exception as e:
            logger.error(f"删除知识条目失败: {e}", exc_info=True)
            await self.db.rollback()
            raise

    async def search_by_semantic(
        self,
        user_id: str,
        query: str,
        category: Optional[KnowledgeCategory] = None,
        tags: Optional[List[str]] = None,
        work_id: Optional[str] = None,
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        语义搜索知识库

        Args:
            user_id: 用户ID
            query: 搜索查询
            category: 分类过滤（可选）
            tags: 标签过滤（可选）
            work_id: 作品ID过滤（可选）
            top_k: 返回结果数量

        Returns:
            List[Dict]: 搜索结果列表，每项包含：
                - item: KnowledgeItem实例
                - relevance_score: 相关性评分
                - highlight: 高亮片段
        """
        try:
            logger.info(f"语义搜索知识库: user_id={user_id}, query={query}")

            # 1. 向量检索
            vector_results = await self.vector_service.search_knowledge(
                query=query,
                user_id=user_id,
                top_k=top_k * 4,  # 多取一些，过滤后再截断，防止重复块占满
                similarity_threshold=0.3
            )

            if not vector_results:
                logger.info("向量检索未找到结果")
                return []

            # 2. 以条目去重保留最优块，避免同一条目多块占满结果
            best_hits: Dict[str, Dict[str, Any]] = {}
            for vector_result in vector_results:
                source_id = vector_result['source_id']
                hit = best_hits.get(source_id)
                if not hit or vector_result['similarity'] > hit['similarity']:
                    best_hits[source_id] = {
                        'similarity': vector_result['similarity'],
                        'text': vector_result.get('text', '')
                    }

            # 按相似度排序，逐个加载条目并应用过滤
            sorted_hits = sorted(
                best_hits.items(),
                key=lambda item: item[1]['similarity'],
                reverse=True
            )

            results = []
            for source_id, hit in sorted_hits:
                if len(results) >= top_k:
                    break

                item = await self.get_item(source_id, user_id)
                if not item:
                    continue

                # 分类过滤
                if category and item.category != category:
                    continue

                # 标签过滤
                if tags and not any(tag in item.tags for tag in tags):
                    continue

                # 作品过滤
                if work_id:
                    work_uuid = UUID(work_id) if isinstance(work_id, str) else work_id
                    if item.work_id != work_uuid:
                        continue

                highlight_source = hit['text'] or item.content
                highlight = self._extract_highlight(highlight_source, query)

                results.append({
                    'item': item,
                    'relevance_score': hit['similarity'],
                    'highlight': highlight
                })

            logger.info(f"语义搜索完成: 返回{len(results)}个结果")
            return results

        except Exception as e:
            logger.error(f"语义搜索失败: {e}", exc_info=True)
            return []

    async def increment_reference_count(self, item_id: str, user_id: str) -> bool:
        """
        增加引用次数

        Args:
            item_id: 条目ID
            user_id: 用户ID

        Returns:
            bool: 是否成功
        """
        try:
            item = await self.get_item(item_id, user_id)
            if not item:
                return False

            item.reference_count += 1
            await self.db.commit()

            logger.info(f"引用次数增加: item_id={item_id}, count={item.reference_count}")
            return True

        except Exception as e:
            logger.error(f"增加引用次数失败: {e}", exc_info=True)
            return False

    def _extract_highlight(self, content: str, query: str, context_len: int = 100) -> str:
        """
        提取相关片段（简单实现）

        Args:
            content: 完整内容
            query: 查询关键词
            context_len: 上下文长度

        Returns:
            str: 高亮片段
        """
        # 简单实现：查找关键词首次出现的位置，提取前后文
        query_lower = query.lower()
        content_lower = content.lower()

        pos = content_lower.find(query_lower)
        if pos == -1:
            # 未找到，返回开头
            return content[:context_len] + "..."

        # 提取前后文
        start = max(0, pos - context_len // 2)
        end = min(len(content), pos + len(query) + context_len // 2)

        highlight = content[start:end]
        if start > 0:
            highlight = "..." + highlight
        if end < len(content):
            highlight = highlight + "..."

        return highlight
