# 后端待开发功能清单

> **分析日期**: 2025-10-26
> **当前后端完成度**: 95%
> **分析依据**: docs/04-milestones.md, tasks/todo.md, docs/03-current-status.md

---

## 📊 后端开发现状总览

### ✅ 已完成的后端功能 (95%)

**核心系统**:
1. ✅ 用户认证系统 (JWT + Token刷新)
2. ✅ 作品/章节管理 (CRUD + 拖拽排序)
3. ✅ AI服务 (续写/扩写/润色/总结/翻译)
4. ✅ 世界观管理 (角色/地点/设定/关系/时间线)
5. ✅ 小说分析 (微观/宏观分析 + 向量存储)
6. ✅ 导入导出 (JSON/Markdown)
7. ✅ 全局搜索 (5种类型)
8. ✅ 管理后台 (用户管理/统计)
9. ✅ AI日志系统 (调用记录 + 成本追踪)

**Milestone 2 AI增强功能**:
1. ✅ AI去痕迹功能 (100% 后端完成)
2. ✅ AI评估反馈系统 (100% 后端完成)
3. ✅ AI改写竞技场 (100% 后端完成)
4. ✅ **小说评审系统 Week 1** (100% 后端完成) ⭐⭐⭐

---

## 🎯 后端待开发功能 (按优先级)

### 🔥 优先级 P0: 评审系统深化 (推荐)

#### 1. Phase 2: 段落级评审 (预计2-3天)

**功能描述**:
- 用户选中编辑器中的段落(100-500字),快速获得4维度评审
- 比章节级评审更轻量,响应更快(<5秒)

**需要开发**:

**后端部分** (Day 1-2):
```python
# 1. 新增服务
backend/app/services/review/paragraph_review_service.py  # 段落评审服务 (~200行)

# 2. 新增Prompt模板
backend/app/prompts/review_prompts.py  # 添加段落级4维度Prompt (~100行)

# 3. 新增API接口
backend/app/api/v1/review.py  # 添加段落评审端点
```

**API设计**:
```python
POST /api/v1/review/paragraphs
Request: {
    "text": "段落文本内容",
    "context": {
        "chapter_id": "uuid",
        "previous_text": "上文片段",  # 可选,用于上下文理解
        "next_text": "下文片段"      # 可选
    }
}

Response: {
    "overall_score": 78,
    "dimensions": {
        "language_quality": 80,      # 语言质量
        "vividness": 75,             # 描写生动度
        "dialogue_authenticity": 82, # 对话真实性
        "emotional_expression": 76   # 情感表达
    },
    "highlights": ["...", "..."],
    "issues": ["...", "..."],
    "suggestions": ["...", "..."]
}
```

**评审维度** (4个):
1. 语言质量 - 文字流畅度、修辞手法
2. 描写生动度 - 画面感、代入感
3. 对话真实性 - 符合人物性格
4. 情感表达 - 感染力、共鸣度

**工作量估算**:
- ParagraphReviewService: 4小时
- Prompt模板设计: 2小时
- API接口开发: 2小时
- 测试验证: 2小时
- **总计**: 1-2天

---

#### 2. Phase 3: 作品级评审 (预计3-5天) ⭐⭐⭐

**功能描述**:
- 对整部小说(50k-200k字)进行深度评审
- 10维度专业评价,分析大纲结构、人物弧光、节奏曲线
- **差异化竞争优势** - 市场罕见的完整作品评审系统

**需要开发**:

**后端部分** (Day 1-3):
```python
# 1. 核心服务
backend/app/services/review/work_review_service.py  # 作品评审服务 (~500行)

# 2. 分析算法
backend/app/services/review/outline_analyzer.py     # 大纲分析 (~300行)
backend/app/services/review/character_arc_tracker.py # 人物弧光追踪 (~300行)
backend/app/services/review/pacing_analyzer.py      # 节奏分析 (~200行)
backend/app/services/review/worldview_checker.py    # 世界观一致性检查 (~200行)

# 3. Prompt模板
backend/app/prompts/review_prompts.py  # 添加作品级10维度Prompt (~200行)

# 4. API接口
backend/app/api/v1/review.py  # 添加作品评审端点
```

**API设计**:
```python
POST /api/v1/review/works/{work_id}
Request: {
    "review_type": "standard" | "commercial",  # 标准评审 or 商业分析
    "options": {
        "analyze_outline": true,      # 是否分析大纲
        "track_character_arc": true,  # 是否追踪人物弧光
        "check_worldview": true,      # 是否检查世界观一致性
        "analyze_pacing": true        # 是否分析节奏
    }
}

Response: {
    "overall_score": 82,
    "dimensions": {
        "outline_structure": 85,       # 大纲结构
        "theme_expression": 80,        # 主题表达
        "character_arc": 78,           # 人物弧光
        "pacing": 84,                  # 节奏把控
        "worldview_consistency": 88,   # 世界观一致性
        "foreshadowing_recovery": 75,  # 伏笔回收率
        "dialogue_quality": 82,        # 对白质量
        "style_consistency": 90,       # 文笔风格统一性
        "commercial_potential": 76,    # 商业潜力
        "innovation": 70               # 创新度
    },
    "outline_analysis": {              # 大纲分析
        "structure_type": "三幕式",
        "plot_points": [...],
        "climax_distribution": [...]
    },
    "character_arcs": [                # 人物弧光
        {
            "character_name": "主角A",
            "arc_type": "成长型",
            "key_turning_points": [...]
        }
    ],
    "pacing_curve": {                  # 节奏曲线
        "chapter_pacing": [...],       # 每章节奏评分
        "overall_rhythm": "张弛有度"
    },
    "worldview_issues": [...],         # 世界观问题
    "highlights": [...],
    "issues": [...],
    "suggestions": [...]
}
```

**评审维度** (10个):
1. **大纲结构** - 三幕/五幕结构完整性
2. **主题表达** - 中心思想/价值观深度
3. **人物弧光** - 主角/配角成长轨迹
4. **情节节奏** - 高潮分布/起承转合
5. **世界观一致性** - 设定逻辑/内部统一
6. **伏笔回收率** - 埋伏笔→挖伏笔完成度
7. **对白质量** - 个性化/推动情节
8. **文笔风格统一性** - 前后风格一致
9. **商业潜力** - 类型定位/市场接受度
10. **创新度** - 同类作品对比/差异化

**技术亮点**:
- ✅ **联动世界观数据**: 利用已有的worldview表检查一致性
- ✅ **利用小说分析**: 复用novel_analysis表的微观/宏观分析数据
- ✅ **智能分批处理**: 大作品分章节分析再聚合,避免超时
- ✅ **异步后台任务**: 使用Celery或后台任务处理,WebSocket推送进度

**工作量估算**:
- 大纲分析算法: 6小时
- 人物弧光追踪: 6小时
- 节奏分析: 4小时
- 世界观一致性检查: 4小时
- WorkReviewService: 8小时
- Prompt模板设计: 4小时
- API接口开发: 4小时
- 测试验证: 4小时
- **总计**: 3-5天

---

#### 3. Phase 4: 评审系统增强功能 (预计2-3天)

**可选优化功能**:

**1. 版本对比功能** (1天):
```python
# 新增服务
backend/app/services/review/version_comparator.py  # 版本对比服务

# API接口
GET /api/v1/review/versions/compare?version1_id=xxx&version2_id=xxx

# 功能:
- 文本diff可视化
- 评分变化趋势
- 任务完成情况对比
- 修改热点图
```

**2. 进步报告生成** (1天):
```python
# 新增服务
backend/app/services/review/progress_reporter.py  # 进步报告生成器

# API接口
GET /api/v1/review/chapters/{id}/progress-report

# 功能:
- 多版本评分趋势分析
- 优点/问题变化统计
- 任务完成率统计
- 改进建议汇总
```

**3. 自动归档定时任务** (0.5天):
```python
# 新增定时任务
backend/app/tasks/archive_old_versions.py  # 版本归档任务

# 功能:
- 30天前版本 → diff压缩
- 90天前版本 → 对象存储
- 里程碑版本 → 永不归档
```

**4. 导出评审报告** (1天):
```python
# 新增服务
backend/app/services/review/report_exporter.py  # 报告导出服务

# API接口
GET /api/v1/review/sessions/{id}/export?format=pdf|markdown

# 功能:
- PDF格式专业报告
- Markdown格式便于编辑
- 包含图表和统计数据
```

---

### 🟡 优先级 P1: 其他后端优化

#### 1. 管理后台增强 (1-2天)

**目前状态**: 60%完成,后端API已就绪,前端占位

**待开发后端功能**:
```python
# 1. AI模型动态配置
backend/app/api/v1/admin.py
- POST /api/v1/admin/ai-models  # 添加模型
- PUT /api/v1/admin/ai-models/{id}  # 更新模型配置
- DELETE /api/v1/admin/ai-models/{id}  # 删除模型
- PATCH /api/v1/admin/ai-models/{id}/status  # 启用/禁用

# 2. 成本预警系统
backend/app/services/cost_alerter.py
- 实时成本监控
- 超额预警通知
- 成本优化建议

# 3. 用户配额管理
backend/app/services/quota_manager.py
- 用户级别配额设置
- 配额消耗追踪
- 超额限流
```

---

#### 2. 性能优化 (1-2天)

**小说分析性能优化**:
```python
# 当前问题: 100章分析需要59分钟
# 优化目标: 降低到30分钟以内

# 优化方案:
1. 批量分析优化 (并发处理)
2. 缓存机制 (重复文本缓存结果)
3. 智能采样 (大作品采样分析)
4. 增量分析 (只分析新增/修改章节)

# 需要修改的文件:
backend/app/services/novel_analysis_service.py
backend/app/api/v1/novel_analysis.py
```

**AI调用优化**:
```python
# 优化点:
1. 连接池复用 (httpx AsyncClient池化)
2. 请求合并 (批量请求合并为一个)
3. 智能重试 (指数退避策略)
4. 超时控制 (分级超时设置)

# 需要修改的文件:
backend/app/services/ai/http_ai_service.py
```

---

#### 3. 容错增强 (1天)

**错误处理优化**:
```python
# 1. 全局异常处理器增强
backend/app/core/exception_handlers.py
- AI调用失败降级策略
- 数据库连接失败重试
- 第三方服务超时处理

# 2. 数据验证增强
backend/app/schemas/
- 更严格的输入验证
- 自动类型转换
- 友好的错误提示

# 3. 日志系统增强
backend/app/core/logging.py
- 结构化日志 (JSON格式)
- 日志分级存储
- 错误追踪链路
```

---

### 🟢 优先级 P2: 长期优化

#### 1. 缓存系统 (2天)

```python
# Redis缓存集成
backend/app/core/cache.py

# 缓存策略:
1. AI调用结果缓存 (1小时)
2. 小说分析结果缓存 (24小时)
3. 用户配置缓存 (永久,手动失效)
4. 评审结果缓存 (30天)

# 需要缓存的接口:
- /api/v1/ai/complete
- /api/v1/novel-analysis/analyze
- /api/v1/review/chapters/{id}
```

---

#### 2. 消息队列 (3天)

```python
# Celery异步任务集成
backend/app/tasks/

# 异步任务:
1. 作品级评审 (耗时10分钟+)
2. 大规模小说分析 (100章+)
3. 批量导出功能
4. 定时清理任务

# WebSocket推送进度
backend/app/api/v1/websocket.py
```

---

#### 3. 数据分析系统 (2-3天)

```python
# 新增数据分析模块
backend/app/services/analytics/

# 功能:
1. 用户行为分析 (使用习惯、高频功能)
2. AI模型效果分析 (满意度、质量评分)
3. 成本趋势分析 (成本预测、优化建议)
4. 内容质量分析 (评分分布、改进趋势)
```

---

## 📊 优先级推荐总结

### 🔥 立即可做 (本周)

1. **Phase 2: 段落级评审** (2-3天) ⭐⭐⭐⭐
   - 工作量小,价值高
   - 完善评审系统的完整性
   - 提升用户体验

### 🎯 短期目标 (下周)

2. **Phase 3: 作品级评审** (3-5天) ⭐⭐⭐⭐⭐
   - 差异化核心功能
   - 市场竞争优势
   - 技术难度高,展示实力

### 📅 中期规划 (2周内)

3. **Phase 4: 增强功能** (2-3天)
   - 版本对比
   - 进步报告
   - 报告导出

4. **管理后台增强** (1-2天)
   - AI模型管理
   - 成本预警
   - 配额管理

### 🔮 长期优化 (按需)

5. **性能优化** (1-2天)
6. **缓存系统** (2天)
7. **消息队列** (3天)
8. **数据分析** (2-3天)

---

## 💡 我的建议

### 推荐路径 1: 完善评审系统 (推荐 ⭐⭐⭐⭐⭐)

**时间**: 5-8天
**顺序**: Phase 2 → Phase 3 → Phase 4

**优势**:
- 形成完整的差异化功能体系
- 从段落级→章节级→作品级,覆盖全部场景
- 市场罕见的专业小说评审系统
- 可以作为核心卖点宣传

**产出**:
- 3个粒度评审系统完整实现
- 版本对比、进步报告等增值功能
- 完整的技术文档和API文档

---

### 推荐路径 2: 性能优化优先

**时间**: 3-4天
**顺序**: 小说分析优化 → AI调用优化 → 容错增强

**优势**:
- 提升现有功能的稳定性
- 降低成本
- 改善用户体验

---

### 推荐路径 3: 混合策略

**时间**: 7-10天
**顺序**: Phase 2段落级 → 性能优化 → Phase 3作品级 → 管理后台

**优势**:
- 平衡新功能和优化
- 持续交付价值
- 降低风险

---

## 📝 下一步行动

**我的建议**: 选择推荐路径1 - 完善评审系统

**立即开始**: Phase 2 段落级评审 (2-3天)

**你想要我帮你**:
A. 立即开始 Phase 2 段落级评审开发
B. 立即开始 Phase 3 作品级评审开发
C. 先做性能优化
D. 其他想法

请告诉我你的选择! 🚀
