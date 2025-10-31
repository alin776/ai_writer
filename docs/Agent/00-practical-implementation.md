# AI Writer Agent 务实实施方案

> 基于7个小说写作Agent项目的深度分析
>
> 结合当前项目实际情况的落地方案
>
> 版本：v2.0 实战版

---

## 🔍 研究项目分析总结

### 1. AI_Gen_Novel (cjyyx)
**核心思路**：基于 RecurrentGPT 的循环生成模式

```
关键发现:
├─ Planning → Transformation → Review 三阶段
├─ 语言驱动的循环计算
├─ 借鉴网文写作经验优化流程
└─ 坦承: 当前LLM能力不足以生成长篇网文
```

**可借鉴点**：
- ✅ 三阶段写作流程（规划→转换→评审）
- ✅ 循环迭代机制
- ❌ 但要承认局限性：不要一次生成太长

---

### 2. pulpgen
**核心思路**：基于 Gemini 的命令行工具，三相流程

```
Phase 1: Outlining (大纲规划)
   ↓
Phase 2: Auto-writing (自动写作)
   ↓
Phase 3: Interactive Editing (交互式编辑)
```

**可借鉴点**：
- ✅ 清晰的三阶段流程
- ✅ 交互式编辑（AI分析 + 用户选择应用补丁）
- ✅ 配置化模型参数（temperature, top_p等）
- ✅ 增量改进：指定字数扩写、带指令重写等

---

### 3. novel-multi-agents (OpenAI Agent SDK)
**核心思路**：多Agent协作架构

```
NovelAssistant (协调者)
    ↓
PlanStoryAction (规划Agent)
    ├─ Brainstorming
    ├─ Character Setup
    ├─ Story Structure Planning
    └─ Core Plot Development
```

**可借鉴点**：
- ✅ 协调者 + 专项Agent 模式
- ✅ 角色职责明确
- ✅ 适合复杂任务分解

---

### 4. MetaGPT 框架思路
**核心思路**：SOP（标准化操作流程）+ 角色专业化

```
Product Manager → PRD
    ↓
Architect → Tech Specs
    ↓
Engineers → Implementation
```

**可借鉴点**：
- ✅ SOP 编码到 Prompt
- ✅ 模块化输出（减少累积错误）
- ✅ 角色专业化

---

### 5. 中文小说写作Agent共性
**发现的模式**：

1. **三段论写作流程**（几乎所有项目）：
   - 规划 → 执行 → 评审

2. **协调者模式**：
   - 一个中心Agent协调多个专项Agent

3. **渐进式生成**：
   - 不要一次生成太多
   - 章节级别生成 + 段落级别精修

4. **人机协同必不可少**：
   - 关键节点需要人工介入
   - AI提供建议，人类做决策

---

## 🎯 对你们项目的启示

### 当前系统回顾

你们已有：
```
✅ LangGraph 基础架构
✅ ChatOpenAI 模式（已启用）
✅ 意图分类 + 5种场景
✅ 7个工具（续写/润色/分析等）
✅ Planning/Reflection Agent
✅ Memory Manager + User Profile
```

### 问题诊断

```
❌ 扁平化架构（无协调者）
❌ 一次性生成（无循环优化）
❌ 工具串行调用（性能差）
❌ 内存Checkpointer（不持久）
❌ 缺乏HITL（人机协同弱）
```

---

## 🚀 务实实施方案（3周迭代）

### 设计原则

```
1. 渐进式改造（不推倒重来）
2. 保留现有优势（LangGraph + 工具）
3. 借鉴成功模式（协调者 + 三阶段）
4. 务实可落地（3周见效）
```

---

## 第一周：核心流程重构

### 目标：实现 Planning → Writing → Review 三阶段

#### 1.1 新增 Writing Coordinator（写作协调者）

```python
# backend/app/services/agent/coordinators/writing_coordinator.py
class WritingCoordinator:
    """
    写作协调者 - 管理完整写作流程

    借鉴: pulpgen + novel-multi-agents
    """

    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.phases = ["planning", "writing", "review"]

    async def coordinate_writing(self, request: WritingRequest):
        """协调写作流程"""

        # Phase 1: Planning（规划阶段）
        plan = await self._planning_phase(request)

        # Phase 2: Writing（写作阶段）
        draft = await self._writing_phase(plan)

        # Phase 3: Review（评审阶段）
        final = await self._review_phase(draft)

        return final

    async def _planning_phase(self, request):
        """
        规划阶段

        借鉴: MetaGPT 的 SOP + pulpgen 的 Outlining
        """

        logger.info("[Phase 1] 开始规划")

        # 1. 理解需求
        intent = await self._analyze_intent(request.message)

        # 2. 制定计划
        if intent == "continue_writing":
            plan = await self._plan_continuation(request)
        elif intent == "new_chapter":
            plan = await self._plan_new_chapter(request)
        else:
            plan = await self._plan_general(request)

        return {
            "intent": intent,
            "plan": plan,
            "target_length": self._estimate_length(plan),
            "structure": self._extract_structure(plan)
        }

    async def _writing_phase(self, plan):
        """
        写作阶段（渐进式生成）

        借鉴: RecurrentGPT 的循环生成
        """

        logger.info("[Phase 2] 开始写作")

        structure = plan["structure"]
        draft_parts = []

        # 分段生成（避免一次生成太长）
        for i, section in enumerate(structure):
            logger.info(f"[Phase 2] 生成第 {i+1}/{len(structure)} 段")

            # 上下文：已生成的内容 + 当前段落要求
            context = {
                "previous_content": "\n".join(draft_parts[-2:]),  # 最近2段
                "section_plan": section,
                "overall_plan": plan["plan"]
            }

            part = await self._generate_section(context)
            draft_parts.append(part)

        return {
            "content": "\n\n".join(draft_parts),
            "parts": draft_parts,
            "metadata": {
                "sections": len(draft_parts),
                "word_count": sum(len(p) for p in draft_parts)
            }
        }

    async def _review_phase(self, draft):
        """
        评审阶段（质量检查 + 改进）

        借鉴: AI_Gen_Novel 的 Review + Reflection Pattern
        """

        logger.info("[Phase 3] 开始评审")

        content = draft["content"]

        # 1. 质量评估
        evaluation = await self._evaluate_quality(content)

        logger.info(f"[Phase 3] 质量评分: {evaluation['score']}")

        # 2. 决定是否需要改进
        if evaluation["score"] < 75:
            logger.info("[Phase 3] 质量不达标，进行改进")
            improved = await self._improve_content(content, evaluation["issues"])

            return {
                "content": improved,
                "original_score": evaluation["score"],
                "improved": True
            }
        else:
            return {
                "content": content,
                "score": evaluation["score"],
                "improved": False
            }
```

#### 1.2 实现 Section-based Generation（分段生成）

```python
async def _generate_section(self, context):
    """
    生成单个段落（500-800字）

    关键: 小块生成 + 保持连贯
    """

    prompt = f"""
你是一位专业的网文作家。

已写内容:
{context['previous_content'][-1000:]}  # 最近1000字

本段要求:
{context['section_plan']}

整体规划:
{context['overall_plan'][:500]}  # 规划摘要

要求:
1. 字数: 500-800字
2. 与上文自然衔接
3. 符合本段规划要求
4. 保持故事节奏

请开始写作:
"""

    section = await self.ai_service.generate(
        prompt,
        temperature=0.8,  # 创意性
        max_tokens=1000
    )

    return section
```

#### 1.3 集成到现有系统

```python
# backend/app/api/v1/agent.py

@router.post("/chat/writing")
async def agent_writing_v2(
    request: AgentChatRequest,
    current_user: User = Depends(get_current_active_user),
    ai_service: HTTPAIService = Depends(get_ai_service)
):
    """
    新版写作接口 - 使用 Writing Coordinator
    """

    # 创建协调者
    coordinator = WritingCoordinator(ai_service)

    # 协调写作流程
    result = await coordinator.coordinate_writing(
        WritingRequest(
            message=request.message,
            work_id=request.work_id,
            chapter_id=request.chapter_id,
            user_id=str(current_user.id)
        )
    )

    return {
        "response": result["content"],
        "metadata": result.get("metadata", {}),
        "improved": result.get("improved", False),
        "score": result.get("score")
    }
```

---

## 第二周：增强交互和人机协同

### 目标：实现 HITL + 交互式编辑

#### 2.1 Interactive Editing（借鉴 pulpgen）

```python
class InteractiveEditor:
    """
    交互式编辑器

    借鉴: pulpgen 的 Phase 3
    """

    async def edit_menu(self, draft):
        """提供编辑选项"""

        return {
            "draft": draft,
            "suggestions": await self._generate_suggestions(draft),
            "actions": [
                {
                    "id": "expand",
                    "name": "扩写",
                    "description": "增加到指定字数",
                    "params": {"target_words": "int"}
                },
                {
                    "id": "rewrite",
                    "name": "重写",
                    "description": "按照新指令重写",
                    "params": {"instruction": "str"}
                },
                {
                    "id": "polish",
                    "name": "润色",
                    "description": "改进语言表达"
                },
                {
                    "id": "analyze",
                    "name": "AI分析",
                    "description": "获取改进建议"
                }
            ]
        }

    async def apply_edit(self, draft, action, params):
        """应用编辑操作"""

        if action == "expand":
            return await self._expand_to_length(draft, params["target_words"])
        elif action == "rewrite":
            return await self._rewrite_with_instruction(draft, params["instruction"])
        elif action == "polish":
            return await self._polish(draft)
        elif action == "analyze":
            return await self._ai_analyze(draft)
```

#### 2.2 HITL Checkpoints（人机协同检查点）

```python
class HITLManager:
    """
    人机协同管理器

    借鉴: LangGraph HITL + novel-multi-agents 的协调模式
    """

    CHECKPOINTS = ["after_planning", "after_draft", "before_final"]

    async def check_approval(self, stage, content):
        """检查是否需要人工审批"""

        if stage not in self.CHECKPOINTS:
            return {"approved": True, "auto": True}

        # 暂停流程，等待用户反馈
        approval_request = {
            "stage": stage,
            "content": content,
            "options": ["通过", "修改", "重做"],
            "timeout": 300  # 5分钟超时
        }

        # 保存到 Redis（等待前端响应）
        await self.redis.set(
            f"approval:{stage}:{uuid}",
            json.dumps(approval_request),
            ex=300
        )

        return {
            "approved": False,
            "requires_human": True,
            "request_id": uuid
        }
```

---

## 第三周：优化和完善

### 目标：性能优化 + 持久化 + 用户体验

#### 3.1 PostgreSQL Checkpointer（持久化）

```python
# 直接使用第一周文档中的方案
from langgraph.checkpoint.postgres import AsyncPostgresSaver

checkpointer = AsyncPostgresSaver.from_conn_string(settings.DATABASE_URL)
await checkpointer.setup()
```

#### 3.2 并行工具调用

```python
async def parallel_context_gathering(work_id, chapter_id, user_id):
    """并行获取上下文"""

    tasks = [
        get_context_tool(work_id, chapter_id),
        search_analysis_fragments_tool(work_id, "情节发展"),
        get_user_style(user_id),
        get_chapter_history(work_id)
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    return {
        "context": results[0],
        "knowledge": results[1],
        "style": results[2],
        "history": results[3]
    }
```

#### 3.3 动态模型选择（成本优化）

```python
class ModelRouter:
    """模型路由器"""

    MODELS = {
        "fast": "gemini-2.5-flash",      # 规划、分析
        "balanced": "gemini-2.5-pro",    # 写作
        "powerful": "gpt-5"              # 复杂任务
    }

    def select_model(self, phase, complexity):
        if phase == "planning":
            return self.MODELS["fast"]
        elif phase == "writing" and complexity == "high":
            return self.MODELS["powerful"]
        else:
            return self.MODELS["balanced"]
```

---

## 📊 最终架构图

```
                    ┌─────────────────────┐
                    │  Writing Coordinator│  ← 新增：协调者
                    │   (三阶段管理)        │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
   ┌────▼────┐          ┌─────▼──────┐        ┌─────▼──────┐
   │ Phase 1 │          │  Phase 2   │        │  Phase 3   │
   │Planning │          │  Writing   │        │  Review    │
   └────┬────┘          └─────┬──────┘        └─────┬──────┘
        │                     │                      │
        │                     │                      │
   ┌────▼────────┐      ┌────▼────────┐       ┌────▼────────┐
   │ 需求分析     │      │ 分段生成     │       │ 质量评估     │
   │ 制定计划     │      │ (500-800字)  │       │ 改进建议     │
   │ 结构拆分     │      │ 循环迭代     │       │ 应用改进     │
   └─────────────┘      └──────┬──────┘       └─────────────┘
                                │
                         ┌──────▼──────┐
                         │ HITL检查点   │  ← 新增：人机协同
                         │ (可选暂停)    │
                         └─────────────┘
```

---

## 🎯 核心特性对比

### 改造前 vs 改造后

| 特性 | 改造前 | 改造后 |
|------|--------|--------|
| **架构** | 扁平化，5个并列Agent | 协调者模式，三阶段流程 |
| **生成方式** | 一次性生成 | 分段生成（500-800字） |
| **质量保证** | 无 | Planning → Writing → Review |
| **人机协同** | 弱 | HITL检查点 + 交互式编辑 |
| **工具调用** | 串行 | 并行（性能↑50%） |
| **记忆系统** | 内存 | PostgreSQL持久化 |
| **模型选择** | 固定 | 动态路由（成本↓30%） |

---

## 📝 实施检查清单

### Week 1: 核心流程

- [ ] 实现 WritingCoordinator
- [ ] 三阶段流程（Planning/Writing/Review）
- [ ] 分段生成逻辑
- [ ] 质量评估机制
- [ ] 集成测试

### Week 2: 交互增强

- [ ] InteractiveEditor 实现
- [ ] HITL检查点
- [ ] 前端交互UI
- [ ] 编辑操作API
- [ ] 用户测试

### Week 3: 优化完善

- [ ] PostgreSQL Checkpointer
- [ ] 并行工具调用
- [ ] 动态模型路由
- [ ] 性能测试
- [ ] 文档更新

---

## 🚀 快速开始

### 1. 创建新文件

```bash
# 创建协调者目录
mkdir -p backend/app/services/agent/coordinators

# 创建编辑器目录
mkdir -p backend/app/services/agent/editors
```

### 2. 复制示例代码

将上面的 `WritingCoordinator` 代码保存到：
`backend/app/services/agent/coordinators/writing_coordinator.py`

### 3. 修改路由

在 `backend/app/api/v1/agent.py` 添加新路由

### 4. 测试

```python
# 测试脚本
async def test_writing_coordinator():
    coordinator = WritingCoordinator(ai_service)

    result = await coordinator.coordinate_writing(
        WritingRequest(
            message="帮我写第三章，主角遇到了神秘高手",
            work_id="test_work",
            chapter_id="chapter_3"
        )
    )

    assert result["metadata"]["sections"] > 0
    assert result["content"]
    print(f"生成成功: {result['metadata']['word_count']}字")
```

---

## 💡 关键洞察

### 1. 不要追求完美

```
❌ 错误: 一次生成5000字完美小说
✅ 正确: 分段生成，逐步优化
```

### 2. 人机协同是必须的

```
❌ 错误: 完全自动化
✅ 正确: 关键节点人工介入
```

### 3. 渐进式改造

```
❌ 错误: 推倒重来
✅ 正确: 保留现有优势，逐步增强
```

### 4. 借鉴但不照搬

```
✅ pulpgen: 三阶段流程
✅ novel-multi-agents: 协调者模式
✅ RecurrentGPT: 循环生成
✅ MetaGPT: SOP思想

但要结合你们的 LangGraph 架构
```

---

## 📚 参考资料

### 借鉴的项目

1. **cjyyx/AI_Gen_Novel** - 循环生成模式
2. **pulpgen-dev/pulpgen** - 三阶段流程
3. **novel-multi-agents** - 协调者模式
4. **MetaGPT** - SOP标准化流程

### 技术文档

- LangGraph Checkpointer
- HITL Implementation
- Multi-Agent Coordination

---

## ✅ 成功标准

3周后应达到：

- [ ] 支持 500-2000 字的章节生成
- [ ] 质量评分 > 75 分的内容占比 > 80%
- [ ] 响应时间 < 30秒（单段）
- [ ] 用户满意度 > 4.0/5.0
- [ ] 成本降低 30%
- [ ] 会话持久化正常工作

---

**下一步**：建议从 Week 1 的 WritingCoordinator 开始实施。需要我帮你写完整代码吗？
