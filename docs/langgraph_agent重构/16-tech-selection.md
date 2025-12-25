# 技术选型分析

## 文档版本
- 版本：1.0
- 日期：2025-12-23
- 类型：技术分析

---

## 一、分析背景

### 1.1 参考资料

本分析基于以下资料：
- 《Agent 架构的探索》- Deep Agent 理论文章
- `02-deep-agents-concepts.md` - Deep Agents 框架概念
- LangGraph 官方文档
- 项目现有代码分析

### 1.2 分析目的

评估各种技术方案的适用性，为实施决策提供依据。

---

## 二、Deep Agents vs LangGraph 原生

### 2.1 Deep Agents 框架

**官方描述**:
> Deep Agents (deepagents 库) 是 LangChain 团队推出的用于构建深度代理的框架。

**核心功能**:
- Sub-agents 管理
- 上下文压缩
- 规划工具（write_todos）
- 文件系统集成

### 2.2 关键发现

通过分析 `02-deep-agents-concepts.md` 中的 API 验证代码：

```python
# 验证代码
from deepagents import create_deep_agent
from langgraph.types import interrupt, Command  # ← 关键发现

# interrupt 和 Command 来自 langgraph.types，不是 deepagents
```

**结论**: `interrupt()` 和 `Command(resume=...)` 是 **LangGraph 原生功能**，不需要 deepagents 库。

### 2.3 对比分析

| 功能 | deepagents | LangGraph 原生 |
|------|-----------|---------------|
| interrupt/resume | ✅ 封装 | ✅ 原生支持 |
| Sub-agents | ✅ 内置 | ⚠️ 需自行实现 |
| 上下文压缩 | ✅ 内置 | ⚠️ 需自行实现 |
| 规划工具 | ✅ write_todos | ⚠️ 需自行实现 |
| 学习成本 | 高 | 低 |
| 依赖复杂度 | 高 | 低 |

### 2.4 选型结论

| 场景 | 推荐 |
|------|------|
| 只需 interrupt/resume | **LangGraph 原生** |
| 需要完整 Deep Agent 能力 | deepagents |
| 本项目 | **LangGraph 原生** |

**理由**: 本项目核心需求是 HITL + 任务调整，只需 interrupt 机制，无需引入完整框架。

---

## 三、Skills 实现方案对比

### 3.1 方案 A: 新建 Skills 文件系统

**来源**: `09-skills-mechanism.md`

**结构**:
```
skills/
├── __init__.py
├── loader.py           # SkillLoader 类
├── writing/
│   ├── SKILL.md        # 核心文件
│   ├── continue.md     # 附加资源
│   └── polish.md
└── planning/
    ├── SKILL.md
    └── outline.md
```

**三级加载**:
1. 元数据（始终加载）
2. SKILL.md 正文（按需）
3. 附加资源（仅在需要时）

**优点**:
- 符合 Anthropic Skills 设计理念
- 高度模块化
- 易于分享复用

**缺点**:
- 新建大量文件
- 与现有 PromptManager 重复
- 维护两套系统

### 3.2 方案 B: 增强 PromptManager

**来源**: 本次讨论提出

**改动**:
```yaml
# YAML 添加字段
triggers:
  - 续写
  - 写作
summary: |
  **writing**: 小说写作能力...
```

```python
# PromptManager 添加方法
def get_all_summaries(self) -> str
def detect_template(self, message) -> Optional[str]
def render_with_detection(self, message, base_prompt) -> str
```

**两级加载**:
1. 摘要（始终加载）
2. 完整模板（按需）

**优点**:
- 复用现有系统
- 改动量小（~50 行）
- 向后兼容

**缺点**:
- 没有三级加载
- 附加资源需放在同一 YAML

### 3.3 选型对比

| 对比项 | 方案 A | 方案 B |
|--------|--------|--------|
| 工期 | 1.5 天 | 0.5 天 |
| 新文件数 | 15+ | 0 |
| 代码行数 | ~300 新增 | ~50 改动 |
| 维护系统 | 2 套 | 1 套 |
| 功能完整性 | 三级 | 两级 |
| 适用规模 | 10+ skills | 5-6 skills |

### 3.4 选型结论

**推荐方案 B（增强 PromptManager）**

**理由**:
1. 项目当前只有 5-6 个技能，两级加载足够
2. 避免维护两套系统
3. 工期节省 1 天
4. 后续如需扩展，可再迁移到方案 A

---

## 四、HITL 实现方案对比

### 4.1 方案 A: Redis 轮询（现有）

**代码**:
```python
async def wait_for_approval(self, request_id, check_interval=5):
    while True:
        result = await redis.get(f"approval:{request_id}")
        if result:
            return result
        await asyncio.sleep(check_interval)
```

**优点**:
- 已实现
- 跨进程/跨服务可用

**缺点**:
- 延迟高（2-5秒）
- 资源浪费（持续轮询）
- 代码复杂

### 4.2 方案 B: LangGraph interrupt（推荐）

**代码**:
```python
from langgraph.types import interrupt, Command

def task_node(state):
    response = interrupt({
        "type": "confirmation",
        "message": "确认执行？"
    })
    return {"confirmed": response == "确认"}

# 恢复
result = await agent.ainvoke(
    None,
    command=Command(resume="确认")
)
```

**优点**:
- 延迟低（<100ms）
- 事件驱动
- 代码简洁
- 框架原生支持

**缺点**:
- 需要改造现有流程
- 依赖 thread_id 持久化

### 4.3 选型对比

| 对比项 | Redis 轮询 | LangGraph interrupt |
|--------|-----------|---------------------|
| 延迟 | 2-5 秒 | < 100ms |
| 资源消耗 | 高 | 低 |
| 代码复杂度 | 高 | 低 |
| 改造成本 | 0（已有） | 中 |

### 4.4 选型结论

**推荐 LangGraph interrupt**

**理由**:
1. 用户体验提升明显
2. 代码更简洁
3. 符合框架设计理念
4. 长期维护成本低

---

## 五、中断类型设计

### 5.1 参考设计（06-interrupt-resume.md）

原规划 5 种类型：
1. confirmation - 确认型
2. select - 选择型
3. select_version - 版本选择
4. text_input - 输入型
5. progress_control - 进度控制

### 5.2 简化设计（推荐）

第一阶段只实现 2 种：

**confirmation**:
```typescript
{
  type: "confirmation",
  message: "确认执行此操作？",
  options: ["确认", "取消"],
  severity?: "normal" | "warning"
}
```

**task_confirmation**:
```typescript
{
  type: "task_confirmation",
  message: "即将执行以下任务",
  current_task: Task,
  remaining_tasks: Task[],
  options: ["执行", "跳过", "修改列表", "停止"]
}
```

### 5.3 对比

| 类型 | 用途 | 第一阶段 |
|------|------|----------|
| confirmation | 简单确认 | ✅ 实现 |
| task_confirmation | 任务确认 | ✅ 实现 |
| select_version | 改写选版本 | ❌ 延后 |
| text_input | 用户输入 | ❌ 延后 |
| progress_control | 进度控制 | ❌ task_confirmation 已覆盖 |

### 5.4 选型结论

**第一阶段 2 种类型**，后续按需扩展。

**理由**:
- MVP 原则
- 减少前端工作量
- 核心功能已覆盖

---

## 六、前后端通信方案

### 6.1 方案 A: WebSocket

**优点**:
- 双向通信
- 实时性好

**缺点**:
- 需要新建连接
- 服务端状态管理复杂
- 与现有 SSE 架构不一致

### 6.2 方案 B: SSE + REST（推荐）

**SSE（下行）**:
```typescript
// 中断事件
{ type: "interrupt", data: { ... } }

// 内容事件
{ type: "content", data: { ... } }
```

**REST（上行）**:
```typescript
POST /api/v1/agent/resume
{ thread_id, interrupt_id, response }
```

**优点**:
- 复用现有 SSE 架构
- 实现简单
- 与现有 API 一致

**缺点**:
- 非完全双向

### 6.3 选型结论

**推荐 SSE + REST**

**理由**:
1. 复用现有基础设施
2. 改动量最小
3. 够用（中断响应频率低）

---

## 七、状态持久化方案

### 7.1 现有方案

项目已有 `AsyncRedisSaver` 作为 checkpointer：

```python
from langgraph.checkpoint.aio import AsyncRedisSaver

checkpointer = AsyncRedisSaver(redis_client)
agent = create_agent(checkpointer=checkpointer)
```

### 7.2 interrupt 状态

interrupt 发生时，LangGraph 自动将状态保存到 checkpointer。恢复时通过 `thread_id` 定位。

### 7.3 选型结论

**复用现有 AsyncRedisSaver**，无需额外方案。

---

## 八、综合选型结果

| 技术点 | 选择 | 理由 |
|--------|------|------|
| Agent 框架 | LangGraph 原生 | interrupt 是原生功能 |
| Skills 方案 | PromptManager 增强 | 复用现有系统 |
| HITL 方案 | LangGraph interrupt | 延迟低、代码简洁 |
| 中断类型 | 2 种（confirmation, task_confirmation） | MVP 原则 |
| 通信方案 | SSE + REST | 复用现有架构 |
| 状态持久化 | AsyncRedisSaver | 复用现有 |

---

## 九、参考：《Agent 架构的探索》技术要点

### 9.1 四大支柱

| 支柱 | 本项目采用 | 说明 |
|------|-----------|------|
| Planning | ✅ 部分 | 已有任务规划，添加确认机制 |
| Sub-Agents | ❌ 暂不 | 当前场景不需要 |
| File System | ❌ 暂不 | 已有 UnifiedMemoryCoordinator |
| System Prompt | ✅ 采用 | PromptManager 增强 |

### 9.2 分层工具调用

| 层级 | 本项目采用 | 说明 |
|------|-----------|------|
| 原子层 | ✅ 采用 | 现有 20+ 工具 |
| 沙箱工具层 | ❌ 不采用 | 场景不匹配 |
| 代码/包层 | ❌ 不采用 | 非通用 Agent |

### 9.3 关键观点

> "Skills 本质上是一个多层级的文件系统，让 Agent 可以动态地发现和加载"

**本项目应用**: PromptManager 增强实现两级加载，符合核心理念，简化实现。

> "渐进式披露是使 Agent Skills 灵活和可扩展的核心设计原则"

**本项目应用**: YAML 添加 triggers + summary，实现按需加载。

---

**文档结束**
