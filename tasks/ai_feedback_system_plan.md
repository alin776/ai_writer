# AI 交互式反馈系统 - 优化方案与实施计划

> **创建时间**: 2025-10-26
> **优先级**: P0 (差异化核心功能)
> **预计工期**: 3天
> **状态**: 规划中

---

## 📋 功能概述

### 核心价值

AI交互式反馈系统是一个**实时评价 + 持续对话**的双模式系统,与现有功能对比:

| 功能 | 小说分析 | AI去痕迹 | **AI反馈系统** |
|------|---------|---------|---------------|
| **定位** | 宏观诊断 | 微观优化 | **持续指导** |
| **触发时机** | 手动启动 | 生成后 | **生成中/后** |
| **交互方式** | 一次性报告 | 自动处理 | **多轮对话** |
| **上下文** | 整部作品 | 单段文本 | **章节+世界观** |

### 差异化优势

1. **即时反馈** - AI生成内容后立即评分(0-100),让用户知道"这次生成得好不好"
2. **透明化思考** - 显示AI的评价逻辑(5维度评分),增强信任感
3. **可对话** - 用户可以追问"为什么这样写?""如何改进?",AI记住上下文
4. **个性化** - 根据作品世界观、人物设定提供针对性建议

---

## 🎯 两种工作模式

### 模式1: 即时评价模式 (推荐优先实现⭐⭐⭐)

**使用场景**: 用户在编辑器中使用AI续写/润色后

**工作流程**:
```
用户点击"续写"
  → AI生成内容 (流式输出)
  → 自动触发评价 (后台运行)
  → 显示评分卡片 (5维度 + 总分)
  → 用户可选:
      - 接受内容 (保存到编辑器)
      - 查看详情 (展开优点/缺点/建议)
      - 重新生成 (带上评价反馈)
      - 进入对话模式 (深度讨论)
```

**技术实现**:
```python
# 后端新增接口
POST /ai/evaluate
{
  "text": "AI生成的内容",
  "context": {
    "work_id": 123,
    "chapter_id": 456,
    "previous_text": "前文500字"
  }
}

# 响应
{
  "overall_score": 82,
  "dimensions": {
    "literary_quality": 85,    // 文学性
    "coherence": 80,           // 连贯性
    "creativity": 78,          // 创意性
    "emotional_impact": 84,    // 情感感染力
    "pacing": 75               // 节奏把控
  },
  "highlights": [
    "语言流畅自然,修辞手法运用得当",
    "情感描写细腻,能引发读者共鸣",
    "人物对话符合角色性格"
  ],
  "issues": [
    "节奏略慢,可适当加快推进",
    "部分描写过于详细,可精简"
  ],
  "suggestions": [
    "建议删减第2段中的景物描写,直接进入对话",
    "可增加一个转折,提升紧张感"
  ]
}
```

### 模式2: 持续对话模式 (高级功能)

**使用场景**: 用户需要深度创作指导

**工作流程**:
```
用户创建反馈会话 (选择模式: general/plot/character/conflict/pacing)
  → 绑定作品/章节 (自动加载上下文)
  → 多轮对话:
      User: "我想写一个反转情节,但不知道怎么铺垫"
      AI: "根据你的世界观设定...[结合上下文建议]"
      User: "具体在哪里加这个线索比较好?"
      AI: "建议在第3章和第5章各埋一个伏笔..."
  → 保存对话历史 (随时恢复)
```

**技术实现**:
- 使用 LangChain Memory 管理对话历史
- 自动加载作品世界观、人物设定作为上下文
- 5种专家模式(剧情/人物/冲突/节奏/通用)

---

## 🔧 优化建议 (相比原方案)

### 问题1: Memory 内存泄漏风险 ⚠️

**原方案**:
```python
self._memories: dict[int, ConversationBufferMemory] = {}
# 问题: 会话越来越多,内存无限增长
```

**优化方案**:
```python
from cachetools import TTLCache

class FeedbackService:
    def __init__(self):
        self.http_ai = HTTPAIService()
        # 使用TTL缓存,1小时后自动清理
        self._memories = TTLCache(maxsize=1000, ttl=3600)

    async def _load_memory_from_db(self, session_id: int, db: AsyncSession):
        """从数据库恢复历史消息到Memory"""
        if session_id in self._memories:
            return self._memories[session_id]

        # 从数据库加载最近20条消息
        messages = await db.execute(
            select(FeedbackMessage)
            .where(FeedbackMessage.session_id == session_id)
            .order_by(FeedbackMessage.created_at.desc())
            .limit(20)
        )

        memory = ConversationBufferMemory(return_messages=True)
        for msg in reversed(messages.scalars().all()):
            if msg.role == "user":
                memory.chat_memory.add_user_message(msg.content)
            else:
                memory.chat_memory.add_ai_message(msg.content)

        self._memories[session_id] = memory
        return memory
```

### 问题2: 上下文加载不够智能 🤔

**原方案**: 只加载作品简介 + 章节前500字

**优化方案**: 智能提取相关上下文
```python
async def _load_smart_context(
    self,
    db: AsyncSession,
    work_id: int,
    chapter_id: int,
    user_message: str
) -> str:
    """智能加载上下文"""
    context_parts = []

    # 1. 基础信息
    work = await self._get_work(db, work_id)
    context_parts.append(f"作品: {work.title} ({work.genre})")

    # 2. 根据用户问题,智能加载世界观
    if "人物" in user_message or "角色" in user_message:
        characters = await self._get_characters(db, work_id)
        context_parts.append(f"主要人物: {', '.join([c.name for c in characters[:5]])}")

    if "地点" in user_message or "场景" in user_message:
        locations = await self._get_locations(db, work_id)
        context_parts.append(f"主要地点: {', '.join([l.name for l in locations[:3]])}")

    # 3. 当前章节摘要(如果存在)
    chapter = await self._get_chapter(db, chapter_id)
    if chapter.summary:
        context_parts.append(f"章节概要: {chapter.summary}")

    # 4. 前一章节的结尾(承上启下)
    prev_chapter = await self._get_previous_chapter(db, chapter_id)
    if prev_chapter:
        context_parts.append(f"前章结尾: {prev_chapter.content[-200:]}...")

    return "\n\n".join(context_parts)
```

### 问题3: Prompt 可以更专业 ✨

**增强版 Prompt**:
```python
INSTANT_EVALUATION_PROMPT = """你是专业的AI文本评审专家。请对以下生成内容进行客观、严谨的评价。

生成内容:
{text}

上下文信息:
{context}

请从以下5个维度评分(0-100):
1. **文学性** - 语言质量、修辞手法、文字美感
2. **连贯性** - 与前文衔接、逻辑流畅度
3. **创意性** - 新颖度、想象力、打破常规
4. **情感感染力** - 情感表达、读者共鸣度
5. **节奏把控** - 快慢适度、张弛有度

返回JSON格式:
{{
  "overall_score": 总分(5个维度的平均分),
  "dimensions": {{
    "literary_quality": 分数,
    "coherence": 分数,
    "creativity": 分数,
    "emotional_impact": 分数,
    "pacing": 分数
  }},
  "highlights": ["优点1", "优点2", "优点3"],  // 3-5个具体亮点
  "issues": ["问题1", "问题2"],              // 2-3个可改进点
  "suggestions": ["建议1", "建议2"]          // 具体可操作的修改建议
}}

评价要求:
- 客观中立,既要肯定优点也要指出不足
- 建议要具体可操作,不要泛泛而谈
- 结合上下文和作品风格评价
- 避免主观偏见,以读者视角评判
"""
```

---

## 🚀 实施方案

### Phase 1: 即时评价模式 (Day 1-2) ⭐ 优先

**Day 1 上午**: 后端实现
- [ ] 创建评价Prompt模板
- [ ] 实现 `EvaluationService.evaluate_text()` 方法
- [ ] 添加 `POST /ai/evaluate` API接口
- [ ] 单元测试

**Day 1 下午**: 前端实现
- [ ] 创建类型定义 `src/types/evaluation.ts`
- [ ] 扩展 `AIService.evaluateText()`
- [ ] 创建 `useAIEvaluation` Hook
- [ ] 创建 `AIEvaluationCard` 组件(评分卡片)

**Day 2 上午**: 集成到编辑器
- [ ] 修改 AI 菜单,添加"查看评价"按钮
- [ ] 在AI生成完成后自动触发评价
- [ ] 显示评分卡片(可折叠/展开)
- [ ] 实现"重新生成"功能(带评价反馈)

**Day 2 下午**: 测试与优化
- [ ] 端到端测试
- [ ] UI/UX 优化
- [ ] 性能测试(评价延迟<2s)

### Phase 2: 对话模式 (Day 3) - 可选

**如果时间充裕**,实现完整的多轮对话功能:
- [ ] 数据库迁移(feedback_sessions + feedback_messages)
- [ ] 实现 FeedbackService (带Memory管理)
- [ ] API路由 (创建/列表/对话/删除会话)
- [ ] 前端对话界面
- [ ] 集成到编辑器侧边栏

**如果时间紧张**,暂缓对话模式,先上线即时评价

---

## 📊 成本分析

### Token消耗估算

**即时评价模式** (500字文本):
```
Prompt Tokens:
  - 系统Prompt: ~400
  - 待评价文本: ~750
  - 上下文信息: ~300
  = 1450 tokens

Completion Tokens:
  - JSON结构化输出: ~500

总计: ~1950 tokens
成本: $0.02 (GPT-4 Turbo)
```

**对话模式** (单轮):
```
Prompt Tokens:
  - 系统Prompt: ~500
  - 历史对话(10轮): ~2000
  - 上下文: ~500
  - 用户问题: ~100
  = 3100 tokens

Completion Tokens: ~800

总计: ~3900 tokens
成本: $0.04 (GPT-4 Turbo)
```

### 成本优化策略

1. **智能触发**: 只在用户主动请求时评价,不自动评价所有生成
2. **缓存结果**: 相同内容不重复评价
3. **模型降级**: 评价功能可用 GPT-3.5-Turbo (便宜10倍)
4. **上下文裁剪**: 只加载必要的上下文信息

---

## 🎨 UI/UX 设计建议

### 即时评价卡片 (Compact Mode)

```
┌─────────────────────────────────────┐
│ 🎯 AI生成质量评分: 82分 ⭐⭐⭐⭐     │
├─────────────────────────────────────┤
│ 文学性 █████████░ 85               │
│ 连贯性 ████████░░ 80               │
│ 创意性 ███████░░░ 78               │
│ 情感   ████████░░ 84               │
│ 节奏   ███████░░░ 75               │
│                                      │
│ [✓ 接受] [🔄 重新生成] [💬 详细分析] │
└─────────────────────────────────────┘
```

### 详细分析面板 (Expanded Mode)

```
┌─────────────────────────────────────┐
│ ✨ 优点 (3个亮点)                    │
│ • 语言流畅自然,修辞手法运用得当      │
│ • 情感描写细腻,能引发读者共鸣        │
│ • 人物对话符合角色性格              │
├─────────────────────────────────────┤
│ ⚠️ 可改进 (2个问题)                 │
│ • 节奏略慢,可适当加快推进            │
│ • 部分描写过于详细,可精简            │
├─────────────────────────────────────┤
│ 💡 建议 (具体修改方案)               │
│ 1. 删减第2段景物描写,直接进入对话    │
│ 2. 增加一个转折,提升紧张感           │
│                                      │
│ [应用建议] [进入对话模式]            │
└─────────────────────────────────────┘
```

---

## ✅ 验收标准

### 功能验收
- [ ] 评价功能正常工作,返回5维度评分
- [ ] 评分合理(符合人类判断)
- [ ] 优点/缺点/建议具体可操作
- [ ] UI交互流畅,不影响创作体验

### 性能验收
- [ ] 评价响应时间 < 3秒
- [ ] 不阻塞AI生成流程
- [ ] 并发评价不卡顿

### 用户体验
- [ ] 评分卡片设计简洁美观
- [ ] 可折叠/展开,不干扰编辑器
- [ ] "重新生成"功能带上评价反馈,质量提升明显

---

## 🤔 关键决策点

### 决策1: 是否自动评价?

**方案A**: 每次AI生成后自动评价 (推荐❌)
- ✅ 用户无需手动触发
- ❌ Token消耗翻倍
- ❌ 可能打断创作流程

**方案B**: 用户主动点击"评价"按钮 (推荐✅)
- ✅ 节省成本
- ✅ 用户可控
- ❌ 需要多一步操作

**建议**: 采用方案B,但提供"自动评价"开关(用户偏好设置)

### 决策2: 即时评价 vs 对话模式,先做哪个?

**建议**:
1. **Day 1-2**: 先做即时评价模式(MVP,快速验证)
2. **Day 3**: 根据时间决定是否做对话模式
3. **理由**: 即时评价是80%用户需要的功能,对话模式是高级用户需求

### 决策3: 使用 LangChain 还是纯原生?

**即时评价模式**: 纯原生(不需要Memory)
**对话模式**: LangChain Memory(管理历史对话)

**依赖最小化**: 只在需要时引入 LangChain

---

## 📝 下一步行动

请确认以下问题,我立即开始实施:

1. **优先级确认**: 是否先做"即时评价模式"?(推荐✅)
2. **Day 3安排**: 时间充裕做对话模式,否则做测试优化?(建议测试优化)
3. **自动评价**: 默认关闭,用户可选开启?(推荐✅)
4. **UI风格**: 卡片式 vs 侧边栏? (建议卡片式,不遮挡编辑器)

确认后我立即开始编写代码! 🚀
