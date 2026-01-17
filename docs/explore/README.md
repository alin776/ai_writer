# Explore 功能文档索引

> ✅ **实现状态（2026-01-17 更新）**
>
> | 组件 | 状态 |
> |------|------|
> | `explore_tools.py` 核心类 | ✅ 已实现 |
> | `read_paragraph` 工具 | ✅ 已实现 |
> | `flow_events.py` 事件方法 | ✅ 已实现 |
> | 前端事件处理 | ✅ 已实现 |

## 文档列表

| 序号 | 文档 | 内容 | 状态 |
|------|------|------|------|
| 00 | [Review 报告 V5](./00-review-report.md) | 八轮 Review 发现的问题与修正 | ✅ 更新 |
| 01 | [概述](./01-overview.md) | Explore 定位、与 get_writing_context 的关系 | ✅ |
| 02 | [工具接口](./02-tools.md) | 复用现有工具 + read_paragraph 实现 | ✅ |
| 03 | [状态管理](./03-state.md) | ExploreState 结构、去重逻辑、收敛检测 | ✅ |
| 04 | [AI 决策](./04-ai-decision.md) | AI Plan Prompt、停止条件、输出解析 | ⚠️ 简化为规则驱动 |
| 05 | [流式事件](./05-events.md) | 融入现有 FlowEventBuilder 体系 | ✅ 已实现 |
| 06 | [输出格式](./06-output.md) | ExploreResult 结构、上下文构建 | ✅ |
| 07 | [核心实现](./07-implementation.md) | ContentExplorer 类、主循环、工具调用 | ⚠️ 实现有简化 |
| 08 | [架构集成](./08-integration.md) | 最小改动现有架构 | ⚠️ 部分未实现 |
| 09 | [**前端 UI 规范**](./09-frontend-ui.md) | **一比一复刻 HTML 设计稿的 Explore 轨迹板块** | ❌ 待验证 |

---

## 八轮 Review 总结

### 第一轮：工具复用

| 问题 | 修正 |
|------|------|
| 工具重复定义 | 复用现有 3 个工具 |
| 事件类型不兼容 | 融入 FlowEventBuilder |
| Planning 强制第一步 | AI 自主选择 |

### 第二轮：代码复用

| 问题 | 修正 |
|------|------|
| 段落解析重复实现 | 复用 `_split_paragraphs()` |
| 缺少段落级缓存 | 新增段落缓存 |
| 大章节性能风险 | 添加分块保护 |

### 第三轮：接口验证

| 问题 | 修正 |
|------|------|
| ChapterRepository 不存在 | 使用 WorkService |
| 工具描述位置错误 | 改为 tool_descriptions.py |

### 第四轮：端到端验证

| 问题 | 严重程度 | 修正 |
|------|----------|------|
| smart_continue 没有 context 参数 | ❌ 严重 | 通过 TaskRunner state 传递 |
| 前端未处理 explore_analysis | ⚠️ 中 | 添加前端修改 |
| TaskRunner 集成缺失 | ⚠️ 中 | 补充 task_runner.py |

### 第五轮：实际代码验证

| 验证项 | 结果 |
|--------|------|
| 现有接口引用 | ✅ 全部正确 |
| _split_paragraphs() 复用 | ✅ 可行 |
| WorkService 获取章节 | ✅ 正确方式 |
| smart_continue 参数 | ✅ 第四轮已修正 |

### 第六轮：UI 设计对照

| 问题 | 严重程度 | 修正 |
|------|----------|------|
| 缺少前端 UI 组件规范 | 🔴 严重 | 新增 09-frontend-ui.md |
| explore_analysis 事件字段不完整 | 🟡 中 | 修改为 explore_round + explore_summary |
| 缺少工具标签图标映射 | 🟡 中 | 在 05-events.md 补充 |

### 第七轮：深度验证与修复

| 问题 | 严重程度 | 修正 |
|------|----------|------|
| 缺少 status_text 字段 | 🟡 中 | 添加灰色状态文本支持 |
| 前端字段命名未说明 | 🟡 中 | 添加 snake_case → camelCase 转换表 |
| agentApi.ts 处理代码缺失 | 🟡 中 | 添加完整的 switch case 代码 |

### 第八轮：代码实现核对（2026-01-17 更新）

| 问题 | 严重程度 | 状态 |
|------|----------|------|
| read_paragraph 工具未实现 | 🔴 严重 | ✅ 已实现 |
| flow_events.py 事件方法未实现 | 🔴 严重 | ✅ 已实现 |
| AI 决策简化为规则驱动 | 🟡 中 | ✅ 接受简化 |
| 前端事件处理未验证 | 🟡 中 | ❌ 待验证 |

---

## 改动文件清单（V8 实际状态）

### 后端

| 文件 | 改动 | 代码量 | 状态 |
|------|------|--------|------|
| `tools/explore_tools.py` | 新增 | ~800行 | ✅ 已实现 |
| `langgraph_tools.py` | 添加 read_paragraph | ~130行 | ✅ 已实现 |
| `prompts/tool_descriptions.py` | 添加工具描述 | ~50行 | ⚠️ 待验证 |
| `execution/task_runner.py` | 添加 explore 结果处理 | ~40行 | ⚠️ 待验证 |
| `stream/flow_events.py` | 添加 explore_round/explore_summary 事件 | ~80行 | ✅ 已实现 |
| `utils/tool_cache.py` | 段落级缓存 | ~40行 | ❌ 未实现 |

### 前端

| 文件 | 改动 | 代码量 | 状态 |
|------|------|--------|------|
| `src/services/agentApi.ts` | 添加 explore_round/explore_summary | ~30行 | ✅ 已实现 |
| `src/hooks/useAgentChat.ts` | 添加事件处理 | ~40行 | ✅ 已实现 |
| `src/hooks/useAgentChatStream.ts` | 添加事件处理 | ~40行 | ✅ 已实现 |
| `src/components/ExplorePanel.tsx` | **新增 UI 组件** | ~200行 | ❌ 待实现 |

**已实现**：~1120行 | **待实现**：~200行（UI 组件）

---

## 新增 UI 组件清单

基于 HTML 设计稿 `agent-writing-preview - 副本 (2).html`：

| 组件 | 对应 HTML 类名 | 说明 |
|------|----------------|------|
| ExplorePanel | `.explore-panel` | 探索面板容器 |
| ExploreRound | `.explore-round` | 单轮探索 |
| ExploreRoundCapsule | `.explore-round-capsule` | 折叠胶囊 |
| ExploreTags | `.explore-tags` | 工具标签组 |
| ExploreTag | `.explore-tag` | 单个工具标签 |
| ExploreStatus | `.explore-status` | 状态信息（命中/警告） |
| ExploreEvidence | `.explore-evidence` | 证据片段列表 |
| AIAnalysisCard | `knowledge-section` | AI 分析与规划卡片 |

---

## 事件类型清单（V2 更新）

| 事件类型 | 用途 | 前端组件 |
|----------|------|----------|
| `step_start` | Explore 步骤开始 | execution-step 容器 |
| `explore_round` | 单轮探索数据 | ExploreRound 组件 |
| `step_complete` | 步骤完成 | step-description + tool-operation |
| `explore_summary` | AI 分析与规划 | AIAnalysisCard 组件 |

---

## 验证清单（八轮 Review 后）

| 验证项 | 第五轮 | 第六轮 | 第七轮 | 第八轮 |
|--------|--------|--------|--------|--------|
| 代码接口匹配？ | ✅ | ✅ | ✅ | ✅ |
| 获取章节方式正确？ | ✅ | ✅ | ✅ | ✅ |
| smart_continue 参数？ | ✅ | ✅ | ✅ | ✅ |
| 前端事件处理？ | ⚠️ | ✅ | ✅ | ✅ 已实现 |
| UI 组件规范？ | ❌ | ✅ | ✅ | ❌ 待实现 |
| 颜色/样式规范？ | ❌ | ✅ | ✅ | ❌ 待实现 |
| 折叠/展开交互？ | ❌ | ✅ | ✅ | ❌ 待实现 |
| 与 HTML 设计稿一致？ | ❌ | ⚠️ | ✅ | ❌ 待实现 |
| status_text 字段？ | - | ❌ | ✅ | ✅ |
| 字段命名转换？ | - | ❌ | ✅ | ✅ |
| agentApi.ts 代码？ | - | ❌ | ✅ | ✅ 已实现 |
| **read_paragraph 实现？** | - | - | - | ✅ 已实现 |
| **flow_events 事件方法？** | - | - | - | ✅ 已实现 |

---

## 遗留问题（第八轮 Review 后更新）

### 已实现（高优先级）

1. **flow_events.py 事件方法** ✅
   - `FlowEventBuilder.explore_round()` - 已实现
   - `FlowEventBuilder.explore_summary()` - 已实现
   - 影响：explore_tools.py 事件回调功能现已可用

2. **read_paragraph 工具** ✅
   - 在 `langgraph_tools.py` 中实现（~130行）
   - 支持精确读取段落 + 上下文
   - 复用 `_split_paragraphs()` 函数

3. **前端事件处理** ✅
   - agentApi.ts - 添加 explore_round/explore_summary 事件
   - useAgentChat.ts - 添加 FlowItem 处理
   - useAgentChatStream.ts - 添加 FlowItem 处理

### 待实现

4. **ExplorePanel UI 组件**
   - 基于 HTML 设计稿实现 React 组件
   - 需要实现折叠/展开交互
   - 约 200 行代码

5. **tool_cache.py 段落级缓存**
   - 可选优化，非必需

### 已接受的简化

4. **AI 决策简化**
   - 文档设计：AI 自主选择工具
   - 实际实现：规则驱动的固定流程
   - 决策：接受简化，后续按需迭代

### 原遗留问题

5. **大章节实际性能**：需要用 10 万字章节测试
6. **缓存淘汰策略**：LRU vs TTL 的选择
7. **Planning Agent 理解**：多轮机制的 Prompt 优化
8. **前端组件实现**：React 组件的具体实现细节
