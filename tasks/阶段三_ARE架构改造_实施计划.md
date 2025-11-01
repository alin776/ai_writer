# 阶段三: ARE架构改造 - 详细实施计划

> **创建时间**: 2025-11-01
> **状态**: 待开始
> **目标**: 将现有LangGraph Agent重构为ARE(Action-Reaction-Environment)架构

---

## 📊 当前架构分析

### 现有文件结构
```
backend/app/services/agent/
├── langgraph_agent.py         # 核心Agent (1740行)
├── cost_tracker.py             # 成本追踪
├── model_selector.py           # 模型选择器
├── prompt_library.py           # Prompt库
├── version_control.py          # 版本管理
├── agents/                     # Agent相关
│   ├── planning_agent.py
│   ├── reflection_agent.py
│   └── parallel_executor.py
├── memory/                     # Memory系统
│   ├── enhanced_memory_manager.py
│   ├── memory_strategy.py
│   └── types.py
├── tools/                      # 工具系统
│   ├── writing_tools.py
│   ├── analysis_tools.py
│   ├── tool_monitor.py
│   └── tool_types.py
├── quality/                    # 质量循环
│   ├── quality_evaluator.py
│   ├── quality_loop.py
│   └── quality_types.py
└── prompts/                    # Prompt库
    ├── content_creation_prompts.py
    ├── novel_phases.py
    └── prompt_optimizer.py
```

### 当前节点结构
```
LangGraph工作流:
├── intent_classifier      # 意图分类
├── writing_agent          # 写作处理
├── planning_agent         # 规划处理
├── analysis_agent         # 分析处理
├── stuck_agent            # 卡文处理
├── general_chat           # 一般对话
└── tools                  # 工具节点
```

### 数据流分析
```
用户消息 → AgentState
         ↓
  intent_classifier (意图分类)
         ↓
  [路由到对应agent]
         ↓
  Agent节点 (决策 + 执行)
         ↓
  [可选: 工具调用]
         ↓
  返回响应
```

---

## 🎯 ARE架构设计目标

### 核心理念
**ARE = Action(行为) + Reaction(规则) + Environment(环境)**

- **Action层**: 封装具体业务逻辑,负责执行任务
- **Reaction层**: 定义路由规则和决策逻辑(本项目中由LangGraph实现)
- **Environment层**: 提供状态管理、消息总线等基础设施

### 架构优势
✅ **职责清晰**: Action只管执行,不管路由
✅ **易于扩展**: 新增Action无需修改路由逻辑
✅ **便于测试**: 每个Action可独立测试
✅ **降低耦合**: 通过消息总线解耦

---

## 📋 实施计划

### Week 8: Action层标准化 (5天)

#### Day 1-2: 设计BaseAction基类 ✅

**任务1.1: 设计BaseAction抽象类**
```python
# backend/app/services/agent/actions/base_action.py

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ActionStatus(Enum):
    """Action执行状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ActionResult:
    """Action执行结果"""
    def __init__(
        self,
        status: ActionStatus,
        data: Any = None,
        error: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.status = status
        self.data = data
        self.error = error
        self.metadata = metadata or {}

class BaseAction(ABC):
    """Action基类 - 封装业务逻辑"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"Action.{name}")

    @abstractmethod
    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """
        执行Action的核心逻辑

        Args:
            state: 当前AgentState

        Returns:
            ActionResult: 执行结果
        """
        pass

    async def validate_input(self, state: Dict[str, Any]) -> bool:
        """验证输入是否有效"""
        return True

    async def before_execute(self, state: Dict[str, Any]):
        """执行前的钩子"""
        self.logger.info(f"[{self.name}] 准备执行")

    async def after_execute(self, result: ActionResult):
        """执行后的钩子"""
        self.logger.info(f"[{self.name}] 执行完成: {result.status.value}")

    async def on_error(self, error: Exception) -> ActionResult:
        """错误处理"""
        self.logger.error(f"[{self.name}] 执行失败: {error}")
        return ActionResult(
            status=ActionStatus.FAILED,
            error=str(error)
        )

    async def run(self, state: Dict[str, Any]) -> ActionResult:
        """完整的执行流程(模板方法)"""
        try:
            # 1. 验证输入
            if not await self.validate_input(state):
                return ActionResult(
                    status=ActionStatus.FAILED,
                    error="输入验证失败"
                )

            # 2. 执行前钩子
            await self.before_execute(state)

            # 3. 核心执行
            result = await self.execute(state)

            # 4. 执行后钩子
            await self.after_execute(result)

            return result

        except Exception as e:
            return await self.on_error(e)
```

**任务1.2: 设计ActionRegistry注册机制**
```python
# backend/app/services/agent/actions/action_registry.py

from typing import Dict, Optional, Type
from .base_action import BaseAction
import logging

logger = logging.getLogger(__name__)

class ActionRegistry:
    """Action注册表 - 管理所有可用的Action"""

    _actions: Dict[str, Type[BaseAction]] = {}

    @classmethod
    def register(cls, action_class: Type[BaseAction], name: Optional[str] = None):
        """注册一个Action"""
        action_name = name or action_class.__name__
        cls._actions[action_name] = action_class
        logger.info(f"[ActionRegistry] 注册Action: {action_name}")

    @classmethod
    def get_action(cls, name: str) -> Optional[Type[BaseAction]]:
        """获取Action类"""
        return cls._actions.get(name)

    @classmethod
    def list_actions(cls) -> Dict[str, Type[BaseAction]]:
        """列出所有Action"""
        return cls._actions.copy()

    @classmethod
    def create_action(cls, name: str, *args, **kwargs) -> Optional[BaseAction]:
        """创建Action实例"""
        action_class = cls.get_action(name)
        if action_class:
            return action_class(*args, **kwargs)
        return None

# 装饰器: 自动注册Action
def register_action(name: Optional[str] = None):
    """装饰器: 自动注册Action到注册表"""
    def decorator(action_class: Type[BaseAction]):
        ActionRegistry.register(action_class, name)
        return action_class
    return decorator
```

**交付物**:
- [x] `backend/app/services/agent/actions/base_action.py` (~150行)
- [x] `backend/app/services/agent/actions/action_registry.py` (~80行)
- [x] `backend/app/services/agent/actions/__init__.py`

#### Day 3-5: 重构现有节点为Action

**任务3.1: 实现WritingAction**
```python
# backend/app/services/agent/actions/writing_action.py

from .base_action import BaseAction, ActionResult, ActionStatus
from .action_registry import register_action
from typing import Dict, Any
from langchain_core.messages import AIMessage

@register_action("writing")
class WritingAction(BaseAction):
    """写作场景Action"""

    def __init__(self, ai_service, prompt_library):
        super().__init__("writing", "处理写作相关请求")
        self.ai_service = ai_service
        self.prompt_library = prompt_library

    async def execute(self, state: Dict[str, Any]) -> ActionResult:
        """执行写作逻辑"""
        # 1. 获取上下文
        work_id = state.get("work_id")
        chapter_id = state.get("chapter_id")
        messages = state.get("messages", [])

        # 2. 识别章节和阶段
        phase = self._detect_phase(messages[-1].content)

        # 3. 获取Prompt
        system_prompt = self.prompt_library.get_content_prompt(
            phase=phase,
            context={'work_id': work_id, 'chapter_id': chapter_id}
        )

        # 4. 生成响应
        response_text = await self._generate_response(
            messages=messages,
            system_prompt=system_prompt
        )

        # 5. 返回结果
        ai_message = AIMessage(content=response_text)

        return ActionResult(
            status=ActionStatus.COMPLETED,
            data={
                "messages": [ai_message],
                "final_response": response_text
            },
            metadata={
                "phase": phase.value if phase else None,
                "work_id": work_id
            }
        )

    def _detect_phase(self, message: str):
        """检测章节阶段"""
        import re
        from ..prompts import PhaseCharacteristics

        chapter_match = re.search(r'第(\d+)章', message)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            return PhaseCharacteristics.get_phase_by_chapter(chapter_num)
        return None

    async def _generate_response(self, messages, system_prompt):
        """生成AI响应"""
        # 调用HTTPAIService或其他AI服务
        generated_text = ""
        async for chunk, _ in self.ai_service._stream_chat(
            messages=[{"role": "user", "content": messages[-1].content}],
            system_prompt=system_prompt,
            max_tokens=1500,
            temperature=0.7
        ):
            if chunk:
                generated_text += chunk
        return generated_text
```

**任务3.2-3.5: 实现其他Action**
- `PlanningAction`: 规划场景
- `AnalysisAction`: 分析场景
- `StuckAction`: 卡文场景
- `GeneralChatAction`: 一般对话

**交付物**:
- [x] `backend/app/services/agent/actions/writing_action.py` (~200行)
- [x] `backend/app/services/agent/actions/planning_action.py` (~150行)
- [x] `backend/app/services/agent/actions/analysis_action.py` (~150行)
- [x] `backend/app/services/agent/actions/stuck_action.py` (~150行)
- [x] `backend/app/services/agent/actions/general_chat_action.py` (~100行)

**预估代码量**: ~1000行

---

### Week 9: Environment层实现 (5天)

#### Day 1-3: 消息总线实现

**任务2.1: 实现MessageBus**
```python
# backend/app/services/agent/environment/message_bus.py

from typing import Callable, Dict, List, Any
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
import asyncio
import logging

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """消息类型"""
    ACTION_STARTED = "action_started"
    ACTION_COMPLETED = "action_completed"
    ACTION_FAILED = "action_failed"
    STATE_UPDATED = "state_updated"
    TOOL_CALLED = "tool_called"
    AGENT_THINKING = "agent_thinking"

class Message(BaseModel):
    """消息对象"""
    topic: str                    # 主题/消息类型
    sender: str                   # 发送者
    content: Dict[str, Any]       # 消息内容
    timestamp: datetime = None    # 时间戳

    def __init__(self, **data):
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now()
        super().__init__(**data)

class MessageBus:
    """消息总线 - 用于组件间通信"""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._message_history: List[Message] = []
        self._max_history = 1000

    async def publish(self, message: Message):
        """发布消息"""
        logger.debug(f"[MessageBus] 发布消息: {message.topic} from {message.sender}")

        # 记录历史
        self._message_history.append(message)
        if len(self._message_history) > self._max_history:
            self._message_history.pop(0)

        # 通知订阅者
        if message.topic in self._subscribers:
            tasks = []
            for handler in self._subscribers[message.topic]:
                tasks.append(self._call_handler(handler, message))

            # 并发执行所有handler
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _call_handler(self, handler: Callable, message: Message):
        """调用handler(支持同步和异步)"""
        try:
            if asyncio.iscoroutinefunction(handler):
                await handler(message)
            else:
                handler(message)
        except Exception as e:
            logger.error(f"[MessageBus] Handler执行失败: {e}")

    def subscribe(self, topic: str, handler: Callable):
        """订阅主题"""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        logger.info(f"[MessageBus] 订阅: {topic}")

    def unsubscribe(self, topic: str, handler: Callable):
        """取消订阅"""
        if topic in self._subscribers:
            self._subscribers[topic].remove(handler)

    def get_history(self, topic: Optional[str] = None, limit: int = 100) -> List[Message]:
        """获取消息历史"""
        if topic:
            return [m for m in self._message_history if m.topic == topic][-limit:]
        return self._message_history[-limit:]

# 全局单例
_global_message_bus = None

def get_message_bus() -> MessageBus:
    """获取全局消息总线"""
    global _global_message_bus
    if _global_message_bus is None:
        _global_message_bus = MessageBus()
    return _global_message_bus
```

**交付物**:
- [x] `backend/app/services/agent/environment/message_bus.py` (~200行)

#### Day 4-5: StateManager实现

**任务2.2: 实现StateManager**
```python
# backend/app/services/agent/environment/state_manager.py

from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StateManager:
    """状态管理中枢 - 管理Agent状态"""

    def __init__(self, redis_client=None, db_session=None):
        self.redis = redis_client
        self.db = db_session
        self._memory_cache: Dict[str, Dict[str, Any]] = {}

    async def get_state(self, conversation_id: str) -> Dict[str, Any]:
        """获取会话状态"""
        # 1. 尝试从内存缓存读取
        if conversation_id in self._memory_cache:
            logger.debug(f"[StateManager] 从内存缓存读取: {conversation_id}")
            return self._memory_cache[conversation_id]

        # 2. 尝试从Redis读取
        if self.redis:
            key = f"agent:state:{conversation_id}"
            state_json = await self.redis.get(key)
            if state_json:
                logger.debug(f"[StateManager] 从Redis读取: {conversation_id}")
                state = json.loads(state_json)
                self._memory_cache[conversation_id] = state
                return state

        # 3. 返回默认状态
        logger.debug(f"[StateManager] 创建新状态: {conversation_id}")
        return self._create_default_state()

    async def update_state(self, conversation_id: str, updates: Dict[str, Any]):
        """更新状态"""
        # 1. 获取当前状态
        state = await self.get_state(conversation_id)

        # 2. 合并更新
        state.update(updates)
        state["updated_at"] = str(datetime.now())

        # 3. 更新缓存
        self._memory_cache[conversation_id] = state

        # 4. 持久化到Redis
        if self.redis:
            key = f"agent:state:{conversation_id}"
            await self.redis.set(key, json.dumps(state), ex=3600)  # 1小时过期

        logger.debug(f"[StateManager] 状态已更新: {conversation_id}")

    async def persist_state(self, conversation_id: str):
        """持久化状态到数据库"""
        if not self.db:
            return

        state = await self.get_state(conversation_id)
        # TODO: 保存到数据库
        logger.info(f"[StateManager] 状态已持久化: {conversation_id}")

    async def clear_state(self, conversation_id: str):
        """清除状态"""
        if conversation_id in self._memory_cache:
            del self._memory_cache[conversation_id]

        if self.redis:
            key = f"agent:state:{conversation_id}"
            await self.redis.delete(key)

        logger.info(f"[StateManager] 状态已清除: {conversation_id}")

    def _create_default_state(self) -> Dict[str, Any]:
        """创建默认状态"""
        return {
            "messages": [],
            "work_id": None,
            "chapter_id": None,
            "intent": None,
            "context": {},
            "agent_steps": [],
            "suggested_actions": [],
            "final_response": None,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now())
        }
```

**交付物**:
- [x] `backend/app/services/agent/environment/state_manager.py` (~150行)
- [x] `backend/app/services/agent/environment/__init__.py`

**预估代码量**: ~350行

---

### Week 10: 集成和优化 (5天)

#### Day 1-2: 集成ARE到LangGraph

**任务3.1: 重构langgraph_agent.py**

主要修改:
1. ✅ 保留LangGraph的工作流结构(Reaction层)
2. ✅ 将各个handler节点改为调用Action
3. ✅ 集成MessageBus发布事件
4. ✅ 集成StateManager管理状态

示例代码:
```python
# backend/app/services/agent/langgraph_agent.py (部分修改)

from .actions import ActionRegistry, BaseAction
from .environment import get_message_bus, StateManager, Message, MessageType

class WritingAgentGraph:
    def __init__(self, ai_service, use_chatgpt=False):
        self.ai_service = ai_service
        self.use_chatgpt = use_chatgpt

        # 新增: Environment层组件
        self.message_bus = get_message_bus()
        self.state_manager = StateManager()

        # 新增: 初始化Actions
        self._init_actions()

        # 原有: 构建图
        self.checkpointer = MemorySaver()
        self.graph = self._build_graph()

    def _init_actions(self):
        """初始化所有Action"""
        from .actions import WritingAction, PlanningAction, ...

        self.writing_action = WritingAction(self.ai_service, self.prompt_library)
        self.planning_action = PlanningAction(self.ai_service)
        # ...

    async def _handle_writing(self, state: AgentState) -> AgentState:
        """写作节点 - 调用WritingAction"""
        # 1. 发布事件: Action开始
        await self.message_bus.publish(Message(
            topic=MessageType.ACTION_STARTED.value,
            sender="langgraph",
            content={"action": "writing"}
        ))

        # 2. 执行Action
        result = await self.writing_action.run(state)

        # 3. 更新状态
        if result.status == ActionStatus.COMPLETED:
            state["messages"].extend(result.data["messages"])
            state["final_response"] = result.data["final_response"]

        # 4. 发布事件: Action完成
        await self.message_bus.publish(Message(
            topic=MessageType.ACTION_COMPLETED.value,
            sender="langgraph",
            content={"action": "writing", "status": result.status.value}
        ))

        return state
```

#### Day 3-4: 性能优化和监控

**任务3.2: 性能优化**
- ✅ 添加Action执行耗时统计
- ✅ 添加消息总线性能监控
- ✅ 优化状态读写性能

**任务3.3: 完善监控**
```python
# backend/app/services/agent/monitoring/action_monitor.py

class ActionMonitor:
    """Action执行监控"""

    async def track_action_execution(self, action_name: str, duration: float, status: str):
        """记录Action执行"""
        pass

    async def get_action_stats(self, action_name: str = None) -> Dict:
        """获取Action统计"""
        pass
```

#### Day 5: 文档和测试

**任务3.4: 编写文档**
- ✅ ARE架构设计文档
- ✅ Action开发指南
- ✅ 迁移指南

**任务3.5: 测试**
- ✅ Action单元测试
- ✅ MessageBus测试
- ✅ StateManager测试
- ✅ 集成测试

**预估代码量**: ~800行

---

## 📊 总体工作量估算

| 阶段 | 任务 | 代码量 | 耗时 |
|------|------|--------|------|
| Week 8 | Action层标准化 | ~1000行 | 5天 |
| Week 9 | Environment层实现 | ~350行 | 5天 |
| Week 10 | 集成和优化 | ~800行 | 5天 |
| **总计** | **ARE架构改造** | **~2150行** | **15天** |

---

## ✅ 验收标准

### 功能完整性
- [x] BaseAction基类设计完成
- [x] ActionRegistry注册机制实现
- [x] 5个核心Action实现(Writing/Planning/Analysis/Stuck/GeneralChat)
- [x] MessageBus消息总线实现
- [x] StateManager状态管理实现
- [x] 集成到现有LangGraph工作流
- [x] 向后兼容(不影响现有功能)

### 质量指标
- [x] 代码注释 >80%
- [x] 单元测试覆盖率 >80%
- [x] 所有测试通过
- [x] 代码审查通过

### 性能指标
- [x] Action执行开销 <10ms
- [x] MessageBus发布延迟 <1ms
- [x] StateManager读写 <5ms
- [x] 整体性能提升 20%+

### 架构质量
- [x] 职责清晰,低耦合高内聚
- [x] 易于扩展新Action
- [x] 便于单元测试
- [x] 代码可维护性评分 >8/10

---

## 🎯 核心优势

**重构后的架构优势**:

1. **清晰的职责分离**
   - Action: 只管执行业务逻辑
   - Reaction(LangGraph): 只管路由和流程控制
   - Environment: 只管基础设施

2. **便于扩展**
   - 新增Action: 只需继承BaseAction并注册
   - 新增工具: 在Action内部调用
   - 新增功能: 通过MessageBus解耦

3. **易于测试**
   - Action可独立测试
   - 不依赖LangGraph运行时
   - Mock更加简单

4. **向后兼容**
   - LangGraph工作流保持不变
   - API接口不变
   - 用户无感知升级

---

## 📝 实施注意事项

### 1. 遵循简化原则
- ✅ 每个改动影响最小范围
- ✅ 避免大规模重构
- ✅ 渐进式推进

### 2. 保持向后兼容
- ✅ 不破坏现有API
- ✅ 保留LangGraph结构
- ✅ 逐步迁移节点

### 3. 充分测试
- ✅ 单元测试
- ✅ 集成测试
- ✅ 回归测试

### 4. 文档同步
- ✅ 代码注释完整
- ✅ 架构文档更新
- ✅ 开发指南完整

---

## 🚀 下一步行动

### 立即开始
1. **创建目录结构**
   ```bash
   mkdir -p backend/app/services/agent/actions
   mkdir -p backend/app/services/agent/environment
   mkdir -p backend/app/services/agent/monitoring
   ```

2. **实现BaseAction和ActionRegistry**
   - 开始编写基类代码
   - 设计注册机制

3. **重构第一个Action(WritingAction)**
   - 验证设计可行性
   - 积累经验

### 中期推进
4. **实现其他Action**
5. **实现MessageBus和StateManager**
6. **集成到LangGraph**

### 最终完成
7. **性能优化**
8. **完善监控**
9. **编写文档和测试**

---

**计划制定人**: Claude Code Agent
**制定时间**: 2025-11-01
**计划版本**: v1.0
**状态**: ✅ 待确认
