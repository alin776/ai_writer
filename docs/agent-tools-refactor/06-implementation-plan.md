# 实现计划

> **实现状态**: ✅ 阶段 1-3 已完成 (2026-01-12)

## 1. 实现阶段

### 阶段 1：创建聚合工具 ✅ 已完成

| 任务 | 文件 | 优先级 | 状态 |
|------|------|--------|------|
| 创建 `get_writing_context` | `langgraph_tools.py` | P0 | ✅ 完成 |
| 创建 `analyze_content` | `analysis_tools.py` | P0 | ✅ 完成 |
| 重命名 `search_analysis_fragments_tool` → `search_content` | `langgraph_tools.py` | P1 | 待评估 |

### 阶段 2：添加向后兼容层 ✅ 已完成

| 任务 | 文件 | 优先级 | 状态 |
|------|------|--------|------|
| 添加工具名称映射 | `tool_executor.py` | P0 | ✅ 完成 |
| 添加参数转换逻辑 | `tool_executor.py` | P0 | ✅ 完成 |
| 标记旧工具为 deprecated | 各工具文件 | P1 | ✅ 完成 |

### 阶段 3：更新 Agent 配置 ✅ 已完成

| 任务 | 文件 | 优先级 | 状态 |
|------|------|--------|------|
| 更新工具描述 | `planning_examples.py` | P0 | ✅ 完成 |
| 更新 Planning Prompt | `planning_prompts.py` | P0 | ✅ 完成 |
| 更新工具描述模块 | `tool_descriptions.py` | P0 | ✅ 完成 |
| 更新决策提示词 | `decision_prompts.py` | P0 | ✅ 完成 |
| 更新 LANGGRAPH_TOOLS 列表 | `langgraph_tools.py` | P0 | ✅ 完成 |
| 添加 get_writing_context 到 LEGACY_TOOLS | `tool_executor.py` | P0 | ✅ 完成 |

### 阶段 4：测试与验证

| 任务 | 文件 | 优先级 | 状态 |
|------|------|--------|------|
| 编写单元测试 | `tests/` | P0 | 待完成 |
| 编写集成测试 | `tests/` | P1 | 待完成 |
| 回归测试 | - | P0 | 待完成 |

---

## 2. 详细实现步骤

### 2.1 创建 get_writing_context

**文件**：`backend/app/services/agent/langgraph_tools.py`

**步骤**：

1. 在文件末尾添加 `get_writing_context` 函数
2. 实现智能压缩逻辑
3. 实现章节序号解析逻辑
4. 添加到 `LANGGRAPH_TOOLS` 列表

**代码位置**：在 `get_worldview_summary` 函数之后

```python
# 在 langgraph_tools.py 中添加

@tool
async def get_writing_context(
    work_id: str,
    chapter_id: str = "",
    chapter_orders: str = "",
    user_id: str = "",
    include: str = "work,chapter,worldview,style,rag",
    rag_query: str = "",
    rag_top_k: int = 5
) -> str:
    """
    获取创作上下文（一站式）

    合并了 get_context_tool, read_chapter_tool, get_worldview_summary, get_style_guidance_tool

    Args:
        work_id: 作品ID
        chapter_id: 章节ID（单章节）
        chapter_orders: 章节序号（支持批量："1" / "1,2,3" / "1-5"）
        user_id: 用户ID（用于获取风格指导）
        include: 包含的内容类型，逗号分隔（work,chapter,worldview,style,rag）
        rag_query: RAG 检索查询
        rag_top_k: RAG 返回数量

    Returns:
        JSON 格式的创作上下文
    """
    # 实现代码见 03-read-tools.md
    pass
```

### 2.2 创建 analyze_content

**文件**：`backend/app/services/agent/tools/analysis_tools.py`

**步骤**：

1. 在文件末尾添加 `analyze_content` 函数
2. 复用现有的分析逻辑
3. 添加参数控制分析类型
4. 注册到工具列表

**代码位置**：在 `evaluate_quality_tool` 函数之后

```python
# 在 analysis_tools.py 中添加

@tool
async def analyze_content(
    text: str,
    work_id: str = "",
    chapter_id: str = "",
    analysis_types: str = "text,style",
    focus: str = "all",
    depth: str = "normal"
) -> str:
    """
    分析内容质量（一站式）

    合并了 analyze_text_tool, analyze_style_tool, check_story_consistency_tool, evaluate_quality_tool

    Args:
        text: 待分析文本
        work_id: 作品ID（用于一致性检查）
        chapter_id: 章节ID（用于上下文）
        analysis_types: 分析类型，逗号分隔（text,style,consistency,quality）
        focus: 分析重点
        depth: 分析深度

    Returns:
        JSON 格式的分析报告
    """
    # 实现代码见 04-analyze-tools.md
    pass
```

### 2.3 重命名 search_content

**文件**：`backend/app/services/agent/langgraph_tools.py`

**步骤**：

1. 将 `search_analysis_fragments_tool` 重命名为 `search_content`
2. 修改返回格式，只返回 snippet
3. 保留原函数作为别名（向后兼容）

```python
# 重命名
@tool
async def search_content(
    work_id: str,
    query: str,
    top_k: int = 10,
    chapter_id: str = "",
    look_ahead: int = 0
) -> str:
    """搜索多个相关位置"""
    # 实现代码见 02-search-tools.md
    pass

# 向后兼容别名
search_analysis_fragments_tool = search_content
```

### 2.4 添加工具名称映射

**文件**：`backend/app/services/agent/execution/tool_executor.py`

**步骤**：

1. 扩展 `TOOL_NAME_MAPPING` 字典
2. 添加参数转换函数

```python
# 在 tool_executor.py 中扩展

TOOL_NAME_MAPPING = {
    # 现有映射...

    # Search 类
    "search_analysis_fragments_tool": "search_content",
    "search_analysis_fragments": "search_content",

    # Read 类
    "get_context_tool": "get_writing_context",
    "get_context": "get_writing_context",
    "read_chapter_tool": "get_writing_context",
    "read_chapter": "get_writing_context",
    "get_chapter_by_order_tool": "get_writing_context",
    "get_chapter_by_order": "get_writing_context",
    "get_worldview_summary": "get_writing_context",
    "get_style_guidance_tool": "get_writing_context",
    "get_style_guidance": "get_writing_context",

    # Analyze 类
    "analyze_text_tool": "analyze_content",
    "analyze_text": "analyze_content",
    "analyze_style_tool": "analyze_content",
    "analyze_style": "analyze_content",
    "check_story_consistency_tool": "analyze_content",
    "check_story_consistency": "analyze_content",
    "evaluate_quality_tool": "analyze_content",
    "evaluate_quality": "analyze_content",
}
```

### 2.5 添加参数转换逻辑

**文件**：`backend/app/services/agent/execution/tool_executor.py`

**步骤**：

1. 创建参数转换函数
2. 在 `prepare_params` 中调用

```python
# 在 tool_executor.py 中添加

def _convert_legacy_params(original_tool: str, target_tool: str, params: dict) -> dict:
    """将旧工具参数转换为新工具参数"""

    # Read 类工具转换
    if target_tool == "get_writing_context":
        if original_tool in ["read_chapter_tool", "read_chapter"]:
            return {
                "work_id": params.get("work_id", ""),
                "chapter_id": params.get("chapter_id", ""),
                "include": "chapter"
            }
        if original_tool in ["get_chapter_by_order_tool", "get_chapter_by_order"]:
            return {
                "work_id": params.get("work_id", ""),
                "chapter_orders": params.get("chapter_order", ""),
                "include": "chapter"
            }
        if original_tool == "get_worldview_summary":
            return {
                "work_id": params.get("work_id", ""),
                "include": "worldview"
            }
        if original_tool in ["get_style_guidance_tool", "get_style_guidance"]:
            return {
                "work_id": params.get("work_id", ""),
                "user_id": params.get("user_id", ""),
                "include": "style"
            }

    # Analyze 类工具转换
    if target_tool == "analyze_content":
        if original_tool in ["analyze_text_tool", "analyze_text"]:
            return {
                "text": params.get("text", ""),
                "analysis_types": "text",
                "focus": params.get("focus", "all")
            }
        if original_tool in ["analyze_style_tool", "analyze_style"]:
            return {
                "text": params.get("text", ""),
                "analysis_types": "style"
            }
        if original_tool in ["check_story_consistency_tool", "check_story_consistency"]:
            return {
                "text": params.get("text", ""),
                "work_id": params.get("work_id", ""),
                "analysis_types": "consistency"
            }
        if original_tool in ["evaluate_quality_tool", "evaluate_quality"]:
            return {
                "text": params.get("text", ""),
                "analysis_types": "quality",
                "depth": params.get("depth", "normal")
            }

    return params
```

### 2.6 更新工具描述

**文件**：`backend/app/services/agent/prompts/planning_examples.py`

**步骤**：

1. 更新 `TOOL_DESCRIPTIONS` 常量
2. 按四大类组织工具描述

```python
TOOL_DESCRIPTIONS = """
## 可用工具

### Search 类（定位内容）
- **search_content**: 搜索多个相关位置，返回位置+片段
  - 参数：work_id, query, top_k, chapter_id, look_ahead
  - 场景：找一下关于XX的内容

- **locate_content**: 定位单个位置，返回位置+片段
  - 参数：chapter_id, query, chapter_content
  - 场景：把第三段改了

### Read 类（获取内容）
- **get_writing_context**: 获取创作上下文（一站式）
  - 参数：work_id, chapter_id, chapter_orders, user_id, include, rag_query, rag_top_k
  - include 可选值：work, chapter, worldview, style, rag
  - 场景：续写前获取上下文、批量阅读多章

### Analyze 类（分析内容）
- **analyze_content**: 分析内容质量（一站式）
  - 参数：text, work_id, chapter_id, analysis_types, focus, depth
  - analysis_types 可选值：text, style, consistency, quality
  - 场景：检查文本问题、分析写作风格

### Update 类（修改内容）

#### 创作类
- **smart_continue**: 智能续写
- **smart_rewrite**: 智能重写
- **smart_insert**: 智能插入

#### 增强类
- **show_emotion_tool**: 展示情感
- **enhance_scene_tool**: 增强场景
- **learn_style_tool**: 学习风格

#### 操作类
- **apply_chapter_edit**: 应用编辑
- **create_chapter**: 创建章节
- **update_chapter_title**: 更新标题
- **update_chapter_content**: 更新内容
- **delete_chapter**: 删除章节
"""
```

### 2.7 更新 LANGGRAPH_TOOLS 列表

**文件**：`backend/app/services/agent/langgraph_tools.py`

**步骤**：

1. 移除已合并的旧工具
2. 添加新的聚合工具
3. 按四大类组织

```python
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

---

## 3. 向后兼容策略

### 3.1 工具名称兼容

通过 `TOOL_NAME_MAPPING` 实现旧工具名到新工具名的映射。

### 3.2 参数兼容

通过 `_convert_legacy_params` 函数实现旧参数到新参数的转换。

### 3.3 返回格式兼容

新工具的返回格式是旧工具返回格式的超集，不会破坏现有逻辑。

### 3.4 渐进式迁移

1. **第一阶段**：添加新工具，保留旧工具（标记 deprecated）
2. **第二阶段**：更新 Planning Prompt，引导使用新工具
3. **第三阶段**：监控旧工具使用情况
4. **第四阶段**：移除旧工具（确认无使用后）

---

## 4. 测试计划

### 4.1 单元测试

| 测试项 | 测试内容 |
|--------|---------|
| `test_search_content` | 搜索功能、返回格式 |
| `test_get_writing_context` | 各种 include 组合、智能压缩、章节序号解析 |
| `test_analyze_content` | 各种 analysis_types 组合、重试机制 |
| `test_tool_name_mapping` | 旧工具名映射 |
| `test_param_conversion` | 参数转换逻辑 |

### 4.2 集成测试

| 测试项 | 测试内容 |
|--------|---------|
| `test_search_read_chain` | Search → Read 链路 |
| `test_read_update_chain` | Read → Update 链路 |
| `test_analyze_update_chain` | Analyze → Update 链路 |
| `test_legacy_tool_call` | 旧工具名调用 |

### 4.3 回归测试

| 测试项 | 测试内容 |
|--------|---------|
| 续写场景 | 确保续写功能正常 |
| 改写场景 | 确保改写功能正常 |
| 分析场景 | 确保分析功能正常 |
| 搜索场景 | 确保搜索功能正常 |

---

## 5. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 旧工具调用失败 | 现有功能不可用 | 完善向后兼容层 |
| 参数转换错误 | 功能异常 | 充分测试参数转换 |
| 返回格式变化 | 前端解析失败 | 保持返回格式兼容 |
| Planning 生成错误工具 | 任务执行失败 | 更新 Planning Prompt |

---

## 6. 文件变更清单

| 文件 | 变更类型 | 变更内容 |
|------|---------|---------|
| `langgraph_tools.py` | 修改 | 添加 get_writing_context, 重命名 search_content |
| `analysis_tools.py` | 修改 | 添加 analyze_content |
| `tool_executor.py` | 修改 | 添加工具映射和参数转换 |
| `planning_examples.py` | 修改 | 更新工具描述 |
| `agent_executor.py` | 修改 | 更新二次工具调用逻辑（可选） |
| `tests/test_tools.py` | 新增 | 单元测试 |
| `tests/test_integration.py` | 新增 | 集成测试 |

---

## 7. 检查清单

### 实现前检查

- [x] 确认现有工具的完整列表
- [x] 确认现有工具的调用频率
- [x] 确认 Planning Prompt 的当前内容
- [x] 确认 tool_executor.py 的当前映射

### 实现中检查

- [x] get_writing_context 实现完成 ✅ (2026-01-12)
- [x] analyze_content 实现完成 ✅ (2026-01-12)
- [ ] search_content 重命名完成（待评估）
- [x] 工具映射添加完成 ✅ (2026-01-12)
- [x] 参数转换添加完成 ✅ (2026-01-12)
- [x] Planning Prompt 更新完成 ✅ (2026-01-12)
- [x] LANGGRAPH_TOOLS 更新完成 ✅ (2026-01-12)
- [x] get_writing_context 添加到 LEGACY_TOOLS ✅ (2026-01-12)

### 实现后检查

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 回归测试通过
- [x] 旧工具调用兼容 ✅ (2026-01-12)
- [ ] 前端功能正常
