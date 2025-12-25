# 简化实施方案

## 文档版本
- 版本：2.0
- 日期：2025-12-24
- 类型：实施方案
- 状态：📋 部分完成

---

## 一、方案概述

### 1.1 目标

基于过度设计评估结论，制定简化的实施方案，实现三个核心需求：

1. **Human-in-the-loop** - 人机交互确认
2. **实时任务调整** - 执行过程中可修改任务
3. **渐进式知识披露** - 按需加载提示词

### 1.2 当前进度

| 阶段 | 内容 | 状态 |
|------|------|------|
| 代码拆分 | langgraph_agent.py 模块化 | ✅ 已完成 |
| 执行轨迹可视化 | UI 展示 AI 思考过程 | 🔥 下一步 |
| interrupt 人机交互 | 任务确认/跳过/修改 | 📋 待实施 |
| 渐进式知识披露 | PromptManager 增强 | ⚠️ 需验证 |

### 1.3 与原方案对比

| 对比项 | 原方案 (07-implementation-plan.md) | 简化方案 |
|--------|-----------------------------------|----------|
| 工期 | 15 天 | 6-7 天 |
| 依赖 | deepagents 库 | 0 新依赖 |
| Skills | 新建文件系统 | 增强 PromptManager |
| 复杂度 | 完整框架迁移 | 最小改动 |

---

## 二、技术方案

### 2.1 Human-in-the-loop

#### 2.1.1 核心思路

使用 LangGraph 原生 `interrupt()` 和 `Command(resume=...)`，无需 deepagents 库。

#### 2.1.2 关键代码

```python
# 来自 langgraph.types，不是 deepagents
from langgraph.types import interrupt, Command

# 在需要用户确认的节点中
def task_execution_node(state):
    task = state["current_task"]

    # 发起中断，等待用户确认
    response = interrupt({
        "type": "confirmation",
        "message": f"即将执行任务: {task.name}",
        "options": ["执行", "跳过", "修改"]
    })

    if response == "跳过":
        return {"task_skipped": True}
    elif response == "修改":
        return {"need_modification": True}
    else:
        return {"task_confirmed": True}

# 恢复执行
result = await agent.ainvoke(
    None,
    config={"configurable": {"thread_id": thread_id}},
    command=Command(resume="执行")
)
```

#### 2.1.3 改造点

| 文件 | 改动 |
|------|------|
| `langgraph_agent.py` | 在 `_execute_task` 方法前添加 interrupt |
| `deep_agent/executor.py` | 在任务循环中添加中断点 |
| `api/v1/agent.py` | 添加 `/resume` 端点 |

---

### 2.2 实时任务调整

#### 2.2.1 核心思路

在 DeepAgentExecutor 的任务循环中添加中断点，允许用户在每个任务执行前确认或修改任务列表。

#### 2.2.2 改造前后对比

**改造前**（只能任务完成后反思）：
```python
class DeepAgentExecutor:
    async def execute_with_reflection(self, tasks):
        for task in tasks:
            await self._execute_task(task)  # 直接执行

        # 只在完成后反思
        reflection = await self._reflect_on_results()
```

**改造后**（每个任务前可确认）：
```python
class DeepAgentExecutor:
    async def execute_with_confirmation(self, tasks):
        remaining_tasks = tasks.copy()

        while remaining_tasks:
            task = remaining_tasks[0]

            # 中断点：确认当前任务
            response = interrupt({
                "type": "task_confirmation",
                "current_task": task,
                "remaining_tasks": remaining_tasks,
                "options": ["执行", "跳过", "修改列表", "停止"]
            })

            if response == "跳过":
                remaining_tasks.pop(0)
                continue
            elif response == "修改列表":
                # 用户可以重新排列或删除任务
                remaining_tasks = response.get("new_tasks", remaining_tasks)
                continue
            elif response == "停止":
                break

            # 执行任务
            await self._execute_task(task)
            remaining_tasks.pop(0)
```

---

### 2.3 渐进式知识披露

#### 2.3.1 核心思路

**不新建 Skills 文件系统**，而是增强现有 PromptManager：

1. YAML 模板添加 `triggers` 和 `summary` 字段
2. PromptManager 添加检测和渐进加载方法

#### 2.3.2 YAML 格式改动

```yaml
# templates/writing_agent.yaml

# 新增字段
triggers:
  - 续写
  - 写作
  - 改写
  - 润色
summary: |
  **writing**: 小说写作能力，支持续写、改写、润色等创作操作

# 原有字段保持不变
version: "1.0"
description: "写作助手核心提示词"
template: |
  你是文枢AI，专业的小说写作助手...
```

#### 2.3.3 PromptManager 改动

```python
class PromptManager:
    def __init__(self, ...):
        self.summaries: Dict[str, str] = {}
        self.triggers: Dict[str, List[str]] = {}
        self._load_metadata()

    def _load_metadata(self):
        """加载所有模板的 triggers 和 summary（第一级）"""
        for name, template in self.templates.items():
            if hasattr(template, 'triggers'):
                self.triggers[name] = template.triggers
            if hasattr(template, 'summary'):
                self.summaries[name] = template.summary

    def get_all_summaries(self) -> str:
        """获取所有模板摘要（始终加载到 System Prompt）"""
        lines = ["## 可用能力\n"]
        for name, summary in self.summaries.items():
            if summary:
                lines.append(f"- {summary}")
        return "\n".join(lines)

    def detect_template(self, message: str) -> Optional[str]:
        """根据用户消息检测需要加载的模板"""
        message_lower = message.lower()
        for name, trigger_list in self.triggers.items():
            for trigger in trigger_list:
                if trigger.lower() in message_lower:
                    return name
        return None

    def render_with_detection(self, message: str, base_prompt: str = "", **kwargs) -> str:
        """智能渲染：基础提示 + 检测到的模板"""
        result = base_prompt + "\n" + self.get_all_summaries()

        template_name = self.detect_template(message)
        if template_name:
            template_content = self.render(template_name, **kwargs)
            result += f"\n\n## 当前技能\n{template_content}"

        return result
```

---

## 三、实施计划

### 3.0 代码拆分（已完成）✅

**执行日期**: 2025-12-23 ~ 2025-12-24

**成果**:
- langgraph_agent.py: 5703 → 3272 行（-43%）
- 新增 14 个模块

**模块结构**:
```
backend/app/services/agent/
├── intent/classifier.py        # IntentClassifier
├── handlers/base.py            # 场景处理函数
├── execution/
│   ├── tool_executor.py        # ToolExecutor
│   └── parallel_executor.py    # ParallelExecutor
├── stream/
│   ├── event_parser.py         # EventParser
│   └── stream_event_handler.py # StreamEventHandler
├── planning/
│   ├── response_builder.py     # ResponseBuilder
│   ├── plan_generator.py       # PlanGenerator
│   └── quick_path.py           # QuickPathHandler
├── core/
│   ├── message_builder.py      # MessageBuilder
│   ├── tool_dispatcher.py      # ToolDispatcher
│   └── message_cleaner.py      # MessageCleaner
└── utils/tool_helpers.py       # 工具辅助函数
```

详见 [simple-refactor-plan.md](./simple-refactor-plan.md)

---

### 3.1 Phase 1: 执行轨迹可视化（3天）🔥 优先

详见 [17-execution-trace-visualization.md](./17-execution-trace-visualization.md)

#### Day 1: 后端准备
- [ ] Prompt 添加"先说再做"引导
- [ ] 实现 `format_tool_display()` 函数
- [ ] SSE 事件增加 text/tool 类型
- [ ] 对接现有 `stream/event_parser.py`

#### Day 2: 前端核心
- [ ] 创建 ExecutionFlow 组件
- [ ] 创建 StepItem/TextBlock/ToolCard 组件
- [ ] 创建 TaskList/TaskItem 组件
- [ ] 实现布局（上滚动 + 下固定）

#### Day 3: 联调优化
- [ ] 端到端测试
- [ ] 样式调整
- [ ] Bug 修复

---

### 3.2 Phase 2: interrupt 人机交互（2-3天）

- [ ] 在 `langgraph_agent.py` 的 `_execute_task` 方法前添加 interrupt
- [ ] 修改 `DeepAgentExecutor.execute_with_reflection` 为 `execute_with_confirmation`
- [ ] 在任务循环中添加中断点
- [ ] 处理用户响应（执行/跳过/修改/停止）
- [ ] 添加 `/api/v1/agent/resume` 端点
- [ ] 前端 InterruptDialog 组件
- [ ] SSE 事件处理

---

### 3.3 Phase 3: 渐进式知识披露（可选，0.5-1天）

⚠️ **注意**: 此功能需先验证必要性，详见 [14-prompt-manager-enhancement.md](./14-prompt-manager-enhancement.md)

**验证点**:
- `detect_template()` 是否与 IntentClassifier 功能重叠
- 两级加载的实际 token 节省量

如确认需要:
- [ ] 修改 YAML 模板格式（添加 triggers, summary）
- [ ] PromptManager 添加渐进加载方法

---

## 四、文件变更清单

### 4.1 已完成 ✅

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `services/agent/intent/` | 新增 | IntentClassifier 模块 |
| `services/agent/handlers/` | 新增 | 场景处理模块 |
| `services/agent/execution/` | 新增 | 工具执行模块 |
| `services/agent/stream/` | 新增 | 流式处理模块 |
| `services/agent/planning/` | 新增 | 规划执行模块 |
| `services/agent/core/` | 新增 | 核心工具链模块 |
| `services/agent/utils/` | 新增 | 工具辅助函数 |
| `services/agent/langgraph_agent.py` | 修改 | 主文件精简 |

### 4.2 待完成

| 文件 | 变更类型 | 说明 |
|------|----------|------|
| `prompts/templates/*.yaml` | 修改 | 添加"先说再做"引导 |
| `services/agent/stream/event_parser.py` | 修改 | 增加 text/tool 事件类型 |
| `api/v1/agent.py` | 修改 | 添加 /resume 端点 |
| `components/agent/ExecutionFlow.tsx` | 新增 | 执行轨迹容器组件 |
| `components/agent/ToolCard.tsx` | 新增 | 工具调用卡片组件 |
| `components/agent/InterruptDialog.tsx` | 新增 | 中断对话框 |

---

## 五、验收标准

### 5.1 已完成 ✅

- [x] langgraph_agent.py 行数 < 3500 行（实际 3272 行）
- [x] 代码模块化，职责清晰
- [x] 无新增依赖
- [x] API 接口不变

### 5.2 Phase 1 验收（执行轨迹可视化）

- [ ] AI 说明文字实时显示
- [ ] 工具调用显示为卡片样式
- [ ] 思考、工具、内容按时间顺序交织显示
- [ ] 任务列表固定底部，完成的任务划掉

### 5.3 Phase 2 验收（interrupt 人机交互）

- [ ] 任务执行前弹出确认对话框
- [ ] 用户可以跳过某个任务
- [ ] 用户可以修改任务列表顺序
- [ ] 用户可以随时停止执行
- [ ] interrupt 响应延迟 < 100ms

### 5.4 Phase 3 验收（渐进式知识披露，可选）

- [ ] 用户发送"帮我续写一段"时，自动加载 writing 模板
- [ ] System Prompt 只包含摘要（~500 tokens），详细模板按需加载

---

## 六、风险与回滚

### 6.1 风险

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| interrupt 与现有流程冲突 | 中 | 中 | 可配置开关，默认关闭 |
| YAML 格式变更导致解析错误 | 低 | 高 | 向后兼容，新字段可选 |
| 前端适配工作量超预期 | 中 | 中 | 先实现最小化 UI |

### 6.2 回滚方案

每个阶段前备份关键文件：

```bash
# Day 1 前
cp prompt_manager.py prompt_manager.py.backup_day1

# Day 2 前
cp langgraph_agent.py langgraph_agent.py.backup_day2
cp executor.py executor.py.backup_day2
```

---

## 七、后续扩展

本方案只实现核心需求，以下功能可后续按需添加：

1. **更复杂的中断类型** - 多选、输入框
2. **中断超时处理** - 用户长时间不响应
3. **中断历史记录** - 用于审计
4. **更多模板触发规则** - 正则、语义匹配

---

**文档结束**
