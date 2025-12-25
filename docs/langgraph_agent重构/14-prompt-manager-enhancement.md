# PromptManager 增强方案

## 文档版本
- 版本：2.0
- 日期：2025-12-24
- 类型：技术方案
- 状态：⚠️ 需验证必要性

---

## 〇、前置验证

### 0.1 与 IntentClassifier 的关系

项目已有 `intent/classifier.py` 实现了意图分类功能：

```python
# intent/classifier.py
class IntentClassifier:
    def classify_by_rules(self, message: str) -> tuple[str, float]
    async def classify_by_ai(self, message: str) -> tuple[str, float]
    def detect_quick_action(self, message: str) -> Optional[dict]
```

**功能重叠分析**:

| 功能 | IntentClassifier | 本方案提议 | 重叠 |
|------|------------------|------------|------|
| 关键词检测 | `classify_by_rules()` | `detect_template()` | ⚠️ 重叠 |
| 意图识别 | 核心功能 | 触发模板加载 | ⚠️ 重叠 |
| 模板选择 | ❌ 无 | ✅ 新功能 | - |
| 摘要展示 | ❌ 无 | ✅ 新功能 | - |

### 0.2 验证问题

**需要回答的问题**:

1. **是否真正需要两级加载？**
   - 当前所有模板总 token 数是多少？
   - 每次请求平均使用多少模板？
   - 节省的 token 量是否值得增加复杂度？

2. **`detect_template()` 是否与 IntentClassifier 重复？**
   - IntentClassifier 已有规则分类
   - 是否可以复用现有分类结果？

### 0.3 建议方案

**方案 A**: 合并到 IntentClassifier（推荐）

```python
# intent/classifier.py 扩展
class IntentClassifier:
    # 现有方法...

    def get_template_for_intent(self, intent: str) -> Optional[str]:
        """根据意图返回模板名称"""
        INTENT_TEMPLATE_MAP = {
            "writing": "writing_agent",
            "planning": "planning_agent",
            "analysis": "analyze_text",
            # ...
        }
        return INTENT_TEMPLATE_MAP.get(intent)
```

**方案 B**: 独立实现（如本文档所述）

建议先验证方案 A 是否足够，再决定是否需要方案 B。

---

## 一、背景

### 1.1 为什么不新建 Skills 文件系统

原 `09-skills-mechanism.md` 规划了完整的 Skills 文件系统：
- 新建 `skills/` 目录
- 每个 skill 包含 `SKILL.md` + 附加资源
- 三级渐进式加载

经过讨论评估，这是**过度设计**，原因：
1. 项目已有完善的 PromptManager + YAML 模板系统
2. 新建系统意味着维护两套机制
3. 工期从 0.5 天增加到 1.5 天

### 1.2 现有 PromptManager 分析

**文件位置**: `backend/app/prompts/prompt_manager.py`

**现有功能**:
```python
class PromptManager:
    def __init__(self, prompts_dir):
        self.templates: Dict[str, Template] = {}  # Jinja2 模板
        self.versions: Dict[str, str] = {}        # 版本号
        self.descriptions: Dict[str, str] = {}    # 描述

    def render(self, template_name, **kwargs) -> str  # 渲染模板
    def get_version(self, template_name) -> str       # 获取版本
    def list_templates() -> Dict                      # 列出模板
```

**现有模板** (`templates/` 目录):
- `writing_agent.yaml` - 写作助手（190+ 行）
- `planning_agent.yaml` - 规划助手
- `tool_agent.yaml` - 工具调用
- `query_agent.yaml` - 问答
- `analyze_text.yaml` - 文本分析
- `intent_classifier.yaml` - 意图分类
- `system_agent_prompt.yaml` - 系统层
- `creative_writing_prompt.yaml` - 创作层

---

## 二、增强方案

### 2.1 目标

实现**两级渐进式加载**（简化版，非三级）：
- **第一级**：所有模板的摘要（始终加载到 System Prompt）
- **第二级**：检测到需要时，加载完整模板

### 2.2 YAML 格式扩展

#### 新增字段

```yaml
# 新增字段（可选，向后兼容）
triggers:          # 触发词列表
  - 续写
  - 写作
  - 改写
summary: |         # 简短摘要（~50字）
  **writing**: 小说写作能力，支持续写、改写、润色等创作操作

# 原有字段保持不变
version: "1.0"
description: "写作助手核心提示词"
template: |
  你是文枢AI...
```

#### 示例：writing_agent.yaml

```yaml
version: "1.0"
description: "写作助手核心提示词"

# 🆕 新增：渐进式加载支持
triggers:
  - 续写
  - 写作
  - 改写
  - 润色
  - 创作
  - 生成
  - 接着写
  - 继续写

summary: |
  **writing**: 小说写作能力，支持续写、改写、润色等创作操作。当用户请求写作相关任务时使用。

# 原有模板（190+ 行）
template: |
  你是文枢AI，专业的小说写作助手...
```

#### 示例：planning_agent.yaml

```yaml
version: "1.0"
description: "规划助手提示词"

triggers:
  - 大纲
  - 规划
  - 世界观
  - 设定
  - 角色
  - 人设

summary: |
  **planning**: 小说规划能力，支持大纲设计、世界观构建、角色设定等。

template: |
  你是小说架构师...
```

---

### 2.3 PromptManager 代码改动

#### 新增属性

```python
class PromptManager:
    def __init__(self, prompts_dir: Optional[str] = None):
        # 原有
        self.templates: Dict[str, Template] = {}
        self.versions: Dict[str, str] = {}
        self.descriptions: Dict[str, str] = {}

        # 🆕 新增：渐进式加载支持
        self.triggers: Dict[str, List[str]] = {}   # 触发词
        self.summaries: Dict[str, str] = {}        # 摘要

        self._load_templates()
```

#### 修改 _load_template 方法

```python
def _load_template(self, filename: str, template_name: str):
    """加载单个模板文件"""
    filepath = self.prompts_dir / filename

    with open(filepath, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    # 原有逻辑
    self.versions[template_name] = config.get("version", "1.0.0")
    self.descriptions[template_name] = config.get("description", "")

    # 🆕 新增：加载 triggers 和 summary
    self.triggers[template_name] = config.get("triggers", [])
    self.summaries[template_name] = config.get("summary", "")

    # 创建Jinja2模板
    template_str = config.get("template", "")
    if template_str:
        self.templates[template_name] = Template(template_str)
```

#### 新增方法：获取所有摘要

```python
def get_all_summaries(self) -> str:
    """
    获取所有模板的摘要（第一级，始终加载）

    Returns:
        格式化的摘要文本，用于添加到 System Prompt
    """
    lines = ["## 可用能力\n"]

    for name, summary in self.summaries.items():
        if summary and summary.strip():
            lines.append(f"- {summary.strip()}")

    if len(lines) == 1:
        return ""  # 没有摘要

    lines.append("")
    lines.append("当任务涉及上述能力时，将自动加载详细指令。")

    return "\n".join(lines)
```

#### 新增方法：检测需要加载的模板

```python
def detect_template(self, message: str) -> Optional[str]:
    """
    根据用户消息检测需要加载的模板

    Args:
        message: 用户消息文本

    Returns:
        检测到的模板名称，未检测到返回 None
    """
    message_lower = message.lower()

    for name, trigger_list in self.triggers.items():
        for trigger in trigger_list:
            if trigger.lower() in message_lower:
                return name

    return None
```

#### 新增方法：智能渲染

```python
def render_with_detection(
    self,
    message: str,
    base_prompt: str = "",
    **kwargs
) -> str:
    """
    智能渲染：基础提示 + 检测到的模板内容

    Args:
        message: 用户消息（用于检测模板）
        base_prompt: 基础 System Prompt
        **kwargs: 模板渲染参数

    Returns:
        组装后的完整 Prompt
    """
    # 第一级：基础提示 + 所有摘要
    result = base_prompt
    summaries = self.get_all_summaries()
    if summaries:
        result += "\n\n" + summaries

    # 第二级：检测并加载详细模板
    template_name = self.detect_template(message)
    if template_name:
        try:
            template_content = self.render(template_name, **kwargs)
            result += f"\n\n## 当前技能: {template_name}\n\n{template_content}"
        except Exception as e:
            print(f"警告: 加载模板 {template_name} 失败: {e}")

    return result
```

#### 新增方法：获取已加载的模板列表

```python
def get_loaded_templates(self, message: str) -> List[str]:
    """
    获取根据消息会加载的模板列表

    Args:
        message: 用户消息

    Returns:
        模板名称列表
    """
    loaded = []
    message_lower = message.lower()

    for name, trigger_list in self.triggers.items():
        for trigger in trigger_list:
            if trigger.lower() in message_lower:
                loaded.append(name)
                break  # 每个模板只加载一次

    return loaded
```

---

### 2.4 完整改动后的代码

```python
"""
Prompt模板管理器 - 增强版

支持渐进式知识披露：
- 第一级：所有模板摘要（始终加载）
- 第二级：根据触发词按需加载详细模板
"""

import yaml
from typing import Dict, Any, Optional, List
from jinja2 import Template
from pathlib import Path


class PromptManager:
    """Prompt模板管理器 - 支持渐进式加载"""

    def __init__(self, prompts_dir: Optional[str] = None):
        if prompts_dir is None:
            current_dir = Path(__file__).parent
            prompts_dir = current_dir / "templates"

        self.prompts_dir = Path(prompts_dir)

        # 原有属性
        self.templates: Dict[str, Template] = {}
        self.versions: Dict[str, str] = {}
        self.descriptions: Dict[str, str] = {}

        # 🆕 渐进式加载支持
        self.triggers: Dict[str, List[str]] = {}
        self.summaries: Dict[str, str] = {}

        self._load_templates()

    def _load_templates(self):
        """加载所有Prompt模板"""
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompt模板目录不存在: {self.prompts_dir}")

        template_files = [
            "analyze_text.yaml",
            "intent_classifier.yaml",
            "writing_agent.yaml",
            "planning_agent.yaml",
            "tool_agent.yaml",
            "query_agent.yaml",
            "system_agent_prompt.yaml",
            "creative_writing_prompt.yaml",
        ]

        for filename in template_files:
            try:
                template_name = filename.replace(".yaml", "")
                self._load_template(filename, template_name)
            except Exception as e:
                print(f"警告: 加载模板失败 {filename}: {e}")

    def _load_template(self, filename: str, template_name: str):
        """加载单个模板文件"""
        filepath = self.prompts_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"模板文件不存在: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        self.versions[template_name] = config.get("version", "1.0.0")
        self.descriptions[template_name] = config.get("description", "")

        # 🆕 加载 triggers 和 summary
        self.triggers[template_name] = config.get("triggers", [])
        self.summaries[template_name] = config.get("summary", "")

        template_str = config.get("template", "")
        if template_str:
            self.templates[template_name] = Template(template_str)
            print(f"成功加载模板: {template_name} (v{self.versions[template_name]})")

    # --- 原有方法 ---

    def render(self, template_name: str, **kwargs) -> str:
        """渲染模板"""
        template = self.templates.get(template_name)
        if not template:
            available = ", ".join(self.templates.keys())
            raise ValueError(f"模板不存在: {template_name}. 可用: {available}")
        return template.render(**kwargs)

    def get_version(self, template_name: str) -> str:
        return self.versions.get(template_name, "unknown")

    def get_description(self, template_name: str) -> str:
        return self.descriptions.get(template_name, "")

    def list_templates(self) -> Dict[str, Dict[str, str]]:
        return {
            name: {
                "version": self.versions.get(name, "unknown"),
                "description": self.descriptions.get(name, ""),
                "triggers": self.triggers.get(name, []),  # 🆕
            }
            for name in self.templates.keys()
        }

    # --- 🆕 新增方法 ---

    def get_all_summaries(self) -> str:
        """获取所有模板摘要（第一级）"""
        lines = ["## 可用能力\n"]
        for name, summary in self.summaries.items():
            if summary and summary.strip():
                lines.append(f"- {summary.strip()}")
        if len(lines) == 1:
            return ""
        lines.append("")
        lines.append("当任务涉及上述能力时，将自动加载详细指令。")
        return "\n".join(lines)

    def detect_template(self, message: str) -> Optional[str]:
        """根据消息检测模板"""
        message_lower = message.lower()
        for name, trigger_list in self.triggers.items():
            for trigger in trigger_list:
                if trigger.lower() in message_lower:
                    return name
        return None

    def render_with_detection(
        self,
        message: str,
        base_prompt: str = "",
        **kwargs
    ) -> str:
        """智能渲染：基础提示 + 检测到的模板"""
        result = base_prompt
        summaries = self.get_all_summaries()
        if summaries:
            result += "\n\n" + summaries

        template_name = self.detect_template(message)
        if template_name:
            try:
                content = self.render(template_name, **kwargs)
                result += f"\n\n## 当前技能: {template_name}\n\n{content}"
            except Exception as e:
                print(f"警告: 加载模板 {template_name} 失败: {e}")

        return result


# 全局单例
_prompt_manager_instance: Optional[PromptManager] = None

def get_prompt_manager() -> PromptManager:
    global _prompt_manager_instance
    if _prompt_manager_instance is None:
        _prompt_manager_instance = PromptManager()
    return _prompt_manager_instance
```

---

## 三、与 Agent 集成

### 3.1 在 WritingAgentGraph 中使用

```python
# langgraph_agent.py

class WritingAgentGraph:
    def __init__(self, ...):
        self.prompt_manager = get_prompt_manager()

    def _build_system_prompt(self, user_message: str) -> str:
        """构建系统提示词"""
        base_prompt = "你是文枢AI，专业的小说写作助手。"

        # 使用渐进式加载
        return self.prompt_manager.render_with_detection(
            message=user_message,
            base_prompt=base_prompt,
            # 可传入其他模板参数
            work_title=self.current_work_title,
            chapter_context=self.current_context,
        )
```

### 3.2 上下文变化示意

```
初始请求: "你好"
System Prompt:
  - 基础提示
  - 可用能力摘要 (~200 tokens)
  [无详细模板]

请求: "帮我续写一段战斗场景"
System Prompt:
  - 基础提示
  - 可用能力摘要
  - 当前技能: writing_agent (~800 tokens)  ← 自动加载

请求: "设计一个反派角色"
System Prompt:
  - 基础提示
  - 可用能力摘要
  - 当前技能: planning_agent ← 切换
```

---

## 四、测试方案

### 4.1 单元测试

```python
# tests/test_prompt_manager.py

import pytest
from app.prompts.prompt_manager import PromptManager

def test_triggers_loading():
    """测试触发词加载"""
    pm = PromptManager()

    assert "writing_agent" in pm.triggers
    assert "续写" in pm.triggers["writing_agent"]

def test_summary_loading():
    """测试摘要加载"""
    pm = PromptManager()

    assert "writing_agent" in pm.summaries
    assert "writing" in pm.summaries["writing_agent"].lower()

def test_detect_template():
    """测试模板检测"""
    pm = PromptManager()

    assert pm.detect_template("帮我续写一段") == "writing_agent"
    assert pm.detect_template("设计一个大纲") == "planning_agent"
    assert pm.detect_template("今天天气怎样") is None

def test_get_all_summaries():
    """测试摘要汇总"""
    pm = PromptManager()

    summaries = pm.get_all_summaries()
    assert "可用能力" in summaries
    assert "writing" in summaries.lower()

def test_render_with_detection():
    """测试智能渲染"""
    pm = PromptManager()

    result = pm.render_with_detection(
        message="帮我续写一段",
        base_prompt="你是文枢AI"
    )

    assert "你是文枢AI" in result
    assert "可用能力" in result
    assert "当前技能: writing_agent" in result

def test_backward_compatibility():
    """测试向后兼容（无 triggers 的模板）"""
    pm = PromptManager()

    # 即使模板没有 triggers，render 仍应正常工作
    result = pm.render("writing_agent")
    assert result  # 不为空
```

---

## 五、迁移检查清单

### 5.1 代码改动

- [ ] `prompt_manager.py` 添加 `triggers` 和 `summaries` 属性
- [ ] `prompt_manager.py` 修改 `_load_template` 方法
- [ ] `prompt_manager.py` 添加 `get_all_summaries` 方法
- [ ] `prompt_manager.py` 添加 `detect_template` 方法
- [ ] `prompt_manager.py` 添加 `render_with_detection` 方法

### 5.2 YAML 模板更新

- [ ] `writing_agent.yaml` 添加 triggers + summary
- [ ] `planning_agent.yaml` 添加 triggers + summary
- [ ] `analyze_text.yaml` 添加 triggers + summary
- [ ] `query_agent.yaml` 添加 triggers + summary

### 5.3 集成

- [ ] `langgraph_agent.py` 使用 `render_with_detection`

### 5.4 测试

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 向后兼容性验证

---

## 六、与原 Skills 方案对比

| 对比项 | 原 Skills 方案 | PromptManager 增强 |
|--------|---------------|-------------------|
| 新文件 | 15+ 个 .md 文件 | 0 |
| 新目录 | `skills/` | 无 |
| 代码行数 | ~300 行新代码 | ~50 行改动 |
| 维护成本 | 两套系统 | 一套系统 |
| 工期 | 1.5 天 | 0.5 天 |
| 功能 | 三级加载 | 两级加载（够用） |

---

**文档结束**
