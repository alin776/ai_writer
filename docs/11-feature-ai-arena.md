# AI写作竞技场 - 明星功能设计

> 📋 **文档**: 11-feature-ai-arena.md | **最后更新**: 2025-10-24
> **功能定位**: Milestone 2 P1级明星功能 ⭐⭐
> **开发优先级**: 高优先级，独立页面打造
> **预计工期**: 1周（5-7个工作日）

[← 返回文档导航](./README.md)

---

## 📋 功能概述

### 核心价值

当用户对AI生成的内容不满意时，**同时调用4-6个顶级AI模型**重新生成，用户可以对比选择最满意的版本。

### 解决的问题

- ❌ **单一模型不稳定**: AI生成质量波动大，用户不满意时无法快速尝试其他模型
- ❌ **手动切换低效**: 逐个切换模型测试耗时长，用户体验差
- ❌ **选择困难**: 不知道哪个模型更适合当前场景

### 带来的价值

- ✅ **差异化竞争优势**: 市场上少见的多模型并发对比功能
- ✅ **提高用户满意度**: 一次生成多个选项，总有满意的
- ✅ **展示技术实力**: 证明接入了多个顶级模型
- ✅ **营销价值**: 可作为核心卖点宣传："6个顶级AI同时为你改写"

---

## 🎨 UI设计方案

### 页面命名

```
✅ "AI写作竞技场" (AI Writing Arena) - 推荐
✅ "多模型创作台" (Multi-Model Studio)
✅ "智能改写对比" (Smart Rewrite Comparison)
```

### 路由设计

```
/ai-arena          # 主页面
/ai-arena/new      # 新建对比任务
/ai-arena/history  # 历史对比记录
```

### 战斗竞技场风格UI（推荐）

**主界面布局**:
```
┌─────────────────────────────────────────────────────────────┐
│  🏟️ AI 写作竞技场                    [历史记录] [设置]      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📝 输入你想改写的内容：                                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 夜色如墨，月光洒在窗台上，映照着桌上未完成的稿纸。    │  │
│  │ 他叹了口气，手指在键盘上犹豫不决...                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  🎯 选择对战模型：                                            │
│  [√] GPT-4         [√] Claude-3.5    [√] Gemini-Pro         │
│  [√] Qwen-Max      [√] 文心4.0       [ ] 智谱GLM-4          │
│                                                               │
│  ⚙️ 生成参数：                                                │
│  长度：[短(100字)] [中(300字)] [长(500字)]                    │
│  风格：[严肃] [幽默] [诗意] [简洁]                           │
│  温度：[保守 ◉────────────── 创意] 0.7                      │
│                                                               │
│          [🚀 开始对比生成] (预计消耗 0.5元)                   │
└─────────────────────────────────────────────────────────────┘
```

**生成结果展示**:
```
┌─────────────────────────────────────────────────────────────┐
│  ⚡ 生成中... 已完成 5/5                                      │
│                                                               │
│  ┌──────────────┬──────────────┬──────────────┐             │
│  │ 🥇 GPT-4     │ 🥈 Claude-3.5│ 🥉 Gemini    │             │
│  │ ✅ 1.2s      │ ✅ 0.9s      │ ✅ 1.5s      │             │
│  ├──────────────┼──────────────┼──────────────┤             │
│  │ 深夜时分，    │ 夜幕低垂，    │ 月色如霜，    │             │
│  │ 月华如水般   │ 皎洁的月光   │ 银光透过窗棂 │             │
│  │ 泼洒在窗台   │ 温柔地洒落   │ 洒在他的书桌 │             │
│  │ 上...        │ 窗台...      │ 上...        │             │
│  │              │              │              │             │
│  │ [312字]      │ [298字]      │ [305字]      │             │
│  │ [😊 9.2分]   │ [😊 9.0分]   │ [😊 8.8分]   │             │
│  │              │              │              │             │
│  │ [👁️ 展开]    │ [👁️ 展开]    │ [👁️ 展开]    │             │
│  │ [✓ 选择]     │ [✓ 选择]     │ [✓ 选择]     │             │
│  │ [💬 10人选]  │ [💬 8人选]   │ [💬 6人选]   │             │
│  └──────────────┴──────────────┴──────────────┘             │
│                                                               │
│  ┌──────────────┬──────────────┐                            │
│  │ 🏅 Qwen-Max  │ 🏅 文心4.0   │                            │
│  │ ✅ 1.1s      │ ✅ 1.3s      │                            │
│  │ [287字]      │ [295字]      │                            │
│  └──────────────┴──────────────┘                            │
│                                                               │
│  [📊 查看详细对比] [💾 保存对比记录] [🔁 重新生成]            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 技术实现方案

### 1. 数据模型设计

```typescript
// 对比任务
interface CompareTask {
  id: string;
  userId: string;
  originalText: string;        // 原始文本
  instruction?: string;         // 改写要求（可选）
  models: string[];             // 选择的模型列表
  parameters: {
    maxTokens: number;          // 生成长度
    temperature: number;        // 创意度 0-1
    style?: string;             // 风格标签
  };
  status: 'pending' | 'processing' | 'completed' | 'failed';
  createdAt: Date;
  completedAt?: Date;
}

// 对比结果
interface CompareResult {
  id: string;
  taskId: string;
  model: string;                // 模型名称
  status: 'pending' | 'generating' | 'completed' | 'failed';
  content: string;              // 生成内容
  metadata: {
    elapsedTime: number;        // 耗时（秒）
    tokens: number;             // Token数
    cost: number;               // 成本（元）
    qualityScore?: QualityScore;// AI质量评分
  };
  userRating?: number;          // 用户评分（1-5星）
  selectedAsWinner: boolean;    // 是否被选为最佳
  createdAt: Date;
}

// 智能质量评分
interface QualityScore {
  fluency: number;      // 流畅度 0-10
  coherence: number;    // 连贯性 0-10
  creativity: number;   // 创意度 0-10
  relevance: number;    // 相关性 0-10
  overall: number;      // 总分 0-10
}
```

### 2. 数据库设计

```sql
-- 对比任务表
CREATE TABLE compare_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    original_text TEXT NOT NULL,
    instruction TEXT,
    models JSONB NOT NULL,  -- ["gpt-4", "claude-3.5-sonnet"]
    parameters JSONB NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- 对比结果表
CREATE TABLE compare_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id UUID NOT NULL REFERENCES compare_tasks(id) ON DELETE CASCADE,
    model VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    content TEXT,
    elapsed_time FLOAT,
    tokens INTEGER,
    cost DECIMAL(10, 4),
    quality_score JSONB,  -- {fluency: 9.2, coherence: 9.0, ...}
    user_rating INTEGER CHECK (user_rating >= 1 AND user_rating <= 5),
    selected_as_winner BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_compare_tasks_user ON compare_tasks(user_id);
CREATE INDEX idx_compare_results_task ON compare_results(task_id);
```

### 3. 后端API设计

```python
# POST /api/v1/ai-arena/compare
# 创建对比任务并并发生成
@router.post("/compare")
async def create_compare_task(request: CompareRequest, current_user: User):
    """并发调用多个模型生成"""
    # 1. 创建任务记录
    task = await create_task(request, current_user.id)

    # 2. 并发调用多个模型
    tasks = [
        generate_with_model(model, request.original_text, request.parameters)
        for model in request.models
    ]

    # 3. 使用asyncio.gather并发执行
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # 4. 保存结果
    for model, result in zip(request.models, results):
        await save_result(task.id, model, result)

    # 5. 返回任务ID
    return {"task_id": task.id, "status": "processing"}

# GET /api/v1/ai-arena/compare/{task_id}
# 查询对比结果

# POST /api/v1/ai-arena/compare/{task_id}/select
# 用户选择最佳结果

# GET /api/v1/ai-arena/history
# 获取历史记录

# GET /api/v1/ai-arena/stats
# 获取统计数据
```

### 4. 前端组件结构

```
src/views/AIArena/
├── AIArenaView.tsx          # 主页面（路由：/ai-arena）
├── CompareInput.tsx         # 输入区组件
├── ModelSelector.tsx        # 模型选择器
├── ParametersPanel.tsx      # 参数配置面板
├── ResultsGrid.tsx          # 结果网格（卡片式）
├── ResultCard.tsx           # 单个结果卡片
├── QualityScoreDisplay.tsx  # 质量评分展示
├── HistoryList.tsx          # 历史记录列表
├── StatsPanel.tsx           # 统计面板
└── AIArena.css              # 样式文件
```

### 5. 核心逻辑实现

```typescript
// 前端：触发多模型对比
async function startComparison(input: CompareInput) {
  try {
    setLoading(true);

    // 调用后端API
    const response = await fetch('/api/v1/ai-arena/compare', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(input)
    });

    const { task_id } = await response.json();

    // 轮询获取结果（实时更新）
    const results = await pollResults(task_id);

    displayResults(results);

  } catch (error) {
    showError('生成失败，请重试');
  } finally {
    setLoading(false);
  }
}

// 轮询结果（支持流式更新）
async function pollResults(taskId: string) {
  const maxAttempts = 60; // 最多60秒
  let attempts = 0;

  while (attempts < maxAttempts) {
    const response = await fetch(`/api/v1/ai-arena/compare/${taskId}`);
    const data = await response.json();

    // 更新UI显示部分完成的结果
    updateResultsDisplay(data.results);

    // 检查是否全部完成
    const allCompleted = data.results.every(r =>
      r.status === 'completed' || r.status === 'failed'
    );

    if (allCompleted) {
      return data.results;
    }

    await sleep(1000);
    attempts++;
  }

  throw new Error('生成超时');
}
```

---

## 📊 功能模块清单

### MVP版本（1周）
- [ ] 基础UI布局（输入区 + 结果展示）
- [ ] 固定4个模型（GPT-4, Claude-3.5, Gemini-Pro, Qwen-Max）
- [ ] 并发生成功能
- [ ] 实时状态展示
- [ ] 用户选择最佳结果
- [ ] 数据库表创建
- [ ] 后端5个API接口

### 增强版（+1周）
- [ ] 自定义模型选择（用户可选择任意模型组合）
- [ ] 历史记录功能
- [ ] 简单统计（总对比次数、最常用模型）
- [ ] 智能质量评分（后端AI评分）
- [ ] 导出对比结果

### 完整版（+2周）
- [ ] 数据分析面板（模型胜率、用户偏好分析）
- [ ] 社交分享功能
- [ ] 对比结果评论
- [ ] 高级参数配置
- [ ] 批量对比功能

---

## 🎯 营销与宣传建议

### 产品文案
```
✨ 不满意AI的生成结果？
🚀 让6个顶级AI同时为你改写！
🏆 一键对比，选出最佳版本
💡 GPT-4 vs Claude vs Gemini，谁更懂你？
```

### 视频演示脚本（20秒）
```
00:00 - 用户在编辑器写作
00:05 - 对AI生成的内容不满意
00:08 - 点击"AI竞技场"按钮
00:10 - 选择4个模型，点击"开始对比"
00:12 - 震撼的4个结果同时生成
00:15 - 快速浏览对比，选择最佳
00:18 - 一键替换到编辑器
00:20 - 继续创作，完美！
```

### 社交媒体话题
```
#AI写作对决
#6个顶级AI谁更强
#我让GPT和Claude对决了
```

---

## 📈 预期效果

**用户价值**:
- 提高AI生成满意度 30%+
- 节省手动切换模型时间 80%
- 用户留存率提升 15%+

**产品价值**:
- 明星功能，可作为核心卖点
- 展示技术实力（多模型接入）
- 差异化竞争优势

**数据收集**:
- 模型偏好统计（哪个模型最受欢迎）
- 场景适配分析（不同场景适合哪个模型）
- 用户行为分析（平均对比次数、选择时长）

---

## 🔮 后续优化方向

### P0（高优先级）
- [ ] 性能优化（并发控制、缓存）
- [ ] 错误处理（模型调用失败、超时）
- [ ] 成本控制（用户每日对比次数限制）

### P1（中优先级）
- [ ] 智能推荐（根据历史数据推荐最佳模型）
- [ ] 对比模板（预设常用对比场景）
- [ ] 高级过滤（按字数、风格筛选结果）

### P2（低优先级）
- [ ] A/B测试（真正的盲测机制）
- [ ] 模型排行榜（社区投票）
- [ ] API开放（让第三方接入）

---

## 🔗 相关链接

- **任务清单**: [05-tasks.md](./05-tasks.md#p1-14-ai写作竞技场)
- **路线图**: [04-milestones.md](./04-milestones.md#milestone-2)
- **API文档**: [07-api-reference.md](./07-api-reference.md)
- **返回**: [文档导航](./README.md)

---

**最后更新**: 2025-10-24
**功能状态**: 📅 待开发（Milestone 2）
**维护者**: NovelAIde 团队

---

**祝开发顺利！如有问题，请随时联系团队成员。** 🚀
