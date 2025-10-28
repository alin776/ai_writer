"""
去痕迹功能 Prompt 模板库

包含:
1. AI特征检测 Prompt
2. 三种强度的去痕迹 Prompt (light/medium/strong)
3. 验证 Prompt
"""

from typing import Literal


# ========== AI特征检测 Prompt ==========

DETECTION_PROMPT = """检测以下文本的AI特征,从3个核心维度评分(0-100分,分越高越像AI):

**维度:**
1. **pattern_repetition (模式重复)**: 规整结构、重复句式
2. **word_choice (词汇风格)**: 过于书面化、缺乏口语
3. **tone_style (语气风格)**: 过于客观、缺乏情感

**返回JSON格式:**
```json
{{
  "overall_score": 75,
  "dimensions": {{
    "pattern_repetition": {{"score": 80, "description": "模式重复", "issues": ["典型AI结构"]}},
    "word_choice": {{"score": 70, "description": "词汇选择", "issues": ["书面语过多"]}},
    "tone_style": {{"score": 65, "description": "语气风格", "issues": ["语气过于客观"]}}
  }},
  "detected_patterns": ["首先...其次...最后...", "过度使用连接词"],
  "needs_humanization": true
}}
```

**待检测文本:**
{text}

请严格返回JSON,不要其他内容。"""


# ========== 轻度去痕迹 Prompt (5%改动) ==========

HUMANIZE_LIGHT_PROMPT = """对以下AI文本进行**轻度**去痕迹改写(~5%改动):

**目标:**
- 仅修改最明显的AI痕迹
- 保持99%原文内容、结构、语义

**策略:**
1. 替换1-2个AI化用词 (如: "值得注意" → "要注意")
2. 调整1-2处过于工整的句式

**禁止:** 添加/删除段落、改变观点、修改超过5%内容

**原文:**
{text}

**直接输出改写后的文本:**"""


# ========== 中度去痕迹 Prompt (15-20%改动) ==========

HUMANIZE_MEDIUM_PROMPT = """对以下AI文本进行**中度**去痕迹改写(15-20%改动):

**目标:** 平衡自然度与内容保留

**策略:**
1. 打破AI模板 (避免"首先...其次...最后...")
2. 自然化用词 (减少书面语,增加口语)
3. 增加不规则性 (句子长短不一,适当省略/倒装)

**保持:** 核心内容、观点、逻辑

**原文:**
{text}

**直接输出改写后的文本:**"""


# ========== 强度去痕迹 Prompt (30-40%改动) ==========

HUMANIZE_STRONG_PROMPT = """对以下AI文本进行**强度**去痕迹改写(30-40%改动):

**目标:** 最大化自然度

**策略:**
1. 彻底重构句式和段落
2. 用口语化方式重新表达
3. 添加语气词 (如: "吧"、"呢"、"嘛")
4. 使用反问、感叹等修辞

**保持:** 核心论点、事实数据

**原文:**
{text}

**直接输出改写后的文本:**"""


# ========== 验证 Prompt ==========

VERIFICATION_PROMPT = """对比两段文本的AI特征分数(0-100,分越高越像AI):

**原文:**
{original_text}

**改写后:**
{humanized_text}

**返回JSON:**
```json
{{
  "score_before": 75,
  "score_after": 45,
  "improvement": 30,
  "success": true
}}
```"""


# ========== 辅助函数 ==========

def get_humanize_prompt(
    text: str,
    intensity: Literal["light", "medium", "strong"] = "medium"
) -> str:
    """
    获取去痕迹 Prompt

    Args:
        text: 待去痕迹的文本
        intensity: 强度 (light/medium/strong)

    Returns:
        完整的 Prompt
    """
    prompt_map = {
        "light": HUMANIZE_LIGHT_PROMPT,
        "medium": HUMANIZE_MEDIUM_PROMPT,
        "strong": HUMANIZE_STRONG_PROMPT
    }

    template = prompt_map.get(intensity, HUMANIZE_MEDIUM_PROMPT)
    return template.format(text=text)


def get_detection_prompt(text: str) -> str:
    """获取检测 Prompt"""
    return DETECTION_PROMPT.format(text=text)


def get_verification_prompt(original_text: str, humanized_text: str) -> str:
    """获取验证 Prompt"""
    return VERIFICATION_PROMPT.format(
        original_text=original_text,
        humanized_text=humanized_text
    )
