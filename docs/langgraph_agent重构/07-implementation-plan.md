# 实施计划 - 分阶段

## 文档版本
- 版本：1.1
- 日期：2025-12-19
- 更新：更新工具数量统计

---

## 一、总体时间线

```
┌─────────────────────────────────────────────────────────────────┐
│                        总工期：15 天                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Week 1                          Week 2                   Week 3│
│  ├─ Phase 1: 准备 (2d)          ├─ Phase 4: 核心 (3d)    ├─ P6 │
│  ├─ Phase 2: 工具 (3d)          ├─ Phase 5: 测试 (2d)    │     │
│  └─ Phase 3: 中间件 (2d)        └─ Phase 3 续 (2d)       │     │
│                                                                 │
│  Day: 1  2  3  4  5  6  7  8  9  10 11 12 13 14 15             │
│       ├──P1──┤├────P2────┤├────P3────┤├───P4───┤├─P5─┤├P6┤     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、Phase 1: 准备工作 (Day 1-2)

### 2.1 目标

- 环境准备
- 目录结构创建
- 测试框架搭建
- 代码备份

### 2.2 任务清单

#### Day 1

| 任务 | 预计时间 | 负责人 | 验收标准 |
|------|----------|--------|----------|
| 安装 deepagents 依赖 | 0.5h | - | `pip install deepagents` 成功 |
| 创建新目录结构 | 0.5h | - | 目录结构符合设计 |
| 备份现有代码 | 0.5h | - | `legacy/` 目录包含所有旧代码 |
| 编写基础测试框架 | 2h | - | pytest 配置完成 |
| 创建功能开关配置 | 1h | - | `USE_DEEP_AGENTS` 配置项 |

#### Day 2

| 任务 | 预计时间 | 负责人 | 验收标准 |
|------|----------|--------|----------|
| Deep Agents 基础 Demo | 2h | - | 能创建并运行简单 Agent |
| 确认依赖兼容性 | 1h | - | 所有依赖版本兼容 |
| 编写迁移脚本框架 | 1h | - | 脚本可执行 |
| 文档更新 | 1h | - | README 更新 |

### 2.3 交付物

```
backend/app/services/agent/
├── __init__.py              # 更新导出
├── middleware/              # 新建
│   └── __init__.py
├── legacy/                  # 新建 - 备份旧代码
│   ├── langgraph_agent.py
│   ├── deep_agent/
│   └── hitl.py
└── tests/
    └── test_deep_agents_base.py  # 新建
```

### 2.4 验收检查

- [ ] `pip install deepagents` 无报错
- [ ] 新目录结构创建完成
- [ ] 旧代码备份到 `legacy/`
- [ ] 基础 Demo 运行成功
- [ ] 功能开关配置完成

---

## 三、Phase 2: 工具迁移 (Day 3-5)

### 3.1 目标

- 将 14 工具适配到 Deep Agents 格式
- 使用依赖注入模式
- 编写工具测试

### 3.2 任务清单

#### Day 3 - 核心工具

| 工具 | 优先级 | 预计时间 | 验收标准 |
|------|--------|----------|----------|
| `read_chapter_tool` | P0 | 1h | 单测通过 |
| `get_chapter_by_order_tool` | P0 | 1h | 单测通过 |
| `get_context_tool` | P0 | 1h | 单测通过 |
| `continue_writing_tool` | P0 | 2h | 单测通过 |

#### Day 4 - 编辑工具

| 工具 | 优先级 | 预计时间 | 验收标准 |
|------|--------|----------|----------|
| `smart_rewrite` | P0 | 2h | 含 interrupt 测试通过 |
| `smart_continue` | P0 | 1.5h | 单测通过 |
| `smart_insert` | P0 | 1.5h | 单测通过 |
| `apply_chapter_edit` | P1 | 1h | 单测通过 |

#### Day 5 - 分析工具

| 工具 | 优先级 | 预计时间 | 验收标准 |
|------|--------|----------|----------|
| `analyze_text_tool` | P0 | 1.5h | 单测通过 |
| `consistency_checker` | P1 | 1.5h | 单测通过 |
| `style_adapter` | P1 | 1h | 单测通过 |
| 工具注册表更新 | - | 1h | 所有工具可发现 |
| 集成测试 | - | 1h | 工具在 Agent 中可调用 |

### 3.3 代码模板

```python
# tools/writing_tools.py (迁移后)

def continue_writing_tool(
    prompt: str,
    context: str = "",
    style: str = "默认",
    length: int = 500
) -> str:
    """续写小说内容

    Args:
        prompt: 续写指令
        context: 前文上下文
        style: 写作风格
        length: 目标字数
    """
    # 使用依赖注入获取服务
    from app.services.ai import get_ai_service

    ai_service = get_ai_service()

    result = ai_service.call_ai_sync(
        system_prompt="你是专业的小说写作助手",
        user_prompt=f"上下文：{context}\n风格：{style}\n要求：{prompt}\n字数：约{length}字",
        max_tokens=length * 2
    )

    return result
```

### 3.4 交付物

```
backend/app/services/agent/tools/
├── __init__.py              # 更新 - 导出所有工具
├── writing_tools.py         # 更新 - 添加 runtime
├── editor_tools.py          # 更新 - 添加 interrupt
├── analysis_tools.py        # 更新 - 添加 runtime
└── data_tools.py            # 新建 - 数据相关工具

backend/app/services/agent/tests/
├── test_writing_tools.py    # 新建
├── test_editor_tools.py     # 新建
└── test_analysis_tools.py   # 新建
```

### 3.5 验收检查

- [ ] 所有 P0 工具迁移完成
- [ ] 所有 P1 工具迁移完成
- [ ] 工具单元测试全部通过
- [ ] 工具可在 Deep Agents 中正常调用
- [ ] interrupt_on 配置工具正常

---

## 四、Phase 3: 中间件开发 (Day 6-9)

### 4.1 目标

- 开发 5 个自定义中间件
- 集成现有功能模块

### 4.2 任务清单

#### Day 6 - 记忆中间件

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `MemoryMiddleware` 开发 | 3h | 单测通过 |
| `EnhancedMemoryStore` 适配 | 2h | 单测通过 |
| 记忆工具 (remember/recall) | 1h | 单测通过 |

#### Day 7 - 上下文中间件

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `ContextMiddleware` 开发 | 2h | 单测通过 |
| `BudgetMiddleware` 开发 | 2h | 单测通过 |
| `HistorySyncMiddleware` 开发 | 2h | 单测通过 |

#### Day 8 - 模型和成本中间件

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `ModelMiddleware` 开发 | 2h | 单测通过 |
| `CostMiddleware` 开发 | 2h | 单测通过 |
| 中间件集成测试 | 2h | 集成测试通过 |

#### Day 9 - 统一协调

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `UnifiedMemoryMiddleware` 开发 | 3h | 单测通过 |
| `IntentMiddleware` 开发 | 2h | 单测通过 |
| 全部中间件集成测试 | 1h | 集成测试通过 |

### 4.3 中间件清单

```python
# middleware/__init__.py

from .memory_middleware import MemoryMiddleware
from .context_middleware import ContextMiddleware
from .budget_middleware import BudgetMiddleware
from .model_middleware import ModelMiddleware
from .cost_middleware import CostMiddleware
from .history_sync_middleware import HistorySyncMiddleware
from .unified_memory_middleware import UnifiedMemoryMiddleware
from .intent_middleware import IntentMiddleware

__all__ = [
    "MemoryMiddleware",
    "ContextMiddleware",
    "BudgetMiddleware",
    "ModelMiddleware",
    "CostMiddleware",
    "HistorySyncMiddleware",
    "UnifiedMemoryMiddleware",
    "IntentMiddleware",
]
```

### 4.4 交付物

```
backend/app/services/agent/middleware/
├── __init__.py
├── memory_middleware.py
├── context_middleware.py
├── budget_middleware.py
├── model_middleware.py
├── cost_middleware.py
├── history_sync_middleware.py
├── unified_memory_middleware.py
├── intent_middleware.py
└── store_adapter.py

backend/app/services/agent/tests/
├── test_memory_middleware.py
├── test_context_middleware.py
└── test_middleware_integration.py
```

### 4.5 验收检查

- [ ] 所有中间件开发完成
- [ ] 中间件单元测试全部通过
- [ ] 中间件可正确注入到 Agent
- [ ] 记忆系统功能正常
- [ ] Token 预算管理正常

---

## 五、Phase 4: 核心替换 (Day 10-12)

### 5.1 目标

- 用 Deep Agents 替换 langgraph_agent.py
- 实现新的 WritingAgent
- 适配 API 层

### 5.2 任务清单

#### Day 10 - WritingAgent 核心

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `WritingAgent` 类设计 | 1h | 设计文档完成 |
| `create_writing_agent()` 实现 | 3h | 可创建 Agent |
| 工具注册 | 1h | 所有工具可用 |
| 中间件注册 | 1h | 所有中间件生效 |

#### Day 11 - API 适配

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `/chat` 端点适配 | 2h | 流式响应正常 |
| `/resume` 端点实现 | 2h | 中断恢复正常 |
| 功能开关逻辑 | 1h | 可切换新旧系统 |
| API 测试 | 1h | API 测试通过 |

#### Day 12 - interrupt/resume

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| 中断事件格式定义 | 1h | 格式文档完成 |
| 前端事件处理 | 2h | 前端可接收中断 |
| 恢复流程实现 | 2h | 恢复后继续执行 |
| 端到端测试 | 1h | E2E 测试通过 |

### 5.3 核心代码

```python
# writing_agent.py

from deepagents import create_deep_agent
from .tools import ALL_TOOLS
from .middleware import (
    UnifiedMemoryMiddleware,
    ModelMiddleware,
    CostMiddleware,
    IntentMiddleware,
)

class WritingAgent:
    """基于 Deep Agents 的写作助手"""

    def __init__(
        self,
        ai_service,
        redis_client,
        checkpointer
    ):
        self.ai_service = ai_service

        # 创建中间件
        self.middleware = [
            UnifiedMemoryMiddleware(redis_client, ai_service, checkpointer),
            ModelMiddleware(ai_service),
            CostMiddleware(),
            IntentMiddleware(),
        ]

        # 创建 Agent
        self.agent = create_deep_agent(
            tools=ALL_TOOLS,
            system_prompt=self._get_system_prompt(),
            middleware=self.middleware,
            checkpointer=checkpointer,
        )

    def _get_system_prompt(self):
        return """你是文枢AI，一个专业的小说写作助手。

你可以帮助用户：
1. 续写小说内容 - 使用 continue_writing_tool
2. 改写和优化文本 - 使用 smart_rewrite
3. 分析文本质量 - 使用 analyze_text_tool
4. 检查一致性问题 - 使用 consistency_checker

在执行关键操作前，请先确认用户的意图。
对于改写操作，生成多个版本供用户选择。
"""

    async def chat(self, message: str, thread_id: str, **kwargs):
        """对话接口"""
        return await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"thread_id": thread_id, **kwargs}}
        )

    async def chat_stream(self, message: str, thread_id: str, **kwargs):
        """流式对话接口"""
        async for event in self.agent.astream(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"thread_id": thread_id, **kwargs}},
            stream_mode=["values", "custom"]
        ):
            yield event

    async def resume(self, thread_id: str, response: any):
        """恢复中断的执行"""
        from langgraph.types import Command
        return await self.agent.ainvoke(
            None,
            config={"configurable": {"thread_id": thread_id}},
            command=Command(resume=response)
        )
```

### 5.4 交付物

```
backend/app/services/agent/
├── writing_agent.py         # 新建 - 核心入口
└── __init__.py              # 更新 - 导出 WritingAgent

backend/app/api/v1/
└── agent.py                 # 更新 - 适配新 Agent
```

### 5.5 验收检查

- [ ] WritingAgent 可正常创建
- [ ] 基本对话流程通过
- [ ] 流式响应正常
- [ ] interrupt 事件正确发送
- [ ] resume 后继续执行正常
- [ ] 功能开关可切换新旧系统

---

## 六、Phase 5: 集成测试 (Day 13-14)

### 6.1 目标

- 全面测试新系统
- 性能基准测试
- 回归测试

### 6.2 任务清单

#### Day 13 - 功能测试

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| 对话流程 E2E 测试 | 2h | 全部通过 |
| 改写流程 E2E 测试 | 2h | 含 interrupt 通过 |
| 分析流程 E2E 测试 | 1h | 全部通过 |
| 记忆系统 E2E 测试 | 1h | 全部通过 |

#### Day 14 - 性能和回归测试

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| 性能基准测试 | 2h | 不低于旧系统 |
| 并发压力测试 | 2h | 10 并发稳定 |
| 回归测试 | 1h | 无功能退化 |
| Bug 修复 | 1h | 无严重 Bug |

### 6.3 测试用例

```python
# tests/test_e2e.py

@pytest.mark.asyncio
async def test_chat_flow():
    """测试完整对话流程"""
    agent = create_writing_agent(...)

    # 1. 发起对话
    result = await agent.chat("帮我续写一段", thread_id="test")
    assert result["messages"][-1].content

    # 2. 继续对话
    result = await agent.chat("再长一点", thread_id="test")
    assert len(result["messages"]) > 2


@pytest.mark.asyncio
async def test_rewrite_with_interrupt():
    """测试改写中断流程"""
    agent = create_writing_agent(...)

    # 1. 触发改写
    events = []
    async for event in agent.chat_stream("改写这段文字", thread_id="test"):
        events.append(event)

    # 2. 验证中断
    interrupt_event = next(e for e in events if e.get("__interrupt__"))
    assert interrupt_event["type"] == "select_version"

    # 3. 恢复执行
    result = await agent.resume("test", response=1)
    assert "已选择" in result["messages"][-1].content


@pytest.mark.asyncio
async def test_memory_persistence():
    """测试记忆持久化"""
    agent = create_writing_agent(...)

    # 1. 第一次对话
    await agent.chat("我喜欢幽默风格", thread_id="test")

    # 2. 第二次对话（新会话）
    result = await agent.chat("帮我写一段", thread_id="test2")

    # 3. 验证记忆被召回
    # (取决于记忆系统实现)
```

### 6.4 性能指标

| 指标 | 旧系统基线 | 目标 | 验收标准 |
|------|-----------|------|----------|
| 首次响应时间 | 2s | ≤2s | ✅ 不退化 |
| 流式首字延迟 | 500ms | ≤500ms | ✅ 不退化 |
| interrupt 延迟 | 5s (轮询) | ≤100ms | ✅ 大幅提升 |
| 内存占用 | 500MB | ≤500MB | ✅ 不增加 |
| 并发能力 | 10 | ≥10 | ✅ 不退化 |

### 6.5 验收检查

- [ ] 所有 E2E 测试通过
- [ ] 性能不低于旧系统
- [ ] 10 并发压力测试通过
- [ ] 无功能退化
- [ ] 无严重 Bug

---

## 七、Phase 6: 上线切换 (Day 15)

### 7.1 目标

- 灰度发布
- 监控告警
- 确认稳定

### 7.2 任务清单

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| 灰度开关配置 | 1h | 可控制灰度比例 |
| 监控告警配置 | 1h | 告警规则生效 |
| 灰度 10% 发布 | 1h | 运行稳定 |
| 灰度 50% 发布 | 1h | 运行稳定 |
| 全量发布 | 1h | 运行稳定 |
| 旧代码归档 | 1h | legacy/ 目录完整 |

### 7.3 灰度策略

```python
# core/config.py

class Settings:
    # Deep Agents 灰度配置
    USE_DEEP_AGENTS: bool = False
    DEEP_AGENTS_GRAY_RATIO: int = 0  # 0-100

# api/v1/agent.py

def should_use_deep_agents(user_id: str) -> bool:
    if not settings.USE_DEEP_AGENTS:
        return False

    if settings.DEEP_AGENTS_GRAY_RATIO >= 100:
        return True

    # 按用户 ID hash 灰度
    return hash(user_id) % 100 < settings.DEEP_AGENTS_GRAY_RATIO
```

### 7.4 监控告警

```yaml
# 告警规则
alerts:
  - name: deep_agents_error_rate
    condition: error_rate > 1%
    action: notify
    severity: warning

  - name: deep_agents_error_rate_critical
    condition: error_rate > 5%
    action: auto_rollback
    severity: critical

  - name: deep_agents_latency
    condition: p99_latency > 10s
    action: notify
    severity: warning
```

### 7.5 回滚流程

```bash
# 紧急回滚
# 1. 关闭功能开关
export USE_DEEP_AGENTS=false

# 2. 重启服务
docker-compose restart backend

# 3. 验证回滚
curl http://localhost:8000/health
```

### 7.6 验收检查

- [ ] 灰度 10% 运行 1 小时无异常
- [ ] 灰度 50% 运行 1 小时无异常
- [ ] 全量发布成功
- [ ] 监控告警正常
- [ ] 旧代码归档完成

---

## 八、里程碑总结

| 里程碑 | 完成日期 | 关键交付物 |
|--------|----------|-----------|
| M1: 准备完成 | Day 2 | 目录结构、测试框架 |
| M2: 工具迁移完成 | Day 5 | 16+ 工具适配完成 |
| M3: 中间件完成 | Day 9 | 8 个中间件开发完成 |
| M4: 核心替换完成 | Day 12 | WritingAgent 可用 |
| M5: 测试通过 | Day 14 | 所有测试通过 |
| M6: 上线完成 | Day 15 | 全量发布成功 |

---

## 九、风险预案

| 风险 | 概率 | 影响 | 预案 |
|------|------|------|------|
| 依赖兼容问题 | 中 | 高 | 提前验证，准备降级方案 |
| 性能退化 | 低 | 高 | 性能测试，必要时优化 |
| 功能遗漏 | 中 | 中 | 完整测试用例，回归测试 |
| 上线故障 | 低 | 高 | 灰度发布，一键回滚 |

---

## 十、下一步

阅读 `08-risk-assessment.md` 了解详细的风险评估和回滚方案。
