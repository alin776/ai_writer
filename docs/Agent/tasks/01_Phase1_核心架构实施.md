# Phase 1: 核心架构实施

**优先级**: ⚡ P0（最高）
**预计时间**: 4小时
**前置依赖**: 无
**风险等级**: 🟢 低

---

## 📋 概述

Phase 1 的目标是建立进度跟踪的核心基础设施，包括：

1. **NODE_METADATA** - 节点元数据配置（权重、预估时间）
2. **ProgressTracker** - 进度跟踪器类（核心逻辑）
3. **集成到LangGraph** - 与现有Agent系统集成

**为什么是P0**: 这是后续所有功能的基础，必须先完成。

---

## 🎯 任务清单

### Task 1.1: 创建NODE_METADATA配置（1小时）

**文件**: `backend/app/services/agent/node_metadata.py`

**目标**: 定义所有LangGraph节点的元数据

#### 详细步骤

**Step 1: 创建文件结构（10分钟）**

```bash
cd D:\Java\ai_writer\backend\app\services\agent
# 创建新文件
touch node_metadata.py
```

**Step 2: 定义数据结构（20分钟）**

```python
# backend/app/services/agent/node_metadata.py

"""
节点元数据配置
定义每个LangGraph节点的权重、预估时间和友好描述
"""

from typing import Dict, Any, TypedDict


class NodeMetadata(TypedDict):
    """节点元数据类型定义"""
    name: str              # 节点友好名称
    description: str       # 节点描述（给用户看）
    estimated_time: int    # 预估执行时间（秒）
    progress_weight: float # 进度权重（0-1，所有节点总和应该为1）
    category: str          # 节点类别（用于分组）


# 🎯 核心配置：节点元数据
NODE_METADATA: Dict[str, NodeMetadata] = {
    # === 分析类节点 ===
    "intent_classifier": {
        "name": "🧠 意图分析",
        "description": "正在分析您的需求...",
        "estimated_time": 18,
        "progress_weight": 0.30,  # 30% - 意图分类是关键步骤
        "category": "analysis"
    },

    # === 路由类节点 ===
    "route_intent": {
        "name": "🔀 路由决策",
        "description": "正在决定处理方式...",
        "estimated_time": 6,
        "progress_weight": 0.10,  # 10% - 快速路由
        "category": "routing"
    },

    # === Agent类节点 ===
    "writing_agent": {
        "name": "✍️ 创作中",
        "description": "正在为您创作内容...",
        "estimated_time": 25,
        "progress_weight": 0.35,  # 35% - 写作是主要任务
        "category": "generation"
    },

    "planning_agent": {
        "name": "📋 规划中",
        "description": "正在制定计划...",
        "estimated_time": 15,
        "progress_weight": 0.30,  # 30% - 规划也是主要任务
        "category": "planning"
    },

    "analysis_agent": {
        "name": "📊 分析中",
        "description": "正在分析内容...",
        "estimated_time": 20,
        "progress_weight": 0.35,  # 35% - 分析任务
        "category": "analysis"
    },

    "stuck_agent": {
        "name": "💡 寻找灵感",
        "description": "正在寻找解决方案...",
        "estimated_time": 12,
        "progress_weight": 0.25,  # 25% - 卡文处理
        "category": "assistance"
    },

    "general_chat": {
        "name": "💬 对话中",
        "description": "正在思考回复...",
        "estimated_time": 8,
        "progress_weight": 0.20,  # 20% - 简单对话
        "category": "chat"
    },

    # === 工具执行节点 ===
    "tools": {
        "name": "🔧 执行工具",
        "description": "正在调用工具...",
        "estimated_time": 5,
        "progress_weight": 0.10,  # 10% - 工具调用通常较快
        "category": "tool"
    },

    # === 上下文构建节点 ===
    "context_build": {
        "name": "📚 构建上下文",
        "description": "正在加载相关信息...",
        "estimated_time": 21,
        "progress_weight": 0.15,  # 15% - 上下文加载
        "category": "preparation"
    }
}


def get_node_info(node_name: str) -> NodeMetadata:
    """
    获取节点元数据

    Args:
        node_name: 节点名称

    Returns:
        NodeMetadata: 节点元数据，如果不存在则返回默认值
    """
    return NODE_METADATA.get(node_name, {
        "name": "⏳ 处理中",
        "description": f"正在执行 {node_name}...",
        "estimated_time": 10,
        "progress_weight": 0.10,
        "category": "unknown"
    })


def calculate_total_estimated_time(node_names: list[str]) -> int:
    """
    计算一组节点的总预估时间

    Args:
        node_names: 节点名称列表

    Returns:
        int: 总预估时间（秒）
    """
    total_time = 0
    for node_name in node_names:
        metadata = get_node_info(node_name)
        total_time += metadata["estimated_time"]
    return total_time


def get_nodes_by_category(category: str) -> list[str]:
    """
    获取指定类别的所有节点

    Args:
        category: 节点类别

    Returns:
        list[str]: 节点名称列表
    """
    return [
        node_name
        for node_name, metadata in NODE_METADATA.items()
        if metadata["category"] == category
    ]


def validate_weights() -> bool:
    """
    验证权重配置是否合理

    注意：由于不同场景会经过不同的节点，总权重不一定为1
    这个函数用于确保单个节点的权重在合理范围内

    Returns:
        bool: 权重配置是否合理
    """
    for node_name, metadata in NODE_METADATA.items():
        weight = metadata["progress_weight"]
        if weight < 0 or weight > 1:
            print(f"警告: {node_name} 的权重 {weight} 不在 [0, 1] 范围内")
            return False
    return True


# 执行验证
if __name__ == "__main__":
    print("=== 节点元数据验证 ===")
    print(f"节点总数: {len(NODE_METADATA)}")
    print(f"权重验证: {'通过' if validate_weights() else '失败'}")

    print("\n=== 节点类别统计 ===")
    categories = set(meta["category"] for meta in NODE_METADATA.values())
    for category in categories:
        nodes = get_nodes_by_category(category)
        print(f"{category}: {len(nodes)} 个节点")

    print("\n=== 预估时间统计 ===")
    all_nodes = list(NODE_METADATA.keys())
    total_time = calculate_total_estimated_time(all_nodes)
    print(f"所有节点总时间: {total_time} 秒 ({total_time/60:.1f} 分钟)")
```

**Step 3: 调优预估时间（30分钟）**

根据实际日志数据调整`estimated_time`：

1. 查看最近的执行日志
```bash
cd D:\Java\ai_writer
# 查找包含节点执行时间的日志
grep -r "节点.*耗时" backend/logs/ | tail -50
```

2. 统计各节点平均执行时间
3. 更新`NODE_METADATA`中的`estimated_time`

**验证方法**:
```python
# 运行验证脚本
cd D:\Java\ai_writer\backend
python -m app.services.agent.node_metadata
```

预期输出：
```
=== 节点元数据验证 ===
节点总数: 9
权重验证: 通过

=== 节点类别统计 ===
analysis: 2 个节点
routing: 1 个节点
generation: 1 个节点
...
```

---

### Task 1.2: 实现ProgressTracker类（2小时）

**文件**: `backend/app/services/agent/progress_tracker.py`

**目标**: 实现进度跟踪的核心逻辑

#### 详细步骤

**Step 1: 创建基础类结构（30分钟）**

```python
# backend/app/services/agent/progress_tracker.py

"""
进度跟踪器
实时追踪Agent执行进度，计算百分比和ETA
"""

import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

from app.services.agent.node_metadata import (
    get_node_info,
    NODE_METADATA,
    NodeMetadata
)

logger = logging.getLogger(__name__)


class ProgressTracker:
    """
    进度跟踪器

    功能：
    1. 追踪节点执行状态（pending/running/completed）
    2. 计算进度百分比（基于节点权重）
    3. 预估剩余时间（ETA）
    4. 统计执行耗时
    """

    def __init__(self):
        """初始化进度跟踪器"""
        # === 时间追踪 ===
        self.start_time: float = time.time()  # 整体开始时间
        self.node_start_times: Dict[str, float] = {}  # 每个节点的开始时间
        self.node_durations: Dict[str, List[float]] = {}  # 历史耗时记录（用于优化ETA）

        # === 节点状态 ===
        self.completed_nodes: List[str] = []  # 已完成的节点
        self.current_node: Optional[str] = None  # 当前执行的节点
        self.node_statuses: Dict[str, str] = {}  # 节点状态映射

        # === 进度计算 ===
        self.expected_nodes: List[str] = []  # 预期要经过的节点（可动态调整）

        logger.info("[ProgressTracker] 初始化完成")

    def set_expected_nodes(self, node_names: List[str]):
        """
        设置预期要经过的节点

        这对于准确计算进度非常重要，因为不同场景会经过不同的节点
        例如：写作场景会经过 writing_agent，而规划场景会经过 planning_agent

        Args:
            node_names: 预期节点列表
        """
        self.expected_nodes = node_names
        logger.info(f"[ProgressTracker] 设置预期节点: {node_names}")

    def start_node(self, node_name: str):
        """
        记录节点开始执行

        Args:
            node_name: 节点名称
        """
        self.current_node = node_name
        self.node_start_times[node_name] = time.time()
        self.node_statuses[node_name] = "running"

        logger.info(f"[ProgressTracker] 节点开始: {node_name}")

    def complete_node(self, node_name: str):
        """
        记录节点完成

        Args:
            node_name: 节点名称
        """
        if node_name not in self.completed_nodes:
            self.completed_nodes.append(node_name)

        # 记录耗时
        if node_name in self.node_start_times:
            duration = time.time() - self.node_start_times[node_name]

            # 保存到历史记录（用于优化未来的ETA计算）
            if node_name not in self.node_durations:
                self.node_durations[node_name] = []
            self.node_durations[node_name].append(duration)

            logger.info(f"[ProgressTracker] 节点完成: {node_name} (耗时: {duration:.2f}秒)")

        self.node_statuses[node_name] = "completed"
        self.current_node = None

    def fail_node(self, node_name: str, error: str):
        """
        记录节点失败

        Args:
            node_name: 节点名称
            error: 错误信息
        """
        self.node_statuses[node_name] = "failed"
        self.current_node = None
        logger.error(f"[ProgressTracker] 节点失败: {node_name} - {error}")

    def calculate_progress(self) -> Dict[str, Any]:
        """
        计算当前进度

        算法说明：
        1. 基于已完成节点的权重累加
        2. 当前节点按50%计算（假设执行到一半）
        3. 基于实际耗时动态调整ETA

        Returns:
            Dict: 包含进度信息的字典
                - progress: int 进度百分比（0-99，完成时100）
                - eta: int 预估剩余时间（秒）
                - current_step: int 当前步骤数（从1开始）
                - total_steps: int 总步骤数
                - elapsed: int 已经过时间（秒）
                - current_node: str 当前节点名称
                - current_node_display: str 当前节点友好名称
        """
        elapsed = time.time() - self.start_time

        # === 计算已完成权重 ===
        completed_weight = 0.0
        for node in self.completed_nodes:
            metadata = get_node_info(node)
            completed_weight += metadata["progress_weight"]

        # === 当前节点的部分进度 ===
        if self.current_node:
            current_metadata = get_node_info(self.current_node)
            # 假设当前节点已完成50%
            completed_weight += current_metadata["progress_weight"] * 0.5

        # === 如果设置了预期节点，基于预期节点计算进度 ===
        if self.expected_nodes:
            total_weight = sum(
                get_node_info(node)["progress_weight"]
                for node in self.expected_nodes
            )
            if total_weight > 0:
                progress = int((completed_weight / total_weight) * 100)
            else:
                progress = 0
        else:
            # 否则，基于所有节点的平均权重
            progress = int(completed_weight * 100)

        # 确保进度不超过99%（只有真正完成时才100%）
        progress = min(progress, 99)

        # === 计算ETA ===
        eta = self._calculate_eta(elapsed, completed_weight)

        # === 步骤计数 ===
        if self.expected_nodes:
            total_steps = len(self.expected_nodes)
        else:
            total_steps = len(NODE_METADATA)

        current_step = len(self.completed_nodes) + 1

        # === 当前节点信息 ===
        current_node_display = ""
        if self.current_node:
            current_metadata = get_node_info(self.current_node)
            current_node_display = current_metadata["description"]

        return {
            "progress": progress,
            "eta": eta,
            "current_step": current_step,
            "total_steps": total_steps,
            "elapsed": int(elapsed),
            "current_node": self.current_node or "",
            "current_node_display": current_node_display
        }

    def _calculate_eta(self, elapsed: float, completed_weight: float) -> int:
        """
        计算预估剩余时间

        算法：
        1. 如果已经有进度，基于实际速度估算
        2. 否则，使用节点的预估时间

        Args:
            elapsed: 已经过时间（秒）
            completed_weight: 已完成的权重（0-1）

        Returns:
            int: 预估剩余时间（秒）
        """
        if completed_weight > 0.1:  # 至少完成10%才基于速度估算
            # 基于实际速度
            estimated_total_time = elapsed / completed_weight
            remaining_time = estimated_total_time * (1 - completed_weight)
            return int(remaining_time)

        # 使用预估值
        if self.expected_nodes:
            remaining_nodes = [
                node for node in self.expected_nodes
                if node not in self.completed_nodes
            ]
        else:
            remaining_nodes = [
                node for node in NODE_METADATA.keys()
                if node not in self.completed_nodes
            ]

        total_estimated_time = 0
        for node in remaining_nodes:
            # 优先使用历史平均耗时
            if node in self.node_durations and self.node_durations[node]:
                avg_duration = sum(self.node_durations[node]) / len(self.node_durations[node])
                total_estimated_time += avg_duration
            else:
                # 使用配置的预估时间
                metadata = get_node_info(node)
                total_estimated_time += metadata["estimated_time"]

        return int(total_estimated_time)

    def get_node_description(self, node_name: str) -> str:
        """
        获取节点的友好描述

        Args:
            node_name: 节点名称

        Returns:
            str: 友好描述
        """
        metadata = get_node_info(node_name)
        return f"{metadata['name']} {metadata['description']}"

    def reset(self):
        """重置跟踪器（用于新的对话）"""
        self.start_time = time.time()
        self.node_start_times = {}
        self.completed_nodes = []
        self.current_node = None
        self.node_statuses = {}
        self.expected_nodes = []

        logger.info("[ProgressTracker] 已重置")

    def get_summary(self) -> Dict[str, Any]:
        """
        获取执行摘要

        Returns:
            Dict: 执行摘要信息
        """
        total_time = time.time() - self.start_time

        return {
            "total_time": total_time,
            "completed_nodes": len(self.completed_nodes),
            "node_details": [
                {
                    "node": node,
                    "duration": self.node_durations.get(node, [None])[-1],
                    "status": self.node_statuses.get(node, "unknown")
                }
                for node in self.completed_nodes
            ]
        }
```

**Step 2: 添加单元测试（30分钟）**

创建测试文件：

```python
# backend/tests/test_progress_tracker.py

import pytest
import asyncio
from app.services.agent.progress_tracker import ProgressTracker


def test_progress_tracker_initialization():
    """测试初始化"""
    tracker = ProgressTracker()

    assert tracker.start_time > 0
    assert len(tracker.completed_nodes) == 0
    assert tracker.current_node is None


def test_node_tracking():
    """测试节点追踪"""
    tracker = ProgressTracker()

    # 设置预期节点
    tracker.set_expected_nodes(["intent_classifier", "writing_agent"])

    # 开始第一个节点
    tracker.start_node("intent_classifier")
    assert tracker.current_node == "intent_classifier"

    # 完成第一个节点
    tracker.complete_node("intent_classifier")
    assert "intent_classifier" in tracker.completed_nodes
    assert tracker.current_node is None


def test_progress_calculation():
    """测试进度计算"""
    tracker = ProgressTracker()
    tracker.set_expected_nodes(["intent_classifier", "writing_agent"])

    # 完成第一个节点
    tracker.start_node("intent_classifier")
    tracker.complete_node("intent_classifier")

    progress_info = tracker.calculate_progress()

    assert progress_info["progress"] > 0
    assert progress_info["progress"] < 100
    assert progress_info["current_step"] == 2
    assert progress_info["total_steps"] == 2


def test_eta_calculation():
    """测试ETA计算"""
    tracker = ProgressTracker()
    tracker.set_expected_nodes(["intent_classifier", "writing_agent"])

    import time

    # 模拟节点执行
    tracker.start_node("intent_classifier")
    time.sleep(0.1)  # 模拟执行时间
    tracker.complete_node("intent_classifier")

    progress_info = tracker.calculate_progress()

    assert progress_info["eta"] >= 0
    assert progress_info["elapsed"] > 0


def test_reset():
    """测试重置功能"""
    tracker = ProgressTracker()

    tracker.start_node("intent_classifier")
    tracker.complete_node("intent_classifier")

    tracker.reset()

    assert len(tracker.completed_nodes) == 0
    assert tracker.current_node is None
```

运行测试：
```bash
cd D:\Java\ai_writer\backend
pytest tests/test_progress_tracker.py -v
```

**Step 3: 优化和文档（1小时）**

1. 添加更多的日志记录
2. 添加错误处理
3. 优化ETA计算算法
4. 添加docstring文档

---

### Task 1.3: 集成到LangGraph Agent（1小时）

**文件**: `backend/app/services/agent/langgraph_agent.py`

**目标**: 将ProgressTracker集成到现有的Agent系统

#### 详细步骤

**Step 1: 导入依赖（5分钟）**

在`langgraph_agent.py`文件顶部添加：

```python
# 在文件顶部的导入区域添加
from app.services.agent.progress_tracker import ProgressTracker
from app.services.agent.node_metadata import get_node_info
```

**Step 2: 初始化ProgressTracker（10分钟）**

在`WritingAgentGraph`类的`__init__`方法中：

```python
class WritingAgentGraph:
    def __init__(self, ...):
        # ... 现有初始化代码

        # ✅ 新增：初始化进度跟踪器
        self.progress_tracker: Optional[ProgressTracker] = None

        logger.info("[WritingAgentGraph] 初始化完成（包含进度跟踪）")
```

**Step 3: 在流式处理中集成（30分钟）**

修改`_handle_stream_event`方法：

```python
async def _handle_stream_event(
    self,
    event: dict,
    on_progress=None,
    on_tool_call=None,
    on_content=None
):
    """处理流式事件（已有方法，需要修改）"""

    # 获取节点信息
    event_type = event.get("event")
    if event_type != "on_chain_start" and event_type != "on_chain_end":
        return

    node_name = event.get("name", "")
    if not node_name:
        return

    # ✅ 新增：节点开始时更新进度跟踪器
    if event_type == "on_chain_start":
        if self.progress_tracker:
            self.progress_tracker.start_node(node_name)

    # ✅ 新增：节点结束时更新进度跟踪器
    elif event_type == "on_chain_end":
        if self.progress_tracker:
            self.progress_tracker.complete_node(node_name)

    # ... 现有的事件处理代码

    # 1. 解析进度事件并触发on_progress
    if on_progress:
        progress_event = self._parse_node_event(node_name, event)

        # ✅ 新增：添加进度跟踪信息
        if self.progress_tracker and progress_event:
            progress_info = self.progress_tracker.calculate_progress()
            progress_event.update(progress_info)

        if progress_event:
            try:
                await on_progress(progress_event)
            except Exception as e:
                logger.error(f"[Stream] 进度回调失败: {e}")

    # ... 其余现有代码
```

**Step 4: 在chat方法中初始化（15分钟）**

修改`chat`或`chat_stream`方法，在开始执行前初始化：

```python
async def chat(
    self,
    message: str,
    work_id: Optional[int] = None,
    chapter_id: Optional[int] = None,
    conversation_id: Optional[str] = None,
    context: Optional[str] = None,
    on_progress=None,
    on_tool_call=None,
    on_content=None
):
    """与Agent对话（已有方法，需要修改）"""

    # ✅ 新增：初始化进度跟踪器
    self.progress_tracker = ProgressTracker()

    # ✅ 新增：根据意图设置预期节点
    # 注意：这里先用默认配置，后续可以根据意图分类动态调整
    self.progress_tracker.set_expected_nodes([
        "intent_classifier",
        "route_intent",
        "writing_agent",  # 或 planning_agent、analysis_agent等
        "tools"
    ])

    try:
        # ... 现有的执行逻辑

        # 执行完成后
        if self.progress_tracker:
            summary = self.progress_tracker.get_summary()
            logger.info(f"[Agent] 执行摘要: {summary}")

    finally:
        # ✅ 新增：清理
        self.progress_tracker = None
```

---

## ✅ 验收标准

### Task 1.1: NODE_METADATA

- [ ] 文件创建：`backend/app/services/agent/node_metadata.py`
- [ ] 至少定义9个节点的元数据
- [ ] 所有节点的权重在0-1之间
- [ ] 所有节点的预估时间合理（基于实际日志调优）
- [ ] 验证脚本运行通过

### Task 1.2: ProgressTracker

- [ ] 文件创建：`backend/app/services/agent/progress_tracker.py`
- [ ] 类实现完整（包含所有必要方法）
- [ ] 单元测试通过（至少5个测试用例）
- [ ] 日志记录完整
- [ ] 代码有完整的docstring文档

### Task 1.3: 集成

- [ ] ProgressTracker正确集成到`langgraph_agent.py`
- [ ] 节点开始/结束时正确调用跟踪器
- [ ] 进度信息正确添加到progress事件
- [ ] 不影响现有功能（回归测试通过）

---

## 🧪 测试方法

### 1. 单元测试

```bash
cd D:\Java\ai_writer\backend
pytest tests/test_progress_tracker.py -v
```

### 2. 集成测试

启动后端服务，发送测试请求：

```python
# 测试脚本
import asyncio
from app.services.agent.langgraph_agent import WritingAgentGraph

async def test_progress_tracking():
    agent = WritingAgentGraph()

    progress_events = []

    async def on_progress(event):
        progress_events.append(event)
        print(f"进度: {event.get('progress')}%, ETA: {event.get('eta')}秒")

    result = await agent.chat(
        message="帮我续写第5章",
        work_id=1,
        on_progress=on_progress
    )

    # 验证
    assert len(progress_events) > 0
    assert all('progress' in e for e in progress_events)
    assert all('eta' in e for e in progress_events)

    print(f"收到 {len(progress_events)} 个进度事件")

if __name__ == "__main__":
    asyncio.run(test_progress_tracking())
```

---

## ⚠️ 注意事项

### 1. 权重配置

- 不同场景经过的节点不同，权重总和不一定为1
- 权重反映节点的相对重要性和耗时
- 需要根据实际日志持续优化

### 2. ETA计算

- 初始阶段ETA可能不准确（基于预估值）
- 随着执行，ETA会基于实际速度动态调整
- 保守估计，避免误导用户

### 3. 性能影响

- ProgressTracker操作应该非常轻量
- 避免在关键路径上阻塞
- 如果出现问题，应该优雅降级

---

## 📝 下一步

完成Phase 1后，继续：

**[02_Phase2_核心功能实施.md](./02_Phase2_核心功能实施.md)** - 实现进度计算和ETA优化

---

**创建时间**: 2025-11-10
**预计完成**: 4小时
**依赖**: 无
**风险**: 🟢 低
