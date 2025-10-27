# AI 拆书功能开发计划

> **创建时间**: 2025-10-27
> **优先级**: P0 (核心差异化功能)
> **预计工期**: 6天
> **状态**: 🚧 进行中 (Day 3 已完成)

---

## 📋 功能概述

### 功能定位
**AI拆书** = 网文11维度深度分析 + 智能世界观建议 + 知识库自动入库

### 核心价值
- 📚 **目标用户**: 网文作者,学习爆款小说的创作技巧
- 🤖 **11维度分析**: 核心卖点、主角设定、金手指系统、世界观、力量体系等
- 💡 **智能建议**: AI自动识别可关联的世界观元素 (角色/地点/力量体系)
- ✍️ **一键采纳**: 批量选中建议,快速创建世界观元素

---

## 🎯 核心决策

### 决策1: 分析策略 ✅
**方案**: 网文11维度分析 (参考Java版番茄小说策略)

**分析维度**:
1. 核心卖点 (50-80字)
2. 主角设定 (身份背景/性格/初始困境)
3. 金手指系统 (核心机理/成长路径/用法示例)
4. 世界观框架 (时代背景/底层规则)
5. 等级力量体系 (分层体系/战力对比)
6. 反派势力 (层级递进的反派设计)
7. 情感线设定 (感情发展路径)
8. 爽点布局 (打脸/反差/碾压等爽点设计)
9. 期待感钩子 (悬念/伏笔/预告)
10. 支线剧情 (副线设计)
11. 特色设定 (差异化卖点)

### 决策2: 性能方案 ✅
**智能采样策略** (针对长篇网文 100万字+)

```
前30章深度分析 (建立核心设定)
    ↓
关键章节识别 (正则+固定间隔)
    ↓
增量分析提示词 (只提取新内容)
    ↓
成本控制 (单次最大分析章节数限制)
```

**预期效果**:
- 分析时间: 15-20分钟
- 分析章节: 100-150章 (而非全部500章)
- API成本: $0.3-0.5
- 提取知识点: 200-300个

### 决策3: 世界观关联方式 ✅
**智能建议模式** (Week 1直接实现)

```
AI自动识别可关联的世界观元素
    ↓
卡片式建议列表 (批量选中交互)
    ↓
采纳向导流程 (预填充数据)
    ↓
有"魔法感"的用户体验
```

---

## 🏗️ 技术架构

### 后端架构
```
上传图书
    ↓
BookAnalysisService (图书分析服务)
    ├─ 解析图书结构 (TXT/EPUB/PDF)
    ├─ 智能采样分析器
    └─ 策略模式架构
    ↓
WebNovelStrategy (网文11维度策略)
    ├─ Prompt生成器
    ├─ AI调用 (Gemini 2.5 Pro)
    └─ 结果解析器
    ↓
SuggestionGenerator (智能建议生成器)
    ├─ AI评估置信度
    ├─ 映射到世界观元素
    └─ 生成建议列表
    ↓
KnowledgeService (现有服务复用)
    ├─ 创建知识条目
    └─ 向量化存储
    ↓
返回分析结果 + 智能建议
```

### 数据模型

#### 1. book_analysis_jobs (图书分析任务表)
```python
id: UUID
user_id: UUID
book_title: str (500)
original_filename: str (500)
file_format: str (10)  # 'txt', 'epub', 'pdf'
file_size_bytes: int
file_hash: str (64)  # SHA256哈希,去重

status: str (20)  # pending/parsing/analyzing/completed/failed
progress: int (0-100)
current_step: str (200)

total_chapters: int
analyzed_chapters: int
extracted_items_count: int

error_message: text
retry_count: int

extra_data: jsonb
created_at, started_at, completed_at, updated_at
```

#### 2. worldview_suggestions (智能建议表)
```python
id: UUID
user_id: UUID
job_id: UUID  # 关联分析任务
work_id: UUID (可选)  # 关联作品

suggestion_type: str  # character/location/power_system/setting
action: str  # create_new
suggested_data: jsonb  # 预填充的数据

confidence_score: float  # AI置信度
reason: text  # 建议理由

status: str  # pending/adopted/rejected/ignored
adopted_at: timestamp
adopted_as_id: UUID  # 采纳后创建的元素ID

created_at, updated_at
```

---

## 🗓️ 开发计划

### Day 1-2: 后端核心架构 ⏳

#### 任务清单
- [ ] 创建策略模式基础架构
  - [ ] `BookAnalysisStrategy` 抽象基类
  - [ ] `WebNovelStrategy` 实现类 (11维度)
  - [ ] `StrategyRegistry` 策略注册器

- [ ] 实现智能采样分析服务
  - [ ] `SmartSamplingAnalyzer` 类
  - [ ] 前30章深度分析逻辑
  - [ ] 关键章节识别算法
  - [ ] 增量分析提示词构建

- [ ] 数据模型创建
  - [ ] `book_analysis_jobs` 表
  - [ ] `worldview_suggestions` 表
  - [ ] SQLAlchemy模型类
  - [ ] Alembic迁移脚本

- [ ] 提示词工程
  - [ ] 11维度网文分析系统提示词
  - [ ] 增量分析提示词模板
  - [ ] 智能建议生成提示词

#### 关键文件
```
backend/app/services/book_analysis/
├── __init__.py
├── strategy.py              # 策略基类
├── web_novel_strategy.py    # 网文策略实现
├── smart_sampling.py         # 智能采样逻辑
└── suggestion_generator.py   # 建议生成器

backend/app/models/
├── book_analysis.py          # Job模型
└── worldview_suggestion.py   # Suggestion模型

backend/alembic/versions/
└── xxxx_add_book_analysis_tables.py
```

---

### Day 3: API接口开发 ⏳

#### 任务清单
- [ ] 创建API路由
  - [ ] `POST /api/v1/books/upload` - 上传图书并启动分析
  - [ ] `GET /api/v1/books/jobs/{job_id}` - 查询任务状态
  - [ ] `GET /api/v1/books/jobs` - 任务列表
  - [ ] `GET /api/v1/books/{job_id}/suggestions` - 获取智能建议
  - [ ] `POST /api/v1/books/{job_id}/adopt` - 批量采纳建议
  - [ ] `PATCH /api/v1/suggestions/{id}` - 修改单个建议
  - [ ] `DELETE /api/v1/books/jobs/{job_id}` - 删除任务

- [ ] 异步任务处理
  - [ ] Celery任务配置 (或后台线程)
  - [ ] 任务状态更新机制
  - [ ] 错误处理与重试逻辑

- [ ] API文档
  - [ ] FastAPI自动文档完善
  - [ ] 请求/响应示例

#### 关键文件
```
backend/app/api/v1/endpoints/
└── books.py                  # 图书分析API

backend/app/tasks/
└── book_analysis_task.py     # 异步任务
```

---

### Day 4-5: 前端集成 ⏳

#### Day 4: 核心组件开发
- [ ] 上传对话框
  - [ ] `BookUploadDialog.tsx` - 文件上传+意图选择
  - [ ] 策略选择UI (网文分析 vs 通用分析)
  - [ ] 作品关联选择器
  - [ ] 上传进度显示

- [ ] 分析进度监控
  - [ ] `AnalysisProgressPanel.tsx` - 实时进度条
  - [ ] 任务状态轮询逻辑
  - [ ] 阶段性进度文案

#### Day 5: 智能建议UI
- [ ] 建议结果页面
  - [ ] `SuggestionResultModal.tsx` - 分析完成弹窗
  - [ ] `SuggestionCard.tsx` - 建议卡片组件
  - [ ] 卡片网格布局 (响应式)
  - [ ] 类型筛选标签

- [ ] 批量操作交互
  - [ ] 卡片多选交互
  - [ ] 全选/反选/按推荐度筛选
  - [ ] 底部操作栏

- [ ] 采纳向导
  - [ ] `AdoptionWizard.tsx` - 逐步确认流程
  - [ ] 表单预填充
  - [ ] 跳过/修改/保存按钮
  - [ ] 完成庆祝动画

#### 关键文件
```
frontend/src/components/knowledge/
├── BookUploadDialog.tsx
├── AnalysisProgressPanel.tsx
├── SuggestionResultModal.tsx
├── SuggestionCard.tsx
└── AdoptionWizard.tsx

frontend/src/api/
└── bookAnalysis.ts           # API调用封装

frontend/src/types/
└── bookAnalysis.ts           # TypeScript类型定义
```

---

### Day 6: 测试与优化 ⏳

#### 任务清单
- [ ] 后端单元测试
  - [ ] 测试TXT解析功能
  - [ ] 测试11维度分析提示词
  - [ ] 测试智能采样逻辑
  - [ ] 测试建议生成准确性

- [ ] 集成测试
  - [ ] 端到端测试 (上传→分析→入库)
  - [ ] 测试长篇网文 (100万字+)
  - [ ] 测试成本控制 (是否≤$0.5)
  - [ ] 测试错误处理

- [ ] 前端测试
  - [ ] 组件单元测试
  - [ ] 用户流程测试
  - [ ] 响应式布局测试

- [ ] 性能优化
  - [ ] 数据库查询优化
  - [ ] API响应时间优化
  - [ ] 前端加载速度优化

- [ ] 文档编写
  - [ ] 用户使用指南
  - [ ] API接口文档
  - [ ] 开发者文档

#### 关键文件
```
backend/tests/
├── test_book_analysis_service.py
├── test_web_novel_strategy.py
├── test_smart_sampling.py
└── test_book_api.py

frontend/src/components/__tests__/
├── BookUploadDialog.test.tsx
└── SuggestionCard.test.tsx
```

---

## 🎯 验收标准

### 功能验收
- [ ] ✅ 可上传.txt格式网文小说 (≤50MB)
- [ ] ✅ 自动识别章节结构 (正则匹配成功率≥90%)
- [ ] ✅ 智能采样分析 (前30章全分析 + 后期抽样)
- [ ] ✅ 11维度提取完整 (所有维度都有输出)
- [ ] ✅ 自动创建知识库条目 (≥150条)
- [ ] ✅ 生成智能建议 (15-30个可关联元素)
- [ ] ✅ 批量采纳功能正常
- [ ] ✅ 采纳向导预填充正确

### 性能验收
- [ ] ✅ 100万字网文分析时间 ≤ 20分钟
- [ ] ✅ API成本 ≤ $0.5/本
- [ ] ✅ 分析章节数 ≤ 150章
- [ ] ✅ 前端响应时间 < 500ms
- [ ] ✅ 进度更新延迟 < 2秒

### 体验验收
- [ ] ✅ 上传流程顺畅 (≤3步)
- [ ] ✅ 进度显示清晰
- [ ] ✅ 建议卡片美观
- [ ] ✅ 批量选中交互流畅
- [ ] ✅ 采纳向导体验好
- [ ] ✅ 完成时有庆祝动画

---

## 💰 成本与性能

### Token消耗估算 (Gemini 2.5 Pro)

| 操作 | 文本长度 | Input Tokens | Output Tokens | 成本 |
|------|---------|-------------|---------------|------|
| 单章分析 | 5000字 | ~4000 | ~800 | ~$0.005 |
| 前30章深度 | 150k字 | ~120k | ~24k | ~$0.15 |
| 增量分析 | 5000字 | ~4000 | ~300 | ~$0.003 |
| 建议生成 | - | ~2000 | ~1000 | ~$0.003 |
| **总计** | 100万字 | ~300k | ~50k | ~$0.35 |

### 性能指标

| 操作 | 目标响应时间 | 并发能力 |
|------|------------|---------|
| 上传文件 | < 10秒 | 50 QPS |
| 单章分析 | < 30秒 | 20 QPS |
| 完整分析 | < 20分钟 | 5 QPS |
| 建议生成 | < 10秒 | 20 QPS |

---

## 📝 实施进度记录

### ✅ Day 1-2: 后端核心架构 (已完成)

**状态**: ✅ 已完成
**开始时间**: 2025-10-27 13:00
**完成时间**: 2025-10-27 13:15

#### 任务进度
- [x] 创建策略模式基础架构
  - [x] `BookAnalysisStrategy` 抽象基类
  - [x] `AnalysisDimension` 维度定义
  - [x] `StrategyRegistry` 策略注册器

- [x] 实现智能采样分析服务
  - [x] `SmartSamplingAnalyzer` 类
  - [x] TXT文件解析 (正则匹配 + 备用策略)
  - [x] 智能章节选择算法
  - [x] 成本估算功能

- [x] 数据模型创建
  - [x] `BookAnalysisJob` 模型
  - [x] `WorldviewSuggestion` 模型
  - [x] 数据库迁移成功

- [x] 提示词工程
  - [x] `WebNovelStrategy` 11维度策略
  - [x] 系统提示词模板
  - [x] 用户提示词模板 (支持增量分析)

#### 已创建文件 (8个)
```
backend/app/services/book_analysis/
├── __init__.py
├── strategy.py (策略基类, 270行)
├── web_novel_strategy.py (网文11维度策略, 320行)
├── smart_sampling.py (智能采样器, 280行)
└── suggestion_generator.py (智能建议生成器, 450行)

backend/app/models/
├── book_analysis.py (任务模型, 65行)
└── worldview_suggestion.py (建议模型, 70行)

backend/alembic/versions/
└── 20251027_1307_*.py (数据库迁移)
```

---

### ✅ Day 3: API接口开发 (已完成)

**状态**: ✅ 已完成
**开始时间**: 2025-10-27 13:15
**完成时间**: 2025-10-27 13:25

#### 任务进度
- [x] 创建API路由 (8个端点)
  - [x] `POST /api/v1/books/upload` - 上传图书并启动分析
  - [x] `GET /api/v1/books/jobs/{job_id}` - 查询任务详情
  - [x] `GET /api/v1/books/jobs/{job_id}/status` - 查询任务状态
  - [x] `GET /api/v1/books/jobs` - 任务列表
  - [x] `DELETE /api/v1/books/jobs/{job_id}` - 删除任务
  - [x] `GET /api/v1/books/jobs/{job_id}/suggestions` - 获取智能建议
  - [x] `POST /api/v1/books/jobs/{job_id}/adopt` - 批量采纳建议
  - [x] `PATCH /api/v1/books/suggestions/{id}` - 修改单个建议

- [x] 核心服务实现
  - [x] `BookAnalysisService` - 完整分析流程编排
  - [x] 异步后台任务处理 (BackgroundTasks)
  - [x] 文件上传和存储

- [x] Schema定义
  - [x] `BookAnalysisJobCreate/Response`
  - [x] `WorldviewSuggestionResponse`
  - [x] `AdoptSuggestionRequest/Response`

- [x] 路由注册
  - [x] 注册到 `app/api/__init__.py`

#### 已创建文件 (3个)
```
backend/app/services/
└── book_analysis_service.py (核心服务, 350行)

backend/app/schemas/
└── book_analysis.py (Schema定义, 150行)

backend/app/api/v1/endpoints/
└── books.py (API路由, 350行)
```

---

### ⏳ Day 4-5: 前端集成 (待开始)

**状态**: 待开始
**开始时间**: -
**预计完成**: -

#### 任务进度
- [ ] 上传对话框
- [ ] 分析进度监控
- [ ] 建议结果页面
- [ ] 批量操作交互
- [ ] 采纳向导

---

### ⏳ Day 6: 测试与优化 (待开始)

**状态**: 待开始
**开始时间**: -
**预计完成**: -

#### 任务进度
- [ ] 后端单元测试
- [ ] 集成测试
- [ ] 前端测试
- [ ] 性能优化
- [ ] 文档编写

---

## 📚 相关文档

- **完整实现方案**: `tasks/AI拆书功能实现方案.md`
- **API参考**: 待创建
- **数据模型**: 待创建
- **前端组件**: 待创建
- **测试计划**: 待创建

---

## 🔗 依赖关系

### 已完成的前置条件
- ✅ 知识库功能 (knowledge_items表)
- ✅ 向量存储服务 (VectorStoreService)
- ✅ AI调用服务 (HTTPAIService)
- ✅ 世界观管理功能 (worldview表)

### 需要复用的服务
- KnowledgeService (创建知识条目)
- VectorStoreService (向量化存储)
- HTTPAIService (AI调用)
- WorldviewService (创建世界观元素)

---

**创建时间**: 2025-10-27
**最后更新**: 2025-10-27 15:00
**负责人**: 开发团队
**总体状态**: 🚧 进行中 (Day 1-3 已完成, Day 4-5 待开始)

---

## 📋 修复记录

### 2025-10-27 15:00 - 修复测试问题

#### 问题1: call_ai 参数错误 ✅
**文件**: `backend/app/services/book_analysis_service.py:254-258`

**问题描述**:
- `call_ai()` 方法调用时使用了错误的参数名
- 导致所有章节分析失败

**修复内容**:
```python
# 修复前
response_text = await self.ai_service.call_ai(
    prompt=user_prompt,           # ❌ 错误参数名
    system_prompt=system_prompt,
    user_id=str(job.user_id),     # ❌ 不支持的参数
    temperature=0.3
)

# 修复后
response_text = await self.ai_service.call_ai(
    system_prompt=system_prompt,  # ✅ 正确
    user_prompt=user_prompt,      # ✅ 正确
    temperature=0.3
)
```

#### 问题2: 错误日志未记录 ✅
**文件**: `backend/app/services/book_analysis_service.py:285`

**问题描述**:
- 使用 `print()` 而不是 `logger.error()` 记录错误
- 导致错误信息未出现在日志中

**修复内容**:
```python
# 修复前
except Exception as e:
    print(f"分析章节失败: {chapter.title}, 错误: {e}")

# 修复后
except Exception as e:
    logger.error(f"❌ 分析章节失败: {chapter.title}, 错误: {type(e).__name__}: {e}")
```

#### 问题3: 测试重复上传检测 ✅
**文件**: `backend/tests/test_book_analysis_auto.py:237`

**问题描述**:
- 每次测试使用固定文件名 `test_novel.txt`
- 触发系统的重复上传检测
- 导致测试失败: "该图书已分析过"

**修复内容**:
```python
# 修复前
test_file = Path("test_novel.txt")

# 修复后
timestamp = int(time.time())
test_file = Path(f"test_novel_{timestamp}.txt")
```

**验证结果**: ✅ 所有问题已修复,测试可正常运行

