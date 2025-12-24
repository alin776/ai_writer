# Skills 机制 - 渐进式知识披露

## 文档版本
- 版本：1.0
- 日期：2025-12-21
- 背景：基于《Agent 架构的探索》文章理念补充

---

## 一、为什么需要 Skills

### 1.1 当前问题

| 问题 | 现状 | 影响 |
|------|------|------|
| **Prompt 臃肿** | 所有业务知识一次性塞入 System Prompt | Token 浪费，Context 拥挤 |
| **加载不智能** | 无论任务类型，都加载全部指令 | 模型注意力分散 |
| **难以复用** | 业务知识硬编码在 YAML 中 | 无法模块化分享 |
| **扩展困难** | 新增能力需要修改核心代码 | 维护成本高 |

### 1.2 文章核心理念

> **Skills 本质上是一个多层级的文件系统，封装了指令、脚本和相关资源，让 Agent 可以动态地发现和加载这些内容。**
>
> ——《Agent 架构的探索》

### 1.3 渐进式披露原则

```
┌─────────────────────────────────────────────────────────────┐
│                     渐进式披露三级结构                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  第一级：元数据（始终加载）                                   │
│  ├── name: "writing"                                       │
│  ├── description: "小说写作能力，支持续写、改写..."          │
│  └── 作用：让 Agent 知道何时应该使用这个 Skill              │
│                                                             │
│  第二级：核心指令（按需加载）                                 │
│  ├── SKILL.md 正文                                         │
│  └── 作用：提供详细的执行指令                               │
│                                                             │
│  第三级：附加资源（仅在需要时加载）                          │
│  ├── reference.md, examples.md, scripts/                   │
│  └── 作用：提供特定场景的深入指导                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、Skills 目录结构

### 2.1 整体结构

```
backend/app/skills/
├── __init__.py                    # Skills 加载器
├── loader.py                      # SkillLoader 实现
│
├── writing/                       # 写作技能
│   ├── SKILL.md                   # 核心文件（必须）
│   ├── continue_writing.md        # 续写详细指令
│   ├── polish.md                  # 润色详细指令
│   └── scripts/
│       └── style_analyzer.py      # 风格分析脚本
│
├── planning/                      # 规划技能
│   ├── SKILL.md
│   ├── outline.md                 # 大纲规划
│   ├── worldbuilding.md           # 世界观构建
│   └── character.md               # 角色设定
│
├── analysis/                      # 分析技能
│   ├── SKILL.md
│   ├── text_analysis.md           # 文本分析
│   ├── consistency_check.md       # 一致性检查
│   └── scripts/
│       └── diff_checker.py        # 差异检查脚本
│
└── editing/                       # 编辑技能
    ├── SKILL.md
    ├── rewrite.md                 # 改写指令
    └── insert.md                  # 插入指令
```

### 2.2 SKILL.md 格式规范

```markdown
---
name: writing
version: 1.0.0
description: |
  小说写作能力，支持续写、改写、润色等操作。
  当用户请求创作、写作、续写相关任务时使用此技能。
triggers:
  - 续写
  - 写作
  - 创作
  - 生成内容
dependencies:
  - read_chapter_tool
  - get_context_tool
---

# 写作技能

你是专业的网文写作助手，擅长以下能力：

## 核心能力

1. **续写** - 根据上下文继续创作
2. **润色** - 优化文字表达
3. **风格适配** - 匹配指定写作风格

## 使用工具

- `continue_writing_tool`: 续写内容
- `smart_continue`: 智能续写（带上下文感知）

## 注意事项

- 保持角色一致性
- 遵循已有的文风
- 控制节奏感

## 详细指引

如需续写详细指令，请读取 `continue_writing.md`。
如需润色详细指令，请读取 `polish.md`。
```

---

## 三、SkillLoader 实现

### 3.1 核心类设计

```python
# skills/loader.py

from pathlib import Path
from typing import Dict, List, Optional
import yaml
import re

class Skill:
    """技能定义"""

    def __init__(self, path: Path):
        self.path = path
        self.name: str = ""
        self.version: str = ""
        self.description: str = ""
        self.triggers: List[str] = []
        self.dependencies: List[str] = []
        self.content: Optional[str] = None  # 延迟加载
        self._loaded = False

        self._parse_metadata()

    def _parse_metadata(self):
        """解析 SKILL.md 的 YAML Frontmatter"""
        skill_file = self.path / "SKILL.md"
        if not skill_file.exists():
            raise ValueError(f"SKILL.md not found in {self.path}")

        content = skill_file.read_text(encoding="utf-8")

        # 提取 YAML Frontmatter
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if match:
            metadata = yaml.safe_load(match.group(1))
            self.name = metadata.get("name", self.path.name)
            self.version = metadata.get("version", "1.0.0")
            self.description = metadata.get("description", "")
            self.triggers = metadata.get("triggers", [])
            self.dependencies = metadata.get("dependencies", [])

    def load_content(self) -> str:
        """加载核心内容（第二级）"""
        if not self._loaded:
            skill_file = self.path / "SKILL.md"
            content = skill_file.read_text(encoding="utf-8")
            # 移除 Frontmatter，保留正文
            match = re.match(r'^---\n.*?\n---\n(.*)$', content, re.DOTALL)
            self.content = match.group(1) if match else content
            self._loaded = True
        return self.content

    def load_resource(self, resource_name: str) -> Optional[str]:
        """加载附加资源（第三级）"""
        resource_path = self.path / resource_name
        if resource_path.exists():
            return resource_path.read_text(encoding="utf-8")
        return None

    def get_metadata_prompt(self) -> str:
        """生成元数据提示（用于 System Prompt）"""
        return f"- **{self.name}**: {self.description.strip()}"


class SkillLoader:
    """技能加载器"""

    def __init__(self, skills_dir: str = "backend/app/skills"):
        self.skills_dir = Path(skills_dir)
        self.skills: Dict[str, Skill] = {}
        self._load_all_skills()

    def _load_all_skills(self):
        """扫描并加载所有技能的元数据"""
        if not self.skills_dir.exists():
            return

        for skill_path in self.skills_dir.iterdir():
            if skill_path.is_dir() and (skill_path / "SKILL.md").exists():
                try:
                    skill = Skill(skill_path)
                    self.skills[skill.name] = skill
                except Exception as e:
                    print(f"Warning: Failed to load skill {skill_path}: {e}")

    def get_all_metadata_prompt(self) -> str:
        """生成所有技能的元数据提示（第一级）"""
        if not self.skills:
            return ""

        lines = ["## 可用技能", ""]
        for skill in self.skills.values():
            lines.append(skill.get_metadata_prompt())
        lines.append("")
        lines.append("当任务涉及上述技能时，请先加载对应的技能详情。")
        return "\n".join(lines)

    def should_load_skill(self, user_message: str) -> Optional[str]:
        """判断是否需要加载某个技能"""
        message_lower = user_message.lower()
        for name, skill in self.skills.items():
            for trigger in skill.triggers:
                if trigger.lower() in message_lower:
                    return name
        return None

    def load_skill(self, skill_name: str) -> Optional[str]:
        """加载技能详情（第二级）"""
        skill = self.skills.get(skill_name)
        if skill:
            return skill.load_content()
        return None

    def load_skill_resource(self, skill_name: str, resource: str) -> Optional[str]:
        """加载技能资源（第三级）"""
        skill = self.skills.get(skill_name)
        if skill:
            return skill.load_resource(resource)
        return None
```

### 3.2 与 Agent 集成

```python
# middleware/skills_middleware.py

from deepagents import AgentMiddleware
from app.skills.loader import SkillLoader

class SkillsMiddleware(AgentMiddleware):
    """Skills 中间件 - 实现渐进式知识披露"""

    def __init__(self, skills_dir: str = "backend/app/skills"):
        self.loader = SkillLoader(skills_dir)
        self.loaded_skills: set = set()  # 当前会话已加载的技能

    def get_system_prompt_extension(self) -> str:
        """返回添加到 System Prompt 的内容（第一级）"""
        return self.loader.get_all_metadata_prompt()

    def get_tools(self):
        """提供技能相关工具"""
        return [
            self._create_load_skill_tool(),
            self._create_load_resource_tool(),
        ]

    def _create_load_skill_tool(self):
        """创建加载技能工具"""
        loader = self.loader
        loaded_skills = self.loaded_skills

        def load_skill(skill_name: str) -> str:
            """加载指定技能的详细指令

            Args:
                skill_name: 技能名称（如 writing, planning, analysis）
            """
            if skill_name in loaded_skills:
                return f"技能 {skill_name} 已加载"

            content = loader.load_skill(skill_name)
            if content:
                loaded_skills.add(skill_name)
                return f"已加载技能 [{skill_name}]：\n\n{content}"
            return f"未找到技能: {skill_name}"

        return load_skill

    def _create_load_resource_tool(self):
        """创建加载资源工具"""
        loader = self.loader

        def load_skill_resource(skill_name: str, resource_name: str) -> str:
            """加载技能的附加资源

            Args:
                skill_name: 技能名称
                resource_name: 资源文件名（如 continue_writing.md）
            """
            content = loader.load_skill_resource(skill_name, resource_name)
            if content:
                return f"已加载资源 [{skill_name}/{resource_name}]：\n\n{content}"
            return f"未找到资源: {skill_name}/{resource_name}"

        return load_skill_resource

    def before_invoke(self, state, config):
        """调用前 - 自动检测是否需要加载技能"""
        messages = state.get("messages", [])
        if messages:
            last_message = messages[-1]
            content = getattr(last_message, 'content', str(last_message))

            # 检测是否需要自动加载技能
            skill_name = self.loader.should_load_skill(content)
            if skill_name and skill_name not in self.loaded_skills:
                # 自动加载相关技能到上下文
                skill_content = self.loader.load_skill(skill_name)
                if skill_content:
                    state["auto_loaded_skill"] = {
                        "name": skill_name,
                        "content": skill_content
                    }
                    self.loaded_skills.add(skill_name)

        return state
```

---

## 四、具体 Skill 示例

### 4.1 Writing Skill

```markdown
<!-- skills/writing/SKILL.md -->
---
name: writing
version: 1.0.0
description: |
  小说写作能力，支持续写、改写、润色等创作操作。
  当用户请求写作、续写、创作内容时使用此技能。
triggers:
  - 续写
  - 写作
  - 创作
  - 生成
  - 接着写
  - 继续写
dependencies:
  - continue_writing_tool
  - smart_continue
  - get_context_tool
---

# 写作技能

你是专业的网文写作助手。

## 核心原则

### 网文创作黄金法则
1. **节奏感**: 开篇抓人、中期不拖、高潮迭起
2. **爽点设计**: 打脸、逆袭、装逼、收获
3. **冲突升级**: 从小到大、层层递进
4. **金手指设定**: 合理但不无敌

### 写作质量标准
- 文字流畅自然
- 情节逻辑合理
- 角色行为一致
- 细节描写到位

## 可用工具

| 工具 | 用途 |
|------|------|
| `continue_writing_tool` | 基础续写 |
| `smart_continue` | 智能续写（带上下文感知） |
| `get_context_tool` | 获取前文上下文 |

## 执行流程

1. 使用 `get_context_tool` 获取前文
2. 分析写作风格和当前情节
3. 使用 `smart_continue` 或 `continue_writing_tool` 续写
4. 确保续写内容与前文风格一致

## 详细指引

- 续写详细指令：`continue_writing.md`
- 润色详细指令：`polish.md`
```

```markdown
<!-- skills/writing/continue_writing.md -->
# 续写详细指令

## 续写前准备

### 1. 上下文分析
- 确认当前场景（战斗/日常/对话/心理）
- 识别在场角色
- 把握当前情绪基调
- 了解未完成的情节线

### 2. 风格匹配
- 识别原文风格（轻松/严肃/幽默/热血）
- 匹配句式长度
- 保持相似的描写密度
- 延续对话风格

## 续写要点

### 情节推进
```
不要：原地打转，重复描写
要做：每段都有信息增量
```

### 节奏控制
```
紧张场景：短句、动作描写
舒缓场景：长句、心理/环境描写
```

### 衔接技巧
```
自然过渡，避免突兀转折
使用承接词："于是"、"就在这时"、"然而"
```

## 常见问题

1. **续写与原文风格不符**
   - 解决：重新阅读原文最后500字，提取关键特征

2. **情节推进过快/过慢**
   - 解决：参考原文节奏，保持相似的信息密度

3. **角色行为不一致**
   - 解决：回顾角色设定，确保行为符合人设
```

### 4.2 Planning Skill

```markdown
<!-- skills/planning/SKILL.md -->
---
name: planning
version: 1.0.0
description: |
  小说规划能力，支持大纲设计、世界观构建、角色设定等。
  当用户请求规划、设计大纲、构建世界观时使用此技能。
triggers:
  - 大纲
  - 规划
  - 世界观
  - 设定
  - 角色
  - 人设
  - 力量体系
dependencies:
  - read_chapter_tool
---

# 规划技能

你是专业的小说架构师。

## 核心能力

1. **大纲规划** - 章节结构、情节走向、节奏把控
2. **世界观设定** - 力量体系、规则体系、背景设定
3. **角色设定** - 主角、配角、反派的人物塑造
4. **情节设计** - 冲突设计、转折点、爽点布局

## 规划原则

### 大纲设计
- 开篇：建立世界观 + 主角困境
- 发展：逐级升级 + 不断打脸
- 高潮：大决战 + 真相揭示
- 结局：收尾干净 + 留有余韵

### 世界观构建
- 规则自洽，不能打脸设定
- 留有扩展空间
- 与情节相互支撑

### 角色塑造
- 主角：有明确目标、成长空间
- 配角：各有特色、功能清晰
- 反派：动机合理、实力匹配

## 详细指引

- 大纲规划：`outline.md`
- 世界观构建：`worldbuilding.md`
- 角色设定：`character.md`
```

### 4.3 Analysis Skill

```markdown
<!-- skills/analysis/SKILL.md -->
---
name: analysis
version: 1.0.0
description: |
  文本分析能力，支持文本分析、一致性检查、风格评估等。
  当用户请求分析、检查、评估文本时使用此技能。
triggers:
  - 分析
  - 检查
  - 评估
  - 问题
  - 一致性
  - 逻辑
dependencies:
  - analyze_text_tool
  - consistency_checker
---

# 分析技能

你是专业的文学分析师。

## 核心能力

1. **文本分析** - 结构、风格、情节分析
2. **一致性检查** - 人设、剧情、设定一致性
3. **质量评估** - 文笔、节奏、可读性评估

## 分析维度

### 结构分析
- 开头吸引力
- 情节推进节奏
- 高潮设置
- 结尾处理

### 人物分析
- 形象是否立体
- 行为是否合理
- 成长是否自然

### 文笔分析
- 句式变化
- 修辞运用
- 描写层次

## 输出格式

```markdown
## 分析报告

### 整体评价
[一句话概括]

### 优点
1. ...
2. ...

### 问题
1. ...
2. ...

### 改进建议
1. ...
2. ...
```

## 详细指引

- 文本分析：`text_analysis.md`
- 一致性检查：`consistency_check.md`
```

---

## 五、与现有系统集成

### 5.1 集成到 WritingAgent

```python
# writing_agent.py（更新）

from deepagents import create_deep_agent
from .tools import ALL_TOOLS
from .middleware import (
    UnifiedMemoryMiddleware,
    ModelMiddleware,
    CostMiddleware,
    IntentMiddleware,
    SkillsMiddleware,  # 新增
)

class WritingAgent:
    """基于 Deep Agents 的写作助手"""

    def __init__(self, ai_service, redis_client, checkpointer):
        self.ai_service = ai_service

        # 创建 Skills 中间件
        self.skills_middleware = SkillsMiddleware()

        # 创建中间件栈
        self.middleware = [
            self.skills_middleware,  # Skills 放在最前面
            UnifiedMemoryMiddleware(redis_client, ai_service, checkpointer),
            ModelMiddleware(ai_service),
            CostMiddleware(),
            IntentMiddleware(),
        ]

        # 创建 Agent
        self.agent = create_deep_agent(
            tools=ALL_TOOLS,
            system_prompt=self._get_system_prompt(),
            middleware=self.middleware,
            checkpointer=checkpointer,
        )

    def _get_system_prompt(self):
        """构建系统提示"""
        base_prompt = """你是文枢AI，一个专业的小说写作助手。

## 工作方式

当收到用户请求时：
1. 首先判断需要使用哪个技能
2. 使用 `load_skill` 工具加载对应技能的详细指令
3. 根据加载的指令执行任务
4. 如需更详细指导，使用 `load_skill_resource` 加载附加资源

"""
        # 添加技能元数据（第一级）
        skills_metadata = self.skills_middleware.get_system_prompt_extension()

        return base_prompt + skills_metadata
```

### 5.2 上下文管理优化

```python
# 技能加载后的上下文变化示意

# 初始状态（仅元数据）
Context: [
    System Prompt (基础 + 技能元数据),  # ~500 tokens
    User Message,
]

# 加载技能后（第二级）
Context: [
    System Prompt,
    User Message,
    Tool Call: load_skill("writing"),
    Tool Result: [SKILL.md 内容],  # ~800 tokens
]

# 加载资源后（第三级）
Context: [
    System Prompt,
    User Message,
    Tool Call: load_skill("writing"),
    Tool Result: [SKILL.md 内容],
    Tool Call: load_skill_resource("writing", "continue_writing.md"),
    Tool Result: [continue_writing.md 内容],  # ~500 tokens
]
```

---

## 六、与文章理念对照

### 6.1 渐进式披露实现

| 文章描述 | 本方案实现 |
|---------|-----------|
| 元数据预加载到 System Prompt | ✅ `get_all_metadata_prompt()` |
| SKILL.md 按需加载 | ✅ `load_skill()` 工具 |
| 附加文件仅在需要时加载 | ✅ `load_skill_resource()` 工具 |

### 6.2 优势对比

| 方面 | 改进前 | 改进后 |
|------|--------|--------|
| **Token 消耗** | 一次性加载 ~3000 tokens | 按需加载，平均 ~800 tokens |
| **模型注意力** | 分散在大量无关指令 | 聚焦于当前任务相关指令 |
| **可维护性** | 修改需改代码 | 修改 .md 文件即可 |
| **可复用性** | 无法复用 | Skill 文件夹可直接复制 |
| **扩展性** | 需改核心代码 | 新建 Skill 文件夹即可 |

---

## 七、测试方案

### 7.1 单元测试

```python
# tests/test_skills.py

import pytest
from app.skills.loader import SkillLoader, Skill

def test_skill_metadata_parsing():
    """测试 Skill 元数据解析"""
    loader = SkillLoader()

    # 验证技能加载
    assert "writing" in loader.skills
    assert "planning" in loader.skills
    assert "analysis" in loader.skills

    # 验证元数据
    writing_skill = loader.skills["writing"]
    assert writing_skill.name == "writing"
    assert "续写" in writing_skill.triggers


def test_skill_content_loading():
    """测试 Skill 内容加载"""
    loader = SkillLoader()

    # 加载技能内容
    content = loader.load_skill("writing")
    assert content is not None
    assert "写作技能" in content


def test_skill_resource_loading():
    """测试资源加载"""
    loader = SkillLoader()

    # 加载附加资源
    resource = loader.load_skill_resource("writing", "continue_writing.md")
    assert resource is not None
    assert "续写" in resource


def test_trigger_detection():
    """测试触发词检测"""
    loader = SkillLoader()

    # 测试各种触发词
    assert loader.should_load_skill("帮我续写一段") == "writing"
    assert loader.should_load_skill("设计一个大纲") == "planning"
    assert loader.should_load_skill("分析这段文字") == "analysis"
    assert loader.should_load_skill("今天天气怎么样") is None
```

### 7.2 集成测试

```python
@pytest.mark.asyncio
async def test_skill_loading_in_agent():
    """测试 Agent 中的技能加载"""
    agent = create_writing_agent(...)

    # 发送需要写作技能的请求
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": "帮我续写一段战斗场景"}]
    })

    # 验证技能被加载
    messages = result.get("messages", [])
    tool_calls = [m for m in messages if hasattr(m, 'tool_calls')]

    # 应该调用了 load_skill
    assert any("load_skill" in str(tc) for tc in tool_calls)
```

---

## 八、迁移检查清单

### 8.1 Skills 框架

- [ ] `skills/` 目录结构创建
- [ ] `Skill` 类实现
- [ ] `SkillLoader` 类实现
- [ ] 元数据解析功能
- [ ] 内容加载功能
- [ ] 资源加载功能

### 8.2 具体 Skills

- [ ] `writing/SKILL.md` 编写
- [ ] `writing/continue_writing.md` 编写
- [ ] `planning/SKILL.md` 编写
- [ ] `analysis/SKILL.md` 编写
- [ ] `editing/SKILL.md` 编写

### 8.3 集成

- [ ] `SkillsMiddleware` 开发
- [ ] `WritingAgent` 集成
- [ ] System Prompt 更新
- [ ] 工具注册

### 8.4 测试

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 渐进式加载验证
- [ ] Token 消耗对比

---

## 九、下一步

阅读 `07-implementation-plan.md` 中的 Phase 3.5 了解 Skills 机制的具体实施时间安排。

---

## 十、参考资料

### A. 相关文章

- 《Agent 架构的探索》- Skills 理念来源
- Anthropic Blog: [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

### B. 相关文档

- [00-overview.md](./00-overview.md) - 重构概述
- [03-migration-strategy.md](./03-migration-strategy.md) - 迁移策略
- [05-memory-integration.md](./05-memory-integration.md) - 记忆系统集成
