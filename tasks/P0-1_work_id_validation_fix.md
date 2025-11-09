# P0-1: work_id 参数验证失败修复方案

## 📋 问题概述

**严重性**: 🔴 P0 - 阻塞性
**影响范围**: Planning模式约50%的请求
**发现时间**: 2025-11-09
**责任人**: 待分配

---

## 🔍 问题详情

### 症状描述

```
14:52:10 ERROR [ParallelExecution] 并行任务1最终失败: 1 validation error for get_context_tool
work_id
  Input should be a valid string [type=string_type, input_value=None, input_type=NoneType]
```

### 触发场景

1. 用户在非作品详情页发起对话："帮我分析一下"
2. Planning模式启动，AI规划任务
3. AI生成任务："获取作品的整体上下文信息"，调用 `get_context_tool`
4. State中 `work_id=None`
5. Pydantic验证失败 → 任务崩溃

### 代码位置

**工具定义**:
```python
# backend/app/services/agent/langgraph_agent.py:547
@tool
async def get_context_tool(work_id: str, chapter_id: str = "") -> str:
    """获取上下文工具：检索作品、章节和世界观信息（真实数据）

    Args:
        work_id: 作品ID  # ❌ 必需参数，不接受None
```

**State定义**:
```python
# backend/app/services/agent/langgraph_agent.py:42
work_id: Optional[str]  # 作品ID  # ✅ 可以为None
```

---

## 🎯 根本原因分析

### 问题本质

不是简单的参数验证问题，而是**AI规划时缺乏上下文感知能力**：

```
AI规划阶段                    任务执行阶段
     ↓                            ↓
"需要获取作品上下文"    →    work_id=None    →    💥失败
     ↑
  AI不知道work_id不可用！
```

### 设计缺陷

1. **工具定义与State不一致**
   - 工具要求必需参数 `work_id: str`
   - State允许可选 `work_id: Optional[str]`

2. **AI规划缺少前置条件检查**
   - Planning prompt没有告知AI当前可用的资源
   - AI盲目规划，不知道哪些工具当前不可用

3. **没有降级策略**
   - 工具执行失败时没有优雅处理
   - 直接抛异常，导致任务崩溃

---

## 💡 解决方案（三层防御）

### 🎯 第一层：让AI知道"能力边界"（推荐）

**核心思想**：在规划阶段就告诉AI当前的上下文状态

#### 实施步骤

**1. 添加上下文状态构建方法**

```python
# backend/app/services/agent/langgraph_agent.py

def _build_context_status(self, state: dict) -> str:
    """构建上下文状态描述，供AI规划时参考"""
    status_lines = []

    # 作品上下文
    if state.get('work_id'):
        status_lines.append(f"✅ 作品ID: {state['work_id']} (作品相关工具可用)")
    else:
        status_lines.append("❌ 作品ID: 未提供 (作品相关工具不可用)")

    # 章节上下文
    if state.get('chapter_id'):
        status_lines.append(f"✅ 章节ID: {state['chapter_id']}")
    else:
        status_lines.append("❌ 章节ID: 未提供")

    # 工具可用性提示
    available_tools = []
    unavailable_tools = []

    if not state.get('work_id'):
        unavailable_tools.extend([
            'get_context_tool (需要work_id)',
            'read_chapter_tool (需要work_id)',
            'get_chapter_by_order_tool (需要work_id)',
            'search_analysis_fragments_tool (需要work_id)'
        ])
    else:
        available_tools.extend([
            'get_context_tool',
            'read_chapter_tool',
            'get_chapter_by_order_tool',
            'search_analysis_fragments_tool'
        ])

    # 通用工具（总是可用）
    available_tools.extend([
        'analyze_text_tool',
        'continue_writing_tool',
        'polish_text_tool'
    ])

    status_lines.append(f"\n✅ 可用工具: {', '.join(available_tools)}")
    if unavailable_tools:
        status_lines.append(f"⚠️  不可用工具: {', '.join(unavailable_tools)}")

    return '\n'.join(status_lines)
```

**2. 修改Planning Prompt**

```python
# backend/app/services/agent/langgraph_agent.py:2689

async def _plan_with_agent(...):
    # 构建上下文状态描述
    context_status = self._build_context_status(state)

    plan_prompt = f"""你是专业的AI写作助手。

【当前上下文状态】
{context_status}

【用户请求】
{message}

请根据当前上下文状态，生成可执行的任务清单。

【重要规则】
1. 不要规划需要不可用工具的任务
2. 如果缺少必要信息（如work_id），可以：
   - 生成"询问用户"类型的任务
   - 使用通用工具完成部分功能
   - 礼貌地说明需要用户提供哪些信息

【任务格式】
{{
  "user_intent": "用户意图",
  "tasks": [
    {{
      "task_id": 1,
      "description": "任务描述",
      "tool": "工具名称",
      "params": {{...}}
    }}
  ]
}}
"""
    # 继续原有逻辑...
```

**预期效果**：
```
修复前：
AI: "好的，我来规划3个任务..."
    任务1: get_context_tool(work_id=None) → ❌ 失败
    任务2: search_analysis_fragments_tool(work_id=None) → ❌ 失败
    任务3: analyze_text_tool(...) → ✅ 成功
输出: "部分任务失败，结果不完整"

修复后：
AI: "检测到work_id未提供，我来规划1个引导任务..."
    任务1: general_chat("引导用户提供作品ID") → ✅ 成功
输出: "我很乐意帮您分析！请问您想分析哪个作品呢？
      您可以在作品详情页使用，或告诉我作品ID。"
```

---

### 🛡️ 第二层：工具定义容错（快速止血）

**核心思想**：即使AI规划错了，工具也能优雅处理

#### 实施步骤

**修改 get_context_tool**

```python
# backend/app/services/agent/langgraph_agent.py:547

@tool
async def get_context_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """获取上下文工具：检索作品、章节和世界观信息（真实数据）

    Args:
        work_id: 作品ID（可选，但强烈推荐提供）
        chapter_id: 章节ID（可选）

    Returns:
        上下文信息（JSON格式字符串）
    """
    if not work_id:
        # ✅ 返回结构化的"需要用户输入"信号
        return json.dumps({
            "status": "missing_prerequisite",  # 状态标记
            "missing": "work_id",
            "message": "需要指定作品ID才能获取上下文",
            "user_action_required": True,  # 需要用户操作
            "suggested_response": "请问您想查看哪个作品的信息？您可以在作品详情页使用此功能，或者告诉我作品ID。"
        }, ensure_ascii=False, indent=2)

    # 原有逻辑...
    try:
        from app.core.database import AsyncSessionLocal
        from app.services.work_service import WorkService
        # ... 正常流程
    except Exception as e:
        logger.error(f"[get_context_tool] 获取上下文失败: {e}")
        return json.dumps({
            "status": "error",
            "error": str(e),
            "work_id": work_id
        }, ensure_ascii=False, indent=2)
```

**优点**：
- ✅ 不会抛异常，任务不会崩溃
- ✅ 返回结构化错误，方便后续处理
- ✅ 提供友好的用户引导

---

### 🔍 第三层：智能响应汇总（体验优化）

**核心思想**：将技术错误转化为友好的用户引导

#### 实施步骤

```python
# backend/app/services/agent/langgraph_agent.py (Response生成部分)

def _generate_final_response(self, task_results: List[dict]) -> str:
    """生成最终响应，智能处理缺失前置条件的情况"""

    # 检查是否有任务因缺少前置条件失败
    missing_prerequisites = []
    for result in task_results:
        if isinstance(result.get('output'), str):
            try:
                output_json = json.loads(result['output'])
                if output_json.get('status') == 'missing_prerequisite':
                    missing_prerequisites.append(output_json)
            except:
                pass

    # 如果有缺失的前置条件，优先处理
    if missing_prerequisites:
        # 去重
        missing_params = set(m['missing'] for m in missing_prerequisites)

        if 'work_id' in missing_params:
            return """我注意到您的请求需要访问特定作品的信息，但我目前不知道是哪个作品。

您可以：
1. 在作品详情页使用此功能（推荐）
2. 或者告诉我："分析作品 [作品ID]"

这样我就能为您提供完整的分析了！😊"""

    # 否则正常汇总结果
    return self._summarize_results(task_results)
```

---

## 📅 实施计划

### 阶段1：快速止血（今天，1小时）

- [ ] 修改 `get_context_tool` 参数为 `Optional[str]`
- [ ] 添加 work_id 为空时的友好错误返回
- [ ] 本地测试：验证不再抛异常
- [ ] 提交代码

**验收标准**：
- Planning模式不再因work_id=None崩溃
- 返回友好提示而非500错误

### 阶段2：根本优化（本周，2小时）

- [ ] 实现 `_build_context_status()` 方法
- [ ] 修改 Planning prompt，注入上下文状态
- [ ] 测试AI规划质量：验证AI能识别工具可用性
- [ ] 代码review + 提交

**验收标准**：
- AI规划时不再生成不可执行的任务
- Planning任务成功率 > 95%

### 阶段3：体验优化（下周，1小时）

- [ ] 实现 `_generate_final_response()` 智能汇总
- [ ] 添加测试用例：覆盖各种缺失参数场景
- [ ] 监控Planning任务失败率
- [ ] 文档更新

**验收标准**：
- 用户看到友好引导而非技术错误
- 测试覆盖率 > 80%

---

## 🧪 测试用例

### 测试1：work_id为None的处理

```python
async def test_work_id_none_handling():
    """测试work_id为None时的优雅处理"""

    # 准备
    state = {
        'work_id': None,
        'chapter_id': None,
        'message': "帮我分析一下"
    }

    # 执行
    response = await agent.chat_with_planning(
        message="帮我分析一下",
        work_id=None
    )

    # 验证
    assert response['status'] == 'success'  # 不应该失败
    assert '作品ID' in response['content']  # 应该提示需要作品ID
    assert response['requires_user_action'] == True  # 标记需要用户操作
```

### 测试2：AI规划质量验证

```python
async def test_ai_planning_with_missing_work_id():
    """测试AI是否能根据上下文状态正确规划"""

    # 准备
    state = {'work_id': None}

    # 执行规划
    plan = await agent._plan_with_agent(
        message="分析第一章",
        state=state
    )

    # 验证
    for task in plan['tasks']:
        # 不应该规划需要work_id的工具
        assert task['tool'] not in [
            'get_context_tool',
            'read_chapter_tool',
            'search_analysis_fragments_tool'
        ]
```

---

## 📊 监控指标

### 关键指标

1. **planning_task_failure_rate**
   - 修复前: ~50%
   - 目标: < 5%

2. **work_id_missing_error_count**
   - 修复前: 3次/会话
   - 目标: 0次/会话

3. **user_guidance_shown_rate**
   - 新指标
   - 目标: > 90%（当work_id缺失时）

### 监控代码

```python
# backend/app/services/agent/monitoring.py

from app.services.agent.utils.monitoring import increment_counter

# 在_plan_with_agent中
if not state.get('work_id'):
    increment_counter("work_id_missing_in_planning")

# 在get_context_tool中
if not work_id:
    increment_counter("get_context_tool_missing_work_id")
    increment_counter("user_guidance_shown")
```

---

## 🔗 相关问题

- **P0-2**: search_analysis_fragments_tool 同样问题（一起修复）
- **前端**: 考虑在前端提前检测并提示用户

---

## 📚 参考资料

- Pydantic验证文档: https://docs.pydantic.dev/latest/
- LangGraph工具定义: https://langchain-ai.github.io/langgraph/
- 类似问题案例: 见 `DEFECT_ANALYSIS_REPORT.md`

---

**创建时间**: 2025-11-09
**最后更新**: 2025-11-09
**状态**: 📝 待实施
