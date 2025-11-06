# Chat模式深度优化 - 实施计划

**创建时间**: 2025-01-06
**当前状态**: ✅ 解除暂缓，开始深度优化
**预计总工期**: 10-14天

---

## 🎯 优化目标

### 主要目标
1. ✅ 利用已实现的chat_stream()方法（Line 1836-1953）
2. 🎯 添加API端点mode参数支持
3. 🎯 实现分层上下文管理体系
4. 🎯 优化Prompt体系，提升意图识别准确率
5. 🎯 建立完整的监控和日志体系
6. 🎯 完善配置和错误处理

### 成功标准
- [ ] chat_stream可以通过API调用
- [ ] 意图识别准确率>90%
- [ ] 长对话(>30轮)稳定运行
- [ ] Token使用降低30-50%
- [ ] 响应时间≤Planning模式
- [ ] 完整的监控指标

---

## 📋 实施计划

### Phase 0: 验证当前状态 (1天) ✅

#### 0.1 验证已实现功能
- [ ] 验证chat_stream()方法功能完整性
  - 文件位置: `backend/app/services/agent/langgraph_agent.py:1836-1953`
  - 验证astream()流式执行
  - 验证回调机制(on_progress, on_tool_call, on_content)
  - 验证异常处理

- [ ] 检查依赖版本
  ```bash
  pip show langgraph langchain langchain-core
  ```
  - langgraph >= 0.2.0
  - langchain >= 0.3.0

- [ ] 检查现有API端点
  - 文件位置: `backend/app/api/v1/agent_react_stream.py`
  - 确认ReAct Stream端点是否使用了chat_stream()
  - 检查是否可以复用

#### 0.2 准备工作
- [ ] 创建功能分支
  ```bash
  git checkout -b feature/chat-optimization
  ```

- [ ] 备份当前配置
  ```bash
  cp -r backend/app/config backend/app/config.backup
  ```

---

### Phase 1: P1核心功能实现 (5-7天) 🎯

#### 1.1 P1-02: API端点适配 (2天)

**目标**: 修改现有API，添加mode参数支持

**Day 1上午**: 设计数据模型
- [ ] 定义ChatMode枚举
  ```python
  class ChatMode(str, Enum):
      PLANNING = "planning"
      REACT = "react"
  ```

- [ ] 扩展ChatRequest模型
  - 添加mode字段
  - 添加model_selector字段

- [ ] 定义统一的事件格式
  - ChatEvent模型
  - SSE格式转换

**Day 1下午**: 修改API端点
- [ ] 修改`/agent/chat/stream`端点
  - 添加mode参数（Header或Body）
  - 实现模式路由逻辑
  - 保持向后兼容（默认planning）

- [ ] 实现_handle_react_mode()
  - 调用chat_stream()
  - 转换事件为SSE格式
  - 错误处理

- [ ] 实现_handle_planning_mode()
  - 保持现有逻辑
  - 统一格式输出

**Day 2上午**: 事件格式化
- [ ] 实现_format_chat_event_to_sse()
  - 统一事件格式
  - 添加mode标识

- [ ] 实现_format_planning_chunk_to_sse()
  - 保持兼容性

**Day 2下午**: 测试
- [ ] 编写单元测试
  - 测试模式切换
  - 测试向后兼容性

- [ ] API手动测试
  - 测试react模式
  - 测试planning模式
  - 测试默认行为

**验收标准**:
- [ ] API支持mode参数
- [ ] React和Planning模式都能正常工作
- [ ] 不传mode时默认planning
- [ ] 所有测试通过

#### 1.2 P1-04: 上下文管理 (2天)

**目标**: 实现分层记忆体系，控制token使用

**Day 1上午**: 设计ContextManager
- [ ] 定义ContextStore接口
  ```python
  class ContextStore:
      async def load(session_id: str) -> Context
      async def save(session_id: str, context: Context)
      async def update(session_id: str, messages: List)
  ```

- [ ] 设计内存分层
  - Short Memory: 最近5-8轮
  - Summary Memory: 滚动摘要
  - LongTerm: 向量存储(可选)

- [ ] 定义Token预算
  | 组件 | 预算 |
  |------|------|
  | 系统提示 | 20% |
  | 摘要上下文 | 25% |
  | 近期对话 | 35% |
  | 工具结果 | 15% |
  | 预留区 | 5% |

**Day 1下午**: 实现基础功能
- [ ] 实现ContextManager类
  - build_context(): 构建上下文
  - update_context(): 更新上下文
  - compress_context(): 压缩上下文

- [ ] 实现摘要生成
  - 对话摘要模板
  - 工具结果摘要

**Day 2上午**: 集成到chat_stream
- [ ] 在chat_stream入口注入上下文构建
  ```python
  context_bundle = await context_manager.build_context(session_id)
  input_state["messages"] = context_bundle.messages
  ```

- [ ] 在事件回调中更新上下文
  ```python
  await context_manager.update_context(session_id, new_messages)
  ```

**Day 2下午**: 测试和优化
- [ ] 长对话测试(30轮)
- [ ] Token使用统计
- [ ] 调整预算参数

**验收标准**:
- [ ] 长对话Token使用<80%窗口
- [ ] 摘要内容可读且保留关键信息
- [ ] 通过30轮对话测试

#### 1.3 P1-05: Prompt优化 (2天)

**目标**: 设计高质量Prompt体系，提升意图识别和输出质量

**Day 1上午**: 创建Prompt管理器
- [ ] 实现PromptManager类
  ```python
  class PromptManager:
      def load_templates()
      def render(template_name, **kwargs)
      def get_version(template_name)
  ```

- [ ] 创建模板目录结构
  ```
  prompts/templates/
  ├── intent_classifier.yaml
  ├── writing_agent.yaml
  ├── planning_agent.yaml
  └── tool_agent.yaml
  ```

**Day 1下午**: 设计Prompt模板
- [ ] 意图分类Prompt (intent_classifier.yaml)
  - 定义4种意图: writing/planning/tool/query
  - 添加示例和规则
  - JSON输出格式

- [ ] Writing Agent Prompt (writing_agent.yaml)
  - 角色定位
  - 能力描述
  - 输出规范
  - 支持动态参数注入

**Day 2上午**: 完成其他Agent Prompt
- [ ] Tool Agent Prompt (tool_agent.yaml)
  - 可用工具列表
  - 工具选择原则
  - 参数构造指导

- [ ] Planning Agent Prompt (planning_agent.yaml)
  - SMART原则
  - 输出格式（目标/分析/计划/风险）

**Day 2下午**: 集成和测试
- [ ] 集成到chat_stream各节点
  ```python
  prompt = prompt_manager.render(
      "intent_classifier",
      user_message=message,
      context_summary=context.summary
  )
  ```

- [ ] 意图分类测试
  - 准备10-20个测试用例
  - 验证准确率>90%

**验收标准**:
- [ ] PromptManager正常工作
- [ ] 所有模板可以正确渲染
- [ ] 意图识别准确率>90%
- [ ] Agent输出符合预期格式

---

### Phase 2: P2完善功能 (3-4天) 🎯

#### 2.1 P2-01: 监控日志 (1天)

**上午**: 设计监控体系
- [ ] 定义关键指标
  ```python
  # 性能指标
  - chat_stream_duration: 处理时间
  - llm_call_duration: LLM调用时间
  - context_build_duration: 上下文构建时间

  # Token使用
  - token_usage_total
  - token_usage_prompt
  - token_usage_completion

  # 业务指标
  - intent_accuracy: 意图识别准确率
  - chat_requests_total
  - chat_errors_total
  ```

- [ ] 实现MetricsCollector
  ```python
  class MetricsCollector:
      def counter(name, value, **labels)
      def gauge(name, value, **labels)
      def histogram(name, value, **labels)
  ```

**下午**: 集成监控
- [ ] 在关键节点添加监控
  - API入口/出口
  - chat_stream开始/结束
  - LLM调用前后
  - 上下文构建前后

- [ ] 实现日志输出
  - 结构化日志
  - 包含trace_id关联

**验收标准**:
- [ ] 所有关键指标可以收集
- [ ] 日志可追溯完整执行流程

#### 2.2 P2-02: 错误处理 (1天)

**上午**: 优化错误处理
- [ ] 实现统一错误处理器
  ```python
  class ErrorHandler:
      async def handle_llm_error(error)
      async def handle_tool_error(error)
      async def handle_context_error(error)
  ```

- [ ] 定义降级策略
  - LLM调用失败 → 重试3次 → 使用缓存 → 返回友好提示
  - 工具调用失败 → 重试1次 → 返回错误信息
  - 上下文构建失败 → 使用基础上下文

**下午**: 集成错误处理
- [ ] 在chat_stream各节点添加错误处理
- [ ] 实现错误事件上报
- [ ] 添加错误恢复测试

**验收标准**:
- [ ] 所有错误都有处理机制
- [ ] 错误率<1%
- [ ] 用户看到友好提示

#### 2.3 P2-03: 配置管理 (1天)

**上午**: 设计配置体系
- [ ] 创建配置文件结构
  ```
  config/
  ├── chat_modes.yaml
  ├── context_config.yaml
  └── prompt_config.yaml
  ```

- [ ] 定义配置项
  - 模式相关: 默认模式、用户权限
  - 上下文相关: Token预算、压缩阈值
  - Prompt相关: 版本、A/B测试

**下午**: 实现配置加载
- [ ] 实现ConfigManager
  ```python
  class ConfigManager:
      def load_config(config_name)
      def get(config_path)
      def reload()  # 热重载
  ```

- [ ] 集成到各模块

**验收标准**:
- [ ] 配置集中管理
- [ ] 支持热重载
- [ ] 配置验证完整

---

### Phase 3: 测试和验证 (2-3天) 🎯

#### 3.1 单元测试 (1天)

**上午**: 核心功能测试
- [ ] ContextManager测试
  - 上下文构建
  - Token预算控制
  - 摘要生成

- [ ] PromptManager测试
  - 模板加载
  - 模板渲染
  - 参数注入

**下午**: API测试
- [ ] mode参数测试
- [ ] 事件格式测试
- [ ] 向后兼容性测试

#### 3.2 集成测试 (1天)

**上午**: 完整流程测试
- [ ] React模式端到端测试
  - 意图识别 → Agent执行 → 工具调用 → 响应生成

- [ ] Planning模式兼容性测试

**下午**: 边缘case测试
- [ ] 极长消息
- [ ] 快速连续请求
- [ ] 并发请求
- [ ] 网络中断恢复

#### 3.3 性能测试 (1天)

**上午**: 基准测试
- [ ] 响应时间测试
  - 简单对话: <2秒
  - 复杂任务: <10秒

- [ ] Token使用测试
  - 对比优化前后
  - 目标: 降低30-50%

**下午**: 长对话测试
- [ ] 30轮对话稳定性
- [ ] 60轮对话Token管理
- [ ] 压力测试(100并发)

**验收标准**:
- [ ] 所有测试通过
- [ ] 性能指标达标
- [ ] 无严重bug

---

### Phase 4: 部署和灰度 (持续) 🎯

#### 4.1 部署准备
- [ ] 代码review
- [ ] 文档更新
- [ ] 部署脚本准备

#### 4.2 灰度发布
- [ ] Phase 1: 10%流量 (观察1周)
  - 监控指标
  - 收集反馈

- [ ] Phase 2: 30%流量 (观察1周)
- [ ] Phase 3: 50%流量 (观察2周)
- [ ] Phase 4: 100%流量

#### 4.3 持续监控
- [ ] 每日监控关键指标
- [ ] 每周数据分析
- [ ] 问题快速响应

---

## 📊 进度追踪

### 完成情况
- Phase 0: ⏸️ 待开始
- Phase 1: ⏸️ 待开始
- Phase 2: ⏸️ 待开始
- Phase 3: ⏸️ 待开始
- Phase 4: ⏸️ 待开始

### 时间线
```
Week 1:  Phase 0 + P1-02 (API适配)
Week 2:  P1-04 (上下文) + P1-05 (Prompt)
Week 3:  Phase 2 (P2完善功能)
Week 4:  Phase 3 (测试验证) + Phase 4开始
Week 5+: 灰度发布和监控
```

---

## 🎯 关键决策点

### 决策点1: Phase 0完成后
**问题**: 技术可行性是否验证？
**决策**: 是否继续Phase 1？

### 决策点2: Phase 1完成后
**问题**: 核心功能是否达标？
**决策**: 是否继续Phase 2？

### 决策点3: Phase 3完成后
**问题**: 测试是否通过？
**决策**: 是否开始灰度发布？

---

## ⚠️ 风险控制

### 高风险
1. **chat_stream与现有系统集成**: 需仔细测试
2. **长对话Token溢出**: 需完善压缩策略
3. **性能回退**: 需持续监控

### 应对措施
- 每个Phase完成后进行评估
- 保留回滚方案
- 小步快跑，快速验证

---

## 📚 相关文档

### 核心文档
- [chat优化/README.md](../docs/Agent/tasks/chat优化/README.md)
- [chat优化/IMPLEMENTATION_PLAN.md](../docs/Agent/tasks/chat优化/IMPLEMENTATION_PLAN.md)

### P1系列
- [P1-01-实现chat_stream.md](../docs/Agent/tasks/chat优化/P1-01-实现chat_stream.md) - 已完成
- [P1-02-API端点适配.md](../docs/Agent/tasks/chat优化/P1-02-API端点适配.md)
- [P1-04-上下文管理.md](../docs/Agent/tasks/chat优化/P1-04-上下文管理.md)
- [P1-05-Prompt优化.md](../docs/Agent/tasks/chat优化/P1-05-Prompt优化.md)

### P2系列
- [P2-01-监控日志.md](../docs/Agent/tasks/chat优化/P2-01-监控日志.md)
- [P2-02-错误处理.md](../docs/Agent/tasks/chat优化/P2-02-错误处理.md)
- [P2-03-配置管理.md](../docs/Agent/tasks/chat优化/P2-03-配置管理.md)

---

**状态**: ⏸️ 待确认
**下一步**: 等待确认后开始Phase 0
**负责人**: 开发团队

---

## 📝 实施记录

### 2025-01-06
- ✅ 创建实施计划
- ✅ 解除P1/P2/P3暂缓状态
- ⏸️ 等待确认后开始Phase 0
