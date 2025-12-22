# Phase 3.5 补充计划 - Skills 机制实施

## 文档版本
- 版本：1.0
- 日期：2025-12-21
- 说明：本文档是 `07-implementation-plan.md` 的补充，新增 Skills 机制实施阶段

---

## 一、计划调整说明

### 1.1 调整背景

基于《Agent 架构的探索》文章理念，原重构计划缺少 **Skills 机制**（渐进式知识披露）。为符合行业最佳实践，在 Phase 3（中间件开发）和 Phase 4（核心替换）之间新增 **Phase 3.5: Skills 机制**。

### 1.2 时间线调整

```
原计划：15 天
├─ Phase 1: 准备 (Day 1-2)
├─ Phase 2: 工具 (Day 3-5)
├─ Phase 3: 中间件 (Day 6-9)
├─ Phase 4: 核心 (Day 10-12)
├─ Phase 5: 测试 (Day 13-14)
└─ Phase 6: 上线 (Day 15)

调整后：18 天
├─ Phase 1: 准备 (Day 1-2)
├─ Phase 2: 工具 (Day 3-5)
├─ Phase 3: 中间件 (Day 6-9)
├─ Phase 3.5: Skills (Day 10-12) ⭐新增
├─ Phase 4: 核心 (Day 13-15)
├─ Phase 5: 测试 (Day 16-17)
└─ Phase 6: 上线 (Day 18)
```

### 1.3 新增工期理由

| 任务 | 工期 | 理由 |
|------|------|------|
| Skills 框架开发 | 1.5 天 | SkillLoader、Skill 类实现 |
| 核心 Skills 编写 | 1 天 | writing、planning、analysis |
| SkillsMiddleware | 0.5 天 | 与 Agent 集成 |

---

## 二、Phase 3.5: Skills 机制 (Day 10-12)

### 2.1 目标

- 实现渐进式知识披露机制
- 开发 SkillLoader 和 Skill 类
- 编写 4 个核心 Skills
- 开发 SkillsMiddleware 并集成

### 2.2 任务清单

#### Day 10 - Skills 框架

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| 创建 `skills/` 目录结构 | 0.5h | 目录结构符合设计 |
| 实现 `Skill` 类 | 2h | 单测通过 |
| 实现 `SkillLoader` 类 | 2h | 单测通过 |
| 元数据解析功能 | 1h | YAML Frontmatter 正确解析 |
| 内容加载功能 | 0.5h | 按需加载正常 |

#### Day 11 - 核心 Skills 编写

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `writing/SKILL.md` | 2h | 包含网文创作知识 |
| `writing/continue_writing.md` | 1h | 续写详细指令 |
| `planning/SKILL.md` | 1.5h | 包含规划知识 |
| `analysis/SKILL.md` | 1h | 包含分析知识 |
| `editing/SKILL.md` | 0.5h | 包含编辑知识 |

#### Day 12 - 中间件集成

| 任务 | 预计时间 | 验收标准 |
|------|----------|----------|
| `SkillsMiddleware` 开发 | 2h | 单测通过 |
| `load_skill` 工具实现 | 1h | 可加载技能详情 |
| `load_skill_resource` 工具实现 | 1h | 可加载附加资源 |
| 与 WritingAgent 集成 | 1h | 技能可被调用 |
| 集成测试 | 1h | 渐进式加载验证 |

### 2.3 交付物

```
backend/app/skills/
├── __init__.py                    # 导出
├── loader.py                      # SkillLoader 实现
│
├── writing/                       # 写作技能
│   ├── SKILL.md                   # 核心文件
│   ├── continue_writing.md        # 续写详细指令
│   └── polish.md                  # 润色详细指令
│
├── planning/                      # 规划技能
│   ├── SKILL.md
│   ├── outline.md
│   └── worldbuilding.md
│
├── analysis/                      # 分析技能
│   ├── SKILL.md
│   └── consistency_check.md
│
└── editing/                       # 编辑技能
    ├── SKILL.md
    └── rewrite.md

backend/app/services/agent/middleware/
└── skills_middleware.py           # 新增

backend/app/services/agent/tests/
├── test_skill_loader.py           # 新增
└── test_skills_middleware.py      # 新增
```

### 2.4 核心代码结构

```python
# skills/loader.py

class Skill:
    """技能定义"""
    def __init__(self, path: Path): ...
    def _parse_metadata(self): ...       # 解析 YAML Frontmatter
    def load_content(self) -> str: ...   # 加载核心内容（第二级）
    def load_resource(self, name) -> str: ...  # 加载附加资源（第三级）
    def get_metadata_prompt(self) -> str: ...  # 生成元数据提示


class SkillLoader:
    """技能加载器"""
    def __init__(self, skills_dir: str): ...
    def _load_all_skills(self): ...      # 扫描加载所有技能元数据
    def get_all_metadata_prompt(self) -> str: ...  # 生成系统提示扩展
    def should_load_skill(self, msg) -> str: ...   # 判断是否需要加载
    def load_skill(self, name) -> str: ...         # 加载技能详情
    def load_skill_resource(self, name, res) -> str: ...  # 加载资源
```

```python
# middleware/skills_middleware.py

class SkillsMiddleware(AgentMiddleware):
    """Skills 中间件"""

    def get_system_prompt_extension(self) -> str: ...  # 第一级：元数据
    def get_tools(self) -> list: ...  # 提供 load_skill, load_skill_resource
    def before_invoke(self, state, config): ...  # 自动检测技能需求
```

### 2.5 验收检查

- [ ] `skills/` 目录结构创建完成
- [ ] `Skill` 类单元测试通过
- [ ] `SkillLoader` 类单元测试通过
- [ ] 4 个核心 Skills 编写完成
- [ ] `SkillsMiddleware` 单元测试通过
- [ ] 渐进式加载集成测试通过
- [ ] Token 消耗对比测试（预期节省 ~60%）

---

## 三、里程碑更新

| 里程碑 | 原计划 | 调整后 | 关键交付物 |
|--------|--------|--------|-----------|
| M1: 准备完成 | Day 2 | Day 2 | 目录结构、测试框架 |
| M2: 工具迁移完成 | Day 5 | Day 5 | 14 工具适配完成 |
| M3: 中间件完成 | Day 9 | Day 9 | 8 个中间件开发完成 |
| **M3.5: Skills 完成** | - | **Day 12** | **Skills 机制可用** ⭐新增 |
| M4: 核心替换完成 | Day 12 | Day 15 | WritingAgent 可用 |
| M5: 测试通过 | Day 14 | Day 17 | 所有测试通过 |
| M6: 上线完成 | Day 15 | Day 18 | 全量发布成功 |

---

## 四、风险评估补充

| 风险 | 概率 | 影响 | 预案 |
|------|------|------|------|
| Skills 触发不准确 | 中 | 低 | 调整触发词，增加 fallback |
| 非 Claude 模型兼容性差 | 高 | 中 | 针对不同模型调整 Prompt |
| 技能加载延迟 | 低 | 低 | 缓存已加载技能 |

---

## 五、与原计划的关系

本文档是 `07-implementation-plan.md` 的**补充**，而非替代。阅读顺序：

1. 先阅读 `07-implementation-plan.md` 了解整体计划
2. 再阅读本文档了解 Phase 3.5 详细内容
3. 参考 `09-skills-mechanism.md` 了解 Skills 技术细节

---

## 六、参考文档

- [07-implementation-plan.md](./07-implementation-plan.md) - 原实施计划
- [09-skills-mechanism.md](./09-skills-mechanism.md) - Skills 机制详细设计
- [05-memory-integration.md](./05-memory-integration.md) - 中间件开发参考
