# Agent 工具调用错误分析报告

## 📋 问题总结

**时间**: 2025-11-09 20:22:00
**严重程度**: 🔴 P0（严重 - 所有工具调用失败）
**影响范围**: ReAct模式下的所有章节读取操作

### 核心错误

```
❌ invalid UUID 'ch_1': length must be between 32..36 characters, got 4
❌ invalid UUID 'ch_2': length must be between 32..36 characters, got 4
❌ invalid UUID 'ch_4': length must be between 32..36 characters, got 4
❌ invalid UUID 'YXTW_001': length must be between 32..36 characters, got 8
```

**统计**：5个工具调用全部失败（100%失败率）

---

## 🔍 根因分析

### 问题根源

**位置**: `backend/app/services/agent/langgraph_agent.py:2766`

```python
# ❌ 错误示例（当前代码）
- 示例：{{"tool": "read_chapter_tool", "params": {{"chapter_id": "abc-123-def"}}}}
```

**问题**：
1. ❌ `"abc-123-def"` 不是标准UUID格式（只有11个字符）
2. ❌ LLM学习了这个错误示例
3. ❌ 生成了简化ID：`ch_1`, `ch_2`, `ch_3`, `ch_4`
4. ❌ 数据库要求标准UUID（32-36字符），导致查询失败

### 真实UUID格式示例

```
✅ 正确: 550e8400-e29b-41d4-a716-446655440000  (36字符)
✅ 正确: c9dd9cbf-fa57-447e-9605-3020bbde5350  (36字符)
❌ 错误: abc-123-def                          (11字符)
❌ 错误: ch_1                                 (4字符)
```

---

## 📂 相关代码位置

### 1. 工具定义（第348-415行）

```python
@tool
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """读取指定章节工具：从数据库读取章节内容

    Args:
        work_id: 作品ID（可选，但强烈推荐提供）
        chapter_id: 章节ID  # ⚠️ 缺少UUID格式说明
    """
```

**问题**：
- ⚠️ 只标记为 `str` 类型
- ⚠️ docstring 没有说明必须是UUID格式
- ⚠️ 没有参数验证逻辑

### 2. Prompt示例（第2762-2766行）

```python
2. read_chapter_tool: 通过章节ID读取章节内容
   - 使用场景：已知具体的chapter_id时使用
   - 参数：chapter_id (字符串UUID)  # ✅ 文字说明了UUID
   - 注意：如果不知道具体的chapter_id，不要使用这个工具！应该用get_chapter_by_order_tool
   - 示例：{{"tool": "read_chapter_tool", "params": {{"chapter_id": "abc-123-def"}}}}  # ❌ 示例错误
```

**矛盾**：
- ✅ 第2764行文字说明：`(字符串UUID)`
- ❌ 第2766行示例代码：`"abc-123-def"`（不是UUID）

### 3. 数据库查询（chapter_service.py:50）

```python
# 数据库期望UUID格式
result = await self.db.execute(
    select(Chapter).where(Chapter.id == chapter_id)  # chapter_id必须是UUID
)
```

---

## 🔧 修复方案

### 方案1：修复Prompt示例（推荐 - P1优先级）

**位置**: `langgraph_agent.py:2766`

```python
# ❌ 修改前
- 示例：{{"tool": "read_chapter_tool", "params": {{"chapter_id": "abc-123-def"}}}}

# ✅ 修改后
- 示例：{{"tool": "read_chapter_tool", "params": {{"chapter_id": "627feba4-2097-4f28-a3f3-7641d10f7f40"}}}}
```

**优点**：
- ✅ 最直接有效
- ✅ LLM能正确学习UUID格式
- ✅ 无需修改其他代码

---

### 方案2：完善工具Docstring（推荐 - P2优先级）

**位置**: `langgraph_agent.py:350-358`

```python
# ❌ 修改前
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """读取指定章节工具：从数据库读取章节内容

    Args:
        work_id: 作品ID（可选，但强烈推荐提供）
        chapter_id: 章节ID
    """

# ✅ 修改后
async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    """读取指定章节工具：从数据库读取章节内容

    Args:
        work_id: 作品ID（可选，但强烈推荐提供），标准UUID格式（36字符）
        chapter_id: 章节ID，必须是标准UUID格式（例如：627feba4-2097-4f28-a3f3-7641d10f7f40）

    Returns:
        章节信息（包含标题和内容）的JSON字符串
    """
```

---

### 方案3：增强RAG上下文（可选 - P3优先级）

在Prompt中明确说明：

```python
**重要提示**：
1. 所有ID（work_id, chapter_id）都必须使用标准UUID格式（36字符）
2. 不要自己编造ID，必须从以下来源获取：
   - 用户上下文中的work_id
   - RAG检索结果中的真实chapter_id
   - get_context_tool返回的章节列表
3. 如果不知道具体的UUID，使用get_chapter_by_order_tool（通过章节序号查询）
```

---

### 方案4：添加参数验证（可选 - P4优先级）

```python
import re

UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

async def read_chapter_tool(work_id: Optional[str] = None, chapter_id: str = "") -> str:
    # ... 现有检查 ...

    # 新增：UUID格式验证
    if chapter_id and not UUID_PATTERN.match(chapter_id):
        return json.dumps({
            "error": f"无效的章节ID格式: {chapter_id}",
            "message": "章节ID必须是标准UUID格式（例如：627feba4-2097-4f28-a3f3-7641d10f7f40）",
            "suggestion": "请使用 get_chapter_by_order_tool 通过章节序号查询，或从上下文中获取真实的UUID"
        }, ensure_ascii=False, indent=2)
```

---

## ✅ 推荐实施顺序

| 优先级 | 方案 | 工作量 | 效果 | 时间估计 |
|-------|------|--------|------|----------|
| **P1** | 修复Prompt示例 | ⭐ 极小 | 🔥 立即见效 | 2分钟 |
| **P2** | 完善工具Docstring | ⭐⭐ 小 | ✅ 提升准确率 | 5分钟 |
| **P3** | 增强RAG上下文 | ⭐⭐ 小 | ✅ 提升鲁棒性 | 5分钟 |
| **P4** | 添加参数验证 | ⭐⭐⭐ 中 | ⚡ 更好错误提示 | 10分钟 |

**建议**：先实施P1（立即见效），再逐步实施P2-P4（提升质量）

---

## 📊 影响范围

### 受影响的工具
1. ✅ `read_chapter_tool` - 主要受影响
2. ✅ `get_chapter_by_order_tool` - 也可能受影响（如果prompt示例也有问题）
3. ✅ `search_analysis_fragments_tool` - work_id参数也是UUID

### 受影响的场景
1. ✅ ReAct模式的分析请求
2. ✅ 需要读取章节内容的所有操作
3. ✅ 跨章节的内容对比分析

---

## 🎯 验证方法

修复后，使用相同的测试请求验证：

```
请深度分析《一夕千悟》主角段融的以下方面：
1. 性格特征和心理变化
2. 能力体系和成长轨迹
3. ...
```

**期望结果**：
- ✅ 工具调用使用正确的UUID格式
- ✅ 数据库查询成功
- ✅ 返回完整的分析结果
- ✅ 无UUID验证错误

---

## 📝 附加说明

### 为什么会出现这个问题？

1. **历史原因**：可能早期代码使用简化ID进行测试
2. **文档不同步**：代码更新为UUID但示例未更新
3. **测试覆盖不足**：缺少工具调用的端到端测试

### 如何避免类似问题？

1. ✅ **代码审查**：重点检查Prompt示例的正确性
2. ✅ **集成测试**：添加完整的工具调用测试
3. ✅ **文档同步**：代码变更时同步更新示例
4. ✅ **参数验证**：关键参数添加格式验证

---

**生成时间**: 2025-11-09
**分析工具**: Claude Code
**严重程度**: P0（关键bug）
**状态**: ⏳ 待修复
