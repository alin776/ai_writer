# Day 8-11: 自适应Token分配 🎯

> ⚠️ **文档性质：规划文档 - 功能尚未实施**
>
> - ❌ **实施状态**: 未开始（0%）
> - 📝 **实际情况**: AdaptiveBudget类不存在
> - 🔍 **代码现状**: 只有固定的TokenBudget类（models.py:90-119）
> - 📊 **详细状态**: 查看 [`IMPLEMENTATION_STATUS.md`](./IMPLEMENTATION_STATUS.md#5-自适应token分配文档05)
> - 💡 **建议**: 优先级较低，可在阶段一完成后评估

---

> 动态优化Token预算，提升使用效率
>
> **优先级**: P2 - 优化（可选）
> **工期**: 4天
> **难度**: ⭐⭐⭐⭐ 较复杂
> **依赖**: Day 1-7完成并稳定

---

## 任务目标

根据不同任务类型，动态调整Token预算分配。

---

## 核心思路

### 固定预算 vs 自适应预算

**当前（固定）**:
```python
TokenBudget(
    system_prompt=0.20,  # 20%
    summary=0.25,        # 25%
    short_memory=0.35,   # 35%
    tools=0.15,          # 15%
    reserved=0.05        # 5%
)
```

**目标（自适应）**:
```python
# 创作任务
AdaptiveBudget(
    task_type="CREATIVE",
    system_prompt=0.15,   # ↓ 减少系统提示
    summary=0.20,         # ↓ 减少摘要
    short_memory=0.50,    # ↑ 增加对话历史
    tools=0.10,
    reserved=0.05
)

# 分析任务
AdaptiveBudget(
    task_type="ANALYTICAL",
    system_prompt=0.25,   # ↑ 增加系统指导
    summary=0.15,
    short_memory=0.30,
    tools=0.25,           # ↑ 增加工具结果
    reserved=0.05
)
```

---

## 实施步骤

### 1. 创建AdaptiveBudget类

**新建文件**: `backend/app/services/context/adaptive_budget.py`

```python
from enum import Enum
from dataclasses import dataclass

class TaskType(Enum):
    """任务类型"""
    CREATIVE = "creative"       # 创作（小说、文章）
    ANALYTICAL = "analytical"   # 分析（总结、评价）
    QA = "qa"                   # 问答
    CHAT = "chat"               # 闲聊

@dataclass
class AdaptiveBudget:
    """自适应Token预算"""
    
    # 预算模板
    BUDGETS = {
        TaskType.CREATIVE: {
            "system_prompt": 0.15,
            "summary": 0.20,
            "short_memory": 0.50,
            "tools": 0.10,
            "reserved": 0.05
        },
        TaskType.ANALYTICAL: {
            "system_prompt": 0.25,
            "summary": 0.15,
            "short_memory": 0.30,
            "tools": 0.25,
            "reserved": 0.05
        },
        TaskType.QA: {
            "system_prompt": 0.20,
            "summary": 0.25,
            "short_memory": 0.35,
            "tools": 0.15,
            "reserved": 0.05
        },
        TaskType.CHAT: {
            "system_prompt": 0.10,
            "summary": 0.15,
            "short_memory": 0.60,
            "tools": 0.10,
            "reserved": 0.05
        }
    }
    
    def get_budget(self, task_type: TaskType) -> dict:
        """获取指定任务类型的预算"""
        return self.BUDGETS.get(task_type, self.BUDGETS[TaskType.QA])
```

---

### 2. 集成到ContextManager

```python
class ContextManager:
    def __init__(
        self,
        ...,
        enable_adaptive_budget: bool = False
    ):
        self.enable_adaptive_budget = enable_adaptive_budget
        if enable_adaptive_budget:
            self.adaptive_budget = AdaptiveBudget()
    
    async def build_context(
        self,
        session_id: str,
        system_prompt: str = "",
        task_type: TaskType = TaskType.QA
    ):
        # 根据任务类型选择预算
        if self.enable_adaptive_budget:
            budget = self.adaptive_budget.get_budget(task_type)
        else:
            budget = self.token_budget
        
        # 使用预算构建上下文
        ...
```

---

### 3. 测试和优化

```python
async def test_adaptive_budget():
    manager = ContextManager(enable_adaptive_budget=True)
    
    # 测试创作任务
    creative_result = await manager.build_context(
        "session_1",
        task_type=TaskType.CREATIVE
    )
    
    # 验证预算分配
    # 创作任务应该有更多短期记忆
```

---

## 验收标准

- [ ] AdaptiveBudget实现完成
- [ ] 4种任务类型预算配置
- [ ] ContextManager集成
- [ ] A/B测试验证效果

---

## 效果预期

- Token利用率提升 20%
- 不同任务类型体验优化

---

**完整实施细节请参考v1.1文档 1902-2111行**

---

## 下一步

阶段一完成！可选进入 [06_扩展方案_向量检索长期记忆.md](./06_扩展方案_向量检索长期记忆.md)
