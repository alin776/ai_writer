"""
工具监控系统 (Tool Monitor)

提供工具执行的监控和统计功能,包括:
1. 执行日志记录
2. 性能统计
3. 错误追踪
4. 使用分析

支持 Redis 存储(可选)和内存存储。
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
import logging
import json
from app.utils.datetime_utils import get_utc_now

logger = logging.getLogger(__name__)


# ==================== 工具监控器 ====================

class ToolMonitor:
    """
    工具监控器

    负责记录和统计工具的执行情况,包括:
    - 执行次数统计
    - 成功率统计
    - 执行时间统计
    - 错误追踪
    - 使用趋势分析

    支持两种存储方式:
    1. Redis 存储(推荐,用于生产环境)
    2. 内存存储(默认,用于开发/测试)
    """

    def __init__(self, redis_client=None, retention_days: int = 7):
        """
        初始化工具监控器

        Args:
            redis_client: Redis 客户端实例(可选)
            retention_days: 数据保留天数(默认7天)
        """
        self.redis = redis_client
        self.retention_days = retention_days

        # 内存存储(当没有 Redis 时使用)
        self._memory_logs: List[Dict[str, Any]] = []
        self._memory_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "total_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "total_time": 0.0,
            "errors": []
        })

        logger.info(
            f"ToolMonitor initialized with "
            f"{'Redis' if redis_client else 'Memory'} storage, "
            f"retention: {retention_days} days"
        )

    # ==================== 日志记录 ====================

    def log_execution(
        self,
        tool_name: str,
        execution_time: float,
        success: bool,
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        记录工具执行日志

        Args:
            tool_name: 工具名称
            execution_time: 执行时间(秒)
            success: 是否成功
            input_data: 输入数据(可选)
            output_data: 输出数据(可选)
            error: 错误消息(如果失败)
            metadata: 额外的元数据
        """
        timestamp = get_utc_now()

        log_entry = {
            "tool_name": tool_name,
            "timestamp": timestamp.isoformat(),
            "execution_time": execution_time,
            "success": success,
            "error": error,
            "metadata": metadata or {}
        }

        # 添加输入输出数据的摘要(避免存储大量数据)
        if input_data:
            log_entry["input_summary"] = self._summarize_data(input_data)
        if output_data:
            log_entry["output_summary"] = self._summarize_data(output_data)

        if self.redis:
            self._log_to_redis(log_entry)
        else:
            self._log_to_memory(log_entry)

        # 更新统计
        self._update_statistics(tool_name, execution_time, success, error)

    def _log_to_redis(self, log_entry: Dict[str, Any]):
        """记录到 Redis"""
        try:
            # 使用 Redis List 存储日志
            key = f"tool_monitor:logs:{log_entry['tool_name']}"
            self.redis.lpush(key, json.dumps(log_entry, ensure_ascii=False))

            # 设置过期时间
            self.redis.expire(key, self.retention_days * 86400)

            # 限制列表长度(最多保留1000条)
            self.redis.ltrim(key, 0, 999)

        except Exception as e:
            logger.error(f"Failed to log to Redis: {e}")
            # 回退到内存存储
            self._log_to_memory(log_entry)

    def _log_to_memory(self, log_entry: Dict[str, Any]):
        """记录到内存"""
        self._memory_logs.append(log_entry)

        # 限制内存日志数量
        if len(self._memory_logs) > 1000:
            self._memory_logs = self._memory_logs[-1000:]

    def _update_statistics(
        self,
        tool_name: str,
        execution_time: float,
        success: bool,
        error: Optional[str] = None
    ):
        """更新统计信息"""
        if self.redis:
            self._update_stats_in_redis(tool_name, execution_time, success, error)
        else:
            self._update_stats_in_memory(tool_name, execution_time, success, error)

    def _update_stats_in_redis(
        self,
        tool_name: str,
        execution_time: float,
        success: bool,
        error: Optional[str] = None
    ):
        """更新 Redis 中的统计信息"""
        try:
            key = f"tool_monitor:stats:{tool_name}"

            # 使用 Redis Hash 存储统计
            self.redis.hincrby(key, "total_count", 1)
            if success:
                self.redis.hincrby(key, "success_count", 1)
            else:
                self.redis.hincrby(key, "failure_count", 1)

            # 累加执行时间
            self.redis.hincrbyfloat(key, "total_time", execution_time)

            # 记录错误(如果有)
            if error:
                error_key = f"tool_monitor:errors:{tool_name}"
                self.redis.lpush(error_key, json.dumps({
                    "timestamp": get_utc_now().isoformat(),
                    "error": error
                }, ensure_ascii=False))
                self.redis.ltrim(error_key, 0, 99)  # 最多保留100个错误
                self.redis.expire(error_key, self.retention_days * 86400)

            # 设置过期时间
            self.redis.expire(key, self.retention_days * 86400)

        except Exception as e:
            logger.error(f"Failed to update stats in Redis: {e}")
            # 回退到内存存储
            self._update_stats_in_memory(tool_name, execution_time, success, error)

    def _update_stats_in_memory(
        self,
        tool_name: str,
        execution_time: float,
        success: bool,
        error: Optional[str] = None
    ):
        """更新内存中的统计信息"""
        stats = self._memory_stats[tool_name]
        stats["total_count"] += 1
        if success:
            stats["success_count"] += 1
        else:
            stats["failure_count"] += 1
        stats["total_time"] += execution_time

        if error:
            stats["errors"].append({
                "timestamp": get_utc_now().isoformat(),
                "error": error
            })
            # 限制错误记录数量
            if len(stats["errors"]) > 100:
                stats["errors"] = stats["errors"][-100:]

    # ==================== 统计查询 ====================

    def get_tool_stats(
        self,
        tool_name: str,
        days: int = 1
    ) -> Dict[str, Any]:
        """
        获取工具统计信息

        Args:
            tool_name: 工具名称
            days: 统计天数(默认1天)

        Returns:
            统计信息字典
        """
        if self.redis:
            return self._get_stats_from_redis(tool_name, days)
        else:
            return self._get_stats_from_memory(tool_name)

    def _get_stats_from_redis(
        self,
        tool_name: str,
        days: int
    ) -> Dict[str, Any]:
        """从 Redis 获取统计信息"""
        try:
            key = f"tool_monitor:stats:{tool_name}"
            stats_data = self.redis.hgetall(key)

            if not stats_data:
                return self._empty_stats()

            total_count = int(stats_data.get(b"total_count", 0))
            success_count = int(stats_data.get(b"success_count", 0))
            failure_count = int(stats_data.get(b"failure_count", 0))
            total_time = float(stats_data.get(b"total_time", 0))

            return {
                "tool_name": tool_name,
                "total_count": total_count,
                "success_count": success_count,
                "failure_count": failure_count,
                "success_rate": success_count / total_count if total_count > 0 else 0,
                "avg_execution_time": total_time / total_count if total_count > 0 else 0,
                "total_execution_time": total_time,
                "recent_errors": self._get_recent_errors_from_redis(tool_name, limit=10)
            }

        except Exception as e:
            logger.error(f"Failed to get stats from Redis: {e}")
            return self._empty_stats()

    def _get_stats_from_memory(self, tool_name: str) -> Dict[str, Any]:
        """从内存获取统计信息"""
        if tool_name not in self._memory_stats:
            return self._empty_stats()

        stats = self._memory_stats[tool_name]
        total_count = stats["total_count"]

        return {
            "tool_name": tool_name,
            "total_count": total_count,
            "success_count": stats["success_count"],
            "failure_count": stats["failure_count"],
            "success_rate": stats["success_count"] / total_count if total_count > 0 else 0,
            "avg_execution_time": stats["total_time"] / total_count if total_count > 0 else 0,
            "total_execution_time": stats["total_time"],
            "recent_errors": stats["errors"][-10:] if stats["errors"] else []
        }

    def _get_recent_errors_from_redis(
        self,
        tool_name: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """从 Redis 获取最近的错误"""
        try:
            error_key = f"tool_monitor:errors:{tool_name}"
            errors = self.redis.lrange(error_key, 0, limit - 1)
            return [json.loads(e) for e in errors]
        except Exception as e:
            logger.error(f"Failed to get errors from Redis: {e}")
            return []

    def _empty_stats(self) -> Dict[str, Any]:
        """返回空统计信息"""
        return {
            "tool_name": "",
            "total_count": 0,
            "success_count": 0,
            "failure_count": 0,
            "success_rate": 0,
            "avg_execution_time": 0,
            "total_execution_time": 0,
            "recent_errors": []
        }

    # ==================== 批量统计 ====================

    def get_all_tools_stats(self) -> List[Dict[str, Any]]:
        """
        获取所有工具的统计信息

        Returns:
            工具统计信息列表
        """
        if self.redis:
            return self._get_all_stats_from_redis()
        else:
            return self._get_all_stats_from_memory()

    def _get_all_stats_from_redis(self) -> List[Dict[str, Any]]:
        """从 Redis 获取所有统计"""
        try:
            # 扫描所有统计key
            pattern = "tool_monitor:stats:*"
            stats_list = []

            for key in self.redis.scan_iter(match=pattern):
                tool_name = key.decode().split(":")[-1]
                stats_list.append(self.get_tool_stats(tool_name))

            return stats_list

        except Exception as e:
            logger.error(f"Failed to get all stats from Redis: {e}")
            return []

    def _get_all_stats_from_memory(self) -> List[Dict[str, Any]]:
        """从内存获取所有统计"""
        return [
            self.get_tool_stats(tool_name)
            for tool_name in self._memory_stats.keys()
        ]

    # ==================== 辅助方法 ====================

    def _summarize_data(self, data: Dict[str, Any], max_length: int = 100) -> str:
        """
        生成数据摘要

        Args:
            data: 数据字典
            max_length: 最大长度

        Returns:
            数据摘要字符串
        """
        summary = json.dumps(data, ensure_ascii=False)
        if len(summary) > max_length:
            return summary[:max_length] + "..."
        return summary

    def clear_old_data(self, days: int = None):
        """
        清理旧数据

        Args:
            days: 保留天数(默认使用初始化时的 retention_days)
        """
        days = days or self.retention_days

        if self.redis:
            # Redis 会自动过期,不需要手动清理
            logger.info(f"Redis will auto-expire data after {days} days")
        else:
            # 清理内存中的旧日志
            cutoff_time = get_utc_now() - timedelta(days=days)
            self._memory_logs = [
                log for log in self._memory_logs
                if datetime.fromisoformat(log["timestamp"]) > cutoff_time
            ]
            logger.info(f"Cleared old memory logs, kept {len(self._memory_logs)} logs")


# ==================== 全局监控器实例 ====================

# 全局工具监控器(默认使用内存存储)
_global_monitor: Optional[ToolMonitor] = None


def get_tool_monitor() -> ToolMonitor:
    """
    获取全局工具监控器实例

    Returns:
        ToolMonitor 实例
    """
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = ToolMonitor()
    return _global_monitor


def set_tool_monitor(monitor: ToolMonitor):
    """
    设置全局工具监控器

    Args:
        monitor: ToolMonitor 实例
    """
    global _global_monitor
    _global_monitor = monitor
    logger.info("Global tool monitor updated")


# ==================== 导出 ====================

__all__ = [
    "ToolMonitor",
    "get_tool_monitor",
    "set_tool_monitor",
]
