# AI写作平台Agent化改造开发计划

> **创建时间**: 2025-10-31
> **总工期**: 7-10周
> **当前阶段**: 准备启动

---

## 📊 项目概况

### 改造目标
1. **零破坏承诺**: 不影响现有普通AI模式功能
2. **渐进式改造**: 在 `backend/app/services/agent/` 目录下增强
3. **高价值产出**:
   - 内容质量提升 +15%
   - API成本降低 40-50%
   - Memory检索速度 < 100ms
   - 用户满意度 > 4.5/5

### 技术方案来源
从5个优秀开源项目提取精华:
- **novel-multi-agents**: 工具驱动通信 + 强类型输出 + 质量循环
- **pulpgen**: 补丁式版本管理
- **novel-agent**: 分层Memory系统
- **MetaGPT**: ARE模式
- **novel-ai-agent-Chinese**: 网文爽感优化Prompt

---

## 🎯 三大阶段任务

### 阶段一: 核心基础设施改造 (Week 1-3)
- [ ] Week 1: Memory系统增强
- [ ] Week 2: 工具系统标准化
- [ ] Week 3: 版本管理系统

### 阶段二: 高价值功能集成 (Week 4-7)
- [ ] Week 4-5: 质量循环机制
- [ ] Week 6: Prompt库优化
- [ ] Week 7: 模型选择器

### 阶段三: 架构优化与完善 (Week 8-10)
- [ ] Week 8-9: ARE设计理念
- [ ] Week 10: 完善和优化

---

## 📅 Week 1: Memory系统增强 (5个工作日)

### 目标
实现分层记忆（短期/中期/长期）、智能遗忘策略、状态快照与恢复

### Day 1-2: 设计和架构
- [ ] 设计 MemoryItem 数据结构
  - 定义字段: id, role, content, timestamp, importance, decay_rate, access_count
  - 创建 Pydantic 模型
  - 文件位置: `backend/app/services/agent/memory/types.py`

- [ ] 设计 MemoryLayer 枚举
  - SHORT_TERM (短期记忆, 最近10条)
  - MEDIUM_TERM (中期记忆, 最近100条)
  - LONG_TERM (长期记忆, 压缩摘要)

- [ ] 设计智能遗忘策略算法
  - 重要度计算公式: `importance = initial_score × time_decay × access_frequency`
  - 遗忘阈值: 0.1
  - 衰减速率设计

### Day 3-4: 核心实现
- [ ] 实现 EnhancedMemoryManager 类
  - 文件: `backend/app/services/agent/memory/enhanced_memory_manager.py`
  - 方法: add_memory(), get_relevant_memories(), apply_forgetting()
  - 方法: create_snapshot(), restore_snapshot()

- [ ] 实现 SmartForgetStrategy 类
  - 文件: `backend/app/services/agent/memory/memory_strategy.py`
  - 方法: calculate_importance(), should_forget(), compress_to_summary()

- [ ] 实现分层存储 (Redis)
  - 短期记忆: `user:{user_id}:memory:short` (Redis List)
  - 中期记忆: `user:{user_id}:memory:medium` (Redis List)
  - 长期记忆: `user:{user_id}:memory:long` (Redis String)

### Day 5: 快照功能和测试
- [ ] 实现状态快照
  - create_snapshot(user_id, conversation_id)
  - restore_snapshot(snapshot_id)
  - 存储位置: Redis + PostgreSQL

- [ ] 编写单元测试
  - test_add_memory()
  - test_smart_forgetting()
  - test_create_snapshot()
  - test_restore_snapshot()
  - 测试文件: `tests/test_memory/test_enhanced_memory.py`

- [ ] 性能测试
  - Memory检索速度 < 100ms
  - 并发性能测试

### ✅ Week 1 验收标准
- [ ] 所有单元测试通过
- [ ] Memory检索速度 < 100ms
- [ ] 测试覆盖率 > 80%

---

## 📅 Week 2: 工具系统标准化 (5个工作日)

### 目标
实现标准化工具接口、强类型输入输出、改造现有工具

### Day 1-2: 类型系统设计
- [ ] 设计工具类型定义
  - 文件: `backend/app/services/agent/tools/tool_types.py`
  - 类: ToolInput(BaseModel), ToolOutput(BaseModel)
  - 类: StandardTool(Generic[InputT, OutputT])

- [ ] 设计工具执行流程
  - 输入验证 (Pydantic)
  - 执行逻辑
  - 输出验证
  - 统计记录

- [ ] 编写工具装饰器
  ```python
  @register_as_tool("tool_id", "category", "description")
  async def my_tool(...): pass
  ```

### Day 3-4: 工具改造
- [ ] 改造 continue_writing_tool
  - 定义 ContinueWritingInput / ContinueWritingOutput
  - 使用 StandardTool 基类

- [ ] 改造 polish_text_tool
  - 定义输入/输出类型
  - 添加验证逻辑

- [ ] 改造 analyze_text_tool
  - 定义输入/输出类型
  - 添加验证逻辑

- [ ] 更新 tool_registry.py
  - 支持新的工具类型
  - 添加工具调用统计
  - 添加监控日志

### Day 5: 集成和测试
- [ ] 集成到 LangGraph
  - 更新 `langgraph_agent.py`
  - 使用新的工具接口
  - 测试工具调用

- [ ] 编写单元测试
  - test_tool_validation()
  - test_tool_execution()
  - test_tool_statistics()
  - 测试文件: `tests/test_tools/test_writing_tools.py`

- [ ] 集成测试
  - 端到端测试工具调用
  - 验证类型安全

### ✅ Week 2 验收标准
- [ ] 所有工具改造完成
- [ ] 工具调用成功率 > 99%
- [ ] 类型检查通过 (mypy)

---

## 📅 Week 3: 版本管理系统 (5个工作日)

### 目标
实现补丁式版本控制、支持版本回滚、支持版本分支

### Day 1-2: 数据模型设计
- [ ] 设计 Patch 数据结构
  - PatchOperation: INSERT/DELETE/REPLACE/REORDER
  - Patch(BaseModel): patch_id, operation, position, content, metadata

- [ ] 设计 Version 数据结构
  - Version(BaseModel): version_id, parent_version_id, patches, timestamp, description

- [ ] 设计 VersionedContent 数据结构
  - content_id, base_content, versions, current_version_id, branches

### Day 3-4: 核心功能实现
- [ ] 实现 VersionControlService
  - 文件: `backend/app/services/agent/version_control.py`
  - 方法: create_content(), apply_patch()
  - 方法: get_content_at_version(), rollback_to_version()
  - 方法: create_branch()

- [ ] 实现补丁应用逻辑
  - INSERT: 在指定位置插入内容
  - DELETE: 删除指定范围
  - REPLACE: 替换指定内容
  - REORDER: 重新排序

- [ ] 实现版本树遍历
  - 从 base 到 target 的补丁路径
  - 分支管理逻辑

### Day 5: 集成和测试
- [ ] 集成到章节创作流程
  - 每次修改创建新版本
  - 自动保存变更历史
  - 支持回滚操作

- [ ] 创建 API 端点
  - POST /api/v1/agent/versions/create
  - POST /api/v1/agent/versions/apply-patch
  - GET /api/v1/agent/versions/{version_id}
  - POST /api/v1/agent/versions/rollback

- [ ] 编写单元测试
  - test_create_content()
  - test_apply_patch()
  - test_rollback()
  - test_branch_creation()
  - 测试文件: `tests/test_version_control.py`

- [ ] 性能测试
  - 版本回滚速度 < 200ms

### ✅ Week 3 验收标准
- [ ] 版本创建和回滚功能正常
- [ ] 版本回滚速度 < 200ms
- [ ] 完整的变更历史可查询

---

## ✅ 阶段一总体验收标准

### 功能完整性
- [ ] Memory系统增强完成，支持三层记忆
- [ ] 工具系统标准化完成，类型安全
- [ ] 版本管理系统完成，支持回滚和分支

### 性能指标
- [ ] Memory检索速度 < 100ms
- [ ] 版本回滚速度 < 200ms
- [ ] 工具调用成功率 > 99%

### 质量指标
- [ ] 所有单元测试通过
- [ ] 测试覆盖率 > 80%
- [ ] 类型检查通过 (mypy)
- [ ] 不影响现有功能

---

## 📝 重要原则

### 1. 简化原则
- 每个改动影响最小范围代码
- 保持代码简洁易读
- 避免过度设计

### 2. 测试优先
- 每个功能都有对应测试
- 测试覆盖率 > 80%
- 自动化测试

### 3. 可回滚性
- 配置开关控制
- 数据库迁移可回滚
- Git 分支管理

### 4. 文档同步
- 代码和文档同步更新
- 每完成一个 Week 提交一次代码

---

## 📚 参考文档

详细设计文档位于 `docs/Agent/tasks/`:
- `00_实施总览.md` - 项目背景和目标
- `01_改造原则和目标.md` - 设计原则和技术选型
- `02_技术架构设计.md` - 完整技术架构
- `03_Memory系统设计.md` - Memory详细设计
- `04_工具系统设计.md` - 工具系统详细设计
- `05_版本管理设计.md` - 版本管理详细设计
- `09_实施路线图.md` - 完整路线图
- `10_阶段一任务清单.md` - 阶段一详细任务
- `18_快速开始指南.md` - 环境准备和快速体验

---

## 🎯 下一步行动

1. **立即开始**: 阅读 `03_Memory系统设计.md`，理解Memory系统的详细设计
2. **环境准备**: 参考 `18_快速开始指南.md` 配置开发环境
3. **开始开发**: 按照 Week 1 Day 1-2 的任务开始设计 MemoryItem 数据结构

---

## 📞 Review 机制

- 每完成一个 Day 的任务，标记为完成
- 每完成一个 Week，进行 Review 并更新进度
- 遇到问题随时查阅 `docs/Agent/tasks/` 中的详细文档

---

**准备就绪，等待确认开始开发！** 🚀
