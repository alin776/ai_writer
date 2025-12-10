问题：三层各自独立发展，但职责有重叠。展开说说

● 好，让我详细拆解这个问题：

  三层的设计初衷 vs 实际职责

  Planning 层

  设计初衷：
  用户目标 → 分解成多个子任务 → 并发/顺序执行

  实际承担的职责：
  # planning_agent.py 实际在做的事
  1. 意图分析（判断用户想干什么）
  2. 任务分解（拆成子任务）
  3. 依赖管理（任务顺序）
  4. 执行调度（并发/顺序）
  5. 失败处理（重试策略）      ← 与 DeepAgent 重叠
  6. 动态调整（任务变更）      ← 与 DeepAgent 重叠

---
  DeepAgent 层

  设计初衷：
  任务执行过程中 → 插入反思检查点 → 评估是否重规划

  实际承担的职责：
  # deep_agent/executor.py 实际在做的事
  1. 任务执行循环              ← 与 Planning 重叠
  2. 反思触发判断
  3. 调用 think_tool 反思
  4. 重规划决策
  5. 新任务生成              ← 与 Planning 重叠
  6. 任务增强（补全 tool 字段）← 与 Planning 重叠
  7. 失败处理                ← 与 Planning 重叠

---
  MultiAgent 层

  设计初衷：
  写作任务 → 5 个专业角色分工 → 高质量输出

  实际承担的职责：
  # multi_agent/executor.py 实际在做的事
  1. 模式选择（lite/standard/full）
  2. 大纲生成                 ← 可以是 Planning 的一个任务
  3. 内容写作
  4. 角色一致性检查           ← 可以是 Planning 的一个任务
  5. 逻辑审计                 ← 可以是 Planning 的一个任务
  6. 总编修订
  7. 自己的任务调度           ← 与 Planning 重叠
  8. 自己的事件系统           ← 与 Planning 重叠

---
  具体重叠点分析

  重叠 1：任务执行循环

  # Planning 的执行循环
  async def _execute_tasks_in_parallel(self, tasks):
      for task in tasks:
          result = await self._execute_task(task)

  # DeepAgent 的执行循环（包装了 Planning）
  async def execute_with_reflection(self, tasks):
      for task in tasks:
          result = await execute_task_func(task)  # 调用 Planning
          if should_reflect(task):
              await self._do_reflection(...)

  # MultiAgent 的执行循环（被 Planning 调用）
  async def execute(self, context):
      outline = await self.outline_agent.run()
      draft = await self.writer_agent.run(outline)
      # ...

  问题：三层各有自己的 for task in tasks 循环，嵌套调用。

---
  重叠 2：失败处理和重试

  # Planning 层的失败处理
  if task_failed:
      if retry_count < max_retries:
          await retry_task(task)
      else:
          await skip_or_simplify(task)

  # DeepAgent 层的失败处理
  if task_failed:
      await trigger_reflection()  # 反思
      if needs_replan:
          new_tasks = await replan()  # 重新规划

  # MultiAgent 层的失败处理
  if stage_failed:
      if mode == "full":
          downgrade_to_standard()  # 降级

  问题：三层都有自己的失败处理逻辑，策略不统一。

---
  重叠 3：动态任务生成

  # Planning 可以动态调整任务
  original_tasks = [task1, task2, task3]
  if condition:
      tasks.insert(1, new_task)  # 插入新任务

  # DeepAgent 的重规划
  if needs_replan:
      new_tasks = await generate_new_tasks()  # 完全重新生成
      remaining_tasks = new_tasks

  # MultiAgent 没有，但它的 5 阶段本质上也是"子任务"
  stages = [outline, write, check1, check2, edit]

  问题：Planning 和 DeepAgent 都能生成/修改任务，职责不清。

---
  重叠 4：事件发送

  # Planning 发送事件
  on_plan({"tasks": [...]})
  on_task_start({"task_id": 1})
  on_task_done({"task_id": 1})

  # DeepAgent 发送事件（通过回调）
  on_task_progress({"task_id": 1, "status": "reflecting"})

  # MultiAgent 发送事件（自己的体系）
  on_plan({"tasks": [stage1, stage2, ...]})  # 又一个 plan 事件！
  on_task_start({"task_id": 1})  # task_id 冲突！

  问题：三层都往前端发事件，命名空间冲突。

---
  重叠 5：上下文管理

  # Planning 维护上下文
  context = {
      "completed_tasks": [...],
      "work_id": "xxx",
      "previous_content": "..."
  }

  # DeepAgent 维护上下文
  context = {
      "completed_results": [...],  # 几乎一样
      "reflection_history": [...]
  }

  # MultiAgent 维护上下文
  context = {
      "outline": "...",
      "draft": "...",
      "reviews": [...]
  }

  问题：三层各自维护 context，数据重复传递。

---
  根本原因

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  三层是在不同时期、为了不同目的独立开发的：                    │
  │                                                             │
  │  1. Planning：最早的任务分解系统                             │
  │  2. DeepAgent：后来加的反思能力（参考论文）                   │
  │  3. MultiAgent：再后来加的写作专用协作                       │
  │                                                             │
  │  问题：没有统一设计，而是层层包装                             │
  │                                                             │
  └─────────────────────────────────────────────────────────────┘

  本质上：
  - DeepAgent 是给 Planning 加了"反思外壳"
  - MultiAgent 是给写作任务加了"协作外壳"
  - 两个外壳各自独立，没有整合

---
  理想的统一设计

  class UnifiedExecutor:
      """统一的任务执行器"""

      async def execute(self, goal: str):
          # 1. 规划（原 Planning）
          tasks = await self.plan(goal)
    
          # 2. 执行循环（唯一的循环）
          for task in tasks:
              # 3. 根据任务类型选择执行方式
              if task.type == "writing":
                  result = await self.execute_writing(task)  # 内置协作逻辑
              else:
                  result = await self.execute_simple(task)
    
              # 4. 统一的检查点（原 DeepAgent）
              if self.should_checkpoint(task, result):
                  adjustment = await self.evaluate(result)
                  if adjustment.needs_replan:
                      tasks = self.adjust_tasks(tasks, adjustment)
    
          return results

  收益：
  - 一个执行循环
  - 一套事件系统
  - 一个上下文
  - 职责清晰

---
  要不要按这个方向做重构？还是先做小步简化？

---
---

# 重构方案（2025-12-10 讨论确定）

## 一、整体目标

```
当前：Planning → DeepAgent → MultiAgent（三层嵌套，职责重叠）

目标：Planning（内置反思 + 简化写作）（一层，职责清晰）
```

---

## 二、核心改动

### 改动 1：删除 DeepAgent 层，反思内置到 Planning

**思路**：反思是执行过程的一部分，不是外层包装

```
之前：
┌─────────────────────────────┐
│  DeepAgent（外壳）           │
│  ┌───────────────────────┐  │
│  │  Planning（执行）       │  │
│  └───────────────────────┘  │
└─────────────────────────────┘

之后：
┌─────────────────────────────────────────┐
│  Planning（带反思能力）                   │
│                                         │
│  Plan → Execute → Check → Adjust        │
│           ↓         ↓         ↓         │
│        任务      评估结果   修改Plan      │
└─────────────────────────────────────────┘
```

---

### 改动 2：反思触发机制 - 响应式而非预测式

**核心思想**：不预测哪个任务重要，根据执行结果决定是否反思

```python
async def execute_tasks(self, tasks):
    for task in tasks:
        # 1. 执行任务
        result = await self._execute_task(task)

        # 2. 轻量检查（规则，不调用 AI）
        issue = self._quick_check(result)

        # 3. 有问题才深度反思
        if issue:
            adjustment = await self._reflect(task, result, issue)
            if adjustment.needs_change:
                tasks = self._adjust(tasks, adjustment)
```

**quick_check 规则**：
- 任务失败 → 触发反思
- 结果为空 → 触发反思
- 写作任务审校不通过 → 触发反思
- 其他 → 不触发，继续执行

**去掉的机制**：
- ❌ checkpoint 预标记
- ❌ 间隔触发（每N个任务）
- ❌ 首个任务强制反思
- ❌ 复杂的 think_tool

---

### 改动 3：删除 MultiAgent（已完成 ✅）

**说明**：MultiAgent 模块已于 2025-12-09 删除，写作功能由现有的 WritingAction 和工具直接处理。

---

## 三、文件变化

### 删除

```
backend/app/services/agent/
├── deep_agent/              # 整个目录删除
│   ├── executor.py
│   ├── reflection.py
│   └── config.py
│
└── multi_agent/             # 整个目录删除
    ├── executor.py
    ├── mode_selector.py
    └── agents/
        ├── outline_agent.py
        ├── writer_agent.py
        ├── character_guard.py
        ├── logic_auditor.py
        └── editor_agent.py
```

### 修改

```
backend/app/services/agent/
├── langgraph_agent.py       # 移除 DeepAgent 调用
└── agents/
    └── planning_agent.py    # 内置反思逻辑
```

---

## 四、对比总结

| 维度 | 重构前 | 重构后 |
|------|--------|--------|
| 架构层数 | 3 层 | 1 层 |
| 执行循环 | 3 个 | 1 个 |
| 事件系统 | 3 套 | 1 套 |
| 反思触发 | 预测式（checkpoint） | 响应式（结果驱动） |
| 代码文件 | 15+ | 5 |
| 复杂度 | 高 | 低 |

---

## 五、实施步骤

### 第一步：删除 DeepAgent，反思内置到 Planning

1. 将 `deep_agent/reflection.py` 的核心逻辑移到 `planning_agent.py`
2. 简化为 `_quick_check` + `_reflect`
3. 删除 `deep_agent/` 目录
4. 修改 `langgraph_agent.py` 移除 DeepAgent 调用

### 第二步：统一事件系统

1. 所有事件从 Planning 发出
2. 删除重复的事件发送逻辑
3. 简化前端 TaskListPanel

### 第三步：测试验证

1. 集成测试：Planning 完整执行流程
2. 端到端测试：用户对话到内容生成

---

*方案确定时间: 2025-12-10*

---
---

# 反思机制优化：AI 自己决定是否反思（2025-12-10 补充）

## 一、问题回顾

之前的方案（改动 2）存在问题：

```
问题：为什么要区分普通任务和写作任务？
问题：所有任务不都需要反思机制包裹吗？
问题：反思触发规则依赖任务类型判断，不够优雅
```

**核心洞察**：
- 不应该由外部规则决定是否反思
- AI 执行任务时，它自己最清楚执行得怎么样
- 让 AI 自己决定是否需要反思

---

## 二、新方案：AI 自我评估

### 核心思路

```
每个任务执行时，AI 同时输出：
1. 任务结果
2. 自我评估（是否建议反思）

零额外 AI 调用，反思决策内置在执行中
```

### 优点

| 优点 | 说明 |
|------|------|
| **零额外成本** | 反思决策和执行在同一次 AI 调用中 |
| **最准确** | AI 自己最清楚执行质量 |
| **不需要规则** | 不需要硬编码触发条件 |
| **不需要任务分类** | 不需要区分普通/写作任务 |
| **自适应** | AI 根据具体情况判断 |

---

## 三、数据结构定义

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class SelfAssessment:
    """AI 的自我评估"""
    confident: bool                    # 对结果是否有信心
    concerns: List[str]                # 担忧点
    suggest_reflection: bool           # 是否建议反思
    reason: str                        # 原因

@dataclass
class TaskResult:
    """任务执行结果"""
    content: str                       # 任务输出内容
    assessment: SelfAssessment         # 自我评估
    raw_response: str                  # 原始响应（备用）
```

---

## 四、任务执行器实现

```python
class TaskExecutor:
    """统一的任务执行器"""

    def __init__(self, ai_service):
        self.ai = ai_service

    async def execute(self, task: dict, context: dict) -> TaskResult:
        # 1. 构建 prompt
        prompt = self._build_prompt(task, context)

        # 2. 调用 AI
        response = await self.ai.generate(prompt)

        # 3. 解析响应
        result = self._parse_response(response)

        return result

    def _build_prompt(self, task: dict, context: dict) -> str:
        return f"""
## 任务
{task['description']}

## 上下文
{self._format_context(context)}

## 要求
请完成上述任务，并对你的执行结果进行自我评估。

## 输出格式（严格 JSON）
```json
{{
    "result": "你的任务执行结果（完整内容）",
    "self_assessment": {{
        "confident": true或false,
        "concerns": ["担忧点1", "担忧点2"],
        "suggest_reflection": true或false,
        "reason": "简述为什么建议/不建议在此处进行反思"
    }}
}}
```

## 自我评估指南

**confident**: 你对这个结果是否满意？能否支撑后续任务？
**concerns**: 有什么担忧或不确定的地方？
**suggest_reflection**: 是否建议在此处停下来反思和检查？
**reason**: 简要说明原因

### 以下情况建议反思（suggest_reflection: true）：
1. 对结果质量不够满意
2. 有明显的不确定性或担忧
3. 结果可能影响后续任务的方向
4. 需要用户确认或补充信息

### 以下情况不需要反思（suggest_reflection: false）：
1. 任务完成度高，结果清晰
2. 没有明显担忧
3. 不影响后续任务
"""

    def _parse_response(self, response: str) -> TaskResult:
        """解析 AI 响应"""
        try:
            data = self._extract_json(response)

            assessment = SelfAssessment(
                confident=data["self_assessment"]["confident"],
                concerns=data["self_assessment"].get("concerns", []),
                suggest_reflection=data["self_assessment"]["suggest_reflection"],
                reason=data["self_assessment"].get("reason", "")
            )

            return TaskResult(
                content=data["result"],
                assessment=assessment,
                raw_response=response
            )
        except Exception as e:
            # 解析失败，返回保守结果（建议反思）
            return TaskResult(
                content=response,
                assessment=SelfAssessment(
                    confident=False,
                    concerns=["响应解析失败"],
                    suggest_reflection=True,
                    reason="无法解析自我评估，建议检查"
                ),
                raw_response=response
            )

    def _extract_json(self, text: str) -> dict:
        """从文本中提取 JSON"""
        import json
        import re

        # 尝试直接解析
        try:
            return json.loads(text)
        except:
            pass

        # 尝试提取 ```json ``` 代码块
        match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return json.loads(match.group(1))

        # 尝试提取 { } 内容
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))

        raise ValueError("无法提取 JSON")
```

---

## 五、Planning 引擎集成

```python
class PlanningEngine:
    """Planning 执行引擎"""

    def __init__(self, ai_service):
        self.executor = TaskExecutor(ai_service)
        self.ai = ai_service

    async def execute_plan(self, tasks: List[dict], context: dict):
        results = []
        i = 0

        while i < len(tasks):
            task = tasks[i]
            remaining = tasks[i + 1:]

            # 1. 执行任务（AI 返回结果 + 自我评估）
            result = await self.executor.execute(task, context)
            results.append(result)

            # 2. 更新上下文
            context = self._update_context(context, task, result)

            # 3. AI 建议反思？
            if result.assessment.suggest_reflection:
                # 4. 执行反思
                adjustment = await self._reflect(
                    task=task,
                    result=result,
                    completed=results,
                    remaining=remaining,
                    context=context
                )

                # 5. 应用调整
                if adjustment and adjustment.has_changes:
                    tasks = self._apply_adjustment(tasks, i, adjustment)

            # 6. 兜底检查（即使 AI 说不需要反思）
            elif self._needs_fallback_check(result):
                adjustment = await self._reflect(task, result, results, remaining, context)
                if adjustment and adjustment.has_changes:
                    tasks = self._apply_adjustment(tasks, i, adjustment)

            i += 1

        return results

    def _needs_fallback_check(self, result: TaskResult) -> bool:
        """兜底检查：极端情况"""
        # 结果为空
        if not result.content or len(result.content.strip()) < 10:
            return True
        return False
```

---

## 六、反思实现

```python
async def _reflect(self, task, result, completed, remaining, context):
    """执行反思"""

    prompt = f"""
## 反思检查点

### 刚完成的任务
{task['description']}

### 执行结果
{result.content}

### AI 自我评估
- 置信度：{"高" if result.assessment.confident else "低"}
- 担忧点：{result.assessment.concerns}
- 建议反思原因：{result.assessment.reason}

### 已完成的任务
{self._format_completed(completed)}

### 后续计划
{self._format_remaining(remaining)}

### 请评估

1. 当前结果的问题是否需要处理？如何处理？
2. 后续计划是否需要调整？

### 输出格式
```json
{{
    "analysis": "简要分析当前状况",
    "needs_adjustment": true或false,
    "adjustments": {{
        "redo_current": false,
        "add_tasks": [
            {{"description": "新任务描述", "insert_before": 0}}
        ],
        "modify_tasks": [
            {{"index": 0, "new_description": "修改后的描述"}}
        ],
        "remove_indices": []
    }},
    "message_to_user": "如需告知用户，写在这里"
}}
```
"""

    response = await self.ai.generate(prompt)
    return self._parse_adjustment(response)
```

---

## 七、完整流程图

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   开始执行 Plan                                              │
│        ↓                                                    │
│   ┌─────────────────────────────────────┐                  │
│   │ 执行任务                             │                  │
│   │  - AI 返回：结果 + 自我评估           │                  │
│   │  - 自我评估包含：confident, concerns, │                  │
│   │    suggest_reflection, reason        │                  │
│   └─────────────────────────────────────┘                  │
│        ↓                                                    │
│   assessment.suggest_reflection?                            │
│        │                                                    │
│        ├── Yes ──────────────────────────┐                 │
│        │                                 ↓                 │
│        │                    ┌─────────────────────────┐    │
│        │                    │ 反思                     │    │
│        │                    │  - 分析担忧点            │    │
│        │                    │  - 评估后续计划          │    │
│        │                    │  - 决定是否调整          │    │
│        │                    └─────────────────────────┘    │
│        │                                 ↓                 │
│        │                    有调整？                        │
│        │                    ├── Yes → 修改任务列表          │
│        │                    └── No ──┐                     │
│        │                             │                     │
│        └── No ───→ 兜底检查？ ────────┴─────────┐          │
│                        │                       ↓          │
│                        └─────────────→ 下一个任务          │
│                                                ↓          │
│                                        还有任务？          │
│                                        ├── Yes → 循环     │
│                                        └── No → 完成      │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

---

## 八、AI 什么时候会建议反思？

AI 自己会根据具体情况判断：

```
场景 1：角色创建
"我创建的这个角色有点单薄，可能支撑不了后面的故事"
→ suggest_reflection: true
→ concerns: ["角色特点不够鲜明", "背景故事较简单"]

场景 2：世界观设定
"这个世界观设定很完整，没有问题"
→ suggest_reflection: false
→ confident: true

场景 3：需求分析
"用户的需求我理解了，但有些细节不太确定"
→ suggest_reflection: true
→ concerns: ["不确定用户想要的风格"]

场景 4：大纲生成
"大纲生成完成，结构清晰，情节完整"
→ suggest_reflection: false
→ confident: true
```

---

## 九、文件结构更新

```
backend/app/services/agent/
├── executor/
│   ├── __init__.py
│   ├── task_executor.py      # TaskExecutor（通用任务执行 + 自我评估）
│   └── models.py             # TaskResult, SelfAssessment 等
│
├── planning/
│   ├── __init__.py
│   ├── engine.py             # PlanningEngine（主流程）
│   └── reflection.py         # 反思逻辑
│
└── langgraph_agent.py        # 入口，集成 PlanningEngine
```

---

## 十、对比总结（更新）

| 维度 | 原方案 | 改动 2 方案 | 最终方案 |
|------|--------|-------------|----------|
| 反思触发 | checkpoint 预标记 | 规则判断 | **AI 自己决定** |
| 任务分类 | 需要 | 需要 | **不需要** |
| 额外 AI 调用 | 每个 checkpoint | 规则检查 0，反思时才调用 | **0（内置在执行中）** |
| 准确性 | 低（预测可能错） | 中（规则有限） | **高（AI 自己最清楚）** |
| 灵活性 | 低 | 中 | **高** |

---

*最终方案确定时间: 2025-12-10*

---
---

# Review 反馈与方案修正（2025-12-10）

## 一、发现的问题

### 问题 1：触发条件过窄 ⚠️ 严重

**原方案问题**：
- `_needs_fallback_check` 只看失败/空输出
- 取消了所有计划内 checkpoint
- 逻辑错但有输出的结果不会触发反思

**修正方案**：

```python
def _needs_fallback_check(self, result: TaskResult) -> bool:
    """兜底检查：多维度判断"""

    # 1. 基础检查
    if not result.content or len(result.content.strip()) < 10:
        return True

    # 2. 置信度检查（即使 AI 说不需要反思）
    if not result.assessment.confident:
        return True

    # 3. 有担忧但 AI 没建议反思（过度自信）
    if result.assessment.concerns and len(result.assessment.concerns) > 0:
        return True

    # 4. 关键任务强制检查（通过任务标记）
    if task.get("critical", False):
        return True

    return False
```

---

### 问题 2：缺少护栏机制 ⚠️ 严重

**原方案问题**：
- 完全依赖模型自评，无二次校验
- 缺少反思次数上限
- 缺少费用控制

**修正方案**：

```python
@dataclass
class ExecutionConfig:
    """执行配置与护栏"""
    max_reflections: int = 3          # 单次执行最大反思次数
    max_retries_per_task: int = 2     # 单任务最大重试次数
    max_total_ai_calls: int = 20      # 总 AI 调用上限
    force_reflection_interval: int = 5 # 每 N 个任务强制反思一次（兜底）

class PlanningEngine:
    def __init__(self, ai_service, config: ExecutionConfig = None):
        self.config = config or ExecutionConfig()
        self.reflection_count = 0
        self.total_ai_calls = 0
        self.task_retry_counts = {}

    async def execute_plan(self, tasks, context):
        results = []
        i = 0
        tasks_since_reflection = 0

        while i < len(tasks):
            # 护栏检查
            if self.total_ai_calls >= self.config.max_total_ai_calls:
                raise ExecutionLimitExceeded("AI 调用次数超限")

            task = tasks[i]
            result = await self.executor.execute(task, context)
            self.total_ai_calls += 1
            results.append(result)
            tasks_since_reflection += 1

            # 反思判断（带护栏）
            should_reflect = (
                result.assessment.suggest_reflection or
                self._needs_fallback_check(result) or
                tasks_since_reflection >= self.config.force_reflection_interval
            )

            if should_reflect and self.reflection_count < self.config.max_reflections:
                adjustment = await self._reflect(...)
                self.reflection_count += 1
                self.total_ai_calls += 1
                tasks_since_reflection = 0

                if adjustment and adjustment.has_changes:
                    tasks = self._apply_adjustment(tasks, i, adjustment)

            i += 1

        return results
```

---

### 问题 3：事件命名冲突未解决 ⚠️ 严重

**原方案问题**：
- 未给出统一事件/ID 命名空间
- 前端仍会收到重复或歧义 task_id

**修正方案**：

```python
# 事件命名规范
EVENT_SCHEMA = {
    "version": "2.0",
    "namespaces": {
        "planning": "plan:",      # plan:1, plan:2
        "execution": "exec:",     # exec:1, exec:2
        "reflection": "refl:",    # refl:1
        "writer": "write:",       # write:1.review, write:1.revise
    }
}

@dataclass
class TaskEvent:
    """统一事件结构"""
    event_id: str              # 全局唯一 UUID
    event_type: str            # task_start | task_done | reflection | error
    namespace: str             # planning | execution | reflection | writer
    task_id: str               # 带命名空间的 ID，如 "plan:3"
    parent_task_id: Optional[str]  # 父任务 ID（用于嵌套）
    timestamp: datetime
    data: dict

# 事件发送
def emit_event(event_type: str, namespace: str, task_id: str, data: dict):
    event = TaskEvent(
        event_id=str(uuid.uuid4()),
        event_type=event_type,
        namespace=namespace,
        task_id=f"{EVENT_SCHEMA['namespaces'][namespace]}{task_id}",
        parent_task_id=current_parent_task_id,
        timestamp=datetime.now(),
        data=data
    )
    # 发送给前端
```

**前端兼容映射**：
```typescript
// 旧格式 -> 新格式
function migrateEvent(oldEvent) {
    return {
        ...oldEvent,
        task_id: `plan:${oldEvent.task_id}`,  // 添加命名空间
        event_id: generateUUID(),
    }
}
```

---

### 问题 4：上下文结构未统一 ⚠️ 中等

**原方案问题**：
- 传递不定形的 context
- Writer/反思各自取键
- 数据漂移与重复存储风险

**修正方案**：

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict

@dataclass
class TaskContext:
    """统一的任务上下文 Schema"""

    # 必填字段
    work_id: str
    user_id: str
    session_id: str

    # 作品信息（可选）
    worldview: Optional[str] = None
    characters: List[Dict] = field(default_factory=list)
    outline: Optional[str] = None
    previous_content: Optional[str] = None
    previous_summary: Optional[str] = None

    # 执行状态
    completed_tasks: List[Dict] = field(default_factory=list)
    completed_results: List[Dict] = field(default_factory=list)

    # 元数据
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(self, task: dict, result: TaskResult) -> 'TaskContext':
        """更新上下文（返回新实例，不可变）"""
        return TaskContext(
            **{**self.__dict__,
               'completed_tasks': self.completed_tasks + [task],
               'completed_results': self.completed_results + [result.__dict__],
               'updated_at': datetime.now()
            }
        )

    def to_prompt_dict(self) -> dict:
        """转换为 prompt 使用的字典（只包含必要字段）"""
        return {
            'worldview': self.worldview or "未设定",
            'characters': self.characters or [],
            'outline': self.outline or "未设定",
            'previous_summary': self.previous_summary or "无",
        }
```

**迁移计划**：
1. 定义 `TaskContext` schema
2. 在入口处将旧 dict 转换为 `TaskContext`
3. 内部统一使用 `TaskContext`
4. 逐步移除旧的 dict 传递

---

### 问题 5：执行流退化为串行 ⚠️ 中等

**原方案问题**：
- 丢失原 Planning 的并行能力
- 对无依赖任务会产生性能回退

**修正方案**：

```python
@dataclass
class Task:
    id: str
    description: str
    dependencies: List[str] = field(default_factory=list)  # 依赖的任务 ID
    critical: bool = False  # 是否关键任务（强制反思）

class PlanningEngine:
    async def execute_plan(self, tasks: List[Task], context: TaskContext):
        """支持并行的执行引擎"""

        # 1. 构建依赖图
        graph = self._build_dependency_graph(tasks)

        # 2. 拓扑排序，分层
        layers = self._topological_layers(graph)

        results = {}

        # 3. 按层执行，同层并行
        for layer in layers:
            # 同一层的任务可以并行
            layer_tasks = [tasks[tid] for tid in layer]

            if len(layer_tasks) == 1:
                # 单任务，直接执行
                result = await self._execute_single(layer_tasks[0], context)
                results[layer_tasks[0].id] = result
            else:
                # 多任务，并行执行
                layer_results = await asyncio.gather(*[
                    self._execute_single(t, context) for t in layer_tasks
                ])
                for t, r in zip(layer_tasks, layer_results):
                    results[t.id] = r

            # 更新上下文
            context = self._update_context_batch(context, layer_tasks, layer_results)

            # 层边界反思（可选）
            if self._should_reflect_at_layer_boundary(layer, results):
                await self._reflect(...)

        return results

    def _build_dependency_graph(self, tasks):
        """构建依赖图"""
        graph = {t.id: t.dependencies for t in tasks}
        return graph

    def _topological_layers(self, graph):
        """拓扑排序，返回可并行的层"""
        # 返回 [[task1, task2], [task3], [task4, task5]]
        # 同一层的任务可以并行执行
        ...
```

**任务依赖声明**：
```python
tasks = [
    Task(id="1", description="分析需求", dependencies=[]),
    Task(id="2", description="创建世界观", dependencies=["1"]),
    Task(id="3", description="创建角色", dependencies=["1"]),  # 2 和 3 可并行
    Task(id="4", description="生成大纲", dependencies=["2", "3"]),
    Task(id="5", description="写第一章", dependencies=["4"], critical=True),
]
```

---

### 问题 6：失败/重试策略消失 ⚠️ 中等

**原方案问题**：
- 无最大重试或降级策略
- 单个坏任务可能反复反思或直接放过

**修正方案**：

```python
class PlanningEngine:
    async def _execute_single(self, task: Task, context: TaskContext) -> TaskResult:
        """带重试和降级的单任务执行"""

        retry_count = 0
        last_error = None

        while retry_count <= self.config.max_retries_per_task:
            try:
                result = await self.executor.execute(task, context)

                # 检查结果质量
                if self._is_acceptable(result):
                    return result

                # 质量不达标，重试
                retry_count += 1
                if retry_count <= self.config.max_retries_per_task:
                    # 降级策略：简化任务
                    task = self._simplify_task(task, retry_count)

            except Exception as e:
                last_error = e
                retry_count += 1

        # 重试耗尽，返回降级结果或抛出异常
        return self._create_fallback_result(task, last_error)

    def _simplify_task(self, task: Task, retry_count: int) -> Task:
        """降级策略：简化任务"""
        if retry_count == 1:
            # 第一次重试：简化描述
            return Task(
                **{**task.__dict__,
                   'description': f"简化版本：{task.description}"}
            )
        else:
            # 第二次重试：最小化
            return Task(
                **{**task.__dict__,
                   'description': f"最小化：只完成核心部分 - {task.description}"}
            )

    def _create_fallback_result(self, task: Task, error: Exception) -> TaskResult:
        """创建降级结果"""
        return TaskResult(
            content=f"[任务执行失败，已跳过] {task.description}",
            assessment=SelfAssessment(
                confident=False,
                concerns=[f"执行失败: {str(error)}"],
                suggest_reflection=True,
                reason="任务执行失败，需要人工介入或调整计划"
            )
        )
```

---

### 问题 7：JSON 解析可能误判 ⚠️ 低

**原方案问题**：
- `_extract_json` 以首个 `{}` 解析
- 若正文含花括号会误判

**修正方案**：

```python
def _extract_json(self, text: str) -> dict:
    """强化的 JSON 解析"""
    import json
    import re

    # 方法 1：优先提取 ```json fenced block
    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    # 方法 2：尝试直接解析整个文本
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 方法 3：从末尾向前找最后一个完整 JSON（避免正文干扰）
    # 使用栈匹配花括号
    try:
        json_str = self._extract_last_json_object(text)
        if json_str:
            return json.loads(json_str)
    except:
        pass

    # 解析失败，返回结构化错误
    raise JSONParseError(
        message="无法解析 AI 响应中的 JSON",
        raw_text=text[:500],  # 只保留前 500 字符用于调试
        suggestion="请检查 prompt 格式要求"
    )

def _extract_last_json_object(self, text: str) -> Optional[str]:
    """从文本末尾提取最后一个完整的 JSON 对象"""
    stack = []
    end = -1

    # 从后向前扫描
    for i in range(len(text) - 1, -1, -1):
        if text[i] == '}':
            if end == -1:
                end = i
            stack.append('}')
        elif text[i] == '{':
            if stack:
                stack.pop()
                if not stack:
                    return text[i:end + 1]

    return None

class JSONParseError(Exception):
    """JSON 解析错误"""
    def __init__(self, message: str, raw_text: str, suggestion: str):
        self.message = message
        self.raw_text = raw_text
        self.suggestion = suggestion
        super().__init__(message)
```

---

### 问题 8：ReviewResult 字段未定义 ⚠️ 低

**修正方案**：

```python
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class IssueSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Issue:
    """审校发现的问题"""
    type: str                    # 角色 | 逻辑 | 表达 | 其他
    severity: IssueSeverity
    detail: str
    suggestion: Optional[str] = None

@dataclass
class ReviewResult:
    """审校结果"""
    passed: bool
    issues: List[Issue] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    summary: str = ""

    @property
    def has_serious_issues(self) -> bool:
        return any(i.severity == IssueSeverity.HIGH for i in self.issues)

    @property
    def has_issues(self) -> bool:
        return len(self.issues) > 0

    def merge(self, other: 'ReviewResult') -> 'ReviewResult':
        """合并两个审校结果"""
        return ReviewResult(
            passed=self.passed and other.passed,
            issues=self.issues + other.issues,
            suggestions=self.suggestions + other.suggestions,
            summary=f"{self.summary}\n{other.summary}".strip()
        )

    @classmethod
    def parse(cls, response: str) -> 'ReviewResult':
        """从 AI 响应解析"""
        data = json.loads(response)  # 使用强化的解析

        issues = [
            Issue(
                type=i.get("type", "其他"),
                severity=IssueSeverity(i.get("severity", "medium")),
                detail=i.get("detail", ""),
                suggestion=i.get("suggestion")
            )
            for i in data.get("issues", [])
        ]

        return cls(
            passed=data.get("passed", True),
            issues=issues,
            suggestions=data.get("suggestions", []),
            summary=data.get("summary", "")
        )
```

---

## 二、需要澄清的点（回答）

### 1. 事件/任务 ID 的统一命名与版本化方案

**答案**：见问题 3 的修正方案
- 使用命名空间前缀：`plan:`, `exec:`, `refl:`, `write:`
- 全局唯一 event_id（UUID）
- 支持 parent_task_id 表示嵌套关系
- 版本号：`EVENT_SCHEMA.version = "2.0"`

### 2. context 的规范 schema

**答案**：见问题 4 的修正方案
- 定义 `TaskContext` dataclass
- 必填字段：work_id, user_id, session_id
- 可选字段：worldview, characters, outline 等
- 提供 `to_prompt_dict()` 方法供 prompt 使用

### 3. 反思/重试的次数与费用上限

**答案**：见问题 2 的修正方案
- `max_reflections = 3`（单次执行）
- `max_retries_per_task = 2`（单任务）
- `max_total_ai_calls = 20`（总上限）
- `force_reflection_interval = 5`（兜底）

### 4. 并行执行

**答案**：见问题 5 的修正方案
- 任务通过 `dependencies` 字段声明依赖
- 构建依赖图，拓扑排序分层
- 同层任务使用 `asyncio.gather` 并行执行
- 串行保留依赖顺序

---

## 三、更新后的对比表格

| 维度 | 原方案 | 最终方案（修正后） |
|------|--------|-------------------|
| 架构层数 | 3 层 | 1 层 |
| 执行方式 | 嵌套串行 | **并行 + 依赖串行** |
| 反思触发 | checkpoint 预标记 | **AI 自评 + 护栏兜底** |
| 反思上限 | 无 | **3 次/执行** |
| 重试策略 | 分散在各层 | **统一 2 次 + 降级** |
| 事件系统 | 3 套冲突 | **统一命名空间** |
| 上下文 | 不定形 dict | **TaskContext schema** |
| AI 调用/普通任务 | 1 | 1（无反思）/ 2（有反思） |
| 总调用上限 | 无 | **20 次** |

---

## 四、更新后的文件结构

```
backend/app/services/agent/
├── executor/
│   ├── __init__.py
│   ├── task_executor.py      # TaskExecutor
│   └── models.py             # TaskResult, SelfAssessment, ReviewResult, Issue
│
├── planning/
│   ├── __init__.py
│   ├── engine.py             # PlanningEngine（带护栏 + 并行）
│   ├── reflection.py         # 反思逻辑
│   ├── dependency.py         # 依赖图 + 拓扑排序
│   └── config.py             # ExecutionConfig
│
├── context/
│   ├── __init__.py
│   └── task_context.py       # TaskContext schema
│
├── events/
│   ├── __init__.py
│   ├── schema.py             # EVENT_SCHEMA, TaskEvent
│   └── emitter.py            # 事件发送
│
└── langgraph_agent.py        # 入口
```

---

## 五、更新后的实施步骤

### 第一步：基础设施（优先）

1. 定义 `TaskContext` schema
2. 定义 `EVENT_SCHEMA` 和 `TaskEvent`
3. 定义 `ExecutionConfig` 护栏配置
4. 定义 `ReviewResult`, `Issue` 等数据结构

### 第二步：核心执行引擎

1. 实现 `TaskExecutor`（带自评）
2. 实现 `PlanningEngine`（带护栏 + 并行）
3. 实现依赖图和拓扑排序

### 第三步：集成与迁移

1. 集成到 `langgraph_agent.py`
2. 前端事件兼容映射
3. 删除旧的 `deep_agent/`

### 第四步：测试与验证

1. 单元测试：JSON 解析、自评构造
2. 集成测试：并行执行、护栏触发
3. 端到端测试：完整计划执行

---

*修正时间: 2025-12-10*