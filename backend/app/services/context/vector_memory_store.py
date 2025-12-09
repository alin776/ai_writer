"""
向量记忆存储 - 基于ChromaDB实现语义检索

提供长期记忆的向量化存储和检索能力，让Agent能够跨会话记忆重要信息。

核心功能：
- 向量化存储：使用sentence-transformers本地模型生成embeddings
- 语义检索：基于余弦相似度检索相关记忆
- 元数据过滤：支持按用户、会话、时间等条件过滤
- 持久化存储：本地存储，重启不丢失
- 隔离层级：支持 USER/WORK/SESSION 三级隔离

设计原则：
- 使用本地模型（sentence-transformers）避免API调用成本
- 简单可靠的降级策略
- 完整的日志和错误处理
"""

import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict, Optional, Any
import logging
import time
import uuid

from app.services.context.models import IsolationLevel, build_isolation_key

logger = logging.getLogger(__name__)


class VectorMemoryStore:
    """向量记忆存储 - 使用ChromaDB + sentence-transformers"""

    def __init__(
        self,
        persist_directory: str = "./data/chroma_db",
        embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
        collection_name: str = "user_memories"
    ):
        """
        初始化向量存储

        Args:
            persist_directory: 持久化目录
            embedding_model: sentence-transformers模型名称
                默认: paraphrase-multilingual-MiniLM-L12-v2 (中英文支持)
            collection_name: ChromaDB集合名称
        """
        self.persist_directory = persist_directory
        self.embedding_model = embedding_model
        self.collection_name = collection_name

        try:
            # 初始化ChromaDB客户端（持久化模式）
            self.client = chromadb.PersistentClient(path=persist_directory)

            # 初始化本地Embedding函数（sentence-transformers）
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=embedding_model
            )

            # 创建/获取collection
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
            )

            logger.info(
                f"✅ VectorMemoryStore初始化成功 | "
                f"目录={persist_directory} | "
                f"模型={embedding_model} | "
                f"集合={collection_name}"
            )

        except Exception as e:
            logger.error(f"❌ VectorMemoryStore初始化失败: {e}")
            raise

    async def add_memory(
        self,
        content: str,
        user_id: str,
        work_id: Optional[str] = None,
        session_id: Optional[str] = None,
        memory_type: str = "general",
        importance: float = 0.5,
        isolation_level: IsolationLevel = IsolationLevel.WORK,  # ✅ 新增：隔离级别
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        添加记忆到向量库

        Args:
            content: 记忆内容（文本）
            user_id: 用户ID
            work_id: 作品ID（WORK 级别时使用）
            session_id: 会话ID（SESSION 级别时使用）
            memory_type: 记忆类型（如：character, plot, setting等）
            importance: 重要度（0.0-1.0）
            isolation_level: 隔离级别（默认 WORK 级）
            metadata: 额外的元数据

        Returns:
            memory_id: 记忆的唯一ID
        """
        try:
            # 生成唯一ID
            memory_id = f"{user_id}_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}"

            # ✅ 构建隔离键
            isolation_key = build_isolation_key(
                user_id=user_id,
                level=isolation_level,
                work_id=work_id,
                session_id=session_id
            )

            # 构建元数据
            mem_metadata = {
                "user_id": user_id,
                "work_id": work_id or "",
                "session_id": session_id or "",
                "isolation_key": isolation_key,  # ✅ 新增：隔离键
                "isolation_level": isolation_level.value,  # ✅ 新增：隔离级别
                "memory_type": memory_type,
                "importance": importance,
                "timestamp": time.time(),
                "content_length": len(content)
            }

            # 合并自定义元数据
            if metadata:
                mem_metadata.update(metadata)

            # 添加到ChromaDB
            self.collection.add(
                documents=[content],
                metadatas=[mem_metadata],
                ids=[memory_id]
            )

            logger.debug(
                f"✅ 添加记忆 | ID={memory_id} | "
                f"用户={user_id} | 隔离={isolation_key} | "
                f"类型={memory_type} | 重要度={importance:.2f}"
            )

            return memory_id

        except Exception as e:
            logger.error(f"❌ 添加记忆失败: {e}")
            raise

    async def search_memories(
        self,
        query: str,
        user_id: str,
        work_id: Optional[str] = None,
        session_id: Optional[str] = None,
        top_k: int = 5,
        min_similarity: float = 0.6,
        memory_type: Optional[str] = None,
        include_user_level: bool = True,  # ✅ 新增：是否包含用户级记忆
        isolation_level: IsolationLevel = IsolationLevel.WORK  # ✅ 新增：主要隔离级别
    ) -> List[Dict[str, Any]]:
        """
        语义检索相关记忆（支持多级隔离）

        Args:
            query: 查询文本
            user_id: 用户ID（必须）
            work_id: 作品ID（WORK 级别时使用）
            session_id: 会话ID（SESSION 级别时使用）
            top_k: 返回Top K结果
            min_similarity: 最低相似度阈值（0.0-1.0）
            memory_type: 记忆类型过滤（可选）
            include_user_level: 是否包含用户级记忆（默认 True）
            isolation_level: 主要隔离级别（默认 WORK）

        Returns:
            记忆列表，按相关度排序
        """
        try:
            # ✅ 构建多级隔离键查询
            isolation_keys = []

            # 主要级别的隔离键
            primary_key = build_isolation_key(
                user_id=user_id,
                level=isolation_level,
                work_id=work_id,
                session_id=session_id
            )
            isolation_keys.append(primary_key)

            # 可选：包含用户级记忆（如偏好、风格）
            if include_user_level and isolation_level != IsolationLevel.USER:
                user_key = build_isolation_key(user_id=user_id, level=IsolationLevel.USER)
                isolation_keys.append(user_key)

            # ✅ 构建 ChromaDB 查询条件
            # 使用 $or 匹配多个隔离键
            if len(isolation_keys) == 1:
                where_filter = {"isolation_key": isolation_keys[0]}
            else:
                where_filter = {"$or": [{"isolation_key": k} for k in isolation_keys]}

            # 添加记忆类型过滤
            if memory_type:
                where_filter = {"$and": [where_filter, {"memory_type": memory_type}]}

            # 执行向量检索
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where_filter
            )

            # 格式化结果
            memories = []
            if results["ids"] and len(results["ids"][0]) > 0:
                for i in range(len(results["ids"][0])):
                    distance = results["distances"][0][i]
                    similarity = 1.0 - distance

                    if similarity < min_similarity:
                        continue

                    memories.append({
                        "id": results["ids"][0][i],
                        "content": results["documents"][0][i],
                        "similarity": round(similarity, 4),
                        "metadata": results["metadatas"][0][i]
                    })

            logger.info(
                f"🔍 检索记忆 | 查询='{query[:30]}...' | "
                f"隔离键={isolation_keys} | "
                f"找到={len(memories)}条"
            )

            return memories

        except Exception as e:
            logger.error(f"❌ 记忆检索失败: {e}")
            return []

    async def delete_memory(self, memory_id: str) -> bool:
        """
        删除单条记忆

        Args:
            memory_id: 记忆ID

        Returns:
            是否成功
        """
        try:
            self.collection.delete(ids=[memory_id])
            logger.debug(f"🗑️ 删除记忆 | ID={memory_id}")
            return True
        except Exception as e:
            logger.error(f"❌ 删除记忆失败: {e}")
            return False

    async def delete_memories_by_user(
        self,
        user_id: str,
        session_id: Optional[str] = None
    ) -> int:
        """
        删除用户的记忆（批量）

        Args:
            user_id: 用户ID
            session_id: 会话ID（可选，如指定则只删除该会话的记忆）

        Returns:
            删除的记忆数量
        """
        try:
            # 构建过滤条件（支持多条件）
            conditions = [{"user_id": user_id}]
            if session_id:
                conditions.append({"session_id": session_id})

            # 根据条件数量构建查询
            if len(conditions) == 1:
                where_filter = conditions[0]
            else:
                where_filter = {"$and": conditions}

            # 查询符合条件的记忆
            results = self.collection.get(where=where_filter)

            if results["ids"]:
                # 批量删除
                self.collection.delete(ids=results["ids"])
                count = len(results["ids"])
                logger.info(
                    f"🗑️ 删除用户记忆 | 用户={user_id} | "
                    f"会话={session_id or 'ALL'} | 数量={count}"
                )
                return count
            else:
                logger.debug(f"未找到符合条件的记忆 | 用户={user_id}")
                return 0

        except Exception as e:
            logger.error(f"❌ 批量删除记忆失败: {e}")
            return 0

    async def cleanup_old_memories(
        self,
        user_id: str,
        max_age_days: int = 30,
        keep_important: bool = True,
        importance_threshold: float = 0.7
    ) -> int:
        """
        清理过期的记忆

        Args:
            user_id: 用户ID
            max_age_days: 最大保留天数
            keep_important: 是否保留重要记忆
            importance_threshold: 重要度阈值（keep_important=True时有效）

        Returns:
            清理的记忆数量
        """
        try:
            # 获取用户所有记忆
            results = self.collection.get(where={"user_id": user_id})

            if not results["ids"]:
                return 0

            # 计算时间阈值
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 3600
            threshold_timestamp = current_time - max_age_seconds

            # 筛选需要删除的记忆
            to_delete = []
            for i, memory_id in enumerate(results["ids"]):
                metadata = results["metadatas"][i]
                timestamp = metadata.get("timestamp", 0)
                importance = metadata.get("importance", 0.5)

                # 判断是否过期
                is_old = timestamp < threshold_timestamp
                is_important = importance >= importance_threshold

                # 过期且不重要的记忆需要删除
                if is_old and not (keep_important and is_important):
                    to_delete.append(memory_id)

            # 批量删除
            if to_delete:
                self.collection.delete(ids=to_delete)
                logger.info(
                    f"🧹 清理过期记忆 | 用户={user_id} | "
                    f"保留天数={max_age_days} | 清理数量={len(to_delete)}"
                )

            return len(to_delete)

        except Exception as e:
            logger.error(f"❌ 清理记忆失败: {e}")
            return 0

    async def get_memory_by_id(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        根据ID获取单条记忆

        Args:
            memory_id: 记忆ID

        Returns:
            记忆内容（如果存在）
        """
        try:
            results = self.collection.get(ids=[memory_id])

            if results["ids"]:
                return {
                    "id": results["ids"][0],
                    "content": results["documents"][0],
                    "metadata": results["metadatas"][0]
                }
            return None

        except Exception as e:
            logger.error(f"❌ 获取记忆失败: {e}")
            return None

    def get_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取统计信息

        Args:
            user_id: 用户ID（可选，如指定则返回该用户的统计）

        Returns:
            统计信息字典
        """
        try:
            # 全局统计
            total_count = self.collection.count()

            stats = {
                "total_memories": total_count,
                "embedding_model": self.embedding_model,
                "persist_directory": self.persist_directory,
                "collection_name": self.collection_name
            }

            # 用户统计
            if user_id:
                results = self.collection.get(where={"user_id": user_id})
                user_count = len(results["ids"]) if results["ids"] else 0
                stats["user_memories"] = user_count

            return stats

        except Exception as e:
            logger.error(f"❌ 获取统计失败: {e}")
            return {}

    def reset_collection(self) -> bool:
        """
        重置集合（删除所有数据）- 谨慎使用！

        Returns:
            是否成功
        """
        try:
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_function,
                metadata={"hnsw:space": "cosine"}
            )
            logger.warning(f"⚠️ 重置集合 | 集合={self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"❌ 重置集合失败: {e}")
            return False

    async def migrate_legacy_data(self) -> int:
        """
        迁移旧数据：为没有 isolation_key 的记忆添加隔离键

        旧数据迁移策略：
        - 有 work_id 的 → user:{user_id}:work:{work_id}
        - 无 work_id 的 → user:{user_id}:work:_legacy_

        Returns:
            迁移的记忆数量
        """
        try:
            # 查找没有 isolation_key 的记忆
            # ChromaDB 不支持 "字段不存在" 查询，所以获取全部数据检查
            all_results = self.collection.get()

            if not all_results["ids"]:
                logger.info("📦 无需迁移：没有记忆数据")
                return 0

            migrated_count = 0

            for i, memory_id in enumerate(all_results["ids"]):
                metadata = all_results["metadatas"][i]

                # 检查是否已有 isolation_key
                if "isolation_key" in metadata and metadata["isolation_key"]:
                    continue

                # 构建隔离键
                user_id = metadata.get("user_id", "unknown")
                work_id = metadata.get("work_id", "")

                if work_id and work_id != "":
                    isolation_key = f"user:{user_id}:work:{work_id}"
                else:
                    isolation_key = f"user:{user_id}:work:_legacy_"

                # 更新元数据
                metadata["isolation_key"] = isolation_key
                metadata["isolation_level"] = IsolationLevel.WORK.value

                # ChromaDB 的 update 方法
                self.collection.update(
                    ids=[memory_id],
                    metadatas=[metadata]
                )
                migrated_count += 1

            logger.info(f"📦 数据迁移完成 | 迁移={migrated_count}条记忆")
            return migrated_count

        except Exception as e:
            logger.error(f"❌ 数据迁移失败: {e}")
            return 0

    def close(self):
        """
        关闭ChromaDB连接

        用于释放资源，特别是在测试后清理时
        """
        try:
            # ChromaDB PersistentClient没有显式close方法
            # 但可以通过删除引用让Python GC处理
            self.collection = None
            self.client = None
            logger.debug(f"关闭向量存储连接 | 集合={self.collection_name}")
        except Exception as e:
            logger.error(f"关闭连接失败: {e}")


# 全局单例
_global_vector_store: Optional[VectorMemoryStore] = None


def get_vector_memory_store(
    persist_directory: str = "./data/chroma_db",
    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2",
    collection_name: str = "user_memories"
) -> VectorMemoryStore:
    """
    获取全局向量存储实例（单例模式）

    Args:
        persist_directory: 持久化目录
        embedding_model: sentence-transformers模型名称
        collection_name: ChromaDB集合名称

    Returns:
        VectorMemoryStore实例
    """
    global _global_vector_store
    if _global_vector_store is None:
        _global_vector_store = VectorMemoryStore(
            persist_directory=persist_directory,
            embedding_model=embedding_model,
            collection_name=collection_name
        )
    return _global_vector_store
