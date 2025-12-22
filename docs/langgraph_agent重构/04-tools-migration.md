# 工具迁移 - 详细方案

## 文档版本
- 版本：1.2
- 日期：2025-12-22
- 更新：更新工具数量统计(20个)，补充 StandardToolRegistry 迁移方案，添加双轨系统说明

---

## 一、现有工具清单

> **统计更新 (2025-12-22)**：实际工具约 20 个（去重后），包括 @tool 装饰器 6 个 + StandardTool 实例 13 个 + 工具类 3 个

### 1.1 写作工具

| 工具名 | 文件位置 | 类型 | 功能 | 迁移优先级 |
|--------|----------|------|------|-----------|
| `continue_writing_tool` | `langgraph_tools.py` | @tool | 接龙写作 | P0 |
| `continue_writing_tool` | `writing_tools.py` | StandardTool | 接龙写作(ST版) | P0 |
| `expand_text_tool` | `writing_tools.py` | StandardTool | 扩写文本 | P1 |
| `smart_continue` | `editor_tools.py` | StandardTool | 智能接龙 | P0 |
| `smart_rewrite` | `editor_tools.py` | StandardTool | 智能改写 | P0 |
| `smart_insert` | `editor_tools.py` | StandardTool | 智能插入 | P0 |
| `apply_chapter_edit` | `editor_tools.py` | StandardTool | 应用编辑 | P1 |

### 1.2 分析工具

| 工具名 | 文件位置 | 类型 | 功能 | 迁移优先级 |
|--------|----------|------|------|-----------|
| `analyze_text_tool` | `langgraph_tools.py` | @tool | 文本分析 | P0 |
| `analyze_text_tool` | `analysis_tools.py` | StandardTool | 文本分析(ST版) | P0 |
| `analyze_content_tool` | `analysis_tools.py` | StandardTool | 内容分析 | P1 |
| `evaluate_quality_tool` | `analysis_tools.py` | StandardTool | 质量评估 | P1 |
| `search_analysis_fragments_tool` | `langgraph_tools.py` | @tool | 搜索分析片段 | P2 |
| `StoryBibleConsistencyChecker` | `consistency_checker.py` | Class | 一致性检查 | P1 |
| `StyleAdapter` | `style_adapter.py` | Class | 风格适配 | P1 |
| `ShowDontTellTool` | `show_dont_tell.py` | Class | Show Don't Tell 检查 | P2 |

### 1.3 数据工具

| 工具名 | 文件位置 | 类型 | 功能 | 迁移优先级 |
|--------|----------|------|------|-----------|
| `read_chapter_tool` | `langgraph_tools.py` | @tool | 读取章节 | P0 |
| `read_chapter_tool_st` | `langgraph_tools.py` | StandardTool | 读取章节(ST版) | P0 |
| `get_chapter_by_order_tool` | `langgraph_tools.py` | @tool | 按序号获取章节 | P0 |
| `get_chapter_by_order_tool_st` | `langgraph_tools.py` | StandardTool | 按序号获取(ST版) | P0 |
| `get_context_tool` | `langgraph_tools.py` | @tool | 获取上下文 | P0 |
| `get_context_tool_st` | `langgraph_tools.py` | StandardTool | 获取上下文(ST版) | P0 |
| `search_analysis_fragments_tool_st` | `langgraph_tools.py` | StandardTool | 搜索片段(ST版) | P2 |

### 1.4 现有双轨系统说明

当前项目使用 **双轨工具系统**：
- **@tool 装饰器**：LangChain 原生工具定义
- **StandardTool**：项目自定义的标准化工具类，通过 `StandardToolRegistry` 管理

双轨系统的调用逻辑：
```python
# langgraph_agent.py 中的调用逻辑
async def _call_tool_via_registry(self, tool_name, tool_args, state):
    normalized_name = TOOL_NAME_MAPPING.get(tool_name, tool_name)
    try:
        # 优先使用 StandardTool
        return await registry.call_tool(normalized_name, params)
    except:
        # 降级到 @tool 版本
        return await invoke_tool_function(tool_name, tool_args)
```

---

## 二、工具适配模式

### 2.1 现有工具格式

```python
# 现有格式 (langgraph_tools.py)
from langchain_core.tools import tool

@tool
def read_chapter_tool(chapter_id: str) -> str:
    """读取章节内容

    Args:
        chapter_id: 章节ID
    """
    # 通过全局变量获取服务
    ai_service = get_global_ai_service()
    # ...
    return content
```

### 2.2 Deep Agents 工具格式

Deep Agents 支持多种工具定义方式，推荐使用普通函数：

```python
# 方式一：普通函数（推荐）
def read_chapter_tool(chapter_id: str) -> str:
    """读取章节内容

    Args:
        chapter_id: 章节的唯一标识符
    """
    # 通过依赖注入获取服务
    from app.services.chapter import get_chapter_service
    chapter_service = get_chapter_service()

    content = chapter_service.fetch_chapter(chapter_id)
    return content

# 方式二：使用 @tool 装饰器
from langchain.tools import tool

@tool
def read_chapter_tool(chapter_id: str) -> str:
    """读取章节内容

    Args:
        chapter_id: 章节的唯一标识符
    """
    from app.services.chapter import get_chapter_service
    chapter_service = get_chapter_service()
    return chapter_service.fetch_chapter(chapter_id)
```

### 2.3 关键差异

| 方面 | 现有方式 | Deep Agents 方式 |
|------|----------|------------------|
| 服务获取 | 全局变量 | 依赖注入/模块导入 |
| 状态访问 | 传参 | 通过 Agent State |
| 进度输出 | 无 | 通过流式事件 |
| 存储访问 | 直接调用 | LangGraph Store API |

> **注意**: Deep Agents 不使用 `ToolRuntime` 参数。工具应该是纯函数，通过依赖注入获取服务。

---

## 三、逐个工具迁移方案

### 3.1 read_chapter_tool

**现有实现：**
```python
@tool
def read_chapter_tool(chapter_id: str) -> str:
    """读取指定章节的内容"""
    if not validate_uuid(chapter_id):
        return f"无效的章节ID: {chapter_id}"

    async def _read():
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = result.scalar_one_or_none()
            if not chapter:
                return f"未找到章节: {chapter_id}"
            return f"【{chapter.title}】\n\n{chapter.content}"

    return asyncio.get_event_loop().run_until_complete(_read())
```

**迁移后：**
```python
def read_chapter_tool(chapter_id: str) -> str:
    """读取指定章节的内容

    Args:
        chapter_id: 章节的唯一标识符
    """
    if not validate_uuid(chapter_id):
        return f"无效的章节ID: {chapter_id}"

    # 使用依赖注入获取服务
    from app.services.chapter import get_chapter_service

    chapter_service = get_chapter_service()
    chapter = chapter_service.get_chapter_sync(chapter_id)

    if not chapter:
        return f"未找到章节: {chapter_id}"

    return f"【{chapter.title}】\n\n{chapter.content}"
```

### 3.2 continue_writing_tool

**现有实现：**
```python
@tool
def continue_writing_tool(
    prompt: str,
    context: str = "",
    style: str = "默认",
    length: int = 500
) -> str:
    """续写内容"""
    ai_service = get_global_ai_service()

    full_prompt = f"""
    上下文：{context}
    风格：{style}
    要求：{prompt}
    字数：约{length}字
    """

    async def _generate():
        result = await ai_service.call_ai(
            system_prompt="你是专业的小说写作助手",
            user_prompt=full_prompt,
            max_tokens=length * 2
        )
        return result

    return asyncio.get_event_loop().run_until_complete(_generate())
```

**迁移后：**
```python
def continue_writing_tool(
    prompt: str,
    context: str = "",
    style: str = "默认",
    length: int = 500
) -> str:
    """续写小说内容

    Args:
        prompt: 续写指令，描述要写什么内容
        context: 前文上下文，帮助保持连贯性
        style: 写作风格（如：幽默、严肃、悬疑）
        length: 目标字数
    """
    # 使用依赖注入获取 AI 服务
    from app.services.ai import get_ai_service

    ai_service = get_ai_service()

    full_prompt = f"""
    上下文：{context}
    风格：{style}
    要求：{prompt}
    字数：约{length}字
    """

    # 同步调用（Deep Agents 会处理异步）
    result = ai_service.call_ai_sync(
        system_prompt="你是专业的小说写作助手",
        user_prompt=full_prompt,
        max_tokens=length * 2
    )

    return result
```

### 3.3 smart_rewrite (带 HITL)

**现有实现：**
```python
@tool
def smart_rewrite(
    text: str,
    instruction: str,
    chapter_id: str = None
) -> str:
    """智能改写，返回多个版本供用户选择"""
    ai_service = get_global_ai_service()

    # 生成多个版本
    versions = []
    for i in range(3):
        result = await ai_service.call_ai(...)
        versions.append(result)

    # 返回需要确认的格式
    return json.dumps({
        "requires_confirmation": True,
        "action_type": "rewrite",
        "original_text": text,
        "versions": versions,
        "chapter_id": chapter_id
    })
```

**迁移后（使用 interrupt_on 配置）：**
```python
def smart_rewrite(
    text: str,
    instruction: str,
    chapter_id: str = None
) -> dict:
    """智能改写文本，生成多个版本

    Args:
        text: 要改写的原文
        instruction: 改写指令（如：更生动、更简洁）
        chapter_id: 章节ID（可选，用于保存）
    """
    from app.services.ai import get_ai_service

    ai_service = get_ai_service()

    # 生成多个版本
    versions = []
    for i in range(3):
        result = ai_service.call_ai_sync(
            system_prompt="你是文字改写专家",
            user_prompt=f"改写指令：{instruction}\n原文：{text}",
            temperature=0.7 + i * 0.1  # 不同温度产生不同版本
        )
        versions.append({
            "id": i + 1,
            "content": result,
            "style": ["保守", "中等", "激进"][i]
        })

    # 返回结构化数据，由 interrupt_on 配置决定是否暂停
    return {
        "original_text": text,
        "versions": versions,
        "chapter_id": chapter_id
    }

# 在创建 Agent 时配置 interrupt_on
agent = create_deep_agent(
    tools=[smart_rewrite],
    interrupt_on={
        "smart_rewrite": {
            "allowed_decisions": ["select_1", "select_2", "select_3", "cancel"]
        }
    }
)
```

### 3.4 analyze_text_tool

**迁移后：**
```python
def analyze_text_tool(
    text: str,
    focus: str = "综合分析"
) -> str:
    """分析文本内容

    Args:
        text: 要分析的文本内容
        focus: 分析焦点（如：人物关系、情节结构、文笔风格）
    """
    from app.services.ai import get_ai_service

    ai_service = get_ai_service()

    result = ai_service.call_ai_sync(
        system_prompt="你是专业的文学分析师",
        user_prompt=f"""
        请对以下文本进行{focus}：

        {text[:3000]}

        分析要求：
        1. 结构清晰
        2. 观点明确
        3. 有具体例证
        """
    )

    return result
```

---

## 四、工具注册

### 4.1 工具收集

```python
# tools/__init__.py

from .writing_tools import (
    continue_writing_tool,
    smart_continue,
)
from .editor_tools import (
    smart_rewrite,
    smart_insert,
    apply_chapter_edit,
)
from .analysis_tools import (
    analyze_text_tool,
    consistency_checker,
    style_adapter,
)
from .data_tools import (
    read_chapter_tool,
    get_chapter_by_order_tool,
    get_context_tool,
)

# 所有工具列表
ALL_TOOLS = [
    # 写作工具
    continue_writing_tool,
    smart_continue,
    smart_rewrite,
    smart_insert,
    apply_chapter_edit,

    # 分析工具
    analyze_text_tool,
    consistency_checker,
    style_adapter,

    # 数据工具
    read_chapter_tool,
    get_chapter_by_order_tool,
    get_context_tool,
]
```

### 4.2 注册到 Deep Agents

```python
# writing_agent.py

from deepagents import create_deep_agent
from .tools import ALL_TOOLS
from .middleware import (
    MemoryMiddleware,
    ModelMiddleware,
    CostMiddleware,
)

def create_writing_agent(checkpointer, **kwargs):
    """创建写作 Agent"""

    return create_deep_agent(
        # 注册所有工具（普通函数列表）
        tools=ALL_TOOLS,

        # 系统提示
        system_prompt="""你是一个专业的小说写作助手。
        你可以帮助用户：
        1. 续写小说内容
        2. 改写和优化文本
        3. 分析文本质量
        4. 检查一致性问题
        """,

        # 中间件
        middleware=[
            MemoryMiddleware(),
            ModelMiddleware(),
            CostMiddleware(),
        ],

        # 配置需要人工确认的工具
        interrupt_on={
            "smart_rewrite": True,
            "apply_chapter_edit": True,
        },

        # 检查点
        checkpointer=checkpointer,

        # 其他配置
        **kwargs
    )
```

---

## 五、工具上下文注入

### 5.1 依赖注入模式

Deep Agents 工具应该使用依赖注入模式获取服务：

```python
# 方式一：模块级别的服务工厂
def get_ai_service():
    """获取 AI 服务实例"""
    from app.core.config import settings
    from app.services.ai import HTTPAIService
    return HTTPAIService(settings)

def get_chapter_service():
    """获取章节服务实例"""
    from app.services.chapter import ChapterService
    return ChapterService()

# 方式二：在工具内部延迟导入
def my_tool(param: str) -> str:
    """工具示例"""
    from app.services.ai import get_ai_service
    ai_service = get_ai_service()
    return ai_service.process(param)
```

### 5.2 配置注入（通过 Agent 配置）

```python
# 在调用 Agent 时传入配置
async def chat(request: ChatRequest, db: AsyncSession):
    agent = get_writing_agent()

    # 执行时传入配置
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": request.message}]},
        config={
            "configurable": {
                "thread_id": request.thread_id,
                "user_id": request.user_id,
                "work_id": request.work_id,
            }
        }
    )

    return result
```

---

## 六、测试策略

### 6.1 单元测试

```python
# tests/test_tools.py

import pytest
from unittest.mock import Mock, patch

def test_read_chapter_tool():
    """测试读取章节工具"""
    # 模拟服务
    with patch('app.services.chapter.get_chapter_service') as mock_service:
        mock_chapter = Mock()
        mock_chapter.title = "第一章"
        mock_chapter.content = "内容..."
        mock_service.return_value.get_chapter_sync.return_value = mock_chapter

        # 调用工具
        from app.services.agent.tools import read_chapter_tool
        result = read_chapter_tool("valid-uuid")

        # 验证
        assert "第一章" in result
        assert "内容" in result


def test_continue_writing_tool():
    """测试续写工具"""
    with patch('app.services.ai.get_ai_service') as mock_ai:
        mock_ai.return_value.call_ai_sync.return_value = "生成的内容"

        from app.services.agent.tools import continue_writing_tool
        result = continue_writing_tool(
            prompt="继续写",
            context="前文",
            length=500
        )

        assert result == "生成的内容"
```

### 6.2 集成测试

```python
@pytest.mark.asyncio
async def test_tool_in_agent():
    """测试工具在 Agent 中的执行"""
    agent = create_writing_agent(checkpointer=None)

    result = await agent.ainvoke({
        "messages": [{
            "role": "user",
            "content": "读取章节 xxx-xxx-xxx 的内容"
        }]
    })

    # 验证工具被正确调用
    assert result.get("messages")
```

---

## 七、迁移检查清单

### 7.1 每个工具迁移检查

- [ ] 移除 `runtime: ToolRuntime` 参数
- [ ] 使用依赖注入替代全局变量
- [ ] 使用同步调用或确保异步兼容
- [ ] 更新 docstring（Google 风格）
- [ ] 编写单元测试
- [ ] 编写集成测试

### 7.2 整体检查

- [ ] 所有工具编译通过
- [ ] 所有单元测试通过
- [ ] 所有集成测试通过
- [ ] 工具可在 Deep Agents 中正常调用
- [ ] interrupt_on 配置正确
- [ ] 流式响应正常

---

## 八、StandardToolRegistry 迁移方案

### 8.1 现有 StandardToolRegistry 分析

当前项目有一套自定义的工具注册系统：

```python
# tools/tool_registry.py
class StandardToolRegistry:
    """元数据驱动的工具注册表"""

    _tools: Dict[str, StandardTool] = {}

    @classmethod
    def register(cls, tool: StandardTool):
        """注册工具"""
        cls._tools[tool.tool_id] = tool

    @classmethod
    async def call_tool(cls, tool_id: str, params: dict) -> ToolOutput:
        """调用工具"""
        tool = cls._tools.get(tool_id)
        if not tool:
            raise ToolNotFoundError(f"Tool {tool_id} not found")
        return await tool.execute(**params)

    @classmethod
    def list_tools_by_category(cls, category: ToolCategory) -> List[ToolInfo]:
        """按类别列举工具"""
        return [t for t in cls._tools.values() if t.category == category]
```

### 8.2 迁移策略

**方案 A：完全迁移到 Deep Agents（推荐）**

将 StandardTool 转换为普通函数，直接注册到 Deep Agents：

```python
# 迁移前：StandardTool
continue_writing_tool = StandardTool(
    tool_id="continue_writing",
    name="续写工具",
    category=ToolCategory.WRITING,
    execute=_continue_writing_impl,
    input_schema=ContinueWritingInput,
    output_schema=ContinueWritingOutput
)

# 迁移后：普通函数
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
    from app.services.ai import get_ai_service
    ai_service = get_ai_service()
    return ai_service.call_ai_sync(...)
```

**方案 B：保留 Registry 作为适配层**

如果需要保留工具分类等元数据功能：

```python
# 保留 Registry，但让它生成 Deep Agents 兼容的工具
class ToolRegistryAdapter:
    """将 StandardTool 转换为 Deep Agents 工具"""

    @classmethod
    def to_deep_agent_tools(cls) -> List[Callable]:
        """转换所有注册的工具"""
        tools = []
        for tool_id, st_tool in StandardToolRegistry._tools.items():
            # 创建包装函数
            def wrapper(**kwargs):
                return st_tool.execute(**kwargs)

            wrapper.__name__ = tool_id
            wrapper.__doc__ = st_tool.description
            tools.append(wrapper)
        return tools

# 使用
agent = create_deep_agent(
    tools=ToolRegistryAdapter.to_deep_agent_tools()
)
```

### 8.3 工具类迁移

对于工具类（如 `StoryBibleConsistencyChecker`），转换为函数：

```python
# 迁移前：工具类
class StoryBibleConsistencyChecker:
    def __init__(self, ai_service):
        self.ai_service = ai_service

    async def check(self, text: str, worldview: dict) -> dict:
        ...

# 迁移后：工具函数
def consistency_check_tool(
    text: str,
    worldview_json: str
) -> str:
    """检查文本与世界观的一致性

    Args:
        text: 要检查的文本
        worldview_json: 世界观设定（JSON格式）
    """
    import json
    from app.services.ai import get_ai_service

    ai_service = get_ai_service()
    worldview = json.loads(worldview_json)

    # 复用原有逻辑
    checker = StoryBibleConsistencyChecker(ai_service)
    result = checker.check_sync(text, worldview)

    return json.dumps(result, ensure_ascii=False)
```

### 8.4 迁移检查清单

- [ ] 列出所有 StandardTool 实例
- [ ] 为每个 StandardTool 创建对应的函数
- [ ] 将工具类转换为工具函数
- [ ] 更新 ALL_TOOLS 列表
- [ ] 测试所有转换后的工具
- [ ] 验证工具在 Deep Agents 中可正常调用

---

## 九、下一步

阅读 `05-memory-integration.md` 了解如何将三层记忆系统集成到 Deep Agents。
