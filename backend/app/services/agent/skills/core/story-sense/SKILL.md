---
name: story-sense
description: "诊断任何故事的当前状态及其所需。当写作者陷入瓶颈、评估故事问题、叙事感觉失控，或有人问'我的故事哪里出了问题？'时，应使用本技能。关键词：故事、诊断、瓶颈、叙事、情节、角色、世界观构建、修订。"
license: MIT
compatibility: 适用于任何小说体裁。小说诊断的入口技能。
metadata:
  author: jwynia
  version: "1.0"
  type: diagnostic
  mode: diagnostic
  domain: fiction
allowed-tools: [read_file, glob, grep, semantic_search, execute]
---

# Story Sense：诊断技能

识别故事所处的状态，以及推动它前进所需的条件。这不是一个线性流程，而是一个诊断模型：评估 → 诊断 → 干预 → 再评估。

## 何时使用本技能

适用场景：
- 写作者陷入瓶颈，不知道原因
- 故事感觉不对劲，但根本原因不明
- 需要系统性地评估故事问题
- 有人问"我的故事哪里出了问题？"

不适用场景：
- 写作者希望你来写故事（使用 story-collaborator）
- 写作者只想要引导性提问（使用 story-coach）
- 出版/营销相关问题（使用 book-marketing）

## 核心原则

**Story Sense 是一种能力——无论故事处于什么状态或面向什么媒介，都能判断它需要什么。**

**不存在所谓的"卡住了"。** 只有：
- 尚未诊断出问题
- 尚未使用正确的干预手段

## 故事状态

### 状态 0：没有故事（空白页）
**症状：** 什么都还没写
**干预手段：** story-idea-generator、元素类型

### 状态 1：有概念但缺乏根基
**症状：** 有想法，但世界观/角色/情节感觉单薄
**干预手段：** cliche-transcendence、systemic-worldbuilding、key-moments

### 状态 2：有世界但缺乏生命力
**症状：** 设定存在但感觉只是背景板
**干预手段：** 世界观构建技能套件（belief-systems、economic-systems、governance-systems）

### 状态 3：扁平的非人类角色
**症状：** 外星人/奇幻种族感觉像是穿了戏服的人类
**干预手段：** conlang、物种开发框架

### 状态 4：缺乏维度的角色
**症状：** 角色为情节服务，而非驱动情节
**干预手段：** character-arc、underdog-unit、positional-revelation

### 状态 4.5：有情节但缺乏节奏
**症状：** 单个场景没问题，但无法形成累积效果
**干预手段：** scene-sequencing

### 状态 5：有情节但缺乏意义
**症状：** 事件发生了，但没有积累出意义
**干预手段：** moral-parallax、key-moments

### 状态 5.5：对白感觉平淡
**症状：** 角色听起来千篇一律，对话缺乏生气
**干预手段：** dialogue

### 状态 5.75：结局没有力度
**症状：** 故事铺垫得很好，但结局令人失望
**干预手段：** endings

### 状态 5.85：草稿无法推进
**症状：** 规划已完成，但草稿写不下去
**干预手段：** drafting

### 状态 5.9：文笔感觉平淡
**症状：** 故事成立，但句子只是功能性的，并不令人难忘
**干预手段：** prose-style

### 状态 6：草稿完成，需要修订
**症状：** 草稿已有，但修订工作令人无从下手
**干预手段：** revision

### 状态 7：准备接受评估
**症状：** 故事已完成，但质量不确定
**干预手段：** sensitivity-check、story-analysis

## 决策树

```
Is there anything on the page?
├── NO → story-idea-generator
└── YES → What's the problem?
    ├── Feels generic → cliche-transcendence
    ├── World feels thin → worldbuilding
    ├── Non-humans feel fake → conlang
    ├── Characters flat → character-arc
    ├── Pacing off → scene-sequencing
    ├── Dialogue wooden → dialogue
    ├── Ending weak → endings
    ├── Meaning unclear → moral-parallax
    ├── Draft not progressing → drafting
    ├── Prose flat → prose-style
    └── Draft needs revision → revision
```

## 诊断流程

1. **倾听症状** —— 他们描述的问题是什么？
2. **追问澄清** —— 具体卡在哪里？
3. **识别状态** —— 将症状与状态列表匹配
4. **命名诊断** —— 解释你观察到的问题
5. **推荐干预** —— 指向具体的技能
6. **提供后续步骤** —— 他们应该先尝试什么？

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
python skills/core/story-sense/scripts/functions.py --setting scifi
python skills/core/story-sense/scripts/functions.py healer --setting fantasy
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
