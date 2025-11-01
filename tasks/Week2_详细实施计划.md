# Week 2 详细实施计划 - 工具系统标准化

> **创建日期**: 2025-10-31
> **预计工期**: 5个工作日
> **状态**: 📋 计划完成

---

## 📊 现状分析

### 1. 现有代码结构

```
backend/app/services/agent/
├─ langgraph_agent.py          (1681行) - LangGraph工作流
├─ agents/                      - 各个子Agent
│  ├─ planning_agent.py
│  ├─ reflection_agent.py
│  └─ parallel_executor.py
├─ tools/                       - 工具目录
│  ├─ __init__.py              (12行) - 仅导出HITL
│  ├─ tool_registry.py         (482行) - ✅ 已有工具注册系统
│  ├─ consistency_checker.py   - 一致性检查工具
│  ├─ style_learning.py        - 风格学习工具
│  ├─ show_dont_tell.py        - Show不Tell工具
│  ├─ hitl.py                  - 人机协同工具
│  └─ hitl_nodes.py            - HITL节点
└─ memory/                      - 记忆系统(Week1已完成)
   ├─ types.py
   ├─ memory_strategy.py
   └─ enhanced_memory_manager.py
```

### 2. 现有tool_registry.py分析

#### ✅ 优点
- 已有完整的工具注册系统
- 支持工具元数据(ToolDefinition)
- 支持工具统计(ToolMetadata)
- 支持装饰器注册(@register_as_tool)
- 支持参数验证
- 支持工具调用统计

#### ⚠️ 不足
- **缺少强类型输入输出**: 当前使用Dict[str, Any]
- **缺少Pydantic验证**: 仅有简单的required参数检查
- **缺少工具分类枚举**: 使用字符串分类
- **缺少输出标准化**: 没有统一的ToolOutput格式
- **缺少日志记录**: 统计信息但无详细日志
- **缺少LangChain集成**: 没有to_langchain_tool()方法

### 3. 工具调用方式

**当前方式** (langgraph_agent.py):
```python
# 使用@tool装饰器定义工具
@tool
async def continue_writing_tool(...):
    pass

# 直接调用
result = await continue_writing_tool(...)
```

**目标方式** (设计文档):
```python
# 使用StandardTool + 强类型
tool = StandardTool(
    name="continue_writing",
    input_schema=ContinueWritingInput,
    output_schema=ContinueWritingOutput,
    executor=continue_writing_executor
)

# 通过registry调用
result = await registry.get_tool("continue_writing").execute(input_data)
```

---

## 🎯 改造策略

### 核心原则
1. **渐进式改造**: 不破坏现有功能
2. **向后兼容**: 保留旧接口作为过渡
3. **最小影响**: 改动范围限制在tools/目录

### 改造方式

#### 方案A: 完全重写 (❌不推荐)
- 删除现有tool_registry.py
- 按设计文档从0实现
- 风险大,改动多

#### 方案B: 增强现有代码 (✅推荐)
- 保留现有DynamicToolRegistry
- 新增StandardTool和类型系统
- 两套系统共存,逐步迁移
- 风险小,平滑过渡

### 选择方案B的实施步骤

```
Step 1: 创建tool_types.py (新增)
  ├─ ToolInput/ToolOutput基类
  ├─ ToolCategory枚举
  └─ StandardTool[InputT, OutputT]类

Step 2: 增强tool_registry.py (兼容模式)
  ├─ 保留DynamicToolRegistry
  ├─ 新增StandardToolRegistry
  └─ 提供统一的registry接口

Step 3: 创建writing_tools.py (新增)
  ├─ ContinueWritingInput/Output
  ├─ PolishTextInput/Output
  └─ 注册到registry

Step 4: 更新langgraph_agent.py (最小修改)
  └─ 使用新工具(可选),保持兼容

Step 5: 测试 (完整覆盖)
  └─ 确保两套系统都能工作
```

---

## 📅 5天详细任务分解

### Day 1: 类型系统 + 注册表增强

#### Task 1.1: 创建tool_types.py ⏱️ 2-3小时
**文件**: `backend/app/services/agent/tools/tool_types.py`

```python
# 需要实现的内容
class ToolInput(BaseModel):
    """工具输入基类"""
    pass

class ToolOutput(BaseModel):
    """工具输出基类"""
    success: bool
    message: str
    data: Any = None
    metadata: Dict[str, Any] = {}

class ToolCategory(str, Enum):
    """工具分类枚举"""
    WRITING = "writing"
    ANALYSIS = "analysis"
    MEMORY = "memory"
    VERSION = "version"
    QUALITY = "quality"
    UTILITY = "utility"

class StandardTool(Generic[InputT, OutputT]):
    """标准化工具基类"""
    def __init__(...)
    async def execute(self, input_data: InputT) -> OutputT
    def _log_execution(...)
    def to_langchain_tool(self)
```

**验收**:
- [ ] 类型定义完整
- [ ] Pydantic验证正常
- [ ] mypy类型检查通过

#### Task 1.2: 增强tool_registry.py ⏱️ 3-4小时
**文件**: `backend/app/services/agent/tools/tool_registry.py` (修改)

```python
# 新增内容
class StandardToolRegistry:
    """标准化工具注册表(兼容DynamicToolRegistry)"""

    def __init__(self):
        self._standard_tools: Dict[str, StandardTool] = {}
        self._dynamic_registry = DynamicToolRegistry()  # 保留旧系统

    def register_standard_tool(self, tool: StandardTool):
        """注册标准化工具"""
        pass

    def get_standard_tool(self, name: str) -> Optional[StandardTool]:
        """获取标准化工具"""
        pass

    # 兼容方法
    def call_tool(self, tool_id: str, parameters: Dict) -> Any:
        """调用工具(兼容两种类型)"""
        # 优先使用StandardTool
        if tool_id in self._standard_tools:
            tool = self._standard_tools[tool_id]
            # 自动转换Dict到Pydantic
            input_obj = tool.input_schema(**parameters)
            return await tool.execute(input_obj)

        # 回退到DynamicToolRegistry
        return await self._dynamic_registry.call_tool(tool_id, parameters)

# 导出统一接口
registry = StandardToolRegistry()
```

**验收**:
- [ ] StandardToolRegistry实现完整
- [ ] 与DynamicToolRegistry兼容
- [ ] 旧工具仍可正常调用

---

### Day 2: 基础写作工具改造

#### Task 2.1: 创建writing_tools.py ⏱️ 4-5小时
**文件**: `backend/app/services/agent/tools/writing_tools.py`

```python
# 需要实现的工具
1. continue_writing_tool
   - ContinueWritingInput(context, requirements, target_length, style)
   - ContinueWritingOutput(generated_text, word_count, quality_score)

2. polish_text_tool
   - PolishTextInput(content, aspect)
   - PolishTextOutput(polished_text, changes)

3. expand_text_tool
   - ExpandTextInput(content, target_length, direction)
   - ExpandTextOutput(expanded_text, added_length)
```

**实现要点**:
- 从langgraph_agent.py中提取现有工具逻辑
- 包装为StandardTool格式
- 保留原有AI Service调用
- 添加输入输出验证

**验收**:
- [ ] 3个工具实现完成
- [ ] 注册到registry
- [ ] 单元测试通过

#### Task 2.2: 更新__init__.py ⏱️ 30分钟
**文件**: `backend/app/services/agent/tools/__init__.py`

```python
# 新增导出
from .tool_types import ToolInput, ToolOutput, ToolCategory, StandardTool
from .tool_registry import registry
from .writing_tools import (
    continue_writing_tool,
    polish_text_tool,
    expand_text_tool
)

__all__ = [
    # 类型
    "ToolInput", "ToolOutput", "ToolCategory", "StandardTool",
    # 注册表
    "registry",
    # 工具
    "continue_writing_tool", "polish_text_tool", "expand_text_tool",
    # HITL (保留)
    "HITLManager", "ApprovalRequest", "ApprovalStatus"
]
```

---

### Day 3: 分析工具 + 工具监控

#### Task 3.1: 创建analysis_tools.py ⏱️ 3-4小时
**文件**: `backend/app/services/agent/tools/analysis_tools.py`

```python
# 需要实现的工具
1. analyze_content_tool
   - AnalyzeContentInput(content, aspects)
   - AnalyzeContentOutput(analysis, summary, scores)

2. evaluate_quality_tool
   - EvaluateQualityInput(content, context)
   - EvaluateQualityOutput(score, dimensions, feedback)
```

#### Task 3.2: 创建tool_monitor.py ⏱️ 2-3小时
**文件**: `backend/app/services/agent/tools/tool_monitor.py`

```python
class ToolMonitor:
    """工具调用监控"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def log_execution(
        self,
        tool_name: str,
        execution_time: float,
        success: bool,
        error: str = None
    ):
        """记录工具执行"""
        pass

    def get_tool_stats(
        self,
        tool_name: str,
        days: int = 1
    ) -> Dict[str, Any]:
        """获取工具统计"""
        pass
```

**集成到StandardTool**:
- 在execute()中调用monitor.log_execution()
- 记录到Redis

---

### Day 4: LangGraph集成

#### Task 4.1: 更新langgraph_agent.py ⏱️ 3-4小时
**修改**: 使用新工具系统(可选,不破坏现有功能)

```python
# 方式1: 继续使用@tool装饰器(不改)
@tool
async def continue_writing_tool(...):
    pass

# 方式2: 使用StandardTool(新增,共存)
from app.services.agent.tools import registry

async def continue_writing_via_registry(...):
    tool = registry.get_standard_tool("continue_writing")
    result = await tool.execute(input_data)
    return result
```

**改造策略**:
- 保留现有@tool工具
- 新增使用registry的版本
- 两套系统共存
- 逐步迁移

#### Task 4.2: 工具转换为LangChain Tool ⏱️ 2小时
**实现**: StandardTool.to_langchain_tool()

```python
def to_langchain_tool(self):
    """转换为 LangChain Tool"""
    from langchain.tools import Tool

    def sync_wrapper(**kwargs):
        import asyncio
        loop = asyncio.get_event_loop()
        input_obj = self.input_schema(**kwargs)
        return loop.run_until_complete(self.execute(input_obj))

    return Tool(
        name=self.name,
        description=self.description,
        func=sync_wrapper,
        args_schema=self.input_schema
    )
```

**测试**:
- [ ] 转换后的Tool可在LangChain中使用
- [ ] ToolNode可正常调用

---

### Day 5: 测试 + 文档

#### Task 5.1: 单元测试 ⏱️ 3-4小时
**文件**: `backend/tests/test_tools/`

```
test_tool_types.py          - 测试类型系统
test_tool_validation.py     - 测试输入输出验证
test_tool_execution.py      - 测试工具执行
test_tool_registry.py       - 测试注册表
test_writing_tools.py       - 测试写作工具
test_analysis_tools.py      - 测试分析工具
test_tool_monitor.py        - 测试监控
```

**覆盖率要求**: > 80%

#### Task 5.2: 集成测试 ⏱️ 2小时
**测试场景**:
1. 注册工具 → 调用工具 → 验证结果
2. 类型验证失败 → 抛出异常
3. 工具执行失败 → 记录统计
4. LangChain集成 → ToolNode调用

#### Task 5.3: 文档编写 ⏱️ 1-2小时
**文档**:
- `docs/工具系统使用手册.md`
- `tasks/Week2_完成总结.md`
- 代码内docstring完善

---

## 📊 验收标准

### 功能验收
- [ ] tool_types.py 创建完成,类型定义清晰
- [ ] tool_registry.py 增强完成,兼容旧系统
- [ ] writing_tools.py 创建完成,3个工具可用
- [ ] analysis_tools.py 创建完成,2个工具可用
- [ ] tool_monitor.py 创建完成,监控功能正常
- [ ] langgraph_agent.py 集成完成(可选)
- [ ] 所有工具都能转换为LangChain Tool

### 质量验收
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试全部通过
- [ ] mypy类型检查通过
- [ ] 无P0/P1问题

### 性能验收
- [ ] 工具调用成功率 > 99%
- [ ] 类型验证开销 < 10ms
- [ ] 工具执行延迟增加 < 50ms

### 兼容性验收
- [ ] 现有DynamicToolRegistry功能不受影响
- [ ] 现有@tool装饰器的工具正常工作
- [ ] langgraph_agent.py无功能退化

---

## 🔧 技术决策

### 决策1: 增强 vs 重写
**选择**: 增强现有代码
**原因**:
- 现有tool_registry.py已有完整功能
- 重写风险大,改动多
- 增强可实现渐进式迁移

### 决策2: 两套系统共存
**选择**: StandardToolRegistry + DynamicToolRegistry共存
**原因**:
- 保证向后兼容
- 降低迁移风险
- 给予足够的过渡时间

### 决策3: LangGraph集成方式
**选择**: 可选集成,不强制迁移
**原因**:
- langgraph_agent.py代码量大(1681行)
- 避免大规模重构
- 新功能可使用StandardTool

---

## 📁 交付清单

### 新增文件 (4个)
- [ ] `backend/app/services/agent/tools/tool_types.py` (~300行)
- [ ] `backend/app/services/agent/tools/writing_tools.py` (~200行)
- [ ] `backend/app/services/agent/tools/analysis_tools.py` (~150行)
- [ ] `backend/app/services/agent/tools/tool_monitor.py` (~100行)

### 修改文件 (2个)
- [ ] `backend/app/services/agent/tools/tool_registry.py` (+~150行)
- [ ] `backend/app/services/agent/tools/__init__.py` (+~20行)

### 测试文件 (7个)
- [ ] `backend/tests/test_tools/test_tool_types.py`
- [ ] `backend/tests/test_tools/test_tool_validation.py`
- [ ] `backend/tests/test_tools/test_tool_execution.py`
- [ ] `backend/tests/test_tools/test_tool_registry.py`
- [ ] `backend/tests/test_tools/test_writing_tools.py`
- [ ] `backend/tests/test_tools/test_analysis_tools.py`
- [ ] `backend/tests/test_tools/test_tool_monitor.py`

### 文档 (2个)
- [ ] `docs/工具系统使用手册.md`
- [ ] `tasks/Week2_完成总结.md`

---

## 🔍 风险和应对

### 风险1: 类型系统过于复杂
**影响**: 开发速度慢
**应对**: 先实现最小可用版本,后续迭代

### 风险2: 兼容性问题
**影响**: 现有功能受影响
**应对**: 充分测试,保留回退方案

### 风险3: 性能开销
**影响**: 工具调用变慢
**应对**: 性能测试,优化验证逻辑

---

## 📝 下一步

**立即开始**:
1. 创建 `tool_types.py`
2. 实现 `ToolInput/ToolOutput/ToolCategory`
3. 实现 `StandardTool` 基类

**或者**:
1. 先编写测试用例(TDD)
2. 再实现功能代码

---

**计划制定完成!** ✅

**建议下一步**: 开始 Day 1 Task 1.1 - 创建 tool_types.py
