# -*- coding: utf-8 -*-
"""
操作日志管理器 - 支持 Agent 批量操作的记录和回滚

设计思路：
- Agent 执行链路不打断，所有操作直接执行
- 记录每个操作的"回滚信息"
- 用户弃用时，按逆序回滚所有操作
"""
import json
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
import redis

logger = logging.getLogger(__name__)


@dataclass
class OperationRecord:
    """单个操作记录"""
    op_id: str                    # 操作ID
    op_type: str                  # 操作类型: create_chapter, update_title, update_content, delete_chapter
    timestamp: str                # 时间戳
    # 回滚所需数据
    chapter_id: Optional[str] = None
    work_id: Optional[str] = None
    # 回滚数据（根据操作类型不同）
    rollback_data: Dict[str, Any] = field(default_factory=dict)
    # 操作描述（用于前端显示）
    description: str = ""


class OperationLogManager:
    """操作日志管理器"""

    # Redis key 前缀
    KEY_PREFIX = "agent:operation_log:"
    # 日志过期时间（1小时）
    TTL_SECONDS = 3600

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def _get_key(self, conversation_id: str) -> str:
        return f"{self.KEY_PREFIX}{conversation_id}"

    def record_operation(
        self,
        conversation_id: str,
        op_id: str,
        op_type: str,
        chapter_id: Optional[str] = None,
        work_id: Optional[str] = None,
        rollback_data: Optional[Dict[str, Any]] = None,
        description: str = ""
    ) -> OperationRecord:
        """记录一个操作"""
        record = OperationRecord(
            op_id=op_id,
            op_type=op_type,
            timestamp=datetime.utcnow().isoformat(),
            chapter_id=chapter_id,
            work_id=work_id,
            rollback_data=rollback_data or {},
            description=description
        )

        key = self._get_key(conversation_id)
        # 追加到列表
        self.redis.rpush(key, json.dumps(asdict(record), ensure_ascii=False))
        self.redis.expire(key, self.TTL_SECONDS)

        logger.info(f"[OperationLog] 记录操作: {op_type} - {description}")
        return record

    def get_operations(self, conversation_id: str) -> List[OperationRecord]:
        """获取会话的所有操作记录"""
        key = self._get_key(conversation_id)
        records = self.redis.lrange(key, 0, -1)

        result = []
        for r in records:
            try:
                data = json.loads(r)
                result.append(OperationRecord(**data))
            except Exception as e:
                logger.warning(f"[OperationLog] 解析记录失败: {e}")

        return result

    def clear_operations(self, conversation_id: str) -> None:
        """清除会话的操作记录（采纳后调用）"""
        key = self._get_key(conversation_id)
        self.redis.delete(key)
        logger.info(f"[OperationLog] 清除操作记录: {conversation_id}")

    async def rollback_all(self, conversation_id: str, db) -> Dict[str, Any]:
        """
        回滚会话的所有操作（弃用时调用）

        按逆序执行回滚，确保依赖关系正确
        """
        from app.services.chapter_service import ChapterService
        from app.schemas.chapter import ChapterUpdate

        operations = self.get_operations(conversation_id)
        if not operations:
            return {"success": True, "rolled_back": 0}

        chapter_service = ChapterService(db)
        rolled_back = 0
        errors = []

        # 逆序回滚
        for op in reversed(operations):
            try:
                if op.op_type == "create_chapter":
                    # 回滚创建 = 删除章节
                    if op.chapter_id:
                        await chapter_service.delete_chapter(op.chapter_id)
                        logger.info(f"[Rollback] 删除章节: {op.chapter_id}")
                        rolled_back += 1

                elif op.op_type == "update_title":
                    # 回滚标题修改 = 恢复原标题
                    if op.chapter_id and op.rollback_data.get("old_title"):
                        await chapter_service.update_chapter(
                            op.chapter_id,
                            ChapterUpdate(title=op.rollback_data["old_title"])
                        )
                        logger.info(f"[Rollback] 恢复标题: {op.rollback_data['old_title']}")
                        rolled_back += 1

                elif op.op_type == "update_content":
                    # 回滚内容修改 = 恢复原内容
                    if op.chapter_id and "old_content" in op.rollback_data:
                        await chapter_service.update_chapter(
                            op.chapter_id,
                            ChapterUpdate(content=op.rollback_data["old_content"])
                        )
                        logger.info(f"[Rollback] 恢复内容: chapter_id={op.chapter_id}")
                        rolled_back += 1

                elif op.op_type == "delete_chapter":
                    # 回滚删除 = 重新创建章节（需要完整数据）
                    if op.rollback_data.get("chapter_data"):
                        data = op.rollback_data["chapter_data"]
                        await chapter_service.create_chapter_simple(
                            work_id=data["work_id"],
                            title=data["title"],
                            content=data.get("content", ""),
                            order=data.get("order"),
                            chapter_id=data.get("id")
                        )
                        logger.info(f"[Rollback] 恢复章节: {data['title']}")
                        rolled_back += 1

            except Exception as e:
                logger.error(f"[Rollback] 回滚失败: {op.op_type} - {e}")
                errors.append({"op_id": op.op_id, "error": str(e)})

        # 清除操作记录
        self.clear_operations(conversation_id)

        return {
            "success": len(errors) == 0,
            "rolled_back": rolled_back,
            "errors": errors
        }
