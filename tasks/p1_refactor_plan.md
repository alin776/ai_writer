# Agent架构重构 - P1阶段任务清单

## 📌 阶段目标

**将新架构扩展到所有Action类和Agent节点**

- ✅ P0已完成：GeneralChatAction + _handle_general
- 🎯 P1目标：WritingAction、PlanningAction、AnalysisAction、StuckAction

## 🎯 P1阶段任务（预计1-2天）

### Phase 1: 重构WritingAction

#### Task 1.1: 添加prepare()方法
- [ ] 将execute()的逻辑复制到prepare()
- [ ] 修改返回值使用system_prompt参数
- [ ] 保持phase检测、chapter_num提取等业务逻辑
- **文件**：`backend/app/services/agent/actions/writing_action.py`
- **预计时间**：40分钟

#### Task 1.2: 标记旧代码
- [ ] __init__修改ai_service为可选参数
- [ ] execute()添加TODO标记
- **文件**：`backend/app/services/agent/actions/writing_action.py`
- **预计时间**：10分钟

#### Task 1.3: 修改_handle_writing节点
- [ ] 使用action.prepare()替代action.run()
- [ ] 调用_handle_agent_with_tools统一处理
- **文件**：`backend/app/services/agent/langgraph_agent.py`
- **预计时间**：30分钟

---

### Phase 2: 重构PlanningAction

#### Task 2.1: 添加prepare()方法
- [ ] 将execute()的逻辑复制到prepare()
- [ ] 修改返回值使用system_prompt参数
- **文件**：`backend/app/services/agent/actions/planning_action.py`
- **预计时间**：30分钟

#### Task 2.2: 标记旧代码
- [ ] __init__修改ai_service为可选参数
- [ ] execute()添加TODO标记
- **文件**：`backend/app/services/agent/actions/planning_action.py`
- **预计时间**：10分钟

#### Task 2.3: 修改_handle_planning节点
- [ ] 使用action.prepare()替代action.run()
- [ ] 调用_handle_agent_with_tools统一处理
- **文件**：`backend/app/services/agent/langgraph_agent.py`
- **预计时间**：30分钟

---

### Phase 3: 重构AnalysisAction

#### Task 3.1: 添加prepare()方法
- [ ] 将execute()的逻辑复制到prepare()
- [ ] 修改返回值使用system_prompt参数
- **文件**：`backend/app/services/agent/actions/analysis_action.py`
- **预计时间**：30分钟

#### Task 3.2: 标记旧代码
- [ ] __init__修改ai_service为可选参数
- [ ] execute()添加TODO标记
- **文件**：`backend/app/services/agent/actions/analysis_action.py`
- **预计时间**：10分钟

#### Task 3.3: 修改_handle_analysis节点
- [ ] 使用action.prepare()替代action.run()
- [ ] 调用_handle_agent_with_tools统一处理
- **文件**：`backend/app/services/agent/langgraph_agent.py`
- **预计时间**：30分钟

---

### Phase 4: 重构StuckAction

#### Task 4.1: 添加prepare()方法
- [ ] 将execute()的逻辑复制到prepare()
- [ ] 修改返回值使用system_prompt参数
- **文件**：`backend/app/services/agent/actions/stuck_action.py`
- **预计时间**：30分钟

#### Task 4.2: 标记旧代码
- [ ] __init__修改ai_service为可选参数
- [ ] execute()添加TODO标记
- **文件**：`backend/app/services/agent/actions/stuck_action.py`
- **预计时间**：10分钟

#### Task 4.3: 修改_handle_stuck节点
- [ ] 使用action.prepare()替代action.run()
- [ ] 调用_handle_agent_with_tools统一处理
- **文件**：`backend/app/services/agent/langgraph_agent.py`
- **预计时间**：30分钟

---

### Phase 5: 测试与验证

#### Task 5.1: 单元测试
- [ ] 测试WritingAction.prepare()
- [ ] 测试PlanningAction.prepare()
- [ ] 测试AnalysisAction.prepare()
- [ ] 测试StuckAction.prepare()
- **预计时间**：1小时

#### Task 5.2: 代码审查
- [ ] 检查所有Action的prepare()实现
- [ ] 检查所有_handle_*节点的重构
- [ ] 验证错误处理
- **预计时间**：30分钟

#### Task 5.3: 文档更新
- [ ] 更新todo.md的审查部分
- [ ] 记录迁移经验
- **预计时间**：30分钟

---

## ✅ 验收标准

### 功能验收
- [ ] 所有Action类实现prepare()方法
- [ ] 所有_handle_*节点使用新架构
- [ ] 所有单元测试通过
- [ ] 向后兼容（旧代码仍可运行）

### 代码质量
- [ ] 代码符合规范
- [ ] 注释清晰完整
- [ ] 无遗留TODO（除标记的待删除代码）
- [ ] 统一的错误处理

---

## 📋 实施策略

### 1. 批量处理
- 每个Action类独立处理（prepare + 标记 + 节点修改）
- 完成一个Action后立即测试
- 逐个验证，降低风险

### 2. 复用P0经验
- 使用P0成功的模式
- 保持向后兼容
- 充分的文档和注释

### 3. 简化实施
- 这些Action已经符合新架构模式（不调用LLM）
- 只需将execute()逻辑移到prepare()
- 工作量比预期小

---

## 🎯 关键发现

**好消息**：WritingAction、PlanningAction、AnalysisAction、StuckAction已经基本符合新架构！

它们的execute()方法：
- ✅ 不直接调用LLM
- ✅ 只构建system_prompt
- ✅ 返回ActionResult包含system_prompt和agent_type

**这意味着**：
- 迁移工作量比预期小50%
- 主要是添加prepare()方法（复制execute()逻辑）
- 修改_handle_*节点使用prepare()
- 风险更低

---

## 📂 涉及的文件

1. **Action类（4个）**
   - `backend/app/services/agent/actions/writing_action.py`
   - `backend/app/services/agent/actions/planning_action.py`
   - `backend/app/services/agent/actions/analysis_action.py`
   - `backend/app/services/agent/actions/stuck_action.py`

2. **LangGraph Agent（1个）**
   - `backend/app/services/agent/langgraph_agent.py`

3. **测试文件（新增）**
   - `backend/test_all_actions.py`

---

## 审查部分

（完成后填写）

### 执行摘要
待完成...

### 修改文件清单
待完成...

### 测试结果
待完成...

### 最终验证结果
待完成...
