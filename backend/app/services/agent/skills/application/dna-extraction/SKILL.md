---
name: dna-extraction
description: 从现有作品（电视、电影、书籍、戏剧）中提取功能DNA。适用于改编源作品、分析作品成功要素、创建可复用的类型模式图谱，或需要区分结构必要性与风格选择时。
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  type: utility
  mode: evaluative
  domain: fiction
allowed-tools: [read_file, glob, grep, semantic_search, execute]
---

# DNA提取：面向改编的功能分析

你帮助从现有作品中提取功能DNA。你的角色是识别作品运作的机制——不是表面元素，而是在改编中可以保留的底层结构、关系和情感机制。

## 核心原则

**改编时的第一反应是表面元素。功能DNA是那些元素所做的事，而非它们是什么。**

哈姆雷特的王子身份不是DNA——它是一种形式。DNA是：
- "主角接近权力中心但不是权力持有者"
- "主角有与个人欲望冲突的结构性义务"
- "主角有内部人的途径观察他们无法采取行动的腐败"

## 状态

### 状态 EX0：未提取
**症状：**作品已确定但未开始分析。用户说"我想改编X"但没有分析X为什么有效。
**关键问题：**
- 我们从什么作品提取？
- 源作品是什么媒介？（影响提取方式）
- 你的提取目标是什么？（改编、类型映射、分析）
**干预措施：**从情感核心识别开始。使用 genre-conventions 技能识别主要/次要类型。

### 状态 EX1：表面阅读
**症状：**分析聚焦于发生了什么，而非为什么有效。"这是关于一个看到鬼魂的王子。"情节概述而非功能识别。用户混淆了事件和功能。
**关键问题：**
- 这个元素为什么存在？
- 如果我们移除它，什么会坏掉？
- 因为这个元素，观众感受到什么？
- 这是作品所是的，还是作品所做的？
**干预措施：**四轴功能提取。对每个元素应用"功能而非形式"的重构。

### 状态 EX2：单轴提取
**症状：**只为情节或角色或主题提取功能。缺少互联性。"鬼魂提供了启动事件。"（没错，但不完整——角色功能呢？情感功能呢？关系功能呢？）
**关键问题：**
- 这个元素还服务于什么其他功能？
- 它与角色弧线有什么联系？
- 它满足了什么类型承诺？
- 它创造或复杂化了什么关系？
**干预措施：**多轴检查清单。与 genre-conventions 技能交叉参考。强制在所有六个轴上提取。

### 状态 EX3：缺失情感核心
**症状：**功能已提取但不清楚作品创造了什么情感体验。机械分析缺乏类型承诺。能描述情节功能但不能描述观众感受。
**关键问题：**
- 观众在体验这部作品时感受到什么？
- 这部作品传递了哪些基本类型？
- 情感高峰和低谷在哪里？
- 喜爱这部作品的人会说他们为什么喜爱它？
**干预措施：**genre-conventions 整合。使用 `emotional_beat_map.py` 进行情感节拍映射。主要/次要类型识别。

### 状态 EX4：结构/风格混淆
**症状：**分析将风格选择当作结构必要性。莎士比亚的语言被当作结构性的，而它是风格性的。时代背景被当作必需的，而它是可改编的。
**关键问题：**
- 如果我们改变这个，故事会坏掉吗？
- 这对功能来说是本质的还是形式的特征？
- 另一种形式能服务于相同功能吗？
- 不同的背景会使这不可能吗？
**干预措施：**使用 `structural_stylistic.py` 进行结构/风格分类。对每个元素测试"故事还能运作吗？"标准。

### 状态 EX5：缺失关系
**症状：**提取了单个角色功能但没有提取关系动态。"哈姆雷特犹豫不决"而没有"克劳狄斯代表了哈姆雷特如果行动可能变成的样子。"角色被孤立分析。
**关键问题：**
- 这个角色对其他角色意味着什么？
- 这段关系强迫了什么选择？
- 如果这段关系不存在，会失去什么？
- 角色如何通过对比来定义彼此？
**干预措施：**关系功能映射。角色网络分析。识别镜像对及其揭示的内容。

### 状态 EX6：没有层级
**症状：**一切被同等对待。无法区分承重元素和可移除细节。每个场景、角色、支线都被赋予同等权重。
**关键问题：**
- 哪些功能是主要的（没有它们故事会坏掉）？
- 哪些是加强的（没有它们故事会减弱）？
- 哪些是可选的风味（好但非必需）？
- 最小可行提取是什么？
**干预措施：**功能层级分类。影响评分。识别哪3-5个元素是真正不可妥协的。

### 状态 EX7：提取完成
**症状：**综合提取文档已存在。多层级功能已识别。情感核心清晰。结构/风格已分离。层级已建立。聚类链接已记录。
**关键问题：**
- 这个提取是否完整到足以生成新作品？
- 是否有会导致合成失败的缺口？
- 你是否对照情感体验进行了验证？
- 是否识别了聚类链接？
**干预措施：**验证清单。转交给 adaptation-synthesis 技能。

## 六轴提取

对每个故事元素，在所有六个轴上提取功能：

| 轴 | 问题 | 揭示什么 |
|----|------|---------|
| **形式** | 它是什么？ | 表面元素（可改编的容器） |
| **结构功能** | 它在情节中实现了什么？ | 故事机制，因果链 |
| **角色功能** | 它在角色旅程中实现了什么？ | 弧线需求，转变催化剂 |
| **情感功能** | 它让观众感受到什么？ | 类型承诺交付，情感节拍 |
| **主题功能** | 它探索了什么思想？ | 意义，问题，共鸣 |
| **关系功能** | 它在元素之间创造了什么动态？ | 连接网络，对比，张力 |

## 语气和声音提取

除了结构功能之外，作品还有定义其感觉的独特语调签名。单独提取这些：

### 语调寄存器

| 寄存器 | 描述 | 示例 |
|--------|------|------|
| **真诚度** | 真挚 vs. 反讽/疏离 | Killjoys：尽管有幽默但真诚度高。Bebop：用冷漠掩饰痛苦 |
| **幽默模式** | 喜剧如何运作 | 对白交锋（Killjoys）、冷面笑匠（Bebop）、肢体喜剧（成龙）、黑色幽默（绝命毒师） |
| **情感表达** | 感情如何呈现 | 直接陈述、潜台词密集、行动揭示情感、否认/转移 |
| **对话密度** | 对话与行动比例 | 俏皮/快速连珠炮 vs. 稀疏/有分量的沉默 |
| **冲突风格** | 角色如何争斗 | 言语交锋、冷漠沉默、爆发、被动攻击 |

### 需要提取的声音模式

**角色声音独特性：**
- 角色听起来是否彼此不同？
- 什么说话模式标记每个角色？（行话、正式度、句子长度）
- 角色如何通过对话揭示与隐藏？

**对话功能：**
- 信息传递（说明文处理）
- 关系表达（连接如何在言语中体现）
- 冲突升级（争论如何构建）
- 潜台词密度（说的 vs. 意思的）

**语调一致性：**
- 语调是否在场景/集之间转变？如何转变？
- 什么触发了语调转变？
- 是否有锚定作品的基调？

### 示例：Killjoys vs. Cowboy Bebop 语调提取

| 元素 | Killjoys | Cowboy Bebop |
|------|----------|--------------|
| 真诚度 | 高——角色言出必行 | 低——反讽距离掩饰脆弱 |
| 幽默 | 对白交锋、俏皮话、戏谑对抗 | 冷面、荒诞、忧郁喜剧 |
| 情感表达 | 直接——"我爱你，混蛋" | 转移——通过行动展示，而非言语 |
| 对话密度 | 高——不断的言语交锋 | 变化——大量沉默被稀疏台词打断 |
| 冲突风格 | 大声、直接、快速解决 | 回避、缓慢酝酿、常常未解决 |

两者都服务于"赏金猎人科幻"的结构功能，但因为语调选择而感觉完全不同。

### 示例：哈姆雷特中的鬼魂

| 轴 | 提取 |
|----|------|
| 形式 | 被谋杀父亲的超自然显灵 |
| 结构 | 提供主角无法验证的特权信息；创造启动义务 |
| 角色 | 迫使哈姆雷特面对不可能的责任；代表被腐败者取代的理想化父亲 |
| 情感 | 揭露时的恐惧；义务的不安；对可靠性的不确定 |
| 主题 | 质疑证词的可靠性；探索对死者的责任；引入超自然/道德的不确定性 |
| 关系 | 创造哈姆雷特-克劳狄斯动态（秘密知识）；创造哈姆雷特-格特鲁德张力（她不知道） |

## 提取深度级别

| 深度 | 范围 | 使用场景 |
|------|------|---------|
| **快速** | 核心功能，主要类型，3-5个关键角色 | 探索，比较多部作品，可行性检查 |
| **标准** | 完整六轴提取，关系，情节结构 | 大多数改编项目 |
| **详细** | 节拍级映射，集结构，语调变化，对话模式 | 严肃的长篇改编，学术分析 |

使用提取工具时用 `--depth quick|standard|detailed`。

## 诊断流程

1. **确定来源** - 什么作品？什么媒介？你的目标是什么？
2. **映射情感体验** - 什么类型？观众感受到什么？什么时候？
3. **列出主要元素** - 角色、背景、情节结构、关系
4. **对每个元素，提取功能** - 跨所有六个轴
5. **分类结构 vs. 风格** - 什么必须保留？什么可以改变？
6. **构建层级** - 主要功能、加强功能、可选功能
7. **识别聚类** - 这属于什么类型模式？
8. **验证完整性** - 有人能从这个合成新作品吗？
9. **生成DNA文档** - 用于合成的结构化输出

## 关键问题

### 用于情感核心
- 喜爱这部作品的人喜爱什么？
- 它做出了什么类型承诺？是否交付了？
- 情感高点在哪里？低点在哪里？
- 什么会背叛观众的期望？

### 用于角色功能
- 这个角色相信什么谎言？（character-arc 整合）
- 他们想要什么 vs. 他们需要什么？
- 他们经历了什么转变？
- 他们与谁形成对比？对比揭示了什么？

### 用于结构功能
- 如果我们移除这个，什么会坏掉？
- 这传达了什么信息？给谁？什么时候？
- 这为故事后面的什么提供了支撑？
- 这是原因还是结果？

### 用于可改编性
- 这是特定于背景的，还是普遍的？
- 这个功能能被不同的形式服务吗？
- 什么是本质的 vs. 什么是特征性的？
- 其他作品如何以不同方式服务于类似功能？

## 反模式

### 情节概述陷阱
**模式：**提取读起来像附了"功能"标签的情节概述。
**问题：**混淆事件和目的。"鬼魂出现并揭露了谋杀"不是功能。
**修正：**对每个元素，强制提问"这实现了什么？"而非"这做了什么？"
**检测：**如果你的提取可以由一个不理解作品的人写出来，那就太表面了。

### 偏爱元素偏差
**模式：**从喜爱的元素过度提取，而对其他元素提取不足。
**问题：**创造了强调分析者喜欢什么而非作品需要什么的不平衡提取。
**修正：**强迫自己从你觉得无聊或烦人的元素中提取功能。
**检测：**如果提取深度在元素之间差异很大且没有理由，就存在偏差。

### 一切皆必需陷阱
**模式：**将所有元素标记为结构必需以避免艰难决定。
**问题：**创造不可用的提取——如果一切都是必需的，什么都无法改编。
**修正：**强制层级。哪5件事不能改变？然后下5件是什么？
**检测：**如果你的"可改编"列表比"必需"列表短，你可能是错的。

### 形式即功能混淆
**模式：**把具体形式当作功能。"剑斗的功能是有一场剑斗。"
**问题：**使改编变得不可能，因为你看不透表面。
**修正：**问"如果我们移除这个会发生什么？"答案揭示功能。
**检测：**如果你的功能描述包含元素的名称，你在描述形式而非功能。

## 可用工具

### extract_functions.py
逐元素提取的交互式问卷。引导完成六轴分析。


> **路径提示**: 脚本位于 `skills/application/dna-extraction/scripts/` 目录下。
> 执行时必须使用从项目根目录出发的完整相对路径。

```bash
# Start extraction session
python skills/application/dna-extraction/scripts/extract_functions.py "Hamlet"

# Extract at specific depth
python skills/application/dna-extraction/scripts/extract_functions.py "Killjoys" --depth quick

# Extract specific element
python skills/application/dna-extraction/scripts/extract_functions.py --element "The Ghost"

# Validate existing extraction
python skills/application/dna-extraction/scripts/extract_functions.py --validate extraction.json
```

### emotional_beat_map.py
映射作品时间线上的情感高峰/低谷。

```bash
# Generate beat map template
python skills/application/dna-extraction/scripts/emotional_beat_map.py "Hamlet" --acts 5

# For episodic work
python skills/application/dna-extraction/scripts/emotional_beat_map.py "Killjoys S1" --episodes 10

# Compare against genre expectations
python skills/application/dna-extraction/scripts/emotional_beat_map.py --compare drama,thriller
```

### structural_stylistic.py
用于将元素分类为结构性（必须保留）vs 风格性（可以改编）的清单。

```bash
# Classification questionnaire
python skills/application/dna-extraction/scripts/structural_stylistic.py "royal court setting"

# Batch classification
python skills/application/dna-extraction/scripts/structural_stylistic.py --file elements.json
```

## DNA文档输出

提取保存到链接网络：

```
{project}/dna-library/
├── extractions/          # 作品特定的提取
│   ├── hamlet.json
│   └── killjoys.json
├── clusters/             # 类型聚类文档
│   └── bounty-hunter-scifi.json
└── syntheses/            # 生成的合成计划
    └── my-project.json
```

### 作品提取模式

```json
{
  "_meta": {
    "type": "work-extraction",
    "source_work": "Hamlet",
    "source_author": "William Shakespeare",
    "source_medium": "stage play",
    "extraction_date": "2025-01-15",
    "extraction_depth": "standard",
    "clusters": ["revenge-tragedy", "political-drama"]
  },
  "emotional_core": {
    "primary_genre": "drama",
    "secondary_genres": ["thriller", "horror"],
    "emotional_experience": "The dread of knowing truth but being unable to act",
    "emotional_beats": [
      {"position": 0.05, "emotion": "unease", "element": "Guards report ghost"},
      {"position": 0.15, "emotion": "horror/obligation", "element": "Ghost reveals murder"}
    ]
  },
  "tone": {
    "sincerity_level": "high",
    "humor_mode": "dark/ironic",
    "emotional_expression": "soliloquy-heavy, internal made external",
    "dialogue_density": "high - language-forward",
    "conflict_style": "verbal sparring, passive aggression, delayed explosion",
    "baseline_tone": "melancholic brooding punctuated by dark wit",
    "tonal_shifts": [
      {"trigger": "players arrive", "shift": "lightens temporarily"},
      {"trigger": "Ophelia's death", "shift": "pure tragedy"}
    ]
  },
  "characters": {
    "hamlet": {
      "form": "Prince of Denmark",
      "functions": {
        "structural": ["Proximity to power without holding it"],
        "character": ["Lie: I can know truth absolutely before acting"],
        "emotional": ["Audience vehicle for knowing-but-not-acting"],
        "thematic": ["Embodies question: Is certainty possible?"],
        "relational": ["To Claudius: corrupt mirror of what he could become"]
      },
      "structural_necessity": "high",
      "adaptable_elements": ["royal status", "gender", "era", "name"]
    }
  },
  "plot_structures": {},
  "relationships": {},
  "structural_requirements": ["Protagonist must have privileged info others lack"],
  "adaptable_without_breaking": ["Royal status", "Era", "Ghost mechanism"],
  "links": {
    "clusters": ["revenge-tragedy.json"],
    "similar_works": [],
    "derived_syntheses": []
  }
}
```

### 类型聚类模式

```json
{
  "_meta": {
    "type": "trope-cluster",
    "cluster_name": "bounty-hunter-scifi",
    "description": "Episodic bounty/warrant structure in sci-fi setting"
  },
  "core_functions": {
    "structural": ["Case-of-the-week provides episodic entry points"],
    "character": ["Found family dynamics among crew"],
    "emotional": ["Competence satisfaction"]
  },
  "required_elements": ["Mission structure", "Mobile base", "Team with complementary skills"],
  "variance_axes": [
    {"axis": "tone", "range": ["noir/melancholic", "action/humor"]}
  ],
  "source_works": ["killjoys.json", "cowboy-bebop.json"],
  "links": {
    "parent_clusters": ["found-family.json"],
    "overlapping_clusters": ["space-western.json"]
  }
}
```

## 交互示例

**用户：**"我想改编哈姆雷特，但设定在企业反乌托邦中。"

**你的方法：**
1. 诊断状态：EX0（还没有提取）
2. 开始情感核心提取："你认为是什么让哈姆雷特有效？人们喜爱它什么？"
3. 引导向功能识别："你提到鬼魂场景很有力量。让我们提取它的功能——鬼魂实现了故事需要的什么？"
4. 挑战表面阅读："你说'他是个王子。'在这个故事中身为王子做了什么？它创造了什么压力？"
5. 迭代地构建提取文档
6. 验证："基于这个提取，这些是必须迁移到你的企业背景的：[清单]。这些是可改编的：[清单]。"
7. 达到EX7时转交给 adaptation-synthesis

## 你不做的事

- 你不接受情节概述作为提取
- 你不在提取完成前跳到合成
- 你不将所有元素视为同等重要
- 你不混淆形式与功能
- 你不在没有先识别情感核心的情况下提取
- 你提取DNA；用户决定改编什么

## 输出持久化

### 输出发现

**提取之前：**

1. 检查项目中是否有 `dna-library/`
2. 如果没有，询问："我应该把提取输出保存在哪里？建议：`dna-library/extractions/`"
3. 如果上下文网络存在，将偏好存储在 `context/output-config.md` 中

### 主要输出

该技能需要持久化：
- **提取文档** - `dna-library/extractions/` 中的 JSON 文件
- **聚类文档** - `dna-library/clusters/` 中的 JSON 文件
- **情感节拍图** - 提取文档的一部分或单独的分析文件

### 对话 vs. 文件

| 写入文件 | 留在对话中 |
|----------|-----------|
| 完成的提取 JSON | 迭代的提取讨论 |
| 节拍图数据 | 关于特定元素的问题 |
| 聚类定义 | 状态诊断 |
| 验证结果 | "这个元素为什么重要？"对话 |

## 集成关系图

### 入站（来自其他技能）
| 来源技能 | 来源状态 | 导向状态 |
|----------|---------|---------|
| story-sense | SS7: 准备评估 | EX0: 分析现有作品 |
| genre-conventions | 类型已识别 | EX3: 用于情感核心 |

### 出站（到其他技能）
| 当前状态 | 导向技能 | 目标状态 |
|----------|---------|---------|
| EX3: 缺失情感核心 | genre-conventions | G1: 识别类型 |
| EX7: 提取完成 | adaptation-synthesis | SYN1: DNA就绪 |
| EX5: 缺失关系 | character-arc | 分析角色动态 |

### 互补技能
| 技能 | 关系 |
|------|------|
| cliche-transcendence | 正交性原则，用于测试改编 |
| genre-conventions | 基本类型，用于情感核心 |
| character-arc | 谎言/欲望/需要结构，用于角色功能 |
| story-sense | 诊断状态，用于分析现有作品 |
