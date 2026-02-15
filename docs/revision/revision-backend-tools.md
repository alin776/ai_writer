# 修订编辑器章节 - 后端工具实现

## 1. 现有工具分析

### 1.1 已有的编辑工具

位置: `backend/app/services/agent/tools/editor_tools.py`

| 工具 | 功能 | HITL | 返回格式 |
|------|------|------|----------|
| `apply_chapter_edit` | 章节编辑 | ✅ | `requires_confirmation: true` |
| `smart_continue` | 智能续写 | ✅ | 调用 apply_chapter_edit |
| `smart_rewrite` | 智能改写 | ✅ | `versions: [3个版本]` |
| `smart_insert` | 智能插入 | ✅ | `position_inference` |

### 1.2 工具返回格式

```python
# apply_chapter_edit 返回
{
    "success": True,
    "requires_confirmation": True,
    "action_type": "edit",
    "chapter_id": "xxx",
    "operation": "append",  # append | replace | insert
    "content": "续写内容...",
    "content_length": 1234,
    "description": "AI续写：+1234字"
}

# smart_rewrite 返回
{
    "success": True,
    "requires_confirmation": True,
    "action_type": "rewrite",
    "chapter_id": "xxx",
    "original_text": "原文...",
    "versions": [
        {"style_name": "版本A", "reason": "更有画面感", "content": "..."},
        {"style_name": "版本B", "reason": "更简洁有力", "content": "..."},
        {"style_name": "版本C", "reason": "更有情感", "content": "..."}
    ]
}
```

---

## 2. 新增工具设计

### 2.1 create_chapter - 新建章节

```python
# 文件: backend/app/services/agent/tools/chapter_tools.py

@tool
@register_as_tool(
    "create_chapter",
    "chapter",
    "创建新章节并写入内容。此操作需要用户确认。"
)
async def create_chapter(
    work_id: str,
    title: str,
    content: str = "",
    order: int = None,
    user_id: str = None
) -> str:
    """
    创建新章节

    Args:
        work_id: 作品ID
        title: 章节标题 (如 "第六章：新的征程")
        content: 章节内容 (可选)
        order: 章节顺序 (可选，默认追加到末尾)
        user_id: 用户ID

    Returns:
        包含确认请求的结果
    """
    try:
        # 检查速率限制
        if user_id:
            is_allowed, remaining = await agent_edit_limiter.check(user_id)
            if not is_allowed:
                return json.dumps({
                    "success": False,
                    "error": "rate_limit_exceeded"
                }, ensure_ascii=False)

        # 验证参数
        if not work_id:
            return json.dumps({"success": False, "error": "missing_work_id"})
        if not title:
            return json.dumps({"success": False, "error": "missing_title"})

        # 返回需要用户确认的信息
        return json.dumps({
            "success": True,
            "requires_confirmation": True,
            "action_type": "create",
            "work_id": work_id,
            "title": title,
            "content": content,
            "content_length": len(content) if content else 0,
            "order": order,
            "description": f"新建章节：{title}"
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
```

### 2.2 update_chapter_title - 修改标题

```python
@tool
@register_as_tool(
    "update_chapter_title",
    "chapter",
    "修改章节标题。此操作需要用户确认。"
)
async def update_chapter_title(
    chapter_id: str,
    new_title: str,
    user_id: str = None
) -> str:
    """
    修改章节标题

    Args:
        chapter_id: 章节ID
        new_title: 新标题
        user_id: 用户ID

    Returns:
        包含确认请求的结果
    """
    try:
        # 获取原标题
        async with AsyncSessionLocal() as db:
            chapter_svc = ChapterService(db)
            chapter = await chapter_svc.get_chapter_by_id(chapter_id)
            if not chapter:
                return json.dumps({
                    "success": False,
                    "error": "chapter_not_found"
                })
            old_title = chapter.title

        return json.dumps({
            "success": True,
            "requires_confirmation": True,
            "action_type": "rename",
            "chapter_id": chapter_id,
            "old_title": old_title,
            "new_title": new_title,
            "description": f"修改标题：{old_title} → {new_title}"
        }, ensure_ascii=False)

    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})
```

---

## 3. HITL 确认处理

### 3.1 StreamEventHandler 修改

位置: `backend/app/services/agent/stream/stream_event_handler.py`

```python
async def _handle_hitl_confirmation(self, node_data: dict):
    """处理 HITL 确认请求"""
    # ... 现有代码 ...

    # 检查是否需要用户确认
    if not tool_result.get("requires_confirmation"):
        continue

    # 构建审批数据
    action_type = tool_result.get("action_type", "edit")

    approval_data = {
        "request_id": f"{msg.name}_{msg.tool_call_id}",
        "action_type": action_type,
        # 通用字段
        "chapter_id": tool_result.get("chapter_id"),
        "description": tool_result.get("description"),
        # 内容编辑字段
        "operation": tool_result.get("operation"),
        "original_content": tool_result.get("original_text"),
        "new_content": tool_result.get("content"),
        "versions": tool_result.get("versions"),
        # 新建章节字段
        "work_id": tool_result.get("work_id"),
        "title": tool_result.get("title"),
        "order": tool_result.get("order"),
        # 修改标题字段
        "old_title": tool_result.get("old_title"),
        "new_title": tool_result.get("new_title"),
    }

    await self._approval_callback(approval_data)
```

### 3.2 发送修订事件

```python
# 在 flow_events.py 中新增

def emit_revision_event(
    self,
    revision_type: str,  # append | replace | insert | create | rename
    chapter_id: str = None,
    chapter_title: str = None,
    content_preview: str = None,
    old_title: str = None,
    new_title: str = None,
    versions: list = None,
    status: str = "pending"  # pending | accepted | discarded
):
    """发送修订事件到执行轨迹"""
    if not self._on_flow_event:
        return

    self._on_flow_event({
        "type": "revision",
        "data": {
            "revision_type": revision_type,
            "chapter_id": chapter_id,
            "chapter_title": chapter_title,
            "content_preview": content_preview[:100] if content_preview else None,
            "old_title": old_title,
            "new_title": new_title,
            "versions": versions,
            "status": status
        }
    })
```

---

## 4. 确认后执行

### 4.1 新建章节执行

```python
# 在 hitl.py 或新文件中

async def execute_create_chapter(approval_data: dict, db: AsyncSession):
    """执行新建章节"""
    chapter_svc = ChapterService(db)

    new_chapter = await chapter_svc.create_chapter(
        work_id=approval_data["work_id"],
        title=approval_data["title"],
        content=approval_data.get("content", ""),
        order=approval_data.get("order")
    )

    return {"chapter_id": str(new_chapter.id), "title": new_chapter.title}
```

### 4.2 修改标题执行

```python
async def execute_update_title(approval_data: dict, db: AsyncSession):
    """执行修改标题"""
    chapter_svc = ChapterService(db)

    await chapter_svc.update_chapter(
        chapter_id=approval_data["chapter_id"],
        title=approval_data["new_title"]
    )

    return {"success": True}
```

---

## 5. 工具注册

```python
# 在 __init__.py 中注册

from .chapter_tools import (
    create_chapter,
    update_chapter_title,
    create_chapter_tool,
    update_chapter_title_tool
)

def register_all_tools(registry: ToolRegistry):
    # ... 现有注册 ...

    # 章节管理工具
    registry.register_standard_tool(create_chapter_tool)
    registry.register_standard_tool(update_chapter_title_tool)
```

---

## 6. 测试用例

```python
# tests/test_chapter_tools.py

async def test_create_chapter():
    result = await create_chapter(
        work_id="test-work-id",
        title="第六章：新的征程",
        content="晨曦初露，林逸踏上了新的旅程..."
    )
    data = json.loads(result)
    assert data["success"] == True
    assert data["requires_confirmation"] == True
    assert data["action_type"] == "create"

async def test_update_chapter_title():
    result = await update_chapter_title(
        chapter_id="test-chapter-id",
        new_title="命运的转折"
    )
    data = json.loads(result)
    assert data["success"] == True
    assert data["action_type"] == "rename"
```
