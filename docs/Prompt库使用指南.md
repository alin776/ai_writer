# Prompt 库使用指南

> **版本**: v1.0
> **创建日期**: 2025-11-01
> **适用于**: ai_writer Week 6 - Prompt库优化

---

## 📚 目录

1. [概述](#概述)
2. [快速开始](#快速开始)
3. [核心概念](#核心概念)
4. [详细使用](#详细使用)
5. [高级功能](#高级功能)
6. [最佳实践](#最佳实践)
7. [API 参考](#api-参考)

---

## 概述

Prompt 库是一个系统化的网文创作 Prompt 管理系统,提供:

- ✅ **网文爽感优化 Prompts** - 四维度加权设计
- ✅ **五阶段分级创作** - 起承转合终
- ✅ **场景模板化** - 打脸/升级/战斗等
- ✅ **动态组合能力** - 灵活组合多个 Prompt
- ✅ **质量循环集成** - 支持质量反馈和优化
- ✅ **使用统计追踪** - 数据驱动优化

**参考来源**: novel-ai-agent-Chinese 项目精华

---

## 快速开始

### 安装

```python
# 已集成在项目中,无需额外安装
from backend.app.services.agent.prompts import *
from backend.app.services.agent.prompt_library import *
```

### 5分钟上手

```python
from prompts import NovelPhase
from prompt_library import get_content_prompt

# 获取内容创作 Prompt
prompt = get_content_prompt(
    phase=NovelPhase.CLIMAX,  # 转 - 冲突升级阶段
    scene_type='battle',       # 战斗场景
    user_preferences={
        'style': '热血',
        'focus': ['打脸', '升级']
    },
    context={
        'target_length': 3000,
        'current_chapter': 25
    }
)

# 使用 Prompt 调用 LLM
# response = await llm_service.call(prompt)
```

---

## 核心概念

### 1. 网文五阶段

| 阶段 | 名称 | 章节 | 实力等级 | 字数 |
|------|------|------|---------|------|
| **起** | 故事开端 | 1-10 | Lv1 → Lv5 | 2000 |
| **承** | 主角成长 | 11-20 | Lv5 → Lv15 | 2500 |
| **转** | 冲突升级 | 21-30 | Lv15 → Lv50 | 3000 |
| **合** | 势力对抗 | 31-40 | Lv50 → Lv100+ | 3500 |
| **终** | 终极决战 | 41-50 | Lv100+ → 传说 | 4000 |

```python
from prompts import NovelPhase

# 使用枚举
phase = NovelPhase.CLIMAX  # 转阶段
```

### 2. 爽感公式

```
爽感 = 反转(35%) + 升级(35%) + 场景(20%) + 对话(10%)
```

**四个维度**:
1. **反转与震撼** (35%) - 出人意料的能力展现,身份转变,打脸
2. **期待与升级** (35%) - 能力提升,资源积累,真相揭露
3. **场景描写** (20%) - 震撼场面,众人反应,氛围渲染
4. **对话设计** (10%) - 犀利交锋,反击台词,装逼金句

### 3. 场景类型

```python
from prompts import SceneType

SceneType.SLAP_FACE   # 打脸场景
SceneType.UPGRADE     # 升级突破
SceneType.BATTLE      # 战斗场景
SceneType.REVEAL      # 真相揭露
# ... 更多场景类型
```

### 4. 打脸四要素

```python
from prompts import SlapFaceStructure

structure = SlapFaceStructure.get_structure()
# 铺垫 (30%) → 转折 (20%) → 反击 (30%) → 结果 (20%)
```

---

## 详细使用

### 1. 获取基础 Prompt

#### 1.1 系统级 Prompt

```python
from prompts import ContentCreationPrompts

# 获取核心系统 Prompt (包含四维度爽感设计)
system_prompt = ContentCreationPrompts.get_system_prompt()
```

#### 1.2 阶段 Prompt

```python
# 获取特定阶段的 Prompt
climax_prompt = ContentCreationPrompts.get_phase_prompt(
    NovelPhase.CLIMAX
)

# 带上下文
climax_with_context = ContentCreationPrompts.get_phase_prompt(
    NovelPhase.CLIMAX,
    context={
        'target_length': 3000,
        'previous_content': '上一章主角...',
        'current_chapter': 25,
        'total_chapters': 50
    }
)
```

#### 1.3 场景模板

```python
# 打脸场景
slap_face = ContentCreationPrompts.get_scene_prompt('slap_face')

# 升级场景
upgrade = ContentCreationPrompts.get_scene_prompt('upgrade')

# 战斗场景
battle = ContentCreationPrompts.get_scene_prompt('battle')
```

### 2. 组合多个 Prompt

```python
# 组合: 系统 + 阶段 + 场景 + 用户偏好
combined = ContentCreationPrompts.get_combined_prompt(
    phase=NovelPhase.OPENING,      # 起阶段
    scene_type='slap_face',         # 打脸场景
    user_preferences='增加武侠元素,主角使用剑法'
)
```

### 3. 使用 Prompt 优化器

#### 3.1 添加用户偏好

```python
from prompts import PromptOptimizer

enhanced = PromptOptimizer.add_user_preferences(
    base_prompt,
    user_preferences={
        'style': '轻松幽默',           # 写作风格
        'focus': ['打脸', '升级'],      # 重点关注
        'avoid': ['虐主', '感情戏过多'], # 避免元素
        'special_requirements': '主角要展现高智商'
    }
)
```

#### 3.2 添加质量反馈 (质量循环)

```python
# 用于质量循环的第二次生成
enhanced = PromptOptimizer.add_quality_feedback(
    base_prompt,
    feedback="连贯性需要提升,对话不够生动"
)
```

#### 3.3 添加上下文

```python
enhanced = PromptOptimizer.add_context(
    base_prompt,
    context={
        'current_chapter': 25,
        'total_chapters': 50,
        'target_length': 3000,
        'phase': '转',
        'previous_content': '前文内容...'
    }
)
```

#### 3.4 组合多个 Prompt

```python
combined = PromptOptimizer.combine_prompts(
    system_prompt="...",
    phase_prompt="...",
    user_prompt="重点描写主角的心理活动",
    scene_prompt="..."
)
```

### 4. 使用 Prompt 库管理系统

#### 4.1 使用全局库实例

```python
from prompt_library import prompt_library, get_content_prompt

# 便捷函数获取内容创作 Prompt
prompt = get_content_prompt(
    phase=NovelPhase.CLIMAX,
    scene_type='battle',
    user_preferences={'style': '热血'},
    context={'target_length': 3000}
)
```

#### 4.2 直接从库获取

```python
# 获取特定 Prompt
system_prompt = prompt_library.get_prompt('content_creation', 'system')
phase_prompt = prompt_library.get_prompt('content_creation', 'phase_climax')
```

#### 4.3 列出所有 Prompt

```python
# 列出所有类别
all_prompts = prompt_library.list_available_prompts()

# 列出特定类别
content_prompts = prompt_library.list_available_prompts('content_creation')
```

#### 4.4 追踪使用统计

```python
# 记录使用和质量
prompt_library.track_prompt_usage(
    'content_creation.phase_climax',
    result_quality=9.0  # 0-10 分
)

# 获取统计
stats = prompt_library.get_usage_stats('content_creation.phase_climax')
print(f"使用次数: {stats['usage_count']}")
print(f"平均质量: {stats['avg_quality']}")

# 获取最佳 Prompts
best = prompt_library.get_best_prompts('content_creation', top_n=5)
```

### 5. 规划类 Prompts

```python
from prompt_library import get_planning_prompt

# 主题分析
theme_prompt = get_planning_prompt('theme')

# 世界观构建
world_prompt = get_planning_prompt('world')

# 角色设计
character_prompt = get_planning_prompt('character')

# 故事大纲
outline_prompt = get_planning_prompt('outline')

# 章节梗概
synopsis_prompt = get_planning_prompt('synopsis')

# 基调风格
tone_prompt = get_planning_prompt('tone')

# 标题生成
title_prompt = get_planning_prompt('title')
```

### 6. 自定义 Prompt

```python
# 注册自定义 Prompt
custom_scene = """
【自定义场景模板】
...
"""

prompt_library.register_prompt('custom', 'my_scene', custom_scene)

# 使用自定义 Prompt
my_prompt = prompt_library.get_prompt('custom', 'my_scene')
```

---

## 高级功能

### 1. 质量循环集成

```python
from prompt_library import get_content_prompt
from prompts import PromptOptimizer

# 第一次生成
prompt_v1 = get_content_prompt(phase=NovelPhase.DEVELOPMENT)
# content_v1 = await llm.call(prompt_v1)

# 质量评估 (假设得分 7.5,反馈如下)
feedback = "连贯性: 6.5/10, 对话: 7.0/10"

# 第二次生成 (添加反馈)
prompt_v2 = PromptOptimizer.add_quality_feedback(prompt_v1, feedback)
# content_v2 = await llm.call(prompt_v2)

# 记录质量
prompt_library.track_prompt_usage('content_creation.phase_development', 9.0)
```

### 2. 迭代式生成

```python
# 创建迭代 Prompt
iterative_prompt = PromptOptimizer.create_iterative_prompt(
    base_prompt=base_prompt,
    iteration_num=3,
    previous_results=["第一次生成", "第二次生成"],
    best_aspects=["场景描写生动", "对话犀利"]
)
```

### 3. 重试优化

```python
# 为重试优化 Prompt
retry_prompt = PromptOptimizer.optimize_for_retry(
    original_prompt=original,
    previous_output="上一次的输出...",
    issue_description="字数不足,只有1500字"
)
```

### 4. 创造性控制

```python
# 调整创造性水平
low_creativity = PromptOptimizer.adjust_temperature_guidance(
    base_prompt,
    creativity_level='low'  # 强调准确性
)

high_creativity = PromptOptimizer.adjust_temperature_guidance(
    base_prompt,
    creativity_level='high'  # 鼓励创新
)
```

### 5. 导出/导入 Prompts

```python
# 导出 Prompts
exported = prompt_library.export_prompts('custom')

# 导入到其他项目
new_library = PromptLibrary()
count = new_library.import_prompts(exported)
```

---

## 最佳实践

### 1. 选择合适的阶段

根据章节号自动选择阶段:

```python
from prompts import PhaseCharacteristics

chapter_num = 25
phase = PhaseCharacteristics.get_phase_by_chapter(chapter_num)
# phase = NovelPhase.CLIMAX
```

### 2. 组合使用场景模板

对于特定场景,组合阶段 + 场景模板:

```python
# 第 5 章,起阶段,打脸场景
prompt = get_content_prompt(
    phase=NovelPhase.OPENING,
    scene_type='slap_face',
    context={'current_chapter': 5}
)
```

### 3. 保持用户偏好一致

为每个用户/项目保存偏好配置:

```python
user_prefs = {
    'style': '热血',
    'focus': ['打脸', '升级'],
    'avoid': ['虐主']
}

# 每次使用相同的偏好
prompt = get_content_prompt(
    phase=phase,
    user_preferences=user_prefs
)
```

### 4. 利用质量追踪优化

定期检查最佳 Prompts:

```python
# 查看哪些 Prompts 效果最好
best = prompt_library.get_best_prompts('content_creation', top_n=10)

# 优先使用高质量的 Prompts
```

### 5. 与前文保持连贯

始终提供前文内容:

```python
prompt = get_content_prompt(
    phase=phase,
    context={
        'previous_content': previous_chapter_content[-500:],  # 最后500字
        'current_chapter': chapter_num
    }
)
```

---

## API 参考

### NovelPhase (枚举)

```python
NovelPhase.OPENING       # 起 - 故事开端 (1-10章)
NovelPhase.DEVELOPMENT   # 承 - 主角成长 (11-20章)
NovelPhase.CLIMAX        # 转 - 冲突升级 (21-30章)
NovelPhase.RESOLUTION    # 合 - 势力对抗 (31-40章)
NovelPhase.ENDING        # 终 - 终极决战 (41-50章)
```

### SceneType (枚举)

```python
SceneType.SLAP_FACE      # 打脸场景
SceneType.UPGRADE        # 升级突破
SceneType.BATTLE         # 战斗场景
SceneType.REVEAL         # 真相揭露
SceneType.ALLIANCE       # 结盟
SceneType.BETRAYAL       # 背叛反转
SceneType.TREASURE       # 获得宝物
SceneType.RECOGNITION    # 身份认可
```

### ContentCreationPrompts

```python
# 获取系统 Prompt
ContentCreationPrompts.get_system_prompt() -> str

# 获取阶段 Prompt
ContentCreationPrompts.get_phase_prompt(
    phase: NovelPhase,
    context: Optional[Dict] = None
) -> str

# 获取场景 Prompt
ContentCreationPrompts.get_scene_prompt(scene_type: str) -> str

# 组合多个 Prompt
ContentCreationPrompts.get_combined_prompt(
    phase: NovelPhase,
    scene_type: Optional[str] = None,
    user_preferences: Optional[str] = None
) -> str

# 获取爽感公式
ContentCreationPrompts.get_coolness_formula() -> str
```

### NovelPlanningPrompts

```python
# 获取规划 Prompt
NovelPlanningPrompts.get_planning_prompt(planning_type: str) -> str
# planning_type: 'theme', 'world', 'character', 'outline', 'tone', 'title'

# 获取章节内容 Prompt
NovelPlanningPrompts.get_chapter_content_prompt(
    meta_info: Dict,
    chapter_synopsis: str,
    chapter_num: int
) -> str

# 获取章节梗概 Prompt
NovelPlanningPrompts.get_chapter_synopsis_prompt(
    chapter_titles: List[str]
) -> str
```

### PromptOptimizer

```python
# 添加用户偏好
PromptOptimizer.add_user_preferences(
    base_prompt: str,
    user_preferences: Dict
) -> str

# 添加质量反馈
PromptOptimizer.add_quality_feedback(
    base_prompt: str,
    feedback: str
) -> str

# 添加上下文
PromptOptimizer.add_context(
    base_prompt: str,
    context: Dict
) -> str

# 组合 Prompts
PromptOptimizer.combine_prompts(
    system_prompt: str,
    phase_prompt: str,
    user_prompt: Optional[str] = None,
    scene_prompt: Optional[str] = None
) -> str

# 优化重试
PromptOptimizer.optimize_for_retry(
    original_prompt: str,
    previous_output: str,
    issue_description: str
) -> str

# 提取关键要求
PromptOptimizer.extract_key_requirements(prompt: str) -> List[str]

# 添加示例
PromptOptimizer.add_examples(
    base_prompt: str,
    examples: List[str]
) -> str

# 调整创造性
PromptOptimizer.adjust_temperature_guidance(
    base_prompt: str,
    creativity_level: str = "medium"  # 'low', 'medium', 'high'
) -> str

# 创建迭代 Prompt
PromptOptimizer.create_iterative_prompt(
    base_prompt: str,
    iteration_num: int,
    previous_results: List[str],
    best_aspects: Optional[List[str]] = None
) -> str
```

### PromptLibrary

```python
# 注册 Prompt
prompt_library.register_prompt(
    category: str,
    subcategory: str,
    template: str
) -> bool

# 获取 Prompt
prompt_library.get_prompt(
    category: str,
    subcategory: str,
    **kwargs
) -> Optional[str]

# 列出可用 Prompts
prompt_library.list_available_prompts(
    category: Optional[str] = None
) -> Dict

# 追踪使用
prompt_library.track_prompt_usage(
    prompt_id: str,
    result_quality: float  # 0-10
)

# 获取统计
prompt_library.get_usage_stats(
    prompt_id: Optional[str] = None
) -> Dict

# 获取最佳 Prompts
prompt_library.get_best_prompts(
    category: str,
    top_n: int = 5
) -> List[Dict]

# 导出/导入
prompt_library.export_prompts(category: Optional[str] = None) -> Dict
prompt_library.import_prompts(prompts_data: Dict) -> int
```

### 便捷函数

```python
# 获取内容创作 Prompt
get_content_prompt(
    phase: Optional[NovelPhase] = None,
    scene_type: Optional[str] = None,
    user_preferences: Optional[Dict] = None,
    context: Optional[Dict] = None
) -> str

# 获取规划 Prompt
get_planning_prompt(
    planning_type: str,
    **kwargs
) -> str
```

---

## 常见问题 (FAQ)

### Q1: 如何为不同章节选择合适的阶段?

```python
from prompts import PhaseCharacteristics

# 自动根据章节号选择
phase = PhaseCharacteristics.get_phase_by_chapter(chapter_num)
```

### Q2: 如何组合多个场景类型?

多个场景可以通过 Prompt 优化器组合:

```python
base = get_content_prompt(phase=phase, scene_type='battle')
enhanced = PromptOptimizer.add_user_preferences(
    base,
    {'special_requirements': '同时包含打脸和升级元素'}
)
```

### Q3: 如何与质量循环系统集成?

```python
# 在质量循环中使用
from quality import QualityLoopManager

async def generator(**kwargs):
    prompt = get_content_prompt(**kwargs)
    return await llm.call(prompt)

result = await QualityLoopManager.run_quality_loop(
    generator,
    generator_kwargs={'phase': NovelPhase.CLIMAX}
)
```

### Q4: 如何自定义 Prompt?

```python
# 方式1: 直接注册
prompt_library.register_prompt('custom', 'my_type', "My Prompt")

# 方式2: 通过继承扩展
class MyPrompts(ContentCreationPrompts):
    MY_CUSTOM = "My Custom Prompt"
```

### Q5: Prompt 库的性能如何?

- ✅ Prompt 检索: < 0.001秒/次
- ✅ Prompt 组合: < 0.02秒/次
- ✅ 内存占用: ~5MB (包含所有 Prompts)

---

## 示例代码

完整示例请参考:
- `backend/examples/prompt_usage_examples.py` - 11个详细示例
- `backend/tests/test_prompt_library.py` - 集成测试

---

## 支持和反馈

如有问题或建议,请查阅:
- 项目文档: `docs/Agent/tasks/`
- 测试代码: `backend/tests/test_prompt_library.py`

---

**文档版本**: v1.0
**最后更新**: 2025-11-01
