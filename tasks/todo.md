# 小说评审增强功能 - 完整实施计划

> **创建时间**: 2025-10-26
> **优先级**: P0 (差异化核心功能)
> **预计工期**: 4周
> **状态**: 📋 规划完成，待实施

---

## 📋 目录

- [功能概述](#功能概述)
- [核心决策](#核心决策)
- [技术架构](#技术架构)
- [实施路线](#实施路线)
- [数据模型设计](#数据模型设计)
- [API接口设计](#api接口设计)
- [前端UI设计](#前端ui设计)
- [成本与性能](#成本与性能)

---

## 📖 功能概述

### 功能定位

小说评审增强 = **多粒度评审** + **智能任务清单** + **版本追踪** 的完整评审系统

### 核心价值

| 功能模块 | 用户价值 | 差异化优势 |
|---------|---------|-----------|
| **多粒度评审** | 从段落→章节→作品全方位评价 | 市场少见的完整评审体系 |
| **智能任务清单** | AI自动生成改稿任务，精确定位问题 | 可操作性强，提升修改效率 |
| **版本管理** | 追踪每次修改，展示进步曲线 | 激励用户持续优化 |
| **进度追踪** | 任务完成率、评分提升趋势 | 游戏化体验，增强粘性 |

---

## ✅ 核心决策

### 决策1: 评审粒度 ⭐⭐⭐⭐⭐

**方案**: ✅ **分阶段实施，三个粒度都做**

```
MVP (Week 1-2):     章节级评审 (最实用) ⭐⭐⭐⭐⭐
Phase 2 (Week 3):   段落级评审 (提升体验) ⭐⭐⭐⭐
Phase 3 (Week 4):   作品级评审 (差异化) ⭐⭐⭐⭐⭐
```

**创新功能**: 智能粒度推荐
```python
def recommend_review_level(context):
    if user_selected_text and len(text) < 500:
        return "paragraph"  # 段落级

    if chapter_just_finished and word_count > 2000:
        return "chapter"    # 章节级

    if work_status == "completed" and total_chapters > 10:
        return "work"       # 作品级
```

**成本控制**: 按Token消耗计费，成本透明

| 粒度 | 文本长度 | Token估算 | 成本 | 使用频率 |
|------|---------|----------|------|---------|
| 段落级 | 100-500字 | ~800 | $0.01 | 高 |
| 章节级 | 3000-8000字 | ~4500 | $0.05-0.15 | 中 |
| 作品级 | 50k-200k字 | ~60000 | $2-5 | 低 |

---

### 决策2: 评审维度

**方案**: ✅ **分级维度体系**

#### 段落级评审 (4维度)
```
1. 语言质量 (文字流畅度/修辞手法)
2. 描写生动度 (画面感/代入感)
3. 对话真实性 (符合人物性格)
4. 情感表达 (感染力/共鸣度)
```

#### 章节级评审 (8维度) ⭐ MVP重点
```
1. 文学性 (语言质量/修辞手法)
2. 情节合理性 (逻辑/因果关系)
3. 人物塑造 (行为/对话一致性)
4. 节奏把控 (快慢/张弛有度)
5. 场景描写 (画面感/细节)
6. 情感感染力 (共鸣度/情绪调动)
7. 伏笔铺垫 (悬念设置/回收)
8. 创意新颖度 (打破常规/想象力)
```

#### 作品级评审 (10维度)
```
1. 大纲结构 (三幕/五幕结构完整性)
2. 主题表达 (中心思想/价值观深度)
3. 人物弧光 (主角/配角成长轨迹)
4. 情节节奏 (高潮分布/起承转合)
5. 世界观一致性 (设定逻辑/内部统一)
6. 伏笔回收率 (埋伏笔→挖伏笔完成度)
7. 对白质量 (个性化/推动情节)
8. 文笔风格统一性 (前后风格一致)
9. 商业潜力 (类型定位/市场接受度)
10. 创新度 (同类作品对比/差异化)
```

---

### 决策3: 任务清单系统

**方案**: ✅ **AI自动生成 + 用户手动添加 (混合模式)**

#### 任务来源
```
AI自动生成 (主要来源 80%)
    ↓
根据评审结果智能生成 5-10 个任务
    ↓
用户可以:
    ├─ 修改任务 (标题/描述/优先级)
    ├─ 删除任务 (不相关的)
    ├─ 添加任务 (AI未发现的问题) (20%)
    └─ 调整顺序 (拖拽排序)
```

#### 任务属性
```python
class ReviewTask:
    # 基本信息
    title: str              # "优化第3段的人物动机描写"
    description: str        # 详细说明 + 修改建议

    # 定位信息 (精确到段落)
    location: {
        paragraph_index: int,   # 段落序号
        start_pos: int,        # 字符起始位置
        end_pos: int,          # 字符结束位置
        text_snippet: str      # 原文片段 (50字)
    }

    # 任务属性
    priority: str           # P0/P1/P2 三级优先级
    category: str          # character/plot/pacing/language...
    status: str            # pending/in_progress/completed/skipped

    # AI元数据
    related_score: str     # 关联的评审维度
    current_score: int     # 该维度当前分数
    estimated_time: int    # 预估修改时间(分钟)
    tags: List[str]        # ["人物动机", "内心独白"]

    # 依赖关系
    depends_on: List[UUID]  # 必须先完成的任务
    blocks: List[UUID]      # 完成后才能做的任务
```

#### 优先级系统 (P0/P1/P2)
```python
智能优先级分配算法:

    评分影响 (40%):
        - 评分 < 60分 → +40分
        - 评分 60-75 → +25分
        - 评分 > 75  → +10分

    问题类型 (30%):
        - 核心问题 (plot/character) → +30分
        - 其他问题 → +15分

    影响范围 (20%):
        - 跨章节问题 → +20分
        - 单章节问题 → +10分

    修改难度 (10%):
        - 容易修改 (<30分钟) → +10分
        - 困难修改 → +5分

    总分映射:
        >= 70分 → P0 (紧急)
        >= 50分 → P1 (重要)
        < 50分  → P2 (优化)
```

#### 批量操作 ✅ 全功能支持
```
MVP必做:
  ✅ 批量完成
  ✅ 批量跳过
  ✅ 拖拽排序

增强功能:
  ✅ 批量删除 (带二次确认)
  ✅ 批量修改优先级

优化功能:
  🟢 快捷键支持 (Ctrl+A全选, Delete删除)
  🟢 批量修改分类
```

---

### 决策4: 版本管理系统

**方案**: ✅ **混合模式 (完整快照 + 生命周期管理)**

#### 核心策略
```
新版本 (7天内):      完整快照  → 秒级访问
近期版本 (30天内):   完整快照  → 快速访问
中期版本 (90天内):   diff压缩  → 可接受延迟
长期版本 (90天后):   对象存储  → 低成本归档
里程碑版本:          完整快照  → 永久保留 ⭐
```

#### 版本类型
```python
class VersionType(str, Enum):
    SNAPSHOT = "snapshot"      # 完整快照
    COMPRESSED = "compressed"  # diff压缩
    ARCHIVED = "archived"      # 对象存储归档
```

#### 存储优化
```
示例: 10个版本

版本1 (基线):  完整存储 5000字 → 10KB
版本2-4:      完整快照 (30天内) → 30KB
版本5 (基线):  完整存储 5100字 → 10KB
版本6-9:      diff补丁 (90天内) → 8KB
版本10 (里程碑): 完整存储 → 10KB

总存储: 68KB (相比完整快照100KB，节省32%)
```

#### 自动归档任务
```python
定期任务 (每天凌晨执行):

    1. 30天前普通版本 → 转为diff压缩
    2. 90天前版本 → 迁移到对象存储
    3. 里程碑版本 → 永不归档
```

---

## 🏗️ 技术架构

### 后端架构

```
评审请求
    ↓
API路由层
    ├─ /review/paragraph    (段落级)
    ├─ /review/chapter      (章节级)
    └─ /review/work         (作品级)
    ↓
ReviewService (评审编排服务)
    ├─ 获取文本内容
    ├─ 智能粒度判断
    ├─ 调用评审引擎
    └─ 生成任务清单
    ↓
EvaluationEngine (评审引擎)
    ├─ Prompt生成器
    ├─ HTTPAIService (AI调用)
    ├─ AILogMiddleware (日志记录)
    └─ 结果解析器
    ↓
TaskGenerator (任务生成器)
    ├─ 问题定位
    ├─ 优先级分配
    ├─ 依赖关系分析
    └─ 任务持久化
    ↓
VersionManager (版本管理)
    ├─ 创建版本快照
    ├─ 保存评审数据
    └─ 生命周期管理
    ↓
返回评审结果 + 任务清单
```

---

## 🗓️ 实施路线

### 📅 MVP: 章节级评审 (Week 1-2)

**目标**: 实现最核心的章节评审功能

#### Week 1: 后端实现

**Day 1-2: 数据模型设计** ✅
- [x] 创建 `review_sessions` 表 (评审会话)
- [x] 创建 `review_tasks` 表 (任务清单)
- [x] 创建 `chapter_versions` 表 (版本管理)
- [x] 创建 Pydantic Schema
- [x] 数据库迁移

**Day 3-4: 核心服务实现** ✅
- [x] `NovelReviewService` - 章节评审服务
- [x] `TaskGeneratorService` - 任务生成服务
- [x] `VersionManagerService` - 版本管理服务
- [x] Prompt模板库 (8维度评审)

**Day 5: API路由实现** ✅
- [x] `POST /review/chapters/{id}` - 发起评审
- [x] `GET /review/sessions/{id}` - 获取评审结果
- [x] `GET /chapters/{id}/tasks` - 获取任务清单
- [x] `POST /tasks` - 创建任务 (手动)
- [x] `PATCH /tasks/{id}/status` - 更新任务状态
- [x] `POST /tasks/batch-operations` - 批量操作
- [x] `GET /chapters/{id}/versions` - 版本列表
- [x] 其他辅助接口 (删除任务、任务统计、版本对比等)

#### Week 2: 前端实现

**Day 1-2: 类型定义 + 服务层**
- [ ] `types/review.ts` - 评审相关类型
- [ ] `types/task.ts` - 任务类型
- [ ] `types/version.ts` - 版本类型
- [ ] `services/ReviewService.ts` - 评审服务
- [ ] `services/TaskService.ts` - 任务服务
- [ ] `hooks/useChapterReview.ts` - 评审Hook
- [ ] `hooks/useTaskList.ts` - 任务清单Hook

**Day 3-4: UI组件开发**
- [ ] `ReviewPanel.tsx` - 评审面板
- [ ] `ReviewResultCard.tsx` - 评审结果卡片
- [ ] `DimensionScoreChart.tsx` - 维度评分图表
- [ ] `TaskList.tsx` - 任务清单列表
- [ ] `TaskCard.tsx` - 任务卡片 (可拖拽)
- [ ] `BatchActionsBar.tsx` - 批量操作栏
- [ ] `AddTaskDialog.tsx` - 添加任务对话框
- [ ] `VersionTimeline.tsx` - 版本时间轴

**Day 5: 集成与测试**
- [ ] 集成到 `EditorView`
- [ ] 端到端测试
- [ ] UI/UX优化
- [ ] 性能测试

---

### 📅 Phase 2: 段落级评审 (Week 3)

**目标**: 提升即时反馈体验

**Day 1-2: 后端实现**
- [ ] `ParagraphReviewService` - 段落评审服务
- [ ] Prompt模板 (4维度评审)
- [ ] `POST /review/paragraphs` - 段落评审接口

**Day 3-4: 前端实现**
- [ ] `ParagraphReviewButton.tsx` - 段落评审按钮
- [ ] `QuickReviewPopover.tsx` - 快速评审弹窗
- [ ] 集成到编辑器气泡菜单

**Day 5: 测试优化**
- [ ] 功能测试
- [ ] 性能优化 (减少API调用)

---

### 📅 Phase 3: 作品级评审 (Week 4)

**目标**: 差异化竞争优势

**Day 1-2: 后端实现**
- [ ] `WorkReviewService` - 作品评审服务
- [ ] Prompt模板 (10维度评审)
- [ ] 大纲分析算法
- [ ] 人物弧光追踪
- [ ] 世界观一致性检查 (联动worldview数据)
- [ ] `POST /review/works/{id}` - 作品评审接口

**Day 3-4: 前端实现**
- [ ] `WorkReviewPanel.tsx` - 作品评审面板
- [ ] `OutlineStructureView.tsx` - 大纲结构视图
- [ ] `CharacterArcChart.tsx` - 人物弧光图表
- [ ] `PacingCurve.tsx` - 节奏曲线图
- [ ] `CommercialPotentialReport.tsx` - 商业潜力报告

**Day 5: 测试与发布**
- [ ] 完整测试
- [ ] 成本分析
- [ ] 文档更新
- [ ] 发布上线

---

### 📅 Phase 4: 增强功能 (Week 5+)

**可选优化功能**:
- [ ] 版本对比 (文本diff可视化)
- [ ] 进步报告生成
- [ ] 评分趋势分析
- [ ] 任务依赖关系可视化
- [ ] 快捷键支持
- [ ] 自动归档定时任务
- [ ] 导出评审报告 (PDF/Markdown)

---

## 📊 数据模型设计

### 1. 评审会话表

```sql
CREATE TABLE review_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id),

    -- 评审对象
    review_level VARCHAR(20) NOT NULL,  -- paragraph/chapter/work
    target_id UUID NOT NULL,            -- 段落ID/章节ID/作品ID

    -- 评审结果
    overall_score FLOAT,                -- 总分 (0-100)
    dimension_scores JSONB,             -- 各维度评分
    highlights JSONB,                   -- 优点列表
    issues JSONB,                       -- 问题列表
    suggestions JSONB,                  -- 改进建议

    -- 元数据
    word_count INTEGER,
    review_type VARCHAR(20),            -- quick/standard/deep
    ai_model VARCHAR(50),
    ai_call_log_id UUID,                -- 关联AI日志

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_review_sessions_user ON review_sessions(user_id, created_at DESC);
CREATE INDEX idx_review_sessions_target ON review_sessions(review_level, target_id);
```

### 2. 任务清单表

```sql
CREATE TABLE review_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- 关联关系
    review_session_id UUID REFERENCES review_sessions(id),
    chapter_id UUID NOT NULL REFERENCES chapters(id),
    user_id UUID NOT NULL REFERENCES users(id),

    -- 任务基本信息
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    source VARCHAR(20) DEFAULT 'ai',    -- ai/manual

    -- 定位信息 (精确到段落)
    location JSONB,                     -- {paragraph_index, start_pos, end_pos, text_snippet}

    -- 任务属性
    priority VARCHAR(10) DEFAULT 'P1',  -- P0/P1/P2
    category VARCHAR(50),               -- character/plot/pacing...
    status VARCHAR(20) DEFAULT 'pending', -- pending/in_progress/completed/skipped

    -- AI生成的元数据
    related_score VARCHAR(50),          -- 关联的评审维度
    current_score INTEGER,              -- 该维度当前分数
    estimated_time INTEGER,             -- 预估分钟数
    tags JSONB,                         -- ["人物动机", "内心独白"]

    -- 依赖关系
    depends_on JSONB,                   -- [task_id1, task_id2]
    blocks JSONB,                       -- [task_id3, task_id4]

    -- 用户操作
    user_notes TEXT,
    completed_at TIMESTAMP,
    skipped_reason VARCHAR(200),

    -- 排序
    sort_order INTEGER DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_chapter ON review_tasks(chapter_id, status);
CREATE INDEX idx_tasks_user ON review_tasks(user_id, created_at DESC);
CREATE INDEX idx_tasks_priority ON review_tasks(priority, status);
```

### 3. 版本管理表

```sql
CREATE TABLE chapter_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID NOT NULL REFERENCES chapters(id),
    user_id UUID NOT NULL REFERENCES users(id),

    -- 版本信息
    version_number INTEGER NOT NULL,
    version_type VARCHAR(20) DEFAULT 'snapshot',  -- snapshot/compressed/archived
    is_milestone BOOLEAN DEFAULT FALSE,           -- 里程碑版本
    version_tag VARCHAR(50),                      -- "初稿", "评审后v1"
    change_summary TEXT,                          -- 本次修改说明

    -- 内容存储 (根据version_type决定使用哪个字段)
    content TEXT,                                 -- 完整内容 (snapshot)
    diff_patch TEXT,                              -- diff补丁 (compressed)
    storage_location VARCHAR(200),                -- 对象存储URL (archived)

    -- 评审数据
    review_session_id UUID REFERENCES review_sessions(id),
    overall_score FLOAT,
    dimension_scores JSONB,

    -- 任务数据
    completed_tasks_count INTEGER DEFAULT 0,
    task_completion_rate FLOAT,

    -- 统计数据
    word_count INTEGER,

    created_at TIMESTAMP DEFAULT NOW(),
    archived_at TIMESTAMP
);

-- 索引
CREATE INDEX idx_versions_chapter ON chapter_versions(chapter_id, version_number DESC);
CREATE INDEX idx_versions_milestone ON chapter_versions(chapter_id, is_milestone) WHERE is_milestone = TRUE;
CREATE INDEX idx_versions_to_archive ON chapter_versions(version_type, created_at)
    WHERE version_type = 'snapshot' AND is_milestone = FALSE;
```

---

## 🔌 API接口设计

### 评审接口

```typescript
// 章节评审
POST /api/v1/review/chapters/{chapter_id}
Request: {
  review_type: 'quick' | 'standard' | 'deep',  // 评审深度
  auto_generate_tasks: boolean,                // 是否自动生成任务
  create_version: boolean                      // 是否创建版本快照
}
Response: {
  session_id: string,
  overall_score: number,
  dimension_scores: {
    literary_quality: number,
    plot_logic: number,
    character: number,
    pacing: number,
    scene: number,
    emotion: number,
    foreshadowing: number,
    creativity: number
  },
  highlights: string[],
  issues: string[],
  suggestions: string[],
  generated_tasks: Task[]  // 自动生成的任务
}

// 段落评审
POST /api/v1/review/paragraphs
Request: {
  text: string,
  context: {
    chapter_id: string,
    previous_text?: string
  }
}

// 作品评审
POST /api/v1/review/works/{work_id}
Request: {
  review_type: 'standard' | 'commercial'
}
```

### 任务管理接口

```typescript
// 获取任务清单
GET /api/v1/chapters/{chapter_id}/tasks
Query: {
  status?: 'pending' | 'in_progress' | 'completed' | 'skipped',
  priority?: 'P0' | 'P1' | 'P2',
  category?: string,
  sort_by?: 'smart' | 'priority' | 'location' | 'time'
}

// 创建任务 (手动)
POST /api/v1/tasks
Request: {
  chapter_id: string,
  title: string,
  description: string,
  priority: 'P0' | 'P1' | 'P2',
  category: string,
  location?: {
    paragraph_index: number,
    start_pos: number,
    end_pos: number
  }
}

// 更新任务状态
PATCH /api/v1/tasks/{task_id}/status
Request: {
  status: 'pending' | 'in_progress' | 'completed' | 'skipped',
  notes?: string,
  skipped_reason?: string
}

// 批量操作
POST /api/v1/tasks/batch-operations
Request: {
  action: 'complete' | 'skip' | 'delete' | 'update_priority' | 'reorder',
  task_ids: string[],
  notes?: string,
  reason?: string,
  new_priority?: string,
  task_orders?: Array<{task_id: string, sort_order: number}>
}

// 任务统计
GET /api/v1/tasks/stats
Query: {
  chapter_id?: string
}
Response: {
  total: number,
  by_status: {pending: 10, in_progress: 3, completed: 5},
  by_priority: {P0: 2, P1: 8, P2: 8},
  estimated_total_time: 180,  // 分钟
  completion_rate: 0.28
}
```

### 版本管理接口

```typescript
// 创建版本
POST /api/v1/chapters/{chapter_id}/versions
Request: {
  is_milestone: boolean,
  version_tag?: string,
  change_summary?: string
}

// 版本列表
GET /api/v1/chapters/{chapter_id}/versions
Response: {
  versions: Array<{
    id: string,
    version_number: number,
    version_type: string,
    is_milestone: boolean,
    overall_score: number,
    word_count: number,
    created_at: string
  }>
}

// 版本详情
GET /api/v1/versions/{version_id}
Response: {
  id: string,
  content: string,  // 完整内容 (可能需要重建)
  overall_score: number,
  dimension_scores: {...},
  completed_tasks_count: number,
  change_summary: string
}

// 版本对比
GET /api/v1/versions/compare
Query: {
  version1_id: string,
  version2_id: string
}
Response: {
  score_diff: {
    overall: {old: 75, new: 82, change: +7},
    dimensions: {...}
  },
  text_diff: {
    added: number,
    deleted: number,
    modified: number,
    diff_html: string  // HTML格式的diff
  },
  completed_tasks: Task[]
}

// 标记里程碑
PATCH /api/v1/versions/{version_id}/milestone
Request: {
  is_milestone: boolean,
  version_tag?: string
}
```

---

## 🎨 前端UI设计

### 1. 评审面板组件

```tsx
// src/components/review/ReviewPanel.tsx

<ReviewPanel chapterId={chapterId}>
  {/* 顶部操作栏 */}
  <ReviewActions>
    <Button onClick={startReview}>
      🔍 开始评审
    </Button>
    <Select value={reviewType}>
      <option value="quick">快速评审</option>
      <option value="standard">标准评审</option>
      <option value="deep">深度评审</option>
    </Select>
  </ReviewActions>

  {/* 评审结果 */}
  {reviewResult && (
    <ReviewResult>
      {/* 总分 */}
      <OverallScore score={82} />

      {/* 8维度雷达图 */}
      <DimensionRadarChart scores={dimensionScores} />

      {/* 优点/问题/建议 */}
      <ReviewDetails
        highlights={highlights}
        issues={issues}
        suggestions={suggestions}
      />

      {/* 自动生成的任务清单 */}
      <GeneratedTasks tasks={generatedTasks} />
    </ReviewResult>
  )}
</ReviewPanel>
```

### 2. 任务清单组件

```tsx
// src/components/review/TaskList.tsx

<TaskList chapterId={chapterId}>
  {/* 批量操作栏 */}
  {selectedTasks.size > 0 && (
    <BatchActionsBar
      selectedCount={selectedTasks.size}
      onComplete={batchComplete}
      onSkip={batchSkip}
      onDelete={batchDelete}
      onChangePriority={batchChangePriority}
    />
  )}

  {/* 筛选和排序 */}
  <TaskFilters
    status={statusFilter}
    priority={priorityFilter}
    sortBy={sortBy}
  />

  {/* 任务统计 */}
  <TaskStats
    total={18}
    completed={5}
    inProgress={3}
    pending={10}
  />

  {/* 任务分组 (拖拽排序) */}
  <DndContext onDragEnd={handleDragEnd}>
    <TaskGroup priority="P0" tasks={p0Tasks} />
    <TaskGroup priority="P1" tasks={p1Tasks} />
    <TaskGroup priority="P2" tasks={p2Tasks} />
  </DndContext>

  {/* 添加任务按钮 */}
  <Button onClick={openAddDialog}>
    ➕ 手动添加任务
  </Button>
</TaskList>
```

### 3. 任务卡片组件

```tsx
// src/components/review/TaskCard.tsx

<TaskCard task={task}>
  {/* 拖拽手柄 */}
  <DragHandle />

  {/* 多选框 */}
  <Checkbox checked={selected} />

  {/* 优先级标签 */}
  <PriorityBadge priority="P0" />

  {/* 任务内容 */}
  <div className="task-content">
    <h4>{task.title}</h4>
    <p>{task.description}</p>
  </div>

  {/* 定位信息 */}
  <LocationTag
    paragraph={3}
    onClick={scrollToLocation}
  />

  {/* 元数据 */}
  <div className="meta">
    <CategoryBadge category="character" />
    <TimeEstimate minutes={10} />
    <Tags tags={["人物动机", "内心独白"]} />
  </div>

  {/* 操作按钮 */}
  <TaskActions>
    <Button onClick={startTask}>开始修改</Button>
    <Button onClick={completeTask}>✅ 完成</Button>
    <Button onClick={skipTask}>跳过</Button>
  </TaskActions>
</TaskCard>
```

### 4. 版本时间轴组件

```tsx
// src/components/review/VersionTimeline.tsx

<VersionTimeline chapterId={chapterId}>
  {versions.map(version => (
    <VersionNode
      key={version.id}
      version={version}
      isMilestone={version.is_milestone}
    >
      {/* 版本号 */}
      <VersionBadge>
        {version.is_milestone && '⭐'} v{version.version_number}
      </VersionBadge>

      {/* 评分 + 趋势 */}
      <ScoreDisplay
        score={version.overall_score}
        trend={version.score_change}
      />

      {/* 日期 */}
      <Date>{formatDate(version.created_at)}</Date>

      {/* 修改说明 */}
      <ChangeSummary>{version.change_summary}</ChangeSummary>

      {/* 操作 */}
      <VersionActions>
        <Button onClick={viewVersion}>查看</Button>
        <Button onClick={compareVersion}>对比</Button>
        <Button onClick={markMilestone}>标记里程碑</Button>
      </VersionActions>
    </VersionNode>
  ))}
</VersionTimeline>
```

---

## 💰 成本与性能

### Token消耗估算

| 操作 | 文本长度 | Prompt Tokens | Completion Tokens | 成本 (GPT-4) |
|------|---------|--------------|-------------------|-------------|
| 段落评审 | 300字 | ~800 | ~300 | ~$0.01 |
| 章节评审 | 5000字 | ~4000 | ~800 | ~$0.05 |
| 作品评审 | 100k字 | ~50000 | ~5000 | ~$2.00 |
| 任务生成 | - | ~1000 | ~500 | ~$0.015 |

### 性能指标

| 操作 | 目标响应时间 | 并发能力 |
|------|------------|---------|
| 段落评审 | < 5秒 | 100 QPS |
| 章节评审 | < 30秒 | 50 QPS |
| 作品评审 | < 10分钟 | 10 QPS |
| 任务CRUD | < 500ms | 200 QPS |

### 优化策略

1. **缓存机制**
   - 相同内容评审结果缓存1小时
   - 减少重复AI调用

2. **异步处理**
   - 作品级评审使用后台任务
   - WebSocket推送进度

3. **分批处理**
   - 大型作品分章节评审
   - 结果聚合展示

4. **成本控制**
   - 用户配额限制
   - 高级功能付费

---

## 📚 相关文档

- **API参考**: `docs/07-api-reference.md` (待更新)
- **数据模型**: `backend/app/models/` (待创建)
- **前端组件**: `src/components/review/` (待创建)
- **测试计划**: `tasks/review_test_plan.md` (待创建)

---

## 🎯 验收标准

### MVP验收 (Week 2结束)

**功能完整性**:
- [ ] 章节评审返回8维度评分
- [ ] AI自动生成5-10个任务
- [ ] 任务精确定位到段落
- [ ] 支持批量完成/跳过/删除
- [ ] 支持拖拽排序
- [ ] 版本快照自动创建
- [ ] 评分趋势图展示

**性能指标**:
- [ ] 章节评审响应 < 30秒
- [ ] 任务列表加载 < 500ms
- [ ] 批量操作响应 < 1秒

**用户体验**:
- [ ] 评审结果清晰易懂
- [ ] 任务描述具体可操作
- [ ] 拖拽交互流畅
- [ ] 无明显Bug

---

## 📝 开发注意事项

### 代码规范

1. **命名规范**
   - 服务类: `NovelReviewService`, `TaskGeneratorService`
   - 模型类: `ReviewSession`, `ReviewTask`, `ChapterVersion`
   - API路由: `/api/v1/review/chapters/{id}`

2. **错误处理**
   - AI调用失败: 返回默认评分 + 错误提示
   - 任务生成失败: 记录日志,不影响评审结果
   - 版本创建失败: 不影响主流程

3. **日志记录**
   - 所有AI调用记录到 `ai_call_logs`
   - 关键操作记录到应用日志
   - 错误信息详细记录

4. **测试覆盖**
   - 单元测试: 核心服务和算法
   - 集成测试: API接口
   - E2E测试: 完整评审流程

---

## 📝 实施进度记录

### ✅ Week 1 后端实现 - 已完成 (2025-10-26)

**完成时间**: 2025-10-26
**开发耗时**: ~4小时
**状态**: ✅ 全部完成

#### 已完成内容

**1. 数据模型层** (3个表)
- ✅ `app/models/review_session.py` - 评审会话模型 (ReviewSession, ReviewLevel, ReviewType)
- ✅ `app/models/review_task.py` - 任务清单模型 (ReviewTask, TaskPriority, TaskStatus, TaskSource)
- ✅ `app/models/chapter_version.py` - 版本管理模型 (ChapterVersion, VersionType)
- ✅ 数据库迁移成功执行

**2. Schema层** (1个文件, 20+ 类型)
- ✅ `app/schemas/review.py` - 完整的请求/响应 Schema
  - 评审会话相关: ReviewSessionCreate, ReviewSessionResponse, DimensionScores
  - 任务管理相关: ReviewTaskCreate, ReviewTaskUpdate, ReviewTaskResponse, BatchOperationRequest, TaskStatsResponse
  - 版本管理相关: ChapterVersionCreate, ChapterVersionResponse, VersionCompareResponse

**3. Prompt 模板库**
- ✅ `app/prompts/review_prompts.py` - 评审提示词模板
  - 章节级评审 Prompt (8维度)
  - 段落级评审 Prompt (4维度)
  - 作品级评审 Prompt (10维度)
  - 任务生成 Prompt

**4. 核心服务层** (3个服务)
- ✅ `app/services/review/novel_review_service.py` - NovelReviewService
  - 章节评审功能
  - AI 调用集成
  - 评审历史查询

- ✅ `app/services/review/task_generator_service.py` - TaskGeneratorService
  - AI 自动生成任务
  - 手动创建任务
  - 任务 CRUD 操作
  - 批量操作 (完成/跳过/删除/调整优先级)
  - 任务统计

- ✅ `app/services/review/version_manager_service.py` - VersionManagerService
  - 创建版本快照
  - 版本列表查询
  - 里程碑标记
  - 版本对比
  - 归档功能框架

**5. API 路由层** (15个接口)
- ✅ `app/api/v1/review.py` - 评审相关 API

  **评审接口**:
  - POST `/review/chapters/{id}/review` - 发起章节评审
  - GET `/review/sessions/{id}` - 获取评审结果
  - GET `/review/chapters/{id}/review-history` - 评审历史

  **任务管理接口**:
  - GET `/review/chapters/{id}/tasks` - 获取任务清单
  - POST `/review/tasks` - 创建任务
  - PATCH `/review/tasks/{id}` - 更新任务
  - PATCH `/review/tasks/{id}/status` - 更新任务状态
  - DELETE `/review/tasks/{id}` - 删除任务
  - POST `/review/tasks/batch-operations` - 批量操作
  - GET `/review/tasks/stats` - 任务统计

  **版本管理接口**:
  - POST `/review/chapters/{id}/versions` - 创建版本
  - GET `/review/chapters/{id}/versions` - 版本列表
  - GET `/review/versions/{id}` - 版本详情
  - PATCH `/review/versions/{id}/milestone` - 标记里程碑
  - GET `/review/versions/compare` - 版本对比

#### 技术亮点

1. **完整的评审系统**: 8维度章节评审 + 智能任务生成 + 版本追踪
2. **AI 集成**: 使用 Gemini 2.5 Pro,成本降低 90%
3. **灵活的任务管理**: 支持 AI 生成 + 手动创建,P0/P1/P2 优先级系统
4. **版本管理**: 混合存储策略 (快照 + diff压缩 + 对象存储)
5. **批量操作**: 支持批量完成/跳过/删除/调整优先级

#### 文件清单 (13个新文件)

**模型层** (3个):
- `app/models/review_session.py`
- `app/models/review_task.py`
- `app/models/chapter_version.py`

**Schema层** (1个):
- `app/schemas/review.py`

**服务层** (5个):
- `app/prompts/review_prompts.py`
- `app/prompts/__init__.py`
- `app/services/review/novel_review_service.py`
- `app/services/review/task_generator_service.py`
- `app/services/review/version_manager_service.py`
- `app/services/review/__init__.py`

**API层** (1个):
- `app/api/v1/review.py`

**数据库迁移** (1个):
- `alembic/versions/20251026_1618_09d7c95bb8ab_add_review_sessions_tasks_and_chapter_.py`

**配置更新** (1个):
- `app/api/__init__.py` (注册新路由)

---

### 🐛 Bug 修复记录 (2025-10-26 下午)

**问题**: 章节评审返回 500 错误 - JSONDecodeError

**原因分析**:
1. Gemini API 返回 JSON 包裹在 markdown 代码块中 (` ```json\n{...}\n``` `)
2. Gemini API 第一个流式块的 `content` 为 `null`
3. NovelReviewService 和 TaskGeneratorService 使用 `json.loads()` 无法解析

**已修复内容**:

**1. 强化 Prompt 模板** ✅
- 文件: `app/prompts/review_prompts.py`
- 添加明确指示: "**重要**: 你必须且只能返回纯 JSON 格式"

**2. 添加智能 JSON 提取函数** ✅
- 文件: `app/services/review/novel_review_service.py:29-86`
- 新增 `extract_json_from_response()` 函数
- 支持 3 种格式: 纯 JSON、markdown 包裹、前后有额外文本

**3. 修复 HTTPAIService** ✅
- 文件: `app/services/ai/http_ai_service.py:126`
- 添加 `content is not None` 检查，避免 None 类型错误

**4. 修复 NovelReviewService** ✅
- 文件: `app/services/review/novel_review_service.py:221`
- 使用智能提取函数替代 `json.loads()`

**5. 修复 TaskGeneratorService** ✅
- 文件: `app/services/review/task_generator_service.py:29`
- 导入 `extract_json_from_response` 函数
- 文件: `app/services/review/task_generator_service.py:371`
- 使用智能提取函数替代 `json.loads()`

**6. 编写测试脚本** ✅
- 创建 `tests/test_review_simple.py` - 完整的自动化测试
- 创建 `tests/test_ai_direct.py` - 直接测试 AI API

**测试结果**:
```
✅ 登录: PASS
✅ 准备数据: PASS
✅ 章节评审: PASS (修复前 FAIL)
✅ 任务管理: PASS
✅ 版本管理: PASS

成功率: 100% (5/5)
```

**性能数据**:
- 章节评审: ~30秒, 1784字符, 15数据块
- 任务生成: ~32秒, 3818字符, 66数据块
- 生成任务数: 7个

**修复耗时**: ~30分钟

---

#### 下一步计划

✅ **Week 1 后端已全部完成 + Bug 修复完成**

⏭️ **Week 2: 前端实现** (待开始)
- 类型定义 + 服务层
- UI组件开发
- 集成与测试

---

**创建时间**: 2025-10-26
**最后更新**: 2025-10-26 17:30
**负责人**: 开发团队
**Week 1 状态**: ✅ 已完成并测试通过

---

## 🚀 Git 提交任务

### 待办事项
- [x] 暂存所有更改的文件
- [x] 创建提交记录
- [x] 推送到远程仓库

### 审查

#### 第一次提交: Week 1 评审功能后端实现
- **提交哈希**: ef1c00c
- **分支**: alin2
- **提交时间**: 2025-10-26
- **文件统计**: 22个文件, 新增4572行, 删除65行

**提交内容**:
- 新增15个文件 (模型、服务、API、文档)
- 修改7个文件 (路由注册、Bug修复)
- 完成8维度章节评审系统
- AI智能任务生成器和版本管理

#### 第二次提交: 清理临时文件
- **提交哈希**: 4e5721a
- **分支**: alin2
- **提交时间**: 2025-10-26
- **文件统计**: 19个文件, 新增338行, 删除3211行

**删除清单**:
- 🔴 安全文件: TEST_ACCOUNT_CONFIG.md (包含明文密码)
- 📝 临时测试脚本: 5个 (quick_test*.py, run_tests.py等)
- 📄 临时文档: 11个 (DOCS_UPDATE*.md, TEST*.md等)
- ✅ 新增: CLEANUP_ANALYSIS.md (清理分析报告)

**清理效果**:
- 删除代码: 3,211行
- 保留核心测试: 6个文件
- 保留核心文档: backend/docs 15个, docs 22个
- 项目结构更清晰,安全性提升

#### 远程推送
✅ 两次提交均成功推送到 GitHub: alin776/ai_writer (alin2分支)

#### 下一步
可以开始 Week 2 前端实现工作
