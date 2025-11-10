# ReAct模式 - 进度反馈增强实施计划

**创建日期**: 2025-11-10
**项目**: Phase1优化#3 - 进度反馈增强
**当前状态**: 45分/100分 → 目标: 90分+
**预计完成时间**: 10小时 (1.5个工作日)
**文档参考**: docs/Agent/tasks/

---

## 📊 当前情况

### 已完成 (45%)
- ✅ 流式事件处理基础
- ✅ 节点描述显示
- ✅ 工具名称显示
- ✅ ActivityStream组件已存在
- ✅ activities状态已定义

### 待完成 (55%)
- ❌ 进度百分比计算 (0-100%)
- ❌ ETA动态计算 (预计剩余时间)
- ❌ 步骤计数 (第X/Y步)
- ❌ ProgressTracker类
- ❌ SSE事件映射逻辑
- ❌ 进度条UI组件

---

## ⚡ Pre-Phase 0: 现有实现调查 (1小时) - P0最高优先级

**目标**: 了解已有实现,避免重复开发,明确增强方向

### 调查任务
- [ ] Task 0.1: 调查ActivityStream组件 (15分钟)
  - [ ] 读取 src/components/agent/ActivityStream.tsx 源码
  - [ ] 记录组件功能和显示字段
  - [ ] 确认缺失字段 (progress, eta, step_count)
  - [ ] 决策: 新建ProgressBar 还是 增强ActivityStream

- [ ] Task 0.2: 调查activities状态流程 (15分钟)
  - [ ] 读取 src/hooks/useAgentChat.ts 源码
  - [ ] 找到activities状态定义和更新位置
  - [ ] 搜索progress事件监听器
  - [ ] 确认SSE事件处理是否缺失

- [ ] Task 0.3: 调查ParallelToolNode (15分钟)
  - [ ] 读取 backend/app/services/agent/parallel_tool_node.py
  - [ ] 分析功能和进度跟踪能力
  - [ ] 确定与ProgressTracker的关系 (复用/扩展/独立)

- [ ] Task 0.4: 确认SSE事件流程 (15分钟)
  - [ ] 检查后端SSE实现 (app/api/agent.py)
  - [ ] 查看已发送的事件类型 (progress, content, tool_call等)
  - [ ] 检查progress事件数据格式
  - [ ] 确认前端事件监听逻辑

- [ ] 填写调查总结表格
- [ ] 做出关键决策 (ProgressBar方案、SSE处理、ProgressTracker设计)
- [ ] 编写调查报告

**预期产出**: Pre-Phase 0调查报告,明确后续实施方向

---

## 🏗️ Phase 1: 核心架构实施 (4小时) - P0高优先级

**目标**: 建立进度跟踪的基础设施

### 后端开发任务
- [ ] Task 1.1: 创建NODE_METADATA配置 (1小时)
  - [ ] 创建 backend/app/services/agent/node_metadata.py
  - [ ] 定义NodeMetadata类型 (name, description, estimated_time, progress_weight, category)
  - [ ] 配置所有节点元数据 (intent_classifier, route_intent, writing_agent等)
  - [ ] 实现get_node_info()辅助函数
  - [ ] 验证权重总和为1.0

- [ ] Task 1.2: 实现ProgressTracker类 (1.5小时)
  - [ ] 创建 backend/app/services/agent/progress_tracker.py
  - [ ] 实现__init__方法 (初始化状态)
  - [ ] 实现start_node()方法 (开始节点追踪)
  - [ ] 实现end_node()方法 (结束节点追踪)
  - [ ] 实现calculate_progress()方法 (计算进度百分比)
  - [ ] 实现calculate_eta()方法 (计算预估剩余时间)
  - [ ] 实现get_progress_event()方法 (生成进度事件)

- [ ] Task 1.3: 集成到LangGraph (1小时)
  - [ ] 修改 backend/app/services/agent/langgraph_agent.py
  - [ ] 在LangGraphAgent类中添加progress_tracker属性
  - [ ] 在astream_events()中添加节点开始/结束钩子
  - [ ] 在每个节点事件处理中发送progress事件
  - [ ] 确保不影响现有功能

- [ ] Task 1.4: 添加单元测试 (0.5小时)
  - [ ] 创建 backend/tests/test_progress_tracker.py
  - [ ] 测试进度计算准确性
  - [ ] 测试ETA计算合理性
  - [ ] 测试边界情况处理

**预期产出**: ProgressTracker类完整实现并集成到Agent系统

---

## ⚙️ Phase 2: 核心功能实施 (3小时) - P0高优先级

**目标**: 实现进度计算和ETA预估的核心算法

### 算法优化任务
- [ ] Task 2.1: 优化进度百分比计算 (1小时)
  - [ ] 实现动态节点权重归一化
  - [ ] 基于实际执行时间计算当前节点进度
  - [ ] 添加进度平滑处理 (避免跳跃)
  - [ ] 处理工具执行的细粒度进度
  - [ ] 测试不同场景下的进度准确性

- [ ] Task 2.2: 优化ETA动态计算 (1小时)
  - [ ] 实现基于实际速度的ETA计算
  - [ ] 添加ETA置信度评估 (low/medium/high)
  - [ ] 实现平滑ETA更新 (避免剧烈波动)
  - [ ] 添加ETA显示优化 (智能单位选择)
  - [ ] 处理ETA异常情况 (超时等)

- [ ] Task 2.3: 工具参数提取 (0.5小时)
  - [ ] 实现_extract_tool_params()方法
  - [ ] 提取关键参数 (章节号、文件名等)
  - [ ] 生成友好的工具描述
  - [ ] 添加参数格式化逻辑

- [ ] Task 2.4: 步骤信息增强 (0.5小时)
  - [ ] 添加步骤计数逻辑 (current_step/total_steps)
  - [ ] 生成步骤描述 (第X/Y步)
  - [ ] 添加节点友好名称显示
  - [ ] 增强进度事件数据格式

**预期产出**: 准确的进度百分比和ETA计算,友好的步骤描述

---

## 🎨 Phase 3: 前端集成实施 (2.5小时) - P1中优先级

**目标**: 前端UI组件和用户体验

### 前端开发任务
- [ ] Task 3.1: 补充TypeScript类型定义 (10分钟)
  - [ ] 找到 src/types/agent.ts 或类似文件
  - [ ] 在ProgressEvent接口中添加新字段 (progress, eta, current_step, total_steps等)
  - [ ] 更新ActivityItem类型 (如需要)
  - [ ] 添加类型文档注释

- [ ] Task 3.2: 新建ProgressBar组件 (40分钟)
  - [ ] 创建 src/components/agent/ProgressBar.tsx
  - [ ] 实现进度条UI (使用Shadcn/UI Progress组件)
  - [ ] 显示进度百分比 (0-100%)
  - [ ] 显示ETA倒计时 (智能单位)
  - [ ] 显示步骤计数 (第X/Y步)
  - [ ] 添加响应式设计和动画效果

- [ ] Task 3.3: SSE事件处理 (30分钟) ⚠️ 关键
  - [ ] 修改 src/hooks/useAgentChat.ts
  - [ ] 在sendMessageStream中添加progress事件监听
  - [ ] 实现progress事件到activities的映射
  - [ ] 更新activities状态 (包含新字段)
  - [ ] 测试事件流正确触发

- [ ] Task 3.4: activities更新逻辑 (30分钟) ⚠️ 关键
  - [ ] 在useAgentChat.ts中完善activities更新
  - [ ] 处理progress字段更新
  - [ ] 处理eta字段更新
  - [ ] 处理step_count字段更新
  - [ ] 确保UI实时响应

- [ ] Task 3.5: 完善ActivityStream集成 (20分钟)
  - [ ] 修改 src/components/agent/AgentChatPanel.tsx
  - [ ] 集成ProgressBar组件 (显示在ActivityStream上方或内部)
  - [ ] 传递activities数据到ProgressBar
  - [ ] 调整布局和样式
  - [ ] 测试UI显示效果

**预期产出**: 友好的进度条UI,实时更新的进度信息

---

## 🧪 测试和验收 (1小时)

### 测试任务
- [ ] 后端单元测试
  - [ ] ProgressTracker类所有方法测试通过
  - [ ] NODE_METADATA配置验证通过
  - [ ] 进度计算准确性测试 (误差<5%)
  - [ ] ETA计算合理性测试 (误差<30%)

- [ ] 前端集成测试
  - [ ] SSE事件正确触发activities更新
  - [ ] 进度条平滑更新
  - [ ] ETA倒计时显示正确
  - [ ] UI响应式设计正常

- [ ] 端到端测试
  - [ ] 写作模式完整流程测试
  - [ ] 规划模式完整流程测试
  - [ ] 分析模式完整流程测试
  - [ ] 错误处理测试

- [ ] 性能测试
  - [ ] 进度更新延迟 < 0.5秒
  - [ ] Agent执行性能影响 < 5%
  - [ ] 前端渲染性能正常

- [ ] 用户验收
  - [ ] 进度显示清晰易懂
  - [ ] ETA预估合理可信
  - [ ] UI美观友好
  - [ ] 整体体验提升明显

**预期产出**: 所有测试通过,功能达到90分以上

---

## 📈 成功标准

### 功能完整性
- [ ] ProgressTracker类实现完整
- [ ] NODE_METADATA配置覆盖所有节点
- [ ] 进度百分比准确显示 (0-100%)
- [ ] ETA计算合理 (误差<30%)
- [ ] 步骤计数正确 (第X/Y步)
- [ ] 前端UI友好美观

### 性能指标
- [ ] 进度更新延迟 < 0.5秒
- [ ] ETA误差 < 30%
- [ ] Agent执行性能影响 < 5%
- [ ] 前端渲染流畅无卡顿

### 用户体验
- [ ] 用户满意度 > 90%
- [ ] "卡住"咨询减少 > 80%
- [ ] 用户焦虑感降低 > 70%
- [ ] 任务完成率提升 > 15%

---

## 📝 执行记录

### Pre-Phase 0: 现有实现调查
_待执行_

### Phase 1: 核心架构实施
_待执行_

### Phase 2: 核心功能实施
_待执行_

### Phase 3: 前端集成实施
_待执行_

### 测试和验收
_待执行_

---

## 📊 回顾总结

### 任务完成情况
- [ ] Pre-Phase 0 (0/4 tasks)
- [ ] Phase 1 (0/4 tasks)
- [ ] Phase 2 (0/4 tasks)
- [ ] Phase 3 (0/5 tasks)
- [ ] 测试验收 (0/5 tasks)

**总进度**: 0% (0/22 tasks)

### 变更记录
_待补充_

### 遇到的问题
_待补充_

### 解决方案
_待补充_

---

**最后更新**: 2025-11-10
**负责人**: 待分配
**优先级**: ⚡⚡⚡ P0 (最高)
**预计完成**: 1.5天内 (10小时)
