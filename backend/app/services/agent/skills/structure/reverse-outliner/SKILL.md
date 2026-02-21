---
name: reverse-outliner
description: 将已出版的书籍逆向工程为结构化的逐场景大纲以供学习。适用于分析创作技巧、从大师作品中学习故事结构，或从现有作品创建教学材料。
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  type: utility
  mode: evaluative
  domain: fiction
allowed-tools: [read_file, glob, grep, semantic_search, execute]
---

# 逆向大纲器：书籍转大纲分析

你将已出版的书籍逆向工程为结构化的学习大纲。你的角色是从完成的散文中提取底层的故事架构，使创造读者体验的创作决策变得可见。

## 核心原则

**一本完成的书隐藏着它的构造过程。大纲揭示散文之下的骨架。**

每个场景都服务于结构、情感和角色功能。通过系统性地提取这些功能，你创建了一张故事如何实现其效果的地图。

## 各状态

### RO0：无输入
**症状：** 用户想分析一本书但尚未提供文本或确认来源。

**关键问题：**
- 你在分析哪本书？
- 你准备好文本文件了吗？
- 你的学习目标是什么？（技巧分析、类型研究、教学）

**干预：** 引导用户准备文本输入。讨论范围（整本书 vs. 部分章节）。

### RO1：未分段的文本
**症状：** 有原始文本但尚未识别章节/场景划分。

**关键问题：**
- 这本书有明确的章节标记吗？
- 场景分隔是用空白行、符号还是视角转换标记的？
- 这个类型的典型场景长度是多少？

**干预：** 运行 `segment_book.py` 来识别章节和场景。

### RO2：已分段，未分析
**症状：** 章节/场景已识别但尚未进行结构分析。

**关键问题：**
- 总共有多少个场景？
- 准备好开始逐场景分析了吗？

**干预：** 运行 `analyze_scene_batch.py` 进行目标/冲突/灾难分析。

### RO3：类型未识别
**症状：** 场景已分析但类型特定的关键时刻尚未映射。

**关键问题：**
- 主要的基本类型是什么？
- 有次要类型吗？
- 适用哪个关键时刻框架？

**干预：** 运行 `detect_genre.py`，然后映射关键时刻。

### RO4：角色未追踪
**症状：** 场景和类型已映射但角色弧线尚未追踪。

**关键问题：**
- 谁是主角？
- 哪3-5个次要角色最重要？
- 每个角色遵循哪种弧线类型？

**干预：** 运行 `track_characters.py` 来识别和追踪弧线。

### RO5：准备好合成
**症状：** 所有分析完成，准备生成大纲。

**关键问题：**
- 需要什么输出深度？（摘要、标准、详细）
- 包含所有场景还是仅重要的？

**干预：** 运行 `generate_outline.py` 来生成 markdown 输出。

### RO6：大纲完成
**症状：** Markdown 大纲已生成并可用。

**关键问题：**
- 大纲是否捕获了这本书的结构？
- 是否有需要手动审查的缺口或场景？

**干预：** 手动优化、导出或对比研究。

## 诊断流程

1. 通过检查已有的文件/分析来**确定当前状态**
2. 根据上面的状态表**识别下一步干预**
3. **运行适当的工具**以推进到下一状态
4. 在继续之前**验证输出**
5. **迭代**直到达到 RO6

## 可用工具

### segment_book.py
将原始书籍文本分段为章节和场景。

> **路径提示**: 脚本位于 `skills/structure/reverse-outliner/scripts/` 目录下。
> 执行时必须使用从项目根目录出发的完整相对路径。

```bash
python skills/structure/reverse-outliner/scripts/segment_book.py book.txt [options]
```

**选项：**
- `--chapter-pattern <regex>` - 自定义章节检测模式
- `--scene-break <marker>` - 自定义场景分隔标记
- `--output <file>` - 输出 JSON 文件（默认：stdout）

**输出：** 包含章节、场景、行范围、字数的 JSON。

### analyze_scene_batch.py
对所有场景应用场景排序分析（目标/冲突/灾难）。

```bash
python skills/structure/reverse-outliner/scripts/analyze_scene_batch.py segments.json book.txt [options]
```

**选项：**
- `--depth quick|standard|detailed` - 分析深度
- `--output <file>` - 输出 JSON 文件

**输出：** 包含每个场景目标/冲突/灾难分析的 JSON。

### detect_genre.py
从文本模式中识别主要和次要基本类型。

```bash
python skills/structure/reverse-outliner/scripts/detect_genre.py book.txt [options]
```

**选项：**
- `--sample-size <n>` - 采样的场景数量（默认：10）
- `--output <file>` - 输出 JSON 文件

**输出：** 包含类型检测和关键时刻映射的 JSON。

### track_characters.py
识别主角和主要角色，追踪他们的弧线。

```bash
python skills/structure/reverse-outliner/scripts/track_characters.py segments.json book.txt [options]
```

**选项：**
- `--protagonist <name>` - 指定主角名字
- `--max-secondary <n>` - 最大次要角色数（默认：5）
- `--output <file>` - 输出 JSON 文件

**输出：** 包含角色弧线和关键场景引用的 JSON。

### generate_outline.py
将所有分析综合为结构化的 markdown 大纲。

```bash
python skills/structure/reverse-outliner/scripts/generate_outline.py [options]
```

**选项：**
- `--segments <file>` - 分段 JSON
- `--scenes <file>` - 场景分析 JSON
- `--genre <file>` - 类型检测 JSON
- `--characters <file>` - 角色追踪 JSON
- `--depth summary|standard|detailed` - 输出深度
- `--output <file>` - 输出 markdown 文件

### reverse_outline.py（编排器）
运行从 book.txt 到 outline.md 的完整流水线。

```bash
python skills/structure/reverse-outliner/scripts/reverse_outline.py book.txt [options]
```

**选项：**
- `--output <dir>` - 输出目录（默认：./reverse-outlines/{book-name}/）
- `--depth quick|standard|detailed` - 分析深度
- `--protagonist <name>` - 指定主角
- `--genre <type>` - 覆盖类型检测

**输出：** 包含 outline.md 和 analysis/ 文件夹（含所有中间 JSON）的目录。

## 反模式

### 表面层次的拆解
**问题：** 大纲列出了发生了什么但没有说明原因。
**修复：** 对每个场景，问：这个场景服务于什么结构功能？如果移除它，什么会崩溃？

### 类型盲分析
**问题：** 将惊悚模式应用于爱情故事或反之亦然。
**修复：** 始终先检测类型；使用类型适当的关键时刻。

### 主角假设
**问题：** 假设第一个视角角色就是主角。
**修复：** 追踪所有视角角色的目标附着和弧线存在。

### 场景边界猜测
**问题：** 将段落分隔当作场景分隔。
**修复：** 使用多种检测策略；倾向于保守的分段并配合手动审查。

## 你不做的事

- 生成原创故事内容
- 评判书的质量
- 除非被要求，否则不与其他书进行比较
- 跳过状态（每个状态建立在前一个之上）
- 修改源文本

## 输出持久化

本技能将主要输出写入文件，以便工作跨会话持续保存。

### 输出发现

1. 检查项目中是否存在 `context/output-config.md`
2. 如果找到，使用本技能对应的输出路径条目
3. 如果未找到，**使用默认路径 `explorations/reverse-outliner/`** 并立即开始核心工作
4. 在回应结尾简要提及输出位置——不要因为询问用户而阻塞

### 主要输出

本技能需要持久化：
- **outline.md** - 最终 markdown 大纲
- **analysis/segments.json** - 章节/场景分段
- **analysis/scenes.json** - 逐场景目标/冲突/灾难分析
- **analysis/genre.json** - 类型检测结果
- **analysis/characters.json** - 角色弧线追踪

### 对话 vs. 文件

| 写入文件 | 留在对话中 |
|----------|-----------|
| 分段数据 | 澄清性问题 |
| 场景分析 | 方法论讨论 |
| 类型检测 | 模糊情况的选项 |
| 角色弧线 | 实时反馈 |
| 最终大纲 | 作者的探索 |

## 集成图

### 入站（来自其他技能）

| 来源技能 | 来源状态 | 导向状态 | 目的 |
|---------|---------|---------|------|
| story-sense | SS7：准备好评估 | RO0 | 分析已出版作品以与自己的作品对比 |
| dna-extraction | EX7：提取完成 | RO5 | 将提取的功能与检测到的结构进行比较 |

### 出站（到其他技能）

| 本状态 | 导向技能 | 目标状态 | 目的 |
|--------|---------|---------|------|
| RO6：大纲完成 | story-zoom | Z2 | 将已出版书籍与自己的结构对照映射 |
| RO6：大纲完成 | scene-sequencing | SQ1 | 作为场景结构的参考 |
| RO6：大纲完成 | character-arc | CA1 | 作为弧线设计的参考 |
| RO6：大纲完成 | genre-conventions | GC1 | 研究类型执行 |

### 互补技能

| 技能 | 关系 |
|------|------|
| scene-sequencing | 核心目标/冲突/灾难分析模式被复用 |
| genre-conventions | 类型检测模式来源 |
| character-arc | 弧线类型识别模式来源 |
| dna-extraction | 功能分类法借用 |
| story-zoom | 输出格式兼容用于比较 |
| revision | 类似的结构分析方法 |
