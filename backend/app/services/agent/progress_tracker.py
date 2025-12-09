"""进度追踪器

提供LangGraph Agent执行过程中的实时进度跟踪功能，包括：
- 进度百分比计算（0-100%）
- ETA预估（预计剩余时间）
- 步骤计数（第X/Y步）
- 进度事件生成

Created: 2025-11-10
"""

import time
import logging
import threading
from typing import Dict, List, Optional, Any
from collections import deque

from .node_metadata import get_node_info, get_scenario_nodes, calculate_scenario_total_weight

logger = logging.getLogger(__name__)


class ProgressTracker:
    """进度追踪器

    追踪LangGraph Agent的执行进度，提供实时的进度信息反馈。

    核心功能：
    1. 节点执行追踪（开始/结束时间记录）
    2. 动态进度百分比计算（基于节点权重归一化）
    3. ETA动态计算（基于实际执行速度）
    4. 步骤计数和描述生成
    """

    def __init__(self, scenario: Optional[str] = None, expected_nodes: Optional[List[str]] = None):
        """初始化进度追踪器

        Args:
            scenario: 场景类型 (writing/planning/analysis等)，用于自动设置expected_nodes
            expected_nodes: 预期会经过的节点列表（优先级高于scenario）
        """
        self.start_time = time.time()
        self.current_node: Optional[str] = None
        self.completed_nodes: List[str] = []
        self.node_start_times: Dict[str, float] = {}
        self.node_durations: Dict[str, float] = {}  # 记录每个节点实际执行时间

        # 动态权重归一化相关
        if expected_nodes:
            self.expected_nodes = expected_nodes
        elif scenario:
            self.expected_nodes = get_scenario_nodes(scenario)
        else:
            self.expected_nodes = []

        # ETA计算相关
        self.eta_history: deque = deque(maxlen=5)  # 保存最近5次ETA，用于平滑
        self.last_progress = 0.0  # 上次进度（用于检测跳跃）
        self.last_active_nodes: List[str] = []  # ✅ 新增：上次的active_nodes（用于检测节点变化）

        # ✅ 新增：线程锁保护（P1任务6）- 使用RLock支持可重入
        self._lock = threading.RLock()

        # ✅ 新增：预计算归一化权重
        self._normalized_weights = self._precompute_normalized_weights()

        # 日志输出
        if self.expected_nodes:
            logger.info(
                f"[ProgressTracker] 初始化完成，场景={scenario}, "
                f"预期节点={len(self.expected_nodes)}个{self.expected_nodes}, "
                f"权重总和={sum(self._normalized_weights.values()):.2f}"
            )
        else:
            logger.info(
                "[ProgressTracker] 初始化完成，使用动态节点追踪模式（根据实际执行的节点自动计算进度）"
            )

    def _precompute_normalized_weights(self) -> Dict[str, float]:
        """预计算归一化权重

        确保所有场景的权重总和为1.0，避免运行时计算和除零错误

        Returns:
            Dict[节点名 -> 归一化权重(0-1)]
        """
        if not self.expected_nodes:
            return {}

        # 计算总权重
        total_weight = sum(
            get_node_info(node)["progress_weight"]
            for node in self.expected_nodes
        )

        # 除零保护
        if total_weight == 0:
            logger.warning(
                f"[ProgressTracker] expected_nodes的总权重为0，使用平均权重。"
                f"nodes={self.expected_nodes}"
            )
            return {
                node: 1.0 / len(self.expected_nodes)
                for node in self.expected_nodes
            }

        # 归一化
        normalized = {
            node: get_node_info(node)["progress_weight"] / total_weight
            for node in self.expected_nodes
        }

        logger.debug(f"[ProgressTracker] 归一化权重: {normalized}")
        return normalized

    def start_node(self, node_name: str):
        """开始追踪一个节点

        Args:
            node_name: 节点名称
        """
        with self._lock:
            self.current_node = node_name
            self.node_start_times[node_name] = time.time()

            logger.debug(f"[ProgressTracker] 节点开始: {node_name}")

    def end_node(self, node_name: str):
        """结束追踪一个节点

        Args:
            node_name: 节点名称
        """
        with self._lock:
            if node_name in self.node_start_times:
                duration = time.time() - self.node_start_times[node_name]
                self.node_durations[node_name] = duration

                # 从start_times中移除，避免内存泄漏
                del self.node_start_times[node_name]

            if node_name not in self.completed_nodes:
                self.completed_nodes.append(node_name)

                # ✅ 新增：限制completed_nodes大小（P1任务7）
                if len(self.completed_nodes) > 100:
                    self.completed_nodes = self.completed_nodes[-100:]
                    logger.debug("[ProgressTracker] completed_nodes已修剪到100条")

            if self.current_node == node_name:
                self.current_node = None

            logger.debug(
                f"[ProgressTracker] 节点完成: {node_name} "
                f"({self.node_durations.get(node_name, 0):.2f}s)"
            )

    def calculate_progress(self) -> Dict[str, Any]:
        """计算当前进度

        核心算法：
        1. 动态归一化权重（确保总权重为1）
        2. 当前节点的进度基于实际执行时间
        3. 平滑处理，避免进度跳跃

        Returns:
            Dict: 包含progress, elapsed, current_node等信息
        """
        with self._lock:
            elapsed = time.time() - self.start_time

            # === 动态归一化权重 ===
            nodes_changed = False  # 标记active_nodes是否变化
            if self.expected_nodes:
                # ✅ 使用预计算的归一化权重
                normalized_weights = self._normalized_weights
                active_nodes = self.expected_nodes
            else:
                # 如果没有设置预期节点，使用已完成+当前节点
                active_nodes = self.completed_nodes + ([self.current_node] if self.current_node else [])
                if not active_nodes:
                    # 完全无节点，返回0%
                    return {
                        "progress": 0.0,
                        "elapsed": elapsed,
                        "current_node": None,
                        "current_node_display": None
                    }

                # ✅ 检测active_nodes变化（用于重置平滑处理）
                if active_nodes != self.last_active_nodes:
                    logger.debug(
                        f"[ProgressTracker] active_nodes变化: {self.last_active_nodes} -> {active_nodes}"
                    )
                    nodes_changed = True
                    self.last_active_nodes = active_nodes.copy()

                total_weight = sum(
                    get_node_info(node)["progress_weight"]
                    for node in active_nodes
                )

                # ✅ 除零保护：如果总权重为0，使用平均权重
                if total_weight == 0:
                    logger.warning(
                        f"[ProgressTracker] active_nodes的总权重为0，"
                        f"使用平均权重。nodes={active_nodes}"
                    )
                    normalized_weights = {
                        node: 1.0 / len(active_nodes)
                        for node in active_nodes
                    }
                else:
                    normalized_weights = {
                        node: get_node_info(node)["progress_weight"] / total_weight
                        for node in active_nodes
                    }

            # === 计算已完成权重 ===
            completed_weight = sum(
                normalized_weights.get(node, 0)
                for node in self.completed_nodes
            )

            # === 当前节点的动态进度 ===
            current_node_progress = 0.0
            if self.current_node:
                current_weight = normalized_weights.get(self.current_node, 0)

                # 基于实际执行时间计算当前节点进度
                if self.current_node in self.node_start_times:
                    node_elapsed = time.time() - self.node_start_times[self.current_node]
                    node_metadata = get_node_info(self.current_node)
                    node_estimated_time = node_metadata["estimated_time"]

                    # ✅ 除零保护：estimated_time为0时使用默认进度
                    if node_estimated_time <= 0:
                        logger.warning(
                            f"[ProgressTracker] {self.current_node}的estimated_time<=0，"
                            f"使用默认进度50%"
                        )
                        node_progress_ratio = 0.5
                    else:
                        # 当前节点的进度比例（0-1），最多95%（避免100%时还未完成）
                        node_progress_ratio = min(node_elapsed / node_estimated_time, 0.95)
                else:
                    # 默认50%
                    node_progress_ratio = 0.5

                current_node_progress = current_weight * node_progress_ratio

            # === 总进度（0-1） ===
            total_progress = completed_weight + current_node_progress

            # ✅ 修复：添加上限保护，确保进度不超过100%
            total_progress = min(total_progress, 1.0)

            # === 平滑处理（避免进度倒退） ===
            # 在动态追踪模式下，当active_nodes变化时（新节点加入），允许进度重新计算
            if not self.expected_nodes and nodes_changed:
                # 节点集合变化，重置last_progress允许进度重新计算
                logger.debug(
                    f"[ProgressTracker] 节点集合变化，允许进度重新计算（从{self.last_progress*100:.1f}%到{total_progress*100:.1f}%）"
                )
                self.last_progress = total_progress
            elif total_progress < self.last_progress:
                # 进度不应倒退，保持上次进度
                total_progress = self.last_progress
            else:
                self.last_progress = total_progress

            # 转换为百分比（0-100）
            progress_percentage = total_progress * 100

            return {
                "progress": round(progress_percentage, 1),  # 保留1位小数
                "elapsed": round(elapsed, 1),
                "current_node": self.current_node,
                "current_node_display": get_node_info(self.current_node)["name"] if self.current_node else None
            }

    def calculate_eta(self) -> Dict[str, Any]:
        """计算ETA（预估剩余时间）

        核心算法：
        1. 基于实际速度计算（进度/已用时间 = 速度）
        2. 平滑ETA更新（避免剧烈波动）
        3. 置信度评估（基于已完成节点数）

        Returns:
            Dict: 包含eta, eta_confidence, eta_display等信息
        """
        with self._lock:
            progress_data = self.calculate_progress()
            progress = progress_data["progress"] / 100  # 转换为0-1
            elapsed = progress_data["elapsed"]

            # === 边界情况处理 ===
            if progress <= 0.01:  # 进度小于1%
                # 刚开始，无法准确预估
                return {
                    "eta": None,
                    "eta_confidence": "low",
                    "eta_display": "计算中..."
                }

            if progress >= 0.99:  # 进度大于99%
                # 即将完成
                return {
                    "eta": 0,
                    "eta_confidence": "high",
                    "eta_display": "即将完成"
                }

            # === 基于实际速度计算ETA ===
            # ✅ 除零保护：elapsed为0时使用极小值
            elapsed_safe = max(elapsed, 0.001)
            speed = progress / elapsed_safe  # 进度/时间 = 速度
            remaining_progress = 1 - progress

            # ✅ 除零保护：speed为0时返回最大ETA
            MAX_ETA = 3600  # 最大1小时
            if speed <= 0:
                raw_eta = MAX_ETA
                logger.debug("[ProgressTracker] speed<=0，使用最大ETA")
            else:
                raw_eta = min(remaining_progress / speed, MAX_ETA)

            # === 平滑ETA（移动平均） ===
            self.eta_history.append(raw_eta)
            smoothed_eta = sum(self.eta_history) / len(self.eta_history)

            # === 置信度评估 ===
            completed_count = len(self.completed_nodes)
            if completed_count == 0:
                confidence = "low"
            elif completed_count <= 2:
                confidence = "medium"
            else:
                confidence = "high"

            # === ETA显示优化（智能单位选择） ===
            eta_display = self._format_eta(smoothed_eta)

            return {
                "eta": round(smoothed_eta, 1),
                "eta_confidence": confidence,
                "eta_display": eta_display
            }

    def _format_eta(self, eta_seconds: float) -> str:
        """格式化ETA为友好的显示文本

        Args:
            eta_seconds: ETA秒数

        Returns:
            str: 格式化后的ETA文本
        """
        if eta_seconds < 1:
            return "即将完成"
        elif eta_seconds < 60:
            return f"{int(eta_seconds)}秒"
        elif eta_seconds < 3600:
            minutes = int(eta_seconds / 60)
            return f"{minutes}分钟"
        else:
            hours = int(eta_seconds / 3600)
            return f"{hours}小时"

    def get_step_info(self) -> Dict[str, Any]:
        """获取步骤信息

        Returns:
            Dict: 包含current_step, total_steps, step_description等信息
        """
        current_step = len(self.completed_nodes) + 1  # 当前是第几步（从1开始）
        total_steps = len(self.expected_nodes) if self.expected_nodes else current_step

        # 生成步骤描述
        if total_steps > 0:
            step_description = f"第 {current_step}/{total_steps} 步"
        else:
            step_description = f"第 {current_step} 步"

        return {
            "current_step": current_step,
            "total_steps": total_steps,
            "step_description": step_description
        }

    def get_progress_event(self) -> Dict[str, Any]:
        """生成完整的进度事件数据

        包含所有进度相关信息，用于发送给前端

        Returns:
            Dict: 完整的进度事件数据
        """
        try:
            progress_data = self.calculate_progress()
            eta_data = self.calculate_eta()
            step_data = self.get_step_info()

            # 获取当前节点信息
            node_metadata = get_node_info(self.current_node) if self.current_node else None

            return {
                # 基础信息
                "type": "progress",
                "timestamp": time.time(),

                # 进度信息
                "progress": progress_data.get("progress", 0),
                "elapsed": progress_data.get("elapsed", 0),

                # ETA信息
                "eta": eta_data.get("eta"),
                "eta_confidence": eta_data.get("eta_confidence", "low"),
                "eta_display": eta_data.get("eta_display", "计算中..."),

                # 步骤信息
                "current_step": step_data.get("current_step", 1),
                "total_steps": step_data.get("total_steps", 1),
                "step_description": step_data.get("step_description", "处理中"),

                # 当前节点信息
                "current_node": self.current_node,
                "current_node_display": node_metadata.get("name") if node_metadata else None,
                "current_node_description": node_metadata.get("description") if node_metadata else None,

                # 统计信息
                "completed_nodes_count": len(self.completed_nodes),
                "expected_nodes_count": len(self.expected_nodes) if self.expected_nodes else None
            }
        except Exception as e:
            logger.error(
                f"[ProgressTracker] get_progress_event失败: {e}, "
                f"类型: {type(e).__name__}",
                exc_info=True
            )
            # ✅ 降级处理：返回最基本的进度信息
            return {
                "type": "progress",
                "timestamp": time.time(),
                "progress": 0,
                "elapsed": time.time() - self.start_time,
                "eta": None,
                "eta_confidence": "low",
                "eta_display": "计算中...",
                "current_step": 1,
                "total_steps": 1,
                "step_description": "处理中",
                "current_node": self.current_node,
                "current_node_display": None,
                "current_node_description": None,
                "completed_nodes_count": len(self.completed_nodes) if hasattr(self, 'completed_nodes') else 0,
                "expected_nodes_count": None
            }

    def reset(self):
        """重置追踪器状态"""
        self.start_time = time.time()
        self.current_node = None
        self.completed_nodes = []
        self.node_start_times = {}
        self.node_durations = {}
        self.eta_history.clear()
        self.last_progress = 0.0

        logger.info("[ProgressTracker] 状态已重置")


if __name__ == "__main__":
    # 测试ProgressTracker
    import time as time_module

    print("=== ProgressTracker 测试 ===\n")

    # 场景1：Writing场景
    print("场景1: Writing场景")
    tracker = ProgressTracker(scenario="writing")

    # 模拟intent_classifier节点
    tracker.start_node("intent_classifier")
    time_module.sleep(0.5)
    event = tracker.get_progress_event()
    print(f"  进度: {event['progress']}%, ETA: {event['eta_display']}, {event['step_description']}")
    tracker.end_node("intent_classifier")

    # 模拟writing_agent节点
    tracker.start_node("writing_agent")
    time_module.sleep(1.0)
    event = tracker.get_progress_event()
    print(f"  进度: {event['progress']}%, ETA: {event['eta_display']}, {event['step_description']}")
    tracker.end_node("writing_agent")

    event = tracker.get_progress_event()
    print(f"  完成: {event['progress']}%, 总耗时: {event['elapsed']}s\n")

    print("测试完成!")
