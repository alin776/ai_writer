# Agent 增强改造开发文档

> **文档版本**: v1.0
> **创建日期**: 2025-10-31
> **项目**: AI Writer - Agent 智能助手增强
> **改造方式**: 在现有 `backend/app/services/agent/` 目录下渐进式改造

---

## 📋 目录

- [1. 项目概述](#1-项目概述)
- [2. 现状分析](#2-现状分析)
- [3. 改造目标](#3-改造目标)
- [4. 技术架构](#4-技术架构)
- [5. 核心模块设计](#5-核心模块设计)
- [6. 实施路线图](#6-实施路线图)
- [7. API 设计](#7-api-设计)
- [8. 数据库设计](#8-数据库设计)
- [9. 测试计划](#9-测试计划)
- [10. 风险控制](#10-风险控制)

---

## 1. 项目概述

### 1.1 项目背景

当前 AI Writer 项目已实现基于 LangGraph 的 Agent 系统，提供了基础的智能写作助手功能。通过研究 5 个优秀的开源项目，我们提取了多个可移植的设计模式，计划对现有 Agent 系统进行增强改造。

### 1.2 改造原则

**核心原则：渐进式改造，不破坏现有功能**

1. ✅ **零破坏**: 不影响普通 AI 模式 (`/api/v1/ai/*`)
2. ✅ **渐进式**: 分阶段实施，每个阶段可独立验证
3. ✅ **简洁性**: 每次改动影响最小代码范围
4. ✅ **可测试**: 每个功能都有对应测试
5. ✅ **可回滚**: 支持配置开关，随时切换

### 1.3 参考项目精华

| 项目 | 核心价值 | 可移植性 |
|------|---------|---------|
| **novel-multi-agents** | 工具驱动通信 + 强类型输出 + 质量循环 | 100% |
| **pulpgen** | 补丁式版本管理 + 分散-填充算法 | 100% (改用JSON) |
| **novel-agent** | 分层架构 + Memory系统 + 状态管理 | 100% |
| **MetaGPT** | ARE模式 + 消息驱动 | 100% (理念) |
| **novel-ai-agent-Chinese** | 网文爽感优化Prompt + 模型分级 | 100% |

---

## 2. 现状分析

### 2.1 当前架构

```
ai_writer/
├─ backend/app/api/v1/
│  ├─ ai.py          # 普通AI模式: /ai/* (续写、润色、翻译等)
│  └─ agent.py       # Agent模式: /agent/* (对话、规划、HITL)
│
└─ backend/app/services/
   ├─ ai/            # 普通AI服务 (完全独立，不动！)
   │  ├─ openai_service.py
   │  ├─ http_ai_service.py
   │  └─ ...
   │
   └─ agent/         # Agent服务 (所有改造都在这里)
      ├─ langgraph_agent.py      # LangGraph工作流
      ├─ agents/                 # 4个Agent角色
      │  ├─ planning_agent.py
      │  ├─ reflection_agent.py
      │  └─ parallel_executor.py
      ├─ memory/                 # 记忆系统
      │  ├─ memory_manager.py
      │  ├─ long_term_memory.py
      │  └─ user_profile.py
      └─ tools/                  # 工具系统
         ├─ tool_registry.py
         ├─ consistency_checker.py
         ├─ style_learning.py
         └─ show_dont_tell.py
```

### 2.2 现有功能

**✅ 已有优势**:
- LangGraph 框架 (灵活的图编排)
- 流式响应 (SSE)
- 记忆系统 (Redis)
- HITL 人机协同
- 工具注册系统
- RAG 知识检索

**❌ 待改进点**:
- Memory系统较简单 (FIFO策略)
- 工具调用不够标准化
- 缺乏版本管理
- 缺乏质量循环机制
- 缺乏内容优化Prompt
- 缺乏模型分级策略

---

## 3. 改造目标

### 3.1 总体目标

打造业界领先的 AI 写作 Agent 系统，融合 5 个参考项目的精华，保持简洁高效。

### 3.2 具体目标

#### 阶段一：核心基础设施改造（2-3周）

**目标**: 打牢基础，提升系统可靠性

1. **增强 Memory 系统**
   - ✅ 分层记忆 (短期/中期/长期)
   - ✅ 智能遗忘策略
   - ✅ 状态快照与恢复
   - ✅ 版本历史追踪

2. **标准化工具系统**
   - ✅ 工具驱动通信模式
   - ✅ 强类型输入输出
   - ✅ 工具调用日志
   - ✅ 工具版本管理

3. **实现版本管理**
   - ✅ 补丁式版本控制 (JSON格式)
   - ✅ 版本回滚能力
   - ✅ 版本分支和合并
   - ✅ 完整变更历史

#### 阶段二：高价值功能集成（3-4周）

**目标**: 快速提升内容质量和用户体验

1. **质量循环机制**
   - ✅ 生成 → 评估 → 改进 → 重试
   - ✅ 多维度评估 (质量分数 + 字数 + 连贯性)
   - ✅ 智能反馈生成
   - ✅ 自动优化Prompt

2. **Prompt 库优化**
   - ✅ 直接采用 novel-ai-agent-Chinese 的 Prompt
   - ✅ 四维度爽感优化 (反转35% + 升级35% + 场景20% + 对话10%)
   - ✅ 分阶段生成策略 (起承转合终)

3. **模型分级策略**
   - ✅ 复杂任务 → 强模型
   - ✅ 中等任务 → 中模型
   - ✅ 简单任务 → 弱模型
   - ✅ 成本优化 40-50%

#### 阶段三：架构优化与完善（2-3周）

**目标**: 长期可维护性和可扩展性

1. **引入 ARE 设计理念**
   - ✅ Action层: 标准化节点函数
   - ✅ Role层: 增强Agent职责定义
   - ✅ Environment层: 消息总线和状态管理中枢

2. **批量生成优化**
   - ✅ 分散-填充算法
   - ✅ 全局上下文管理
   - ✅ 长篇质量提升

3. **监控和可观测性**
   - ✅ 完整的性能监控
   - ✅ 成本追踪
   - ✅ 质量分析

---

## 4. 技术架构

### 4.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                     用户请求层                           │
│  /api/v1/agent/chat  |  /api/v1/agent/plan  | ...       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                  LangGraph 工作流层                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │  WritingAgentGraph                              │   │
│  │  ├─ Intent Detection (意图识别)                 │   │
│  │  ├─ Planning Node (规划节点)                    │   │
│  │  ├─ Writing Node (写作节点)                     │   │
│  │  ├─ Reflection Node (反思节点)                  │   │
│  │  ├─ Quality Loop Node (质量循环)        [新增]  │   │
│  │  ├─ Version Control Node (版本管理)     [新增]  │   │
│  │  └─ HITL Node (人机协同)                        │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    Agent 角色层                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Planning │  │ Writing  │  │Reflection│  │Parallel│ │
│  │  Agent   │  │  Agent   │  │  Agent   │  │Executor│ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    核心服务层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Memory       │  │ Tool         │  │ Version      │ │
│  │ Manager      │  │ Registry     │  │ Control      │ │
│  │ (增强)       │  │ (标准化)     │  │ (新增)       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Quality      │  │ Prompt       │  │ Model        │ │
│  │ Evaluator    │  │ Library      │  │ Selector     │ │
│  │ (新增)       │  │ (新增)       │  │ (新增)       │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    基础设施层                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │PostgreSQL│  │  Redis   │  │  Vector  │  │  LLM   │ │
│  │   DB     │  │  Cache   │  │  Store   │  │  API   │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 4.2 改造策略

**原则**: 在现有基础上增强，不重构

```
现有文件                   改造方式                    新增文件
─────────────────────────────────────────────────────────────
langgraph_agent.py    →   增加新节点                  (无)
                          添加质量循环
                          添加版本控制节点

memory_manager.py     →   增强功能                    memory_strategy.py
                          添加智能遗忘                (遗忘策略)
                          添加状态快照

tool_registry.py      →   标准化工具接口              tool_types.py
                          添加类型验证                (类型定义)

(无)                  →   新建                        version_control.py
                                                      (版本管理服务)

(无)                  →   新建                        quality_evaluator.py
                                                      (质量评估服务)

(无)                  →   新建                        prompt_library.py
                                                      (Prompt库)

(无)                  →   新建                        model_selector.py
                                                      (模型选择器)
```

---

## 5. 核心模块设计

### 5.1 增强的 Memory 系统

#### 5.1.1 设计目标

- 分层记忆 (短期/中期/长期)
- 智能遗忘 (重要度加权，非简单FIFO)
- 状态快照与恢复
- 版本历史追踪

#### 5.1.2 类设计

```python
# backend/app/services/agent/memory/memory_manager.py (增强)

class MemoryItem(BaseModel):
    """记忆条目"""
    id: str
    role: str  # user/assistant/system
    content: str
    timestamp: datetime
    importance: float = 0.5  # 重要度 0-1
    decay_rate: float = 0.1  # 遗忘速率
    access_count: int = 0    # 访问次数
    last_access: datetime
    metadata: Dict[str, Any] = {}

class MemoryLayer(str, Enum):
    """记忆层级"""
    SHORT_TERM = "short_term"    # 短期记忆 (最近10条)
    MEDIUM_TERM = "medium_term"  # 中期记忆 (最近100条)
    LONG_TERM = "long_term"      # 长期记忆 (压缩摘要)

class EnhancedMemoryManager(MemoryManager):
    """增强的记忆管理器"""

    def __init__(self, redis_client: redis.Redis):
        super().__init__(redis_client)
        self.strategy = SmartForgetStrategy()  # 智能遗忘策略

    def add_memory(
        self,
        user_id: str,
        role: str,
        content: str,
        importance: float = 0.5,
        metadata: Dict = None
    ) -> MemoryItem:
        """添加记忆（自动分层）"""
        pass

    def get_relevant_memories(
        self,
        user_id: str,
        query: str,
        layer: MemoryLayer = None,
        top_k: int = 5
    ) -> List[MemoryItem]:
        """检索相关记忆（基于语义相似度）"""
        pass

    def create_snapshot(
        self,
        user_id: str,
        conversation_id: str
    ) -> str:
        """创建状态快照"""
        pass

    def restore_snapshot(
        self,
        snapshot_id: str
    ) -> Dict[str, Any]:
        """恢复状态快照"""
        pass

    def apply_forgetting(
        self,
        user_id: str
    ):
        """应用智能遗忘策略"""
        pass
```

#### 5.1.3 智能遗忘策略

```python
# backend/app/services/agent/memory/memory_strategy.py (新建)

class SmartForgetStrategy:
    """智能遗忘策略"""

    def calculate_importance(
        self,
        memory: MemoryItem,
        current_time: datetime
    ) -> float:
        """
        计算记忆重要度

        重要度 = 初始重要度 * 时间衰减 * 访问频率加权
        """
        # 时间衰减（指数衰减）
        time_delta = (current_time - memory.timestamp).total_seconds()
        time_decay = math.exp(-memory.decay_rate * time_delta / 3600)

        # 访问频率加权
        access_weight = 1 + math.log(1 + memory.access_count)

        # 综合重要度
        importance = memory.importance * time_decay * access_weight

        return importance

    def should_forget(
        self,
        memory: MemoryItem,
        threshold: float = 0.1
    ) -> bool:
        """判断是否应该遗忘"""
        current_importance = self.calculate_importance(
            memory,
            datetime.now()
        )
        return current_importance < threshold

    def compress_to_summary(
        self,
        memories: List[MemoryItem]
    ) -> str:
        """将多条记忆压缩为摘要"""
        # 可以用 LLM 生成摘要
        pass
```

### 5.2 标准化工具系统

#### 5.2.1 设计目标

- 工具驱动通信模式（借鉴 novel-multi-agents）
- 强类型输入输出（Pydantic验证）
- 工具调用日志和监控
- 工具版本管理

#### 5.2.2 类型定义

```python
# backend/app/services/agent/tools/tool_types.py (新建)

from pydantic import BaseModel, Field
from typing import TypeVar, Generic, Callable, Any

# 定义泛型类型
InputT = TypeVar('InputT', bound=BaseModel)
OutputT = TypeVar('OutputT', bound=BaseModel)

class ToolInput(BaseModel):
    """工具输入基类"""
    pass

class ToolOutput(BaseModel):
    """工具输出基类"""
    success: bool
    message: str
    data: Any = None
    metadata: Dict[str, Any] = {}

class StandardTool(Generic[InputT, OutputT]):
    """标准化工具基类"""

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Type[InputT],
        output_schema: Type[OutputT],
        executor: Callable[[InputT], OutputT]
    ):
        self.name = name
        self.description = description
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.executor = executor

    async def execute(self, input_data: InputT) -> OutputT:
        """执行工具（带验证）"""
        # 验证输入
        validated_input = self.input_schema(**input_data.dict())

        # 执行
        result = await self.executor(validated_input)

        # 验证输出
        validated_output = self.output_schema(**result.dict())

        return validated_output

    def to_langchain_tool(self):
        """转换为 LangChain Tool"""
        pass
```

#### 5.2.3 工具定义示例

```python
# backend/app/services/agent/tools/writing_tools.py (新建或增强)

from .tool_types import ToolInput, ToolOutput, StandardTool

# ========== 续写工具 ==========

class ContinueWritingInput(ToolInput):
    """续写工具输入"""
    context: str = Field(..., description="上下文内容")
    requirements: str = Field("", description="续写要求")
    target_length: int = Field(500, description="目标字数", ge=100, le=2000)

class ContinueWritingOutput(ToolOutput):
    """续写工具输出"""
    generated_text: str = Field(..., description="续写内容")
    word_count: int = Field(..., description="实际字数")
    quality_score: float = Field(0.0, description="质量分数")

async def continue_writing_executor(
    input: ContinueWritingInput
) -> ContinueWritingOutput:
    """续写执行器"""
    # 调用 AI 服务生成内容
    generated_text = await _generate_with_ai(
        input.context,
        input.requirements,
        input.target_length
    )

    return ContinueWritingOutput(
        success=True,
        message="续写成功",
        generated_text=generated_text,
        word_count=len(generated_text),
        quality_score=0.8
    )

# 注册工具
continue_writing_tool = StandardTool(
    name="continue_writing",
    description="根据上下文续写内容",
    input_schema=ContinueWritingInput,
    output_schema=ContinueWritingOutput,
    executor=continue_writing_executor
)
```

### 5.3 版本管理系统

#### 5.3.1 设计目标

- 补丁式版本控制（借鉴 pulpgen，改用JSON）
- 版本回滚能力
- 版本分支和合并
- 完整变更历史

#### 5.3.2 核心设计

```python
# backend/app/services/agent/version_control.py (新建)

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import json

class PatchOperation(str, Enum):
    """补丁操作类型"""
    INSERT = "insert"      # 插入文本
    DELETE = "delete"      # 删除文本
    REPLACE = "replace"    # 替换文本
    REORDER = "reorder"    # 重排序

class Patch(BaseModel):
    """补丁定义"""
    patch_id: str
    operation: PatchOperation
    position: int  # 操作位置（字符索引或段落索引）
    content: str = ""  # 新内容
    length: int = 0    # 删除长度（DELETE操作）
    metadata: Dict[str, Any] = {}
    created_at: datetime
    created_by: str  # user_id or agent_name
    description: str = ""

class Version(BaseModel):
    """版本定义"""
    version_id: str
    parent_version_id: Optional[str] = None
    patches: List[Patch] = []
    created_at: datetime
    created_by: str
    tag: Optional[str] = None  # 版本标签
    description: str = ""

class VersionedContent(BaseModel):
    """版本化内容"""
    content_id: str
    base_content: str  # 基础版本
    versions: List[Version] = []
    current_version_id: str
    branches: Dict[str, str] = {}  # branch_name -> version_id

class VersionControlService:
    """版本控制服务"""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def create_content(
        self,
        content_id: str,
        initial_content: str,
        created_by: str
    ) -> VersionedContent:
        """创建版本化内容"""
        base_version = Version(
            version_id=self._generate_version_id(),
            patches=[],
            created_at=datetime.now(),
            created_by=created_by,
            description="初始版本"
        )

        versioned = VersionedContent(
            content_id=content_id,
            base_content=initial_content,
            versions=[base_version],
            current_version_id=base_version.version_id
        )

        self._save(versioned)
        return versioned

    def apply_patch(
        self,
        content_id: str,
        patch: Patch
    ) -> Version:
        """应用补丁（创建新版本）"""
        versioned = self._load(content_id)

        # 创建新版本
        new_version = Version(
            version_id=self._generate_version_id(),
            parent_version_id=versioned.current_version_id,
            patches=[patch],
            created_at=datetime.now(),
            created_by=patch.created_by,
            description=patch.description
        )

        versioned.versions.append(new_version)
        versioned.current_version_id = new_version.version_id

        self._save(versioned)
        return new_version

    def get_content_at_version(
        self,
        content_id: str,
        version_id: str = None
    ) -> str:
        """获取指定版本的内容"""
        versioned = self._load(content_id)

        if not version_id:
            version_id = versioned.current_version_id

        # 从base_content开始应用所有补丁
        content = versioned.base_content
        patches = self._collect_patches_to_version(versioned, version_id)

        for patch in patches:
            content = self._apply_single_patch(content, patch)

        return content

    def rollback_to_version(
        self,
        content_id: str,
        version_id: str
    ) -> str:
        """回滚到指定版本"""
        versioned = self._load(content_id)
        versioned.current_version_id = version_id
        self._save(versioned)

        return self.get_content_at_version(content_id, version_id)

    def create_branch(
        self,
        content_id: str,
        branch_name: str,
        from_version_id: str = None
    ) -> str:
        """创建分支"""
        versioned = self._load(content_id)

        base_version = from_version_id or versioned.current_version_id
        versioned.branches[branch_name] = base_version

        self._save(versioned)
        return base_version

    def get_version_history(
        self,
        content_id: str
    ) -> List[Version]:
        """获取版本历史"""
        versioned = self._load(content_id)
        return versioned.versions

    def compare_versions(
        self,
        content_id: str,
        version_id_1: str,
        version_id_2: str
    ) -> Dict[str, Any]:
        """对比两个版本"""
        content_1 = self.get_content_at_version(content_id, version_id_1)
        content_2 = self.get_content_at_version(content_id, version_id_2)

        # 简单的差异统计
        return {
            "version_1": version_id_1,
            "version_2": version_id_2,
            "length_diff": len(content_2) - len(content_1),
            "content_1_preview": content_1[:200],
            "content_2_preview": content_2[:200]
        }

    def _apply_single_patch(self, content: str, patch: Patch) -> str:
        """应用单个补丁"""
        if patch.operation == PatchOperation.INSERT:
            return content[:patch.position] + patch.content + content[patch.position:]

        elif patch.operation == PatchOperation.DELETE:
            return content[:patch.position] + content[patch.position + patch.length:]

        elif patch.operation == PatchOperation.REPLACE:
            return content[:patch.position] + patch.content + content[patch.position + patch.length:]

        return content

    def _collect_patches_to_version(
        self,
        versioned: VersionedContent,
        target_version_id: str
    ) -> List[Patch]:
        """收集到达目标版本的所有补丁"""
        # 构建版本树
        # 从base到target的路径
        # 返回路径上的所有patches
        patches = []
        # ... 实现版本树遍历
        return patches

    def _save(self, versioned: VersionedContent):
        """保存到Redis"""
        key = f"version:{versioned.content_id}"
        self.redis.set(key, versioned.json())

    def _load(self, content_id: str) -> VersionedContent:
        """从Redis加载"""
        key = f"version:{content_id}"
        data = self.redis.get(key)
        return VersionedContent.parse_raw(data)

    def _generate_version_id(self) -> str:
        """生成版本ID"""
        import uuid
        return f"v_{uuid.uuid4().hex[:12]}"
```

### 5.4 质量循环机制

#### 5.4.1 设计目标

- 生成 → 评估 → 改进 → 重试（最多3次）
- 多维度评估（质量分数 + 字数 + 连贯性）
- 智能反馈生成
- 自动优化Prompt

#### 5.4.2 核心设计

```python
# backend/app/services/agent/quality_evaluator.py (新建)

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum

class QualityDimension(str, Enum):
    """质量维度"""
    CONTENT_QUALITY = "content_quality"      # 内容质量
    LENGTH_CHECK = "length_check"            # 字数检查
    COHERENCE = "coherence"                  # 连贯性
    STYLE_CONSISTENCY = "style_consistency"  # 风格一致性
    GRAMMAR = "grammar"                      # 语法正确性

class DimensionScore(BaseModel):
    """维度评分"""
    dimension: QualityDimension
    score: float = Field(..., ge=0, le=10)  # 0-10分
    feedback: str = ""
    weight: float = 1.0  # 权重

class QualityEvaluation(BaseModel):
    """质量评估结果"""
    overall_score: float  # 总分 0-10
    dimension_scores: List[DimensionScore]
    passes: bool  # 是否通过（>= 8分）
    feedback: str  # 综合反馈
    suggestions: List[str] = []  # 改进建议

class QualityEvaluatorService:
    """质量评估服务"""

    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.pass_threshold = 8.0  # 通过阈值

    async def evaluate(
        self,
        content: str,
        context: Dict[str, Any] = None,
        dimensions: List[QualityDimension] = None
    ) -> QualityEvaluation:
        """
        评估内容质量

        Args:
            content: 待评估内容
            context: 上下文信息
            dimensions: 要评估的维度

        Returns:
            QualityEvaluation: 评估结果
        """
        if dimensions is None:
            dimensions = [
                QualityDimension.CONTENT_QUALITY,
                QualityDimension.LENGTH_CHECK,
                QualityDimension.COHERENCE
            ]

        # 评估各个维度
        dimension_scores = []

        for dim in dimensions:
            score_data = await self._evaluate_dimension(content, dim, context)
            dimension_scores.append(score_data)

        # 计算加权总分
        total_weight = sum(s.weight for s in dimension_scores)
        overall_score = sum(
            s.score * s.weight for s in dimension_scores
        ) / total_weight

        # 生成综合反馈
        feedback = self._generate_feedback(dimension_scores, overall_score)

        # 生成改进建议
        suggestions = self._generate_suggestions(dimension_scores)

        return QualityEvaluation(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            passes=overall_score >= self.pass_threshold,
            feedback=feedback,
            suggestions=suggestions
        )

    async def _evaluate_dimension(
        self,
        content: str,
        dimension: QualityDimension,
        context: Dict = None
    ) -> DimensionScore:
        """评估单个维度"""

        if dimension == QualityDimension.LENGTH_CHECK:
            # 字数检查（直接计算，不需要LLM）
            target_length = context.get("target_length", 500) if context else 500
            actual_length = len(content)

            score = min(10, (actual_length / target_length) * 10)
            feedback = f"实际字数: {actual_length}, 目标字数: {target_length}"

            return DimensionScore(
                dimension=dimension,
                score=score,
                feedback=feedback,
                weight=1.0
            )

        elif dimension == QualityDimension.CONTENT_QUALITY:
            # 内容质量（使用LLM评估）
            prompt = f"""请评估以下小说内容的质量（0-10分）:

内容:
{content}

评估标准:
- 情节是否吸引人
- 描写是否生动
- 节奏是否合理
- 是否有明显硬伤

请直接返回分数和简短反馈，格式: score|feedback"""

            result = await self.ai_service.simple_complete(prompt)
            score, feedback = self._parse_llm_result(result)

            return DimensionScore(
                dimension=dimension,
                score=score,
                feedback=feedback,
                weight=2.0  # 内容质量权重更高
            )

        elif dimension == QualityDimension.COHERENCE:
            # 连贯性评估
            previous_content = context.get("previous_content", "") if context else ""

            prompt = f"""请评估以下续写内容与前文的连贯性（0-10分）:

前文:
{previous_content[-500:] if previous_content else "（无前文）"}

续写:
{content}

评估标准:
- 情节是否自然衔接
- 人物表现是否一致
- 风格是否统一

请直接返回分数和简短反馈，格式: score|feedback"""

            result = await self.ai_service.simple_complete(prompt)
            score, feedback = self._parse_llm_result(result)

            return DimensionScore(
                dimension=dimension,
                score=score,
                feedback=feedback,
                weight=1.5
            )

        # 其他维度...
        return DimensionScore(
            dimension=dimension,
            score=7.0,
            feedback="暂未实现",
            weight=1.0
        )

    def _parse_llm_result(self, result: str) -> tuple:
        """解析LLM返回结果"""
        try:
            parts = result.strip().split("|")
            score = float(parts[0].strip())
            feedback = parts[1].strip() if len(parts) > 1 else ""
            return score, feedback
        except:
            return 7.0, result

    def _generate_feedback(
        self,
        dimension_scores: List[DimensionScore],
        overall_score: float
    ) -> str:
        """生成综合反馈"""
        if overall_score >= 9:
            return "内容质量优秀！"
        elif overall_score >= 8:
            return "内容质量良好，达标。"
        elif overall_score >= 6:
            return "内容质量一般，建议优化。"
        else:
            return "内容质量较差，需要重写。"

    def _generate_suggestions(
        self,
        dimension_scores: List[DimensionScore]
    ) -> List[str]:
        """生成改进建议"""
        suggestions = []

        for dim_score in dimension_scores:
            if dim_score.score < 7:
                if dim_score.dimension == QualityDimension.LENGTH_CHECK:
                    suggestions.append("建议增加内容字数")
                elif dim_score.dimension == QualityDimension.CONTENT_QUALITY:
                    suggestions.append("建议优化情节和描写")
                elif dim_score.dimension == QualityDimension.COHERENCE:
                    suggestions.append("建议增强与前文的衔接")

        return suggestions

class QualityLoopManager:
    """质量循环管理器"""

    def __init__(
        self,
        evaluator: QualityEvaluatorService,
        max_iterations: int = 3
    ):
        self.evaluator = evaluator
        self.max_iterations = max_iterations

    async def run_quality_loop(
        self,
        generator: Callable,
        generator_kwargs: Dict,
        context: Dict = None
    ) -> Dict[str, Any]:
        """
        运行质量循环

        Args:
            generator: 生成函数
            generator_kwargs: 生成函数参数
            context: 上下文

        Returns:
            Dict: 最终结果
        """
        iteration = 0
        best_content = None
        best_score = 0.0

        while iteration < self.max_iterations:
            iteration += 1

            # 生成内容
            content = await generator(**generator_kwargs)

            # 评估质量
            evaluation = await self.evaluator.evaluate(content, context)

            # 更新最佳结果
            if evaluation.overall_score > best_score:
                best_content = content
                best_score = evaluation.overall_score

            # 检查是否通过
            if evaluation.passes:
                return {
                    "content": content,
                    "evaluation": evaluation,
                    "iterations": iteration,
                    "success": True
                }

            # 未通过，优化generator_kwargs
            if iteration < self.max_iterations:
                # 根据反馈调整参数
                generator_kwargs = self._optimize_params(
                    generator_kwargs,
                    evaluation
                )

        # 达到最大迭代次数，返回最佳结果
        return {
            "content": best_content,
            "evaluation": evaluation,
            "iterations": iteration,
            "success": False,
            "message": "达到最大迭代次数，返回最佳结果"
        }

    def _optimize_params(
        self,
        params: Dict,
        evaluation: QualityEvaluation
    ) -> Dict:
        """根据评估结果优化参数"""
        # 添加改进建议到提示词
        if "requirements" in params:
            suggestions_text = "\n".join(evaluation.suggestions)
            params["requirements"] += f"\n\n改进建议:\n{suggestions_text}"

        return params
```

### 5.5 Prompt 库

#### 5.5.1 设计目标

直接采用 novel-ai-agent-Chinese 的精品 Prompt，实现：
- 四维度爽感优化
- 分阶段生成策略
- 场景化Prompt模板

#### 5.5.2 核心设计

```python
# backend/app/services/agent/prompt_library.py (新建)

from enum import Enum
from typing import Dict, Any

class NovelPhase(str, Enum):
    """小说创作阶段"""
    OPENING = "opening"      # 起 (开篇)
    DEVELOPMENT = "development"  # 承 (发展)
    CLIMAX = "climax"        # 转 (转折)
    RESOLUTION = "resolution"    # 合 (收束)
    ENDING = "ending"        # 终 (结局)

class ContentCreationPrompts:
    """内容创作Prompt库"""

    # ========== 系统级Prompt (四维度爽感优化) ==========

    CONTENT_CREATION_SYSTEM = """你是一位专业的网络小说创作专家，精通各种类型的网文创作技巧。

# 核心创作理念: 四维度爽感优化

## 1. 反转与震撼 (权重35%)
- 出人意料的能力展现
- 身份地位的突然转变
- 打脸装逼打击对手
- 令众人震惊的场面

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

    # ========== 打脸场景Prompt ==========

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

## 示例场景:

上下文: {context}

请根据上述要求创作一个精彩的打脸场景。
"""

    # ========== 分阶段创作Prompt ==========

    PHASE_PROMPTS = {
        NovelPhase.OPENING: """# 开篇阶段创作要求

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
""",

        NovelPhase.DEVELOPMENT: """# 发展阶段创作要求

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
""",

        NovelPhase.CLIMAX: """# 高潮阶段创作要求

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
""",

        NovelPhase.RESOLUTION: """# 收束阶段创作要求

## 核心目标
- 解决主要矛盾
- 完成角色成长弧
- 给予读者满足感

## 创作要点
1. **矛盾解决**: 主线冲突圆满解决
2. **成果展示**: 展示主角收获
3. **地位提升**: 社会地位/实力飞跃
4. **情感满足**: 给读者满足感

上下文: {context}
字数要求: {target_length}

请创作收束阶段内容。
""",

        NovelPhase.ENDING: """# 结局阶段创作要求

## 核心目标
- 画龙点睛的结尾
- 留下回味空间
- 可选：埋下续集伏笔

## 创作要点
1. **总结升华**: 简短总结主角成长
2. **余韵留白**: 意犹未尽的感觉
3. **开放结局**: 可以有新的可能

## 字数控制
- 结局段落: 300-500字
- 不宜过长

上下文: {context}
字数要求: {target_length}

请创作结局内容。
"""
    }

    # ========== 辅助方法 ==========

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

### 5.6 模型选择器

#### 5.6.1 设计目标

- 根据任务复杂度自动选择模型
- 成本优化 40-50%
- 支持多种LLM提供商

#### 5.6.2 核心设计

```python
# backend/app/services/agent/model_selector.py (新建)

from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel

class TaskComplexity(str, Enum):
    """任务复杂度"""
    SIMPLE = "simple"      # 简单任务 (评估、分类等)
    MEDIUM = "medium"      # 中等任务 (润色、扩写等)
    COMPLEX = "complex"    # 复杂任务 (创作、规划等)

class ModelTier(BaseModel):
    """模型层级"""
    name: str
    provider: str  # openai/anthropic/deepseek/...
    model_id: str
    cost_per_1k: float  # 每1k tokens成本(元)
    max_tokens: int
    speed: str  # fast/medium/slow

class ModelSelector:
    """模型选择器"""

    # 模型配置
    MODEL_TIERS = {
        TaskComplexity.SIMPLE: ModelTier(
            name="快速模型",
            provider="deepseek",
            model_id="deepseek-chat",
            cost_per_1k=0.001,
            max_tokens=4096,
            speed="fast"
        ),
        TaskComplexity.MEDIUM: ModelTier(
            name="均衡模型",
            provider="openai",
            model_id="gpt-3.5-turbo",
            cost_per_1k=0.01,
            max_tokens=4096,
            speed="medium"
        ),
        TaskComplexity.COMPLEX: ModelTier(
            name="强力模型",
            provider="openai",
            model_id="gpt-4",
            cost_per_1k=0.03,
            max_tokens=8192,
            speed="slow"
        )
    }

    def select_model(
        self,
        task_type: str,
        context_length: int = 0,
        quality_requirement: str = "medium"
    ) -> ModelTier:
        """
        选择合适的模型

        Args:
            task_type: 任务类型 (continue/polish/evaluate/plan等)
            context_length: 上下文长度
            quality_requirement: 质量要求 (low/medium/high)

        Returns:
            ModelTier: 选中的模型
        """
        # 根据任务类型判断复杂度
        complexity = self._determine_complexity(
            task_type,
            context_length,
            quality_requirement
        )

        return self.MODEL_TIERS[complexity]

    def _determine_complexity(
        self,
        task_type: str,
        context_length: int,
        quality_requirement: str
    ) -> TaskComplexity:
        """判断任务复杂度"""

        # 简单任务
        simple_tasks = ["evaluate", "classify", "extract"]
        if task_type in simple_tasks and quality_requirement != "high":
            return TaskComplexity.SIMPLE

        # 复杂任务
        complex_tasks = ["plan", "create_outline", "write_chapter"]
        if task_type in complex_tasks or quality_requirement == "high":
            return TaskComplexity.COMPLEX

        # 长上下文任务
        if context_length > 3000:
            return TaskComplexity.COMPLEX

        # 默认中等
        return TaskComplexity.MEDIUM

    def estimate_cost(
        self,
        model: ModelTier,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """估算成本"""
        total_tokens = input_tokens + output_tokens
        return (total_tokens / 1000) * model.cost_per_1k
```

---

## 6. 实施路线图

### 6.1 阶段一：核心基础设施改造（2-3周）

#### Week 1: Memory系统增强

**任务清单**:
- [ ] Day 1-2: 设计增强的Memory系统架构
  - 定义 MemoryItem、MemoryLayer 数据结构
  - 设计智能遗忘策略算法
  - 编写技术方案文档

- [ ] Day 3-4: 实现核心功能
  - 实现 `EnhancedMemoryManager` 类
  - 实现 `SmartForgetStrategy` 类
  - 实现分层记忆存储（Redis）

- [ ] Day 5: 实现状态快照
  - 实现 `create_snapshot()`
  - 实现 `restore_snapshot()`
  - 支持快照版本管理

**交付物**:
- `backend/app/services/agent/memory/enhanced_memory_manager.py`
- `backend/app/services/agent/memory/memory_strategy.py`
- 单元测试

#### Week 2: 工具系统标准化

**任务清单**:
- [ ] Day 1-2: 设计标准化工具接口
  - 定义 ToolInput、ToolOutput 基类
  - 定义 StandardTool 泛型类
  - 编写工具注册装饰器

- [ ] Day 3-4: 改造现有工具
  - 将 `continue_writing_tool` 改为标准格式
  - 将 `polish_text_tool` 改为标准格式
  - 将 `analyze_text_tool` 改为标准格式

- [ ] Day 5: 集成到LangGraph
  - 更新 `langgraph_agent.py` 使用新工具
  - 添加工具调用日志
  - 测试工具调用

**交付物**:
- `backend/app/services/agent/tools/tool_types.py`
- `backend/app/services/agent/tools/writing_tools.py` (重构)
- 工具注册文档

#### Week 3: 版本管理系统

**任务清单**:
- [ ] Day 1-2: 设计版本管理架构
  - 定义 Patch、Version、VersionedContent 数据结构
  - 设计补丁应用算法
  - 设计版本树遍历算法

- [ ] Day 3-4: 实现核心功能
  - 实现 `VersionControlService` 类
  - 实现补丁应用逻辑
  - 实现版本回滚

- [ ] Day 5: 集成到Agent
  - 在章节创作流程中集成版本管理
  - 添加版本历史API
  - 测试版本回滚

**交付物**:
- `backend/app/services/agent/version_control.py`
- API 端点 (`/api/v1/agent/versions/*`)
- 版本管理文档

### 6.2 阶段二：高价值功能集成（3-4周）

#### Week 4-5: 质量循环机制

**任务清单**:
- [ ] Week 4 Day 1-2: 设计质量评估系统
  - 定义评估维度
  - 设计评分算法
  - 设计LLM评估Prompt

- [ ] Week 4 Day 3-5: 实现质量评估
  - 实现 `QualityEvaluatorService`
  - 实现各维度评估逻辑
  - 测试评估准确性

- [ ] Week 5 Day 1-3: 实现质量循环
  - 实现 `QualityLoopManager`
  - 实现参数优化逻辑
  - 集成到写作流程

- [ ] Week 5 Day 4-5: 测试和优化
  - 端到端测试
  - 优化迭代策略
  - 性能调优

**交付物**:
- `backend/app/services/agent/quality_evaluator.py`
- 质量评估API
- 测试报告

#### Week 6: Prompt库优化

**任务清单**:
- [ ] Day 1-2: 整理Prompt库
  - 复制 novel-ai-agent-Chinese 的 Prompt
  - 适配到项目结构
  - 分类组织Prompt

- [ ] Day 3-4: 实现Prompt管理
  - 实现 `ContentCreationPrompts` 类
  - 实现 `PromptOptimizer` 类
  - 支持动态Prompt组合

- [ ] Day 5: 集成到Agent
  - 更新Agent使用新Prompt
  - A/B测试对比效果
  - 收集用户反馈

**交付物**:
- `backend/app/services/agent/prompt_library.py`
- Prompt管理文档
- 效果对比报告

#### Week 7: 模型分级策略

**任务清单**:
- [ ] Day 1-2: 设计模型选择策略
  - 定义任务复杂度分类
  - 配置模型层级
  - 设计成本估算

- [ ] Day 3-4: 实现模型选择器
  - 实现 `ModelSelector` 类
  - 实现复杂度判断逻辑
  - 实现成本追踪

- [ ] Day 5: 集成和测试
  - 集成到Agent工作流
  - 测试成本优化效果
  - 调整策略参数

**交付物**:
- `backend/app/services/agent/model_selector.py`
- 成本优化报告
- 模型选择文档

### 6.3 阶段三：架构优化与完善（2-3周）

#### Week 8-9: 引入ARE设计理念

**任务清单**:
- [ ] Week 8: 重构Action层
  - 标准化所有节点函数为Action
  - 实现Action基类
  - 重构现有节点

- [ ] Week 9: 实现Environment层
  - 实现消息总线
  - 实现状态管理中枢
  - 重构Agent协作逻辑

**交付物**:
- 重构后的Agent架构
- 架构文档更新

#### Week 10: 完善和优化

**任务清单**:
- [ ] Day 1-2: 性能优化
  - 优化Memory查询性能
  - 优化工具调用性能
  - 优化LLM调用次数

- [ ] Day 3-4: 监控和日志
  - 添加性能监控
  - 添加成本追踪
  - 完善错误日志

- [ ] Day 5: 文档完善
  - 更新API文档
  - 编写使用示例
  - 编写最佳实践指南

**交付物**:
- 性能优化报告
- 完整的技术文档
- 使用手册

---

## 7. API 设计

### 7.1 版本管理API

```python
# GET /api/v1/agent/versions/{content_id}
# 获取版本历史

# POST /api/v1/agent/versions/{content_id}/rollback
# 回滚到指定版本
{
  "version_id": "v_abc123"
}

# GET /api/v1/agent/versions/{content_id}/compare
# 对比两个版本
{
  "version_id_1": "v_abc123",
  "version_id_2": "v_def456"
}

# POST /api/v1/agent/versions/{content_id}/branch
# 创建分支
{
  "branch_name": "experimental",
  "from_version_id": "v_abc123"
}
```

### 7.2 质量评估API

```python
# POST /api/v1/agent/quality/evaluate
# 评估内容质量
{
  "content": "待评估的内容...",
  "context": {
    "previous_content": "前文内容...",
    "target_length": 500
  },
  "dimensions": ["content_quality", "length_check", "coherence"]
}

# Response
{
  "overall_score": 8.5,
  "dimension_scores": [
    {
      "dimension": "content_quality",
      "score": 9.0,
      "feedback": "内容生动有趣",
      "weight": 2.0
    },
    ...
  ],
  "passes": true,
  "feedback": "内容质量优秀！",
  "suggestions": []
}
```

### 7.3 增强的Agent对话API

```python
# POST /api/v1/agent/chat
{
  "message": "帮我续写",
  "work_id": "123",
  "chapter_id": "456",
  "conversation_id": "conv_789",
  "options": {
    "enable_quality_loop": true,    # 启用质量循环
    "enable_version_control": true, # 启用版本管理
    "quality_threshold": 8.0,       # 质量阈值
    "max_iterations": 3             # 最大迭代次数
  }
}

# Response (流式)
data: {"type": "status", "message": "开始生成内容..."}
data: {"type": "content", "content": "续写的内容..."}
data: {"type": "evaluation", "score": 7.5, "feedback": "质量一般，重试..."}
data: {"type": "content", "content": "改进后的内容..."}
data: {"type": "evaluation", "score": 8.5, "feedback": "质量良好，通过！"}
data: {"type": "version", "version_id": "v_abc123"}
data: {"type": "done"}
```

---

## 8. 数据库设计

### 8.1 新增表

```sql
-- 版本历史表
CREATE TABLE agent_content_versions (
    id SERIAL PRIMARY KEY,
    content_id VARCHAR(100) NOT NULL,
    version_id VARCHAR(50) NOT NULL,
    parent_version_id VARCHAR(50),
    patches JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_by VARCHAR(100) NOT NULL,
    tag VARCHAR(50),
    description TEXT,
    INDEX idx_content_id (content_id),
    INDEX idx_version_id (version_id)
);

-- 质量评估记录表
CREATE TABLE agent_quality_evaluations (
    id SERIAL PRIMARY KEY,
    content_id VARCHAR(100) NOT NULL,
    version_id VARCHAR(50),
    overall_score FLOAT NOT NULL,
    dimension_scores JSONB NOT NULL,
    passes BOOLEAN NOT NULL,
    feedback TEXT,
    suggestions JSONB,
    created_at TIMESTAMP NOT NULL,
    INDEX idx_content_id (content_id)
);

-- Agent执行日志表
CREATE TABLE agent_execution_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    conversation_id VARCHAR(100),
    agent_type VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    model_used VARCHAR(50),
    tokens_used INTEGER,
    cost FLOAT,
    duration_ms INTEGER,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    created_at TIMESTAMP NOT NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_created_at (created_at)
);

-- 成本统计表
CREATE TABLE agent_cost_stats (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    model VARCHAR(50) NOT NULL,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    total_cost FLOAT NOT NULL DEFAULT 0,
    request_count INTEGER NOT NULL DEFAULT 0,
    UNIQUE (user_id, date, model),
    INDEX idx_user_date (user_id, date)
);
```

### 8.2 Redis数据结构

```
# Memory 存储
memory:{user_id}:short_term -> List<MemoryItem>
memory:{user_id}:medium_term -> List<MemoryItem>
memory:{user_id}:long_term -> String (压缩摘要)

# 版本控制
version:{content_id} -> VersionedContent (JSON)

# 会话状态
session:{conversation_id}:state -> AgentState (JSON)
session:{conversation_id}:snapshot:{snapshot_id} -> State Snapshot

# 工具统计
tool:stats:{tool_id} -> ToolMetadata (JSON)
```

---

## 9. 测试计划

### 9.1 单元测试

**测试覆盖率目标: 80%+**

```python
# tests/agent/test_memory_manager.py
def test_add_memory()
def test_smart_forgetting()
def test_create_snapshot()
def test_restore_snapshot()

# tests/agent/test_version_control.py
def test_create_content()
def test_apply_patch()
def test_rollback()
def test_branch_creation()

# tests/agent/test_quality_evaluator.py
def test_evaluate_content_quality()
def test_evaluate_length()
def test_evaluate_coherence()
def test_quality_loop()

# tests/agent/test_model_selector.py
def test_select_simple_model()
def test_select_complex_model()
def test_cost_estimation()
```

### 9.2 集成测试

```python
# tests/integration/test_agent_workflow.py
async def test_writing_with_quality_loop():
    """测试带质量循环的写作流程"""
    pass

async def test_writing_with_version_control():
    """测试带版本管理的写作流程"""
    pass

async def test_model_auto_selection():
    """测试模型自动选择"""
    pass
```

### 9.3 性能测试

```python
# tests/performance/test_memory_performance.py
def test_memory_retrieval_speed():
    """测试记忆检索速度 (< 100ms)"""
    pass

def test_version_rollback_speed():
    """测试版本回滚速度 (< 200ms)"""
    pass

def test_quality_evaluation_speed():
    """测试质量评估速度 (< 2s)"""
    pass
```

### 9.4 A/B测试

**对比指标**:
- 内容质量分数（旧版 vs 新版）
- 用户满意度（用户反馈）
- 成本节省（API调用成本）
- 响应速度（端到端时间）

---

## 10. 风险控制

### 10.1 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| Memory系统性能问题 | 高 | 中 | 1. Redis缓存优化<br>2. 异步加载<br>3. 分层存储 |
| 版本管理数据量过大 | 中 | 中 | 1. 定期清理旧版本<br>2. 压缩存储<br>3. 分页查询 |
| 质量循环增加响应时间 | 高 | 高 | 1. 异步处理<br>2. 流式反馈<br>3. 超时控制 |
| LLM API不稳定 | 高 | 中 | 1. 重试机制<br>2. 降级策略<br>3. 多提供商备份 |

### 10.2 业务风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 新功能用户不接受 | 中 | 低 | 1. 配置开关<br>2. 灰度发布<br>3. 用户反馈 |
| 成本超预算 | 高 | 中 | 1. 成本监控<br>2. 用量限制<br>3. 模型分级 |
| 质量评估不准确 | 中 | 中 | 1. 持续优化Prompt<br>2. 人工校准<br>3. 用户反馈 |

### 10.3 回滚预案

**紧急回滚机制**:

1. **配置开关回滚**
   ```python
   # config.py
   ENABLE_ENHANCED_MEMORY = False
   ENABLE_QUALITY_LOOP = False
   ENABLE_VERSION_CONTROL = False
   ```

2. **数据库回滚**
   - 保留Alembic迁移脚本
   - 支持一键回滚数据库更改

3. **代码回滚**
   - Git分支管理
   - 快速revert功能

---

## 11. 成功指标

### 11.1 技术指标

- ✅ **Memory检索速度**: < 100ms
- ✅ **版本回滚速度**: < 200ms
- ✅ **质量评估准确率**: > 80%
- ✅ **API成本降低**: 40-50%
- ✅ **代码测试覆盖率**: > 80%

### 11.2 业务指标

- ✅ **内容质量提升**: 质量分数 +15%
- ✅ **用户满意度**: 满意度评分 > 4.5/5
- ✅ **响应速度**: 端到端时间 < 10s
- ✅ **成本节省**: 每用户成本降低 45%

---

## 12. 下一步行动

### 12.1 立即开始（本周）

1. ✅ 完成开发文档审阅
2. ✅ 搭建开发环境
3. ✅ 创建Git分支 `feature/agent-enhancement`
4. ✅ 开始 Week 1 任务

### 12.2 需要确认的问题

1. **优先级确认**: 是否同意分阶段实施？
2. **时间安排**: 总计 7-10周 是否可接受？
3. **资源投入**: 是否需要额外开发人员？
4. **测试策略**: 是否需要外部测试用户？

---

**文档结束**

> 如有任何问题或需要调整，请随时反馈！
