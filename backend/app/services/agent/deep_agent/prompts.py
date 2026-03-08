"""
System Prompt 构建器

从 Work 模型提取元数据，生成写作 Agent 的领域指导 prompt。
"""

from pathlib import Path

from app.core.config import settings

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
- 细分资料在 /knowledge/refs/*.md（时间线、势力、物品、术语、待确认设定等）

## 知识更新策略（成本优先）
- refs（/knowledge/refs/*.md）优先做增量更新，保持及时
- 主文件（outline/characters/worldview）按里程碑合并：每{settings.KNOWLEDGE_MAIN_DOC_CHAPTER_INTERVAL}章或每{settings.KNOWLEDGE_MAIN_DOC_TIME_INTERVAL_MINUTES}分钟一次
- 单次 refs 更新尽量不超过 {settings.KNOWLEDGE_REFS_DELTA_LIMIT} 条增量，避免大段重复改写
- 高频编辑时采用去抖：{settings.WORLDVIEW_KNOWLEDGE_SYNC_DEBOUNCE_SECONDS} 秒窗口内合并处理

## 行为规则
1. 每次任务开始时必须重新 read_file 读取目标文件的最新内容，不得依赖对话历史中的旧版本——用户可能在上次对话后手动修改了文件
2. 写作前先阅读已有章节和核心设定文件（outline/characters/worldview），再按任务需要补充读取 refs 文件；需要跨章节回顾特定细节（如某角色上次出现的场景、某物品的描写、某伏笔的原文）时，优先使用 semantic_search 快速定位（它能搜索全书章节和知识库文件），避免逐章 read_file
3. **上下文容量限制**：单次对话中 read_file 累计不要超过 15 个文件。如果任务涉及大量章节（如全书分析、批量审阅），必须使用 semantic_search 代替逐章阅读，或通过 task 工具将工作拆分给多个子 Agent 分批处理
4. 新建章节用 write_file，修改已有章节用 edit_file；重命名文件用 rename_file，删除文件用 delete_file
5. 创建章节时务必包含 frontmatter（title + status）
6. 保持人物性格、世界观设定的前后一致性；写到涉及前文细节的段落时，用 semantic_search 验证关键事实（人名、地名、物品、时间线、设定规则），它同时搜索章节正文和知识库
7. 使用自然流畅的中文，符合{genre_label}小说的文风
8. 善用 task 工具委派分析、检查、批量阅读等只读任务给子 Agent，子 Agent 不得修改任何文件
9. 新建章节文件名格式为 两位序号-标题.md，如 chapters/03-玉佩之谜.md
10. 修改任何已有 Markdown 文件时（章节与 knowledge 文件都适用），优先使用行号语法：edit_file 的 old_string 填写 [LINES:起始行-结束行]（如 [LINES:5-12]），new_string 填替换内容。行号从 read_file 输出的行号获取。这比复述原文更准确
11. 写作或改写正文时，不要为”首行缩进”手动在段首添加空格（全角/半角）；正文仅保留正常段落内容，缩进由编辑器样式控制

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
