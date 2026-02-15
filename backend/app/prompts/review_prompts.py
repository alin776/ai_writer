"""
小说评审 Prompt 模板库
提供不同粒度(段落/章节/作品)的评审提示词模板
"""


class ReviewPromptTemplates:
    """评审提示词模板"""

    # ==================== 章节级评审 (8维度) ====================

    CHAPTER_REVIEW_SYSTEM = """你是一位资深的小说编辑和文学评论家,擅长从多个维度深入分析小说章节的优缺点。

你的任务是对提供的小说章节进行全面、客观的评审,从以下8个维度进行打分和分析:

1. **文学性** (literary_quality): 语言质量、修辞手法、文字优美程度
2. **情节合理性** (plot_logic): 逻辑严密性、因果关系、情节连贯性
3. **人物塑造** (character): 人物行为一致性、对话真实性、性格鲜明度
4. **节奏把控** (pacing): 快慢节奏、张弛有度、阅读体验
5. **场景描写** (scene): 画面感、细节丰富度、沉浸感
6. **情感感染力** (emotion): 共鸣度、情绪调动能力、感染力
7. **伏笔铺垫** (foreshadowing): 悬念设置、伏笔铺垫、前后呼应
8. **创意新颖度** (creativity): 打破常规、想象力、独创性

评分标准:
- 90-100分: 优秀,该维度表现出色
- 75-89分: 良好,该维度表现不错但有提升空间
- 60-74分: 及格,该维度达到基本要求
- 0-59分: 不及格,该维度存在明显问题

**重要**: 你必须且只能返回纯 JSON 格式,不要包含任何解释、markdown标记或其他文本。直接以 { 开始,以 } 结束。"""

    CHAPTER_REVIEW_USER = """请评审以下小说章节:

**章节标题**: {title}
**章节内容**:
{content}

请从8个维度进行评分,并提供:
1. 每个维度的具体评分(0-100)和简要分析
2. 本章的3-5个亮点
3. 本章的3-5个主要问题
4. 5-8条具体的改进建议

**重要**: 只返回纯 JSON,不要包含任何额外文本或 markdown 标记。直接输出:
{{
    "overall_score": 总分(8个维度平均分),
    "dimension_scores": {{
        "literary_quality": 分数,
        "plot_logic": 分数,
        "character": 分数,
        "pacing": 分数,
        "scene": 分数,
        "emotion": 分数,
        "foreshadowing": 分数,
        "creativity": 分数
    }},
    "dimension_analysis": {{
        "literary_quality": "分析说明",
        "plot_logic": "分析说明",
        ...
    }},
    "highlights": ["亮点1", "亮点2", ...],
    "issues": ["问题1", "问题2", ...],
    "suggestions": ["建议1", "建议2", ...]
}}"""

    # ==================== 段落级评审 (4维度) ====================

    PARAGRAPH_REVIEW_SYSTEM = """你是一位细致的文字编辑,擅长快速评估段落级别的写作质量。

你的任务是对提供的段落进行快速评审,从以下4个维度打分:

1. **语言质量** (language): 文字流畅度、修辞手法
2. **描写生动度** (vividness): 画面感、代入感
3. **对话真实性** (dialogue): 符合人物性格、自然流畅
4. **情感表达** (emotion): 感染力、共鸣度

评分标准: 0-100分

请以JSON格式返回简洁的评审结果。"""

    PARAGRAPH_REVIEW_USER = """请评审以下段落:

**段落内容**:
{content}

{context_hint}

返回JSON格式:
{{
    "overall_score": 总分,
    "dimension_scores": {{
        "language": 分数,
        "vividness": 分数,
        "dialogue": 分数,
        "emotion": 分数
    }},
    "quick_feedback": "简短反馈(50字内)",
    "suggestions": ["建议1", "建议2"]
}}"""

    # ==================== 作品级评审 (10维度) ====================

    WORK_REVIEW_SYSTEM = """你是一位资深的文学编辑和出版顾问,擅长从宏观角度评估整部作品的完整性和商业潜力。

你的任务是对整部作品进行全面评审,从以下10个维度打分:

1. **大纲结构** (structure): 三幕/五幕结构完整性
2. **主题表达** (theme): 中心思想、价值观深度
3. **人物弧光** (character_arc): 主角/配角成长轨迹
4. **情节节奏** (pacing): 高潮分布、起承转合
5. **世界观一致性** (worldview): 设定逻辑、内部统一
6. **伏笔回收率** (foreshadowing): 埋伏笔→挖伏笔完成度
7. **对白质量** (dialogue): 个性化、推动情节
8. **文笔风格统一性** (style): 前后风格一致
9. **商业潜力** (commercial): 类型定位、市场接受度
10. **创新度** (innovation): 同类作品对比、差异化

评分标准: 0-100分

请以JSON格式返回详细的评审报告。"""

    WORK_REVIEW_USER = """请评审以下作品:

**作品标题**: {title}
**作品类型**: {genre}
**总章节数**: {chapter_count}
**总字数**: {word_count}

**作品梗概**:
{summary}

**章节摘要** (前10章):
{chapter_summaries}

返回JSON格式:
{{
    "overall_score": 总分,
    "dimension_scores": {{
        "structure": 分数,
        "theme": 分数,
        "character_arc": 分数,
        "pacing": 分数,
        "worldview": 分数,
        "foreshadowing": 分数,
        "dialogue": 分数,
        "style": 分数,
        "commercial": 分数,
        "innovation": 分数
    }},
    "dimension_analysis": {{
        "structure": "分析",
        ...
    }},
    "highlights": ["亮点1", ...],
    "issues": ["问题1", ...],
    "suggestions": ["建议1", ...],
    "commercial_report": {{
        "target_audience": "目标读者群",
        "market_potential": "市场潜力评估",
        "competitive_analysis": "竞品分析",
        "publishing_suggestions": "出版建议"
    }}
}}"""

    # ==================== 任务生成 Prompt ====================

    TASK_GENERATION_SYSTEM = """你是一位经验丰富的小说编辑助理,擅长将评审结果转化为具体的、可操作的修改任务。

你的任务是根据评审结果,生成5-10个具体的修改任务,每个任务应该:
1. 标题简洁明了(20字内)
2. 描述具体可操作
3. 精确定位到段落
4. 分配合理的优先级(P0/P1/P2)
5. 提供预估修改时间

优先级判断标准:
- P0 (紧急): 评分<60分的维度,或核心问题(plot/character)
- P1 (重要): 评分60-75分的维度
- P2 (优化): 评分>75分但仍可提升的地方

请以JSON数组格式返回任务清单。"""

    TASK_GENERATION_USER = """根据以下评审结果,生成具体的修改任务:

**评审总分**: {overall_score}
**维度评分**: {dimension_scores}
**问题列表**: {issues}
**改进建议**: {suggestions}

**章节内容** (用于定位):
{content}

返回JSON格式:
[
    {{
        "title": "优化第3段的人物动机描写",
        "description": "当前问题: 主角突然做出XX决定,缺乏铺垫。建议: 在第2-3段之间增加内心独白...",
        "priority": "P0",
        "category": "character",
        "location": {{
            "paragraph_index": 3,
            "start_pos": 120,
            "end_pos": 300,
            "text_snippet": "段落前50字..."
        }},
        "related_score": "character",
        "current_score": 65,
        "estimated_time": 15,
        "tags": ["人物动机", "内心独白"]
    }},
    ...
]"""

    # ==================== 辅助方法 ====================

    @staticmethod
    def get_chapter_review_prompt(title: str, content: str) -> tuple[str, str]:
        """获取章节评审提示词"""
        return (
            ReviewPromptTemplates.CHAPTER_REVIEW_SYSTEM,
            ReviewPromptTemplates.CHAPTER_REVIEW_USER.format(
                title=title,
                content=content
            )
        )

    @staticmethod
    def get_paragraph_review_prompt(content: str, context: str = None) -> tuple[str, str]:
        """获取段落评审提示词"""
        context_hint = ""
        if context:
            context_hint = f"\n**上下文**: {context}"

        return (
            ReviewPromptTemplates.PARAGRAPH_REVIEW_SYSTEM,
            ReviewPromptTemplates.PARAGRAPH_REVIEW_USER.format(
                content=content,
                context_hint=context_hint
            )
        )

    @staticmethod
    def get_work_review_prompt(
        title: str,
        genre: str,
        chapter_count: int,
        word_count: int,
        summary: str,
        chapter_summaries: str
    ) -> tuple[str, str]:
        """获取作品评审提示词"""
        return (
            ReviewPromptTemplates.WORK_REVIEW_SYSTEM,
            ReviewPromptTemplates.WORK_REVIEW_USER.format(
                title=title,
                genre=genre,
                chapter_count=chapter_count,
                word_count=word_count,
                summary=summary,
                chapter_summaries=chapter_summaries
            )
        )

    @staticmethod
    def get_task_generation_prompt(
        overall_score: float,
        dimension_scores: dict,
        issues: list,
        suggestions: list,
        content: str
    ) -> tuple[str, str]:
        """获取任务生成提示词"""
        return (
            ReviewPromptTemplates.TASK_GENERATION_SYSTEM,
            ReviewPromptTemplates.TASK_GENERATION_USER.format(
                overall_score=overall_score,
                dimension_scores=dimension_scores,
                issues=issues,
                suggestions=suggestions,
                content=content
            )
        )
