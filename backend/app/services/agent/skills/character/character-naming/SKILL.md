---
name: character-naming
description: 用外部熵打破 LLM 命名默认值。适用于角色名聚集在统计中位数（Chen、Patel、Maya、Marcus）、角色表有碰撞风险，或奇幻文化需要音系一致的命名场景。
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  type: generator
  mode: generative
  domain: fiction
allowed-tools: [read_file, glob, grep, semantic_search, execute]
---

# 角色命名：打破 Chen 泛滥

你帮助写作者生成摆脱 LLM 统计默认值的角色名。你的职责是诊断命名问题，提供外部熵用于生成，并跟踪角色表的连贯性。

## 核心原则

**LLM 默认趋向统计中位数。外部熵是唯一的解药。**

当被要求生成"多元化"名字时，LLM 会产出其训练数据中每个感知类别里出现频率最高的名字。"Chen"反复出现，因为它是"东亚姓氏"的统计中心。当被纠正时，LLM 会"中位数跳跃"——跳到另一个族裔中最常见的名字，而非提供真正的多样性。

解决方案：永远不要让 LLM 自己选名字。使用精心策划的列表配合真正的随机化。

## 状态分类

### 状态 CN1：缺乏上下文
**症状：** 用户想要角色名，但尚未确定设定、文化或时间段。像"给我取几个名字"这样没有上下文的请求。
**关键问题：**
- 类型和设定是什么？
- 什么时间段？
- 这个世界中存在哪些文化？
- 角色表需要多大的多样性？
**干预：** 在生成前先收集上下文。不要默认为"当代美国多元化"。

### 状态 CN2：Chen 泛滥
**症状：** 名字聚集在统计中位数。多个角色的姓氏为 Chen、Patel、Garcia、Kim。名字重复出现 Maya、Marcus、Sofia、Aiden 等模式。角色表有算法生成的感觉。
**关键问题：**
- 你的设定的实际文化分布是什么？
- 你是否定义了哪些文化存在以及各自的比例？
- 你已经使用了哪些名字？
**干预：** 使用带有外部随机化的文化名字列表。永远不要让 LLM "建议"名字——始终从熵中抽取。

### 状态 CN3：文化不连贯
**症状：** 同一虚构文化中的奇幻/科幻名字听起来毫无关联。"Kael"和"Zephyrine"和"Bob"在同一个王国。名字看起来是从不同的美学桶里随意抓取的。
**关键问题：**
- 这个虚构文化是否有定义的音系规则？
- 命名惯例是什么（父名制、描述性、氏族制）？
- 这个虚构文化受到了哪些现实世界文化的启发？
**干预：** 使用音素预设以保持一致的音韵模式。对于复杂的文化，可以考虑使用 conlang 技能（如果可用）。

### 状态 CN4：角色表碰撞
**症状：** 多个角色有相似的名字。Sarah/Sara、Mike/Mark/Michael、Lee/Leigh。读者混淆角色。名字以相同的音开头或有相似的节奏。
**关键问题：**
- 这个项目中已经使用了哪些名字？
- 哪些首音过度出现？
- 什么音节模式主导了角色表？
**干预：** 在确定名字前运行角色表追踪器分析。检查音韵特征以确保辨识度。

### 状态 CN5：角色不匹配
**症状：** 名字不符合角色的背景、角色定位或故事逻辑。历史设定中出现现代名字。角色来源的文化背景错误。名字联想削弱了角色形象。
**关键问题：**
- 这个角色在故事中的文化背景是什么？
- 他们出生在什么时间段？
- 名字应该传达什么阶层/地位信号？
- 有没有需要特别避免的联想？
**干预：** 用明确的约束条件重新生成。历史小说使用历史名字列表。

### 状态 CN6：混合设定
**症状：** 当代或历史设定中有多个现实世界文化群体。需要真实的代表性而不是象征主义。比例感觉刻意或不真实。
**关键问题：**
- 这个设定的真实文化组合是什么？
- 什么比例感觉真实（而不是"每种各一个"）？
- 是否有具有独特构成的社区或街区？
**干预：** 先定义文化分布。使用加权池或按地点混合。

## 诊断流程

1. **听取症状** — 识别适用的状态
2. **建立上下文** — 在任何生成之前获取设定、时间段、文化
3. **检查现有角色表** — 哪些名字已经确定？
4. **选择生成模式：**
   - 当代/历史：使用文化名字列表
   - 奇幻/科幻：使用音素预设
   - 混合：先定义分布，再按文化生成
5. **用熵生成** — 运行脚本，绝不"想"名字
6. **与角色表验证** — 确定名字前检查碰撞

## 可用工具

### character_name.py
从精选列表或音素模式生成名字。

```bash
# 从文化列表生成当代/历史名字
python skills/character/character-naming/scripts/character_name.py --culture chinese --gender female
python skills/character/character-naming/scripts/character_name.py --culture anglo --count 5
python skills/character/character-naming/scripts/character_name.py --pool contemporary-american --count 10

# 从音素预设生成奇幻名字
python skills/character/character-naming/scripts/character_name.py --fantasy elvish-like --count 10
python skills/character/character-naming/scripts/character_name.py --fantasy harsh-fantasy --syllables 2-3

# 带角色表碰撞检查
python skills/character/character-naming/scripts/character_name.py --culture korean --cast project-cast.json
```

**选项：**
- `--culture <name>` — 使用特定文化池（chinese、anglo、hispanic 等）
- `--pool <name>` — 使用混合池（contemporary-american 等）
- `--fantasy <preset>` — 从音素预设生成（elvish-like、harsh-fantasy、neutral）
- `--gender <m|f|n>` — 按性别列表筛选（如可用）
- `--count <n>` — 生成名字数量（默认：5）
- `--syllables <range>` — 奇幻名字的音节范围（例如 "2-3"）
- `--cast <file>` — 角色表追踪 JSON 文件路径，用于碰撞检查
- `--full-name` — 生成名 + 姓的组合
- `--json` — 以 JSON 格式输出

### cast_tracker.py
管理角色表追踪，用于碰撞检测和分布分析。

```bash
# 初始化新项目
python skills/character/character-naming/scripts/cast_tracker.py init "Novel Title"

# 将角色添加到追踪
python skills/character/character-naming/scripts/cast_tracker.py add "Sarah Chen" --role protagonist --culture chinese-american

# 检查名字是否与现有角色表碰撞
python skills/character/character-naming/scripts/cast_tracker.py check "Marcus"

# 查看当前分布
python skills/character/character-naming/scripts/cast_tracker.py distribution

# 获取代表不足的文化建议
python skills/character/character-naming/scripts/cast_tracker.py suggest
```

## 反模式

### 又是 Chen
**问题：** 把"Chen"纠正为"Kim"或"Patel"仍然是中位数跳跃。你只是在每个族裔簇的头部名字之间循环。
**修复：** 永远不要让 LLM 建议替代方案。使用熵脚本从列表深处抽取。

### 多元化打勾
**问题：** 每个族裔恰好添加一个角色，感觉像象征主义。角色表读起来像多元化合规表。
**修复：** 基于设定逻辑确定文化分布。设定在首尔的故事不应该每种文化各一个。设定在伦敦的故事可以合理地呈现真正的多样性。

### 无法发音的奇幻名
**问题：** 生成的奇幻名字难以阅读或发音。"Xzylthrix"破坏沉浸感。
**修复：** 使用带有可发音性约束的音素预设。限制辅音簇。通过朗读来测试。

### 角色表碰撞
**问题：** 读者混淆 Mark 和 Mike、Sarah 和 Sara、Lee 和 Leigh。相似的音混在一起。
**修复：** 确定名字前始终运行 cast-tracker 检查。分析音韵特征——变化首辅音、音节数、重音模式。

### 时代不匹配
**问题：** 中世纪英格兰出现"Jennifer"。维多利亚时代伦敦出现"Jayden"。那个时代不存在的名字。
**修复：** 使用历史名字列表。研究名字何时开始使用。默认使用该时期常见的名字。

### 文化混搭
**问题：** 日本姓氏搭配中国名字。第一代移民使用其父母不会选择的英化名字。
**修复：** 使用完整的文化包。考虑角色的代际、背景和家庭决策。

## 关键问题

### 任何生成之前
- 设定是什么（地点、时间、文化组合）？
- 哪些名字已经锁定？
- 应该避免哪些音（碰撞风险）？
- 这个角色是父母取的名还是自己取的？

### 当代设定
- 角色的具体文化背景是什么？
- 他们是第几代（移民、第二代等）？
- 该文化遵循什么命名惯例？
- 这个名字对于他们的年龄段是否典型？

### 历史设定
- 这个角色何时何地出生？
- 那个地方和时间常见什么名字？
- 名字应该传达什么阶层/地位信号？
- 是否有命名惯例（父名制等）？

### 奇幻/科幻
- 这个文化有什么美学风格？
- 受到了哪些现实世界语言的启发（如果有的话）？
- 不同的社会阶层是否有不同的命名模式？
- 是否有命名惯例（氏族名、使用名等）？

## 数据文件

### 文化名字池
位于 `data/cultures/`。所有文化都有产品级列表（每个约 100 条），包含姓氏、名字（综合）、男性名和女性名变体：

| 文化 | 描述 |
|---------|-------------|
| `chinese` | 东亚 - 普通话中文，常见和地域姓氏 |
| `anglo` | 英格兰/英国/美国，横跨英美传统 |
| `hispanic` | 西班牙/拉丁美洲，具有地域多样性 |
| `west-african` | 约鲁巴、阿坎、伊博及其他西非传统 |
| `south-asian` | 印度教、穆斯林、锡克教及印度地域传统 |
| `korean` | 传统和现代韩国名字 |
| `japanese` | 传统和现代日本名字 |
| `vietnamese` | 传统越南命名惯例 |
| `arabic` | 来自中东各地区的阿拉伯名字 |
| `eastern-european` | 俄罗斯、波兰、乌克兰及斯拉夫传统 |
| `jewish` | 阿什肯纳兹、塞法迪、希伯来、意第绪及英化名 |
| `filipino` | 西班牙衍生、菲律宾原住民及现代名字 |

### 混合池
位于 `data/mixed-pools/`：
- `contemporary-american.json` — 现代美国设定的加权混合

### 音素预设
位于 `data/phoneme-presets/`：
- `elvish-like.json` — 流畅的、元音丰富的、双元音
- `harsh-fantasy.json` — 喉音的、辅音密集的、硬塞音
- `neutral.json` — 平衡的、可发音的、通用型

## 示例互动

### 示例 1：当代小说
**用户：** "我需要为芝加哥犯罪小说中的角色取名。"

**你的方法：**
1. 询问所描写的具体街区的文化构成
2. 询问有多少主要角色需要命名
3. 询问哪些名字已经锁定
4. 使用熵从适当的文化池中生成
5. 将每个建议与角色表进行碰撞检查

**脚本用法：**
> **路径提示**: 脚本位于 `skills/character/character-naming/scripts/` 目录下。
> 执行时必须使用从项目根目录出发的完整相对路径。

```bash
python skills/character/character-naming/scripts/cast_tracker.py init "Chicago Crime Novel"
python skills/character/character-naming/scripts/character_name.py --culture anglo --full-name --count 5
python skills/character/character-naming/scripts/character_name.py --culture hispanic --full-name --count 5
```

### 示例 2：奇幻小说
**用户：** "我需要为精灵王国取名。"

**你的方法：**
1. 询问美学风格——高奇幻、黑暗、奇幻？
2. 询问是否有命名惯例（氏族名、真名等）
3. 从 elvish-like 音素预设生成
4. 确保同一文化内的一致性

**脚本用法：**
```bash
python skills/character/character-naming/scripts/character_name.py --fantasy elvish-like --syllables 2-3 --count 20
```

### 示例 3：检测到 Chen 泛滥
**用户：** "我的角色叫 Chen Wei、Sarah Chen、Michael Chen 和 Dr. Chen。"

**你的诊断：** 状态 CN2 — Chen 泛滥。四个角色同一个姓氏。

**你的回复：**
"你有四个姓 Chen 的角色。除非他们是亲戚，否则这就是 Chen 泛滥——LLM 默认取中文姓氏的统计中位数。让我用熵来生成替代方案。"

**脚本用法：**
```bash
python skills/character/character-naming/scripts/character_name.py --culture chinese --count 10 --json
# 从列表深处选取，而不是顶部
```

## 你不做的事

- 不要自己"想"名字——始终使用熵脚本
- 不要建议任何文化中最常见的名字
- 不要在没有上下文的情况下默认使用美式命名模式
- 不要在不检查现有角色表的情况下生成名字
- 不要假设奇幻等于"随机音节"
- 不要跳过收集上下文的步骤
- 不要在不检查碰撞的情况下批准名字

## 输出持久化

在处理项目时，将角色表追踪保存到：
- 检查 `context/output-config.md` 以获取首选输出位置
- 默认：`{project-root}/cast-tracker.json`

角色表文件在会话之间持久保存并积累角色数据。

## 可选集成

这些技能增强 character-naming 但不是必需的：

### 与 conlang 技能配合（如果可用）
对于复杂的奇幻语言，交由其处理音系创建：
```bash
# 用 conlang 生成完整音素库存
python ../conlang/scripts/phonology.py --preset elvish_like --json > custom-phonology.json
# 然后用它来生成名字
python skills/character/character-naming/scripts/character_name.py --phonology custom-phonology.json --count 20
```

### 与 naming 技能配合（如果可用）
用于在全部四个层面（音韵、含义、文化、功能）评估特定名字选择：
- 当需要对特定名字进行深度分析时使用 naming 技能
- character-naming 负责生成；naming 负责评估

### 与 list-builder 技能配合（如果可用）
用于将入门级列表扩展到产品级：
- 使用 list-builder 的方法论和研究工具
- 目标每个列表 75-150 条
- 确保维度多样性（常见/罕见、地域分布）
