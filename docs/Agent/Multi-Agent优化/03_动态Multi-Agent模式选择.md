# 动态 Multi-Agent 模式选择设计文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 版本 | v1.1.0 |
| 创建日期 | 2025-12-07 |
| 更新日期 | 2025-12-07 |
| 状态 | 设计中 |
| 优先级 | P1 - 性能优化 |

---

## 1. 问题背景

### 1.1 当前问题

> **代码位置**：`backend/app/services/agent/multi_agent/executor.py`
>
> **现状**：所有写作任务均调用 `_execute_internal()` 走完整 5 阶段流程，无模式选择机制。

```
当前 Multi-Agent 流程（固定 5 阶段）：

┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│ 大纲师  │ → │  主笔   │ → │角色守护 │ → │逻辑审计 │ → │  总编   │
│  40s   │   │  80s   │   │  30s   │   │  30s   │   │  25s   │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘

总耗时：约 180 秒（3 分钟）
LLM 调用次数：5 次
```

**问题**：所有写作任务都走完整 5 阶段流程，但：

| 任务类型 | 实际需要 | 当前处理 | 问题 |
|---------|---------|---------|------|
| 润色 200 字 | 1 次 LLM | 5 次 LLM | 过度处理 |
| 写一段对话 | 1-2 次 LLM | 5 次 LLM | 过度处理 |
| 写一个场景 | 3 次 LLM | 5 次 LLM | 略微过度 |
| 写完整章节 | 5 次 LLM | 5 次 LLM | 合适 |

### 1.2 设计目标

根据任务复杂度动态选择处理模式：

```
Lite 模式 (30-60s)     Standard 模式 (60-120s)    Full 模式 (120-180s)
      │                       │                          │
      │   短内容/简单任务      │   中等内容/标准任务       │   长内容/复杂任务
      │                       │                          │
      ▼                       ▼                          ▼
  ┌───────┐              ┌───────┐                 ┌───────┐
  │大纲(可选)│            │ 大纲  │                 │ 大纲  │
  └───┬───┘              └───┬───┘                 └───┬───┘
      │                      │                         │
      ▼                      ▼                         ▼
  ┌───────┐              ┌───────┐                 ┌───────┐
  │ 主笔  │              │ 主笔  │                 │ 主笔  │
  └───┬───┘              └───┬───┘                 └───┬───┘
      │                      │                         │
      ▼                      ├────────┐                ├────────┐
   完成                      ▼        ▼                ▼        ▼
                         ┌───────┐ ┌───────┐      ┌───────┐ ┌───────┐
                         │角色守护│ │逻辑审计│      │角色守护│ │逻辑审计│
                         └───┬───┘ └───┬───┘      └───┬───┘ └───┬───┘
                             │        │                │        │
                             └────┬───┘                └────┬───┘
                                  │                         │
                                  ▼                         ▼
                               完成                     ┌───────┐
                            (审查警告)                  │ 总编  │
                                                       └───┬───┘
                                                           │
                                                           ▼
                                                        完成
```

---

## 2. 模式定义

### 2.1 三种模式对比

| 属性 | Lite 模式 | Standard 模式 | Full 模式 |
|------|-----------|---------------|-----------|
| **适用场景** | 短内容、简单任务 | 中等内容、标准任务 | 长内容、复杂任务 |
| **目标字数** | < 500 字 | 500-1500 字 | > 1500 字 |
| **阶段数** | 1-2 | 4 | 5 |
| **LLM 调用** | 1-2 次 | 4 次 | 5 次 |
| **预计耗时** | 30-60 秒 | 60-120 秒 | 120-180 秒 |
| **质量评分上限** | 0.80 | 0.85 | 1.00 |
| **是否修订** | 否 | 否（仅警告） | 是 |

### 2.2 阶段配置

```python
MODE_STAGES = {
    "lite": {
        "stages": [1, 2],                    # 大纲(可选) + 主笔
        "optional_stages": [1],              # 大纲可跳过
        "skip_revision": True,
        "max_quality_score": 0.80,
    },
    "standard": {
        "stages": [1, 2, 3, 4],              # 大纲 + 主笔 + 并行审查
        "optional_stages": [],
        "skip_revision": True,               # 审查不修订，只返回警告
        "max_quality_score": 0.85,
    },
    "full": {
        "stages": [1, 2, 3, 4, 5],           # 完整 5 阶段
        "optional_stages": [],
        "skip_revision": False,              # 有问题时修订
        "max_quality_score": 1.00,
    },
}
```

---

## 3. 模式判断逻辑

### 3.1 判断维度

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           模式判断流程                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
              ┌──────────┐   ┌──────────┐   ┌──────────┐
              │ 目标字数 │   │ 任务类型 │   │ 上下文   │
              │ 判断     │   │ 判断     │   │ 复杂度   │
              └────┬─────┘   └────┬─────┘   └────┬─────┘
                   │              │              │
                   └──────────────┴──────────────┘
                                  │
                                  ▼
                         ┌───────────────┐
                         │ 综合决策      │
                         │ (取最高模式)  │
                         └───────┬───────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
               lite        standard        full
```

### 3.2 判断规则

#### 规则 1: 目标字数

```python
def _judge_by_word_count(self, task: Dict) -> str:
    """按目标字数判断模式"""
    target_words = self._get_target_words(task)

    if target_words is None:
        return "unknown"

    if target_words < 500:
        return "lite"
    elif target_words < 1500:
        return "standard"
    else:
        return "full"
```

#### 规则 2: 任务类型

```python
TASK_TYPE_MODE_MAP = {
    # Lite 模式任务
    "polish": "lite",           # 润色
    "expand": "lite",           # 扩写一小段
    "dialogue": "lite",         # 写一段对话
    "description": "lite",      # 写一段描写

    # Standard 模式任务
    "scene": "standard",        # 写一个场景
    "transition": "standard",   # 过渡段落
    "flashback": "standard",    # 回忆片段

    # Full 模式任务
    "chapter": "full",          # 写整章
    "climax": "full",           # 高潮戏
    "battle": "full",           # 战斗场面
    "finale": "full",           # 结局
}

def _judge_by_task_type(self, task: Dict) -> str:
    """按任务类型判断模式"""
    task_type = self._infer_task_type(task.get("description", ""))
    return TASK_TYPE_MODE_MAP.get(task_type, "unknown")
```

#### 规则 3: 上下文复杂度

```python
def _judge_by_complexity(self, context: Dict) -> str:
    """按上下文复杂度判断模式"""
    score = 0

    # 涉及角色数量
    characters = context.get("key_characters", [])
    if len(characters) > 3:
        score += 2
    elif len(characters) > 1:
        score += 1

    # 是否有伏笔/悬念要承接
    if context.get("pending_foreshadowing"):
        score += 2

    # 是否是关键情节点
    if context.get("is_key_plot_point"):
        score += 2

    # 是否需要多视角
    if context.get("multi_perspective"):
        score += 1

    # 评分转模式
    if score >= 4:
        return "full"
    elif score >= 2:
        return "standard"
    else:
        return "lite"
```

### 3.3 综合决策

```python
def _determine_mode(
    self,
    task: Dict,
    context: Dict
) -> Literal["lite", "standard", "full"]:
    """综合判断执行模式

    判断优先级：
    1. 用户强制指定 > 其他
    2. 多维度判断取最高模式

    Returns:
        执行模式
    """

    # 1. 用户强制指定（最高优先级）
    if task.get("force_mode"):
        mode = task["force_mode"]
        logger.info(f"[ModeSelector] 用户强制指定模式: {mode}")
        return mode

    # 2. 多维度判断
    modes = []

    # 字数判断
    word_mode = self._judge_by_word_count(task)
    if word_mode != "unknown":
        modes.append(word_mode)
        logger.info(f"[ModeSelector] 字数判断: {word_mode}")

    # 任务类型判断
    type_mode = self._judge_by_task_type(task)
    if type_mode != "unknown":
        modes.append(type_mode)
        logger.info(f"[ModeSelector] 类型判断: {type_mode}")

    # 复杂度判断
    complexity_mode = self._judge_by_complexity(context)
    modes.append(complexity_mode)
    logger.info(f"[ModeSelector] 复杂度判断: {complexity_mode}")

    # 3. 取最高模式（保守策略：宁可过度处理，不可质量不足）
    MODE_PRIORITY = {"lite": 1, "standard": 2, "full": 3}

    if not modes:
        logger.warning("[ModeSelector] 无法判断模式，默认使用 standard")
        return "standard"

    final_mode = max(modes, key=lambda m: MODE_PRIORITY.get(m, 0))
    logger.info(f"[ModeSelector] 最终模式: {final_mode} (候选: {modes})")

    return final_mode
```

---

## 4. 字数提取逻辑

### 4.1 从任务描述提取

```python
def _get_target_words(self, task: Dict) -> Optional[int]:
    """提取或推断目标字数

    支持的表达方式：
    - 直接指定: {"target_words": 500}
    - 描述中提取: "写500字"、"1000字左右"
    - 关键词推断: "写一段"、"写一章"

    Returns:
        目标字数，无法判断时返回 None
    """

    # 1. 直接指定
    if task.get("target_words"):
        return task["target_words"]

    # 2. 从描述中提取
    desc = task.get("description", "")

    # 匹配 "写500字"、"1000字左右"、"约2000字" 等
    import re
    patterns = [
        r'(\d+)\s*字',           # 500字
        r'约\s*(\d+)\s*字',      # 约500字
        r'(\d+)\s*字左右',       # 500字左右
        r'(\d+)-(\d+)\s*字',     # 500-800字 (取中间值)
    ]

    for pattern in patterns:
        match = re.search(pattern, desc)
        if match:
            groups = match.groups()
            if len(groups) == 2:
                # 范围取中间值
                return (int(groups[0]) + int(groups[1])) // 2
            else:
                return int(groups[0])

    # 3. 关键词推断
    KEYWORD_WORD_COUNT = {
        # 短内容
        r'一段|一小段|几句': 300,
        r'一句话|一两句': 50,

        # 中等内容
        r'一节|一小节': 800,
        r'一个场景': 600,

        # 长内容
        r'一章|整章|完整章节': 3000,
        r'两章|三章': 6000,
    }

    for pattern, word_count in KEYWORD_WORD_COUNT.items():
        if re.search(pattern, desc):
            return word_count

    return None
```

### 4.2 从任务类型推断

```python
TASK_TYPE_WORD_COUNT = {
    "polish": 200,       # 润色通常是短内容
    "expand": 300,       # 扩写一小段
    "dialogue": 400,     # 一段对话
    "description": 300,  # 一段描写
    "scene": 800,        # 一个场景
    "transition": 500,   # 过渡段落
    "chapter": 3000,     # 整章
    "battle": 2000,      # 战斗场面
}

def _infer_word_count_by_type(self, task_type: str) -> Optional[int]:
    """根据任务类型推断字数"""
    return TASK_TYPE_WORD_COUNT.get(task_type)
```

---

## 5. 任务类型识别

### 5.1 关键词匹配

```python
TASK_TYPE_KEYWORDS = {
    "polish": ["润色", "优化", "改进", "修饰", "美化"],
    "expand": ["扩写", "展开", "详细写", "丰富"],
    "dialogue": ["对话", "对白", "交谈", "说话"],
    "description": ["描写", "描述", "刻画"],
    "scene": ["场景", "一幕", "画面"],
    "transition": ["过渡", "衔接", "承接"],
    "flashback": ["回忆", "闪回", "往事"],
    "chapter": ["一章", "整章", "第.*章", "章节"],
    "climax": ["高潮", "决战", "最终"],
    "battle": ["战斗", "打斗", "交战", "对决"],
    "finale": ["结局", "结尾", "收尾", "大结局"],
}

def _infer_task_type(self, description: str) -> str:
    """从描述推断任务类型

    Args:
        description: 任务描述

    Returns:
        任务类型，无法识别时返回 "unknown"
    """
    import re

    for task_type, keywords in TASK_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if re.search(keyword, description):
                return task_type

    return "unknown"
```

---

## 6. 代码实现

### 6.1 模式选择器类

```python
# 文件: backend/app/services/agent/multi_agent/mode_selector.py

from typing import Dict, Optional, Literal
import re
import logging

logger = logging.getLogger(__name__)


class ModeSelector:
    """Multi-Agent 执行模式选择器

    根据任务特征动态选择最优执行模式：
    - lite: 轻量模式，1-2 阶段
    - standard: 标准模式，4 阶段
    - full: 完整模式，5 阶段
    """

    # 模式配置
    MODE_CONFIG = {
        "lite": {
            "stages": [1, 2],
            "optional_stages": [1],
            "skip_revision": True,
            "max_quality_score": 0.80,
            "description": "轻量模式（大纲可选 + 主笔）",
        },
        "standard": {
            "stages": [1, 2, 3, 4],
            "optional_stages": [],
            "skip_revision": True,
            "max_quality_score": 0.85,
            "description": "标准模式（大纲 + 主笔 + 并行审查）",
        },
        "full": {
            "stages": [1, 2, 3, 4, 5],
            "optional_stages": [],
            "skip_revision": False,
            "max_quality_score": 1.00,
            "description": "完整模式（全 5 阶段）",
        },
    }

    # 字数阈值
    WORD_THRESHOLDS = {
        "lite": 500,
        "standard": 1500,
    }

    # 任务类型映射
    TASK_TYPE_MODE_MAP = {
        # Lite
        "polish": "lite",
        "expand": "lite",
        "dialogue": "lite",
        "description": "lite",
        # Standard
        "scene": "standard",
        "transition": "standard",
        "flashback": "standard",
        # Full
        "chapter": "full",
        "climax": "full",
        "battle": "full",
        "finale": "full",
    }

    # 任务类型关键词
    TASK_TYPE_KEYWORDS = {
        "polish": ["润色", "优化", "改进", "修饰"],
        "expand": ["扩写", "展开", "详细写"],
        "dialogue": ["对话", "对白", "交谈"],
        "description": ["描写", "描述", "刻画"],
        "scene": ["场景", "一幕", "画面"],
        "transition": ["过渡", "衔接", "承接"],
        "flashback": ["回忆", "闪回", "往事"],
        "chapter": ["一章", "整章", "第.*章"],
        "climax": ["高潮", "决战", "最终"],
        "battle": ["战斗", "打斗", "交战", "对决"],
        "finale": ["结局", "结尾", "大结局"],
    }

    def select(
        self,
        task: Dict,
        context: Dict
    ) -> Literal["lite", "standard", "full"]:
        """选择执行模式

        Args:
            task: 任务信息
            context: 上下文信息

        Returns:
            执行模式
        """
        return self._determine_mode(task, context)

    def get_config(self, mode: str) -> Dict:
        """获取模式配置"""
        return self.MODE_CONFIG.get(mode, self.MODE_CONFIG["standard"])

    def _determine_mode(
        self,
        task: Dict,
        context: Dict
    ) -> Literal["lite", "standard", "full"]:
        """综合判断执行模式"""

        # 1. 用户强制指定
        if task.get("force_mode"):
            mode = task["force_mode"]
            if mode in self.MODE_CONFIG:
                logger.info(f"[ModeSelector] 用户强制指定: {mode}")
                return mode

        # 2. 多维度判断
        modes = []

        # 字数判断
        word_mode = self._judge_by_word_count(task)
        if word_mode:
            modes.append(("word_count", word_mode))

        # 任务类型判断
        type_mode = self._judge_by_task_type(task)
        if type_mode:
            modes.append(("task_type", type_mode))

        # 复杂度判断
        complexity_mode = self._judge_by_complexity(context)
        modes.append(("complexity", complexity_mode))

        # 3. 记录判断过程
        for source, mode in modes:
            logger.info(f"[ModeSelector] {source} → {mode}")

        # 4. 取最高模式
        MODE_PRIORITY = {"lite": 1, "standard": 2, "full": 3}
        mode_values = [m for _, m in modes]

        if not mode_values:
            final_mode = "standard"
        else:
            final_mode = max(mode_values, key=lambda m: MODE_PRIORITY.get(m, 0))

        logger.info(f"[ModeSelector] 最终选择: {final_mode}")
        return final_mode

    def _judge_by_word_count(self, task: Dict) -> Optional[str]:
        """按目标字数判断"""
        target_words = self._get_target_words(task)

        if target_words is None:
            return None

        if target_words < self.WORD_THRESHOLDS["lite"]:
            return "lite"
        elif target_words < self.WORD_THRESHOLDS["standard"]:
            return "standard"
        else:
            return "full"

    def _judge_by_task_type(self, task: Dict) -> Optional[str]:
        """按任务类型判断"""
        task_type = self._infer_task_type(task.get("description", ""))
        return self.TASK_TYPE_MODE_MAP.get(task_type)

    def _judge_by_complexity(self, context: Dict) -> str:
        """按上下文复杂度判断"""
        score = 0

        # 角色数量
        characters = context.get("key_characters", [])
        if len(characters) > 3:
            score += 2
        elif len(characters) > 1:
            score += 1

        # 伏笔/悬念
        if context.get("pending_foreshadowing"):
            score += 2

        # 关键情节点
        if context.get("is_key_plot_point"):
            score += 2

        # 多视角
        if context.get("multi_perspective"):
            score += 1

        if score >= 4:
            return "full"
        elif score >= 2:
            return "standard"
        else:
            return "lite"

    def _get_target_words(self, task: Dict) -> Optional[int]:
        """提取目标字数"""
        # 直接指定
        if task.get("target_words"):
            return task["target_words"]

        desc = task.get("description", "")

        # 正则匹配
        patterns = [
            (r'(\d+)\s*字', 1),
            (r'约\s*(\d+)\s*字', 1),
            (r'(\d+)\s*字左右', 1),
            (r'(\d+)-(\d+)\s*字', 2),
        ]

        for pattern, group_count in patterns:
            match = re.search(pattern, desc)
            if match:
                if group_count == 2:
                    return (int(match.group(1)) + int(match.group(2))) // 2
                else:
                    return int(match.group(1))

        # 关键词推断
        keyword_map = {
            r'一段|一小段|几句': 300,
            r'一节|一小节': 800,
            r'一章|整章|完整章节': 3000,
        }

        for pattern, word_count in keyword_map.items():
            if re.search(pattern, desc):
                return word_count

        return None

    def _infer_task_type(self, description: str) -> str:
        """推断任务类型"""
        for task_type, keywords in self.TASK_TYPE_KEYWORDS.items():
            for keyword in keywords:
                if re.search(keyword, description):
                    return task_type
        return "unknown"
```

### 6.2 executor.py 集成

```python
# 文件: backend/app/services/agent/multi_agent/executor.py

from .mode_selector import ModeSelector


class MultiAgentExecutor:

    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.mode_selector = ModeSelector()
        # ... 初始化各 Agent ...

    async def execute(
        self,
        task: Dict[str, Any],
        work_id: str,
        chapter_id: str,
        context: Dict[str, Any],
        on_event: Optional[Callable[[Dict], Awaitable[None]]] = None
    ) -> Dict[str, Any]:
        """执行写作任务

        根据任务特征自动选择执行模式。
        """

        # 1. 选择执行模式
        mode = self.mode_selector.select(task, context)
        mode_config = self.mode_selector.get_config(mode)

        logger.info(
            f"[MultiAgent] 模式: {mode} ({mode_config['description']}), "
            f"阶段: {mode_config['stages']}"
        )

        # 2. 按模式执行
        try:
            if mode == "lite":
                return await self._execute_lite(task, context, on_event, mode_config)
            elif mode == "standard":
                return await self._execute_standard(task, work_id, context, on_event, mode_config)
            else:
                return await self._execute_full(task, work_id, chapter_id, context, on_event, mode_config)

        except asyncio.TimeoutError:
            logger.error(f"[MultiAgent] 执行超时 (mode={mode})")
            raise TimeoutError(f"Multi-Agent 写作流程超时")

    async def _execute_lite(
        self,
        task: Dict,
        context: Dict,
        on_event: Optional[Callable],
        config: Dict
    ) -> Dict[str, Any]:
        """Lite 模式执行：大纲(可选) + 主笔"""

        stages = [s for s in config["stages"] if s not in config.get("optional_stages", [])]

        # 发送计划（只包含实际执行的阶段）
        await self._send_plan_event(on_event, stages=config["stages"])

        # 阶段1: 大纲（可选）
        outline = None
        if 1 in config["stages"]:
            if self._needs_outline(task):
                await self._report_event(on_event, "task_start", 1, "快速构思中...")
                start_time = time.time()
                outline = await self._quick_outline(task, context)
                await self._report_event(on_event, "task_done", 1, elapsed_time=time.time() - start_time)
            else:
                # 跳过大纲
                await self._report_event(on_event, "task_start", 1, "跳过大纲")
                await self._report_event(on_event, "task_done", 1, elapsed_time=0)
                outline = {"structure": "直接写作", "key_points": []}

        # 阶段2: 主笔
        await self._report_event(on_event, "task_start", 2, "撰写中...")
        start_time = time.time()
        draft = await self.writer_agent.write(outline or {}, context)
        await self._report_event(on_event, "task_done", 2, elapsed_time=time.time() - start_time)

        # 直接返回，不审查不修订
        return {
            "content": draft.get("content", ""),
            "word_count": draft.get("word_count", 0),
            "mode": "lite",
            "quality_score": min(0.80, config["max_quality_score"]),
            "stages_executed": config["stages"],
        }

    async def _execute_standard(
        self,
        task: Dict,
        work_id: str,
        context: Dict,
        on_event: Optional[Callable],
        config: Dict
    ) -> Dict[str, Any]:
        """Standard 模式执行：大纲 + 主笔 + 并行审查（不修订）"""

        await self._send_plan_event(on_event, stages=config["stages"])

        # 阶段1: 大纲
        await self._report_event(on_event, "task_start", 1, "规划结构中...")
        start_time = time.time()
        outline = await self.outline_agent.generate(task, context)
        await self._report_event(on_event, "task_done", 1, elapsed_time=time.time() - start_time)

        # 阶段2: 主笔
        await self._report_event(on_event, "task_start", 2, "撰写中...")
        start_time = time.time()
        draft = await self.writer_agent.write(outline, context)
        await self._report_event(on_event, "task_done", 2, elapsed_time=time.time() - start_time)

        # 阶段3&4: 并行审查
        await self._report_event(on_event, "task_start", 3, "检查角色...")
        await self._report_event(on_event, "task_start", 4, "检查逻辑...")
        start_time = time.time()

        results = await asyncio.gather(
            self.character_guard.check(draft, work_id, context),
            self.logic_auditor.check(draft, work_id, context),
            return_exceptions=True
        )

        check_time = time.time() - start_time
        await self._report_event(on_event, "task_done", 3, elapsed_time=check_time)
        await self._report_event(on_event, "task_done", 4, elapsed_time=check_time)

        # 提取警告（不修订）
        warnings = self._extract_warnings(results)

        return {
            "content": draft.get("content", ""),
            "word_count": draft.get("word_count", 0),
            "mode": "standard",
            "quality_score": min(0.85, config["max_quality_score"]),
            "stages_executed": config["stages"],
            "warnings": warnings,  # 前端可选择展示
        }

    async def _execute_full(
        self,
        task: Dict,
        work_id: str,
        chapter_id: str,
        context: Dict,
        on_event: Optional[Callable],
        config: Dict
    ) -> Dict[str, Any]:
        """Full 模式执行：完整 5 阶段"""

        # 使用原有的完整执行逻辑
        return await self._execute_internal(task, work_id, chapter_id, context, on_event)

    def _needs_outline(self, task: Dict) -> bool:
        """判断是否需要大纲

        以下情况不需要大纲：
        - 润色任务
        - 目标字数 < 300
        - 任务描述很简单
        """
        task_type = self.mode_selector._infer_task_type(task.get("description", ""))
        if task_type in ["polish", "expand"]:
            return False

        target_words = self.mode_selector._get_target_words(task)
        if target_words and target_words < 300:
            return False

        return True

    async def _quick_outline(self, task: Dict, context: Dict) -> Dict:
        """快速生成简化大纲"""
        # 使用简化的 prompt，只生成关键点
        return await self.outline_agent.generate_quick(task, context)

    def _extract_warnings(self, results: List) -> List[str]:
        """从审查结果提取警告"""
        warnings = []

        for result in results:
            if isinstance(result, Exception):
                continue
            if result.get("status") != "pass":
                issues = result.get("issues", [])
                warnings.extend(issues[:3])  # 最多取 3 个

        return warnings
```

---

## 7. 前端展示

### 7.1 模式指示器

```tsx
// 在 TaskListPanel 中显示当前模式

interface TaskListPanelProps {
  tasks: Task[];
  currentTaskId: number | null;
  mode?: 'lite' | 'standard' | 'full';  // ✅ 新增
}

const TaskListPanel: React.FC<TaskListPanelProps> = ({
  tasks,
  currentTaskId,
  mode
}) => {
  const getModeLabel = (mode?: string) => {
    const labels: Record<string, string> = {
      'lite': '轻量模式',
      'standard': '标准模式',
      'full': '完整模式',
    };
    return labels[mode || 'standard'] || '标准模式';
  };

  return (
    <div className={styles.taskListPanel}>
      <div className={styles.header}>
        <h3>执行计划</h3>
        <div className={styles.headerRight}>
          {/* ✅ 新增：模式标签 */}
          {mode && (
            <span className={`${styles.modeTag} ${styles[mode]}`}>
              {getModeLabel(mode)}
            </span>
          )}
          <span className={styles.taskCount}>
            {completedCount} / {tasks.length}
          </span>
        </div>
      </div>
      {/* ... 其他内容 ... */}
    </div>
  );
};
```

### 7.2 CSS 样式

```css
/* 模式标签样式 */
.modeTag {
  padding: 2px 8px;
  font-size: 11px;
  border-radius: 4px;
  margin-right: 8px;
}

.modeTag.lite {
  background: #dbeafe;
  color: #1d4ed8;
}

.modeTag.standard {
  background: #d1fae5;
  color: #047857;
}

.modeTag.full {
  background: #fef3c7;
  color: #b45309;
}
```

---

## 8. 测试用例

```python
# tests/test_mode_selector.py

import pytest
from app.services.agent.multi_agent.mode_selector import ModeSelector


class TestModeSelector:

    @pytest.fixture
    def selector(self):
        return ModeSelector()

    def test_word_count_lite(self, selector):
        """< 500 字应该选择 lite"""
        task = {"description": "润色这段200字的描写"}
        mode = selector.select(task, {})
        assert mode == "lite"

    def test_word_count_standard(self, selector):
        """500-1500 字应该选择 standard"""
        task = {"description": "写一个800字的场景"}
        mode = selector.select(task, {})
        assert mode == "standard"

    def test_word_count_full(self, selector):
        """> 1500 字应该选择 full"""
        task = {"description": "写一章3000字的内容"}
        mode = selector.select(task, {})
        assert mode == "full"

    def test_task_type_polish(self, selector):
        """润色任务应该选择 lite"""
        task = {"description": "润色这段文字，让它更生动"}
        mode = selector.select(task, {})
        assert mode == "lite"

    def test_task_type_battle(self, selector):
        """战斗场面应该选择 full"""
        task = {"description": "写一场精彩的战斗"}
        mode = selector.select(task, {})
        assert mode == "full"

    def test_complexity_high(self, selector):
        """高复杂度上下文应该选择 full"""
        task = {"description": "续写下一段"}
        context = {
            "key_characters": ["李云", "王婷", "张三", "李四"],
            "pending_foreshadowing": True,
            "is_key_plot_point": True,
        }
        mode = selector.select(task, context)
        assert mode == "full"

    def test_force_mode(self, selector):
        """强制指定模式应该生效"""
        task = {"description": "写一章", "force_mode": "lite"}
        mode = selector.select(task, {})
        assert mode == "lite"
```

---

## 9. 监控指标

```python
# 模式分布统计
increment_counter("multi_agent_mode", labels={"mode": mode})

# 各模式耗时
observe_histogram("multi_agent_duration", duration, labels={"mode": mode})

# 各模式质量评分
observe_histogram("multi_agent_quality", quality_score, labels={"mode": mode})
```

---

## 10. 实施计划

| 阶段 | 任务 | 说明 |
|------|------|------|
| 1 | 实现 ModeSelector 类 | 字数提取、任务类型识别、复杂度判断 |
| 2 | executor.py 集成 | 在 `execute()` 入口调用 ModeSelector |
| 3 | 实现 `_execute_lite()` | Lite 模式执行逻辑（1-2 阶段） |
| 4 | 实现 `_execute_standard()` | Standard 模式执行逻辑（4 阶段） |
| 5 | 前端模式展示 | TaskListPanel 显示当前模式 |
| 6 | 单元测试 | 覆盖各种任务场景 |
| 7 | 集成测试 + 调优 | 验证模式选择准确性 |

---

## 11. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|----------|
| 误判模式导致质量不足 | 中 | 中 | 取最高模式策略，宁可过度不可不足 |
| 字数提取失败 | 低 | 低 | 默认使用 standard 模式 |
| Lite 模式质量差 | 低 | 中 | 设置质量评分上限，前端提示 |

---

## 12. 配置参数

```python
# 可通过环境变量或配置文件调整

MULTI_AGENT_CONFIG = {
    # 字数阈值
    "WORD_THRESHOLD_LITE": int(os.getenv("MA_WORD_LITE", 500)),
    "WORD_THRESHOLD_STANDARD": int(os.getenv("MA_WORD_STANDARD", 1500)),

    # 是否启用动态模式
    "ENABLE_DYNAMIC_MODE": os.getenv("MA_DYNAMIC_MODE", "true").lower() == "true",

    # 默认模式（禁用动态模式时使用）
    "DEFAULT_MODE": os.getenv("MA_DEFAULT_MODE", "full"),
}
```

---

## 13. 与现有代码的关系

| 现有代码 | 本方案 | 关系 |
|---------|--------|------|
| `executor.py` | 扩展 | 新增 `_execute_lite()`、`_execute_standard()` 方法 |
| `_execute_internal()` | 保留 | 作为 Full 模式的实现 |
| `OutlineAgent` | 复用 | Lite 模式可选调用 `generate_quick()` |
| `WriterAgent` | 复用 | 所有模式都使用 |
| `CharacterGuard` | 复用 | Standard/Full 模式使用 |
| `LogicAuditor` | 复用 | Standard/Full 模式使用 |
| `EditorAgent` | 复用 | 仅 Full 模式使用 |
| `_send_plan_event()` | 扩展 | 根据模式发送不同数量的任务 |

---

## 14. 实现说明

本功能为**全新实现**，不修改现有代码逻辑，仅在 `execute()` 入口处新增模式选择分支：

```python
# executor.py 修改点

async def execute(self, task, work_id, chapter_id, context, on_event=None):
    # ✅ 新增：模式选择
    mode = self.mode_selector.select(task, context)

    # ✅ 新增：按模式路由
    if mode == "lite":
        return await self._execute_lite(task, context, on_event)
    elif mode == "standard":
        return await self._execute_standard(task, work_id, context, on_event)
    else:
        return await self._execute_internal(task, work_id, chapter_id, context, on_event)  # 原有逻辑
```
