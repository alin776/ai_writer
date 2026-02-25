"""
System Prompt 构建器

从 Work 模型提取元数据，生成写作 Agent 的领域指导 prompt。
"""

from pathlib import Path

GENRE_PROMPTS_DIR = Path(__file__).parent.parent / "genre_prompts"
SKILLS_ROOT = Path(__file__).parent.parent / "skills"

# 始终注入到 system prompt 的 Skill 文件（无需用户选择）
_ALWAYS_ACTIVE_SKILLS = [
    "core/subagent-strategy",
]


def _extract_skill_body(content: str) -> str:
    """从 SKILL.md 内容中提取 Markdown body（去除 YAML frontmatter）。"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return content

_GENRE_FILE_MAP = {
    "fantasy": "xianxia.md",
    "romance": "romance.md",
    "suspense": "suspense.md",
    "urban": "urban.md",
    "western_fantasy": "western-fantasy.md",
    "scifi": "scifi.md",
    "history": "historical.md",
    "wuxia": "wuxia.md",
    "game": "game.md",
    "apocalypse": "apocalypse.md",
}

# 类型名称映射
_GENRE_LABELS = {
    "fantasy": "玄幻",
    "urban": "都市",
    "romance": "言情",
    "scifi": "科幻",
    "wuxia": "武侠",
    "game": "游戏",
    "history": "历史",
    "military": "军事",
    "suspense": "悬疑",
    "western_fantasy": "西幻",
    "apocalypse": "末世",
    "other": "其他",
}


def build_system_prompt(work) -> str:
    """从 Work 模型构建 system prompt。

    Args:
        work: Work ORM 实例（需有 title, genre, description 字段）

    Returns:
        追加到 DeepAgents base prompt 之后的领域指导 prompt
    """
    genre_value = work.genre.value if hasattr(work.genre, "value") else str(work.genre)
    genre_label = _GENRE_LABELS.get(genre_value, "其他")
    desc = work.description or "（暂无简介）"

    prompt = f"""\
你是一位专业的{genre_label}小说写作助手，正在协助创作《{work.title}》。

## 作品信息
- 书名：{work.title}
- 类型：{genre_label}
- 简介：{desc}

## 文件规范
- 章节文件在 /chapters/ 目录，按数字排序（01-标题.md, 02-标题.md, ...）
- 每个章节文件用 YAML frontmatter 存储元数据：
  ```
  ---
  title: 章节标题
  status: draft
  ---
  正文内容
  ```
- 大纲在 /knowledge/outline.md，世界观在 /knowledge/worldview.md，人物在 /knowledge/characters.md

## 行为规则
1. 写作前先阅读已有章节和设定文件，确保上下文连贯
2. 新建章节用 write_file，修改已有章节用 edit_file；重命名文件用 rename_file，删除文件用 delete_file
3. 创建章节时务必包含 frontmatter（title + status）
4. 保持人物性格、世界观设定的前后一致性
5. 使用自然流畅的中文，符合{genre_label}小说的文风
6. 善用 task 工具委派分析、检查、批量阅读等只读任务给子 Agent
7. 新建章节文件名格式为 两位序号-标题.md，如 chapters/03-玉佩之谜.md
8. 修改已有章节时，优先使用行号语法：edit_file 的 old_string 填写 [LINES:起始行-结束行]（如 [LINES:5-12]），new_string 填替换内容。行号从 read_file 输出的行号获取。这比复述原文更准确

## 交互风格
- 每次调用工具前，先用一句简短的话说明你接下来要做什么（如"让我先看看已有的章节…"）
- 工具返回结果后，简要解释关键发现，再决定下一步
- 不要连续调用多个工具而不做任何解释，要像对话一样，一步一步地推进
- 最终给出清晰的总结"""

    # 追加题材风格指南（如果有对应文件）
    genre_file = _GENRE_FILE_MAP.get(genre_value)
    if genre_file:
        genre_path = GENRE_PROMPTS_DIR / genre_file
        if genre_path.exists():
            prompt += f"\n\n## 题材风格指南\n\n{genre_path.read_text(encoding='utf-8')}"

    # 追加始终活跃的策略 Skill
    for skill_rel in _ALWAYS_ACTIVE_SKILLS:
        skill_path = SKILLS_ROOT / skill_rel / "SKILL.md"
        if skill_path.exists():
            body = _extract_skill_body(skill_path.read_text(encoding="utf-8"))
            prompt += f"\n\n{body}"

    return prompt
