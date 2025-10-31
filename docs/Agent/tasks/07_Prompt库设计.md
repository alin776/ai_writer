# 07 - Prompt库设计

> **文档版本**: v1.0
> **创建日期**: 2025-10-31
> **所属阶段**: 阶段二 - 高价值功能集成

---

## 📋 目录

- [1. 设计目标](#1-设计目标)
- [2. 四维度爽感优化](#2-四维度爽感优化)
- [3. 分阶段创作Prompt](#3-分阶段创作prompt)
- [4. 场景化Prompt模板](#4-场景化prompt模板)
- [5. 使用示例](#5-使用示例)

---

## 1. 设计目标

### 1.1 核心目标

**直接采用 novel-ai-agent-Chinese 的精品 Prompt**

- ✅ **四维度爽感优化**: 反转35% + 升级35% + 场景20% + 对话10%
- ✅ **分阶段生成策略**: 起承转合终
- ✅ **场景化模板**: 打脸、升级、战斗等

### 1.2 价值

- 提升网文创作质量
- 标准化爽点设计
- 降低创作门槛

---

## 2. 四维度爽感优化

### 2.1 系统级Prompt

**文件**: `backend/app/services/agent/prompt_library.py`

```python
CONTENT_CREATION_SYSTEM = """你是一位专业的网络小说创作专家，精通各种类型的网文创作技巧。

# 核心创作理念: 四维度爽感优化

## 1. 反转与震撼 (权重35%)
- 出人意料的能力展现
- 身份地位的突然转变
- 打脸装逼打击对手
- 令众人震撼的场面

## 2. 期待与升级 (权重35%)
- 能力不断提升
- 资源持续积累
- 身份地位逐步提高
- 真相逐步揭露

## 3. 场景描写 (权重20%)
- 震撼性的场面描绘
- 众人反应的细节
- 气氛的渲染烘托

## 4. 对话设计 (权重10%)
- 犀利的对话交锋
- 有力的反击台词
- 装逼打脸的金句

# 创作要求

1. **节奏控制**: 快节奏推进，避免冗长铺垫
2. **冲突密度**: 每500字至少一个小冲突，每2000字一个大冲突
3. **爽点密度**: 平均每300-500字一个爽点
4. **描写平衡**: 70%情节推进 + 20%场景描写 + 10%心理活动

# 禁止事项

❌ 拖沓的环境描写
❌ 冗长的心理活动
❌ 说教式的道理阐述
❌ 无意义的日常琐事
"""
```

---

## 3. 分阶段创作Prompt

### 3.1 五阶段定义

```python
class NovelPhase(str, Enum):
    """小说创作阶段"""
    OPENING = "opening"          # 起 (开篇)
    DEVELOPMENT = "development"  # 承 (发展)
    CLIMAX = "climax"            # 转 (转折)
    RESOLUTION = "resolution"    # 合 (收束)
    ENDING = "ending"            # 终 (结局)
```

### 3.2 各阶段Prompt

#### 开篇阶段

```python
PHASE_PROMPTS[NovelPhase.OPENING] = """# 开篇阶段创作要求

## 核心目标
- 快速吸引读者（前100字抓住注意力）
- 展示主角特点
- 埋下悬念钩子

## 创作要点
1. **开场爆点**: 直接进入冲突或震撼场景
2. **主角登场**: 30字内让主角出场
3. **世界观展示**: 自然融入背景设定
4. **节奏**: 快节奏，不拖沓

## 禁止
❌ 大段环境描写开场
❌ 冗长的背景介绍
❌ 平淡的日常开局

上下文: {context}
字数要求: {target_length}

请创作开篇内容。
"""
```

#### 发展阶段

```python
PHASE_PROMPTS[NovelPhase.DEVELOPMENT] = """# 发展阶段创作要求

## 核心目标
- 能力提升和资源积累
- 矛盾冲突升级
- 埋下后续伏笔

## 创作要点
1. **升级节奏**: 每章至少一次提升
2. **冲突升级**: 逐步增强对手实力
3. **支线展开**: 丰富剧情层次
4. **伏笔埋设**: 为高潮做准备

## 爽点设计
- 小怪升级: 200-300字一次
- 打脸装逼: 500-800字一次
- 实力展现: 1000-1500字一次

上下文: {context}
字数要求: {target_length}

请创作发展阶段内容。
"""
```

#### 高潮阶段

```python
PHASE_PROMPTS[NovelPhase.CLIMAX] = """# 高潮阶段创作要求

## 核心目标
- 情节冲突达到顶点
- 主角面临最大挑战
- 读者情绪高度紧张

## 创作要点
1. **冲突激化**: 最强对手出现
2. **反转设计**: 至少2-3次剧情反转
3. **情绪渲染**: 紧张、刺激、震撼
4. **爽点爆发**: 集中释放爽点

## 结构建议
- 危机铺垫 (20%)
- 对抗升级 (30%)
- 绝地反击 (30%)
- 震撼结局 (20%)

上下文: {context}
字数要求: {target_length}

请创作高潮阶段内容。
"""
```

---

## 4. 场景化Prompt模板

### 4.1 打脸场景

```python
SLAP_FACE_TEMPLATE = """# 打脸场景创作要求

## 四要素结构 (总计500-800字)

1. **铺垫** (30% 篇幅, 150-240字)
   - 对手嚣张轻蔑
   - 旁观者附和
   - 主角被低估

2. **转折** (20% 篇幅, 100-160字)
   - 突然的变化
   - 众人疑惑
   - 气氛转变

3. **反击** (30% 篇幅, 150-240字)
   - 主角实力展现
   - 碾压式胜利
   - 对手震惊

4. **结果** (20% 篇幅, 100-160字)
   - 众人震撼
   - 地位翻转
   - 余韵回味

上下文: {context}

请根据上述要求创作一个精彩的打脸场景。
"""
```

### 4.2 完整实现

```python
class ContentCreationPrompts:
    """内容创作Prompt库"""

    @staticmethod
    def get_phase_prompt(
        phase: NovelPhase,
        context: str,
        target_length: int = 500
    ) -> str:
        """获取阶段化Prompt"""
        template = ContentCreationPrompts.PHASE_PROMPTS.get(phase)
        if not template:
            return ""

        return template.format(
            context=context,
            target_length=target_length
        )

    @staticmethod
    def get_system_prompt() -> str:
        """获取系统级Prompt"""
        return ContentCreationPrompts.CONTENT_CREATION_SYSTEM

    @staticmethod
    def get_slap_face_prompt(context: str) -> str:
        """获取打脸场景Prompt"""
        return ContentCreationPrompts.SLAP_FACE_TEMPLATE.format(
            context=context
        )


class PromptOptimizer:
    """Prompt优化器"""

    @staticmethod
    def add_user_preferences(
        base_prompt: str,
        user_preferences: Dict[str, Any]
    ) -> str:
        """根据用户偏好优化Prompt"""
        additions = []

        if user_preferences.get("preferred_style"):
            additions.append(
                f"写作风格偏好: {user_preferences['preferred_style']}"
            )

        if user_preferences.get("preferred_length"):
            additions.append(
                f"篇幅偏好: {user_preferences['preferred_length']}"
            )

        if additions:
            return base_prompt + "\n\n# 用户偏好\n" + "\n".join(additions)

        return base_prompt

    @staticmethod
    def add_quality_feedback(
        base_prompt: str,
        feedback: List[str]
    ) -> str:
        """添加质量反馈"""
        if not feedback:
            return base_prompt

        feedback_text = "\n".join(f"- {f}" for f in feedback)
        return base_prompt + f"\n\n# 改进建议\n{feedback_text}"
```

---

## 5. 使用示例

### 5.1 基本使用

```python
from app.services.agent.prompt_library import (
    ContentCreationPrompts,
    NovelPhase,
    PromptOptimizer
)

# 1. 获取系统Prompt
system_prompt = ContentCreationPrompts.get_system_prompt()

# 2. 获取阶段Prompt
opening_prompt = ContentCreationPrompts.get_phase_prompt(
    phase=NovelPhase.OPENING,
    context="主角穿越到修仙界",
    target_length=800
)

# 3. 获取场景Prompt
slap_face_prompt = ContentCreationPrompts.get_slap_face_prompt(
    context="主角在拍卖会上被人嘲笑"
)

# 4. 添加用户偏好
optimized_prompt = PromptOptimizer.add_user_preferences(
    base_prompt=opening_prompt,
    user_preferences={
        "preferred_style": "热血爽文",
        "preferred_length": "简短有力"
    }
)

# 5. 添加质量反馈
final_prompt = PromptOptimizer.add_quality_feedback(
    base_prompt=optimized_prompt,
    feedback=["增加描写细节", "加快节奏"]
)
```

### 5.2 在Agent中集成

```python
class WritingAgent:
    """写作Agent"""

    def __init__(self):
        self.prompts = ContentCreationPrompts()

    async def write_opening(
        self,
        context: str,
        target_length: int = 800
    ) -> str:
        """创作开篇"""

        # 获取系统Prompt + 阶段Prompt
        system_prompt = self.prompts.get_system_prompt()
        phase_prompt = self.prompts.get_phase_prompt(
            NovelPhase.OPENING,
            context,
            target_length
        )

        # 调用AI生成
        result = await self.ai_service.chat_complete(
            system=system_prompt,
            user=phase_prompt
        )

        return result
```

---

## 相关文档

- [06_质量循环设计](./06_质量循环设计.md) - 质量评估
- [08_模型选择器设计](./08_模型选择器设计.md) - 模型选择

---

> **下一步**: [08_模型选择器设计](./08_模型选择器设计.md)
