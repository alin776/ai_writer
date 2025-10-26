# AI 交互式反馈系统 - 实施计划

> **创建时间**: 2025-10-26
> **优先级**: P0 (差异化核心功能)
> **预计工期**: 3天
> **状态**: 🔧 进行中

---

## 📋 项目概述

### 功能定位
AI交互式反馈系统 = **即时评价** + **持续对话**的双模式系统

| 功能模块 | 触发时机 | 主要价值 | 实施优先级 |
|---------|---------|---------|-----------|
| **即时评价模式** | AI生成后 | 5维度评分+优缺点+建议 | P0 (Day 1-2) |
| **持续对话模式** | 用户主动创建 | 多轮创作指导 | P1 (Day 3) |

---

## ✅ 核心决策 (已确认)

### 决策1: AI日志集成
**方案**: ✅ **完全集成到 ai_call_logs**

```python
# 每次评价都记录到AI日志系统
await ai_log_service.create_log(
    user_id=user_id,
    operation_type="evaluate",  # 新增操作类型
    model=model,
    prompt_tokens=prompt_tokens,
    completion_tokens=completion_tokens,
    total_cost=cost
)
```

**行动项**:
- [ ] 扩展 `operation_type` 枚举: 添加 `evaluate` 和 `feedback_chat`
- [ ] 确保评价调用自动记录到 ai_call_logs 表

---

### 决策2: 架构模式
**方案**: ✅ **分离架构**

```python
# 即时评价 - 无状态API (不创建session)
POST /api/v1/ai/evaluate
→ 直接返回评价结果
→ 不写入会话表

# 对话模式 - 有状态会话
POST /api/v1/feedback/sessions
POST /api/v1/feedback/sessions/{id}/chat
→ 创建会话并保存历史消息
```

**优点**:
- 即时评价更轻量,不污染会话表
- 两种模式职责清晰

---

### 决策3: 数据持久化
**方案**: ✅ **轻量级持久化**

```python
# 新增表: evaluation_records (评价记录)
class EvaluationRecord(Base):
    __tablename__ = "evaluation_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    operation_type = Column(String(50))  # complete/polish/expand/translate/summarize
    overall_score = Column(Float)  # 总分
    dimensions = Column(JSON)  # 5维度评分 {"literary": 85, "coherence": 80, ...}
    created_at = Column(DateTime, default=datetime.utcnow)

    # 不保存全文,只保存评分和元数据
```

**目的**:
- 支持未来的数据分析(生成质量趋势)
- 管理后台可展示"平均生成质量"
- 个性化Prompt优化基础

---

### 决策4: LangChain依赖
**方案**: ✅ **现在安装**

```bash
cd backend
pip install langchain-core==0.3.0
pip freeze > requirements.txt
```

**原因**: Day 1-3 都要做,包括对话模式

---

### 决策5: Prompt设计
**方案**: ✅ **统一Prompt (MVP)**

```python
# 所有类型(续写/润色/扩写/翻译/总结)都用同一套评价
EVALUATION_PROMPT = """
评价以下AI生成内容的质量(5个维度):
1. 文学性 (语言质量、修辞手法)
2. 连贯性 (上下文衔接、逻辑流畅)
3. 创意性 (新颖度、想象力)
4. 情感感染力 (情感表达、共鸣度)
5. 节奏把控 (快慢适度、张弛有度)

返回JSON格式评价结果...
"""
```

**后续优化**: 按类型定制Prompt (Phase 2)

---

### 决策6: API路由位置
**方案**: ✅ **加到现有 ai.py**

```python
# backend/app/api/v1/ai.py (扩展现有文件)
@router.post("/ai/evaluate")
async def evaluate_generated_content(...):
    """评价AI生成内容 - 即时评价模式"""
```

**原因**: 评价是AI功能的延伸,复用现有依赖注入

---

## 🚀 Day 1: 即时评价模式 - 后端实现

### 任务清单

#### 1.1 数据库设计
- [x] 创建 `evaluation_records` 表模型
  - **文件**: `backend/app/models/evaluation_record.py` ✅
  - **字段**: user_id, operation_type, overall_score, dimensions, created_at
- [x] 扩展 `ai_call_logs` 的 operation_type 枚举
  - **文件**: `backend/app/models/ai_call_log.py` ✅
  - **新增**: `evaluate` 类型 (支持任意字符串)
- [x] 创建数据库迁移
  - **状态**: 迁移脚本已生成 ✅
  - **注意**: 表已存在,需执行 `alembic stamp head`

#### 1.2 Pydantic Schema
- [x] 创建评价请求/响应模型
  - **文件**: `backend/app/schemas/evaluation.py` ✅
  - **内容**:
    - `EvaluationRequest` - 评价请求 ✅
    - `EvaluationResponse` - 评价结果(含5维度评分) ✅
    - `DimensionScores` - 维度评分模型 ✅
    - `EvaluationContext` - 上下文信息 ✅

#### 1.3 Prompt模板
- [x] 创建评价Prompt模板库
  - **文件**: `backend/app/services/ai/evaluation_prompts.py` ✅
  - **内容**:
    - `EVALUATION_PROMPT_TEMPLATE` - 统一评价Prompt ✅
    - `EVALUATION_SYSTEM_PROMPT` - 系统Prompt ✅
    - `get_evaluation_prompt()` - 动态生成Prompt ✅
    - `format_context_info()` - 上下文格式化 ✅

#### 1.4 核心服务
- [x] 实现 `EvaluationService`
  - **文件**: `backend/app/services/ai/evaluation_service.py` ✅
  - **方法**:
    - `evaluate_text()` - 评价文本(返回结构化JSON) ✅
    - `_parse_evaluation_result()` - 解析AI返回的JSON ✅
    - `_save_evaluation_record()` - 保存评价记录 ✅
    - `_get_context()` - 获取上下文信息 ✅
    - `_call_ai_non_stream()` - 非流式AI调用 ✅
  - **集成**:
    - 调用 `HTTPAIService` 生成评价 ✅
    - 使用 `AILogMiddleware` 记录Token消耗 ✅
    - 保存到 `evaluation_records` 表 ✅

#### 1.5 API路由
- [x] 扩展 `ai.py` 添加评价接口
  - **文件**: `backend/app/api/v1/ai.py` ✅
  - **接口**: `POST /api/v1/ai/evaluate` ✅
  - **功能**:
    - 接收评价请求 ✅
    - 调用 EvaluationService ✅
    - 返回评价结果 ✅
    - 错误处理 ✅
  - **修复**: 导入语句移到文件顶部 ✅

#### 1.6 代码质量检查
- [x] Python语法检查 ✅
  - evaluation_record.py ✅
  - evaluation.py (schema) ✅
  - evaluation_prompts.py ✅
  - evaluation_service.py ✅
  - ai.py (router) ✅
- [x] 虚拟环境导入测试 ✅
  - Model 导入成功 ✅
  - Schema 导入成功 ✅
  - Service 导入成功 ✅
  - API Router 导入成功 ✅

---

## 🚀 Day 2: 即时评价模式 - 前端实现

### 任务清单

#### 2.1 类型定义
- [ ] 创建评价类型定义
  - **文件**: `src/types/evaluation.ts`
  - **内容**:
    - `EvaluationRequest` 接口
    - `EvaluationResponse` 接口
    - `DimensionScores` 接口

#### 2.2 扩展AIService
- [ ] 添加评价方法
  - **文件**: `src/services/AIService.ts`
  - **方法**:
    ```typescript
    async evaluateText(request: EvaluationRequest): Promise<EvaluationResponse>
    ```

#### 2.3 自定义Hook
- [ ] 创建 `useAIEvaluation` Hook
  - **文件**: `src/hooks/useAIEvaluation.ts`
  - **功能**:
    - 调用评价API
    - 管理加载状态
    - 错误处理

#### 2.4 UI组件
- [ ] 创建 `AIEvaluationCard` 评分卡片
  - **文件**: `src/components/editor/AIEvaluationCard.tsx`
  - **功能**:
    - 显示总分(0-100)
    - 5维度进度条
    - 可折叠/展开(优点/缺点/建议)
    - "接受"/"重新生成"按钮

#### 2.5 集成到编辑器
- [ ] 修改AI菜单,添加"评价"功能
  - **文件**: `src/components/editor/AIMenu.tsx`
  - **改动**:
    - AI生成完成后显示"查看评价"按钮
    - 点击后调用评价API
    - 显示 `AIEvaluationCard` 组件
- [ ] 实现"重新生成"功能
  - 带上评价反馈到Prompt
  - 提示AI改进低分维度

#### 2.6 测试与优化
- [ ] 端到端测试
  - 续写 → 评价 → 查看详情
  - 润色 → 评价 → 重新生成
- [ ] UI/UX优化
  - 评分卡片样式美化
  - 动画效果(评分进度条)
- [ ] 性能测试
  - 评价API响应时间 < 3秒

---

## 🚀 Day 3: 持续对话模式 - 完整实现

### 任务清单

#### 3.1 数据库设计
- [ ] 创建会话表模型
  - **文件**: `backend/app/models/feedback_session.py`
  - **表1**: `feedback_sessions` (会话信息)
  - **表2**: `feedback_messages` (对话消息)
- [ ] 创建数据库迁移
  ```bash
  alembic revision --autogenerate -m "add_feedback_session_tables"
  alembic upgrade head
  ```

#### 3.2 Pydantic Schema
- [ ] 创建对话Schema
  - **文件**: `backend/app/schemas/feedback.py`
  - **内容**:
    - `FeedbackSessionCreate` - 创建会话
    - `FeedbackMessageCreate` - 发送消息
    - `FeedbackSessionResponse` - 会话信息
    - `FeedbackMessageResponse` - 消息信息

#### 3.3 Prompt模板
- [ ] 创建对话Prompt模板
  - **文件**: `backend/app/services/ai/feedback_prompts.py`
  - **内容**:
    - 5种专家模式Prompt (general/plot/character/conflict/pacing)
    - 上下文注入模板

#### 3.4 核心服务
- [ ] 实现 `FeedbackService`
  - **文件**: `backend/app/services/ai/feedback_service.py`
  - **方法**:
    - `_get_memory()` - 获取会话Memory (带TTL缓存)
    - `_load_memory_from_db()` - 从数据库恢复历史
    - `_load_smart_context()` - 智能加载上下文
    - `_get_system_prompt()` - 获取专家Prompt
    - `chat_stream()` - 流式对话
  - **集成**:
    - LangChain Memory 管理历史
    - 自动加载作品世界观

#### 3.5 API路由
- [ ] 创建对话API
  - **文件**: `backend/app/api/v1/feedback.py` (新建)
  - **接口**:
    - `POST /feedback/sessions` - 创建会话
    - `GET /feedback/sessions` - 会话列表
    - `GET /feedback/sessions/{id}` - 会话详情
    - `POST /feedback/sessions/{id}/chat` - 发送消息(流式)
    - `DELETE /feedback/sessions/{id}` - 删除会话
- [ ] 注册路由
  - **文件**: `backend/app/api/v1/__init__.py`
  - **改动**: `router.include_router(feedback.router, tags=["AI Feedback"])`

#### 3.6 前端实现
- [ ] 创建对话UI组件
  - **文件**: `src/components/editor/AIFeedbackPanel.tsx`
  - **功能**:
    - 会话列表
    - 创建会话(选择模式)
    - 对话界面(流式显示)
    - 历史消息展示
- [ ] 集成到编辑器侧边栏
  - 新增"AI导师"标签页
  - 可从评价卡片"进入对话模式"

#### 3.7 测试与优化
- [ ] 功能测试
  - 创建会话 → 多轮对话 → 上下文理解
  - Memory恢复 (刷新页面后继续对话)
- [ ] 性能优化
  - TTL缓存验证
  - 上下文加载优化

---

## 📊 技术细节

### 评价Prompt设计

```python
EVALUATION_PROMPT = """你是专业的AI文本评审专家。请对以下生成内容进行客观、严谨的评价。

生成内容:
{text}

上下文信息:
作品: {work_title}
章节: {chapter_title}
前文片段: {previous_text}

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
  "highlights": ["优点1", "优点2", "优点3"],
  "issues": ["问题1", "问题2"],
  "suggestions": ["建议1", "建议2"]
}}

评价要求:
- 客观中立,既要肯定优点也要指出不足
- 建议要具体可操作,不要泛泛而谈
- 结合上下文和作品风格评价
- 避免主观偏见,以读者视角评判
"""
```

### Memory管理优化

```python
from cachetools import TTLCache

class FeedbackService:
    def __init__(self):
        self.http_ai = HTTPAIService()
        # TTL缓存: 1小时后自动清理,最多1000个会话
        self._memories = TTLCache(maxsize=1000, ttl=3600)

    async def _load_memory_from_db(self, session_id: int, db: AsyncSession):
        """从数据库恢复最近20条消息到Memory"""
        if session_id in self._memories:
            return self._memories[session_id]

        # 查询最近20条消息
        messages = await db.execute(
            select(FeedbackMessage)
            .where(FeedbackMessage.session_id == session_id)
            .order_by(FeedbackMessage.created_at.desc())
            .limit(20)
        )

        # 恢复到Memory
        memory = ConversationBufferMemory(return_messages=True)
        for msg in reversed(messages.scalars().all()):
            if msg.role == "user":
                memory.chat_memory.add_user_message(msg.content)
            else:
                memory.chat_memory.add_ai_message(msg.content)

        self._memories[session_id] = memory
        return memory
```

---

## 📈 成本分析

### Token消耗估算

| 操作 | Prompt Tokens | Completion Tokens | 成本(GPT-4 Turbo) |
|------|--------------|-------------------|-------------------|
| 即时评价(500字) | ~1450 | ~500 | $0.02 |
| 对话(单轮) | ~3100 | ~800 | $0.04 |

### 成本优化策略

1. ✅ 智能触发: 用户主动请求,不自动评价
2. ✅ 缓存结果: 相同内容不重复评价
3. ✅ 上下文裁剪: 只加载必要的信息
4. 🔧 模型降级: 评价功能可用GPT-3.5-Turbo (便宜10倍)

---

## ✅ 验收标准

### 功能验收
- [ ] 即时评价返回5维度评分,合理准确
- [ ] 优点/缺点/建议具体可操作
- [ ] 对话模式支持多轮,上下文理解准确
- [ ] Memory正确恢复(刷新页面后继续对话)

### 性能验收
- [ ] 评价API响应时间 < 3秒
- [ ] 对话流式响应延迟 < 500ms
- [ ] TTL缓存正常工作,无内存泄漏

### 用户体验
- [ ] 评分卡片设计简洁美观
- [ ] 对话界面流畅,不卡顿
- [ ] "重新生成"功能带上评价反馈,质量提升明显

---

## 📝 依赖清单

### 后端新增依赖
```bash
langchain-core==0.3.0
cachetools==5.3.0  # TTL缓存
```

### 前端新增依赖
无 (复用现有依赖)

---

## 🚀 部署步骤

### 1. 安装依赖
```bash
cd backend
pip install langchain-core==0.3.0 cachetools==5.3.0
pip freeze > requirements.txt
```

### 2. 数据库迁移
```bash
cd backend
alembic upgrade head
```

### 3. 验证部署
```bash
# 测试评价接口
curl -X POST http://localhost:8000/api/v1/ai/evaluate \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"text": "测试文本", "context": {}}'
```

---

## ✅ Day 1 完成审查 (2025-10-26)

### 功能测试
- [x] 用户登录功能 ✅
- [x] 评价API调用 ✅
- [x] 5维度评分计算 ✅
- [x] 优点/问题/建议生成 ✅
- [x] 评价记录保存 ✅
- [x] AI日志记录 ✅
- [x] Token消耗统计 ✅

### 测试脚本
- [x] test_evaluation_api.py (完整测试) ✅
- [x] quick_test.py (快速测试) ✅
- [x] TEST_EVALUATION_GUIDE.md (测试文档) ✅

### 测试结果
```
测试账号: 2072855200@qq.com
测试时间: 2025-10-26
测试状态: ✅ 全部通过

示例评价结果:
- 总分: 82.0/100
- 文学性: 85.0
- 连贯性: 80.0
- 创意性: 75.0
- 情感感染力: 88.0
- 节奏把控: 82.0
```

### 文档更新
- [x] docs/14-ai-evaluation-summary.md (功能总结) ✅
- [x] docs/07-api-reference.md (API文档更新) ✅
- [x] tasks/todo.md (任务清单更新) ✅

### 数据库验证
```sql
-- 评价记录表
SELECT COUNT(*) FROM evaluation_records;  -- 已有记录

-- AI调用日志
SELECT COUNT(*) FROM ai_call_logs
WHERE operation_type = 'evaluate';  -- 已有记录
```

---

## 📋 后续优化 (Phase 2)

### 高优先级
- [ ] 按类型定制Prompt (续写/润色/翻译不同评价维度)
- [ ] 评价结果数据分析面板
- [ ] 个性化Prompt优化 (基于历史评分)

### 中优先级
- [ ] Redis存储Memory (替代内存缓存)
- [ ] 评价模型降级到GPT-3.5-Turbo
- [ ] 批量评价接口

### 低优先级
- [ ] 评价结果导出(PDF/Markdown)
- [ ] 多语言评价支持

---

**创建时间**: 2025-10-26
**最后更新**: 2025-10-26
**负责人**: 开发团队
**状态**: ✅ Day 1 后端实现已完成并测试通过
