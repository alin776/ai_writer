"""
质量评估Prompt模板

包含各个维度的评估Prompt
"""


# ========================================
# 内容质量评估Prompt
# ========================================

CONTENT_QUALITY_PROMPT = """你是一位专业的网文编辑,请评估以下内容的质量。

评估内容:
{content}

评估标准:
1. 情节是否吸引人 (是否有冲突、爽点、悬念)
2. 人物刻画是否生动 (对话、动作、心理描写)
3. 场景描写是否细腻 (环境、氛围营造)
4. 节奏是否合理 (不拖沓、不突兀)

请给出0-10分的评分,并说明理由。

输出格式(严格遵守):
分数: [0-10的数字]
理由: [具体的评价,80字以内,简洁清晰]
"""


# ========================================
# 连贯性评估Prompt
# ========================================

COHERENCE_PROMPT = """你是一位专业的网文编辑,请评估内容的连贯性。

前文内容:
{previous_content}

当前内容:
{current_content}

评估标准:
1. 与前文是否自然衔接 (时间、地点、人物状态)
2. 情节发展是否合理 (逻辑自洽,没有突兀)
3. 人物行为是否符合设定 (性格一致,动机合理)
4. 没有明显的断层或跳跃

请给出0-10分的评分,并说明理由。

输出格式(严格遵守):
分数: [0-10的数字]
理由: [具体的评价,80字以内,简洁清晰]
"""


# 连贯性评估Prompt - 无前文版本
COHERENCE_PROMPT_NO_PREVIOUS = """你是一位专业的网文编辑,请评估以下内容的内部连贯性。

当前内容:
{current_content}

评估标准:
1. 情节发展是否合理 (逻辑自洽)
2. 人物行为是否前后一致
3. 场景转换是否自然
4. 没有明显的逻辑矛盾

请给出0-10分的评分,并说明理由。

输出格式(严格遵守):
分数: [0-10的数字]
理由: [具体的评价,80字以内,简洁清晰]
"""


# ========================================
# 风格一致性评估Prompt
# ========================================

STYLE_CONSISTENCY_PROMPT = """你是一位专业的网文编辑,请评估写作风格的一致性。

参考风格:
{reference_style}

当前内容:
{content}

评估标准:
1. 叙述语气是否一致 (第一人称/第三人称)
2. 用词风格是否一致 (现代/古风/幽默等)
3. 句式长短是否协调
4. 整体氛围是否统一

请给出0-10分的评分,并说明理由。

输出格式(严格遵守):
分数: [0-10的数字]
理由: [具体的评价,80字以内,简洁清晰]
"""


# ========================================
# 语法正确性评估Prompt
# ========================================

GRAMMAR_PROMPT = """你是一位专业的文字编辑,请检查以下内容的语法和错别字。

内容:
{content}

评估标准:
1. 没有错别字
2. 没有语法错误 (主谓宾、标点符号正确)
3. 没有逻辑矛盾或表达不清
4. 用词准确恰当

请给出0-10分的评分,并列出发现的问题。

输出格式:
分数: [0-10的数字]
问题列表: [发现的问题,每个问题一行。如果没有问题,写"无"]
"""


# ========================================
# Prompt工具类
# ========================================

class QualityPrompts:
    """质量评估Prompt管理类"""

    @staticmethod
    def get_content_quality_prompt(content: str) -> str:
        """获取内容质量评估Prompt"""
        return CONTENT_QUALITY_PROMPT.format(content=content)

    @staticmethod
    def get_coherence_prompt(current_content: str, previous_content: str = None) -> str:
        """获取连贯性评估Prompt"""
        if previous_content:
            # 只取前1000字避免token过多
            prev_content_truncated = previous_content[-1000:] if len(previous_content) > 1000 else previous_content
            return COHERENCE_PROMPT.format(
                current_content=current_content,
                previous_content=prev_content_truncated
            )
        else:
            # 没有前文,评估内部连贯性
            return COHERENCE_PROMPT_NO_PREVIOUS.format(current_content=current_content)

    @staticmethod
    def get_style_prompt(content: str, reference_style: str = None) -> str:
        """获取风格一致性评估Prompt"""
        style = reference_style or "现代都市网文风格"
        return STYLE_CONSISTENCY_PROMPT.format(
            content=content,
            reference_style=style
        )

    @staticmethod
    def get_grammar_prompt(content: str) -> str:
        """获取语法正确性评估Prompt"""
        return GRAMMAR_PROMPT.format(content=content)
