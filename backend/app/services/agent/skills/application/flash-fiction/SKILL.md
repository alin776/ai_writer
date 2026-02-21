---
name: flash-fiction
description: 诊断和修正闪小说与微型小说中的问题。适用于闪小说感觉薄弱、写作1500字以下的故事、处理微型小说、突然小说或压缩叙事形式时。
license: MIT
metadata:
  author: jwynia
  version: "1.0"
  type: diagnostic
  mode: evaluative
  domain: fiction
allowed-tools: [read_file, write_file, edit_file, glob, grep, execute]
---

# 闪小说诊断

## 目的

诊断和修正闪小说与微型小说（通常1500字以下）中的问题。闪小说要求极高的技巧效率——每个词都必须服务于多重目的。该技能识别当作品不起作用时需要关注的维度。

## 快速参考

| 状态 | 信号 | 核心问题 |
|------|------|---------|
| FF1 | 开头没有钩子 | 结构/节奏问题 |
| FF2 | 角色感觉单薄 | 角色压缩失败 |
| FF3 | 开头/结尾断裂 | 框架薄弱 |
| FF4 | 一切在表面 | 缺少潜台词 |
| FF5 | 散文感觉平淡 | 意象/修辞语言薄弱 |
| FF6 | 背景通用 | 感官细节缺乏 |
| FF7 | 主题缺失或说教 | 主题发展偏差 |
| FF8 | 文字不歌唱 | 语言精准度/节奏问题 |
| FF9 | 某处感觉"不对" | 逻辑一致性破裂 |

## 诊断状态

### FF1：结构与节奏失败

**症状：**
- 开头不吸引人
- 中间拖沓或急促
- 结尾感觉突兀或拖拉
- 字数分配不佳
- 弧线感觉不完整

**诊断问题：**
1. 第一句话是否创造了立即的参与感？
2. 有没有清晰的转折点？
3. 每个段落是否推进了多重目的（情节 + 角色 + 主题）？
4. 范围是否适合字数？
5. 信息是否在最佳时刻释放？

**干预措施：**
- 映射弧线：开头 → 上升 → 高潮 → 结局
- 计算各部分的字数分配
- 加强开头钩子（从中间开始、悬念、声明）
- 确保结尾提供闭合感同时留下余韵
- 删除只做一件事的段落

**转化模式：**
```
WEAK: "Sarah had been working at the firm for three years when she found the file."
STRONG: "The file had no label—just a smudge of what looked like dried blood along its edge."
```

---

### FF2：角色压缩失败

**症状：**
- 角色感觉通用或可互换
- 太多背景故事说明
- 角色变化感觉不够充分
- 关系被解释而非展示
- 没有超出纸面的生命感

**诊断问题：**
1. 每个角色是否通过揭示性动作被介绍？
2. 历史能否在不显式回溯的情况下被推断？
3. 定义性物品/举止是否揭示了本质？
4. 角色弧线是否通过平行动作展示？
5. 关系是否通过互动而非解释浮现？

**干预措施：**
- 用角色特有的细节替换通用描述
- 将背景故事说明转换为暗示
- 确保第一个动作揭示个性
- 通过决策模式的变化展示改变
- 通过未言之事建立关系

**转化模式：**
```
WEAK: "James had PTSD from the war. He moved to escape memories."
STRONG: "James flinched at the turkey platter's clatter, hand reaching for the phantom sidearm.
He'd chosen this town for its population sign: 827 souls—small enough to hear rumors
of strangers before meeting them."
```

---

### FF3：开头/结尾框架薄弱

**症状：**
- 开头和结尾感觉脱节
- 尽管简短却没有旅程感
- 结尾没有兑现开头的承诺
- 首尾意象不产生共鸣
- 结构感觉随意

**诊断问题：**
1. 开头向读者承诺了什么？
2. 结尾是否兑现或有意义地颠覆了那个承诺？
3. 首尾意象之间是否有关系（回声、转化、对比）？
4. 结尾是否既出乎意料又不可避免？
5. 阅读后什么情感持续？

**干预措施：**
- 确定开头创造的隐性契约
- 确保结尾意象与开头意象相关
- 考虑循环结构（带转化的回归）
- 加强最后一句的余韵
- 检查情感旅程是否完整

**转化模式：**
```
WEAK ENDING: "So they decided not to sell. They were happy. The end."
STRONG ENDING: "Daniel returned the FOR SALE sign to the garage, laid it beside the smaller
one from his childhood treehouse. Some prices, they'd decided, were too steep to calculate."
```

---

### FF4：缺少潜台词

**症状：**
- 一切都明确陈述
- 表面之下没有层次
- 读者不参与意义的构建
- 背景故事被倾倒而非暗示
- 没有冰山效应

**诊断问题：**
1. 什么被说出了但可以被暗示？
2. 有什么被策略性地未说？
3. 是否有留给读者填补的有意义空白？
4. 可见部分是否暗示了不可见的深度？
5. 模糊性是有意的还是偶然的？

**干预措施：**
- 将显式陈述转换为暗示
- 创造策略性空白（叙事省略）
- 为揭示的冲击力保留信息
- 应用冰山理论：展示冰山一角，暗示水下的巨大体量
- 确保背景故事通过物品/动作浮现，而非解释

**转化模式：**
```
EXPLICIT: "John never recovered from his divorce. He felt bitter about Maria leaving him."
IMPLIED: "John twisted his wedding ring finger, a reflex unchanged by three years and
the absence of metal. The man at the next table laughed, and John recognized
the laugh before the face."
```

---

### FF5：意象与修辞语言薄弱

**症状：**
- 散文感觉平淡或功利
- 比喻老套或缺失
- 意象没有模式
- 象征过于明显或缺失
- 描写不产生共鸣

**诊断问题：**
1. 比较是否新鲜而精确？
2. 隐喻/明喻是否服务于多重目的（角色 + 主题 + 情感）？
3. 是否有发展中的意象模式？
4. 象征性物品是否自然融入？
5. 具体与抽象之间是否平衡？

**干预措施：**
- 用原创的替换老套的比较
- 确保修辞语言揭示角色视角
- 建立发展中的相关意象模式
- 选择能转化含义的象征性物品
- 用具体意象锚定抽象概念

**转化模式：**
```
FLAT: "The factory was abandoned and looked sad."
RICH: "Machinery hulked under dust shrouds, metal teeth gleaming in fractured light
between boarded windows. No one suggested splitting up."
```

---

### FF6：背景与感官细节缺乏

**症状：**
- 地点通用或缺失
- 只有视觉感被调动
- 背景不服务于角色/主题
- 氛围缺失
- 环境像布景板而非参与者

**诊断问题：**
1. 读者多快被定位到具体的时间/地点？
2. 多种感官是否被调动？
3. 背景是否在不直说的情况下揭示角色？
4. 环境是否强化了主题？
5. 是否通过具体细节建立了情绪氛围？

**干预措施：**
- 用具体的、揭示性的地点替换通用背景
- 加入非视觉感官（声音、气味、触觉、味觉）
- 使背景细节揭示角色与地方的关系
- 使物理环境与主题关切对齐
- 在具体细节中嵌入情绪，而非陈述氛围

**转化模式：**
```
GENERIC: "The coffee shop was busy. People sat drinking coffee."
SPECIFIC: "The Fallout Shelter Café's concrete walls trapped steam from twenty
underemployed grad students' laptops, their whispered theories competing
with grinding beans and Ella Fitzgerald's crackled vinyl."
```

---

### FF7：主题发展偏差

**症状：**
- 主题缺失或不清晰
- 主题被陈述而非体现
- 说教/布道的语气
- 单一视角主导
- 结尾过度简化

**诊断问题：**
1. 主题是否可以识别而不显得刻意？
2. 主题是否从角色和情境中自然浮现（而非强加）？
3. 是否呈现了对主题的多种视角？
4. 主题内容是否通过具体细节传达？
5. 结论是否加深而非简化？

**干预措施：**
- 通过行动和物品而非陈述来体现主题
- 通过具体情境展示主题，然后让读者自行概括
- 包含对主题问题的多种观点
- 用展示的行动替换"角色意识到……"
- 在结论中保持复杂性

**转化模式：**
```
STATED: "Carl realized that trust was essential for relationships."
EMBODIED: "Carl handed her the combination to the safe where he kept
his mother's letters, then turned away so he wouldn't see her expression."
```

---

### FF8：语言精准度与节奏问题

**症状：**
- 动词无力（走了、去了、是）
- 名词模糊（东西、那个、区域）
- 不必要的修饰语
- 句式单调
- 没有音乐性

**诊断问题：**
1. 每个动词是否精确捕捉了具体动作？
2. 名词是否具体而特定？
3. 每个修饰语是否有意义地增进了理解？
4. 句子长度和结构是否有变化？
5. 音韵模式是否增强效果（头韵、节奏、韵律）？

**干预措施：**
- 用精确、有力的替代品替换无力的动词
- 用具体的、感官丰富的名词替换通用名词
- 删除冗余或装饰性修饰语
- 变化句式结构以产生节奏和强调
- 发展与含义匹配的音韵模式

**转化模式：**
```
WEAK: "She went across the field quickly."
PRECISE: "She slashed through the wheat, scattering husks."

MONOTONOUS: "He opened the door. He looked inside. He saw nothing. He closed the door."
VARIED: "He opened the door and looked inside. Nothing. The door clicked shut as he turned."
```

---

### FF9：逻辑一致性破裂

**症状：**
- 某处感觉"不对"即使难以确定
- 物理上的不可能
- 时间线矛盾
- 角色知道他们不该知道的事
- 规则建立后被打破

**诊断问题：**
1. 物品是否一致地运作？
2. 时间线是否允许所描述的事件？
3. 角色是否只知道他们能合理知道的？
4. 物理限制是否被尊重？
5. 如果规则被弯曲，是否一致？

**干预措施：**
- 映射物理移动并验证可能性
- 按时间顺序绘制事件及其持续时间
- 检查角色的知识边界
- 验证因果比例
- 记录世界规则并检查一致应用

**转化模式：**
```
IMPOSSIBLE: "She finished her shift at midnight, drove 30 miles home,
cooked dinner, and was in bed by 12:15."
POSSIBLE: "She finished at midnight. The apartment she'd rented
closer to the hospital meant she could be cooking within minutes."
```

---

## 评估清单

对任何闪小说作品：

**结构（FF1）**
- [ ] 第一句有钩子
- [ ] 每个段落服务于多重目的
- [ ] 尽管压缩但有清晰的弧线
- [ ] 范围匹配字数

**角色（FF2）**
- [ ] 角色通过揭示性动作被介绍
- [ ] 历史被推断而非解释
- [ ] 变化通过动作展示

**框架（FF3）**
- [ ] 首尾意象相关
- [ ] 结尾兑现或转化了承诺
- [ ] 情感旅程完整

**潜台词（FF4）**
- [ ] 暗示多于陈述
- [ ] 策略性空白留给读者参与
- [ ] 冰山效应达成

**意象（FF5）**
- [ ] 新鲜的修辞语言
- [ ] 意象模式发展
- [ ] 象征自然融入

**背景（FF6）**
- [ ] 快速建立具体时间/地点
- [ ] 多种感官被调动
- [ ] 背景服务于主题

**主题（FF7）**
- [ ] 主题浮现而非陈述
- [ ] 呈现多种视角
- [ ] 保持复杂性

**语言（FF8）**
- [ ] 精确的动词
- [ ] 具体的名词
- [ ] 句式变化
- [ ] 音乐性存在

**一致性（FF9）**
- [ ] 物理规律有效
- [ ] 时间线可能
- [ ] 知识边界被尊重

---

## 反模式

### 微型小说
试图将长篇小说级别的故事压缩到闪小说的长度。闪小说不是概要——它是微缩的完整体验。选择适合的范围。

### 反转依赖
完全依赖惊奇的结尾。如果故事只有反转才有效，前面的内容没有发挥作用。旅程本身应该重要。

### 小品陷阱
优美的散文但没有叙事运动。闪小说仍然需要变化——到结尾时必须有所不同，即使是微妙的。

---

## 整合点

**入站：**
- 来自 `story-sense`：确定故事状态后
- 来自 `drafting`：初稿创作过程中
- 来自 `revision`：行级打磨时

**出站：**
- 到 `prose-style`：进行更深入的语言工作
- 到 `dialogue`：处理对话问题
- 到 `endings`：处理结尾问题

**互补：**
- `scene-sequencing`：单场景节奏
- `character-arc`：压缩的转变
- `cliche-transcendence`：生成新鲜意象

---

## 字数指南

| 长度 | 名称 | 重点优先级 |
|------|------|-----------|
| <100 | 百字微小说 | 单一意象、单一时刻、最大压缩 |
| 100-500 | 微型小说 | 一个场景、一次转变、暗示胜于陈述 |
| 500-1000 | 闪小说 | 小弧线、1-2个场景、完整冰山效应 |
| 1000-1500 | 突然小说 | 可以有多个场景、更多角色空间 |
| 1500-2500 | 极短篇 | 接近短篇小说领域 |

---

## 参考来源

框架综合自闪小说写作技巧分析，融合了以下原则：
- 海明威的冰山理论
- 约翰·加德纳关于"生动而持续的梦境"的论述
- 来自诗歌的压缩技术应用于散文
