"""
跨会话记忆关联器 (P2-4修复)

实现不同会话之间的记忆关联：
1. 实体识别：提取角色名、地名等实体
2. 实体关联：建立实体与记忆的映射
3. 跨会话检索：通过实体检索相关记忆
4. 实体图谱：构建简单的实体关系图

核心功能：
- EntityRegistry: 实体注册表
- CrossSessionLinker: 跨会话关联器
- 支持角色、地点、事件等多种实体类型

使用示例：
```python
linker = CrossSessionLinker(redis_client)

# 注册实体
await linker.register_entity(
    user_id="user_123",
    entity_name="张三",
    entity_type="character",
    session_id="session_456",
    memory_id="mem_789"
)

# 跨会话检索
memories = await linker.find_by_entity(
    user_id="user_123",
    entity_name="张三"
)

# 获取实体图谱
graph = await linker.get_entity_graph(user_id="user_123")
```
"""

import json
import re
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from redis import Redis

logger = logging.getLogger(__name__)


class EntityType(Enum):
    """实体类型"""
    CHARACTER = "character"    # 角色/人物
    LOCATION = "location"      # 地点
    ORGANIZATION = "organization"  # 组织
    EVENT = "event"            # 事件
    ITEM = "item"              # 物品
    CONCEPT = "concept"        # 概念/设定
    TIME = "time"              # 时间
    OTHER = "other"            # 其他


@dataclass
class Entity:
    """
    实体数据结构

    表示一个可识别的实体（角色、地点等）
    """
    id: str                              # 实体ID
    name: str                            # 实体名称
    type: EntityType                     # 实体类型
    aliases: List[str] = field(default_factory=list)  # 别名
    description: str = ""                # 描述
    first_seen: Optional[datetime] = None  # 首次出现时间
    last_seen: Optional[datetime] = None   # 最后出现时间
    mention_count: int = 0               # 提及次数
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EntityLink:
    """
    实体-记忆关联

    记录实体与记忆之间的关联
    """
    entity_id: str                       # 实体ID
    memory_id: str                       # 记忆ID
    session_id: str                      # 会话ID
    context: str                         # 上下文片段
    created_at: datetime                 # 创建时间
    relevance: float = 0.5               # 相关度


@dataclass
class EntityRelation:
    """
    实体关系

    记录实体之间的关系
    """
    entity_id_from: str
    entity_id_to: str
    relation_type: str                   # 关系类型（如：朋友、敌人、所在地）
    strength: float = 0.5                # 关系强度
    context: str = ""                    # 关系上下文


class EntityExtractor:
    """
    实体提取器

    从文本中提取实体
    """

    # 常见中文姓氏
    COMMON_SURNAMES = [
        "赵", "钱", "孙", "李", "周", "吴", "郑", "王", "冯", "陈",
        "褚", "卫", "蒋", "沈", "韩", "杨", "朱", "秦", "尤", "许",
        "何", "吕", "施", "张", "孔", "曹", "严", "华", "金", "魏",
        "陶", "姜", "戚", "谢", "邹", "喻", "柏", "水", "窦", "章",
        "云", "苏", "潘", "葛", "奚", "范", "彭", "郎", "鲁", "韦",
        "昌", "马", "苗", "凤", "花", "方", "俞", "任", "袁", "柳"
    ]

    # 地名后缀
    PLACE_SUFFIXES = ["市", "省", "国", "洲", "城", "镇", "县", "区", "岛", "山", "河", "海", "湖"]

    # 组织后缀
    ORG_SUFFIXES = ["门", "派", "宗", "教", "帮", "会", "盟", "堡", "庄", "阁", "殿", "府"]

    def extract_entities(self, text: str) -> List[Tuple[str, EntityType, str]]:
        """
        从文本中提取实体

        Args:
            text: 文本内容

        Returns:
            实体列表：[(实体名, 实体类型, 上下文), ...]
        """
        entities = []

        # 1. 提取引号内容（可能是专有名词）
        quoted = re.findall(r'["""](.*?)["""]', text)
        for q in quoted:
            if 2 <= len(q) <= 20:
                entity_type = self._guess_entity_type(q)
                context = self._get_context(text, q)
                entities.append((q, entity_type, context))

        # 2. 提取书名号内容
        book_names = re.findall(r'《(.*?)》', text)
        for b in book_names:
            if len(b) <= 20:
                entities.append((b, EntityType.ITEM, self._get_context(text, b)))

        # 3. 提取中文人名
        for surname in self.COMMON_SURNAMES:
            names = re.findall(rf'{surname}[\u4e00-\u9fff]{{1,3}}', text)
            for name in names:
                if 2 <= len(name) <= 4:
                    context = self._get_context(text, name)
                    entities.append((name, EntityType.CHARACTER, context))

        # 4. 提取地名
        for suffix in self.PLACE_SUFFIXES:
            places = re.findall(rf'[\u4e00-\u9fff]{{2,6}}{suffix}', text)
            for place in places:
                context = self._get_context(text, place)
                entities.append((place, EntityType.LOCATION, context))

        # 5. 提取组织名
        for suffix in self.ORG_SUFFIXES:
            orgs = re.findall(rf'[\u4e00-\u9fff]{{2,6}}{suffix}', text)
            for org in orgs:
                context = self._get_context(text, org)
                entities.append((org, EntityType.ORGANIZATION, context))

        # 6. 去重（保留第一次出现）
        seen = set()
        unique_entities = []
        for entity in entities:
            name = entity[0]
            if name not in seen:
                seen.add(name)
                unique_entities.append(entity)

        return unique_entities[:30]  # 限制最多30个实体

    def _guess_entity_type(self, text: str) -> EntityType:
        """猜测实体类型"""
        # 根据后缀判断
        for suffix in self.PLACE_SUFFIXES:
            if text.endswith(suffix):
                return EntityType.LOCATION

        for suffix in self.ORG_SUFFIXES:
            if text.endswith(suffix):
                return EntityType.ORGANIZATION

        # 检查是否可能是人名
        if len(text) <= 4 and text[0] in self.COMMON_SURNAMES:
            return EntityType.CHARACTER

        return EntityType.OTHER

    def _get_context(self, text: str, entity: str, window: int = 50) -> str:
        """获取实体的上下文"""
        idx = text.find(entity)
        if idx == -1:
            return ""

        start = max(0, idx - window)
        end = min(len(text), idx + len(entity) + window)

        context = text[start:end]
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."

        return context


class CrossSessionLinker:
    """
    跨会话记忆关联器

    管理实体与记忆之间的跨会话关联
    """

    def __init__(self, redis_client: Redis):
        """
        初始化关联器

        Args:
            redis_client: Redis客户端
        """
        self.redis = redis_client
        self.extractor = EntityExtractor()

        logger.info("[CrossSessionLinker] Initialized")

    def _get_entity_key(self, user_id: str, entity_id: str) -> str:
        """获取实体存储key"""
        return f"entity:{user_id}:{entity_id}"

    def _get_entity_index_key(self, user_id: str) -> str:
        """获取实体索引key"""
        return f"entity:index:{user_id}"

    def _get_entity_links_key(self, user_id: str, entity_id: str) -> str:
        """获取实体关联key"""
        return f"entity:links:{user_id}:{entity_id}"

    def _get_entity_relations_key(self, user_id: str) -> str:
        """获取实体关系key"""
        return f"entity:relations:{user_id}"

    def _generate_entity_id(self, name: str) -> str:
        """生成实体ID"""
        import hashlib
        hash_str = hashlib.md5(name.encode('utf-8')).hexdigest()[:8]
        return f"entity_{hash_str}"

    async def register_entity(
        self,
        user_id: str,
        entity_name: str,
        entity_type: EntityType,
        session_id: str,
        memory_id: str,
        context: str = "",
        aliases: Optional[List[str]] = None
    ) -> str:
        """
        注册实体

        Args:
            user_id: 用户ID
            entity_name: 实体名称
            entity_type: 实体类型
            session_id: 会话ID
            memory_id: 记忆ID
            context: 上下文
            aliases: 别名列表

        Returns:
            实体ID
        """
        entity_id = self._generate_entity_id(entity_name)
        entity_key = self._get_entity_key(user_id, entity_id)

        now = datetime.now(timezone.utc)

        # 检查实体是否已存在
        existing = self.redis.get(entity_key)

        if existing:
            # 更新现有实体
            if isinstance(existing, bytes):
                existing = existing.decode('utf-8')

            entity_data = json.loads(existing)
            entity_data["last_seen"] = now.isoformat()
            entity_data["mention_count"] = entity_data.get("mention_count", 0) + 1

            # 合并别名
            if aliases:
                existing_aliases = set(entity_data.get("aliases", []))
                existing_aliases.update(aliases)
                entity_data["aliases"] = list(existing_aliases)

        else:
            # 创建新实体
            entity_data = {
                "id": entity_id,
                "name": entity_name,
                "type": entity_type.value,
                "aliases": aliases or [],
                "first_seen": now.isoformat(),
                "last_seen": now.isoformat(),
                "mention_count": 1,
                "metadata": {}
            }

            # 添加到索引
            index_key = self._get_entity_index_key(user_id)
            self.redis.sadd(index_key, entity_id)

        # 保存实体
        self.redis.set(entity_key, json.dumps(entity_data, ensure_ascii=False))

        # 创建关联
        await self._create_link(user_id, entity_id, memory_id, session_id, context)

        logger.debug(
            f"[CrossSessionLinker] Registered entity: "
            f"name={entity_name}, type={entity_type.value}, id={entity_id}"
        )

        return entity_id

    async def _create_link(
        self,
        user_id: str,
        entity_id: str,
        memory_id: str,
        session_id: str,
        context: str
    ):
        """创建实体-记忆关联"""
        links_key = self._get_entity_links_key(user_id, entity_id)

        link_data = {
            "entity_id": entity_id,
            "memory_id": memory_id,
            "session_id": session_id,
            "context": context[:200],  # 限制上下文长度
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.redis.lpush(links_key, json.dumps(link_data, ensure_ascii=False))
        # 保留最近100个关联
        self.redis.ltrim(links_key, 0, 99)

    async def find_by_entity(
        self,
        user_id: str,
        entity_name: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        通过实体名称检索关联的记忆

        Args:
            user_id: 用户ID
            entity_name: 实体名称
            limit: 最大返回数量

        Returns:
            关联的记忆信息列表
        """
        entity_id = self._generate_entity_id(entity_name)
        links_key = self._get_entity_links_key(user_id, entity_id)

        links = self.redis.lrange(links_key, 0, limit - 1)

        result = []
        for link in links:
            if isinstance(link, bytes):
                link = link.decode('utf-8')

            link_data = json.loads(link)
            result.append(link_data)

        return result

    async def find_related_entities(
        self,
        user_id: str,
        entity_name: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查找与指定实体相关的其他实体

        基于共同出现在同一记忆中的实体

        Args:
            user_id: 用户ID
            entity_name: 实体名称
            limit: 最大返回数量

        Returns:
            相关实体列表
        """
        entity_id = self._generate_entity_id(entity_name)

        # 获取该实体关联的所有记忆ID
        links_key = self._get_entity_links_key(user_id, entity_id)
        links = self.redis.lrange(links_key, 0, -1)

        memory_ids = set()
        for link in links:
            if isinstance(link, bytes):
                link = link.decode('utf-8')
            link_data = json.loads(link)
            memory_ids.add(link_data.get("memory_id"))

        # 查找同一记忆中出现的其他实体
        related_entities = {}

        # 获取所有实体
        index_key = self._get_entity_index_key(user_id)
        all_entity_ids = self.redis.smembers(index_key)

        for other_entity_id in all_entity_ids:
            if isinstance(other_entity_id, bytes):
                other_entity_id = other_entity_id.decode('utf-8')

            if other_entity_id == entity_id:
                continue

            # 检查是否有共同的记忆
            other_links_key = self._get_entity_links_key(user_id, other_entity_id)
            other_links = self.redis.lrange(other_links_key, 0, -1)

            common_memories = 0
            for other_link in other_links:
                if isinstance(other_link, bytes):
                    other_link = other_link.decode('utf-8')
                other_data = json.loads(other_link)
                if other_data.get("memory_id") in memory_ids:
                    common_memories += 1

            if common_memories > 0:
                # 获取实体信息
                entity_key = self._get_entity_key(user_id, other_entity_id)
                entity_data = self.redis.get(entity_key)

                if entity_data:
                    if isinstance(entity_data, bytes):
                        entity_data = entity_data.decode('utf-8')

                    entity_info = json.loads(entity_data)
                    entity_info["common_memories"] = common_memories
                    related_entities[other_entity_id] = entity_info

        # 按共同记忆数排序
        sorted_entities = sorted(
            related_entities.values(),
            key=lambda x: x.get("common_memories", 0),
            reverse=True
        )

        return sorted_entities[:limit]

    async def extract_and_register(
        self,
        user_id: str,
        session_id: str,
        memory_id: str,
        content: str
    ) -> List[str]:
        """
        从内容中提取实体并注册

        Args:
            user_id: 用户ID
            session_id: 会话ID
            memory_id: 记忆ID
            content: 文本内容

        Returns:
            注册的实体ID列表
        """
        # 提取实体
        entities = self.extractor.extract_entities(content)

        entity_ids = []
        for entity_name, entity_type, context in entities:
            entity_id = await self.register_entity(
                user_id=user_id,
                entity_name=entity_name,
                entity_type=entity_type,
                session_id=session_id,
                memory_id=memory_id,
                context=context
            )
            entity_ids.append(entity_id)

        if entity_ids:
            logger.debug(
                f"[CrossSessionLinker] Extracted {len(entity_ids)} entities "
                f"from memory {memory_id}"
            )

        return entity_ids

    async def get_entity_graph(
        self,
        user_id: str,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        获取用户的实体图谱

        Args:
            user_id: 用户ID
            limit: 最大实体数量

        Returns:
            实体图谱数据
        """
        index_key = self._get_entity_index_key(user_id)
        entity_ids = self.redis.smembers(index_key)

        nodes = []
        edges = []

        # 获取实体节点
        for entity_id in list(entity_ids)[:limit]:
            if isinstance(entity_id, bytes):
                entity_id = entity_id.decode('utf-8')

            entity_key = self._get_entity_key(user_id, entity_id)
            entity_data = self.redis.get(entity_key)

            if entity_data:
                if isinstance(entity_data, bytes):
                    entity_data = entity_data.decode('utf-8')

                entity = json.loads(entity_data)
                nodes.append({
                    "id": entity_id,
                    "name": entity.get("name"),
                    "type": entity.get("type"),
                    "mention_count": entity.get("mention_count", 0)
                })

        # 构建边（基于共同出现）
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i+1:]:
                # 检查是否有共同记忆
                links1_key = self._get_entity_links_key(user_id, node1["id"])
                links2_key = self._get_entity_links_key(user_id, node2["id"])

                memories1 = set()
                for link in self.redis.lrange(links1_key, 0, -1):
                    if isinstance(link, bytes):
                        link = link.decode('utf-8')
                    link_data = json.loads(link)
                    memories1.add(link_data.get("memory_id"))

                memories2 = set()
                for link in self.redis.lrange(links2_key, 0, -1):
                    if isinstance(link, bytes):
                        link = link.decode('utf-8')
                    link_data = json.loads(link)
                    memories2.add(link_data.get("memory_id"))

                common = len(memories1 & memories2)
                if common > 0:
                    edges.append({
                        "from": node1["id"],
                        "to": node2["id"],
                        "weight": common
                    })

        return {
            "nodes": nodes,
            "edges": edges,
            "total_entities": len(nodes),
            "total_relations": len(edges)
        }

    async def list_entities(
        self,
        user_id: str,
        entity_type: Optional[EntityType] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        列出用户的所有实体

        Args:
            user_id: 用户ID
            entity_type: 过滤实体类型
            limit: 最大返回数量

        Returns:
            实体列表
        """
        index_key = self._get_entity_index_key(user_id)
        entity_ids = self.redis.smembers(index_key)

        entities = []
        for entity_id in entity_ids:
            if isinstance(entity_id, bytes):
                entity_id = entity_id.decode('utf-8')

            entity_key = self._get_entity_key(user_id, entity_id)
            entity_data = self.redis.get(entity_key)

            if entity_data:
                if isinstance(entity_data, bytes):
                    entity_data = entity_data.decode('utf-8')

                entity = json.loads(entity_data)

                # 类型过滤
                if entity_type and entity.get("type") != entity_type.value:
                    continue

                entities.append(entity)

        # 按提及次数排序
        entities.sort(key=lambda x: x.get("mention_count", 0), reverse=True)

        return entities[:limit]

    async def delete_entity(
        self,
        user_id: str,
        entity_name: str
    ) -> bool:
        """
        删除实体

        Args:
            user_id: 用户ID
            entity_name: 实体名称

        Returns:
            是否删除成功
        """
        entity_id = self._generate_entity_id(entity_name)

        try:
            # 删除实体数据
            entity_key = self._get_entity_key(user_id, entity_id)
            self.redis.delete(entity_key)

            # 删除关联
            links_key = self._get_entity_links_key(user_id, entity_id)
            self.redis.delete(links_key)

            # 从索引中移除
            index_key = self._get_entity_index_key(user_id)
            self.redis.srem(index_key, entity_id)

            logger.info(f"[CrossSessionLinker] Deleted entity: {entity_name}")
            return True

        except Exception as e:
            logger.error(f"[CrossSessionLinker] Delete failed: {e}")
            return False


# 全局单例
_default_linker: Optional[CrossSessionLinker] = None


def get_cross_session_linker(redis_client: Redis) -> CrossSessionLinker:
    """
    获取全局默认的跨会话关联器实例

    Args:
        redis_client: Redis客户端

    Returns:
        CrossSessionLinker实例
    """
    global _default_linker
    if _default_linker is None:
        _default_linker = CrossSessionLinker(redis_client)
    return _default_linker
