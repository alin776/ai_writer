# Analyze 类工具设计

## 1. 概述

Analyze 类工具负责**评估和分析内容**，使用 LLM 进行语义推理，返回结构化的分析报告。

**设计理念**：对内容进行评价和判断，而不是获取内容本身。

**与 Read 的区别**：
| 维度 | Read | Analyze |
|------|------|---------|
| 目的 | 获取原始数据 | 评估/判断数据 |
| 处理方式 | 规则/向量预处理 | LLM 语义推理 |
| 返回内容 | 内容本身 | 对内容的评价 |
| 示例 | "给我看第三章" | "第三章写得怎么样？" |

## 2. 工具列表

| 工具 | 功能 | 场景 |
|------|------|------|
| `analyze_content` | 分析内容质量（一站式） | 评估文本质量、风格、一致性 |

## 3. analyze_content

### 3.1 功能描述

一站式分析内容质量，合并 3 个原子工具：
- `analyze_text_tool`
- `analyze_style_tool`（实际是 `analyze_content_tool` 的 style 维度）
- `check_story_consistency_tool`

### 3.2 变更说明

| 项目 | 变更前 | 变更后 |
|------|--------|--------|
| 工具数量 | 3 个独立工具 | 1 个聚合工具 |
| 调用次数 | 3 次 | 1 次 |
| 参数控制 | 无 | `analysis_types` 参数控制分析类型 |

### 3.3 参数定义

```python
@dataclass
class AnalyzeContentInput:
    text: str                       # 待分析文本（必需）
    work_id: str = ""               # 作品ID（用于一致性检查）
    chapter_id: str = ""            # 章节ID（用于上下文）
    analysis_types: List[str] = None  # 分析类型
                                    # 可选值：text, style, consistency, quality
                                    # 默认：["text", "style"]
    focus: str = "all"              # 分析重点（可选）
                                    # 可选值：grammar, logic, style, structure, character, plot, all
    depth: str = "normal"           # 分析深度
                                    # 可选值：shallow, normal, deep
```

### 3.4 返回格式

```json
{
    "text_analysis": {
        "issues": [
            {
                "type": "grammar",
                "location": "第3段",
                "description": "主谓搭配不当",
                "suggestion": "将'他们走进了'改为'他走进了'"
            },
            {
                "type": "logic",
                "location": "第5段",
                "description": "时间线矛盾",
                "suggestion": "前文说是早上，这里却说夕阳西下"
            }
        ],
        "summary": "发现2处问题：1处语法问题，1处逻辑问题"
    },
    "style_features": {
        "avg_sentence_length": 25,
        "pov": "first_person",
        "dialogue_ratio": 0.3,
        "description_ratio": 0.5,
        "action_ratio": 0.2,
        "tone": "serious",
        "vocabulary_level": "intermediate"
    },
    "consistency_report": {
        "score": 85,
        "inconsistencies": [
            {
                "type": "character",
                "description": "主角在第2章是黑发，第5章变成了金发",
                "chapters": [2, 5]
            }
        ],
        "warnings": [
            {
                "type": "timeline",
                "description": "第3章和第4章的时间跨度不明确"
            }
        ]
    },
    "quality_evaluation": {
        "overall_score": 78,
        "dimension_scores": {
            "readability": 85,
            "creativity": 70,
            "coherence": 80,
            "engagement": 75,
            "accuracy": 80
        },
        "grade": "B+",
        "strengths": ["对话生动", "场景描写细腻"],
        "weaknesses": ["节奏稍慢", "部分转折生硬"],
        "feedback": "整体质量良好，建议加快叙事节奏..."
    }
}
```

### 3.5 分析类型详解

#### 3.5.1 text（文本分析）

检查语法、逻辑、表达等基础问题。

```python
async def _analyze_text(text: str, focus: str) -> dict:
    """
    文本分析

    检查维度：
    - grammar: 语法错误、标点问题
    - logic: 逻辑矛盾、因果关系
    - expression: 表达不清、冗余
    """
    prompt = f"""
    请分析以下文本的问题，重点关注：{focus}

    文本：
    {text}

    请以 JSON 格式返回分析结果：
    {{
        "issues": [
            {{"type": "问题类型", "location": "位置", "description": "描述", "suggestion": "建议"}}
        ],
        "summary": "总结"
    }}
    """

    result = await ai_service.generate(
        prompt=prompt,
        task_type=TaskType.TEXT_ANALYSIS
    )

    return json.loads(result)
```

#### 3.5.2 style（风格分析）

分析写作风格特征，不需要 LLM（规则计算）。

```python
def _analyze_style(text: str) -> dict:
    """
    风格分析（规则计算，不需要 LLM）

    分析维度：
    - 平均句长
    - 人称视角
    - 对话比例
    - 描写比例
    - 动作比例
    - 语气基调
    - 词汇水平
    """
    features = analyze_writing_style(text)

    return {
        "avg_sentence_length": features.avg_sentence_length,
        "pov": features.pov,
        "dialogue_ratio": round(features.dialogue_ratio, 2),
        "description_ratio": round(features.description_ratio, 2),
        "action_ratio": round(features.action_ratio, 2),
        "tone": features.tone,
        "vocabulary_level": features.vocabulary_level
    }
```

#### 3.5.3 consistency（一致性检查）

检查与作品整体的一致性，需要 work_id。

```python
async def _check_consistency(
    text: str,
    work_id: str,
    chapter_id: str
) -> dict:
    """
    一致性检查

    检查维度：
    - character: 人物设定一致性
    - timeline: 时间线一致性
    - worldview: 世界观一致性
    - plot: 情节逻辑一致性
    """
    # 获取作品上下文
    context = await get_work_context(work_id)

    prompt = f"""
    请检查以下新内容与作品整体的一致性：

    作品上下文：
    {context}

    新内容：
    {text}

    请以 JSON 格式返回检查结果：
    {{
        "score": 0-100,
        "inconsistencies": [
            {{"type": "类型", "description": "描述", "chapters": [相关章节]}}
        ],
        "warnings": [
            {{"type": "类型", "description": "描述"}}
        ]
    }}
    """

    result = await ai_service.generate(
        prompt=prompt,
        task_type=TaskType.CONSISTENCY_CHECK
    )

    return json.loads(result)
```

#### 3.5.4 quality（质量评估）

全面评估文本质量。

```python
async def _evaluate_quality(text: str, depth: str) -> dict:
    """
    质量评估

    评估维度：
    - readability: 可读性
    - creativity: 创意性
    - coherence: 连贯性
    - engagement: 吸引力
    - accuracy: 准确性
    """
    prompt = f"""
    请评估以下文本的质量（深度：{depth}）：

    文本：
    {text}

    请以 JSON 格式返回评估结果：
    {{
        "overall_score": 0-100,
        "dimension_scores": {{
            "readability": 0-100,
            "creativity": 0-100,
            "coherence": 0-100,
            "engagement": 0-100,
            "accuracy": 0-100
        }},
        "grade": "A+/A/B+/B/C+/C/D",
        "strengths": ["优点1", "优点2"],
        "weaknesses": ["缺点1", "缺点2"],
        "feedback": "详细反馈"
    }}
    """

    result = await ai_service.generate(
        prompt=prompt,
        task_type=TaskType.QUALITY_EVALUATION
    )

    return json.loads(result)
```

### 3.6 完整实现代码

```python
async def analyze_content(
    text: str,
    work_id: str = "",
    chapter_id: str = "",
    analysis_types: List[str] = None,
    focus: str = "all",
    depth: str = "normal"
) -> str:
    """
    分析内容质量（一站式）

    Args:
        text: 待分析文本
        work_id: 作品ID（用于一致性检查）
        chapter_id: 章节ID（用于上下文）
        analysis_types: 分析类型列表
        focus: 分析重点
        depth: 分析深度

    Returns:
        JSON 格式的分析报告
    """
    if analysis_types is None:
        analysis_types = ["text", "style"]

    result = {}

    # 1. 文本分析（需要 LLM）
    if "text" in analysis_types:
        result["text_analysis"] = await _analyze_text(text, focus)

    # 2. 风格分析（规则计算）
    if "style" in analysis_types:
        result["style_features"] = _analyze_style(text)

    # 3. 一致性检查（需要 LLM + work_id）
    if "consistency" in analysis_types:
        if not work_id:
            result["consistency_report"] = {
                "error": "一致性检查需要提供 work_id"
            }
        else:
            result["consistency_report"] = await _check_consistency(
                text, work_id, chapter_id
            )

    # 4. 质量评估（需要 LLM）
    if "quality" in analysis_types:
        result["quality_evaluation"] = await _evaluate_quality(text, depth)

    return json.dumps(result, ensure_ascii=False)
```

### 3.7 重试/降级机制

保留现有的重试/降级机制：

```python
async def _analyze_with_retry(
    prompt: str,
    task_type: TaskType,
    max_retries: int = 3
) -> str:
    """
    带重试的分析

    重试策略：
    1. 第一次：使用指定 task_type
    2. 第二次：提高温度 +0.1
    3. 第三次：切换到更强模型
    """
    for attempt in range(max_retries):
        try:
            temperature = 0.3 + (attempt * 0.1)

            # 第三次尝试切换模型
            if attempt == 2:
                task_type = TaskType.COMPLEX_ANALYSIS

            result = await ai_service.generate(
                prompt=prompt,
                task_type=task_type,
                temperature=temperature
            )

            # 验证返回格式
            json.loads(result)
            return result

        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            continue

    raise Exception("分析失败，已达最大重试次数")
```

### 3.8 使用场景

#### 场景 1：检查文本问题

```
用户：帮我检查一下这段文字有什么问题
Agent：
  1. 调用 analyze_content(
       text="用户选中的文本",
       analysis_types=["text"],
       focus="all"
     )
  2. 返回：{text_analysis: {issues: [...], summary: "..."}}
```

#### 场景 2：分析写作风格

```
用户：分析一下我的写作风格
Agent：
  1. 调用 analyze_content(
       text="章节内容",
       analysis_types=["style"]
     )
  2. 返回：{style_features: {avg_sentence_length: 25, pov: "first_person", ...}}
```

#### 场景 3：全面评估

```
用户：这章写得怎么样？
Agent：
  1. 调用 analyze_content(
       text="章节内容",
       work_id="xxx",
       analysis_types=["text", "style", "consistency", "quality"],
       depth="deep"
     )
  2. 返回：完整分析报告
```

---

## 4. 删除的工具

| 工具 | 删除原因 | 功能去向 |
|------|---------|---------|
| `analyze_text_tool` | 合并 | `analyze_content` 的 `analysis_types=["text"]` |
| `analyze_style_tool` | 合并 | `analyze_content` 的 `analysis_types=["style"]` |
| `check_story_consistency_tool` | 合并 | `analyze_content` 的 `analysis_types=["consistency"]` |
| `evaluate_quality_tool` | 合并 | `analyze_content` 的 `analysis_types=["quality"]` |

---

## 5. 与其他类工具的关系

### 5.1 Read → Analyze 链路

```
get_writing_context(chapter_orders="5", include=["chapter"])
   ↓ 返回：第5章完整内容
   ↓
analyze_content(text="第5章内容", analysis_types=["text", "quality"])
   ↓ 返回：分析报告
```

### 5.2 Analyze → Update 链路

```
analyze_content(text="...", analysis_types=["text"])
   ↓ 返回：{issues: [{location: "第3段", suggestion: "..."}]}
   ↓
Agent 根据建议调用
   ↓
smart_rewrite(text_to_rewrite="第3段内容", user_requirement="修复语法问题")
```

---

## 6. 迁移计划

### 6.1 代码变更

| 文件 | 变更 |
|------|------|
| `analysis_tools.py` | 新增 `analyze_content` 函数 |
| `analysis_tools.py` | 标记旧工具为 deprecated |
| `tool_executor.py` | 添加别名映射 |
| `planning_examples.py` | 更新工具描述 |

### 6.2 向后兼容

```python
# tool_executor.py
TOOL_NAME_MAPPING = {
    # ... 现有映射
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

### 6.3 参数转换

```python
def _convert_legacy_analyze_params(tool_name: str, params: dict) -> dict:
    """将旧分析工具参数转换为 analyze_content 参数"""

    if tool_name in ["analyze_text_tool", "analyze_text"]:
        return {
            "text": params.get("text", ""),
            "analysis_types": ["text"],
            "focus": params.get("focus", "all")
        }

    if tool_name in ["analyze_style_tool", "analyze_style"]:
        return {
            "text": params.get("text", ""),
            "analysis_types": ["style"]
        }

    if tool_name in ["check_story_consistency_tool", "check_story_consistency"]:
        return {
            "text": params.get("text", ""),
            "work_id": params.get("work_id", ""),
            "analysis_types": ["consistency"]
        }

    if tool_name in ["evaluate_quality_tool", "evaluate_quality"]:
        return {
            "text": params.get("text", ""),
            "analysis_types": ["quality"],
            "depth": params.get("depth", "normal")
        }

    return params
```
