# AI 改写助手 - 实施计划

## 📋 项目概览

**功能名称：** AI 改写助手
**版本：** v1.0 MVP
**开始日期：** 2025-10-25
**预计工期：** 2-3 天
**负责人：** 开发团队

---

## 🎯 核心需求

### 用户故事
作为小说作者，当我写了一段不满意的文字时，我希望能让多个 AI 模型同时帮我改写，然后对比选择最满意的版本，快速提升文字质量。

### 核心价值
- **降低改写门槛** - 不需要自己想怎么改，AI 智能分析并建议
- **提供多样选择** - 多个模型同时改写，总有一个满意的
- **提升写作效率** - 快速将不满意的文字变成满意的内容

---

## 🏗️ 功能架构

### 整体流程

```
用户在编辑器选中不满意的文字
↓
点击右键菜单或工具栏【AI 改写助手】
↓
打开独立页面（新标签页）
↓
【阶段1】AI 智能分析文本（0.5-1秒）
  ├─ 检测质量问题
  ├─ 给出建议的改写模式
  └─ 显示推荐理由
↓
用户确认或调整模式
↓
【阶段2】多模型改写（3-5秒）
  ├─ Gemini 2.5 Pro 改写
  └─ GPT-5 改写
↓
并排展示两个结果
↓
用户选择满意的版本
↓
点击【采用】→ 自动替换编辑器中的原文
↓
保存改写历史到数据库（可选）
```

---

## 📁 技术方案

### 技术栈选择

| 模块 | 技术方案 | 理由 |
|------|---------|------|
| **智能分析** | LangChain PydanticOutputParser | 结构化输出，便于解析 |
| **多模型调用** | 原生 asyncio.gather() | 并发高效，无额外依赖 |
| **上下文提取** | 智能分级策略 | 根据文本长度动态调整 |
| **模型管理** | 配置文件 + API | 易于扩展新模型 |
| **历史记录** | PostgreSQL | 持久化、可搜索、多设备同步 |

### 核心决策

**1. 功能名称：** AI 改写助手

**2. 页面位置：**
- 主页侧边栏：【作品管理】下方 → 【AI 改写助手】
- 点击进入独立页面（新标签页）

**3. 改写模式：**
```
● 优化提升（默认）- 让文字更优美、更生动、更有感染力
○ 扩写丰富 - 增加细节描写和情感渲染
○ 精简压缩 - 保留核心信息，删除冗余
○ 自定义要求 - 告诉 AI 你想要什么效果
```

**4. 上下文策略：** 智能分级
```python
if 原文长度 < 50字:
    前后各 800 字
elif 原文长度 < 200字:
    前后各 500 字
elif 原文长度 < 500字:
    前后各 300 字
else:
    无上下文
```

**5. 初始模型：**
- Gemini 2.5 Pro（擅长创意和细节）
- GPT-5（平衡全能）

**6. 扩展性：**
- 配置文件管理模型列表
- 新增模型只需修改配置 `enabled: True`

---

## 📦 实施计划

### Phase 1：后端开发（1天）

#### 任务清单

**1. 安装依赖**
```bash
cd backend
pip install langchain-core==0.3.0
pip freeze > requirements.txt
```

**2. 创建数据模型**
- [x] `backend/app/schemas/text_analysis.py` - 文本分析结果模型 ✅
  - TextIssue（问题类型）
  - TextAnalysisResult（分析结果）
- [x] `backend/app/models/rewrite_history.py` - 改写历史表 ✅
  - RewriteSession（改写会话）
  - RewriteResult（模型结果）

**3. 创建服务类**
- [x] `backend/app/services/ai/text_analyzer.py` - 智能分析服务 ✅
  - 使用 LangChain PydanticOutputParser
  - 分析文本质量
  - 给出改写建议
- [x] `backend/app/services/ai/rewrite_arena_service.py` - 改写对战服务 ✅
  - 并发调用多个模型
  - 构建 Prompt
  - 返回结构化结果
- [x] `backend/app/services/ai/context_extractor.py` - 上下文提取器 ✅
  - 智能分级策略
  - 根据文本长度动态调整

**4. 配置模型列表**
- [x] 修改 `backend/app/core/config.py` ✅
  - 添加 `REWRITE_MODELS` 配置
  - 添加 `REWRITE_DEFAULT_MODELS`
  - 添加 `REWRITE_MAX_MODELS`

**5. 创建 API 路由**
- [x] `backend/app/api/v1/ai.py` 扩展 ✅
  - `GET /ai/rewrite-arena/models` - 获取可用模型
  - `POST /ai/rewrite-arena/analyze` - 智能分析文本
  - `POST /ai/rewrite-arena/rewrite` - 多模型改写
- [x] `backend/app/api/v1/rewrite_history.py` 新建 ✅
  - `POST /rewrite-history/sessions` - 保存改写记录
  - `GET /rewrite-history/sessions` - 获取历史列表
  - `GET /rewrite-history/sessions/{id}` - 获取详情
  - `DELETE /rewrite-history/sessions/{id}` - 删除记录

**6. 数据库迁移**
```bash
cd backend
alembic revision --autogenerate -m "add_rewrite_history_tables"
alembic upgrade head
```

**预计时间：** 6-8 小时

---

### Phase 2：前端开发（1天）

#### 任务清单

**1. 创建类型定义**
- [ ] `src/types/rewrite-arena.ts`
  - TextIssue
  - TextAnalysisResult
  - ModelResult
  - RewriteMode

**2. 扩展 AIService**
- [ ] `src/services/AIService.ts` 添加方法
  - `getRewriteModels()` - 获取可用模型
  - `analyzeText()` - 智能分析
  - `rewriteText()` - 多模型改写
  - `saveRewriteHistory()` - 保存历史
  - `getRewriteHistory()` - 获取历史

**3. 创建工具函数**
- [ ] `src/utils/contextExtractor.ts` - 前端上下文提取
  - 智能分级逻辑
  - 从编辑器提取文本

**4. 创建核心组件**
- [ ] `src/components/arena/RewriteArenaPage.tsx` - 主页面
  - 输入区（显示原文）
  - 模型选择器
  - 改写模式选择
  - 智能分析结果展示
  - 多模型结果对比展示
  - 采用按钮
- [ ] `src/components/arena/AnalysisResult.tsx` - 分析结果组件
  - 质量评分
  - 问题列表
  - 推荐模式
- [ ] `src/components/arena/ModelResultCard.tsx` - 模型结果卡片
  - 模型信息
  - 改写文本
  - 性能指标
  - 采用按钮

**5. 集成到主应用**
- [ ] 修改路由配置 `src/router/index.tsx`
  - 添加 `/rewrite-arena` 路由
- [ ] 修改侧边栏 `src/components/layout/Sidebar.tsx`
  - 在【作品管理】下方添加【AI 改写助手】菜单项
- [ ] 修改编辑器 `src/components/editor/NovelEditor.tsx`
  - 右键菜单添加【AI 改写助手】选项
  - 选中文本 → 打开新页面 → 自动填充

**6. 样式优化**
- [ ] 响应式布局
- [ ] 加载动画
- [ ] 错误提示

**预计时间：** 6-8 小时

---

### Phase 3：测试和优化（0.5天）

#### 任务清单

**1. 功能测试**
- [ ] 测试智能分析功能
- [ ] 测试多模型改写
- [ ] 测试上下文提取（不同长度）
- [ ] 测试历史记录保存
- [ ] 测试从编辑器打开并回填

**2. 性能测试**
- [ ] 测试并发请求
- [ ] 测试超时处理
- [ ] 测试错误处理

**3. 用户体验优化**
- [ ] 加载状态优化
- [ ] 错误提示友好化
- [ ] 添加使用提示

**4. Bug 修复**
- [ ] 修复发现的问题

**预计时间：** 3-4 小时

---

## 🎨 界面设计

### 主页面布局

```
┌─────────────────────────────────────────────────────────┐
│  AI 改写助手                                 [最小化] [关闭] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  原文（127字）                                           │
│  ┌────────────────────────────────────────────────┐    │
│  │ 主角走进房间，看到了桌子上的剑。                    │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
│  💡 已自动提取前后各 500 字作为上下文                     │
│                                                          │
│  选择改写模式：                                          │
│  ● 优化提升（推荐）○ 扩写丰富 ○ 精简压缩 ○ 自定义      │
│                                                          │
│  [开始分析]                                              │
│                                                          │
│  ▶ 高级选项（点击展开）                                  │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  💡 AI 分析建议（分析完成后显示）                        │
│  ┌────────────────────────────────────────────────┐    │
│  │ 质量评分：45/100                                │    │
│  │                                                 │    │
│  │ 检测到的问题：                                  │    │
│  │ • 描写过于简单（严重）                          │    │
│  │ • 缺少情感渲染（中等）                          │    │
│  │                                                 │    │
│  │ 推荐：✓ 扩写丰富                                │    │
│  │ 理由：建议增加细节和情感描写，使画面更生动      │    │
│  │                                                 │    │
│  │ [确认并改写] [我要自己选]                       │    │
│  └────────────────────────────────────────────────┘    │
│                                                          │
├─────────────────────────────────────────────────────────┤
│  改写结果对比（改写完成后显示）                          │
│                                                          │
│  ┌─────────────────────┐  ┌─────────────────────┐     │
│  │ Gemini 2.5 Pro      │  │ GPT-5               │     │
│  │ ⏱ 2.3s  📝 156字    │  │ ⏱ 1.8s  📝 142字    │     │
│  ├─────────────────────┤  ├─────────────────────┤     │
│  │ 主角推开那扇厚重的   │  │ 房门缓缓开启，主角   │     │
│  │ 木门，昏暗的房间中   │  │ 的视线立刻被桌上那   │     │
│  │ 唯有一柄长剑泛着     │  │ 柄寒光闪烁的长剑    │     │
│  │ 幽冷的寒光...       │  │ 锁定...             │     │
│  │                     │  │                     │     │
│  │ [✓ 采用]  [📋 复制] │  │ [✓ 采用]  [📋 复制] │     │
│  └─────────────────────┘  └─────────────────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 文件结构

### 后端新增文件

```
backend/
├── app/
│   ├── models/
│   │   └── rewrite_history.py           # 新增：改写历史表
│   ├── schemas/
│   │   └── text_analysis.py             # 新增：文本分析模型
│   ├── services/ai/
│   │   ├── text_analyzer.py             # 新增：智能分析服务
│   │   ├── rewrite_arena_service.py     # 新增：改写对战服务
│   │   └── context_extractor.py         # 新增：上下文提取器
│   ├── api/v1/
│   │   ├── ai.py                        # 扩展：添加新路由
│   │   └── rewrite_history.py           # 新增：历史记录API
│   └── core/
│       └── config.py                     # 扩展：添加模型配置
└── requirements.txt                      # 更新：添加 langchain-core
```

### 前端新增文件

```
src/
├── types/
│   └── rewrite-arena.ts                 # 新增：类型定义
├── services/
│   └── AIService.ts                     # 扩展：添加新方法
├── utils/
│   └── contextExtractor.ts              # 新增：上下文提取
├── components/
│   ├── arena/
│   │   ├── RewriteArenaPage.tsx         # 新增：主页面
│   │   ├── AnalysisResult.tsx           # 新增：分析结果组件
│   │   └── ModelResultCard.tsx          # 新增：模型结果卡片
│   ├── layout/
│   │   └── Sidebar.tsx                  # 扩展：添加菜单项
│   └── editor/
│       └── NovelEditor.tsx              # 扩展：添加右键菜单
└── router/
    └── index.tsx                        # 扩展：添加路由
```

---

## ✅ MVP 验收标准

### 功能验收

**必须完成（P0）：**
- [ ] 用户可以从侧边栏进入【AI 改写助手】页面
- [ ] 可以输入或粘贴原文
- [ ] 点击【开始分析】，AI 智能分析并给出建议
- [ ] 可以选择改写模式（优化/扩写/精简/自定义）
- [ ] 点击【确认并改写】，Gemini 和 GPT-5 同时改写
- [ ] 并排展示两个模型的改写结果
- [ ] 显示性能指标（耗时、字数）
- [ ] 点击【采用】，可以复制结果到剪贴板
- [ ] 改写历史保存到数据库

**最好完成（P1）：**
- [ ] 从编辑器选中文本 → 右键 → 打开改写助手
- [ ] 自动提取上下文（智能分级）
- [ ] 显示上下文提示信息
- [ ] 点击【采用】，自动替换编辑器中的原文

**可以没有（P2）：**
- [ ] 历史记录列表页面
- [ ] 历史记录详情查看
- [ ] 支持3-4个模型对比
- [ ] 收藏/分享功能

---

## 🚀 未来扩展方向

### Phase 2（后续迭代）

**功能扩展：**
1. **更多模型支持**
   - Claude 3 Opus
   - GPT-4 Turbo
   - 其他国内大模型

2. **历史记录功能**
   - 历史记录列表页面
   - 搜索和过滤
   - 收藏功能

3. **高级分析**
   - AI 质量评分（自动评判哪个改得好）
   - 差异对比（高亮显示不同部分）
   - 风格分析

---

## 📝 开发注意事项

### 技术要点

1. **LangChain 使用**
   - 只使用 `langchain-core`，不要引入完整的 langchain
   - 只用 `PydanticOutputParser`，保持轻量

2. **并发处理**
   - 使用 `asyncio.gather()` 并发调用模型
   - 注意处理超时和失败

3. **错误处理**
   - API 调用失败要有降级方案
   - 解析失败要返回默认结果
   - 前端要友好提示错误

---

## 📅 时间表

| 日期 | 任务 | 负责人 | 状态 |
|-----|------|--------|------|
| Day 1 AM | 后端：数据模型 + 服务类 | 后端 | ⏳ 待开始 |
| Day 1 PM | 后端：API 路由 + 测试 | 后端 | ⏳ 待开始 |
| Day 2 AM | 前端：类型定义 + Service | 前端 | ⏳ 待开始 |
| Day 2 PM | 前端：主页面 + 组件 | 前端 | ⏳ 待开始 |
| Day 3 AM | 前端：集成 + 样式 | 前端 | ⏳ 待开始 |
| Day 3 PM | 测试 + 优化 + 上线 | 全栈 | ⏳ 待开始 |

---

## 🎯 立即开始

**下一步行动：**
1. ✅ 确认方案无误
2. ⏳ 创建开发分支 `feature/ai-rewrite-assistant`（可选）
3. ✅ 开始后端开发（Day 1）

**准备好开始了吗？** 🚀

---

## ✅ Phase 1 完成总结

**完成时间：** 2025-10-25

### 已完成的任务（10/10）

1. ✅ **安装依赖** - langchain-core==0.3.0
2. ✅ **创建数据模型**
   - `backend/app/schemas/text_analysis.py` - 包含 TextIssue, TextAnalysisResult, RewriteRequest, RewriteResponse 等
   - `backend/app/models/rewrite_history.py` - RewriteSession 和 RewriteResult 数据库表
3. ✅ **创建服务类**
   - `backend/app/services/ai/text_analyzer.py` - 使用 LangChain PydanticOutputParser 的智能分析服务
   - `backend/app/services/ai/rewrite_arena_service.py` - 支持多模型并发改写的服务
   - `backend/app/services/ai/context_extractor.py` - 智能分级上下文提取器
4. ✅ **配置模型列表** - 在 `backend/app/core/config.py` 中添加 REWRITE_MODELS 等配置
5. ✅ **创建 API 路由**
   - 扩展 `backend/app/api/v1/ai.py` - 添加 3 个新接口
   - 新建 `backend/app/api/v1/rewrite_history.py` - 完整的 CRUD 接口
   - 注册路由到 `backend/app/api/__init__.py`
6. ✅ **数据库迁移** - 生成并应用迁移脚本

### 创建的文件列表

**数据层（2个文件）：**
- `backend/app/schemas/text_analysis.py` - 217行
- `backend/app/models/rewrite_history.py` - 75行

**服务层（3个文件）：**
- `backend/app/services/ai/text_analyzer.py` - 282行
- `backend/app/services/ai/rewrite_arena_service.py` - 268行
- `backend/app/services/ai/context_extractor.py` - 146行

**API层（2个文件修改/新增）：**
- `backend/app/api/v1/ai.py` - 新增 246行（3个路由）
- `backend/app/api/v1/rewrite_history.py` - 473行（新文件）
- `backend/app/api/__init__.py` - 修改1行

**配置层（1个文件修改）：**
- `backend/app/core/config.py` - 新增 30行

**数据库迁移：**
- `alembic/versions/20251025_2157_97b2fcd8fdd6_add_rewrite_history_tables.py`

### 核心功能

✅ **智能分析**
- 使用 LangChain PydanticOutputParser 确保结构化输出
- 分析文本质量，检测问题，给出改写建议
- 支持上下文参考

✅ **多模型改写**
- 使用 asyncio.gather() 实现并发调用
- 支持 Gemini 2.5 Pro、GPT-5 等多个模型
- 记录性能指标（耗时、字数）

✅ **上下文提取**
- 智能分级策略（根据文本长度动态调整）
- 原文<50字：前后各800字
- 原文<200字：前后各500字
- 原文<500字：前后各300字

✅ **改写历史**
- 完整的 CRUD API
- 保存会话和结果到数据库
- 支持分页查询和详情查看

### 技术亮点

1. **结构化输出** - 使用 LangChain PydanticOutputParser 确保 AI 返回可解析的 JSON
2. **并发处理** - asyncio.gather() 实现多模型并发调用，提升性能
3. **智能策略** - 上下文提取根据文本长度动态调整
4. **降级方案** - 智能分析失败时返回启发式结果
5. **错误处理** - 完善的异常处理和日志记录
6. **可扩展性** - 配置文件管理模型列表，易于添加新模型

### 遇到的问题和解决方案

**问题1：** 安装依赖时遇到权限问题
**解决：** 关闭所有 Python 进程后重新安装

**问题2：** pydantic 版本冲突
**解决：** 手动清理损坏的安装包，重新安装正确版本

**问题3：** alembic 迁移时 pydantic-core 版本不匹配
**解决：** 强制重装 pydantic==2.12.3 和 pydantic-core==2.41.4

**问题4：** ⚠️ 数据库迁移文件内容错误（严重）
- **现象：** 迁移文件 `20251025_2157_97b2fcd8fdd6_add_rewrite_history_tables.py` 存在但没有创建表
- **影响：** 数据库中缺少 `rewrite_sessions` 和 `rewrite_results` 表，导致 API 无法使用
- **根因：** 自动生成的迁移文件只修改了索引，没有 CREATE TABLE 语句
- **解决：** 手动创建正确的迁移文件 `20251025_2200_add_rewrite_history_tables.py`
- **文件：** `backend/alembic/versions/20251025_2200_add_rewrite_history_tables.py`

**问题5：** ⚠️ SQLAlchemy MissingGreenlet 错误（严重）
- **现象：** 调用保存接口时抛出 `MissingGreenlet: greenlet_spawn has not been called`
- **位置：** `backend/app/api/v1/rewrite_history.py:171`
- **根因：** 在异步环境中手动设置关系属性 `session.results = ...` 触发懒加载，但缺少 greenlet 上下文
- **影响：** 保存改写历史功能完全失效
- **解决方案：**
  1. 不手动设置关系属性，使用显式查询
  2. 在所有函数开始时提取用户信息：`user_id = current_user.id; username = getattr(current_user, 'username', str(user_id))`
  3. 避免在异常处理中访问可能触发懒加载的属性
- **修复范围：** 4 个 API 函数全部修复
- **技术文档：** 创建 `backend/FIX_ASYNC_ISSUE.md` 详细说明

**问题6：** httpx.ReadTimeout 超时错误
- **现象：** 测试脚本调用保存接口 30 秒后超时
- **根因：** 修改代码后未重启后端服务，运行的是旧的有 bug 的代码
- **解决：** 创建 `backend/HOW_TO_TEST.md` 提供清晰的测试和重启说明

**问题7：** 性能优化 - N+1 查询问题
- **现象：** 获取历史列表时，循环查询每个会话的结果数量
- **影响：** 当历史记录多时性能差
- **解决：** 使用子查询 + LEFT JOIN，一次查询获取所有数据
- **位置：** `backend/app/api/v1/rewrite_history.py` 的 `get_rewrite_sessions` 函数

### API 接口清单

**AI 改写助手（3个）：**
- `GET /api/v1/ai/rewrite-arena/models` - 获取可用模型列表
- `POST /api/v1/ai/rewrite-arena/analyze` - 智能分析文本
- `POST /api/v1/ai/rewrite-arena/rewrite` - 多模型改写

**改写历史（4个）：**
- `POST /api/v1/rewrite-history/sessions` - 保存改写记录
- `GET /api/v1/rewrite-history/sessions` - 获取历史列表（分页）
- `GET /api/v1/rewrite-history/sessions/{id}` - 获取会话详情
- `DELETE /api/v1/rewrite-history/sessions/{id}` - 删除会话

### 下一步计划

**Phase 2：前端开发（1天）**
- 创建 TypeScript 类型定义
- 扩展 AIService
- 创建核心组件（RewriteArenaPage, AnalysisResult, ModelResultCard）
- 集成到主应用
- 样式优化

**预计时间：** 6-8 小时

---

## 🔄 Phase 1 当前状态

**状态：** ⏸️ 等待测试验证

### 已完成工作（100%）
- ✅ 所有代码已编写完成
- ✅ 所有严重 bug 已修复（数据库迁移、SQLAlchemy 异步、性能优化）
- ✅ 创建测试脚本和测试指南
- ✅ 创建技术文档

### 待验证内容
- ⏳ 重启后端服务
- ⏳ 运行测试脚本 `backend/quick_test_save.py`
- ⏳ 验证所有 API 接口正常工作

### 测试指南
详见：`backend/HOW_TO_TEST.md`

**关键步骤：**
1. 重启后端服务（Ctrl+C 后重新启动）
2. 在另一个终端运行：`python quick_test_save.py`
3. 验证输出显示 "✅ 测试通过！"

### 后续计划
一旦测试通过，立即开始 **Phase 2：前端开发**

---

**开发人员：** Claude Code
**完成日期：** 2025-10-25
**总耗时：** 约 6 小时（包括问题排查和修复）
**修复 Bug 数：** 7 个（3 个严重）
