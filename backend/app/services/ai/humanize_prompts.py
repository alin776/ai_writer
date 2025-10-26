"""
去痕迹功能 Prompt 模板库

包含:
1. AI特征检测 Prompt
2. 三种强度的去痕迹 Prompt (light/medium/strong)
3. 验证 Prompt
"""

from typing import Literal


# ========== AI特征检测 Prompt ==========

DETECTION_PROMPT = """你是一位专业的 AI 文本检测专家。请对以下文本进行 AI 特征分析,从5个维度评分:

**评分维度:**
1. **pattern_repetition (模式重复)**: 是否存在过于规整的段落结构、重复的句式模板
2. **word_choice (词汇选择)**: 是否使用过于正式/书面的词汇、缺乏口语化表达
3. **sentence_structure (句式结构)**: 是否句子长度过于均匀、缺乏自然的长短变化
4. **tone_style (语气风格)**: 是否语气过于客观中立、缺乏个人情感
5. **formatting (格式规范)**: 是否格式过于工整、缺乏自然的不规则性

**评分标准:**
- 0-30分: 非常自然,几乎无AI痕迹
- 31-60分: 较为自然,有少量AI痕迹
- 61-80分: 明显AI痕迹,需要人性化改写
- 81-100分: 典型AI生成,强烈建议改写

**请以 JSON 格式返回结果:**
```json
{{
  "overall_score": 75,
  "dimensions": {{
    "pattern_repetition": {{"score": 80, "description": "模式重复", "issues": ["段落结构过于规整", "存在重复句式"]}},
    "word_choice": {{"score": 70, "description": "词汇选择", "issues": ["使用了过多书面语"]}},
    "sentence_structure": {{"score": 75, "description": "句式结构", "issues": ["句子长度过于均匀"]}},
    "tone_style": {{"score": 65, "description": "语气风格", "issues": ["语气过于客观"]}},
    "formatting": {{"score": 85, "description": "格式规范", "issues": ["格式过于工整"]}}
  }},
  "detected_patterns": [
    "首先...其次...最后... 的典型AI结构",
    "过度使用'值得注意的是'等连接词",
    "段落长度过于统一"
  ],
  "needs_humanization": true
}}
```

**待检测文本:**
{text}

请严格按照上述 JSON 格式返回分析结果,不要包含任何其他内容。"""


# ========== 轻度去痕迹 Prompt (5%改动) ==========

HUMANIZE_LIGHT_PROMPT = """你是一位专业的文本人性化专家。请对以下 AI 生成的文本进行**轻度**去痕迹改写。

**改写目标:**
- 改动幅度: ~5% (仅修改最明显的AI痕迹)
- 保持: 99%的原文内容、结构、语义
- 修改: 替换1-2个明显的AI化用词、调整1-2处过于工整的句式

**改写策略:**
1. 将过于正式的词汇替换为日常用语 (如: "值得注意" → "要注意", "综上所述" → "总之")
2. 打破1-2个过于规整的句式 (如: 拆分过长句子、合并短句)
3. 保持所有专业术语、数据、逻辑不变

**禁止:**
- 添加或删除段落
- 改变核心观点
- 修改超过5%的内容

**原文:**
{text}

**请直接输出改写后的文本,不要包含任何解释或说明。**"""


# ========== 中度去痕迹 Prompt (15-20%改动) ==========

HUMANIZE_MEDIUM_PROMPT = """你是一位专业的文本人性化专家。请对以下 AI 生成的文本进行**中度**去痕迹改写。

**改写目标:**
- 改动幅度: 15-20% (平衡自然度与内容保留)
- 保持: 核心内容、主要观点、逻辑结构
- 修改: 句式结构、用词风格、段落组织

**改写策略:**
1. **打破AI模板结构:**
   - 避免"首先...其次...最后..."等典型结构
   - 减少过于规整的段落划分
   - 打破句子长度的均匀性

2. **自然化用词:**
   - 减少书面语,增加口语化表达
   - 避免过度使用"值得注意的是"、"综上所述"等AI化连接词
   - 适当使用口语化的过渡词 (如: "不过"、"话说回来"、"其实")

3. **增加自然不规则性:**
   - 让句子长短不一
   - 适当使用省略、倒装等自然语言特征
   - 保留一些"不完美"的表达

**禁止:**
- 改变核心观点和论据
- 删除重要信息
- 修改专业术语和数据

**原文:**
{text}

**请直接输出改写后的文本,不要包含任何解释或说明。**"""


# ========== 强度去痕迹 Prompt (30-40%改动) ==========

HUMANIZE_STRONG_PROMPT = """你是一位专业的文本人性化专家。请对以下 AI 生成的文本进行**强度**去痕迹改写。

**改写目标:**
- 改动幅度: 30-40% (最大化自然度)
- 保持: 核心观点、关键信息
- 修改: 大幅调整表达方式、语言风格、结构组织

**改写策略:**
1. **彻底打破AI风格:**
   - 完全重构句式和段落结构
   - 避免所有典型AI模板 ("首先...其次..."、"综上所述"等)
   - 用更加个性化、口语化的方式重新表达

2. **增加人类化特征:**
   - 使用更多口语化表达和简短句
   - 适当添加语气词 (如: "吧"、"呢"、"嘛"、"啊")
   - 允许不完全对称的结构
   - 可以适当使用反问、感叹等修辞手法

3. **灵活重组:**
   - 可以调整段落顺序
   - 可以合并或拆分段落
   - 可以用不同的例子替换原例子 (但要保持准确性)

**禁止:**
- 改变核心论点
- 篡改事实和数据
- 添加虚假信息

**原文:**
{text}

**请直接输出改写后的文本,不要包含任何解释或说明。**"""


# ========== 验证 Prompt ==========

VERIFICATION_PROMPT = """请对比以下两段文本的 AI 特征分数:

**原文:**
{original_text}

**改写后:**
{humanized_text}

请分别对两段文本进行 AI 特征评分 (0-100分,分数越高表示AI痕迹越明显),并计算改进幅度。

**请以 JSON 格式返回:**
```json
{{
  "score_before": 75,
  "score_after": 45,
  "improvement": 30,
  "success": true
}}
```

请严格按照上述 JSON 格式返回结果。"""


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
