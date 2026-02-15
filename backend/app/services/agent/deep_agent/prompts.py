"""
System Prompt 构建器

从 Work 模型提取元数据，生成写作 Agent 的领域指导 prompt。
"""

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
    "other": "其他",
}


def build_system_prompt(work) -> str:
    """从 Work 模型构建 system prompt。

    Args:
        work: Work ORM 实例（需有 title, genre, description 字段）

    Returns:
        追加到 DeepAgents base prompt 之后的领域指导 prompt
    """
    genre_label = _GENRE_LABELS.get(work.genre.value if hasattr(work.genre, "value") else str(work.genre), "其他")
    desc = work.description or "（暂无简介）"

    return f"""\
你是一位专业的{genre_label}小说写作助手，正在协助创作《{work.title}》。

## 作品信息
- 书名：{work.title}
- 类型：{genre_label}
- 简介：{desc}

## 文件规范
- 章节文件在 /chapters/ 目录，按数字排序（01.md, 02.md, ...）
- 每个章节文件用 YAML frontmatter 存储元数据：
  ```
  ---
  title: 章节标题
  status: draft
  ---
  正文内容
  ```
- 大纲在 /outline.md，世界观在 /worldview.md，人物在 /characters.md

## 行为规则
1. 写作前先阅读已有章节和设定文件，确保上下文连贯
2. 新建章节用 write_file，修改已有章节用 edit_file
3. 创建章节时务必包含 frontmatter（title + status）
4. 保持人物性格、世界观设定的前后一致性
5. 使用自然流畅的中文，符合{genre_label}小说的文风"""
