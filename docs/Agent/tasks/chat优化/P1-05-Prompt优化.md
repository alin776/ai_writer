# P1-05-Prompt优化：意图识别与Agent提示词

## 📋 文档信息

- **优先级**：P1（核心功能）
- **预估工作量**：2天
- **依赖**：P1-01、P1-04完成（chat_stream框架与上下文管理就绪）
- **验收标准**：
  - 意图识别准确率 >90%
  - Agent输出符合预期格式和质量
  - Prompt模板支持动态参数注入
  - 提供Prompt版本管理机制

---

## 🎯 功能概述

设计和实现React模式下的核心Prompt体系，包括意图分类、各类Agent的系统提示词、工具调用指令等。通过结构化Prompt工程，提升模型的准确性、可控性和输出质量。

### 核心目标

1. **意图识别Prompt**：准确区分writing/planning/tool等意图类型
2. **Agent系统提示词**：为不同Agent设计专业、清晰的角色定位和行为准则
3. **工具调用指导**：优化工具使用的Prompt，提高工具调用成功率
4. **动态上下文注入**：与P1-04上下文管理协同，实现Prompt的动态组装
5. **版本管理与A/B测试**：支持Prompt迭代和效果对比

---

## 🔍 技术分析

### 当前问题

**Planning模式的Prompt问题**：

```python
# 硬编码的系统提示
SYSTEM_PROMPT = """你是一个AI助手，请帮助用户完成任务。"""

# 缺点：
# 1. 过于笼统，没有明确角色定位
# 2. 无意图识别机制，直接进入Planning
# 3. 没有格式约束，输出不可控
# 4. 无法动态调整，缺乏灵活性
```

### React模式的Prompt需求

```
┌─────────────────────────────────────────────┐
│              Prompt体系架构                  │
├─────────────────────────────────────────────┤
│                                             │
│  1. 意图分类器Prompt                        │
│     └─ 识别: writing/planning/tool/query   │
│                                             │
│  2. Agent系统提示词                         │
│     ├─ Writing Agent                        │
│     ├─ Planning Agent                       │
│     ├─ Tool Agent                           │
│     └─ Query Agent                          │
│                                             │
│  3. 工具调用Prompt                          │
│     └─ 工具选择、参数构造指导               │
│                                             │
│  4. 上下文注入模板                          │
│     └─ 摘要、事实、约束的格式化             │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🏗️ 实现方案

### 1. Prompt管理架构

```python
# prompts/prompt_manager.py
from typing import Dict, Any, Optional
from jinja2 import Template
import yaml

class PromptManager:
    """Prompt管理器"""

    def __init__(self, prompts_dir: str = "prompts/templates"):
        self.prompts_dir = prompts_dir
        self.templates: Dict[str, Template] = {}
        self.versions: Dict[str, str] = {}
        self._load_templates()

    def _load_templates(self):
        """加载所有Prompt模板"""
        # 加载意图分类模板
        self.templates["intent_classifier"] = self._load_template(
            "intent_classifier.yaml"
        )

        # 加载各类Agent模板
        self.templates["writing_agent"] = self._load_template(
            "writing_agent.yaml"
        )
        self.templates["planning_agent"] = self._load_template(
            "planning_agent.yaml"
        )
        self.templates["tool_agent"] = self._load_template(
            "tool_agent.yaml"
        )

    def _load_template(self, filename: str) -> Template:
        """加载单个模板文件"""
        filepath = os.path.join(self.prompts_dir, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 保存版本信息
        self.versions[filename] = config.get("version", "1.0.0")

        # 创建Jinja2模板
        template_str = config.get("template", "")
        return Template(template_str)

    def render(
        self,
        template_name: str,
        **kwargs
    ) -> str:
        """渲染模板"""
        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"模板不存在: {template_name}")

        return template.render(**kwargs)

    def get_version(self, template_name: str) -> str:
        """获取模板版本"""
        return self.versions.get(template_name, "unknown")
```

### 2. 意图分类Prompt

```yaml
# prompts/templates/intent_classifier.yaml
version: "1.0.0"
description: "用户意图分类Prompt"
template: |
  你是一个专业的意图分类助手。请分析用户消息并识别其主要意图。

  ## 意图类型定义

  1. **writing** - 写作任务
     - 用户要求写文章、代码、文案、邮件等内容
     - 关键词：写、创作、生成、编写
     - 示例："帮我写一篇关于AI的文章"

  2. **planning** - 规划任务
     - 用户需要制定计划、方案、步骤
     - 关键词：计划、规划、方案、步骤
     - 示例："制定一个学习Python的计划"

  3. **tool** - 工具使用
     - 需要调用外部工具（搜索、计算、翻译等）
     - 关键词：查询、搜索、计算、翻译
     - 示例："查询今天的天气"

  4. **query** - 简单问答
     - 知识性问答，无需工具或复杂处理
     - 关键词：是什么、为什么、如何、解释
     - 示例："什么是机器学习？"

  ## 分类规则

  - 如果消息包含多个意图，选择最主要的一个
  - 优先级：writing > planning > tool > query
  - 不确定时，默认选择query

  ## 用户消息

  ```
  {{ user_message }}
  ```

  {% if context_summary %}
  ## 对话摘要

  {{ context_summary }}
  {% endif %}

  {% if important_facts %}
  ## 重要信息

  {% for fact in important_facts %}
  - {{ fact }}
  {% endfor %}
  {% endif %}

  ## 输出格式

  请严格按照以下JSON格式输出：

  ```json
  {
    "intent": "writing|planning|tool|query",
    "confidence": 0.95,
    "reasoning": "选择该意图的原因",
    "keywords": ["关键词1", "关键词2"]
  }
  ```

  现在请分析并输出结果：
```

### 3. Writing Agent Prompt

```yaml
# prompts/templates/writing_agent.yaml
version: "1.0.0"
description: "写作Agent系统提示词"
template: |
  # 角色定位

  你是一个专业的写作助手，擅长各类文本创作，包括文章、代码、文案、邮件等。

  # 核心能力

  1. **内容创作**：根据用户需求生成高质量文本
  2. **风格适配**：能够适应不同的写作风格和语气
  3. **结构规范**：输出内容结构清晰、逻辑严密
  4. **质量控制**：确保内容准确、完整、符合要求

  # 工作流程

  1. 理解用户需求（主题、风格、长度、格式等）
  2. 确认创作约束（如果有疑问，先提问澄清）
  3. 开始创作内容
  4. 自我检查并优化

  # 输出规范

  - 直接输出创作内容，不要添加"好的，我来帮你写"等多余话术
  - 如果内容较长，提供清晰的章节结构
  - 代码类内容使用markdown代码块包裹
  - 保持专业、准确、有深度

  {% if user_preferences %}
  # 用户偏好

  {% for key, value in user_preferences.items() %}
  - {{ key }}: {{ value }}
  {% endfor %}
  {% endif %}

  {% if context_summary %}
  # 对话上下文

  {{ context_summary }}
  {% endif %}

  {% if writing_constraints %}
  # 创作约束

  {% for constraint in writing_constraints %}
  - {{ constraint }}
  {% endfor %}
  {% endif %}

  # 当前任务

  用户需求：{{ user_message }}

  {% if examples %}
  # 参考示例

  {% for example in examples %}
  ## 示例 {{ loop.index }}

  {{ example }}
  {% endfor %}
  {% endif %}

  现在请开始创作：
```

### 4. Tool Agent Prompt

```yaml
# prompts/templates/tool_agent.yaml
version: "1.0.0"
description: "工具调用Agent提示词"
template: |
  # 角色定位

  你是一个工具调用专家，负责选择合适的工具来满足用户需求。

  # 可用工具

  {% for tool in available_tools %}
  ## {{ tool.name }}

  **功能**：{{ tool.description }}

  **参数**：
  {% for param in tool.parameters %}
  - `{{ param.name }}` ({{ param.type }}): {{ param.description }}
    {% if param.required %}[必需]{% else %}[可选]{% endif %}
  {% endfor %}

  **示例**：
  ```json
  {{ tool.example }}
  ```

  {% endfor %}

  # 工具选择原则

  1. **精准匹配**：选择最符合用户需求的工具
  2. **参数完整**：确保所有必需参数都有值
  3. **单一职责**：一次只调用一个工具
  4. **结果验证**：检查工具返回结果是否符合预期

  # 用户需求

  {{ user_message }}

  {% if context_summary %}
  # 对话上下文

  {{ context_summary }}
  {% endif %}

  # 任务

  请分析用户需求，选择合适的工具并构造调用参数。

  ## 输出格式

  ```json
  {
    "tool": "工具名称",
    "parameters": {
      "param1": "value1",
      "param2": "value2"
    },
    "reasoning": "选择该工具的原因"
  }
  ```

  现在请分析并输出结果：
```

### 5. Planning Agent Prompt

```yaml
# prompts/templates/planning_agent.yaml
version: "1.0.0"
description: "规划Agent系统提示词"
template: |
  # 角色定位

  你是一个专业的规划助手，擅长分析问题、制定计划、拆解任务。

  # 核心能力

  1. **需求分析**：理解用户目标和约束条件
  2. **方案设计**：制定合理、可行的计划
  3. **任务拆解**：将大目标分解为可执行的小步骤
  4. **风险评估**：识别潜在风险并提供应对措施

  # 规划原则

  - **SMART原则**：目标应该是Specific（具体）、Measurable（可衡量）、Achievable（可实现）、Relevant（相关）、Time-bound（有时限）
  - **优先级排序**：区分紧急重要、重要不紧急、紧急不重要、不紧急不重要
  - **迭代思维**：计划应该允许调整和优化

  # 输出格式

  请按以下结构输出计划：

  ## 目标
  - 主目标：...
  - 子目标：...

  ## 分析
  - 现状：...
  - 挑战：...
  - 机会：...

  ## 计划
  ### 阶段1：准备阶段（时间范围）
  - 任务1.1：...
  - 任务1.2：...

  ### 阶段2：执行阶段（时间范围）
  - 任务2.1：...
  - 任务2.2：...

  ## 资源需求
  - 人力：...
  - 工具：...
  - 时间：...

  ## 风险与应对
  - 风险1：... → 应对：...
  - 风险2：... → 应对：...

  ## 成功标准
  - 标准1：...
  - 标准2：...

  {% if context_summary %}
  # 对话上下文

  {{ context_summary }}
  {% endif %}

  {% if constraints %}
  # 约束条件

  {% for constraint in constraints %}
  - {{ constraint }}
  {% endfor %}
  {% endif %}

  # 用户需求

  {{ user_message }}

  现在请开始制定计划：
```

### 6. Prompt集成到chat_stream

```python
# agent/chat_agent.py
class ChatAgent:
    def __init__(self):
        self.prompt_manager = PromptManager()
        # ... 其他初始化

    async def _classify_intent(self, state: AgentState) -> AgentState:
        """意图分类节点"""

        # 构建上下文参数
        context_params = {
            "user_message": state.messages[-1].content,
            "context_summary": state.summary,
            "important_facts": state.important_facts
        }

        # 渲染Prompt
        prompt = self.prompt_manager.render(
            "intent_classifier",
            **context_params
        )

        # 调用LLM
        response = await self.llm.ainvoke(
            [SystemMessage(content=prompt)],
            task_type="simple_query"
        )

        # 解析结果
        intent_data = self._parse_json_response(response.content)

        # 更新状态
        state.intent = intent_data["intent"]
        state.confidence = intent_data["confidence"]
        state.metadata["intent_reasoning"] = intent_data["reasoning"]
        state.metadata["prompt_version"] = self.prompt_manager.get_version(
            "intent_classifier"
        )

        return state

    async def _writing_agent_node(self, state: AgentState) -> AgentState:
        """写作Agent节点"""

        # 提取用户偏好和约束
        user_prefs = state.metadata.get("user_preferences", {})
        constraints = state.metadata.get("writing_constraints", [])

        # 构建Prompt参数
        prompt_params = {
            "user_message": state.messages[-1].content,
            "context_summary": state.summary,
            "user_preferences": user_prefs,
            "writing_constraints": constraints,
            "examples": state.metadata.get("examples", [])
        }

        # 渲染系统提示词
        system_prompt = self.prompt_manager.render(
            "writing_agent",
            **prompt_params
        )

        # 调用LLM
        response = await self.writing_llm.ainvoke(
            [SystemMessage(content=system_prompt)],
            task_type=state.task_type
        )

        # 更新状态
        state.messages.append(response)
        state.metadata["writing_complete"] = True
        state.metadata["prompt_version"] = self.prompt_manager.get_version(
            "writing_agent"
        )

        return state
```

### 7. Prompt版本管理

```python
# prompts/version_manager.py
class PromptVersionManager:
    """Prompt版本管理器"""

    def __init__(self, storage_backend="redis"):
        self.storage = storage_backend
        self.active_versions: Dict[str, str] = {}
        self.ab_tests: Dict[str, Dict] = {}

    async def get_prompt_version(
        self,
        template_name: str,
        session_id: Optional[str] = None
    ) -> str:
        """
        获取要使用的Prompt版本

        Args:
            template_name: 模板名称
            session_id: 会话ID（用于A/B测试）

        Returns:
            版本号（如 "1.0.0" 或 "1.1.0-beta"）
        """

        # 检查是否在A/B测试中
        if template_name in self.ab_tests and session_id:
            return await self._get_ab_test_version(
                template_name,
                session_id
            )

        # 返回活跃版本
        return self.active_versions.get(template_name, "1.0.0")

    async def _get_ab_test_version(
        self,
        template_name: str,
        session_id: str
    ) -> str:
        """获取A/B测试版本"""

        test_config = self.ab_tests[template_name]

        # 检查会话是否已分配版本
        cache_key = f"ab_test:{template_name}:{session_id}"
        cached_version = await self.storage.get(cache_key)

        if cached_version:
            return cached_version

        # 根据流量配置随机分配版本
        import random
        rand = random.random()

        cumulative = 0
        for version, traffic in test_config["traffic"].items():
            cumulative += traffic
            if rand < cumulative:
                # 缓存分配结果
                await self.storage.set(
                    cache_key,
                    version,
                    expire=7 * 24 * 3600  # 7天
                )
                return version

        # 默认返回control组
        return test_config["control"]

    async def create_ab_test(
        self,
        template_name: str,
        control_version: str,
        test_version: str,
        traffic_split: float = 0.5
    ):
        """
        创建A/B测试

        Args:
            template_name: 模板名称
            control_version: 对照版本
            test_version: 测试版本
            traffic_split: 测试组流量比例（0-1）
        """

        self.ab_tests[template_name] = {
            "control": control_version,
            "traffic": {
                control_version: 1.0 - traffic_split,
                test_version: traffic_split
            }
        }

    async def record_prompt_metrics(
        self,
        template_name: str,
        version: str,
        session_id: str,
        metrics: Dict[str, Any]
    ):
        """记录Prompt效果指标"""

        key = f"prompt_metrics:{template_name}:{version}"

        await self.storage.lpush(
            key,
            json.dumps({
                "session_id": session_id,
                "timestamp": time.time(),
                **metrics
            })
        )
```

---

## 📝 实施步骤

### Day 1：Prompt设计与模板化

**上午（4小时）**：
1. 设计意图分类Prompt（2小时）
2. 设计Writing Agent Prompt（2小时）

**下午（4小时）**：
1. 设计Planning/Tool Agent Prompt（2小时）
2. 实现PromptManager（2小时）

### Day 2：集成与优化

**上午（4小时）**：
1. 集成到chat_stream（2小时）
2. 实现版本管理（2小时）

**下午（4小时）**：
1. 测试和调优（2小时）
2. 文档和示例（2小时）

---

## 🧪 测试策略

### 1. 意图分类测试

```python
# tests/test_intent_classification.py
@pytest.mark.asyncio
async def test_intent_classification_accuracy():
    """测试意图分类准确率"""

    test_cases = [
        {
            "message": "帮我写一篇关于AI的文章",
            "expected_intent": "writing",
            "confidence_threshold": 0.8
        },
        {
            "message": "制定一个学习Python的计划",
            "expected_intent": "planning",
            "confidence_threshold": 0.8
        },
        {
            "message": "查询今天的天气",
            "expected_intent": "tool",
            "confidence_threshold": 0.8
        },
        {
            "message": "什么是机器学习？",
            "expected_intent": "query",
            "confidence_threshold": 0.8
        }
    ]

    agent = ChatAgent()
    correct = 0

    for case in test_cases:
        state = AgentState(
            messages=[HumanMessage(content=case["message"])],
            session_id="test"
        )

        result = await agent._classify_intent(state)

        if result.intent == case["expected_intent"]:
            correct += 1

        assert result.confidence >= case["confidence_threshold"]

    # 验证准确率
    accuracy = correct / len(test_cases)
    assert accuracy >= 0.9, f"意图分类准确率 {accuracy} 低于90%"
```

### 2. Agent输出质量测试

```python
# tests/test_agent_output.py
@pytest.mark.asyncio
async def test_writing_agent_output():
    """测试Writing Agent输出质量"""

    agent = ChatAgent()

    test_message = "写一个Python函数计算斐波那契数列"

    events = []
    async for event in agent.chat_stream(test_message, "test_session"):
        events.append(event)

    # 提取最终响应
    response_event = [e for e in events if e.type == "response_complete"][0]
    output = response_event.content["response"]

    # 验证输出包含代码
    assert "```python" in output

    # 验证包含斐波那契相关代码
    assert "fibonacci" in output.lower() or "fib" in output.lower()

    # 验证代码可以执行（可选）
    # ...
```

---

## 📊 预期收益

### 1. 准确性提升

- **意图识别准确率**：>90%
- **Agent输出质量**：更符合用户预期
- **工具调用成功率**：>95%

### 2. 可控性增强

- **输出格式**：结构化、规范化
- **风格一致性**：保持专业、准确
- **版本管理**：支持迭代优化

### 3. 用户体验

- **响应质量**：更专业、更有深度
- **交互流畅性**：意图理解更准确
- **个性化**：支持用户偏好

---

## ⚠️ 风险评估

### 中风险

1. **Prompt质量依赖人工优化**：需要持续迭代
   - **缓解措施**：建立Prompt优化流程和最佳实践
   - **监控方案**：记录用户反馈和效果指标

2. **模型能力限制**：不同模型对Prompt的敏感度不同
   - **缓解措施**：针对不同模型调整Prompt
   - **测试策略**：多模型对比测试

---

## 🔗 相关文档

### 依赖文档
- [P1-01-实现chat_stream.md](./P1-01-实现chat_stream.md) - 集成点
- [P1-04-上下文管理.md](./P1-04-上下文管理.md) - 上下文注入

### 相关文档
- [P2-01-监控日志.md](./P2-01-监控日志.md) - Prompt效果监控
- [P3-01-时间预估.md](./P3-01-时间预估.md) - 基于Prompt的时间估算

---

## 📝 实施记录

### 问题记录
*（实施过程中记录遇到的问题和解决方案）*

### 变更记录
*（记录Prompt的迭代和优化）*

### 测试结果
*（记录意图分类准确率和Agent输出质量）*

---

## ✅ 验收标准

- [ ] PromptManager可以正常加载和渲染模板
- [ ] 意图分类准确率>90%
- [ ] Writing/Planning/Tool Agent输出符合预期
- [ ] 支持动态参数注入
- [ ] Prompt版本管理功能完善
- [ ] 所有单元测试通过
- [ ] 输出质量测试通过
- [ ] Prompt模板文档完整

---

**文档版本**：v1.0
**创建时间**：2025-01-05
**预计完成时间**：P1-01和P1-04完成后2天内
**负责人**：Prompt工程团队