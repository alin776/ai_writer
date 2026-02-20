"""
Knowledge templates bootstrap utilities.

Keep core mirror files stable while providing optional structured refs docs.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


MAIN_TEMPLATES: dict[str, str] = {
    "outline.md": """# 大纲

## 一句话梗概
- 

## 主线剧情（按阶段）
1. 起：
2. 承：
3. 转：
4. 合：

## 当前推进状态
- 当前章节：
- 当前冲突：
- 下章目标：
""",
}


REF_TEMPLATES: dict[str, str] = {
    "README.md": """# refs 使用说明

这些文件用于“细分知识”，不直接替代主文件：
- 主文件：`knowledge/characters.md`、`knowledge/worldview.md`、`knowledge/outline.md`
- 细分文件：`knowledge/refs/*.md`

建议流程：
1. 先在 refs 写细节。
2. 每个里程碑把稳定结论回填到主文件（建议每2章或30分钟）。
3. 对外以主文件为准，refs 作为证据和草稿层。
""",
    "timeline.md": """# 时间线（refs）

> 用途：记录世界观时间顺序，避免前后矛盾。主设定请同步回 `knowledge/worldview.md`。

## 书内时间轴

### T-1000（例）
- 事件：旧神陨落
- 涉及人物：魔王
- 涉及地点：万魂之渊
- 影响：世界进入失序期
- 证据章节：待补
- 状态：草案

## 写作约束
- 约束1：同一事件时间点只能有一个官方版本
- 约束2：重大时间变更必须在 `unresolved.md` 记录变更原因
""",
    "factions.md": """# 势力与组织（refs）

> 用途：沉淀组织关系网。卡片化的核心信息请回填到 `knowledge/worldview.md`。

## 条目模板

### 势力名（例：神殿）
- 立场：中立/正派/反派
- 目标：维护秩序
- 关键人物：神女
- 主要据点：圣城
- 与其他势力关系：与王庭合作、与深渊敌对
- 当前状态：活跃
- 证据章节：待补
- 备注：
""",
    "items.md": """# 关键物品（refs）

> 用途：记录道具生命周期（首次出现、归属变更、能力限制）。

## 条目模板

### 物品名（例：圣印）
- 类型：武器/法器/遗物/消耗品
- 当前持有者：
- 首次出现章节：
- 能力：
- 限制与代价：
- 已知弱点：
- 当前状态：完好/破损/遗失/封印
- 关联事件：
- 备注：
""",
    "power-system.md": """# 力量体系细则（refs）

> 用途：把规则写细，防止战力崩坏。核心结论请同步回 `knowledge/worldview.md`。

## 术语定义
- 术语：
  - 定义：
  - 可否量化：是/否
  - 证据章节：

## 规则清单
1. 规则：
   - 生效条件：
   - 失效条件：
   - 例外：
   - 代价：
   - 证据章节：

## 禁忌清单
- 禁忌：
- 触发后果：
- 可否逆转：
""",
    "glossary.md": """# 术语补充（refs）

> 用途：写作快速查词；正式术语卡片请同步到系统术语表。

## 条目模板

### 术语名
- 定义：
- 同义词/别称：
- 首次出现章节：
- 适用范围：
- 禁止误用：
- 备注：
""",
    "unresolved.md": """# 待确认设定（refs）

> 用途：收集冲突点和未决问题。确认后要回填主文件并关闭条目。

## 未决项模板

### [OPEN] 问题标题
- 冲突描述：
- 候选方案A：
- 候选方案B：
- 影响章节：
- 负责人：
- 截止章节：
- 结论：
- 状态：OPEN/RESOLVED/REJECTED

## 关闭记录
- [RESOLVED] 示例：第12章前统一“神印”叫法
""",
}


def ensure_knowledge_templates(work_dir: Path) -> list[str]:
    """
    Ensure baseline knowledge templates exist in a work directory.

    Existing files are never overwritten.
    Returns created relative paths.
    """
    created: list[str] = []
    knowledge_dir = work_dir / "knowledge"
    refs_dir = knowledge_dir / "refs"

    knowledge_dir.mkdir(parents=True, exist_ok=True)
    refs_dir.mkdir(parents=True, exist_ok=True)

    for filename, content in MAIN_TEMPLATES.items():
        target = knowledge_dir / filename
        if target.exists():
            continue
        target.write_text(content, encoding="utf-8")
        created.append(f"knowledge/{filename}")

    for filename, content in REF_TEMPLATES.items():
        target = refs_dir / filename
        if target.exists():
            continue
        target.write_text(content, encoding="utf-8")
        created.append(f"knowledge/refs/{filename}")

    if created:
        logger.info("[knowledge_templates] created %d template files under %s", len(created), work_dir)
    return created
