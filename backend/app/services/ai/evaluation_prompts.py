"""
AI评价功能的Prompt模板

用于生成AI内容的质量评价
"""

from typing import Optional


# ===== 统一评价Prompt模板 =====
EVALUATION_PROMPT_TEMPLATE = """你是专业的AI文本评审专家。请对以下生成内容进行客观、严谨的评价。

**生成内容**:
{text}

**上下文信息**:
{context_info}

**评价任务**:
请从以下5个维度对生成内容进行评分(0-100分):

1. **文学性** (literary_quality)
   - 语言质量、修辞手法、文字美感
   - 词汇丰富度、句式变化

2. **连贯性** (coherence)
   - 与前文衔接的自然度
   - 逻辑流畅度、过渡顺畅

3. **创意性** (creativity)
   - 新颖度、想象力
   - 打破常规、独特视角

4. **情感感染力** (emotional_impact)
   - 情感表达的细腻度
   - 读者共鸣度、代入感

5. **节奏把控** (pacing)
   - 快慢适度、张弛有度
   - 信息密度合理

**返回格式** (严格JSON):
```json
{{
  "overall_score": <总分(5个维度的平均分)>,
  "dimensions": {{
    "literary_quality": <分数>,
    "coherence": <分数>,
    "creativity": <分数>,
    "emotional_impact": <分数>,
    "pacing": <分数>
  }},
  "highlights": ["优点1", "优点2", "优点3"],
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2", "建议3"]
}}
```

**评价要求**:
1. 客观中立,既要肯定优点也要指出不足
2. 建议要具体可操作,不要泛泛而谈
3. 结合上下文和作品风格评价
4. 避免主观偏见,以读者视角评判
5. 优点至少列举2-3个,问题和建议各1-3个
6. 必须返回有效的JSON格式,不要添加任何注释或说明文字

请开始评价:"""


# ===== 上下文信息格式化 =====
def format_context_info(
    work_title: Optional[str] = None,
    chapter_title: Optional[str] = None,
    previous_text: Optional[str] = None,
    operation_type: str = "continue"
) -> str:
    """
    格式化上下文信息

    Args:
        work_title: 作品标题
        chapter_title: 章节标题
        previous_text: 前文片段
        operation_type: 操作类型

    Returns:
        格式化后的上下文信息
    """
    parts = []

    if work_title:
        parts.append(f"- 作品: {work_title}")

    if chapter_title:
        parts.append(f"- 章节: {chapter_title}")

    # 操作类型的中文映射
    operation_names = {
        "continue": "续写",
        "polish": "润色",
        "expand": "扩写",
        "translate": "翻译",
        "summarize": "总结"
    }
    operation_name = operation_names.get(operation_type, operation_type)
    parts.append(f"- 操作类型: {operation_name}")

    if previous_text:
        # 截取前文(最多500字)
        truncated_text = previous_text[:500]
        if len(previous_text) > 500:
            truncated_text += "..."
        parts.append(f"- 前文片段:\n{truncated_text}")

    if not parts:
        return "- 无上下文信息"

    return "\n".join(parts)


# ===== 生成评价Prompt =====
def get_evaluation_prompt(
    text: str,
    work_title: Optional[str] = None,
    chapter_title: Optional[str] = None,
    previous_text: Optional[str] = None,
    operation_type: str = "continue"
) -> str:
    """
    生成评价Prompt

    Args:
        text: 待评价的文本
        work_title: 作品标题
        chapter_title: 章节标题
        previous_text: 前文片段
        operation_type: 操作类型

    Returns:
        完整的评价Prompt
    """
    context_info = format_context_info(
        work_title=work_title,
        chapter_title=chapter_title,
        previous_text=previous_text,
        operation_type=operation_type
    )

    return EVALUATION_PROMPT_TEMPLATE.format(
        text=text,
        context_info=context_info
    )


# ===== 系统Prompt =====
EVALUATION_SYSTEM_PROMPT = """你是一位专业的文学评审专家,擅长从多个维度客观评价AI生成的文学内容。

你的评价特点:
1. 客观公正,不偏袒也不苛责
2. 既能发现优点,也能指出问题
3. 建议具体可操作,有实际指导价值
4. 评分标准一致,不会受情绪影响

你必须严格返回JSON格式的评价结果,不添加任何额外说明。"""
