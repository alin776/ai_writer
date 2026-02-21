---
name: worldbuilding
description: "诊断世界层面的故事问题。当设定感觉单薄、机构感觉是设计出来而非自然演变的、经济不合理、或非人类物种感觉像穿着戏服的人类时，应使用此技能。关键词：worldbuilding、设定、世界、机构、经济、文化、物种、后果。"
license: MIT
compatibility: 适用于任何虚构类型。与 story-sense 配合用于路由。
metadata:
  author: jwynia
  version: "1.0"
  type: diagnostic
  mode: diagnostic
  domain: worldbuilding
allowed-tools: [read_file, glob, grep, semantic_search]
---

# 世界构建：诊断技能

诊断虚构设定中的世界层面问题。识别缺失或不令人信服之处，并推荐具体的干预措施。

## 何时使用本技能

在以下情况使用本技能：
- 设定感觉像一幅画好的背景板
- 技术/魔法没有改变社会
- 机构感觉是设计出来的而非自然演变的
- 经济不合理
- 文化缺乏深度

不要在以下情况使用本技能：
- 故事问题以角色为中心（使用 character-arc）
- 情节结构问题（使用 scene-sequencing）
- 需要从零开始生成世界（使用 systemic-worldbuilding）

## 核心原则

**当世界感觉是设计出来的而非自然演变的，世界构建就失败了。**

好的世界构建创造一种认知：设定拥有历史、内在逻辑和独立于情节运作的过程。

## 世界状态

### W1：背景板世界
**症状：** 设定存在但没有独立逻辑
**干预措施：** systemic-worldbuilding（追踪后果）

### W2：无后果的世界
**症状：** 技术/魔法存在但没有改变社会
**干预措施：** 后果级联分析

### W3：没有历史的机构
**症状：** 组织感觉像上周才设计的
**干预措施：** 有机制度设计

### W4：经济不合理
**症状：** 贸易存在但没有供应链；价格武断
**干预措施：** economic-systems

### W5：信仰系统肤浅
**症状：** 宗教只是点缀，缺乏神学深度
**干预措施：** belief-systems

### W6：缺乏深度的文化
**症状：** 传统感觉随意；表面级的美学
**干预措施：** memetic-depth

### W7：扁平的非人类
**症状：** 外星人/物种是穿着戏服的人类
**干预措施：** conlang、alien-sensory frameworks

### W7.5：语言感觉泛泛
**症状：** 名字听起来像英语；没有语言质感
**干预措施：** conlang、language-evolution

## 后果级联

适用于任何主要思辨元素：

```
Initial Element
├── 1st Order: Direct practical effects
│   ├── Who gains immediate advantage?
│   ├── What becomes obsolete?
│   └── Technical limitations?
├── 2nd Order: Systemic adaptations
│   ├── How do economic structures adapt?
│   ├── How do power structures respond?
│   └── What resistance movements arise?
└── 3rd Order: Cultural evolution
    ├── What new language emerges?
    ├── What ethical questions arise?
    └── What becomes normalized?
```

## 关键诊断问题

### 针对技术/魔法
- 与我们世界的初始分歧是什么？
- 谁获得权力？什么变得过时？
- 掌权者会如何试图控制它？

### 针对机构
- 这个组织何时成立？
- 它经历了什么危机？
- 它的内部矛盾是什么？

### 针对经济
- 根本的稀缺性是什么？
- 价值如何确定？
- 地下经济是什么样的？

### 针对信仰系统
- 什么解释了存在？
- 信仰如何影响日常决策？
- 分裂和辩论有哪些？

## 常见反模式

### 单一文化
整个星球/物种一种统一文化。
**修复：** 添加区域变异、阶层差异、分裂。

### 便利技术
技术在情节需要时才存在。
**修复：** 追踪后果级联。

### 静态历史
世界数百年不变。
**修复：** 添加近期的扰动、正在进行的改革。

### 邪恶帝国
反派国家统一地邪恶。
**修复：** 添加内部辩论、普通人。

### 橡皮前额外星人
非人类只有微小的外观差异。
**修复：** 从生物学开始，追踪到认知，再追踪到文化。

## 深度 vs 广度

**深入的时机：**
- 元素是情节核心
- 元素将被仔细审视
- 元素创造持续冲突

**保持浅显的时机：**
- 元素是背景细节
- POV角色不会知道深层信息
- 神秘感更有趣

## 相关技能

- **systemic-worldbuilding** - 从初始分歧构建世界
- **belief-systems** - 深度神学设计
- **economic-systems** - 经济逻辑
- **governance-systems** - 政治结构
- **conlang** - 语言设计
- **settlement-design** - 城市和地理
