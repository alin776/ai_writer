# Phase 2: 核心功能实施

**优先级**: ⚡ P0（高）
**预计时间**: 3小时
**前置依赖**: Phase 1 完成
**风险等级**: 🟡 中

---

## 📋 概述

Phase 2 的目标是实现进度反馈的核心功能，包括：

1. **进度百分比计算优化** - 更准确的进度计算
2. **ETA动态优化** - 基于实际速度的ETA
3. **工具参数提取** - 显示具体的工具操作信息
4. **步骤信息增强** - 更友好的步骤描述

**为什么是P0**: 这些功能直接影响用户体验，是进度反馈的核心价值。

---

## 🎯 任务清单

### Task 2.1: 优化进度百分比计算（1小时）

**目标**: 实现更准确、更平滑的进度计算

#### 当前问题

Phase 1的基础实现存在以下问题：
1. 不同场景（写作/规划/分析）经过的节点不同，权重需要动态调整
2. 当前节点按固定50%计算，不够准确
3. 没有考虑工具执行的细粒度进度

#### 优化方案

**Step 1: 动态节点权重归一化（30分钟）**

修改`ProgressTracker.calculate_progress()`方法：

```python
# backend/app/services/agent/progress_tracker.py

def calculate_progress(self) -> Dict[str, Any]:
    """
    计算当前进度（优化版）

    改进点：
    1. 动态归一化权重（确保总权重为1）
    2. 当前节点的进度基于实际执行时间
    3. 平滑处理，避免进度跳跃
    """
    elapsed = time.time() - self.start_time

    # === 动态归一化权重 ===
    if self.expected_nodes:
        # 计算预期节点的总权重
        total_weight = sum(
            get_node_info(node)["progress_weight"]
            for node in self.expected_nodes
        )

        # 归一化：将每个节点的权重除以总权重
        normalized_weights = {
            node: get_node_info(node)["progress_weight"] / total_weight
            for node in self.expected_nodes
        }
    else:
        # 如果没有设置预期节点，使用所有节点
        all_nodes = list(NODE_METADATA.keys())
        total_weight = sum(
            get_node_info(node)["progress_weight"]
            for node in all_nodes
        )
        normalized_weights = {
            node: get_node_info(node)["progress_weight"] / total_weight
            for node in all_nodes
        }

    # === 计算已完成权重 ===
    completed_weight = sum(
        normalized_weights.get(node, 0)
        for node in self.completed_nodes
    )

    # === 当前节点的动态进度 ===
    if self.current_node:
        current_weight = normalized_weights.get(self.current_node, 0)

        # 基于实际执行时间计算当前节点进度
        if self.current_node in self.node_start_times:
            node_elapsed = time.time() - self.node_start_times[self.current_node]
            node_metadata = get_node_info(self.current_node)
            node_estimated_time = node_metadata["estimated_time"]

            # 当前节点的进度比例（0-1）
            node_progress_ratio = min(node_elapsed / node_estimated_time, 0.95)
        else:
            # 默认50%
            node_progress_ratio = 0.5

        # 加上当前节点的部分权重
        completed_weight += current_weight * node_progress_ratio

    # === 进度百分比（0-99） ===
    progress = int(completed_weight * 100)
    progress = min(max(progress, 0), 99)  # 确保在0-99范围内

    # === 其他计算（ETA、步骤等） ===
    eta = self._calculate_eta(elapsed, completed_weight)

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
```

**Step 2: 添加进度平滑处理（15分钟）**

避免进度跳跃，添加平滑逻辑：

```python
class ProgressTracker:
    def __init__(self):
        # ... 现有代码

        # ✅ 新增：上一次报告的进度（用于平滑）
        self.last_reported_progress: int = 0

    def calculate_progress(self) -> Dict[str, Any]:
        # ... 现有计算代码

        # ✅ 平滑处理：确保进度单调递增
        if progress < self.last_reported_progress:
            progress = self.last_reported_progress
        else:
            # 限制单次跳跃幅度（最多增加10%）
            max_increase = 10
            if progress > self.last_reported_progress + max_increase:
                progress = self.last_reported_progress + max_increase

        self.last_reported_progress = progress

        return {
            "progress": progress,
            # ... 其他字段
        }
```

**Step 3: 测试和调优（15分钟）**

```python
# backend/tests/test_progress_calculation.py

def test_progress_normalization():
    """测试权重归一化"""
    tracker = ProgressTracker()

    # 设置3个节点，权重总和不为1
    tracker.set_expected_nodes([
        "intent_classifier",  # 0.30
        "writing_agent",      # 0.35
        "tools"               # 0.10
    ])  # 总和 0.75

    tracker.start_node("intent_classifier")
    tracker.complete_node("intent_classifier")

    progress_info = tracker.calculate_progress()

    # 第一个节点完成应该是约33%（1/3）而不是30%
    assert 30 <= progress_info["progress"] <= 40


def test_progress_smoothness():
    """测试进度平滑"""
    tracker = ProgressTracker()
    tracker.set_expected_nodes(["intent_classifier", "writing_agent"])

    progress_values = []

    # 模拟多次进度查询
    tracker.start_node("intent_classifier")
    for _ in range(5):
        progress_info = tracker.calculate_progress()
        progress_values.append(progress_info["progress"])
        import time
        time.sleep(0.1)

    # 验证进度单调递增
    for i in range(1, len(progress_values)):
        assert progress_values[i] >= progress_values[i-1]

    # 验证没有大幅跳跃
    for i in range(1, len(progress_values)):
        assert progress_values[i] - progress_values[i-1] <= 10
```

---

### Task 2.2: 优化ETA计算（1小时）

**目标**: 实现更准确的剩余时间预估

#### 优化方案

**Step 1: 引入移动平均（30分钟）**

使用历史数据的移动平均来平滑ETA：

```python
# backend/app/services/agent/progress_tracker.py

class ProgressTracker:
    def __init__(self):
        # ... 现有代码

        # ✅ 新增：ETA历史记录（用于平滑）
        self.eta_history: List[int] = []
        self.max_eta_history = 5  # 保留最近5次计算

    def _calculate_eta(self, elapsed: float, completed_weight: float) -> int:
        """
        计算预估剩余时间（优化版）

        改进点：
        1. 使用移动平均平滑ETA
        2. 考虑节点实际耗时
        3. 动态调整预估
        """
        raw_eta = self._calculate_raw_eta(elapsed, completed_weight)

        # ✅ 添加到历史记录
        self.eta_history.append(raw_eta)
        if len(self.eta_history) > self.max_eta_history:
            self.eta_history.pop(0)

        # ✅ 使用移动平均
        if len(self.eta_history) >= 3:
            # 加权移动平均（最近的权重更大）
            weights = [1, 2, 3][-len(self.eta_history):]
            weighted_sum = sum(
                eta * weight
                for eta, weight in zip(self.eta_history, weights)
            )
            smoothed_eta = int(weighted_sum / sum(weights))
        else:
            smoothed_eta = raw_eta

        return max(smoothed_eta, 0)  # 确保非负

    def _calculate_raw_eta(self, elapsed: float, completed_weight: float) -> int:
        """计算原始ETA（未平滑）"""
        # 策略1: 如果已经完成15%以上，基于实际速度估算
        if completed_weight >= 0.15:
            estimated_total_time = elapsed / completed_weight
            remaining_time = estimated_total_time * (1 - completed_weight)
            return int(remaining_time)

        # 策略2: 使用节点预估时间（考虑历史实际耗时）
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
            if node == self.current_node:
                # 当前节点：减去已经过的时间
                if node in self.node_start_times:
                    node_elapsed = time.time() - self.node_start_times[node]
                    node_metadata = get_node_info(node)
                    remaining = max(node_metadata["estimated_time"] - node_elapsed, 0)
                    total_estimated_time += remaining
            else:
                # 未来节点：优先使用历史平均耗时
                if node in self.node_durations and self.node_durations[node]:
                    avg_duration = sum(self.node_durations[node]) / len(self.node_durations[node])
                    total_estimated_time += avg_duration
                else:
                    # 使用配置的预估时间
                    metadata = get_node_info(node)
                    total_estimated_time += metadata["estimated_time"]

        return int(total_estimated_time)
```

**Step 2: 添加置信度指示（15分钟）**

```python
def calculate_progress(self) -> Dict[str, Any]:
    # ... 现有代码

    eta = self._calculate_eta(elapsed, completed_weight)

    # ✅ 新增：ETA置信度
    eta_confidence = "low"
    if completed_weight >= 0.50:
        eta_confidence = "high"
    elif completed_weight >= 0.20:
        eta_confidence = "medium"

    return {
        "progress": progress,
        "eta": eta,
        "eta_confidence": eta_confidence,  # ✅ 新增字段
        # ... 其他字段
    }
```

**Step 3: 测试（15分钟）**

```python
def test_eta_smoothness():
    """测试ETA平滑"""
    tracker = ProgressTracker()
    tracker.set_expected_nodes(["intent_classifier", "writing_agent"])

    import time

    tracker.start_node("intent_classifier")
    time.sleep(0.2)

    eta_values = []
    for _ in range(5):
        progress_info = tracker.calculate_progress()
        eta_values.append(progress_info["eta"])
        time.sleep(0.1)

    # ETA应该逐渐减少且平滑
    # 允许小幅波动，但不应该剧烈跳跃
    for i in range(1, len(eta_values)):
        diff = abs(eta_values[i] - eta_values[i-1])
        assert diff <= 5  # 每次变化不超过5秒
```

---

### Task 2.3: 提取工具参数显示具体信息（45分钟）

**目标**: 让用户看到具体的操作，而不是"正在调用工具..."

#### 实现方案

**Step 1: 在_parse_node_event中提取工具参数（30分钟）**

修改`langgraph_agent.py`中的`_parse_node_event`方法：

```python
# backend/app/services/agent/langgraph_agent.py

def _parse_node_event(self, node_name: str, node_data: dict) -> Optional[dict]:
    """将LangGraph节点事件转换为用户友好的进度信息（优化版）"""

    # ... 现有的节点映射代码

    # ✅ 增强：提取工具详细信息
    if node_name == "tools":
        messages = node_data.get("messages", [])

        for msg in messages:
            # 检查是否有tool_calls
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                for call in msg.tool_calls:
                    tool_name = call.get('name', '')
                    args = call.get('args', {})

                    # 根据不同工具提取具体信息
                    具体描述 = self._extract_tool_specific_info(tool_name, args)
                    if 具体描述:
                        mapping["description"] = 具体描述
                        break

    # ... 返回进度事件

def _extract_tool_specific_info(self, tool_name: str, args: dict) -> Optional[str]:
    """
    提取工具的具体操作信息

    Args:
        tool_name: 工具名称
        args: 工具参数

    Returns:
        str: 友好的描述，如"正在读取第3章..."
    """
    try:
        # === 章节读取工具 ===
        if tool_name == "get_chapter_by_order_tool":
            order = args.get('chapter_order')
            if order:
                return f"📖 正在读取第{order}章..."

        elif tool_name == "read_chapter_tool":
            chapter_id = args.get('chapter_id')
            if chapter_id:
                return f"📖 正在读取章节 #{chapter_id}..."

        # === 检索工具 ===
        elif tool_name == "search_analysis_fragments_tool":
            query = args.get('query', '')
            if query:
                # 截断过长的查询
                display_query = query[:15] + "..." if len(query) > 15 else query
                return f"🔍 正在检索「{display_query}」..."

        elif tool_name == "search_memory_tool":
            query = args.get('query', '')
            if query:
                display_query = query[:15] + "..." if len(query) > 15 else query
                return f"🧠 正在搜索记忆「{display_query}」..."

        # === 写作工具 ===
        elif tool_name == "continue_writing_tool":
            return "✍️ 正在续写内容..."

        # === 上下文工具 ===
        elif tool_name == "get_context_tool":
            context_type = args.get('type', '')
            if context_type:
                type_names = {
                    "chapter": "章节",
                    "work": "作品",
                    "analysis": "分析"
                }
                type_display = type_names.get(context_type, context_type)
                return f"📚 正在获取{type_display}上下文..."

        # === 待办工具 ===
        elif tool_name == "add_todo_tool":
            return "📝 正在添加待办事项..."

        # === 作品信息工具 ===
        elif tool_name == "get_work_details_tool":
            work_id = args.get('work_id')
            if work_id:
                return f"📄 正在获取作品 #{work_id} 信息..."

        elif tool_name == "update_work_metadata_tool":
            return "📝 正在更新作品元数据..."

        # 默认描述
        return None

    except Exception as e:
        logger.error(f"提取工具信息失败: {e}")
        return None
```

**Step 2: 测试工具信息提取（15分钟）**

```python
def test_tool_info_extraction():
    """测试工具信息提取"""
    agent = WritingAgentGraph()

    # 测试章节读取
    info = agent._extract_tool_specific_info(
        "get_chapter_by_order_tool",
        {"chapter_order": 3}
    )
    assert "第3章" in info

    # 测试检索
    info = agent._extract_tool_specific_info(
        "search_analysis_fragments_tool",
        {"query": "主角性格"}
    )
    assert "主角性格" in info
```

---

### Task 2.4: 增强步骤信息（15分钟）

**目标**: 让步骤描述更友好

#### 实现方案

```python
def calculate_progress(self) -> Dict[str, Any]:
    # ... 现有代码

    # ✅ 增强步骤描述
    step_description = self._generate_step_description(
        current_step,
        total_steps,
        self.current_node
    )

    return {
        "progress": progress,
        "eta": eta,
        "current_step": current_step,
        "total_steps": total_steps,
        "step_description": step_description,  # ✅ 新增
        # ... 其他字段
    }

def _generate_step_description(
    self,
    current_step: int,
    total_steps: int,
    current_node: Optional[str]
) -> str:
    """
    生成友好的步骤描述

    Returns:
        str: 如"第 2/5 步" 或 "最后一步"
    """
    if current_step >= total_steps:
        return "最后一步"
    elif current_step == 1:
        return f"第 {current_step}/{total_steps} 步（开始）"
    elif current_step == total_steps - 1:
        return f"第 {current_step}/{total_steps} 步（即将完成）"
    else:
        return f"第 {current_step}/{total_steps} 步"
```

---

## ✅ 验收标准

### Task 2.1: 进度百分比

- [ ] 进度计算准确（与实际进度误差<5%）
- [ ] 进度单调递增，无倒退
- [ ] 进度变化平滑，无大幅跳跃
- [ ] 不同场景的权重正确归一化

### Task 2.2: ETA计算

- [ ] ETA基于实际速度动态调整
- [ ] ETA使用移动平均平滑
- [ ] ETA误差<30%
- [ ] 包含置信度指示

### Task 2.3: 工具信息

- [ ] 至少支持8种常用工具的信息提取
- [ ] 信息提取准确、友好
- [ ] 长文本正确截断
- [ ] 异常情况有降级处理

### Task 2.4: 步骤描述

- [ ] 步骤描述友好易懂
- [ ] 特殊步骤（首步、末步）有特殊提示
- [ ] 格式统一

---

## 🧪 集成测试

```python
async def test_phase2_integration():
    """Phase 2 集成测试"""
    agent = WritingAgentGraph()

    progress_events = []

    async def on_progress(event):
        progress_events.append(event)
        print(f"""
        进度: {event['progress']}%
        ETA: {event['eta']}秒 ({event.get('eta_confidence', 'unknown')})
        步骤: {event.get('step_description', 'N/A')}
        描述: {event['description']}
        """)

    await agent.chat(
        message="帮我读取第3章并分析",
        work_id=1,
        on_progress=on_progress
    )

    # 验证
    assert len(progress_events) > 0

    # 验证进度单调递增
    progresses = [e['progress'] for e in progress_events]
    for i in range(1, len(progresses)):
        assert progresses[i] >= progresses[i-1]

    # 验证包含新字段
    assert 'eta_confidence' in progress_events[-1]
    assert 'step_description' in progress_events[-1]

    # 验证工具信息提取
    tool_events = [e for e in progress_events if '第3章' in e.get('description', '')]
    assert len(tool_events) > 0
```

---

## ⚠️ 注意事项

1. **性能**: 进度计算应该很快（<10ms）
2. **准确性**: 权重配置需要基于实际场景调优
3. **降级**: 如果计算失败，应该优雅降级到基础版本

---

## 📝 下一步

完成Phase 2后，继续：

**[03_Phase3_前端集成实施.md](./03_Phase3_前端集成实施.md)** - 前端UI和用户体验

---

**创建时间**: 2025-11-10
**预计完成**: 3小时
**依赖**: Phase 1
**风险**: 🟡 中
