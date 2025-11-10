# 使用默认writing_agent模板的健壮性分析

**分析日期**: 2025-11-10
**分析人**: Claude Code
**结论**: ⚠️ **不够健壮,存在严重问题**

---

## ❌ 发现的问题

### 问题: 使用错误的Prompt模板会影响Agent行为

**当前方案**:
```python
# chat_stream中使用默认writing_agent模板
system_prompt = self.prompt_manager.render("writing_agent", ...)
```

**问题分析**:

#### 场景1: 用户问一般问题 "你好"
- 规则识别 → `general` → 路由到 `general_chat` Agent
- **但初始Prompt是writing_agent**: "你是专业的网络小说作家Agent"
- general_chat Agent会用**写作专家的身份**回答普通问候
- ❌ **角色定位错误**

#### 场景2: 用户问创作问题 "如何写好战斗场景?"
- 规则识别 → `analysis` → 路由到 `analysis_agent`
- **但初始Prompt是writing_agent**: "专注于创作网文故事"
- analysis_agent应该用**问答顾问**的方式回答
- ❌ **回答方式可能不对**

#### 场景3: 用户要求规划 "帮我规划小说大纲"
- 规则识别 → `planning` → 路由到 `planning_agent`
- **但初始Prompt是writing_agent**: "你是网文作家,写故事"
- planning_agent应该用**规划助手**的角色
- ❌ **角色混淆**

---

## 📊 Prompt模板对比

| Agent类型 | 角色定位 | 核心能力 | 输出格式 |
|----------|---------|---------|---------|
| **writing_agent** | 网络小说作家 | 章节续写、情节推进、人物刻画 | 小说内容 |
| **query_agent** | 创作顾问 | 解答问题、提供建议、分享经验 | 结构化回答 |
| **planning_agent** | 规划助手 | 大纲设计、世界观构建、角色设定 | 结构化规划 |
| **analysis_agent** | (未读取,但应该是分析专家) | 分析文本、评估质量 | 分析报告 |

**差异**: 每个Agent的**角色、能力、输出格式**都完全不同!

---

## ⚠️ 影响程度分析

### 轻微影响场景 ✅
- **writing请求**: 用writing_agent模板 → 路由到writing_agent ✅ 完全匹配

### 中度影响场景 ⚠️
- **general请求**: 用writing_agent模板 → 路由到general_chat
  - 影响: 可能用"网文作家"的口吻回答普通问候
  - 严重性: 中 (不影响功能,但角色不对)

### 严重影响场景 ❌
- **planning请求**: 用writing_agent模板 → 路由到planning_agent
  - 影响: planning_agent收到"你是作家,写故事"的指令
  - 但实际应该是"你是规划助手,做规划"
  - 严重性: 高 (可能导致输出格式错误)

- **query请求**: 用writing_agent模板 → 路由到query_agent
  - 影响: query_agent收到"写小说"的指令
  - 但实际应该是"回答问题,提供建议"
  - 严重性: 高 (回答方式可能不对)

---

## 🔍 深度分析: LangGraph如何处理Prompt

### 关键问题: LangGraph的Prompt机制

让我检查LangGraph的Agent节点如何使用system_prompt:

**chat_stream流程**:
```python
1. system_prompt = render("writing_agent", ...)
2. context_bundle = context_manager.build_context(
     system_prompt=system_prompt,  # ← writing_agent的Prompt
     ...)
3. history_messages = convert(context_bundle["messages"])
4. initial_state = {
     "messages": history_messages + [HumanMessage(message)],
     ...
   }
5. graph.astream(initial_state)
   → intent_classifier节点 → 识别intent
   → 路由到对应Agent (writing/planning/query/...)
```

**问题**: initial_state的messages中已经包含了writing_agent的system_prompt!

**后续Agent是否会覆盖?**
- 需要检查各Agent节点(_handle_writing, _handle_planning等)
- 是否重新设置SystemMessage?

---

## 💡 解决方案对比

### 方案A: 当前方案 (使用默认writing_agent) ❌

**优点**:
- 简单,无需预先识别

**缺点**:
- 角色定位可能错误
- 不同Agent收到不匹配的Prompt
- 可能影响输出质量

**风险**: 中高

### 方案B: 在chat_stream中保留意图识别 ⚠️

**优点**:
- 可以选择正确的Prompt模板
- 各Agent收到匹配的Prompt

**缺点**:
- 重复识别 (chat_stream一次 + LangGraph一次)
- 浪费性能

**风险**: 低 (功能正确,但有重复)

### 方案C: 不使用context_manager的system_prompt ✅ 推荐

**思路**:
```python
# chat_stream中
context_bundle = context_manager.build_context(
    system_prompt="",  # ← 不设置,或使用通用Prompt
    ...
)

# 让各Agent节点自己设置正确的system_prompt
```

**需要验证**: 各Agent节点是否会自己设置SystemMessage

### 方案D: 使用通用的base_prompt ✅ 推荐

**思路**:
```python
# 创建一个通用的base_agent模板
base_prompt = """
你是AI写作助手,根据用户需求提供专业的帮助。

核心能力:
- 小说创作和续写
- 写作规划和建议
- 问题解答和指导
- 文本分析和评估

请根据具体任务调整你的回答方式。
"""

system_prompt = base_prompt  # 使用通用Prompt
```

**优点**:
- 不会误导Agent
- 保持通用性
- 各Agent可以自己补充专业Prompt

---

## 🔧 需要验证的关键问题

### 问题1: 各Agent节点是否重新设置SystemMessage?

需要检查:
```python
async def _handle_writing(self, state):
    # 是否有: messages = [SystemMessage(writing_prompt)] + state["messages"]?
    pass

async def _handle_planning(self, state):
    # 是否有: messages = [SystemMessage(planning_prompt)] + state["messages"]?
    pass
```

**如果有** → 当前方案可行 ✅
**如果没有** → 当前方案有问题 ❌

### 问题2: context_manager的system_prompt如何使用?

需要检查:
```python
context_bundle = context_manager.build_context(
    system_prompt=system_prompt,  # ← 这个Prompt去哪了?
    ...
)
```

**可能性1**: 放入messages[0]作为SystemMessage
**可能性2**: 只用于上下文构建,不影响对话
**可能性3**: 被后续Agent覆盖

---

## ✅ 推荐行动

### 立即执行

1. **验证各Agent节点是否重新设置SystemMessage**
   ```python
   # 检查 _handle_writing, _handle_planning, _handle_general等
   # 看是否有 SystemMessage 的重新设置
   ```

2. **如果Agent节点会覆盖**:
   - ✅ 当前方案可行
   - 只是chat_stream传入的system_prompt被忽略

3. **如果Agent节点不会覆盖**:
   - ❌ 必须修复
   - 建议使用方案D (通用base_prompt)
   - 或方案C (不设置system_prompt)

---

## 📝 结论

**当前方案是否健壮**: ⚠️ **不确定,需要验证**

**关键因素**:
- 各Agent节点是否重新设置SystemMessage
- context_manager的system_prompt如何被使用

**建议**:
1. 立即检查各Agent节点的实现
2. 如果发现问题,使用通用base_prompt
3. 添加测试验证不同场景的输出

**风险评级**: 🟡 **中等** (可能影响输出质量)

---

**下一步**: 检查Agent节点的实现代码

[返回Review报告](./Phase2.4_最终Review报告.md)
