# Update 类工具设计

## 1. 概述

Update 类工具负责**创建、修改、删除内容**，改变系统状态。

**设计理念**：所有会改变数据的操作都归为 Update 类。

## 2. 工具分类

Update 类工具按功能分为三个子类：

| 子类 | 功能 | 工具数量 |
|------|------|---------|
| **创作类** | 生成新内容 | 3 个 |
| **增强类** | 增强现有内容 | 3 个 |
| **操作类** | 章节 CRUD | 5 个 |

## 3. 工具列表

### 3.1 创作类工具

| 工具 | 功能 | 需要 LLM |
|------|------|---------|
| `smart_continue` | 智能续写 | ✅ |
| `smart_rewrite` | 智能重写 | ✅ |
| `smart_insert` | 智能插入 | ✅ |

### 3.2 增强类工具

| 工具 | 功能 | 需要 LLM |
|------|------|---------|
| `show_emotion_tool` | 展示情感 | ✅ |
| `enhance_scene_tool` | 增强场景 | ✅ |
| `learn_style_tool` | 学习风格 | ✅ |

### 3.3 操作类工具

| 工具 | 功能 | 需要 LLM |
|------|------|---------|
| `apply_chapter_edit` | 应用编辑 | ❌ |
| `create_chapter` | 创建章节 | ❌ |
| `update_chapter_title` | 更新标题 | ❌ |
| `update_chapter_content` | 更新内容 | ❌ |
| `delete_chapter` | 删除章节 | ❌ |

---

## 4. 创作类工具详解

### 4.1 smart_continue（智能续写）

#### 功能描述

基于上下文智能续写章节内容。

#### 参数定义

```python
@dataclass
class SmartContinueInput:
    chapter_id: str              # 章节ID（必需）
    chapter_content: str = ""    # 章节内容（可选，避免重复查询）
    user_requirement: str = ""   # 用户续写要求
    target_length: int = 2000    # 目标长度（字数）
    style_reference: str = ""    # 风格参考
```

#### 返回格式

```json
{
    "success": true,
    "content": "续写的内容...",
    "word_count": 2150,
    "metadata": {
        "continuation_point": "从哪里开始续写",
        "style_applied": "应用的风格"
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 4.2 smart_rewrite（智能重写）

#### 功能描述

智能改写指定文本。

#### 参数定义

```python
@dataclass
class SmartRewriteInput:
    chapter_id: str              # 章节ID（必需）
    text_to_rewrite: str         # 待改写文本（必需）
    chapter_content: str = ""    # 章节内容（用于上下文）
    user_requirement: str = ""   # 用户改写要求
    base_version: str = ""       # 基础版本（用于版本控制）
```

#### 返回格式

```json
{
    "success": true,
    "original_text": "原文...",
    "rewritten_text": "改写后的内容...",
    "changes_summary": "主要修改了...",
    "metadata": {
        "paragraph_index": 3,
        "node_id": "abc123",
        "before_anchor": "...",
        "after_anchor": "..."
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 4.3 smart_insert（智能插入）

#### 功能描述

在指定位置智能插入内容。

#### 参数定义

```python
@dataclass
class SmartInsertInput:
    chapter_id: str              # 章节ID（必需）
    insert_position: str         # 插入位置描述（必需）
    chapter_content: str = ""    # 章节内容
    user_requirement: str = ""   # 用户插入要求
    target_length: int = 500     # 目标长度
```

#### 返回格式

```json
{
    "success": true,
    "inserted_text": "插入的内容...",
    "word_count": 520,
    "metadata": {
        "insert_after_paragraph": 3,
        "node_id": "abc123"
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

## 5. 增强类工具详解

### 5.1 show_emotion_tool（展示情感）

#### 功能描述

增强文本的情感表达。

#### 参数定义

```python
@dataclass
class ShowEmotionInput:
    text: str                    # 待增强文本（必需）
    emotion: str = ""            # 目标情感（可选）
    intensity: str = "medium"    # 情感强度：low, medium, high
```

#### 返回格式

```json
{
    "success": true,
    "original_text": "原文...",
    "enhanced_text": "增强后的内容...",
    "emotion_applied": "悲伤",
    "intensity": "high"
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 5.2 enhance_scene_tool（增强场景）

#### 功能描述

增强场景描写的细节和氛围。

#### 参数定义

```python
@dataclass
class EnhanceSceneInput:
    text: str                    # 待增强文本（必需）
    focus: str = "all"           # 增强重点：visual, auditory, tactile, all
    atmosphere: str = ""         # 目标氛围（可选）
```

#### 返回格式

```json
{
    "success": true,
    "original_text": "原文...",
    "enhanced_text": "增强后的内容...",
    "enhancements": ["增加了视觉描写", "增加了环境音效"]
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 5.3 learn_style_tool（学习风格）

#### 功能描述

从参考文本学习写作风格。

#### 参数定义

```python
@dataclass
class LearnStyleInput:
    reference_text: str          # 参考文本（必需）
    user_id: str = ""            # 用户ID（用于保存风格）
    style_name: str = ""         # 风格名称（可选）
```

#### 返回格式

```json
{
    "success": true,
    "style_features": {
        "avg_sentence_length": 25,
        "pov": "first_person",
        "dialogue_ratio": 0.3,
        "tone": "serious"
    },
    "style_prompt": "生成的风格提示词...",
    "saved": true
}
```

#### 变更说明

**无变更**，保持现有实现。

---

## 6. 操作类工具详解

### 6.1 apply_chapter_edit（应用编辑）

#### 功能描述

将编辑应用到章节，支持多种定位方式。

#### 参数定义

```python
@dataclass
class ApplyChapterEditInput:
    chapter_id: str              # 章节ID（必需）
    new_content: str             # 新内容（必需）
    # 定位方式（四选一）
    node_id: str = ""            # 节点ID（前端传入）
    paragraph_index: int = -1    # 段落索引
    original_text: str = ""      # 原文定位
    anchors: dict = None         # 锚点定位 {before: str, after: str}
```

#### 返回格式

```json
{
    "success": true,
    "chapter_id": "xxx",
    "operation": "replace",
    "affected_range": {
        "start_paragraph": 3,
        "end_paragraph": 3
    },
    "rollback_data": {
        "original_content": "原内容..."
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 6.2 create_chapter（创建章节）

#### 功能描述

创建新章节。

#### 参数定义

```python
@dataclass
class CreateChapterInput:
    work_id: str                 # 作品ID（必需）
    title: str                   # 章节标题（必需）
    content: str = ""            # 章节内容（可选）
    order: int = -1              # 章节顺序（-1 表示追加到末尾）
    conversation_id: str = ""    # 会话ID（用于操作日志）
```

#### 返回格式

```json
{
    "success": true,
    "chapter_id": "xxx",
    "title": "第六章 新的开始",
    "order": 6,
    "rollback_data": {
        "operation": "create",
        "chapter_id": "xxx"
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 6.3 update_chapter_title（更新标题）

#### 功能描述

修改章节标题。

#### 参数定义

```python
@dataclass
class UpdateChapterTitleInput:
    chapter_id: str              # 章节ID（必需，支持 UUID 或章节序号）
    new_title: str               # 新标题（必需）
    work_id: str = ""            # 作品ID（当 chapter_id 是序号时需要）
    conversation_id: str = ""    # 会话ID（用于操作日志）
```

#### 返回格式

```json
{
    "success": true,
    "chapter_id": "xxx",
    "old_title": "第一章",
    "new_title": "第一章 起源",
    "rollback_data": {
        "operation": "update_title",
        "chapter_id": "xxx",
        "old_title": "第一章"
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 6.4 update_chapter_content（更新内容）

#### 功能描述

更新章节内容。

#### 参数定义

```python
@dataclass
class UpdateChapterContentInput:
    chapter_id: str              # 章节ID（必需）
    new_content: str             # 新内容（必需）
    operation: str = "replace"   # 操作类型：replace, append, insert
    position: int = -1           # 插入位置（operation=insert 时需要）
    work_id: str = ""            # 作品ID
    conversation_id: str = ""    # 会话ID（用于操作日志）
```

#### 返回格式

```json
{
    "success": true,
    "chapter_id": "xxx",
    "operation": "replace",
    "word_count": 3500,
    "rollback_data": {
        "operation": "update_content",
        "chapter_id": "xxx",
        "old_content": "原内容..."
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

### 6.5 delete_chapter（删除章节）

#### 功能描述

删除章节。

#### 参数定义

```python
@dataclass
class DeleteChapterInput:
    chapter_id: str              # 章节ID（必需）
    work_id: str = ""            # 作品ID
    conversation_id: str = ""    # 会话ID（用于操作日志）
```

#### 返回格式

```json
{
    "success": true,
    "chapter_id": "xxx",
    "deleted_title": "第三章 离别",
    "rollback_data": {
        "operation": "delete",
        "chapter_id": "xxx",
        "work_id": "yyy",
        "title": "第三章 离别",
        "content": "完整内容...",
        "order": 3
    }
}
```

#### 变更说明

**无变更**，保持现有实现。

---

## 7. 操作日志与回滚

### 7.1 操作日志结构

所有操作类工具都会记录操作日志到 Redis：

```python
@dataclass
class OperationLog:
    operation_id: str            # 操作ID
    conversation_id: str         # 会话ID
    tool_name: str               # 工具名称
    timestamp: datetime          # 时间戳
    params: dict                 # 调用参数
    result: dict                 # 执行结果
    rollback_data: dict          # 回滚数据
    status: str                  # 状态：pending, accepted, rejected
```

### 7.2 回滚机制

```python
async def rollback_operation(operation_id: str) -> dict:
    """
    回滚操作

    根据 rollback_data 执行逆操作：
    - create → delete
    - delete → create（恢复完整数据）
    - update_title → update_title（恢复旧标题）
    - update_content → update_content（恢复旧内容）
    """
    log = await get_operation_log(operation_id)

    if log.tool_name == "create_chapter":
        # 删除创建的章节
        await chapter_service.delete_chapter(log.rollback_data["chapter_id"])

    elif log.tool_name == "delete_chapter":
        # 恢复删除的章节
        await chapter_service.create_chapter(
            work_id=log.rollback_data["work_id"],
            title=log.rollback_data["title"],
            content=log.rollback_data["content"],
            order=log.rollback_data["order"]
        )

    elif log.tool_name == "update_chapter_title":
        # 恢复旧标题
        await chapter_service.update_title(
            chapter_id=log.rollback_data["chapter_id"],
            title=log.rollback_data["old_title"]
        )

    elif log.tool_name == "update_chapter_content":
        # 恢复旧内容
        await chapter_service.update_content(
            chapter_id=log.rollback_data["chapter_id"],
            content=log.rollback_data["old_content"]
        )

    # 更新日志状态
    await update_operation_status(operation_id, "rejected")

    return {"success": True, "operation_id": operation_id}
```

---

## 8. 与其他类工具的关系

### 8.1 Search → Update 链路

```
locate_content(query="第三段")
   ↓ 返回：{paragraph_index: 2, text: "..."}
   ↓
smart_rewrite(text_to_rewrite="...", user_requirement="更生动")
   ↓ 返回：{rewritten_text: "..."}
   ↓
apply_chapter_edit(chapter_id="xxx", new_content="...", paragraph_index=2)
```

### 8.2 Read → Update 链路

```
get_writing_context(chapter_orders="5", include=["chapter", "worldview", "rag"])
   ↓ 返回：完整上下文
   ↓
smart_continue(chapter_id="xxx", chapter_content="...", user_requirement="...")
   ↓ 返回：{content: "续写内容..."}
   ↓
update_chapter_content(chapter_id="xxx", new_content="...", operation="append")
```

### 8.3 Analyze → Update 链路

```
analyze_content(text="...", analysis_types=["text"])
   ↓ 返回：{issues: [{location: "第3段", suggestion: "..."}]}
   ↓
smart_rewrite(text_to_rewrite="第3段内容", user_requirement="修复语法问题")
   ↓ 返回：{rewritten_text: "..."}
```

---

## 9. 迁移计划

### 9.1 代码变更

Update 类工具**无需变更**，保持现有实现。

### 9.2 工具注册

确保所有工具正确注册到 `LANGGRAPH_TOOLS`：

```python
# langgraph_tools.py
LANGGRAPH_TOOLS = [
    # Search 类
    search_content,
    locate_content,

    # Read 类
    get_writing_context,

    # Analyze 类
    analyze_content,

    # Update 类 - 创作
    smart_continue,
    smart_rewrite,
    smart_insert,

    # Update 类 - 增强
    show_emotion_tool,
    enhance_scene_tool,
    learn_style_tool,

    # Update 类 - 操作
    apply_chapter_edit,
    create_chapter,
    update_chapter_title,
    update_chapter_content,
    delete_chapter,
]
```

### 9.3 工具描述更新

更新 `planning_examples.py` 中的工具描述，明确分类：

```python
TOOL_DESCRIPTIONS = """
## Search 类工具（定位内容）
- search_content: 搜索多个相关位置
- locate_content: 定位单个位置

## Read 类工具（获取内容）
- get_writing_context: 获取创作上下文（一站式）

## Analyze 类工具（分析内容）
- analyze_content: 分析内容质量（一站式）

## Update 类工具（修改内容）
### 创作类
- smart_continue: 智能续写
- smart_rewrite: 智能重写
- smart_insert: 智能插入

### 增强类
- show_emotion_tool: 展示情感
- enhance_scene_tool: 增强场景
- learn_style_tool: 学习风格

### 操作类
- apply_chapter_edit: 应用编辑
- create_chapter: 创建章节
- update_chapter_title: 更新标题
- update_chapter_content: 更新内容
- delete_chapter: 删除章节
"""
```
