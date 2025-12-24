# 中断恢复机制

## 文档版本
- 版本：1.1
- 日期：2025-12-19
- 更新：修正 interrupt 使用方式，采用 interrupt_on 配置

---

## 一、核心概念

### 1.1 什么是 interrupt/resume

```
interrupt: 暂停 Agent 执行，等待外部输入
resume:   恢复 Agent 执行，传入用户响应

流程图：
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  执行   │ → │ interrupt│ → │  等待   │ → │ resume  │ → 继续执行
│ Task 1  │    │ (暂停)   │    │ 用户输入 │    │ (恢复)  │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

### 1.2 与现有 HITL 对比

| 特性 | 现有 HITL | interrupt/resume |
|------|-----------|------------------|
| **等待方式** | 轮询 Redis (5秒间隔) | 原生阻塞 |
| **延迟** | 2-5 秒 | < 100ms |
| **实现复杂度** | 高 (需要管理状态) | 低 (框架内置) |
| **触发灵活性** | 特定工具 | 任意位置 |
| **用户体验** | 较差 | 流畅 |

### 1.3 使用场景

| 场景 | 说明 |
|------|------|
| **任务确认** | 执行关键任务前询问用户 |
| **版本选择** | 生成多个版本让用户选择 |
| **参数补充** | 缺少必要信息时询问 |
| **进度控制** | 允许用户随时暂停/终止 |
| **质量把关** | 输出后让用户审核 |

---

## 二、基础用法

### 2.1 通过 interrupt_on 配置（推荐）

Deep Agents 主要通过 `interrupt_on` 参数配置哪些工具需要人工确认：

```python
from deepagents import create_deep_agent
from langgraph.types import Command

# 配置需要人工确认的工具
agent = create_deep_agent(
    tools=[dangerous_operation, smart_rewrite],
    interrupt_on={
        "dangerous_operation": True,  # 简单配置
        "smart_rewrite": {
            "allowed_decisions": ["approve", "edit", "reject"]
        }
    }
)

# 执行时会在指定工具前暂停
result = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "执行危险操作"}]},
    config={"configurable": {"thread_id": "test-123"}}
)

# 检查是否被中断
if result.get("__interrupt__"):
    print("需要用户确认:", result["__interrupt__"])

    # 用户确认后恢复
    result = await agent.ainvoke(
        None,
        config={"configurable": {"thread_id": "test-123"}},
        command=Command(resume="approve")
    )
```

### 2.2 工具返回结构化数据

工具本身返回结构化数据，由 `interrupt_on` 决定是否暂停：

```python
def smart_rewrite(text: str, instruction: str) -> dict:
    """智能改写 - 生成多版本供选择"""
    from app.services.ai import get_ai_service
    ai_service = get_ai_service()

    # 生成多个版本
    versions = []
    for i in range(3):
        result = ai_service.call_ai_sync(
            system_prompt="你是文字改写专家",
            user_prompt=f"改写指令：{instruction}\n原文：{text}",
            temperature=0.7 + i * 0.1
        )
        versions.append({
            "id": i + 1,
            "content": result,
            "style": ["保守", "中等", "激进"][i]
        })

    # 返回结构化数据
    return {
        "original": text,
        "versions": versions
    }

# 配置中断
agent = create_deep_agent(
    tools=[smart_rewrite],
    interrupt_on={
        "smart_rewrite": {
            "allowed_decisions": ["select_1", "select_2", "select_3", "cancel"]
        }
    }
)
```

### 2.3 底层 interrupt 机制（高级用法）

在自定义节点中可以直接使用 LangGraph 的 `interrupt()`：

```python
from langgraph.types import interrupt

def custom_confirmation_node(state):
    """自定义确认节点"""
    response = interrupt({
        "type": "confirmation",
        "message": "是否继续？",
        "options": ["确认", "取消"]
    })

    if response == "取消":
        return {"cancelled": True}

    return {"confirmed": True}
```

> **注意**: 在 Deep Agents 中，推荐使用 `interrupt_on` 配置而非直接调用 `interrupt()`。

---

## 三、前端集成

### 3.1 SSE 事件格式

```typescript
// 后端发送的中断事件
interface InterruptEvent {
  type: "interrupt";
  data: {
    interrupt_id: string;      // 中断唯一标识
    interrupt_type: string;    // confirmation | select_version | text_input
    message: string;           // 提示信息
    options?: Option[];        // 选项列表
    versions?: Version[];      // 版本列表（改写场景）
    metadata?: any;            // 额外元数据
  }
}

// 前端发送的恢复请求
interface ResumeRequest {
  thread_id: string;
  interrupt_id: string;
  response: any;  // 用户的选择或输入
}
```

### 3.2 前端处理流程

```typescript
// 监听 SSE 事件
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === "interrupt") {
    // 显示中断 UI
    showInterruptDialog(data.data);
  } else if (data.type === "content") {
    // 正常内容
    appendContent(data.content);
  }
};

// 用户响应后恢复
async function handleUserResponse(interruptId: string, response: any) {
  await fetch("/api/v1/agent/resume", {
    method: "POST",
    body: JSON.stringify({
      thread_id: currentThreadId,
      interrupt_id: interruptId,
      response: response
    })
  });
}
```

### 3.3 UI 组件示例

```tsx
// InterruptDialog.tsx
function InterruptDialog({ interrupt, onRespond }) {
  const { interrupt_type, message, options, versions } = interrupt;

  switch (interrupt_type) {
    case "confirmation":
      return (
        <Dialog>
          <DialogContent>
            <p>{message}</p>
            <div className="flex gap-2">
              {options.map(opt => (
                <Button
                  key={opt}
                  onClick={() => onRespond(opt)}
                >
                  {opt}
                </Button>
              ))}
            </div>
          </DialogContent>
        </Dialog>
      );

    case "select_version":
      return (
        <Dialog>
          <DialogContent>
            <p>{message}</p>
            <div className="space-y-4">
              {versions.map(v => (
                <Card
                  key={v.id}
                  onClick={() => onRespond(v.id)}
                  className="cursor-pointer hover:border-primary"
                >
                  <CardHeader>
                    <Badge>{v.style}</Badge>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm">{v.content.slice(0, 200)}...</p>
                  </CardContent>
                </Card>
              ))}
              <Button variant="outline" onClick={() => onRespond("cancel")}>
                取消
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      );

    case "text_input":
      return (
        <Dialog>
          <DialogContent>
            <p>{message}</p>
            <Textarea
              ref={inputRef}
              placeholder="请输入..."
            />
            <Button onClick={() => onRespond(inputRef.current.value)}>
              提交
            </Button>
          </DialogContent>
        </Dialog>
      );
  }
}
```

---

## 四、后端实现

### 4.1 API 端点

```python
# api/v1/agent.py

from langgraph.types import Command
from deepagents import create_deep_agent

@router.post("/chat")
async def chat(request: ChatRequest):
    """对话接口 - 支持流式 + 中断"""
    agent = get_writing_agent()

    async def generate():
        async for event in agent.astream(
            {"messages": [{"role": "user", "content": request.message}]},
            config={"configurable": {"thread_id": request.thread_id}},
            stream_mode="values"
        ):
            if event.get("__interrupt__"):
                # 中断事件
                yield f"data: {json.dumps({'type': 'interrupt', 'data': event['__interrupt__']})}\n\n"
            else:
                # 正常内容
                yield f"data: {json.dumps({'type': 'content', 'data': event})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.post("/resume")
async def resume(request: ResumeRequest):
    """恢复中断的执行"""
    agent = get_writing_agent()

    # 使用 Command(resume=...) 恢复
    result = await agent.ainvoke(
        None,  # 不需要新消息
        config={"configurable": {"thread_id": request.thread_id}},
        command=Command(resume=request.response)
    )

    return result
```

### 4.2 流式恢复

```python
@router.post("/resume/stream")
async def resume_stream(request: ResumeRequest):
    """恢复中断 - 流式响应"""
    agent = get_writing_agent()

    async def generate():
        async for event in agent.astream(
            None,
            config={"configurable": {"thread_id": request.thread_id}},
            command=Command(resume=request.response),
            stream_mode="values"
        ):
            if event.get("__interrupt__"):
                yield f"data: {json.dumps({'type': 'interrupt', 'data': event['__interrupt__']})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'content', 'data': event})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

---

## 五、中断类型设计

### 5.1 确认型中断

```python
# 用于需要用户确认的操作
CONFIRMATION_INTERRUPT = {
    "type": "confirmation",
    "message": str,           # 提示信息
    "options": ["确认", "取消"],  # 固定选项
    "details": Optional[str], # 详细说明
    "severity": "normal" | "warning" | "danger"  # 严重程度
}
```

### 5.2 选择型中断

```python
# 用于多选一场景
SELECT_INTERRUPT = {
    "type": "select",
    "message": str,
    "options": [
        {"value": str, "label": str, "description": Optional[str]}
    ],
    "allow_cancel": bool,
    "default": Optional[str]
}
```

### 5.3 版本选择中断

```python
# 专门用于改写场景
VERSION_SELECT_INTERRUPT = {
    "type": "select_version",
    "message": str,
    "original": str,          # 原文
    "versions": [
        {
            "id": int,
            "content": str,
            "style": str,
            "diff_summary": Optional[str]  # 与原文的差异摘要
        }
    ],
    "allow_custom": bool      # 是否允许用户自己输入
}
```

### 5.4 输入型中断

```python
# 用于需要用户输入的场景
INPUT_INTERRUPT = {
    "type": "text_input",
    "message": str,
    "placeholder": Optional[str],
    "default": Optional[str],
    "required": bool,
    "validation": Optional[str]  # 验证规则
}
```

### 5.5 进度控制中断

```python
# 用于长任务的进度控制
PROGRESS_INTERRUPT = {
    "type": "progress_control",
    "message": str,
    "current_step": int,
    "total_steps": int,
    "options": ["继续", "暂停", "终止"],
    "current_output": Optional[str]  # 当前已生成的内容
}
```

---

## 六、实际应用场景

### 6.1 改写确认流程（使用 interrupt_on）

```python
# 工具定义
def smart_rewrite_with_confirm(
    text: str,
    instruction: str,
    chapter_id: str = None
) -> dict:
    """改写并确认保存"""
    from app.services.ai import get_ai_service

    ai_service = get_ai_service()

    # 生成改写版本
    versions = []
    for i in range(3):
        result = ai_service.call_ai_sync(
            system_prompt="你是文字改写专家",
            user_prompt=f"改写指令：{instruction}\n原文：{text}",
            temperature=0.7 + i * 0.1
        )
        versions.append({
            "id": i + 1,
            "content": result,
            "style": ["保守", "中等", "激进"][i]
        })

    return {
        "original_text": text,
        "versions": versions,
        "chapter_id": chapter_id
    }

# 配置 Agent
agent = create_deep_agent(
    tools=[smart_rewrite_with_confirm],
    interrupt_on={
        "smart_rewrite_with_confirm": {
            "allowed_decisions": ["select_1", "select_2", "select_3", "cancel"]
        }
    }
)
```

### 6.2 批量分析（带进度控制）

```python
def batch_analyze(chapter_ids: str) -> str:
    """批量分析章节 - 支持中途停止

    Args:
        chapter_ids: 章节ID列表，逗号分隔
    """
    from app.services.chapter import get_chapter_service

    chapter_service = get_chapter_service()
    ids = [id.strip() for id in chapter_ids.split(",")]

    results = []
    for i, chapter_id in enumerate(ids):
        chapter = chapter_service.get_chapter_sync(chapter_id)
        if chapter:
            # 执行分析
            result = f"章节 {chapter.title}: 分析完成"
            results.append(result)

    return "\n".join(results)

# 如果需要进度控制，可以配置 interrupt_on
agent = create_deep_agent(
    tools=[batch_analyze],
    interrupt_on={
        "batch_analyze": True  # 执行前确认
    }
)
```

### 6.3 创建角色（参数收集）

```python
def create_character(name: str, description: str = "") -> str:
    """创建角色

    Args:
        name: 角色名称
        description: 角色描述（可选）
    """
    from app.services.character import get_character_service

    character_service = get_character_service()

    character = character_service.create_character_sync(
        name=name,
        description=description
    )

    return f"角色创建成功：{character.name}"

# 工具本身是简单的，由 LLM 负责收集参数
# 如果需要确认，配置 interrupt_on
```

---

## 七、错误处理

### 7.1 中断超时

```python
@tool
async def with_timeout(param: str, runtime: ToolRuntime) -> str:
    """带超时的中断"""

    try:
        # 设置超时（通过配置）
        response = interrupt({
            "type": "confirmation",
            "message": "请在 5 分钟内确认",
            "timeout": 300  # 秒
        })
        return f"用户确认: {response}"
    except InterruptTimeout:
        return "用户未响应，操作已取消"
```

### 7.2 用户取消

```python
@tool
async def cancellable_operation(runtime: ToolRuntime) -> str:
    """可取消的操作"""

    response = interrupt({
        "type": "confirmation",
        "message": "是否继续？",
        "options": ["继续", "取消"]
    })

    if response == "取消":
        # 清理已分配的资源
        await cleanup()
        return "操作已取消"

    return await do_operation()
```

---

## 八、测试方案

### 8.1 单元测试

```python
@pytest.mark.asyncio
async def test_interrupt_confirmation():
    """测试确认型中断"""
    agent = create_test_agent()

    # 启动执行
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "执行危险操作"}]
    })

    # 验证中断
    assert result.get("__interrupt__") is not None
    assert result["__interrupt__"]["type"] == "confirmation"

    # 恢复执行
    result = await agent.ainvoke(
        None,
        command=Command(resume="确认")
    )

    # 验证继续执行
    assert "执行成功" in result["messages"][-1].content
```

### 8.2 集成测试

```python
@pytest.mark.asyncio
async def test_interrupt_flow_e2e():
    """端到端测试中断流程"""

    # 1. 发起请求
    response = await client.post("/api/v1/agent/chat", json={
        "message": "改写这段文字",
        "thread_id": "test-thread"
    })

    # 2. 解析 SSE 事件
    events = parse_sse(response)
    interrupt_event = next(e for e in events if e["type"] == "interrupt")

    # 3. 验证中断数据
    assert interrupt_event["data"]["type"] == "select_version"
    assert len(interrupt_event["data"]["versions"]) == 3

    # 4. 发送恢复请求
    resume_response = await client.post("/api/v1/agent/resume", json={
        "thread_id": "test-thread",
        "interrupt_id": interrupt_event["data"]["interrupt_id"],
        "response": 1  # 选择第一个版本
    })

    # 5. 验证恢复结果
    assert resume_response.status_code == 200
```

---

## 九、迁移检查清单

- [ ] interrupt 基础功能实现
- [ ] 各类中断类型定义完成
- [ ] API 端点 `/chat` 支持中断
- [ ] API 端点 `/resume` 实现
- [ ] 前端 SSE 处理逻辑
- [ ] 前端中断 UI 组件
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 超时处理
- [ ] 错误处理

---

## 十、下一步

阅读 `07-implementation-plan.md` 了解详细的实施计划和时间安排。
