# P0-03：重构_handle_with_httpai方法

## 📋 基本信息

| 项目 | 内容 |
|------|------|
| **优先级** | P0（必须立即修复） |
| **影响范围** | Agent核心逻辑 |
| **工作量估算** | 5-7天（316行方法重构很复杂，需要仔细测试） |
| **前置依赖** | P0-01（修复task_type） |
| **后续依赖** | P1所有优化 |
| **状态** | 📋 设计完成 | 🚧 实施待开始 |

---

## 🚨 问题描述

### 核心问题

**`_handle_with_httpai()` 方法有316行，违反单一职责原则，做了8件事情，无法维护和测试。**

### 方法职责分析

**当前方法的8个职责**：

```python
async def _handle_with_httpai(self, state, agent_type, system_prompt):
    """HTTPAIService 模式 - 手动工具调用（绕过 Cloudflare）"""

    # 职责1: 判断执行阶段（第一次 vs 第二次）
    if messages and isinstance(messages[-1], ToolMessage):
        # ========== 第二次进入：处理工具结果 ==========
        # 职责2-5: 各种复杂逻辑
        ...

    # ========== 第一次进入：工具决策 ==========
    # 职责6-8: 工具决策、调用、解析
    ...
```

**问题严重性**：
- 圈复杂度：~25（正常应<10）
- 行数：316行（正常应<50行）
- 职责数：8个（应该1个）
- 可测试性：❌ 几乎无法单元测试

---

## 💡 重构方案设计

### 重构目标结构

```python
# 原方法：316行，8个职责
async def _handle_with_httpai(state, agent_type, system_prompt):
    """316行的巨型方法"""
    ...

# ========== 重构后 ==========

# 主入口：20-30行，只做流程编排
async def _handle_with_httpai(state, agent_type, system_prompt):
    """HTTPAIService模式的主入口"""
    messages = state["messages"]

    # 判断执行阶段
    if self._is_tool_result_stage(messages):
        # 第二次进入：处理工具结果
        return await self._handle_tool_result(state, agent_type, system_prompt)
    else:
        # 第一次进入：工具决策
        return await self._handle_tool_decision(state, agent_type, system_prompt)


# ========== 拆分为20个子方法 ==========
# 每个方法只做一件事，可单独测试
```

---

## 🔧 实施步骤

### Step 1：创建新的处理器类

**文件**：`backend/app/services/agent/httpai_handler.py`

```python
"""
HTTPAIService模式的Agent处理器
"""
from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from app.services.agent.model_selector import TaskType
import logging

logger = logging.getLogger(__name__)


class HTTPAIHandler:
    """HTTPAIService模式的处理器类"""

    def __init__(self, ai_service, global_state_accessor):
        self.ai_service = ai_service
        self.get_state_value = global_state_accessor

    # ========== 主入口 ==========

    async def handle(
        self,
        state: Dict[str, Any],
        agent_type: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """HTTPAIService模式的主入口"""
        messages = state["messages"]

        # 判断执行阶段
        if self._is_tool_result_stage(messages):
            # 第二次进入：处理工具结果
            return await self._handle_tool_result(state, agent_type, system_prompt)
        else:
            # 第一次进入：工具决策
            return await self._handle_tool_decision(state, agent_type, system_prompt)

    # ========== 工具结果处理分支 ==========

    def _is_tool_result_stage(self, messages: list) -> bool:
        """判断是否处于处理工具结果阶段"""
        return messages and isinstance(messages[-1], ToolMessage)

    async def _handle_tool_result(
        self,
        state: Dict[str, Any],
        agent_type: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """处理工具执行结果，生成最终响应"""
        # 提取数据
        user_message = self._extract_user_message(state["messages"])
        tool_result = self._extract_tool_result(state["messages"])

        # 构建prompt
        final_prompt = self._build_final_prompt(
            agent_type=agent_type,
            system_prompt=system_prompt,
            user_message=user_message,
            tool_result=tool_result
        )

        # 生成响应
        final_text = await self._generate_final_response(
            prompt=final_prompt,
            agent_type=agent_type
        )

        # 返回结果
        return self._create_final_response_state(final_text, agent_type)

    # ========== 工具决策分支 ==========

    async def _handle_tool_decision(
        self,
        state: Dict[str, Any],
        agent_type: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """第一次进入：决定是否需要工具"""
        last_user_message = state["messages"][-1].content

        # 构建决策prompt
        decision_prompt = self._build_decision_prompt(system_prompt, last_user_message)

        # 调用LLM做决策
        decision_text = await self._generate_decision(decision_prompt)

        # 解析决策
        decision = self._parse_decision(decision_text)

        # 执行决策
        if decision.get("need_tools"):
            return await self._execute_tool_and_recurse(state, agent_type, system_prompt, decision)
        else:
            return self._create_direct_response(decision, agent_type)

    # ========== 其他辅助方法 ==========
    # （省略详细实现，每个方法15-30行）
```

### Step 2：在主类中集成新处理器

**文件**：`backend/app/services/agent/langgraph_agent.py`

```python
class WritingAgentGraph:
    def __init__(self, ai_service, use_chatgpt=False):
        # ... 现有初始化代码

        # 初始化HTTPAI处理器
        self.httpai_handler = HTTPAIHandler(
            ai_service=ai_service,
            global_state_accessor=self._get_state_value
        )

    def _get_state_value(self, key: str, default: Any = None) -> Any:
        """获取state中的值（供handler使用）"""
        # 这里需要根据实际情况实现
        return getattr(self, f"_{key}", default)

    async def _handle_with_httpai(self, state, agent_type, system_prompt):
        """重构后的方法 - 现在只是委托给handler"""
        logger.info(f"[LangGraph] 委托给HTTPAIHandler处理 {agent_type}")
        return await self.httpai_handler.handle(state, agent_type, system_prompt)
```

### Step 3：实现Prompt构建器

**文件**：`backend/app/services/agent/httpai_prompts.py`

```python
class HTTPAIPromptBuilder:
    """Prompt构建器"""

    @staticmethod
    def build_final_prompt(agent_type, system_prompt, user_message, tool_result):
        """根据agent类型构建最终prompt"""
        # 检测用户意图
        intent = HTTPAIPromptBuilder._detect_user_intent(user_message)

        # 根据agent_type选择构建方法
        if agent_type == "writing":
            return HTTPAIPromptBuilder._build_writing_prompt(
                system_prompt, user_message, tool_result, intent
            )
        elif agent_type == "stuck":
            return HTTPAIPromptBuilder._build_stuck_prompt(...)
        # ... 其他类型

    @staticmethod
    def _build_writing_prompt(system_prompt, user_message, tool_result, intent):
        """构建writing agent的prompt"""
        if intent == "read":
            # 用户想查看内容
            return f"""{system_prompt}

用户请求：{user_message}
工具返回：{tool_result}
请按格式展示..."""
        else:
            # 用户想创作
            return f"""{system_prompt}

用户请求：{user_message}
工具返回：{tool_result}
请基于上下文续写..."""

    # ... 其他prompt构建方法
```

### Step 4：实现工具调用管理器

**文件**：`backend/app/services/agent/tool_manager.py`

```python
class ToolManager:
    """统一的工具调用管理器"""

    def __init__(self, tools_dict):
        self.tools = tools_dict

    async def invoke_tool(self, tool_name: str, tool_args: dict) -> str:
        """统一的工具调用接口"""
        tool = self.tools.get(tool_name)

        if not tool:
            logger.warning(f"[Tool] 未知工具: {tool_name}")
            return f"错误：未知工具 {tool_name}"

        try:
            result = await tool.ainvoke(tool_args)
            logger.info(f"[Tool] {tool_name} 执行成功，结果长度: {len(result)}")
            return result
        except Exception as e:
            logger.error(f"[Tool] {tool_name} 执行失败: {e}")
            return f"工具执行失败: {str(e)}"

    def normalize_tool_params(self, tool_name: str, tool_args: dict, state: dict) -> dict:
        """标准化工具参数"""
        # 为某些工具注入work_id和chapter_id
        if tool_name in ["get_context_tool", "read_chapter_tool", "get_chapter_by_order_tool"]:
            tool_args.setdefault("work_id", state.get("work_id", ""))

        if tool_name == "read_chapter_tool":
            tool_args.setdefault("chapter_id", state.get("chapter_id", ""))

        return tool_args
```

### Step 5：更新主类以使用新组件

**文件**：`backend/app/services/agent/langgraph_agent.py`

```python
# 在文件顶部添加导入
from app.services.agent.httpai_handler import HTTPAIHandler
from app.services.agent.httpai_prompts import HTTPAIPromptBuilder
from app.services.agent.tool_manager import ToolManager

class WritingAgentGraph:
    def __init__(self, ai_service, use_chatgpt=False):
        # ... 现有代码

        # 初始化新组件
        self.httpai_handler = HTTPAIHandler(
            ai_service=ai_service,
            global_state_accessor=self._get_state_value
        )

        # 初始化工具管理器
        tools_dict = {
            "continue_writing_tool": continue_writing_tool,
            "polish_text_tool": polish_text_tool,
            "analyze_text_tool": analyze_text_tool,
            "get_context_tool": get_context_tool,
            "read_chapter_tool": read_chapter_tool,
            "get_chapter_by_order_tool": get_chapter_by_order_tool,
            "search_analysis_fragments_tool": search_analysis_fragments_tool,
        }
        self.tool_manager = ToolManager(tools_dict)

        # 将工具管理器传递给handler
        self.httpai_handler.tool_manager = self.tool_manager

    async def _handle_with_httpai(self, state, agent_type, system_prompt):
        """重构后的方法 - 现在只做委托"""
        logger.info(f"[LangGraph] 委托给HTTPAIHandler处理 {agent_type}")
        return await self.httpai_handler.handle(state, agent_type, system_prompt)
```

### Step 6：删除旧代码

**删除 `langgraph_agent.py` 中的旧方法**：
- 删除 `async def _handle_with_httpai(...):` 的316行实现
- 保留方法签名，改为委托调用
- 删除内部的prompt构建逻辑（已移到 `httpai_prompts.py`）
- 删除工具调用逻辑（已移到 `tool_manager.py`）

### Step 7：测试验证

**测试文件**：`backend/tests/unit/test_httpai_handler.py`

```python
import pytest
from app.services.agent.httpai_handler import HTTPAIHandler
from app.services.agent.httpai_prompts import HTTPAIPromptBuilder
from app.services.agent.tool_manager import ToolManager
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

@pytest.mark.asyncio
class TestHTTPAIHandler:
    """测试HTTPAIHandler"""

    @pytest.fixture
    def mock_ai_service(self):
        """Mock AI服务"""
        class MockAIService:
            async def _stream_chat(self, messages, max_tokens, temperature, task_type):
                yield "测试响应", {"total_tokens": 100}
        return MockAIService()

    @pytest.fixture
    def handler(self, mock_ai_service):
        """创建handler实例"""
        def get_state_value(key, default=None):
            return default

        return HTTPAIHandler(mock_ai_service, get_state_value)

    def test_is_tool_result_stage(self, handler):
        """测试阶段判断"""
        # 工具结果阶段
        messages = [HumanMessage("test"), ToolMessage("result", "id")]
        assert handler._is_tool_result_stage(messages) == True

        # 非工具结果阶段
        messages = [HumanMessage("test")]
        assert handler._is_tool_result_stage(messages) == False

    def test_extract_user_message(self, handler):
        """测试提取用户消息"""
        messages = [
            AIMessage("AI响应"),
            HumanMessage("用户消息"),
            AIMessage("AI响应2")
        ]
        assert handler._extract_user_message(messages) == "用户消息"

    def test_build_decision_prompt(self, handler):
        """测试构建决策prompt"""
        prompt = handler._build_decision_prompt("你是助手", "帮我写第三章")
        assert "帮你写第三章" in prompt
        assert "JSON 格式" in prompt

    @pytest.mark.asyncio
    async def test_handle_tool_decision_direct_response(self, handler):
        """测试工具决策 - 直接响应"""
        state = {
            "messages": [HumanMessage("你好")]
        }

        # Mock决策生成
        handler._generate_decision = AsyncMock(return_value='{"need_tools": false, "direct_response": "你好！"}')
        handler._parse_decision = lambda x: {"need_tools": False, "direct_response": "你好！"}

        result = await handler._handle_tool_decision(state, "general", "你是助手")

        assert result["final_response"] == "你好！"
        assert "direct_response" in str(result["agent_steps"])

@pytest.mark.asyncio
class TestHTTPAIPromptBuilder:
    """测试Prompt构建器"""

    def test_detect_user_intent(self):
        """测试用户意图检测"""
        assert HTTPAIPromptBuilder._detect_user_intent("帮我读第三章") == "read"
        assert HTTPAIPromptBuilder._detect_user_intent("帮我写第三章") == "write"
        assert HTTPAIPromptBuilder._detect_user_intent("你好") == "unknown"

    def test_build_writing_prompt(self):
        """测试构建writing prompt"""
        prompt = HTTPAIPromptBuilder._build_writing_prompt(
            system_prompt="你是写作助手",
            user_message="帮我写第三章",
            tool_result='{"current_chapter": {"content": "第一章内容"}}',
            intent="write"
        )

        assert "帮我写第三章" in prompt
        assert "第一章内容" in prompt
        assert "续写内容" in prompt

@pytest.mark.asyncio
class TestToolManager:
    """测试工具管理器"""

    @pytest.fixture
    def mock_tools(self):
        """Mock工具"""
        mock_tool = AsyncMock(return_value="工具执行结果")
        return {"test_tool": mock_tool}

    @pytest.fixture
    def tool_manager(self, mock_tools):
        """创建工具管理器"""
        return ToolManager(mock_tools)

    @pytest.mark.asyncio
    async def test_invoke_tool_success(self, tool_manager, mock_tools):
        """测试工具调用成功"""
        result = await tool_manager.invoke_tool("test_tool", {"param": "value"})

        assert result == "工具执行结果"
        mock_tools["test_tool"].ainvoke.assert_called_once_with({"param": "value"})

    @pytest.mark.asyncio
    async def test_invoke_tool_not_found(self, tool_manager):
        """测试工具不存在"""
        result = await tool_manager.invoke_tool("unknown_tool", {})

        assert "未知工具" in result

    def test_normalize_tool_params(self, tool_manager):
        """测试参数标准化"""
        state = {"work_id": "work123", "chapter_id": "chapter456"}

        # 测试需要work_id的工具
        params = tool_manager.normalize_tool_params(
            "get_context_tool", {}, state
        )
        assert params["work_id"] == "work123"

        # 测试需要chapter_id的工具
        params = tool_manager.normalize_tool_params(
            "read_chapter_tool", {}, state
        )
        assert params["work_id"] == "work123"
        assert params["chapter_id"] == "chapter456"
```

---

## ✅ 测试验证

### 集成测试

**测试文件**：`backend/tests/integration/test_refactored_httpai.py`

```python
import pytest
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.ai.http_ai_service import HTTPAIService

@pytest.mark.asyncio
class TestRefactoredHTTPAI:
    """测试重构后的HTTPAI功能"""

    @pytest.fixture
    def agent(self):
        """创建Agent实例"""
        ai_service = HTTPAIService(enable_model_selector=True)
        return WritingAgentGraph(ai_service, use_chatgpt=False)

    @pytest.mark.asyncio
    async def test_simple_chat(self, agent):
        """测试简单对话"""
        result = await agent.chat(
            message="你好",
            conversation_id="test_simple"
        )

        assert result["response"] is not None
        assert result["metadata"]["intent"] == "general"
        assert len(result["agent_steps"]) > 0

    @pytest.mark.asyncio
    async def test_writing_with_tools(self, agent):
        """测试带工具的写作"""
        result = await agent.chat(
            message="帮我写第三章，需要查询相关信息",
            work_id="test_work",
            conversation_id="test_writing"
        )

        assert result["response"] is not None
        assert result["metadata"]["intent"] == "writing"

        # 验证使用了工具
        tool_steps = [s for s in result["agent_steps"] if "tool" in s["step"].lower()]
        assert len(tool_steps) > 0

        # 验证最终响应
        final_steps = [s for s in result["agent_steps"] if "final_response" in s["step"]]
        assert len(final_steps) > 0

    @pytest.mark.asyncio
    async def test_stuck_scenario(self, agent):
        """测试卡文场景"""
        result = await agent.chat(
            message="我卡住了，不知道怎么写",
            work_id="test_work",
            conversation_id="test_stuck"
        )

        assert result["response"] is not None
        assert result["metadata"]["intent"] == "stuck"
        assert len(result["response"]) > 100  # 应该有具体建议

    @pytest.mark.asyncio
    async def test_planning_scenario(self, agent):
        """测试规划场景"""
        result = await agent.chat(
            message="帮我规划后续章节",
            work_id="test_work",
            conversation_id="test_planning"
        )

        assert result["response"] is not None
        assert result["metadata"]["intent"] == "planning"
```

### 性能测试

**测试脚本**：`backend/tests/performance/test_refactored_performance.py`

```python
"""
性能对比测试：重构前vs重构后
"""
import asyncio
import time
from app.services.agent.langgraph_agent import WritingAgentGraph
from app.services.ai.http_ai_service import HTTPAIService

async def benchmark_agent_requests(agent, requests_count=10):
    """基准测试Agent请求性能"""
    start_time = time.time()
    results = []

    for i in range(requests_count):
        try:
            result = await agent.chat(
                message=f"测试消息{i}",
                conversation_id=f"perf_test_{i}"
            )
            results.append(result)
        except Exception as e:
            print(f"请求{i}失败: {e}")

    elapsed = time.time() - start_time
    success_count = len(results)
    avg_time = elapsed / requests_count

    return {
        "total_time": elapsed,
        "success_count": success_count,
        "avg_time": avg_time,
        "success_rate": success_count / requests_count
    }

async def main():
    ai_service = HTTPAIService(enable_model_selector=True)
    agent = WritingAgentGraph(ai_service, use_chatgpt=False)

    print("=" * 50)
    print("重构后性能基准测试")
    print("=" * 50)

    # 测试不同场景
    scenarios = [
        {"name": "简单对话", "message": "你好"},
        {"name": "写作任务", "message": "帮我写一段话", "work_id": "test"},
        {"name": "分析任务", "message": "分析这段文字"},
    ]

    for scenario in scenarios:
        print(f"\n测试场景: {scenario['name']}")

        for i in range(3):  # 3轮测试
            result = await benchmark_agent_requests(agent, requests_count=5)
            print(f"  第{i+1}轮: {result['avg_time']:.2f}s/次, 成功率: {result['success_rate']:.1%}")

    print("\n" + "=" * 50)
    print("性能要求：")
    print("  简单对话: <2秒/次")
    print("  写作任务: 5-10秒/次")
    print("  成功率: >95%")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📊 验收标准

### 代码质量验收

- [ ] `_handle_with_httpai` 方法行数 < 50行
- [ ] 圈复杂度 < 10
- [ ] 每个子方法都有明确的单一职责
- [ ] 所有方法都有docstring
- [ ] 代码review通过

### 功能验收

- [ ] 所有现有测试仍然通过
- [ ] 新的单元测试通过率 100%
- [ ] 集成测试通过率 100%
- [ ] 性能不低于重构前

### 可维护性验收

- [ ] 每个方法都可以单独测试
- [ ] 修改prompt不需要修改核心逻辑
- [ ] 添加新工具只需要修改配置
- [ ] 新人可以在1小时内理解代码结构

---

## ⚠️ 风险和注意事项

### 风险1：重构引入bug

**风险描述**：大规模重构可能引入新bug

**应对措施**：
- 充分的测试覆盖
- 保留原方法作为备份
- 分步骤验证功能

```python
# 渐进式迁移策略
async def _handle_with_httpai_v2(self, state, agent_type, system_prompt):
    """新版本"""
    return await self.httpai_handler.handle(state, agent_type, system_prompt)

async def _handle_with_httpai(self, state, agent_type, system_prompt):
    """过渡期：可选择新旧版本"""
    use_new_version = os.getenv("USE_NEW_HTTPAI_HANDLER", "true").lower() == "true"

    if use_new_version:
        return await self._handle_with_httpai_v2(state, agent_type, system_prompt)
    else:
        return await self._handle_with_httpai_legacy(state, agent_type, system_prompt)
```

### 风险2：组件间耦合

**风险描述**：新组件之间可能过度耦合

**应对措施**：
- 通过接口定义，降低耦合
- 使用依赖注入
- 单元测试验证解耦

### 风险3：性能下降

**风险描述**：额外的抽象层可能影响性能

**应对措施**：
- 性能基准测试
- 优化关键路径
- 必要时内联热点方法

---

## 📝 问题记录

### 问题1：如何处理工具调用中的异常？

**解决方案**：
```python
class ToolManager:
    async def invoke_tool(self, tool_name: str, tool_args: dict) -> str:
        try:
            result = await tool.ainvoke(tool_args)
            return result
        except Exception as e:
            logger.error(f"[Tool] {tool_name} 执行失败: {e}")
            return f"工具执行失败: {str(e)}"
```

### 问题2：如何确保新版本与旧版本行为一致？

**解决方案**：
- 详细的对比测试
- 保留旧版本作为fallback
- 逐步切换，灰度验证

---

## 📚 相关文档

- [P0-01-修复task_type传递.md](./P0-01-修复task_type传递.md) - 模型选择
- [P0-02-统一工具系统.md](./P0-02-统一工具系统.md) - 工具系统
- [P1-01-实现chat_stream.md](./P1-01-实现chat_stream.md) - 流式执行

---

## 📅 实施计划

### Day 1：创建新组件

**上午**：
- 创建 `HTTPAIHandler` 类
- 实现基础方法（判断、提取、委托）

**下午**：
- 创建 `HTTPAIPromptBuilder` 类
- 实现各种prompt构建方法
- 创建 `ToolManager` 类

### Day 2：集成和重构

**上午**：
- 修改 `WritingAgentGraph` 使用新组件
- 更新 `_handle_with_httpai` 方法
- 删除旧代码

**下午**：
- 编写单元测试
- 运行现有测试确保无regression

### Day 3：测试和优化

**上午**：
- 编写集成测试
- 性能基准测试
- 修复发现的问题

**下午**：
- Code review
- 文档更新
- 准备发布

---

**文档版本**：v1.0
**创建时间**：2025-01-05
**最后更新**：2025-01-05
**负责人**：待分配
**状态**：📝 待开始