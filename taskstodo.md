# Multi-Agent 架构实施任务清单

> 开始日期: 2025-12-06
> 完成日期: 2025-12-06
> 状态: ✅ 已完成

---

## 阶段1: 准备工作（移除 ReAct）✅

- [x] 1.1 前端：修改 `AgentChatPanel.tsx` 默认模式为 'planning'
- [x] 1.2 前端：移除 `ModeSelector.tsx` 中的 ReAct 选项
- [x] 1.3 前端：清理 `useAgentChatStream.ts` 中的 ReAct 相关代码
- [x] 1.4 后端：保持兼容（默认已是 Planning）
- [x] 1.5 测试 Planning 模式正常工作

---

## 阶段2: 创建目录结构 ✅

- [x] 2.1 创建 `backend/app/services/agent/multi_agent/` 目录
- [x] 2.2 创建 `multi_agent/agents/` 子目录
- [x] 2.3 创建 `multi_agent/prompts/` 子目录
- [x] 2.4 创建所有 `__init__.py` 文件

---

## 阶段3: 实现核心 Agent ✅

- [x] 3.1 实现 `base_agent.py` - Agent 基类
- [x] 3.2 实现 `outline_agent.py` - 大纲师
- [x] 3.3 实现 `writer_agent.py` - 主笔
- [x] 3.4 实现 `character_guard.py` - 角色守护
- [x] 3.5 实现 `logic_auditor.py` - 逻辑审计
- [x] 3.6 实现 `editor_agent.py` - 总编

---

## 阶段4: 实现 Prompt 模板 ✅

- [x] 4.1 创建 `outline_prompt.py` - 大纲师 Prompt
- [x] 4.2 创建 `writer_prompt.py` - 主笔 Prompt
- [x] 4.3 创建 `character_guard_prompt.py` - 角色守护 Prompt
- [x] 4.4 创建 `logic_auditor_prompt.py` - 逻辑审计 Prompt
- [x] 4.5 创建 `editor_prompt.py` - 总编 Prompt

---

## 阶段5: 实现执行器 ✅

- [x] 5.1 实现 `executor.py` - MultiAgentExecutor
- [x] 5.2 实现 `is_writing_task()` 判断逻辑
- [x] 5.3 实现进度事件回调

---

## 阶段6: 集成到 Planning 模式 ✅

- [x] 6.1 在 `langgraph_agent.py` 中导入 MultiAgentExecutor
- [x] 6.2 在 `_execute_task()` 中添加 Multi-Agent 判断
- [x] 6.3 当有足够上下文时自动使用 Multi-Agent

---

## 阶段7: 测试与调优

- [ ] 7.1 编写单元测试（待后续）
- [ ] 7.2 端到端测试（待后续）
- [ ] 7.3 Prompt 调优（待后续）

---

## Review 总结

### 完成的工作

1. **前端改动**
   - `AgentChatPanel.tsx`: 默认模式改为 'planning'
   - `ModeSelector.tsx`: 简化为只显示 Planning 模式
   - `useAgentChatStream.ts`: mode 改为 'planning'

2. **Multi-Agent 系统实现**
   - 目录结构: `backend/app/services/agent/multi_agent/`
   - 5 个核心 Agent: 大纲师、主笔、角色守护、逻辑审计、总编
   - 执行器: `MultiAgentExecutor` 串联所有 Agent

3. **集成方式**
   - 在 `langgraph_agent.py` 的 `_execute_task()` 中集成
   - 当任务是 `continue_writing_tool` 且有足够上下文时，自动使用 Multi-Agent
   - 否则回退到原有的单工具执行

### Multi-Agent 工作流程

```
大纲师 (OutlineAgent)
    ↓
主笔 (WriterAgent)
    ↓
角色守护 (CharacterGuard) ─┐
                           ├→ 并行执行
逻辑审计 (LogicAuditor) ───┘
    ↓
总编 (EditorAgent)  ← 如有问题则修订
    ↓
最终内容
```

### 文件清单

```
backend/app/services/agent/multi_agent/
├── __init__.py
├── executor.py           # MultiAgentExecutor
├── agents/
│   ├── __init__.py
│   ├── base_agent.py     # 基类
│   ├── outline_agent.py  # 大纲师
│   ├── writer_agent.py   # 主笔
│   ├── character_guard.py # 角色守护
│   ├── logic_auditor.py  # 逻辑审计
│   └── editor_agent.py   # 总编
└── prompts/
    ├── __init__.py
    ├── outline_prompt.py
    ├── writer_prompt.py
    ├── character_guard_prompt.py
    ├── logic_auditor_prompt.py
    └── editor_prompt.py
```

### 后续优化方向

1. 从 WorldviewService 获取角色设定
2. 从 VectorMemoryStore 获取前文摘要
3. 添加单元测试
4. Prompt 调优

---

## 深度 Review (2025-12-06)

### 发现的问题

| 优先级 | 问题 | 状态 |
|-------|------|------|
| **高** | on_event 回调未传递到 Multi-Agent | ✅ 已修复 |
| **中** | Prompt 缺少风格锚定指标 | ✅ 已修复 |
| **中** | 缺少超时和回退机制 | ✅ 已修复 |
| **中** | Multi-Agent 触发条件过窄：仅检查 character_document/total_outline，previous_summary/world_setting 仍会回退单 Agent | ✅ 已修复 |
| **中** | `is_writing_task` 未被使用，其他写作型工具无法触发 Multi-Agent | ✅ 已修复 |
| **低** | prompts/ 目录文件未被使用 | ✅ 已修复 |

### 修复内容

1. **on_event 回调传递** (`langgraph_agent.py`)
   - 创建 `on_multi_agent_event` 适配器函数
   - 将 Multi-Agent 事件转换为进度消息
   - 显示 5 个阶段的实时进度

2. **风格锚定指标** (`writer_agent.py`, `editor_agent.py`)
   - 添加硬性指标：句子长度≤20字、形容词≤5%
   - 添加禁用词：竟然、居然、没想到等
   - 添加对话占比要求：40%-50%
   - 添加裁决优先级：逻辑自洽 > 人设一致 > 风格一致

3. **超时和回退机制** (`executor.py`)
   - 添加各阶段超时配置（大纲30s、主笔120s、校验30s、总编60s）
   - 添加整体超时保护（300s）
   - 实现回退策略：
     - 大纲师失败 → 使用默认大纲模板
   - 角色守护/逻辑审计失败 → 跳过校验
   - 总编失败 → 使用初稿
   - 主笔失败 → 终止流程（核心步骤不可跳过）

4. **触发范围扩大 + 函数接入** (`langgraph_agent.py`)
   - 使用 `is_writing_task` 识别写作型任务（不仅限 `continue_writing_tool`）
   - 扩展上下文判定，`previous_summary`/`world_setting`/`previous_content` 也能触发 Multi-Agent
   - 上下文不足时仍回退单 Agent，保持兼容

5. **Prompt 与模板对齐** (`multi_agent/prompts/*`, 各 Agent)
   - 将内联系统提示迁移到共享模板，避免漂移
   - 模板包含风格锚定、裁决优先级及 JSON 输出规范

### 文件变更清单

```
修改文件：
backend/app/services/agent/langgraph_agent.py  # 添加 on_event 回调适配器；拓展 Multi-Agent 触发逻辑
backend/app/services/agent/multi_agent/executor.py  # 添加超时和回退机制
backend/app/services/agent/multi_agent/agents/writer_agent.py  # 添加风格锚定；使用共享模板
backend/app/services/agent/multi_agent/agents/editor_agent.py  # 添加裁决优先级；使用共享模板
backend/app/services/agent/multi_agent/agents/outline_agent.py  # 使用共享模板
backend/app/services/agent/multi_agent/agents/character_guard.py  # 使用共享模板
backend/app/services/agent/multi_agent/agents/logic_auditor.py  # 使用共享模板
backend/app/services/agent/multi_agent/prompts/*.py  # 对齐内联 Prompt 内容
```

---

## Deep Agents 深度研究报告 (2025-12-06)

> 项目地址: https://github.com/langchain-ai/deepagents

### 一、项目概述

**Deep Agents** 是 LangChain 官方发布的开源 Agent 框架，基于 LangGraph 构建。其设计灵感来自 Claude Code 和 Manus 等先进 Agent 应用的共同原则。

核心特点：
- **规划能力**: 任务执行前进行结构化规划
- **计算机访问**: 提供 Shell 和文件系统操作能力
- **子代理委派**: 隔离上下文的任务执行机制

### 二、核心架构：三大支柱

```
┌─────────────────────────────────────────────────────────────┐
│                    Deep Agent 架构                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Planning   │  │  Filesystem  │  │   SubAgent   │      │
│  │    规划层    │  │   文件系统   │  │   子代理层   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                │                  │               │
│         ▼                ▼                  ▼               │
│  ┌──────────────────────────────────────────────────┐      │
│  │              Middleware 中间件层                  │      │
│  │  TodoList | Filesystem | SubAgent | Summarization│      │
│  └──────────────────────────────────────────────────┘      │
│                          │                                  │
│                          ▼                                  │
│  ┌──────────────────────────────────────────────────┐      │
│  │              Backend 后端层                       │      │
│  │  StateBackend | FilesystemBackend | StoreBackend │      │
│  └──────────────────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 2.1 Planning (规划层)

**设计哲学**: Todo 工具本质上是个 "no-op"，其价值在于**上下文工程**而非功能执行。

**核心工具**:
- `write_todos`: 任务分解与进度跟踪
- `read_todos`: 读取当前任务状态

**工作方式**:
```python
# 规划工具让 Agent 保持专注
1. Plan: 用 write_todos 分解任务
2. Execute: 按计划执行各子任务
3. Adapt: 根据新信息调整计划
```

#### 2.2 Filesystem (文件系统层)

**核心问题**: 解决上下文窗口溢出

**工具集**:
| 工具 | 功能 |
|------|------|
| `ls` | 列出目录 |
| `read_file` | 读取文件 |
| `write_file` | 写入文件 |
| `edit_file` | 编辑文件 |
| `glob` | 模式匹配 |
| `grep` | 内容搜索 |
| `execute` | Shell 命令 |

**关键作用**:
- 将大量上下文卸载到文件系统
- 防止 Token 限制溢出
- 处理可变长度的工具结果

#### 2.3 SubAgent (子代理层)

**设计原理**: 上下文隔离 + 专业化分工

```python
research_subagent = {
    "name": "research-agent",
    "description": "专业研究员",
    "system_prompt": "你是一个专业研究员...",
    "tools": [tavily_search, think_tool],
    "model": "openai:gpt-4o"  # 可选指定模型
}

agent = create_deep_agent(subagents=[research_subagent])
```

### 三、内置中间件系统

| 中间件 | 功能 |
|--------|------|
| `TodoListMiddleware` | 结构化任务管理 |
| `FilesystemMiddleware` | 文件操作与上下文卸载 |
| `SubAgentMiddleware` | 隔离任务委派 |
| `SummarizationMiddleware` | 170k tokens 自动摘要 |
| `AnthropicPromptCachingMiddleware` | Anthropic 成本优化 |
| `HumanInTheLoopMiddleware` | 审批工作流控制 |

### 四、Deep Research Agent 实战案例

#### 4.1 架构图

```
┌────────────────────────────────────────────────────────┐
│                  Research Orchestrator                  │
│              (RESEARCH_WORKFLOW_INSTRUCTIONS)           │
├────────────────────────────────────────────────────────┤
│                                                        │
│   1. write_todos: 分解研究任务                          │
│   2. write_file: 保存研究请求到 /research_request.md    │
│   3. task(): 委派给子代理                               │
│                      │                                  │
│         ┌───────────┼───────────┐                      │
│         ▼           ▼           ▼                      │
│   ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│   │Research  │ │Research  │ │Research  │   最多3个并行 │
│   │SubAgent 1│ │SubAgent 2│ │SubAgent 3│              │
│   └──────────┘ └──────────┘ └──────────┘              │
│         │           │           │                      │
│         └───────────┼───────────┘                      │
│                     ▼                                  │
│   4. Synthesize: 整合发现，统一引用编号                  │
│   5. write_file: 写入 /final_report.md                 │
│   6. Verify: 检查是否回答所有问题                       │
│                                                        │
└────────────────────────────────────────────────────────┘
```

#### 4.2 核心代码实现

```python
# agent.py
from deepagents import create_deep_agent

# 配置限制
max_concurrent_research_units = 3  # 最大并行子代理数
max_researcher_iterations = 3       # 最大委派轮数

# 定义研究子代理
research_sub_agent = {
    "name": "research-agent",
    "description": "委派研究任务给子代理研究员",
    "system_prompt": RESEARCHER_INSTRUCTIONS.format(date=current_date),
    "tools": [tavily_search, think_tool],
}

# 创建深度代理
agent = create_deep_agent(
    model=model,
    tools=[tavily_search, think_tool],
    system_prompt=INSTRUCTIONS,
    subagents=[research_sub_agent],
)
```

#### 4.3 关键 Prompt 设计

**5步研究工作流** (`RESEARCH_WORKFLOW_INSTRUCTIONS`):
1. **Plan**: 用 `write_todos` 分解研究任务
2. **Save**: 保存请求到 `/research_request.md`
3. **Research**: 用 `task()` 委派给子代理（**必须**用子代理研究）
4. **Synthesize**: 整合发现，统一引用编号
5. **Write**: 写入 `/final_report.md`
6. **Verify**: 确认回答所有问题

**研究员指令** (`RESEARCHER_INSTRUCTIONS`):
- 工具调用预算: 简单查询2-3次，复杂查询最多5次
- 每次搜索后用 `think_tool` 反思
- 停止条件: 有3+相关来源 / 连续2次搜索相似结果

**子代理委派策略** (`SUBAGENT_DELEGATION_INSTRUCTIONS`):
```
默认: 1个子代理处理大多数查询
并行化条件:
- 明确的比较任务 → 每个对比元素1个子代理
- 地理/领域分离 → 每个方面1个子代理
限制: 最多3个并行，最多3轮委派
```

#### 4.4 think_tool 的精髓

```python
@tool
def think_tool(reflection: str) -> str:
    """研究进度的战略反思工具

    在每次搜索后使用，系统化分析结果并规划下一步:
    1. 我找到了什么关键信息？
    2. 还缺什么？
    3. 我能全面回答问题了吗？
    4. 应该继续搜索还是提供答案？
    """
    return f"Reflection recorded: {reflection}"
```

这是一个**纯上下文工程工具**，不执行实际操作，但迫使 Agent 在行动前思考。

### 五、与当前项目 Multi-Agent 的对比

| 维度 | Deep Agents | 当前项目 Multi-Agent |
|------|-------------|---------------------|
| **定位** | 通用 Agent 框架 | 小说写作专用 |
| **规划** | `write_todos` 工具 | 大纲师 Agent |
| **文件系统** | 内置 Middleware | 暂无 |
| **子代理** | 动态 `task()` 委派 | 固定流程串联 |
| **上下文管理** | 文件卸载 + 170k摘要 | 依赖 previous_summary |
| **流程** | 灵活委派 | 固定: 大纲→主笔→校验→总编 |

### 六、借鉴价值

#### 6.1 立即可借鉴

1. **think_tool 模式**: 在关键节点添加反思工具
   ```python
   # 可添加到 WriterAgent
   def think_about_draft(reflection: str) -> str:
       """写作前/后的反思"""
       return reflection
   ```

2. **文件系统卸载**: 将长内容存储到文件而非保持在上下文中
   ```python
   # 大纲 → 保存到文件
   write_file("/outline.md", outline_content)
   # 初稿 → 保存到文件
   write_file("/draft.md", draft_content)
   ```

3. **统一引用管理**: Research Agent 的引用编号机制可用于角色/世界观引用

#### 6.2 中期可借鉴

1. **动态子代理委派**:
   - 根据内容复杂度动态决定是否启用校验 Agent
   - 长篇内容启用并行章节处理

2. **SummarizationMiddleware**:
   - 当上下文超过阈值时自动摘要
   - 保护核心上下文（角色设定、大纲）

3. **Human-in-the-Loop**:
   - 大纲完成后人工确认
   - 争议性内容人工审核

#### 6.3 架构启示

```
现有架构:
大纲师 → 主笔 → 角色守护 → 逻辑审计 → 总编 (固定流程)

可演进为:
┌───────────────────────────────────────────────────┐
│              Writing Orchestrator                 │
│                                                   │
│  1. write_todos: 分析写作任务                      │
│  2. 判断复杂度:                                    │
│     - 简单续写 → 直接 WriterAgent                  │
│     - 复杂章节 → 大纲师 + 主笔                      │
│     - 重要情节 → 完整流程 + 校验                   │
│  3. task(): 动态委派                               │
│  4. 整合输出                                       │
└───────────────────────────────────────────────────┘
```

### 七、总结

Deep Agents 的核心洞见:

1. **规划工具是上下文工程**: 让 Agent 在行动前思考
2. **文件系统是扩展记忆**: 突破上下文限制
3. **子代理是上下文隔离**: 保持主 Agent 清晰
4. **反思工具是质量保证**: 强制 Agent 评估进度

这些原则与当前项目的 Multi-Agent 架构高度互补，可逐步整合以提升写作质量。

### 八、参考资料

- [Deep Agents GitHub](https://github.com/langchain-ai/deepagents)
- [Deep Agents Quickstarts](https://github.com/langchain-ai/deepagents-quickstarts)
- [Deep Agents 官方文档](https://docs.langchain.com/oss/python/deepagents/overview)
- [LangChain Blog: Deep Agents](https://blog.langchain.com/deep-agents/)
- [Dev.to 实战指南](https://dev.to/samadhi_patil_294a4ff7fea/building-advanced-ai-agents-with-langchains-deepagents-a-hands-on-guide-1bk4)
