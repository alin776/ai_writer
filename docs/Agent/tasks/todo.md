# P0优化实施任务清单

## 📋 任务概览

基于《P0优化-精确实施指南》，执行13处代码修改以实现：
- ✅ 模型智能选择（根据任务类型自动选择最优模型）
- ✅ 上下文智能压缩（将Summarization上下文从16K压缩至3K tokens）
- ✅ 性能提升目标：响应时间从2分16秒优化至25-35秒（提升75-82%）

预计总耗时：**90分钟**

---

## ✅ 任务列表

### 准备阶段

- [ ] **Task 0: 备份关键文件**
  - 备份 `backend/app/core/config.py`
  - 备份 `backend/app/services/ai/http_ai_service.py`
  - 备份 `backend/app/services/agent/langgraph_agent.py`
  - 备份 `backend/app/services/agent/tools/writing_tools.py`
  - 预计时间：2分钟

---

### 第一部分：配置和核心服务（2处修改）

- [ ] **Task 1: 修改 config.py - 添加模型选择配置**
  - 文件：`backend/app/core/config.py`
  - 位置：文件末尾
  - 添加：`MODEL_SELECTION_ENABLED = True`
  - 可选：切换默认模型为 `gemini-2.5-flash`（快速验证）
  - 预计时间：1分钟
  - 难度：⭐ 简单

- [ ] **Task 2: 修改 http_ai_service.py - 实现模型选择逻辑 ⭐关键**
  - 文件：`backend/app/services/ai/http_ai_service.py`
  - 位置：Line 113-123
  - 修改：在 `_stream_chat` 方法中实现动态模型选择
  - 关键点：
    - 添加 ModelSelector 调用逻辑
    - 使用动态 model 替换固定 self.model
    - 更新 cache_key 生成逻辑
    - 添加日志记录
  - 预计时间：15分钟
  - 难度：⭐⭐⭐ 关键

---

### 第二部分：LangGraph Agent优化（6处修改）

- [ ] **Task 3: langgraph_agent.py - 导入TaskType**
  - 文件：`backend/app/services/agent/langgraph_agent.py`
  - 位置：文件顶部import区域（约Line 1-30）
  - 添加：`from app.services.agent.model_selector import TaskType`
  - 预计时间：1分钟
  - 难度：⭐ 简单

- [ ] **Task 4: langgraph_agent.py - 修改_generate_text方法签名 ⭐关键**
  - 文件：`backend/app/services/agent/langgraph_agent.py`
  - 位置：Line 670-689
  - 修改：添加 `task_type: Optional[TaskType] = None` 参数
  - 修改：传递 task_type 给 _stream_chat
  - 预计时间：10分钟
  - 难度：⭐⭐⭐ 关键

- [ ] **Task 5: langgraph_agent.py - Planning阶段传递task_type**
  - 文件：`backend/app/services/agent/langgraph_agent.py`
  - 位置：Line 1629
  - 修改：添加 `task_type=TaskType.STORY_PLANNING`
  - 预计时间：2分钟
  - 难度：⭐ 简单

- [ ] **Task 6: langgraph_agent.py - 添加压缩函数 ⭐关键**
  - 文件：`backend/app/services/agent/langgraph_agent.py`
  - 位置：Line 1366之前（类定义外部）
  - 添加：
    - `_compress_task_result()` 函数
    - `_build_summarization_context()` 函数
  - 预计时间：20分钟
  - 难度：⭐⭐ 中等

- [ ] **Task 7: langgraph_agent.py - 验证Execution阶段收集结果**
  - 文件：`backend/app/services/agent/langgraph_agent.py`
  - 位置：Line 1709-1746
  - 检查：确认 task_results 列表正确收集
  - 预计时间：5分钟
  - 难度：⭐ 简单（验证为主）

- [ ] **Task 8: langgraph_agent.py - Summarization使用压缩 ⭐关键**
  - 文件：`backend/app/services/agent/langgraph_agent.py`
  - 位置：Line 1757-1777
  - 修改：
    - 使用 `_build_summarization_context()` 压缩上下文
    - 添加压缩日志
    - 传递 `task_type=TaskType.SUMMARIZATION`
  - 预计时间：10分钟
  - 难度：⭐⭐ 中等

---

### 第三部分：Writing Tools优化（5处修改）

- [ ] **Task 9: writing_tools.py - 导入TaskType**
  - 文件：`backend/app/services/agent/tools/writing_tools.py`
  - 位置：文件顶部import区域
  - 添加：使用 TYPE_CHECKING 导入 TaskType
  - 预计时间：2分钟
  - 难度：⭐ 简单

- [ ] **Task 10: writing_tools.py - 修改_generate_text签名 ⭐关键**
  - 文件：`backend/app/services/agent/tools/writing_tools.py`
  - 位置：Line 51-88
  - 修改：添加 `task_type: Optional['TaskType'] = None` 参数
  - 修改：传递 task_type 给 _stream_chat
  - 预计时间：10分钟
  - 难度：⭐⭐⭐ 关键

- [ ] **Task 11: writing_tools.py - 续写工具传递task_type**
  - 文件：`backend/app/services/agent/tools/writing_tools.py`
  - 修改：在 `_continue_writing_func` 中添加 `task_type=TaskType.CONTENT_CREATION`
  - 预计时间：5分钟
  - 难度：⭐ 简单

- [ ] **Task 12: writing_tools.py - 润色工具传递task_type**
  - 文件：`backend/app/services/agent/tools/writing_tools.py`
  - 修改：在 `_polish_text_func` 中添加 `task_type=TaskType.CONTENT_CREATION`
  - 预计时间：5分钟
  - 难度：⭐ 简单

- [ ] **Task 13: writing_tools.py - 扩写工具传递task_type**
  - 文件：`backend/app/services/agent/tools/writing_tools.py`
  - 修改：在 `_expand_text_func` 中添加 `task_type=TaskType.CONTENT_CREATION`
  - 预计时间：5分钟
  - 难度：⭐ 简单

---

### 测试验证阶段

- [ ] **Task 14: 语法检查所有修改文件**
  - 检查 config.py
  - 检查 http_ai_service.py
  - 检查 langgraph_agent.py
  - 检查 writing_tools.py
  - 预计时间：5分钟

- [ ] **Task 15: 重启服务并测试**
  - 重启 FastAPI 服务
  - 测试简单查询功能
  - 测试续写功能
  - 预计时间：10分钟

- [ ] **Task 16: 验证日志输出和性能提升**
  - 检查 ModelSelector 日志
  - 检查上下文压缩日志
  - 测量响应时间改善
  - 预计时间：5分钟

---

## 📊 关键修改说明

### ⭐ 四个关键修改点

1. **http_ai_service.py Line 113-123** - 模型选择核心逻辑
   - 实现根据 task_type 动态选择模型
   - 这是整个优化的入口点

2. **langgraph_agent.py Line 670-689** - _generate_text签名
   - 添加 task_type 参数传递
   - 打通 Agent 到 AIService 的调用链

3. **langgraph_agent.py Line 1366** - 压缩函数
   - 实现智能压缩算法
   - 将 16K tokens 压缩到 3K tokens

4. **writing_tools.py Line 51-88** - 工具层_generate_text
   - 打通工具层到 AIService 的调用链
   - 确保所有工具都能使用模型选择

---

## 🔍 验证要点

### 日志检查
```bash
# 模型选择是否生效
grep "ModelSelector" backend/INFO.md | tail -20

# 上下文压缩是否生效
grep "压缩" backend/INFO.md | tail -10

# 响应时间
grep "Stream completed" backend/INFO.md | tail -10
```

### 预期日志输出
```
[ModelSelector] 任务=STORY_PLANNING, 模型=gemini-2.5-pro, 原因=复杂规划任务需要高质量模型
[ModelSelector] 任务=CONTENT_CREATION, 模型=gemini-2.5-pro, 原因=创作任务需要高质量输出
[Summarization] 上下文压缩: 原始=8500字符, 压缩后=2800字符, 压缩率=67%
[ModelSelector] 任务=SUMMARIZATION, 模型=gemini-2.5-flash, 原因=总结任务可使用快速模型
```

---

## ⚠️ 注意事项

1. **每次修改后保存文件**
2. **按顺序执行任务**（避免依赖问题）
3. **Task 2, 4, 6, 8, 10 是关键修改**，需要仔细核对代码
4. **修改完成后立即进行语法检查**
5. **遇到问题及时查看日志**

---

## 📝 进度记录

- 开始时间：_____________
- 完成时间：_____________
- 实际耗时：_____________

---

## 📈 预期效果

### 优化前
- 响应时间：2分16秒（136秒）
- Planning：19秒
- Execution：51秒
- Summarization：57秒（使用16K tokens）

### 优化后
- 响应时间：25-35秒
- Planning：18秒（保持pro质量）
- Execution：48秒（保持pro质量）
- Summarization：8秒（flash + 压缩至3K）
- **提升幅度：75-82%**

---

## ✨ Review 部分

> ⚠️ 此部分在所有任务完成后填写

### 修改总结
- [ ] 总修改文件数：4个
- [ ] 总代码行数变更：约150行
- [ ] 新增函数：2个（压缩函数）
- [ ] 修改函数签名：2个
- [ ] 新增参数传递：8处

### 遇到的问题


### 解决方案


### 最终效果


### 其他备注


---

# 🔴 **新发现的关键问题** 🔴

## 📅 2025-11-04 22:30 - 深度代码分析

### ❌ 问题根源已定位

**核心问题：** Execution阶段显示 `task_type=None`，导致强制使用默认的gemini-2.5-pro（慢且贵）

### 🔍 日志证据
```
22:25:14 - 开始调用 AI API: model=gemini-2.5-pro, max_tokens=2000, temp=0.8, task_type=None  ← 问题！
```

### 💡 根本原因

**在 `langgraph_agent.py` 中存在旧版工具，它们没有传递task_type：**

1. **旧版工具定义：** Line 131-193
   - `continue_writing_tool` (Line 131)
   - `polish_text_tool` (Line 155)
   - `analyze_text_tool` (Line 176)

2. **辅助函数缺陷：** Line 89-128 的 `_generate_text_helper`
   - ❌ **没有接受task_type参数**
   - ❌ **调用_stream_chat时没有传递task_type**（Line 101-107）

3. **调用链路：**
   ```
   旧版工具 (Line 151)
   → _generate_text_helper (Line 89, 缺少task_type参数)
   → _stream_chat (Line 101, 未传递task_type)
   → 导致task_type=None！
   ```

4. **对比：**
   - ✅ 新版工具（`writing_tools.py`）：正确传递task_type
   - ❌ 旧版工具（`langgraph_agent.py`）：未传递task_type
   - **系统正在使用旧版工具！**

### 🎯 精确修复方案

#### 修改1：修复 `_generate_text_helper` 函数（核心）

**位置：** `langgraph_agent.py:89-128`

```python
# 修改前：
async def _generate_text_helper(prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
    """辅助函数：使用 HTTPAIService 生成文本（带重试机制）"""
    ...
    async for chunk, _ in _global_ai_service._stream_chat(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
        # ❌ 缺少 task_type
    ):

# 修改后：
async def _generate_text_helper(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    task_type: Optional[TaskType] = None  # ← 新增参数
) -> str:
    """辅助函数：使用 HTTPAIService 生成文本（带重试机制）"""
    ...
    async for chunk, _ in _global_ai_service._stream_chat(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        task_type=task_type  # ← 传递参数
    ):
```

#### 修改2：修复旧版 `continue_writing_tool`

**位置：** `langgraph_agent.py:151`

```python
# 修改前：
return await _generate_text_helper(prompt, temperature=0.8, max_tokens=2000)

# 修改后：
return await _generate_text_helper(
    prompt,
    temperature=0.8,
    max_tokens=2000,
    task_type=TaskType.CONTENT_CREATION  # ← 新增
)
```

#### 修改3：修复旧版 `polish_text_tool`

**位置：** `langgraph_agent.py:172`

```python
# 修改前：
return await _generate_text_helper(prompt, temperature=0.7, max_tokens=2000)

# 修改后：
return await _generate_text_helper(
    prompt,
    temperature=0.7,
    max_tokens=2000,
    task_type=TaskType.TEXT_POLISH  # ← 新增
)
```

#### 修改4：修复旧版 `analyze_text_tool`

**位置：** `langgraph_agent.py:193`

```python
# 修改前：
return await _generate_text_helper(prompt, temperature=0.3, max_tokens=1500)

# 修改后：
return await _generate_text_helper(
    prompt,
    temperature=0.3,
    max_tokens=1500,
    task_type=TaskType.DEEP_ANALYSIS  # ← 新增
)
```

### 📊 预期效果

#### 修复前（当前）
```
[Planning] task_type=SIMPLE_QA, time=25s, model=flash-lite ✅
[Execution] task_type=None, time=42s, model=pro ❌
[Summarization] task_type=SUMMARIZATION, time=34s, model=flash ✅
总时间: 101s
```

#### 修复后（目标）
```
[Planning] task_type=SIMPLE_QA, time=10s, model=flash-lite ✅
[Execution] task_type=CONTENT_CREATION, time=15s, model=flash ✅
[Summarization] task_type=SUMMARIZATION, time=20s, model=flash ✅
总时间: 45s（提升56%！）
```

---

## 🚦 下一步行动

**等待用户确认，然后开始修复代码！**

---

**准备好了吗？等待确认后开始执行！** 🚀
