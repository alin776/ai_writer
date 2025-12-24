# 迁移策略 - 整体规划

## 文档版本
- 版本：1.1
- 日期：2025-12-19
- 更新：修正工具数量，更新中间件命名

---

## 一、迁移原则

### 1.1 核心原则

| 原则 | 说明 |
|------|------|
| **渐进式迁移** | 分阶段进行，每阶段可独立验证 |
| **保留业务价值** | 专业写作工具、三层记忆等核心功能必须保留 |
| **最小化风险** | 每步都有回滚方案 |
| **向后兼容** | API 接口保持兼容，前端无需大改 |

### 1.2 迁移范围

```
┌─────────────────────────────────────────────────────────┐
│                    迁移范围                              │
├─────────────────────────────────────────────────────────┤
│  🔄 替换                                                │
│  ├── langgraph_agent.py (5703行) → Deep Agents 核心    │
│  ├── deep_agent/executor.py → Deep Agents todos        │
│  └── hitl.py 轮询机制 → interrupt/resume              │
├─────────────────────────────────────────────────────────┤
│  ✅ 保留                                                │
│  ├── tools/*.py (14 专业写作工具)                     │
│  ├── memory/*.py (三层记忆系统)                        │
│  ├── model_selector.py (智能模型选择)                  │
│  ├── cost_tracker.py (成本追踪)                        │
│  └── context/*.py (上下文管理)                         │
├─────────────────────────────────────────────────────────┤
│  🔧 适配                                                │
│  ├── 工具接口适配 Deep Agents 工具格式                 │
│  ├── 记忆系统封装为自定义 AgentMiddleware              │
│  └── API 层适配新的调用方式                            │
└─────────────────────────────────────────────────────────┘
```

---

## 二、目标架构

### 2.1 新架构设计

```
┌─────────────────────────────────────────────────────────┐
│                   API Layer                             │
│                 api/v1/agent.py                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│              WritingAgent (新)                          │
│           基于 create_deep_agent                        │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │              配置层                              │   │
│  │  - system_prompt (写作助手提示)                  │   │
│  │  - model (通过 ModelSelector 选择)               │   │
│  │  - checkpointer (AsyncRedisSaver)               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                  AgentMiddleware Stack                  │
├─────────────┬─────────────┬─────────────┬──────────────┤
│  TodoList   │ Filesystem  │  SubAgent   │   Memory     │
│ (内置)      │ (内置)      │ (内置)      │  (自定义)    │
├─────────────┼─────────────┼─────────────┼──────────────┤
│   Model     │    Cost     │   Context   │   Intent     │
│  Selector   │  Tracker    │  Manager    │  Classifier  │
│  (自定义)   │  (自定义)   │  (自定义)   │  (自定义)    │
└─────────────┴─────────────┴─────────────┴──────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                  Tools Registry                         │
├─────────────────────────────────────────────────────────┤
│  写作工具                                               │
│  ├── continue_writing_tool                             │
│  ├── smart_rewrite                                     │
│  ├── smart_continue                                    │
│  └── smart_insert                                      │
├─────────────────────────────────────────────────────────┤
│  分析工具                                               │
│  ├── analyze_text_tool                                 │
│  ├── consistency_checker                               │
│  └── style_adapter                                     │
├─────────────────────────────────────────────────────────┤
│  数据工具                                               │
│  ├── read_chapter_tool                                 │
│  ├── get_chapter_by_order_tool                         │
│  └── get_context_tool                                  │
└─────────────────────────────────────────────────────────┘
```

### 2.2 文件结构规划

```
backend/app/services/agent/
├── __init__.py
├── writing_agent.py          # 新：Deep Agents 入口 (~300行)
│
├── middleware/               # 新：自定义 AgentMiddleware
│   ├── __init__.py
│   ├── memory_middleware.py  # 三层记忆集成
│   ├── model_middleware.py   # ModelSelector 集成
│   ├── cost_middleware.py    # 成本追踪集成
│   ├── context_middleware.py # 上下文管理集成
│   └── intent_middleware.py  # 意图分类集成
│
├── tools/                    # 保留：专业写作工具
│   ├── __init__.py
│   ├── writing_tools.py      # 适配 @tool 装饰器
│   ├── editor_tools.py
│   ├── analysis_tools.py
│   └── ...
│
├── memory/                   # 保留：三层记忆
│   └── ... (无需修改)
│
├── prompts/                  # 保留：提示词模板
│   └── ...
│
├── model_selector.py         # 保留：模型选择
├── cost_tracker.py           # 保留：成本追踪
│
└── legacy/                   # 废弃：旧代码归档
    ├── langgraph_agent.py    # 归档备份
    ├── deep_agent/           # 归档备份
    └── hitl.py               # 归档备份
```

---

## 三、迁移映射

### 3.1 功能映射表

| 现有功能 | 现有实现 | 迁移目标 |
|----------|----------|----------|
| Agent 入口 | `WritingAgentGraph.__init__` | `create_deep_agent()` |
| 图构建 | `_build_graph()` | Deep Agents 内部处理 |
| 意图分类 | `_classify_intent*()` | `IntentMiddleware` |
| 工具调用 | `_call_tool_via_registry()` | Deep Agents 工具系统 |
| 反思机制 | `DeepAgentExecutor` | Deep Agents `write_todos` |
| HITL | `HITLManager` 轮询 | `interrupt/resume` |
| 流式处理 | `chat_stream()` | `agent.astream()` |
| 规划执行 | `chat_with_planning()` | Deep Agents 自动规划 |

### 3.2 API 映射表

| 现有 API | 新 API |
|----------|--------|
| `agent.chat_stream(message, ...)` | `agent.astream({"messages": [...]})` |
| `agent.chat_with_planning(message, ...)` | `agent.invoke({"messages": [...]})` |
| `HITLManager.wait_for_approval()` | `interrupt()` + `Command(resume=)` |

### 3.3 状态映射表

| 现有状态字段 | Deep Agents 对应 |
|--------------|------------------|
| `messages` | `state["messages"]` |
| `work_id` | `config["configurable"]["work_id"]` |
| `chapter_id` | `config["configurable"]["chapter_id"]` |
| `intent` | `state["intent"]` (自定义) |
| `context` | `LangGraph Store API` |

---

## 四、迁移阶段

### 4.1 阶段概览

```
Phase 1: 准备工作 (2天)
    ↓
Phase 2: 工具迁移 (3天)
    ↓
Phase 3: 中间件开发 (4天)
    ↓
Phase 4: 核心替换 (3天)
    ↓
Phase 5: 集成测试 (2天)
    ↓
Phase 6: 上线切换 (1天)

总计: 约 15 天
```

### 4.2 Phase 1: 准备工作

**目标：** 环境准备，不影响现有功能

**任务：**
1. 安装 deepagents 依赖
2. 创建新目录结构
3. 编写基础测试用例
4. 备份现有代码

**验收标准：**
- [ ] `pip install deepagents` 成功
- [ ] 新目录结构创建完成
- [ ] 基础测试框架就绪

### 4.3 Phase 2: 工具迁移

**目标：** 将现有工具适配到 Deep Agents 格式

**任务：**
1. 整理 14 工具为统一格式
2. 移除对全局变量的依赖，使用依赖注入
3. 调整返回格式
4. 编写工具测试

**验收标准：**
- [ ] 14 工具全部适配完成
- [ ] 工具单元测试通过
- [ ] 工具在 Deep Agents 中可正常调用

### 4.4 Phase 3: AgentMiddleware 开发

**目标：** 将核心功能封装为 AgentMiddleware

**任务：**
1. `MemoryMiddleware` - 三层记忆
2. `ModelMiddleware` - 模型选择
3. `CostMiddleware` - 成本追踪
4. `ContextMiddleware` - 上下文管理
5. `IntentMiddleware` - 意图分类

**验收标准：**
- [ ] 所有 AgentMiddleware 开发完成
- [ ] 单元测试通过
- [ ] AgentMiddleware 可正确注入到 Agent

### 4.5 Phase 4: 核心替换

**目标：** 用 Deep Agents 替换 langgraph_agent.py

**任务：**
1. 创建 `WritingAgent` 类
2. 集成所有中间件
3. 实现 interrupt/resume 流程
4. 适配 API 层

**验收标准：**
- [ ] `WritingAgent` 可正常创建
- [ ] 基本对话流程通过
- [ ] interrupt/resume 测试通过

### 4.6 Phase 5: 集成测试

**目标：** 全面测试新系统

**任务：**
1. 端到端测试
2. 性能测试
3. 压力测试
4. 回归测试

**验收标准：**
- [ ] 所有测试用例通过
- [ ] 性能不低于现有系统
- [ ] 无严重 bug

### 4.7 Phase 6: 上线切换

**目标：** 平滑切换到新系统

**任务：**
1. 灰度发布
2. 监控告警
3. 回滚预案执行（如需要）
4. 旧代码归档

**验收标准：**
- [ ] 灰度发布成功
- [ ] 线上运行稳定
- [ ] 用户无感知

---

## 五、并行开发策略

### 5.1 双轨运行

在迁移期间，新旧系统并行运行：

```python
# api/v1/agent.py

async def chat(request: ChatRequest):
    # 功能开关
    if settings.USE_DEEP_AGENTS:
        # 新系统
        return await new_writing_agent.chat(request)
    else:
        # 旧系统
        return await old_writing_agent.chat(request)
```

### 5.2 灰度发布

```python
# 按用户 ID 灰度
def should_use_new_agent(user_id: str) -> bool:
    # 10% 用户使用新系统
    return hash(user_id) % 100 < 10
```

---

## 六、风险控制

### 6.1 回滚策略

每个阶段都有独立的回滚点：

| 阶段 | 回滚方式 |
|------|----------|
| Phase 1-2 | 删除新代码，无影响 |
| Phase 3 | 不启用中间件 |
| Phase 4-5 | 切换功能开关 |
| Phase 6 | 立即切换功能开关 |

### 6.2 监控指标

| 指标 | 阈值 | 触发动作 |
|------|------|----------|
| 错误率 | > 1% | 告警 |
| 错误率 | > 5% | 自动回滚 |
| 响应时间 | > 10s | 告警 |
| Token 消耗 | > 120% 基线 | 告警 |

---

## 七、依赖管理

### 7.1 新增依赖

```txt
# requirements.txt 新增
deepagents>=1.0.0
```

### 7.2 依赖兼容性

| 依赖 | 现有版本 | 要求版本 | 兼容性 |
|------|----------|----------|--------|
| langgraph | 1.0.1 | ≥1.0.0 | ✅ 兼容 |
| langchain | 1.0.2 | ≥1.0.0 | ✅ 兼容 |
| redis | 7+ | 7+ | ✅ 兼容 |

---

## 八、下一步

- 阅读 `04-tools-migration.md` 了解工具迁移详细方案
- 阅读 `05-memory-integration.md` 了解记忆系统集成方案
- 阅读 `06-interrupt-resume.md` 了解中断恢复机制实现
