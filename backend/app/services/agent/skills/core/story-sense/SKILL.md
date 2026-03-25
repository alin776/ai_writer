---
name: story-sense
description: "诊断任何故事的当前状态及其所需。当写作者陷入瓶颈、评估故事问题、叙事感觉失控，或有人问'我的故事哪里出了问题？'时，应使用本技能。关键词：故事、诊断、瓶颈、叙事、情节、角色、世界观构建、修订。"
license: MIT
compatibility: 适用于任何小说体裁。小说诊断的入口技能。
metadata:
  author: jwynia
  version: "2.0"
  type: diagnostic
  mode: diagnostic
  domain: fiction
allowed-tools: read_file, glob, grep, semantic_search, execute, task, web_search, fetch_url
---

# Story Sense：诊断技能

识别故事所处的状态，以及推动它前进所需的条件。这不是一个线性流程，而是一个诊断模型：评估 → 诊断 → 干预 → 再评估。

## 何时使用本技能

适用场景：
- 写作者陷入瓶颈，不知道原因
- 故事感觉不对劲，但根本原因不明
- 需要系统性地评估故事问题
- 有人问"我的故事哪里出了问题？"
- 网文追读数据下滑，需要定位问题
- 开坑新书前做类型可行性诊断

不适用场景：
- 写作者希望你来写故事（使用 story-collaborator）
- 写作者只想要引导性提问（使用 story-coach）
- 出版/营销相关问题（不在本系统范围内）

## 核心原则

**Story Sense 是一种能力——无论故事处于什么状态或面向什么媒介，都能判断它需要什么。**

**不存在所谓的"卡住了"。** 只有：
- 尚未诊断出问题
- 尚未使用正确的干预手段

## 故事状态

### 状态 0：没有故事（空白页）
**症状：** 什么都还没写
**网文场景：** 新作开坑前不知道写什么类型，玄幻、都市、科幻还是系统文都没想好
**干预手段：** entropy 工具、元素类型

### 状态 1：有概念但缺乏根基
**症状：** 有想法，但世界观/角色/情节感觉单薄
**网文场景：** 有"修仙+都市"的想法但金手指和体系都没想好，大纲只有一句话
**干预手段：** cliche-transcendence、systemic-worldbuilding、key-moments

### 状态 2：有世界但缺乏生命力
**症状：** 设定存在但感觉只是背景板
**网文场景：** 写了一大堆修炼等级体系、门派设定，但读者反馈"设定太多看不下去"，世界观没有融入剧情
**干预手段：** systemic-worldbuilding、worldbuilding

### 状态 3：扁平的非人类角色
**症状：** 外星人/奇幻种族感觉像是穿了戏服的人类
**网文场景：** 妖族、龙族、精灵族等异种族写出来和人类没有区别，只是换了个名字
**干预手段：** worldbuilding、物种开发框架

### 状态 4：缺乏维度的角色
**症状：** 角色为情节服务，而非驱动情节
**网文场景：** 角色扁平化——配角沦为工具人，女主沦为花瓶，反派只会送人头
**干预手段：** character-arc、dialogue

### 状态 4.5：有情节但缺乏节奏
**症状：** 单个场景没问题，但无法形成累积效果
**网文场景：** 打脸情节堆叠但没有节奏变化，连续十章都在"装逼-打脸"循环中
**干预手段：** scene-sequencing

### 状态 5：有情节但缺乏意义
**症状：** 事件发生了，但没有积累出意义
**网文场景：** 写了几十万字但主线模糊，读者评论"太水了"，事件之间缺乏因果链
**干预手段：** key-moments、endings

### 状态 5.1：爽点不足
**症状：** 读者追读率下降，缺乏让人拍大腿的时刻。情节平铺直叙，没有情绪高潮点
**网文场景：** 追读数据持续走低，读者评论"没意思""弃了"，缺乏打脸、逆袭、翻盘等核心爽感
**干预手段：** key-moments（设计爽点节奏）

### 状态 5.2：升级曲线失衡
**症状：** 主角实力提升过快（无敌文）或过慢（读者弃书）。成长曲线与故事节奏不匹配
**网文场景：** 主角三章突破一个大境界导致无敌没有悬念，或者百章还在练气期读者等不及弃书
**干预手段：** outline-collaborator（调整升级节奏）

### 状态 5.3：金手指失控
**症状：** 主角的外挂能力无法自洽或过于万能。每次危机都靠金手指无脑解决，失去悬念
**网文场景：** 系统万能到什么都能兑换、功法秒学导致无挑战感，或者金手指前后设定矛盾被读者抓BUG
**干预手段：** worldbuilding（体系自洽性检查）

### 状态 5.5：对白感觉平淡
**症状：** 角色听起来千篇一律，对话缺乏生气
**网文场景：** 所有角色说话一个味道，老爷爷和小萝莉用同一种语气，没有个性化口癖
**干预手段：** dialogue

### 状态 5.75：结局没有力度
**症状：** 故事铺垫得很好，但结局令人失望
**网文场景：** 长篇连载烂尾，大量伏笔没有回收，最终大战草草收场
**干预手段：** endings

### 状态 5.85：草稿无法推进
**症状：** 规划已完成，但草稿写不下去
**网文场景：** 大纲写了十万字但正文一个字都憋不出来，或者日更压力下完全卡文
**干预手段：** drafting

### 状态 5.9：文笔感觉平淡
**症状：** 故事成立，但句子只是功能性的，并不令人难忘
**网文场景：** 读者评论"像在看流水账"，战斗描写没有画面感，环境描写像在念说明书
**干预手段：** prose-style

### 状态 6：草稿完成，需要修订
**症状：** 草稿已有，但修订工作令人无从下手
**网文场景：** 完本后想修订上架精修版，但几百万字的体量不知从何改起
**干预手段：** revision

### 状态 7：准备接受评估
**症状：** 故事已完成，但质量不确定
**网文场景：** 准备投稿签约平台，需要评估作品是否达到签约水平
**干预手段：** story-analysis

## 决策树

```
页面上有内容吗？
├── 没有 → entropy 工具 + 元素类型
└── 有 → 问题是什么？
    ├── 感觉老套 → cliche-transcendence
    ├── 世界观单薄 → worldbuilding
    ├── 非人种族失真 → worldbuilding
    ├── 角色扁平 → character-arc
    ├── 节奏失调 → scene-sequencing
    ├── 对白僵硬 → dialogue
    ├── 结局乏力 → endings
    ├── 主线模糊 → key-moments
    ├── 草稿推不动 → drafting
    ├── 文笔平淡 → prose-style
    ├── 草稿待修订 → revision
    │
    │── ── 网文专项诊断 ── ──
    ├── 爽点不足 → key-moments（爽点节奏设计）
    ├── 升级太快/太慢 → outline-collaborator（升级曲线调整）
    ├── 金手指自洽性差 → worldbuilding（体系检查）
    ├── 黄金三章不够吸引 → drafting（开篇设计）
    └── 追读数据下滑 → 综合诊断（回到状态匹配）
```

## 诊断流程

1. **倾听症状** —— 他们描述的问题是什么？
2. **追问澄清** —— 具体卡在哪里？
3. **识别状态** —— 将症状与状态列表匹配
4. **命名诊断** —— 解释你观察到的问题
5. **推荐干预** —— 指向具体的技能
6. **提供后续步骤** —— 他们应该先尝试什么？

## 输出路径

分析和诊断结果直接在对话中呈现。

## 可用脚本

### entropy.py
从精选列表中注入创意随机性。

> **路径提示**: 脚本位于 `skills/core/story-sense/scripts/` 目录下。
> 执行时必须使用从项目根目录出发的完整相对路径。

```bash
python skills/core/story-sense/scripts/entropy.py lies
python skills/core/story-sense/scripts/entropy.py disasters --count 3
python skills/core/story-sense/scripts/entropy.py --combo
```

**列表：** lies, ghosts, disasters, dilemmas, professions, locations, collisions, openings

### functions.py
从抽象的故事功能生成角色。

```bash
python skills/core/story-sense/scripts/functions.py
python skills/core/story-sense/scripts/functions.py --setting xuanhuan
python skills/core/story-sense/scripts/functions.py healer --setting urban
```

**功能：** healer, enforcer, keeper_of_secrets, maker, trader, guide, entertainer, death_worker, transgressor

## 反模式

### 处方式诊断而非真正的诊断
**修正：** 在做出诊断之前，始终先提出澄清性问题。

### 框架过载
**修正：** 推荐一种干预手段即可。在再评估后再扩展。

### 忽视写作者的能量状态
**修正：** 在诊断准确性和激发写作者热情之间取得平衡。

### 把结构当作故事
**修正：** 在进行结构诊断的同时，持续追问"这感觉对吗？"

## 相关技能

根据诊断出的状态，路由到所有小说写作技能。
