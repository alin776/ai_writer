# ContentOperator Planning 集成

## 需要修改的文件

```
backend/app/services/agent/prompts/
├── planning_prompts.py      # 工具描述
├── planning_examples.py     # 使用示例
└── tool_descriptions.py     # 工具说明（如有）

backend/app/services/agent/core/
└── tool_dispatcher.py       # 工具分类
```

## 1. planning_prompts.py 修改

### 添加 operate_apply 工具描述

```python
# 在工具描述部分添加

OPERATE_APPLY_DESCRIPTION = """
### operate_apply - 智能应用修改（推荐）

【作用】将 Create 工具生成的内容应用到章节，自动处理定位

【参数】
- chapter_id: 章节ID（必填）
- content: 要写入的内容（必填，来自 smart_* 工具）
- operation: 操作类型（append/replace/insert，默认 append）
- target_description: 目标位置描述（insert 时使用）
- original_text: 原文（replace 时使用，用于定位）

【使用场景】
- 续写后应用：operation=append
- 改写后应用：operation=replace, original_text=原文
- 插入内容：operation=insert, target_description="第3段后"

【与 apply_chapter_edit 的区别】
- operate_apply：自动定位，推荐使用
- apply_chapter_edit：需手动传入 paragraph_index/node_id
"""
```

### 更新工具优先级说明

```python
# 在工具选择指南中添加

TOOL_PRIORITY_GUIDE = """
【OPERATION 工具选择】

✅ 推荐：operate_apply
- 自动定位目标位置
- 简化任务规划
- 减少 $ref 依赖

⚠️ 仅在特殊情况使用：apply_chapter_edit
- 已有精确的 paragraph_index
- 需要特殊的锚点定位
"""
```

## 2. planning_examples.py 修改

### 新版续写示例

```python
# 改造前（3任务）
OLD_CONTINUE_EXAMPLE = """
{
  "tasks": [
    {"task_id": 1, "tool": "explore_content", ...},
    {"task_id": 2, "tool": "smart_continue", ...},
    {"task_id": 3, "tool": "apply_chapter_edit", "params": {
      "operation": "append",
      "content": {"$ref": {"task_id": 2, "path": "content"}}
    }}
  ]
}
"""

# 改造后（2任务，更简洁）
NEW_CONTINUE_EXAMPLE = """
{
  "user_intent": "续写第5章",
  "tasks": [
    {
      "task_id": 1,
      "description": "获取上下文并续写",
      "tool": "smart_continue",
      "params": {
        "chapter_id": "$CHAPTER_ID$",
        "user_requirement": "续写500字",
        "word_count": 500
      }
    },
    {
      "task_id": 2,
      "description": "应用续写内容",
      "tool": "operate_apply",
      "params": {
        "chapter_id": "$CHAPTER_ID$",
        "operation": "append",
        "content": {"$ref": {"task_id": 1, "path": "content"}}
      },
      "depends_on": [1]
    }
  ]
}
"""
```

### 新版改写示例

```python
# 改造前（4任务）
OLD_REWRITE_EXAMPLE = """
{
  "tasks": [
    {"task_id": 1, "tool": "locate_content", "params": {"query": "第3段"}},
    {"task_id": 2, "tool": "smart_rewrite", "params": {
      "text_to_rewrite": {"$ref": {"task_id": 1, "path": "text"}}
    }},
    {"task_id": 3, "tool": "apply_chapter_edit", "params": {
      "operation": "replace",
      "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
      "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}},
      "node_id": {"$ref": {"task_id": 1, "path": "node_id"}}
    }}
  ]
}
"""

# 改造后（2任务）
NEW_REWRITE_EXAMPLE = """
{
  "user_intent": "优化第3段描写",
  "tasks": [
    {
      "task_id": 1,
      "description": "改写第3段",
      "tool": "smart_rewrite",
      "params": {
        "chapter_id": "$CHAPTER_ID$",
        "text_to_rewrite": "第3段原文内容...",
        "user_requirement": "增强画面感"
      }
    },
    {
      "task_id": 2,
      "description": "应用改写",
      "tool": "operate_apply",
      "params": {
        "chapter_id": "$CHAPTER_ID$",
        "operation": "replace",
        "content": {"$ref": {"task_id": 1, "path": "versions[0].content"}},
        "original_text": {"$ref": {"task_id": 1, "path": "original_text"}}
      },
      "depends_on": [1]
    }
  ]
}
"""
```

### 新版插入示例

```python
NEW_INSERT_EXAMPLE = """
{
  "user_intent": "在主角出场后添加心理描写",
  "tasks": [
    {
      "task_id": 1,
      "description": "生成心理描写",
      "tool": "smart_insert",
      "params": {
        "chapter_id": "$CHAPTER_ID$",
        "user_intent": "添加主角的内心独白",
        "word_count": 200
      }
    },
    {
      "task_id": 2,
      "description": "插入到指定位置",
      "tool": "operate_apply",
      "params": {
        "chapter_id": "$CHAPTER_ID$",
        "operation": "insert",
        "content": {"$ref": {"task_id": 1, "path": "content"}},
        "target_description": "主角出场的段落之后"
      },
      "depends_on": [1]
    }
  ]
}
"""
```

## 3. 示例对比总结

| 场景 | 改造前任务数 | 改造后任务数 | 简化程度 |
|------|-------------|-------------|----------|
| 续写 | 3 | 2 | 33% |
| 改写 | 4 | 2 | 50% |
| 插入 | 4 | 2 | 50% |

## 4. $ref 引用变化

### 改造前（复杂）
```json
{
  "content": {"$ref": {"task_id": 2, "path": "versions[0].content"}},
  "paragraph_index": {"$ref": {"task_id": 1, "path": "paragraph_index"}},
  "node_id": {"$ref": {"task_id": 1, "path": "node_id"}},
  "before_anchor": {"$ref": {"task_id": 1, "path": "before_anchor"}},
  "after_anchor": {"$ref": {"task_id": 1, "path": "after_anchor"}}
}
```

### 改造后（简洁）
```json
{
  "content": {"$ref": {"task_id": 1, "path": "versions[0].content"}},
  "original_text": {"$ref": {"task_id": 1, "path": "original_text"}}
}
```

## 5. 兼容性处理

```python
# 在 planning_prompts.py 中保留两种模式

COMPATIBLE_MODE_NOTE = """
【工具选择兼容性】

新模式（推荐）：
- smart_* → operate_apply
- 自动定位，无需 locate_content

旧模式（仍支持）：
- locate_content → smart_* → apply_chapter_edit
- 需要手动传递定位参数

⚠️ 新开发请使用新模式
"""
```
