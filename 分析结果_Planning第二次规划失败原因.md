# Planning AI 规划流程详细分析 - 为什么第一次定位失败未被第二次规划使用

## 核心发现：对话历史不包含执行结果

### 问题描述
用户场景：
1. 第一次问："在主角出场的地方添加一段描写"
2. 规划生成：生成了 `locate_content` 任务定位内容位置
3. 执行失败：`locate_content` 返回错误（找不到位置）
4. 第二次问："那就在第二段添加描写"
5. **预期**：第二次规划应该看到第一次定位失败的信息
6. **实际**：第二次规划看不到第一次失败的信息，看不到第一次生成的规划

---

## 代码流程分析

### 1️⃣ **对话历史加载（ContextManager）**

**文件**：`langgraph_agent.py` 第 1291-1349 行

```python
# 加载对话历史（使用 ContextManager 压缩）
context_bundle = await self.context_manager.build_context(
    session_id=isolated_thread_id,
    system_prompt="",  # Planning 阶段不需要系统提示
    query=message,
    work_id=work_id
)

messages = context_bundle.get("messages", [])
context_obj = context_bundle.get("context")
metadata = context_bundle.get("metadata", {})

# 构建历史部分：只包含 user/assistant 的对话内容
recent_lines = []
for msg in messages:
    role = msg.get("role", "")
    content = msg.get("content", "")
    if role == "user":
        recent_lines.append(f"用户: {content}")
    elif role == "assistant":
        recent_lines.append(f"助手: {content}")

conversation_history = "\n".join(recent_lines)
```

**关键点**：
- ✅ 保存了用户和助手的对话文本
- ❌ **没有保存**：规划内容（plan_data）
- ❌ **没有保存**：任务执行结果（task_results）
- ❌ **没有保存**：执行过程中的错误信息

---

### 2️⃣ **第一次规划调用**

**文件**：`langgraph_agent.py` 第 1404-1411 行

```python
plan_data = await self.plan_generator.generate_plan(
    message=message,
    work_id=work_id,
    chapter_id=chapter_id,
    context=context,
    conversation_history=conversation_history,  # ← 只有对话历史，没有任务结果
    enable_reflection=enable_reflection
)
```

**plan_generator.py** 中的 `_build_plan_prompt_async` 构建 Prompt：

```python
plan_prompt = f"""AI写作助手。{history_section}{knowledge_section}{selected_text_section}
用户: {message}

【内部参数 - 用户不可见】
work_id: {work_id}
chapter_id: {chapter_id}
```

**Prompt 包含的内容**：
- ✅ 对话历史（用户/助手的聊天记录）
- ✅ 知识库文档（如果用户引用）
- ✅ 选中的文本（如果用户选中）
- ❌ **没有**：第一次规划的任务列表
- ❌ **没有**：第一次任务执行的结果
- ❌ **没有**：第一次执行中的错误信息

---

### 3️⃣ **任务执行阶段**

**文件**：`langgraph_agent.py` 第 1731-1741 行

```python
task_results = await self._execute_tasks_in_parallel(
    tasks=plan_data["tasks"],
    work_id=work_id,
    chapter_id=chapter_id,
    context=initial_context,
    context_payload=context,
    on_task_start=wrapped_on_task_start,
    on_task_progress=on_task_progress,
    on_task_done=wrapped_on_task_done,
    conversation_id=conversation_id
)
```

**执行结果生成**：
- ✅ `task_results` 列表包含每个任务的执行结果
- ✅ 包括失败的任务和错误信息
- ❌ **但是**这些结果**不会被保存到对话历史**

---

### 4️⃣ **第二次规划时**

当用户发送第二条消息时：

```python
# 再次加载历史
context_bundle = await self.context_manager.build_context(...)
messages = context_bundle.get("messages", [])  # ← 只有两条消息：
                                               #   用户消息1
                                               #   助手回复1（只是文本，没有规划或任务结果）

# 构建对话历史
conversation_history = """
用户: 在主角出场的地方添加一段描写
助手: [这里是最终响应文本，但没有任务执行细节]

用户: 那就在第二段添加描写
"""

# 调用规划生成器
plan_data = await self.plan_generator.generate_plan(
    message="那就在第二段添加描写",  # ← 新消息
    conversation_history=conversation_history  # ← 看不到第一次的任务和失败信息
)
```

---

## 问题根源：三层断裂

### 1. **规划→执行的断裂**
```
[Planning AI 生成规划] 
    ↓ (返回 plan_data)
[执行器执行任务]
    ↓ (产生 task_results)
[构建最终响应]
    ↓ (只返回文本)
[保存到对话历史]  ← ❌ 只保存了最终文本，没有保存规划和任务结果
```

### 2. **对话历史的限制**
```
ContextManager.build_context() 返回：
{
    "messages": [
        {"role": "user", "content": "用户消息1"},
        {"role": "assistant", "content": "最终响应文本"}  ← ❌ 没有：
                                                        - 规划内容
                                                        - 任务列表
                                                        - 执行结果
    ]
}
```

### 3. **Prompt 构建的缺陷**
```
Planning Prompt 中包含：
✅ 用户消息
✅ 对话历史
✅ 知识库文档
❌ 第一次规划的任务（plan_data）
❌ 第一次执行的结果（task_results）
❌ 执行中的错误信息
```

---

## 具体流程图

### 第一次交互
```
用户问：在主角出场的地方添加一段描写
          ↓
[Planning AI] → 生成规划：
                task_1: locate_content(query="主角出场的地方")
                task_2: smart_insert(位置=task_1结果)
          ↓
[执行器] → 执行 task_1
           task_1 失败：locate_content 返回错误"无法定位"
           回复给用户："我没找到主角出场的地方，能提供更多信息吗？"
          ↓
[ContextManager] → 保存对话：
                   {"role": "user", "content": "在主角出场的地方添加一段描写"}
                   {"role": "assistant", "content": "我没找到主角出场的地方，能提供更多信息吗？"}
                   
          ❌ 没有保存：
             - 原始规划（task_1/task_2）
             - 执行失败的细节
             - 为什么失败了
```

### 第二次交互
```
用户问：那就在第二段添加描写
          ↓
[ContextManager] → 加载历史：
                   对话历史只有：
                   用户: 在主角出场的地方添加一段描写
                   助手: 我没找到主角出场的地方，能提供更多信息吗？
          ↓
[Planning AI] → 生成新规划
                看到的历史信息：用户第一次失败询问，但看不到：
                ❌ 为什么失败（locate_content 失败）
                ❌ 尝试过什么（define_content 任务）
                ❌ 错误详情
                
                所以 Planning AI 可能重复同样的错误
```

---

## 代码证据

### 证据1：对话历史只包含文本
**文件**：`langgraph_agent.py` 第 1333-1347 行

```python
# 格式化近期对话消息（只取 user/assistant）
recent_lines = []
for msg in messages:
    role = msg.get("role", "")
    content = msg.get("content", "")
    if role == "user":
        recent_lines.append(f"用户: {content}")
    elif role == "assistant":
        recent_lines.append(f"助手: {content}")
        
if recent_lines:
    history_parts.append("【近期对话】\n" + "\n".join(recent_lines))

conversation_history = "\n".join(history_parts)
```

**问题**：`msg.get("content")` 只是文本，完全没有访问 plan_data 或 task_results

---

### 证据2：执行结果没有被保存到历史

**文件**：`langgraph_agent.py` 第 1817-1829 行

```python
# 保存对话到 ContextManager
await self.context_manager.update_context(
    session_id=isolated_thread_id,
    new_messages=[
        {"role": "user", "content": message},
        {"role": "assistant", "content": final_content}  # ← 只保存了最终文本
    ],
    context=context_bundle.get("context") if context_bundle else None,
    work_id=work_id
)
```

**问题**：
- ❌ 没有保存 `plan_data`
- ❌ 没有保存 `task_results`
- ❌ 没有保存任务执行的详细信息

---

## 为什么第一次失败的定位信息没有被第二次 Planning 使用

### 根本原因

**对话历史链断裂**：
```
第一次规划 → 执行失败 → 最终回复给用户
                      ↓
              保存到对话历史（只有文本）
                      ↓
第二次规划加载历史 → 看不到第一次规划和执行细节
```

### 具体影响

1. **Planning AI 看不到失败细节**
   - 看到用户说"在主角出场的地方添加"
   - 看到助手说"无法找到"
   - ❌ 看不到为什么无法找到（locate_content 失败）
   - ❌ 看不到尝试过的定位方法

2. **Planning AI 无法做出更好的规划**
   - 可能重复同样的错误
   - 无法优化定位策略
   - 无法提出替代方案

3. **用户体验差**
   - 第二次可能还是失败
   - 助手看起来"没有学习"

---

## 解决方案概括

### 方案1：保存规划和执行结果到对话历史
```python
await self.context_manager.update_context(
    session_id=isolated_thread_id,
    new_messages=[
        {"role": "user", "content": message},
        {
            "role": "assistant",
            "content": final_content,
            # ✅ 新增：保存规划和执行细节
            "plan": plan_data,
            "task_results": task_results
        }
    ],
    work_id=work_id
)
```

### 方案2：在 Prompt 中包含上一次的规划和结果
```python
plan_prompt = f"""...
【历史规划和执行结果】
{self._format_previous_execution_context(conversation_history)}
...
"""
```

### 方案3：为失败的任务生成诊断建议
```python
def _diagnose_execution_failures(task_results):
    """分析哪些任务失败以及原因"""
    failures = [t for t in task_results if t["status"] == "failed"]
    return {
        "failed_tasks": failures,
        "diagnosis": "locate_content 定位失败，建议使用段落编号而不是语义定位"
    }
```

---

## 关键代码位置

| 位置 | 文件和行号 | 说明 |
|------|-----------|------|
| 对话历史加载 | `langgraph_agent.py:1291-1349` | ContextManager 加载历史 |
| 规划调用 | `langgraph_agent.py:1404-1411` | generate_plan 调用 |
| Prompt 构建 | `plan_generator.py:180-259` | 构建规划 Prompt |
| 任务执行 | `langgraph_agent.py:1731-1741` | 执行任务 |
| 历史保存 | `langgraph_agent.py:1817-1829` | 保存对话到历史 |
| 参数解析 | `parallel_executor.py:361-485` | 任务执行和结果注册 |

---

## 总结

**问题**：Planning AI 在第二次规划时无法看到第一次定位失败的信息

**原因**：对话历史链在"执行阶段"断裂
- ✅ 对话文本被保存：用户和助手的消息
- ❌ 规划细节未保存：plan_data
- ❌ 执行结果未保存：task_results
- ❌ 错误信息未保存：为什么失败

**后果**：
- Planning AI 看不到上一次的规划
- Planning AI 看不到执行失败的原因
- Planning AI 可能重复同样的错误
- 用户体验不好

**解决方向**：需要在保存对话历史时，同时保存规划和执行结果，这样第二次规划才能看到完整的上下文。
