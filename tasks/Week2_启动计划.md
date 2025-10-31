# Week 2 启动计划 - 工具系统标准化

> **开始日期**: 2025-10-31
> **预计完成**: 5个工作日
> **当前状态**: 准备开始

---

## 🎯 Week 2 目标

根据 `docs/Agent/tasks/09_实施路线图.md`:

### 核心目标
1. ✅ 实现标准化工具接口
2. ✅ 实现强类型输入输出
3. ✅ 改造现有工具
4. ✅ 工具调用统计

---

## 📅 任务分解 (5天)

### Day 1-2: 类型系统设计

#### Task 1.1: 创建工具类型定义
**文件**: `backend/app/services/agent/tools/tool_types.py`

**需要实现**:
```python
- ToolInput          # 输入基类
- ToolOutput         # 输出基类
- ToolCategory       # 工具分类枚举
- StandardTool       # 标准工具基类
```

**参考文档**: `docs/Agent/tasks/04_工具系统设计.md`

#### Task 1.2: 设计工具执行流程
- [ ] 输入验证 (Pydantic)
- [ ] 执行逻辑
- [ ] 输出验证
- [ ] 统计记录

#### Task 1.3: 编写工具装饰器
```python
@register_as_tool("tool_id", "category", "description")
async def my_tool(...):
    pass
```

---

### Day 3-4: 工具改造

#### Task 2.1: 改造 continue_writing_tool

**输入类型**:
```python
class ContinueWritingInput(ToolInput):
    context: str
    requirements: str
    target_length: int
```

**输出类型**:
```python
class ContinueWritingOutput(ToolOutput):
    generated_text: str
    word_count: int
    quality_score: float
```

#### Task 2.2: 改造 polish_text_tool
- 定义 PolishTextInput/Output
- 迁移现有逻辑

#### Task 2.3: 改造 analyze_text_tool
- 定义 AnalyzeTextInput/Output
- 迁移现有逻辑

#### Task 2.4: 更新 tool_registry.py
- 支持新的工具类型
- 添加工具调用统计
- 工具版本管理

---

### Day 5: 集成和测试

#### Task 3.1: 集成到 LangGraph
- 更新 `langgraph_agent.py`
- 使用新的工具接口

#### Task 3.2: 编写单元测试
```python
tests/test_tools/
├── test_tool_validation.py
├── test_tool_execution.py
└── test_tool_statistics.py
```

#### Task 3.3: 集成测试
- 端到端测试工具调用
- 验证类型安全
- 验证统计功能

---

## ✅ 交付物清单

### 代码文件
- [ ] `backend/app/services/agent/tools/tool_types.py` (新建)
- [ ] `backend/app/services/agent/tools/writing_tools.py` (重构)
- [ ] `backend/app/services/agent/tools/tool_registry.py` (更新)
- [ ] `backend/app/services/agent/langgraph_agent.py` (更新)

### 测试文件
- [ ] `backend/tests/test_tools/test_tool_validation.py`
- [ ] `backend/tests/test_tools/test_tool_execution.py`
- [ ] `backend/tests/test_tools/test_tool_statistics.py`

### 文档
- [ ] Week2_进度报告.md
- [ ] 工具系统使用手册.md

---

## 📊 验收标准

### 功能验收
- ✅ 所有工具改造完成
- ✅ 工具调用成功率 > 99%
- ✅ 类型检查通过 (mypy)

### 性能验收
- ✅ 工具调用延迟 < 50ms (验证开销)
- ✅ 统计功能无性能影响

### 质量验收
- ✅ 单元测试覆盖率 > 80%
- ✅ 集成测试通过
- ✅ 无P0/P1问题

---

## 🔍 需要了解的现有代码

### 1. 现有工具位置
```bash
backend/app/services/agent/tools/
├── __init__.py
├── tool_registry.py          # 需要查看
└── writing_tools.py           # 需要查看
```

### 2. LangGraph集成点
```bash
backend/app/services/agent/
├── langgraph_agent.py         # 需要查看
└── agents/
    └── writing_agent.py       # 可能需要查看
```

---

## 🚀 开始步骤

### Step 1: 了解现有代码
1. 查看现有 `tool_registry.py`
2. 查看现有 `writing_tools.py`
3. 了解当前工具调用方式

### Step 2: 创建类型系统
1. 创建 `tool_types.py`
2. 定义基础类型和接口
3. 编写工具装饰器

### Step 3: 逐步改造工具
1. 先改造一个工具作为示例
2. 验证可行性
3. 批量改造其他工具

### Step 4: 测试验证
1. 编写测试用例
2. 运行测试
3. 修复问题

---

## 💡 参考文档

- **核心设计**: `docs/Agent/tasks/04_工具系统设计.md`
- **实施路线**: `docs/Agent/tasks/09_实施路线图.md` (Week 2部分)
- **阶段一清单**: `docs/Agent/tasks/10_阶段一任务清单.md`

---

## ⚠️ 注意事项

### 1. 向后兼容
- 保留旧的工具接口作为临时兼容层
- 逐步迁移现有调用

### 2. 不影响现有功能
- 所有改动在 `/api/v1/agent/*` 范围内
- 不影响 `/api/v1/ai/*`

### 3. 测试驱动
- 先写测试
- 再写实现
- 确保覆盖率

---

## 📞 准备开始?

### 建议的开始方式:

**选项1: 直接开始** (推荐)
```
1. 查看现有工具代码
2. 创建 tool_types.py
3. 开始实现
```

**选项2: 先做调研**
```
1. 详细阅读设计文档
2. 分析现有代码结构
3. 制定详细计划
4. 再开始实现
```

**选项3: 渐进式**
```
1. 先实现最小可用版本
2. 测试验证
3. 逐步增强功能
```

---

**您想从哪里开始?**

我建议选择 **选项1: 直接开始**,因为:
- ✅ Week 1 经验丰富
- ✅ 设计文档已经很清晰
- ✅ 可以边做边调整

您觉得怎么样?
