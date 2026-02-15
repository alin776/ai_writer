# ProgressTracker集成修复计划

## 📋 文档信息

- **创建日期**: 2025-11-11
- **优先级**: P0 - 紧急
- **预计工作量**: 7小时
- **责任人**: 开发团队
- **状态**: 待执行

---

## 🎯 修复目标

将ProgressTracker集成从**不可用状态**修复到**生产就绪状态**

**当前评分**:
- 后端: 5.6/10
- 前端: 3.75/5

**目标评分**:
- 后端: 9/10
- 前端: 4.5/5

---

## 📊 问题概览

| 优先级 | 后端 | 前端 | 总计 |
|--------|------|------|------|
| P0 严重 | 6个 | 3个 | 9个 |
| P1 中等 | 7个 | 6个 | 13个 |
| P2 轻微 | 2个 | 4个 | 6个 |
| **总计** | **15个** | **13个** | **28个** |

---

# 第一优先级修复（P0 - 今天完成）

预计时间：**3小时**

---

## 任务1: 修复start_node缺失问题

### 📍 问题详情

**文件**: `backend/app/services/agent/langgraph_agent.py`
**位置**: 第2443-2455行
**优先级**: P0 - 严重（阻塞）
**预计时间**: 60分钟

**问题描述**:
当前代码只调用了`end_node()`，没有调用`start_node()`，导致：
1. `node_start_times`字典始终为空
2. 当前节点动态进度无法计算（永远是50%默认值）
3. ETA计算完全不准确
4. 进度条会突然跳跃而不是平滑增长

**根本原因**:
LangGraph的`astream()`方法只返回节点完成事件，不包含节点开始事件。

### 🔧 修复方案

**方案**: 使用`astream_events()`替代`astream()`

#### 步骤1.1: 修改导入（如果需要）

```python
# 位置: 第14行附近
from langgraph.graph import StateGraph, END
# ✅ 确认astream_events已在graph对象上可用（无需额外导入）
```

#### 步骤1.2: 替换astream循环

**原代码** (第2443-2455行):
```python
async with asyncio.timeout(300):
    async for event in self.graph.astream(initial_state, config):
        event_count += 1

        # 处理事件并触发回调
        await self._handle_stream_event(
            event,
            on_progress=on_progress,
            on_tool_call=on_tool_call,
            on_content=on_content,
            progress_tracker=progress_tracker
        )
```

**新代码**:
```python
async with asyncio.timeout(300):
    async for event in self.graph.astream_events(initial_state, config, version="v2"):
        event_count += 1

        # 提取事件类型和数据
        event_type = event.get("event")
        event_name = event.get("name")
        event_data = event.get("data", {})

        # 处理节点开始事件
        if event_type == "on_chain_start" and event_name:
            if progress_tracker:
                progress_tracker.start_node(event_name)
                logger.debug(f"[ProgressTracker] 节点开始: {event_name}")

        # 处理节点结束事件
        elif event_type == "on_chain_end" and event_name:
            # 构造原格式的event用于现有逻辑
            formatted_event = {event_name: event_data.get("output", {})}

            # 处理事件并触发回调
            await self._handle_stream_event(
                formatted_event,
                on_progress=on_progress,
                on_tool_call=on_tool_call,
                on_content=on_content,
                progress_tracker=progress_tracker
            )
```

#### 步骤1.3: 更新_handle_stream_event逻辑

**位置**: 第2567-2570行

**原代码**:
```python
# ✅ 追踪节点完成（LangGraph的astream只返回节点完成事件）
if progress_tracker:
    progress_tracker.end_node(node_name)
    logger.debug(f"[ProgressTracker] 节点完成: {node_name}")
```

**新代码** (由于start_node在上层已调用，这里只保留end_node):
```python
# ✅ 追踪节点完成
if progress_tracker:
    progress_tracker.end_node(node_name)
    logger.debug(f"[ProgressTracker] 节点完成: {node_name}")
```

### ✅ 验证步骤

1. **单元测试验证**:
```bash
cd backend
./venv/Scripts/python.exe -m pytest app/services/agent/tests/test_progress_tracker.py::TestNodeTracking -v
```

2. **手动测试验证**:
```python
# 创建临时测试脚本 test_start_node.py
import asyncio
from app.services.agent.langgraph_agent import LangGraphAgent

async def test():
    agent = LangGraphAgent()
    async for event in agent.chat_stream(
        message="测试消息",
        on_progress=lambda p: print(f"Progress: {p.get('progress')}%")
    ):
        pass

asyncio.run(test())
```

3. **日志验证**:
检查日志中应该同时出现：
```
[ProgressTracker] 节点开始: intent_classifier
[ProgressTracker] 节点完成: intent_classifier
```

### 📊 预期结果

- ✅ 日志中同时出现start和end
- ✅ 进度从0%平滑增长到100%
- ✅ ETA倒计时准确
- ✅ 当前节点进度动态更新

---

## 任务2: 修复除零风险

### 📍 问题详情

**文件**: `backend/app/services/agent/progress_tracker.py`
**位置**: 第116行、第232行
**优先级**: P0 - 严重
**预计时间**: 30分钟

**问题描述**:
多处存在除零风险，可能导致运行时崩溃：

1. **位置1**: `calculate_progress()` 第116行
```python
total_weight = sum(...)
normalized_weights = {
    node: get_node_info(node)["progress_weight"] / total_weight  # ❌ total_weight可能为0
    for node in self.expected_nodes
}
```

2. **位置2**: `calculate_eta()` 第232行
```python
speed = progress / elapsed
raw_eta = remaining_progress / speed  # ❌ speed可能为0
```

### 🔧 修复方案

#### 步骤2.1: 修复calculate_progress中的除零

**位置**: 第112-124行

**原代码**:
```python
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
```

**新代码**:
```python
# === 动态归一化权重 ===
if self.expected_nodes:
    # 计算预期节点的总权重
    total_weight = sum(
        get_node_info(node)["progress_weight"]
        for node in self.expected_nodes
    )

    # ✅ 除零保护：如果总权重为0，使用平均权重
    if total_weight == 0:
        logger.warning(
            f"[ProgressTracker] expected_nodes的总权重为0，"
            f"使用平均权重。nodes={self.expected_nodes}"
        )
        normalized_weights = {
            node: 1.0 / len(self.expected_nodes)
            for node in self.expected_nodes
        }
    else:
        # 归一化：将每个节点的权重除以总权重
        normalized_weights = {
            node: get_node_info(node)["progress_weight"] / total_weight
            for node in self.expected_nodes
        }
```

#### 步骤2.2: 修复calculate_eta中的除零

**位置**: 第227-232行

**原代码**:
```python
# === 基于实际速度计算ETA ===
speed = progress / elapsed  # 进度/时间 = 速度
remaining_progress = 1 - progress

# ✅ 修复：添加ETA上限保护（最大1小时）和除零保护
MAX_ETA = 3600  # 最大1小时
raw_eta = min(remaining_progress / speed if speed > 0 else MAX_ETA, MAX_ETA)
```

**新代码** (已经有除零保护，但可以改进):
```python
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
```

#### 步骤2.3: 添加防御性检查到calculate_progress

**位置**: 第158-170行（当前节点进度计算）

**原代码**:
```python
# 基于实际执行时间计算当前节点进度
if self.current_node in self.node_start_times:
    node_elapsed = time.time() - self.node_start_times[self.current_node]
    node_metadata = get_node_info(self.current_node)
    node_estimated_time = node_metadata["estimated_time"]

    # 当前节点的进度比例（0-1），最多95%（避免100%时还未完成）
    node_progress_ratio = min(node_elapsed / node_estimated_time, 0.95)
```

**新代码**:
```python
# 基于实际执行时间计算当前节点进度
if self.current_node in self.node_start_times:
    node_elapsed = time.time() - self.node_start_times[self.current_node]
    node_metadata = get_node_info(self.current_node)
    node_estimated_time = node_metadata["estimated_time"]

    # ✅ 除零保护：estimated_time为0时使用默认值
    if node_estimated_time <= 0:
        logger.warning(
            f"[ProgressTracker] {self.current_node}的estimated_time<=0，"
            f"使用默认进度50%"
        )
        node_progress_ratio = 0.5
    else:
        # 当前节点的进度比例（0-1），最多95%（避免100%时还未完成）
        node_progress_ratio = min(node_elapsed / node_estimated_time, 0.95)
```

### ✅ 验证步骤

1. **单元测试 - 边界情况**:
```python
# 在test_progress_tracker.py中添加测试
def test_zero_total_weight():
    """测试总权重为0的情况"""
    # 创建一个权重全为0的场景
    tracker = ProgressTracker(expected_nodes=["unknown_node_1", "unknown_node_2"])

    # 应该不会崩溃
    progress = tracker.calculate_progress()
    assert progress["progress"] >= 0

def test_zero_elapsed_time():
    """测试elapsed为0的情况"""
    tracker = ProgressTracker(expected_nodes=["intent_classifier"])
    # 立即计算ETA
    eta = tracker.calculate_eta()
    assert eta is not None  # 不应该崩溃
```

2. **压力测试**:
```python
# 快速连续调用
for i in range(1000):
    tracker = ProgressTracker(expected_nodes=["intent_classifier"])
    tracker.calculate_progress()
    tracker.calculate_eta()
```

### 📊 预期结果

- ✅ 所有边界测试通过
- ✅ 无ZeroDivisionError异常
- ✅ 日志中有warning但不崩溃

---

## 任务3: 修复styled-jsx内存泄漏

### 📍 问题详情

**文件**: `src/components/agent/ProgressBar.tsx`
**位置**: 第139-152行
**优先级**: P0 - 严重
**预计时间**: 45分钟

**问题描述**:
使用`<style jsx>`会在每次渲染时向DOM注入新的`<style>`标签：
- 30秒任务：约60次渲染 = 60个style标签
- 5分钟任务：约600次渲染 = 600个style标签
- 长时间运行会导致页面卡顿

**证据**:
```tsx
<style jsx>{`
  @keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
  }
  .animate-shimmer {
    animation: shimmer 1.5s infinite;
  }
`}</style>
```

### 🔧 修复方案

**方案**: 改用CSS Module

#### 步骤3.1: 创建CSS Module文件

**新建文件**: `src/components/agent/ProgressBar.module.css`

```css
/* ProgressBar样式 */
.progressBarContainer {
  /* 容器样式 */
}

/* 动画定义 - 只会加载一次 */
@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.shimmer {
  animation: shimmer 1.5s infinite;
}

.progressFill {
  transition: width 500ms ease-out;
}

.progressFillComplete {
  background: #10b981; /* green-500 */
}

.progressFillActive {
  background: #3b82f6; /* blue-500 */
}

/* 脉冲动画 */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

#### 步骤3.2: 修改ProgressBar.tsx

**原代码** (第139-152行):
```tsx
{/* 自定义动画样式 */}
<style jsx>{`
  @keyframes shimmer {
    0% {
      transform: translateX(-100%);
    }
    100% {
      transform: translateX(100%);
    }
  }

  .animate-shimmer {
    animation: shimmer 1.5s infinite;
  }
`}</style>
```

**新代码** (完整组件重构):

```tsx
import React from 'react';
import { Clock, TrendingUp } from 'lucide-react';
import type { ProgressData } from '@/types/agent';
import styles from './ProgressBar.module.css';  // ✅ 导入CSS Module

interface ProgressBarProps {
  progress: number;
  eta?: number | null;
  etaDisplay?: string;
  etaConfidence?: 'low' | 'medium' | 'high';
  currentStep?: number;
  totalSteps?: number;
  stepDescription?: string;
  currentNodeDescription?: string;
  className?: string;
}

const getConfidenceColor = (confidence?: string): string => {
  switch (confidence) {
    case 'high': return 'text-green-600';
    case 'medium': return 'text-yellow-600';
    case 'low': return 'text-gray-500';
    default: return 'text-gray-500';
  }
};

export default function ProgressBar({
  progress,
  eta,
  etaDisplay,
  etaConfidence,
  currentStep,
  totalSteps,
  stepDescription,
  currentNodeDescription,
  className = '',
}: ProgressBarProps) {
  const clampedProgress = Math.min(Math.max(progress, 0), 100);
  const isNearComplete = clampedProgress >= 95;

  return (
    <div className={`${styles.progressBarContainer} ${className}`}>
      {/* 顶部信息行 */}
      <div className="flex items-center justify-between mb-2 text-sm">
        <div className="flex items-center gap-2">
          {currentNodeDescription && (
            <span className="text-gray-700 font-medium">
              {currentNodeDescription}
            </span>
          )}
          {stepDescription && (
            <span className="text-gray-500 text-xs">
              {stepDescription}
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          {etaDisplay && !isNearComplete && (
            <div className={`flex items-center gap-1 text-xs ${getConfidenceColor(etaConfidence)}`}>
              <Clock size={12} />
              <span>{etaDisplay}</span>
            </div>
          )}

          <div className="flex items-center gap-1 text-xs font-medium text-blue-600">
            <TrendingUp size={12} />
            <span>{clampedProgress.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* 进度条 */}
      <div className="relative w-full h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`
            absolute top-0 left-0 h-full rounded-full
            ${styles.progressFill}
            ${isNearComplete ? styles.progressFillComplete : styles.progressFillActive}
          `}
          style={{ width: `${clampedProgress}%` }}
        >
          {/* 动画光效 */}
          {clampedProgress > 0 && clampedProgress < 100 && (
            <div className={`absolute top-0 right-0 bottom-0 w-20 bg-gradient-to-r from-transparent to-white opacity-30 ${styles.shimmer}`} />
          )}
        </div>

        {/* 完成时的脉冲效果 */}
        {clampedProgress >= 100 && (
          <div className={`absolute top-0 left-0 w-full h-full bg-green-500 ${styles.pulse}`} />
        )}
      </div>

      {/* 底部提示 */}
      {isNearComplete && clampedProgress < 100 && (
        <div className="mt-1 text-xs text-green-600 text-center">
          即将完成...
        </div>
      )}
      {clampedProgress >= 100 && (
        <div className="mt-1 text-xs text-green-600 text-center font-medium">
          ✓ 完成
        </div>
      )}
    </div>
  );
}

// ✅ ProgressBarCompact保持不变（也可以添加CSS Module）
export function ProgressBarCompact({
  progress,
  className = '',
}: {
  progress: number;
  className?: string;
}) {
  const clampedProgress = Math.min(Math.max(progress, 0), 100);

  return (
    <div className={`flex items-center gap-2 ${className}`}>
      <div className="flex-1 h-1.5 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full bg-blue-500 rounded-full ${styles.progressFill}`}
          style={{ width: `${clampedProgress}%` }}
        />
      </div>
      <span className="text-xs text-gray-600 font-medium min-w-[40px] text-right">
        {clampedProgress.toFixed(0)}%
      </span>
    </div>
  );
}
```

### ✅ 验证步骤

1. **内存泄漏测试**:
```tsx
// 创建测试页面，快速更新progress
function MemoryLeakTest() {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setProgress(p => (p + 1) % 100);
    }, 100); // 每100ms更新一次

    return () => clearInterval(timer);
  }, []);

  return <ProgressBar progress={progress} />;
}

// 运行5分钟，观察Chrome DevTools内存使用
```

2. **DOM检查**:
```javascript
// 在浏览器控制台运行
document.querySelectorAll('style').length  // 应该是固定数量，不随渲染增加
```

3. **性能对比**:
- 修复前：5分钟后内存增长 ~50MB
- 修复后：5分钟后内存增长 ~5MB

### 📊 预期结果

- ✅ DOM中只有固定数量的style标签
- ✅ 长时间运行内存稳定
- ✅ 动画效果正常

---

## 任务4: 修复Activity覆盖问题

### 📍 问题详情

**文件**: `src/hooks/useAgentChatStream.ts`
**位置**: 第239-259行
**优先级**: P0 - 严重
**预计时间**: 30分钟

**问题描述**:
当前逻辑按`node`去重，导致：
1. 同一节点多次执行只显示最后一次
2. 已完成的activity被新状态覆盖
3. 丢失历史记录

**原代码**:
```typescript
setActivities((prev) => {
  const existingIndex = prev.findIndex(a => a.node === newActivity.node);

  if (existingIndex !== -1) {
    // ❌ 覆盖了之前的activity
    const updated = [...prev];
    updated[existingIndex] = {
      ...updated[existingIndex],
      ...newActivity,
      id: updated[existingIndex].id,
    };
    return updated;
  } else {
    return [...prev, newActivity];
  }
});
```

### 🔧 修复方案

**方案A**: 追加模式（推荐）
**方案B**: 使用复合键去重

#### 步骤4.1: 实现追加模式（推荐）

**新代码**:
```typescript
// ✅ 新增：更新活动流（追加模式）
const newActivity = progressEventToActivity(progressEvent);
setActivities((prev) => {
  // 直接追加，不去重
  const newList = [...prev, newActivity];

  // 限制最多保留50条（防止无限增长）
  if (newList.length > 50) {
    return newList.slice(-50);
  }

  return newList;
});
```

#### 步骤4.2: 优化progressEventToActivity生成唯一ID

**位置**: 第117-145行

**原代码**:
```typescript
return {
  id: `${event.node}-${event.timestamp}`,  // ❌ 可能重复
  // ...
};
```

**新代码**:
```typescript
return {
  id: `${event.node}-${event.timestamp}-${Math.random().toString(36).substr(2, 9)}`,  // ✅ 唯一ID
  type: activityType,
  description: event.description,
  timestamp: event.timestamp,
  status,
  node: event.node,
  details: event.details,
  elapsedTime: event.elapsed,
};
```

#### 步骤4.3: 添加activities数量提示（可选）

**位置**: 在TodoWrite中更新

```typescript
// 在返回值中添加activities统计
return {
  // ...
  activities,
  activitiesCount: activities.length,  // ✅ 新增
  // ...
};
```

### 🔄 可选方案B: 使用复合键去重

如果需要保持去重逻辑但避免覆盖历史：

```typescript
setActivities((prev) => {
  // 使用 node + timestamp 作为复合键
  const key = `${newActivity.node}-${newActivity.timestamp}`;
  const existingIndex = prev.findIndex(
    a => `${a.node}-${a.timestamp}` === key
  );

  if (existingIndex !== -1) {
    // 只更新状态，不覆盖整个对象
    const updated = [...prev];
    updated[existingIndex] = {
      ...updated[existingIndex],
      status: newActivity.status,  // 只更新状态
      elapsedTime: newActivity.elapsedTime,
    };
    return updated;
  } else {
    const newList = [...prev, newActivity];
    return newList.length > 50 ? newList.slice(-50) : newList;
  }
});
```

### ✅ 验证步骤

1. **手动测试 - 多次调用同一节点**:
```typescript
// 模拟场景：writing_agent被调用3次
sendMessage("写第一段");  // 应该显示1个activity
// ... 完成
sendMessage("写第二段");  // 应该显示2个activity
// ... 完成
sendMessage("写第三段");  // 应该显示3个activity
```

2. **UI检查**:
- ActivityStream应该显示所有历史记录
- 每个activity有唯一的视觉标识
- 滚动查看历史

3. **内存检查**:
```typescript
// 确认限制生效
for (let i = 0; i < 100; i++) {
  sendMessage(`测试${i}`);
}
// activities.length应该 <= 50
```

### 📊 预期结果

- ✅ 所有activity都被记录
- ✅ 不会覆盖历史记录
- ✅ 列表长度受限（不会无限增长）
- ✅ ID唯一不重复

---

## 任务5: 修复权重配置问题

### 📍 问题详情

**文件**: `backend/app/services/agent/node_metadata.py`
**位置**: 第22-90行
**优先级**: P0 - 严重
**预计时间**: 15分钟

**问题描述**:
基础场景的权重总和≠1.0：
```python
# writing场景
"intent_classifier": 0.15
"writing_agent": 0.65
# 总和: 0.80 ❌

# writing_with_tools场景
"intent_classifier": 0.15
"writing_agent": 0.65
"tools": 0.20
# 总和: 1.00 ✅
```

**影响**:
- writing场景进度最多到80%
- 不同场景进度增长不一致
- 用户体验混乱

### 🔧 修复方案

**方案**: 在ProgressTracker初始化时自动归一化（已在calculate_progress中实现，但可以提前）

#### 步骤5.1: 在ProgressTracker.__init__中预计算归一化权重

**文件**: `backend/app/services/agent/progress_tracker.py`
**位置**: 第34-62行

**原代码**:
```python
def __init__(self, scenario: Optional[str] = None, expected_nodes: Optional[List[str]] = None):
    self.start_time = time.time()
    # ...

    if expected_nodes:
        self.expected_nodes = expected_nodes
    elif scenario:
        self.expected_nodes = get_scenario_nodes(scenario)
    else:
        self.expected_nodes = []
```

**新代码**:
```python
def __init__(self, scenario: Optional[str] = None, expected_nodes: Optional[List[str]] = None):
    self.start_time = time.time()
    # ...

    if expected_nodes:
        self.expected_nodes = expected_nodes
    elif scenario:
        self.expected_nodes = get_scenario_nodes(scenario)
    else:
        self.expected_nodes = []

    # ✅ 新增：预计算归一化权重
    self._normalized_weights = self._precompute_normalized_weights()

    logger.info(
        f"[ProgressTracker] 初始化完成，场景={scenario}, "
        f"预期节点={len(self.expected_nodes)}个, "
        f"权重总和={sum(self._normalized_weights.values()):.2f}"
    )

def _precompute_normalized_weights(self) -> Dict[str, float]:
    """预计算归一化权重

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
```

#### 步骤5.2: 使用预计算的权重

**位置**: `calculate_progress()` 第112-144行

**原代码**:
```python
# === 动态归一化权重 ===
if self.expected_nodes:
    total_weight = sum(...)
    normalized_weights = {...}
```

**新代码**:
```python
# === 使用预计算的归一化权重 ===
if self.expected_nodes:
    normalized_weights = self._normalized_weights
```

#### 步骤5.3: 添加权重验证测试

**文件**: `backend/app/services/agent/tests/test_progress_tracker.py`

**新增测试**:
```python
class TestWeightNormalization:
    """测试权重归一化"""

    def test_normalized_weights_sum_to_one(self):
        """测试所有场景的归一化权重总和为1.0"""
        scenarios = ["writing", "planning", "analysis", "stuck", "general",
                     "writing_with_tools", "planning_with_tools", "analysis_with_tools"]

        for scenario in scenarios:
            tracker = ProgressTracker(scenario=scenario)

            # 权重总和应该等于1.0（允许浮点误差）
            total = sum(tracker._normalized_weights.values())
            assert abs(total - 1.0) < 0.001, \
                f"场景{scenario}的权重总和为{total}，应该为1.0"

    def test_zero_weight_scenario(self):
        """测试权重全为0的场景"""
        tracker = ProgressTracker(expected_nodes=["unknown_node_1", "unknown_node_2"])

        # 应该使用平均权重
        assert len(tracker._normalized_weights) == 2
        for weight in tracker._normalized_weights.values():
            assert abs(weight - 0.5) < 0.001
```

### ✅ 验证步骤

1. **运行权重验证测试**:
```bash
cd backend
./venv/Scripts/python.exe -m pytest app/services/agent/tests/test_progress_tracker.py::TestWeightNormalization -v
```

2. **手动验证各场景进度**:
```python
# 测试所有场景都能到100%
for scenario in ["writing", "planning", "analysis"]:
    tracker = ProgressTracker(scenario=scenario)
    nodes = get_scenario_nodes(scenario)

    # 完成所有节点
    for node in nodes:
        tracker.end_node(node)

    progress = tracker.calculate_progress()
    assert progress["progress"] >= 99.0, f"{scenario}进度只有{progress['progress']}%"
```

3. **日志验证**:
检查初始化日志：
```
[ProgressTracker] 初始化完成，场景=writing, 预期节点=2个, 权重总和=1.00
```

### 📊 预期结果

- ✅ 所有场景权重总和=1.0
- ✅ 完成所有节点后进度=100%
- ✅ 日志显示正确的权重总和
- ✅ 测试全部通过

---

# 第二优先级修复（P1 - 本周完成）

预计时间：**4小时**

---

## 任务6: 添加线程锁保护

**预计时间**: 30分钟

### 问题描述
ProgressTracker的所有方法都没有线程锁，多请求并发时可能出现竞态条件。

### 修复方案

**文件**: `backend/app/services/agent/progress_tracker.py`

#### 步骤6.1: 添加锁初始化

```python
import threading

class ProgressTracker:
    def __init__(self, ...):
        # ...现有代码...

        # ✅ 添加线程锁
        self._lock = threading.Lock()
```

#### 步骤6.2: 保护关键方法

```python
def start_node(self, node_name: str):
    with self._lock:
        self.current_node = node_name
        self.node_start_times[node_name] = time.time()
        logger.debug(f"[ProgressTracker] 节点开始: {node_name}")

def end_node(self, node_name: str):
    with self._lock:
        if node_name in self.node_start_times:
            duration = time.time() - self.node_start_times[node_name]
            self.node_durations[node_name] = duration
            del self.node_start_times[node_name]

        if node_name not in self.completed_nodes:
            self.completed_nodes.append(node_name)

        if self.current_node == node_name:
            self.current_node = None

        logger.debug(f"[ProgressTracker] 节点完成: {node_name}")

def calculate_progress(self) -> Dict[str, Any]:
    with self._lock:
        # ...现有逻辑...
        return {...}

def calculate_eta(self) -> Dict[str, Any]:
    with self._lock:
        # ...现有逻辑...
        return {...}
```

### 验证
```python
# 并发测试
import concurrent.futures

tracker = ProgressTracker(scenario="writing")

def worker(i):
    tracker.start_node(f"node_{i}")
    time.sleep(0.01)
    tracker.end_node(f"node_{i}")

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(worker, range(100))

# 不应该有异常
```

---

## 任务7: 添加内存清理逻辑

**预计时间**: 30分钟

### 问题描述
ProgressTracker实例创建后没有显式清理，可能导致内存泄漏。

### 修复方案

**文件**: `backend/app/services/agent/langgraph_agent.py`

#### 步骤7.1: 在finally块中清理

**位置**: 第2504-2537行

```python
try:
    # ...现有逻辑...

except asyncio.TimeoutError:
    # ...

except Exception as e:
    # ...

finally:
    # ✅ 新增：清理ProgressTracker
    if progress_tracker:
        try:
            progress_tracker.reset()
            del progress_tracker
            logger.debug("[ProgressTracker] 已清理")
        except Exception as e:
            logger.warning(f"[ProgressTracker] 清理失败: {e}")
```

#### 步骤7.2: 添加限制到completed_nodes

**文件**: `backend/app/services/agent/progress_tracker.py`

```python
def end_node(self, node_name: str):
    with self._lock:
        # ...现有逻辑...

        if node_name not in self.completed_nodes:
            self.completed_nodes.append(node_name)

        # ✅ 限制completed_nodes大小
        if len(self.completed_nodes) > 100:
            self.completed_nodes = self.completed_nodes[-100:]
            logger.debug("[ProgressTracker] completed_nodes已修剪到100条")
```

---

## 任务8: 添加React.memo优化

**预计时间**: 20分钟

### 问题描述
ProgressBar组件频繁重渲染（30秒任务约300次）。

### 修复方案

**文件**: `src/components/agent/ProgressBar.tsx`

```tsx
import React, { memo } from 'react';

// ✅ 使用memo包装
export default memo(function ProgressBar({
  progress,
  // ...
}: ProgressBarProps) {
  // ...现有逻辑...
}, (prevProps, nextProps) => {
  // 自定义比较逻辑
  return (
    prevProps.progress === nextProps.progress &&
    prevProps.etaDisplay === nextProps.etaDisplay &&
    prevProps.stepDescription === nextProps.stepDescription
  );
});

// ✅ ProgressBarCompact也使用memo
export const ProgressBarCompact = memo(function ProgressBarCompact({
  progress,
  className = '',
}: {
  progress: number;
  className?: string;
}) {
  // ...
}, (prev, next) => prev.progress === next.progress);
```

---

## 任务9: 补充错误处理

**预计时间**: 40分钟

### 修复位置

#### 9.1 ProgressTracker初始化错误处理

**文件**: `backend/app/services/agent/langgraph_agent.py`

```python
# ✅ 添加try-catch
try:
    progress_tracker = ProgressTracker(
        expected_nodes=["intent_classifier", "writing_agent", "tools"]
    )
    logger.info("[ProgressTracker] 初始化完成")
except Exception as e:
    logger.error(f"[ProgressTracker] 初始化失败: {e}")
    progress_tracker = None  # 降级：不使用进度追踪
```

#### 9.2 get_progress_event错误处理

**文件**: `backend/app/services/agent/langgraph_agent.py:2687-2720`

```python
# ✅ 已有try-catch，但可以改进日志
try:
    progress_event = progress_tracker.get_progress_event()
    # ...
except Exception as e:
    logger.error(
        f"[ProgressTracker] 获取进度失败: {e}",
        exc_info=True  # ✅ 记录完整堆栈
    )
    progress_data = {}
```

---

## 任务10: 添加ARIA可访问性

**预计时间**: 15分钟

### 修复方案

**文件**: `src/components/agent/ProgressBar.tsx`

```tsx
<div
  className={`${styles.progressBarContainer} ${className}`}
  role="progressbar"  // ✅ ARIA role
  aria-valuenow={clampedProgress}  // ✅ 当前值
  aria-valuemin={0}  // ✅ 最小值
  aria-valuemax={100}  // ✅ 最大值
  aria-label={currentNodeDescription || `进度: ${clampedProgress}%`}  // ✅ 标签
>
  {/* ... */}
</div>
```

---

## 任务11: 优化条件渲染

**预计时间**: 20分钟

### 修复方案

**文件**: `src/components/agent/ActivityStream.tsx:112-122`

```tsx
{/* ✅ 改进条件渲染 */}
{progressData &&
 typeof progressData.progress === 'number' &&
 progressData.progress < 100 && (
  <div className="mb-4 px-4 py-3 bg-blue-50 rounded-lg border border-blue-100">
    <ProgressBar
      progress={progressData.progress}
      etaDisplay={progressData.eta_display}
      etaConfidence={progressData.eta_confidence}
      stepDescription={progressData.step_description}
      currentNodeDescription={progressData.current_node_description}
    />
  </div>
)}
```

---

## 任务12: 添加类型验证

**预计时间**: 40分钟

### 修复方案

#### 12.1 安装zod

```bash
npm install zod
```

#### 12.2 创建schema

**新建文件**: `src/schemas/progressData.ts`

```typescript
import { z } from 'zod';

export const ProgressDataSchema = z.object({
  progress: z.number().min(0).max(100),
  eta: z.number().nullable(),
  eta_display: z.string(),
  eta_confidence: z.enum(['low', 'medium', 'high']),
  current_step: z.number().int().positive(),
  total_steps: z.number().int().positive(),
  step_description: z.string(),
  elapsed: z.number().nonnegative(),
  current_node: z.string().optional(),
  current_node_display: z.string().optional(),
  current_node_description: z.string().optional(),
});

export type ValidatedProgressData = z.infer<typeof ProgressDataSchema>;
```

#### 12.3 在Hook中验证

**文件**: `src/hooks/useAgentChatStream.ts`

```typescript
import { ProgressDataSchema } from '@/schemas/progressData';

// 在onProgress回调中
if (progress.progress !== undefined) {
  try {
    // ✅ 验证数据
    const validatedData = ProgressDataSchema.parse({
      progress: progress.progress,
      eta: progress.eta ?? null,
      // ...
    });
    setProgressData(validatedData);
  } catch (error) {
    console.error('ProgressData验证失败:', error);
    // 降级：使用部分数据
    setProgressData({
      progress: progress.progress || 0,
      eta: null,
      eta_display: '计算中...',
      // ...
    });
  }
}
```

---

## 任务13-15: 其他优化

### 任务13: 修复完成状态逻辑
**时间**: 10分钟
```typescript
// 不要一刀切标记为completed
setActivities((prev) =>
  prev.map(a =>
    a.status === 'active' ? { ...a, status: 'completed' } : a
  )
);
```

### 任务14: 提取工具函数
**时间**: 10分钟
```typescript
// 提取到组件外部
const getConfidenceColor = (confidence?: string): string => {
  // ...
};
```

### 任务15: 补充generating类型映射
**时间**: 5分钟
```typescript
const stepToTypeMap: Record<string, ActivityType> = {
  'intent_analysis': 'intent_analysis',
  'thinking': 'thinking',
  'tool_execution': 'tool_execution',
  'generating': 'generating',  // ✅ 新增
};
```

---

# 验证和测试

## 集成测试清单

### 后端测试
```bash
# 1. 单元测试
cd backend
./venv/Scripts/python.exe -m pytest app/services/agent/tests/test_progress_tracker.py -v

# 2. 手动测试
./venv/Scripts/python.exe -c "
from app.services.agent.progress_tracker import ProgressTracker
tracker = ProgressTracker(scenario='writing')
# 验证初始化
print(tracker._normalized_weights)
"
```

### 前端测试
```bash
# 1. 类型检查
npm run type-check

# 2. 构建测试
npm run build

# 3. 开发模式测试
npm run dev
```

### 端到端测试
1. 启动后端: `uvicorn app.main:app --reload`
2. 启动前端: `npm run dev`
3. 发送测试消息
4. 观察：
   - 进度条从0平滑增长到100
   - ETA倒计时准确
   - Activities列表正确显示
   - 无内存泄漏（Chrome DevTools）

---

## 成功标准

### 功能验证
- [ ] 进度从0%平滑增长到100%
- [ ] ETA预估准确（误差<20%）
- [ ] 步骤计数正确
- [ ] Activities完整记录
- [ ] 无崩溃和异常

### 性能验证
- [ ] 长时间运行（5分钟）内存稳定
- [ ] DOM style标签数量固定
- [ ] 进度计算耗时<5ms
- [ ] 无明显卡顿

### 代码质量
- [ ] 所有单元测试通过
- [ ] TypeScript类型检查通过
- [ ] 无ESLint错误
- [ ] 代码Review通过

---

## 文档更新

完成修复后需要更新：

1. `tasks/进度反馈系统集成完成报告.md`
   - 更新问题列表
   - 标记已修复

2. `docs/ProgressTracker使用示例.md`
   - 补充已知限制
   - 更新最佳实践

3. `backend/app/services/agent/PROGRESS_TRACKER_INTEGRATION.md`
   - 更新集成说明
   - 补充故障排查

---

## 附录

### 修复优先级矩阵

| 任务 | 影响范围 | 严重程度 | 修复难度 | 优先级 |
|------|---------|---------|---------|--------|
| 任务1 | 高 | 严重 | 中 | P0 |
| 任务2 | 高 | 严重 | 低 | P0 |
| 任务3 | 中 | 严重 | 低 | P0 |
| 任务4 | 中 | 严重 | 低 | P0 |
| 任务5 | 高 | 严重 | 低 | P0 |
| 任务6 | 中 | 中 | 低 | P1 |
| 任务7 | 中 | 中 | 低 | P1 |
| 任务8 | 低 | 中 | 低 | P1 |
| 任务9-15 | 低-中 | 低-中 | 低 | P1-P2 |

### 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| astream_events不兼容 | 低 | 高 | 回退到astream + 估算 |
| CSS Module冲突 | 低 | 中 | 使用唯一类名前缀 |
| 性能回退 | 中 | 中 | 性能基准测试 |
| 引入新bug | 中 | 高 | 完整测试覆盖 |

---

**文档版本**: v1.0
**最后更新**: 2025-11-11
**下次Review**: 修复完成后
