# replace_all 操作实现方案

## 背景

ContentOperator 需要支持"整章重写"场景，即 `operation="content"` 映射到底层的 `replace_all` 操作。

## 设计决策

### 为什么选择 `apply_chapter_edit` 而非 `update_chapter_content`？

| 特性 | apply_chapter_edit | update_chapter_content |
|------|---------------------|-------------------------|
| **HITL 确认** | ✅ 有 (`requires_confirmation: true`) | ❌ 无（直接执行） |
| **修订记录** | ✅ `ChapterRevisionService.create_revision()` | ❌ 只有操作日志 |
| **前端交互** | 用户确认后才写入 | 立即写入数据库 |
| **设计用途** | AI 生成内容 → 用户确认 | 用户自己操作（复制粘贴） |

**结论**：整章替换是高风险操作，必须用户确认后执行，所以选择在 `apply_chapter_edit` 中新增 `replace_all`。

---

## replace_all 语义定义

| 属性 | 说明 |
|------|------|
| **含义** | 用新内容**完全替换**整个章节的**全部内容** |
| **定位** | 无需定位（paragraph_index/node_id/original_text 均忽略） |
| **HITL** | 需要用户确认后才执行 |
| **用途** | 整章重写、全文润色、风格转换等场景 |

### 操作类型对比

| operation | 说明 | 需要定位 | 用途 |
|-----------|------|---------|------|
| append | 追加到末尾 | ✗ | 续写 |
| replace | 替换指定段落 | ✓ | 改写部分内容 |
| insert | 在指定位置插入 | ✓ | 插入新内容 |
| **replace_all** | 整体替换全部内容 | ✗ | 整章重写 |

---

## 需要修改的文件

### 1. editor_tools.py（第360行）

**文件路径**：`backend/app/services/agent/tools/editor_tools.py`

#### 修改1：验证列表添加 `replace_all`

```python
# 第360行
# 修改前
if operation not in ["append", "replace", "insert"]:
    return json.dumps({"success": False, "error": "invalid_operation"}, ensure_ascii=False)

# 修改后
if operation not in ["append", "replace", "insert", "replace_all"]:
    return json.dumps({"success": False, "error": "invalid_operation"}, ensure_ascii=False)
```

#### 修改2：添加 replace_all 处理分支（约第520行，在 replace 分支后）

```python
# 在 replace 处理分支后，insert 处理分支前添加

elif operation == "replace_all":
    # replace_all：整体替换章节全部内容
    # 不需要任何定位信息，直接用 content 替换
    new_content = actual_content
    logger.info(f"[apply_chapter_edit] replace_all: 整章替换，新内容长度={len(actual_content)}")
```

#### 完整上下文示例

```python
# ... 现有的 replace 处理分支 ...

elif operation == "replace":
    replaced = None
    # ... 现有替换逻辑 ...
    new_content = replaced

elif operation == "replace_all":
    # replace_all：整体替换章节全部内容
    # 不需要任何定位信息，直接用 content 替换
    new_content = actual_content
    logger.info(f"[apply_chapter_edit] replace_all: 整章替换，新内容长度={len(actual_content)}")

elif operation == "insert":
    # ... 现有插入逻辑 ...
```

---

### 2. chapter_revision_service.py（第135行 `_build_new_content` 方法）

**文件路径**：`backend/app/services/chapter_revision_service.py`

#### 修改：在 `_build_new_content` 方法中添加 replace_all 分支

在第187行 `if operation == "append":` 之前添加：

```python
# 第187行之前添加
if operation == "replace_all":
    # replace_all：直接用新内容替换全部内容
    # 不需要任何定位逻辑
    return (actual_content, "")

if operation == "append":
    return (old_content + actual_content, "")
```

#### 完整上下文示例

```python
def _build_new_content(
    self,
    old_content: str,
    revision: ChapterRevision,
) -> Tuple[Optional[str], str]:
    actual_content = revision.new_text or ""
    if not actual_content.strip():
        return (None, "empty_content")

    operation = revision.operation
    # ... 其他变量定义 ...

    # 辅助函数定义
    def _replace_by_node_id(...): ...
    def _insert_after_node_id(...): ...
    def _get_paragraph_text(...): ...

    # ⚠️ 新增：replace_all 分支（最简单，直接替换）
    if operation == "replace_all":
        return (actual_content, "")

    if operation == "append":
        return (old_content + actual_content, "")

    if operation == "insert":
        # ... 现有插入逻辑 ...

    if operation == "replace":
        # ... 现有替换逻辑 ...
```

---

## 数据库兼容性

### ChapterRevision 模型

**文件路径**：`backend/app/models/chapter_revision.py`

```python
class ChapterRevision(Base):
    # ...
    operation = Column(String(20))  # ✅ 长度足够存储 "replace_all"
```

✅ **无需修改**：`operation` 字段为 `String(20)`，足够存储 `"replace_all"`（11字符）。

---

## 测试用例

### 单元测试

**文件路径**：`backend/tests/unit/agent/tools/test_editor_tools.py`

```python
import pytest
import json
from unittest.mock import patch, AsyncMock

class TestApplyChapterEditReplaceAll:
    """测试 apply_chapter_edit 的 replace_all 操作"""

    @pytest.fixture
    def mock_chapter(self):
        """模拟章节数据"""
        return {
            "id": "test-chapter-id",
            "work_id": "test-work-id",
            "title": "测试章节",
            "content": "<p>原始内容第一段</p><p>原始内容第二段</p><p>原始内容第三段</p>",
            "version": 1
        }

    async def test_replace_all_basic(self, mock_chapter):
        """测试 replace_all 基本功能"""
        from app.services.agent.tools.editor_tools import apply_chapter_edit

        with patch('app.services.agent.tools.editor_tools.AsyncSessionLocal') as mock_session:
            # 设置 mock
            mock_db = AsyncMock()
            mock_session.return_value.__aenter__.return_value = mock_db
            # ... 其他 mock 设置 ...

            result = await apply_chapter_edit.ainvoke({
                "chapter_id": "test-chapter-id",
                "content": "<p>全新的章节内容</p>",
                "operation": "replace_all"
            })

            data = json.loads(result)
            assert data["success"] == True
            assert data["requires_confirmation"] == True
            assert data["operation"] == "replace_all"

    async def test_replace_all_ignores_position_params(self, mock_chapter):
        """测试 replace_all 忽略定位参数"""
        from app.services.agent.tools.editor_tools import apply_chapter_edit

        # 即使传入 paragraph_index、node_id，也应该忽略
        result = await apply_chapter_edit.ainvoke({
            "chapter_id": "test-chapter-id",
            "content": "<p>全新的章节内容</p>",
            "operation": "replace_all",
            "paragraph_index": 1,  # 应该被忽略
            "node_id": "some-node",  # 应该被忽略
            "original_text": "一些原文"  # 应该被忽略
        })

        data = json.loads(result)
        assert data["success"] == True
        # 新内容应该完全替换，不受定位参数影响

    async def test_replace_all_empty_content_rejected(self):
        """测试 replace_all 空内容被拒绝"""
        from app.services.agent.tools.editor_tools import apply_chapter_edit

        result = await apply_chapter_edit.ainvoke({
            "chapter_id": "test-chapter-id",
            "content": "",
            "operation": "replace_all"
        })

        data = json.loads(result)
        assert data["success"] == False
        assert data["error"] == "empty_content"
```

### 集成测试

**文件路径**：`backend/tests/integration/agent/test_replace_all.py`

```python
import pytest
import json

class TestReplaceAllIntegration:
    """replace_all 集成测试"""

    @pytest.fixture
    async def test_chapter(self, db_session):
        """创建测试章节"""
        from app.services.chapter_service import ChapterService
        svc = ChapterService(db_session)
        chapter = await svc.create_chapter(
            work_id="test-work",
            title="测试章节",
            content="<p>原始内容第一段</p><p>原始内容第二段</p>"
        )
        return chapter

    async def test_replace_all_creates_revision(self, test_chapter):
        """测试 replace_all 创建修订记录"""
        from app.services.agent.tools.editor_tools import apply_chapter_edit

        result = await apply_chapter_edit.ainvoke({
            "chapter_id": str(test_chapter.id),
            "content": "<p>全新的章节内容</p>",
            "operation": "replace_all"
        })

        data = json.loads(result)
        assert data["success"] == True
        assert data["requires_confirmation"] == True
        assert data["revision_id"] is not None
        assert data["request_id"] is not None

    async def test_replace_all_apply_revision(self, test_chapter, db_session):
        """测试 replace_all 修订应用后内容正确"""
        from app.services.agent.tools.editor_tools import apply_chapter_edit
        from app.services.chapter_revision_service import ChapterRevisionService
        from app.services.chapter_service import ChapterService

        # 1. 创建修订
        result = await apply_chapter_edit.ainvoke({
            "chapter_id": str(test_chapter.id),
            "content": "<p>全新的章节内容</p>",
            "operation": "replace_all"
        })
        data = json.loads(result)

        # 2. 应用修订（模拟用户确认）
        revision_svc = ChapterRevisionService(db_session)
        await revision_svc.apply_revision(data["revision_id"])

        # 3. 验证内容已更新
        chapter_svc = ChapterService(db_session)
        updated = await chapter_svc.get_chapter_by_id(str(test_chapter.id))
        assert updated.content == "<p>全新的章节内容</p>"
```

---

## 前端适配

### 无需额外修改

`replace_all` 操作复用现有的 HITL 确认流程：

1. **后端返回** `requires_confirmation: true`
2. **前端展示** 修订确认对话框
3. **用户确认** 后调用 `/api/revisions/{id}/apply`

### 可选优化：差异对比显示

对于 `replace_all` 操作，前端可以优化显示方式：

```typescript
// useAgentChat.ts 或相关组件中
if (approval.operation === 'replace_all') {
    // 显示"整章替换"提示
    // 可以考虑全文对比显示，而非段落级对比
}
```

---

## 流程图

```
用户: "帮我重写整个第五章"
        │
        ▼
┌─────────────────────────────┐
│  Planning                    │
│  Task 1: smart_rewrite       │
│  Task 2: operate_apply       │
│           (operation=content)│
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  ContentOperator             │
│  route: content → replace_all│
│  无需定位                     │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  apply_chapter_edit          │
│  operation="replace_all"     │
│  new_content = content       │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  ChapterRevisionService      │
│  create_revision()           │
│  requires_confirmation=true  │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  前端 HITL 确认              │
│  用户确认/拒绝               │
└─────────────────────────────┘
        │
        ▼ (确认)
┌─────────────────────────────┐
│  _build_new_content()        │
│  return (actual_content, "") │
│  直接全量替换                 │
└─────────────────────────────┘
        │
        ▼
┌─────────────────────────────┐
│  章节内容更新完成             │
└─────────────────────────────┘
```

---

## 实现检查清单

- [ ] `editor_tools.py:360` - operation 验证列表添加 `"replace_all"`
- [ ] `editor_tools.py:520+` - 添加 replace_all 处理分支
- [ ] `chapter_revision_service.py:187-` - `_build_new_content` 添加 replace_all 分支
- [ ] 添加单元测试
- [ ] 添加集成测试
- [ ] 验证 HITL 流程正常工作

---

## 修订记录

| 日期 | 修订内容 |
|------|----------|
| 2026-01-22 | 初始版本 |
