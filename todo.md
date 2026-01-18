# TODO

## 本次优化：Explore 充足性评估 + 可观测性 + 去重收敛（2026-01-19）

### 待办清单

- [ ] 增加 `_ai_assess_sufficiency` 原始响应与解析结果日志（截断避免刷屏）
- [ ] 将 `sufficient/coverage` 写入 `explore_summary` 事件（前端可见）
- [ ] 提升充足性评估的任务类型（QUALITY_EVALUATION → DEEP_ANALYSIS）
- [ ] 证据去重/相似度阈值：仅“有效新增证据”计入收敛判断
- [ ] 输出 review 结论与风险点（含行号）
- [ ] 在本文件补充 review 总结

### 解决方案（拟）

- 在 `_ai_assess_sufficiency` 记录原始响应与解析字段，便于定位“始终 false”的原因
- `explore_summary` 事件新增 `sufficient` 和 `coverage` 字段（前端忽略也不影响）
- 将评估任务切换为高质量模型类型，提高“足够信息”判断准确度
- 对证据做去重（章节+段落+文本摘要），并可选设定 `similarity` 最小阈值

### 预期

- 当信息已充分时，Explore 会提前停止而不是跑满 10 轮
- 前端可看到“充足性结论/覆盖描述”，便于定位停不下来的原因
- 收敛判断更真实，避免重复证据导致“永远有新证据”

---

## 本次排查：Explore 仍跑满 10 轮（AI 充足性未提前停止）（2026-01-19）

### 待办清单

- [x] 复核 `_ai_assess_sufficiency` 调用与异常兜底路径（含 JSON 解析与布尔归一）
- [x] 检查 `TaskType.QUALITY_EVALUATION` 对应模型选择与可能的保守输出
- [x] 复核收敛判定与证据去重机制，确认为何持续有“新证据”
- [x] 对照前端事件/日志，确认实际轮次数与 `stop_reason`
- [x] 输出 review 结论与风险点（含行号）
- [x] 在本文件补充 review 总结

### 解决方案（拟）

- 若 AI 充足性常返回 false，可改用更高质量模型或调整 prompt
- 增加“覆盖不足但无新信息连续 N 轮”的强制停止策略
- 对证据做去重/相似度阈值，避免重复证据导致不收敛
- parse 失败时记录完整响应并回退阈值判定

### review

- 直接原因：探索循环仅在 `assessment.sufficient` 为真时提前停止；否则只靠收敛与最大轮次兜底（`backend/app/services/agent/tools/explore_tools.py:657`）。
- 模型因素：`_ai_assess_sufficiency` 使用 `TaskType.QUALITY_EVALUATION`，映射为简单任务模型（Flash Lite），更易保守判定不足（`backend/app/services/agent/tools/explore_tools.py:944`、`backend/app/services/agent/model_selector.py:165`）。
- 收敛难触发：证据不去重且每次搜索结果都会计为新增，导致“连续无新信息”很难成立（`backend/app/services/agent/tools/explore_tools.py:212`、`backend/app/services/agent/tools/explore_tools.py:265`）。
- 可观测性不足：`stop_reason` 仅在工具结果里，流事件不包含该字段，前端难定位为何跑满 10 轮（`backend/app/services/agent/stream/flow_events.py:315`、`src/hooks/useAgentChatStream.ts:495`）。

---

## 本次修复：Explore 默认轮次从 3 提升到 10（2026-01-19）

### 待办清单

- [x] 调整 `explore_content` 默认 `max_rounds` 为 10，并同步注释
- [x] 调整 `tool_executor.py` 中 `explore_content` 的默认 `max_rounds` 为 10（两处）
- [x] 同步 `tool_descriptions.py` 的默认轮次描述为 10
- [x] 输出 review 结论与风险点（含行号）
- [x] 在本文件补充 review 总结

### 解决方案（拟）

- 维持 `MAX_ROUNDS=10`，仅把默认 `max_rounds` 从 3 提升到 10，避免规划器不传参时被限制在 3 轮
- 更新工具描述，确保 Planning/Decision 提示词与实际默认值一致

### review

- 修复点：`explore_content` 默认 `max_rounds` 改为 10，并同步注释（`backend/app/services/agent/tools/explore_tools.py:1457`、`backend/app/services/agent/tools/explore_tools.py:1465`）。
- 修复点：执行器默认兜底改为 10，避免规划器不传参时回落到 3 轮（`backend/app/services/agent/execution/tool_executor.py:446`、`backend/app/services/agent/execution/tool_executor.py:884`）。
- 提示一致性：工具描述默认轮次改为 10（`backend/app/services/agent/prompts/tool_descriptions.py:20`）。
- 风险：默认上限提升会增加 token 与耗时；但仍受 AI 充足性判断与收敛规则影响，达到充足即会提前停止。

---

## 本次排查：Explore 轮次固定为 3（2026-01-19）

### 待办清单

- [x] 核对 `explore_content` 默认 `max_rounds` 的来源（`explore_tools.py` / `tool_executor.py` / `tool_descriptions.py`）
- [x] 复核 Explore 轮次停止条件与 ReAct 机制的实际行为（AI 充足性判断 + 收敛）
- [x] 给出最小改动方案：允许默认 10 轮/可配置，并对齐提示词与文档
- [x] 输出 review 结论与风险点（含行号）
- [x] 在本文件补充 review 总结

### 解决方案（拟）

- 将 `explore_content` 的默认 `max_rounds` 提升为 10（或读取配置项 `EXPLORE_MAX_ROUNDS`，默认 10）
- 同步更新 `tool_executor.py` 的默认值与 `tool_descriptions.py` 文案，避免仍默认为 3
- 对齐 `docs/explore` 中的默认轮次描述，消除文档与实现不一致

### review

- 现象原因：`explore_content` 默认 `max_rounds=3`，并且 `tool_executor` 会补默认值，规划器不显式传参时固定 3 轮。
- ReAct 实际行为：每轮 AI 规划 + 充足性评估，命中即停；`check_convergence` 连续无新信息也会停止，无法保证跑满 10 轮。
- 限制补充：每轮搜索词最多 3 个、章节最多 2 个、段落最多 3 个，导致“探索深度”还受每轮上限影响。
- 文档不一致：`docs/explore/08-integration.md` 仍写默认 5，与当前代码默认 3 不一致。
- 最小方案：把默认 max_rounds 提升为 10 或改成配置项，并同步提示词/文档；代价是 token 与耗时上升。

---

## 本次排查：AI深度分析未达预期（2026-01-18）

- [x] 核对日志/前端轨迹/素材，确认用户请求与作品内容是否匹配
- [x] 追踪 explore_content → analyze_content → response_builder 的执行链路与关键规则
- [x] 对照前后端事件与规划提示词，整理偏差原因与改进建议
- [x] 在本文件补充 review 总结

---

## Review（2026-01-18）

- 已核对 `Backend.md`、`INFO.md` 与 `docs/Agent/real-book/斗破：开局获取抽取系统.txt`，确认用户请求角色与当前作品不匹配（林仙/叶凡/刘云志等 vs 萧凌）。
- 追踪链路 `explore_content` → `analyze_content` → `response_builder`，确认探索未对缺失实体做强校验，分析工具默认偏文本质量分析，且 `explore_content` 未被归类为输入任务。
- 前后端事件显示 `explore_summary.next_action` 固定为“续写”造成误导，覆盖度不足时仍继续分析，缺少“请确认作品/角色”的前置提示。
- 改进建议：增加实体覆盖度校验并主动询问；分析类任务设置 `aspects`/`focus` 或新增关系分析工具；修正 `INPUT_TOOLS` 与 `next_action` 文案。

---

## 本次排查：搜索不到应有角色（2026-01-18）

- [x] 核对本次请求绑定的 work_id 与目标作品是否一致（日志/前端传参）
- [x] 核对检索链路：HybridRetriever/ChapterVectorService/Chapter.content 是否能命中
- [x] 核对会话/Tab 绑定逻辑，排除跨作品复用会话导致错 work_id
- [x] 汇总原因与修复建议
- [x] 在本文件补充 review 总结

### Review（2026-01-18）

- 日志中的 work_id=25f72108... 对应检索到的章节/世界观是“萧凌/万界抽取系统”方向，和请求角色不一致。
- 仓库素材中包含目标角色的文本在 `docs/Agent/real-book/人在诸天，摆烂成帝.txt`，不是当前日志对应的“斗破”素材。
- 检索链路本身工作正常（RAG + Hybrid 反复返回片段），问题更像是 work_id 指向了错误作品或目标作品未导入数据库。
- 前端 AIPanel 明确传入 work_id，HistoryPanel 也按 work_id/chapter_id 过滤，跨作品复用会话的可能性较低。
- 建议优先核对当前会话绑定作品、确认目标作品已导入并完成向量化，再复测检索。

## Explore 功能设计文档

### ✅ 文档编写 + 四轮 Review 完成

**创建时间：** 2026-01-17
**第一轮 Review：** 2026-01-17
**第二轮深度 Review：** 2026-01-17
**第三轮代码验证：** 2026-01-17
**第四轮端到端验证：** 2026-01-17

---

### 文档列表（10个）

| 文档 | 状态 |
|------|------|
| `docs/explore/README.md` | ✅ 索引（V4更新） |
| `docs/explore/00-review-report.md` | ✅ Review 报告 V4 |
| `docs/explore/01-overview.md` | ✅ 概述 |
| `docs/explore/02-tools.md` | ✅ 工具接口（V3更新） |
| `docs/explore/03-state.md` | ✅ 状态管理 |
| `docs/explore/04-ai-decision.md` | ✅ AI 决策 |
| `docs/explore/05-events.md` | ✅ 流式事件 |
| `docs/explore/06-output.md` | ✅ 输出格式（V4更新） |
| `docs/explore/07-implementation.md` | ✅ 核心实现 |
| `docs/explore/08-integration.md` | ✅ 架构集成（V4更新） |

---

### 四轮 Review 发现的问题

#### 第一轮

| 问题 | 修正 |
|------|------|
| 工具重复定义（4个） | 复用现有 3 个 + 新增 1 个 |
| 事件类型不兼容 | 融入现有 FlowEventBuilder |
| Planning 强制第一步 | AI 自主选择 |

#### 第二轮（深度验证）

| 问题 | 修正 |
|------|------|
| 段落解析重复实现 | 复用 `_split_paragraphs()` |
| 缺少段落级缓存 | 新增 tool_cache.py 段落缓存 |
| 大章节性能风险 | 添加分块保护（200K字符） |
| 上下文传递格式不明 | 定义了输出格式和对接方式 |
| Planning 工具描述缺失 | 补充 tool_descriptions.py |

#### 第三轮（代码验证）

| 问题 | 修正 |
|------|------|
| `ChapterRepository.get_by_order` 不存在 | 使用 `WorkService.get_work_by_id()` |
| 工具描述添加位置错误 | 改为 `tool_descriptions.py` |
| 段落级缓存设计不完整 | 补充 `ParagraphCache` 类设计 |

#### 第四轮（端到端验证）❌ 发现严重问题

| 问题 | 严重程度 | 修正 |
|------|----------|------|
| smart_continue 没有 context 参数 | ❌ 严重 | 通过 TaskRunner state 传递 |
| 前端未处理 explore_analysis 事件 | ⚠️ 中 | 添加前端修改清单 |
| TaskRunner 集成逻辑缺失 | ⚠️ 中 | 补充 task_runner.py 修改 |

---

### 核心设计决策（最终版）

| 决策点 | 结论 |
|--------|------|
| Explore 定位 | get_writing_context 的增强版 |
| 触发时机 | AI 自主选择（不强制） |
| 复用现有工具 | search_content、get_writing_context、locate_content |
| 复用现有函数 | `_split_paragraphs()` |
| 新增工具 | read_paragraph |
| 停止条件 | AI 判断 / 收敛检测 / 超时 |
| 大章节处理 | 分块保护 |
| 获取章节方式 | WorkService.get_work_by_id() |
| 数据传递 | 通过 TaskRunner state 传递 explore_context |

---

### 改动文件清单（V4更新）

#### 后端

| 文件 | 类型 | 代码量 |
|------|------|--------|
| `tools/explore_tools.py` | 新增 | ~300行 |
| `langgraph_tools.py` | 修改 | ~70行 |
| `prompts/tool_descriptions.py` | 修改 | ~50行 |
| `execution/task_runner.py` | 修改 | ~40行 |
| `stream/flow_events.py` | 修改 | ~30行 |
| `utils/tool_cache.py` | 修改 | ~40行 |

#### 前端

| 文件 | 类型 | 代码量 |
|------|------|--------|
| `src/services/agentApi.ts` | 修改 | ~15行 |
| `src/hooks/useAgentChat.ts` | 修改 | ~20行 |
| `src/hooks/useAgentChatStream.ts` | 修改 | ~20行 |

**后端**：~530行 | **前端**：~55行 | **总计**：~585行

---

### 验证清单（四轮 Review 后）

- [x] 是否引入新问题？→ 复用现有工具和函数
- [x] 是否解决原问题？→ 多轮探索 + 精度验证
- [x] 修改完整性？→ 补充了缓存、工具描述、前端修改
- [x] 逻辑一致性？→ 融入现有架构
- [x] 段落解析可行？→ 复用 _split_paragraphs()
- [x] 缓存兼容？→ 新增段落级缓存
- [x] 并发控制？→ 复用 ParallelExecutor
- [x] 错误处理？→ 复用 _retry_on_failure()
- [x] 大章节性能？→ 分块保护
- [x] 上下文对接？→ 定义了格式
- [x] 代码接口匹配？→ 验证通过
- [x] 获取章节方式正确？→ 使用 WorkService
- [x] 数据流完整？→ 通过 TaskRunner state 传递
- [x] 前端事件处理？→ 添加修改清单

---

### 遗留问题（待开发时验证）

1. 大章节实际性能（10万字测试）
2. 缓存淘汰策略选择
3. Planning Agent 对多轮机制的理解

---

---

## 第五轮 Review：实际代码验证报告（2026-01-17）

### 一、Review 结论

**总体评价：✅ 开发文档设计合理，与实际代码架构兼容**

开发文档是**待开发功能**的设计文档，不是对已实现功能的描述。经过深度代码探索，验证了文档中对现有接口的引用是准确的。

---

### 二、文档与实际代码对照表

#### 2.1 现有接口引用验证（✅ 全部正确）

| 文档描述 | 实际代码位置 | 验证结果 |
|----------|-------------|----------|
| `search_content` | langgraph_tools.py:795-856 | ✅ 接口匹配 |
| `get_writing_context` | langgraph_tools.py:944-1182 | ✅ 接口匹配 |
| `locate_content` | locate_tools.py:444-858 | ✅ 接口匹配 |
| `_split_paragraphs()` | locate_tools.py:39-78 | ✅ 可直接复用 |
| `WorkService.get_work_by_id()` | work_service.py:20+ | ✅ 正确方式 |
| `FlowEventBuilder` | flow_events.py:43-269 | ✅ 可复用 |
| `tool_descriptions.py` | prompts/tool_descriptions.py | ✅ 存在 |
| `task_runner.py` | execution/task_runner.py:31-535 | ✅ 存在 |
| `tool_cache.py` | utils/tool_cache.py:140-276 | ✅ 存在 |

#### 2.2 smart_continue 实际接口验证（⚠️ 文档第四轮已修正）

**实际接口**（editor_tools.py:630-713）：
```python
async def smart_continue(
    chapter_id: str,
    chapter_content: Optional[str] = None,  # 非 context！
    user_requirement: Optional[str] = None,
    word_count: int = 500,
    user_id: Optional[str] = None
) -> str
```

**文档修正方案**：通过 TaskRunner state 传递 explore_context → chapter_content

✅ **验证结论**：文档第四轮 Review 的修正方案是正确的

---

### 三、待实现功能清单

以下功能在当前代码库中**不存在**，是文档设计的**新功能**：

| 功能 | 状态 | 说明 |
|------|------|------|
| `read_paragraph` 工具 | 🔴 不存在 | 需要新增到 langgraph_tools.py |
| `explore_content` 工具 | 🔴 不存在 | 需要新增 tools/explore_tools.py |
| `explore_analysis` 事件 | 🔴 不存在 | 需要添加到 flow_events.py |
| 段落级缓存 | 🔴 不存在 | 需要添加到 tool_cache.py |
| 前端 explore_analysis 处理 | 🔴 不存在 | 需要修改前端 3 个文件 |

---

### 四、前端代码验证

#### 4.1 agentApi.ts 事件处理（现有事件）

当前支持的 FlowEvent 类型：
- ✅ `agent_header`
- ✅ `text`
- ✅ `step_start`
- ✅ `knowledge_loaded`
- ✅ `step_complete`
- ✅ `output_ready`
- ✅ `completion`
- ✅ `revision`
- ✅ `summarization_start`
- ✅ `summarization_complete`
- 🔴 `explore_analysis` **不存在**

#### 4.2 useAgentChat.ts 验证

- 行 802-1079：`onFlowEvent` 处理逻辑
- 支持 step、knowledge、output、revision、summarization 等类型
- 🔴 **不支持 explore_analysis**

#### 4.3 useAgentChatStream.ts 验证

- 行 342-488：`onFlowEvent` 处理逻辑
- 🔴 **不支持 explore_analysis**

---

### 五、文档设计的合理性评估

| 评估项 | 评分 | 说明 |
|--------|------|------|
| 复用现有接口 | ⭐⭐⭐⭐⭐ | 正确识别了可复用的函数和工具 |
| 接口参数准确性 | ⭐⭐⭐⭐⭐ | 经四轮 Review 已修正 |
| 架构融入方式 | ⭐⭐⭐⭐⭐ | 最小改动原则，符合现有模式 |
| 前端改动完整性 | ⭐⭐⭐⭐☆ | 识别了需要修改的文件，但缺少具体行号 |
| 代码量估算 | ⭐⭐⭐⭐☆ | ~585行估算合理 |

**总评：4.6/5 ⭐**

---

### 六、开发建议

#### 6.1 实现顺序建议

1. **Phase 1 - 后端核心**
   - 新增 `tools/explore_tools.py`（ContentExplorer 类）
   - 新增 `read_paragraph` 到 langgraph_tools.py

2. **Phase 2 - 后端集成**
   - 修改 task_runner.py（添加 explore_context 传递）
   - 修改 flow_events.py（添加 explore_analysis 事件）
   - 修改 tool_descriptions.py（添加工具描述）

3. **Phase 3 - 前端支持**
   - 修改 agentApi.ts（添加 explore_analysis case）
   - 修改 useAgentChat.ts（添加事件处理）
   - 修改 useAgentChatStream.ts（添加事件处理）

4. **Phase 4 - 缓存优化**
   - 修改 tool_cache.py（添加段落级缓存）

#### 6.2 关键文件修改清单（带行号参考）

| 文件 | 修改位置 | 操作 |
|------|----------|------|
| langgraph_tools.py | ~行856后 | 新增 read_paragraph 函数 |
| task_runner.py | 行66-187 | 添加 explore_content 结果处理 |
| flow_events.py | 行157后 | 新增 explore_analysis 方法 |
| flow_events.py | 行272-294 | 添加 explore/read_paragraph 图标 |
| tool_descriptions.py | 行292后 | 新增 _get_explore_tools_section() |
| agentApi.ts | 行316后 | 添加 explore_analysis case |
| useAgentChat.ts | 行809后 | 添加 explore_analysis 处理 |
| useAgentChatStream.ts | 行345后 | 添加 explore_analysis 处理 |

---

### 七、结论

**开发文档符合实际开发情况** ✅

1. 文档对现有接口的描述**准确无误**
2. 第四轮 Review 发现的 smart_continue 参数问题已正确修正
3. 设计方案与现有架构**高度兼容**
4. 待实现功能清单**完整可行**

**可以按照文档开始实现开发**

---

## 第六轮 Review：UI 设计对照验证（2026-01-17）

### 一、参照文件

**HTML 设计稿**：`agent-writing-preview - 副本 (2).html`

**Explore 轨迹板块位置**：行 241-444（CSS 样式）、行 957-1148（HTML 结构）

---

### 二、HTML 设计稿中的 Explore UI 结构

#### 2.1 整体布局（行 957-1148）

```
execution-step (Explore 轨迹（3 轮）)
├── step-header
│   ├── step-icon.completed (✓)
│   └── step-title ("Explore 轨迹（3 轮）")
└── step-content
    ├── explore-panel
    │   ├── explore-round (轮次1)
    │   ├── explore-round (轮次2)
    │   └── explore-round (轮次3)
    ├── step-description
    ├── AI 分析与规划 (knowledge-section)
    └── tool-operation
```

#### 2.2 explore-round 结构（行 969-1077）

```
explore-round
└── explore-round-capsule.collapsed
    ├── explore-round-header
    │   ├── explore-round-index (scan 图标)
    │   ├── explore-round-title ("初次检索与定位")
    │   └── explore-round-toggle (∧/∨)
    └── explore-round-body.hidden
        ├── explore-tags
        │   ├── explore-tag (Search: 关键词)
        │   ├── explore-tag (Locate: 第N章·第M段)
        │   ├── explore-tag (ReadRaw: 第N章)
        │   └── explore-tag (Review: 状态)
        ├── explore-status
        │   ├── span.hit ("命中 N 条")
        │   └── span.warn ("缺少：XXX")
        └── explore-evidence
            ├── explore-evidence-header
            └── explore-items
                └── explore-item
                    ├── meta (第N章·第M段)
                    └── 文本内容
```

#### 2.3 AI 分析与规划结构（行 1084-1140）

```
knowledge-section
└── 胶囊容器
    ├── header (brain 图标 + "AI 分析与规划")
    └── narrative-content
        ├── 探索总结 (file-search 图标)
        ├── 下一步行动 (arrow-right-circle 图标)
        └── 统计数据标签（世界观、章节、证据、覆盖度）
```

---

### 三、开发文档 vs HTML 设计稿对照表

| UI 组件 | HTML 设计稿 | 开发文档 | 差距 |
|---------|------------|----------|------|
| **explore-round-capsule** | ✅ 行 254-275 | ❌ 未描述 | 🔴 缺少折叠胶囊设计 |
| **explore-tags** | ✅ 行 345-372 | ❌ 未描述 | 🔴 缺少工具标签设计 |
| **explore-status** | ✅ 行 374-391 | ❌ 未描述 | 🔴 缺少状态显示设计 |
| **explore-evidence** | ✅ 行 393-438 | ⚠️ 仅数据结构 | 🟡 缺少 UI 布局 |
| **AI 分析与规划** | ✅ 行 1084-1140 | ⚠️ 仅 analysis 字段 | 🟡 缺少 UI 布局 |
| **统计标签** | ✅ 行 1115-1137 | ⚠️ 仅 stats 字段 | 🟡 缺少 UI 布局 |

---

### 四、开发文档缺失的前端 UI 规范

#### 4.1 缺失：explore-tags 组件规范

HTML 设计稿中的工具标签：
```html
<div class="explore-tags">
  <span class="explore-tag">
    <i data-lucide="search"></i>
    Search: <span class="tag-strong">吞噬器灵 羚羊献食</span>
  </span>
  <span class="explore-tag">
    <i data-lucide="crosshair"></i>
    Locate: 第5章 · 第7段
  </span>
  <span class="explore-tag">
    <i data-lucide="file-text"></i>
    ReadRaw: 第5章
  </span>
  <span class="explore-tag">
    <i data-lucide="check-circle"></i>
    Review: 覆盖不足
  </span>
</div>
```

**开发文档需要补充**：
- 工具标签的图标映射（Search → search, Locate → crosshair, ReadRaw → file-text, Review → check-circle）
- 标签的样式规范（胶囊样式、颜色）
- 关键词高亮规范（tag-strong 类）

#### 4.2 缺失：explore-status 组件规范

HTML 设计稿中的状态显示：
```html
<div class="explore-status">
  <span class="hit">命中 4 条</span>
  <span class="warn">缺少：浑圆桩训练</span>
</div>
```

**开发文档需要补充**：
- 命中数的显示格式和颜色（#10b981 绿色）
- 警告信息的显示格式和颜色（#f59e0b 黄色）

#### 4.3 缺失：折叠/展开交互规范

HTML 设计稿中的交互：
- 默认折叠状态（.collapsed 类）
- 点击展开显示详情
- 展开时移除 .hidden 类

**开发文档需要补充**：
- 折叠/展开的触发机制
- 状态切换的动画效果

---

### 五、事件格式对照

#### 5.1 开发文档中的 explore_analysis 事件

```python
{
    "type": "explore_analysis",
    "step_id": 1,
    "round_idx": 1,
    "reasoning": "...",
    "stats": {"evidences": 8, "chapters": 2, "worldview": 5},
    "sufficient": False,
    "next_actions": ["..."]
}
```

#### 5.2 HTML 设计稿需要的数据

| 字段 | 开发文档 | HTML 设计稿需要 | 差距 |
|------|----------|-----------------|------|
| 轮次标题 | ❌ 无 | "初次检索与定位" | 🔴 缺少 |
| 工具调用列表 | ❌ 无 | Search/Locate/ReadRaw/Review | 🔴 缺少 |
| 命中数 | stats.evidences | "命中 N 条" | 🟢 可转换 |
| 缺失项 | next_actions | "缺少：XXX" | 🟢 可转换 |
| 证据片段 | ❌ 无 | explore-evidence | 🔴 缺少 |

---

### 六、需要补充的开发文档内容

#### 6.1 新增章节建议：09-frontend-ui.md

```markdown
# Explore 前端 UI 设计规范

## 1. 组件层级结构
[参照 HTML 设计稿的结构]

## 2. explore-tags 工具标签
### 2.1 图标映射
| 工具类型 | 图标 | 标签前缀 |
|----------|------|----------|
| 搜索 | search | Search: |
| 定位 | crosshair | Locate: |
| 读取原文 | file-text | ReadRaw: |
| 审查 | check-circle | Review: |

### 2.2 样式规范
- 背景色：#2a2a2a
- 边框：1px solid #3a3a3a
- 圆角：16px
- 关键词高亮：#5c9eff

## 3. explore-status 状态显示
### 3.1 颜色规范
| 状态 | 颜色 | 类名 |
|------|------|------|
| 命中 | #10b981 | .hit |
| 警告 | #f59e0b | .warn |

## 4. 折叠/展开交互
- 默认状态：折叠
- 触发方式：点击 header
- 动画：transition 0.2s

## 5. AI 分析与规划卡片
[参照 HTML 设计稿的结构]
```

#### 6.2 修改 05-events.md

补充 explore_analysis 事件的完整字段：

```python
FlowEventBuilder.explore_analysis(
    step_id=1,
    round_idx=1,
    title="初次检索与定位",           # 新增：轮次标题
    tool_calls=[                       # 新增：工具调用列表
        {"type": "Search", "query": "吞噬器灵 羚羊献食"},
        {"type": "Locate", "location": "第5章·第7段"},
        {"type": "ReadRaw", "chapter": 5},
        {"type": "Review", "status": "覆盖不足"}
    ],
    hit_count=4,                       # 新增：命中数
    missing_items=["浑圆桩训练"],      # 新增：缺失项
    evidences=[                        # 新增：证据片段
        {"chapter": 5, "para": 7, "text": "..."}
    ],
    reasoning="...",
    stats={...},
    sufficient=False
)
```

---

### 七、结论

**开发文档与 HTML 设计稿存在以下差距** ⚠️

| 问题 | 严重程度 | 建议 |
|------|----------|------|
| 缺少前端 UI 组件设计规范 | 🔴 严重 | 新增 09-frontend-ui.md |
| explore_analysis 事件字段不完整 | 🟡 中等 | 修改 05-events.md |
| 缺少工具标签图标映射 | 🟡 中等 | 在 08-integration.md 补充 |
| 缺少颜色/样式规范 | 🟡 中等 | 在新文档中定义 |

**建议**：在开发前补充前端 UI 规范文档，确保开发结果与 HTML 设计稿一致。

---

## 第七轮 Review：深度验证与修复（2026-01-17）

### 一、验证方法

1. 重新读取 HTML 设计稿（行 957-1148）
2. 对比现有 FlowEventBuilder 接口（flow_events.py）
3. 检查前端事件处理逻辑（agentApi.ts）
4. 验证文档完整性

---

### 二、发现的问题

#### 2.1 explore-status 状态不完整

**HTML 设计稿中的三种状态**：

| 轮次 | 状态显示 | 颜色 |
|------|----------|------|
| 第1轮 | "缺少：浑圆桩训练" | 黄色 `.warn` |
| 第2轮 | "补漏完成" | 灰色普通 |
| 第3轮 | "覆盖度达标" | 灰色普通 |

**原文档问题**：只处理了 `missing_items`（黄色警告），没有处理灰色状态文本。

**修复**：添加 `status_text` 字段。

#### 2.2 前端字段命名转换未说明

**问题**：后端使用 snake_case，前端使用 camelCase，但文档未说明转换规则。

**修复**：添加字段命名转换表。

#### 2.3 agentApi.ts 处理代码缺失

**问题**：新增的 `explore_round` 和 `explore_summary` 事件需要在 agentApi.ts 的 switch 中添加处理。

**修复**：添加完整的 switch case 代码示例。

---

### 三、修复的文件

| 文件 | 修复内容 |
|------|----------|
| `05-events.md` | 添加 `status_text` 字段、字段命名转换表、agentApi.ts 代码 |
| `06-output.md` | 添加 `_get_status_text()` 辅助函数 |
| `09-frontend-ui.md` | 完善 explore-status 状态显示逻辑、更新 React 接口 |
| `README.md` | 添加第七轮 Review 总结 |

---

### 四、验证清单

| 验证项 | 结果 |
|--------|------|
| 是否引入新问题？ | ✅ 否 |
| 是否真正解决原问题？ | ✅ 是 |
| 修改完整性？ | ✅ 完整 |
| 逻辑一致性？ | ✅ 一致 |
| 与 HTML 设计稿一致？ | ✅ 一致 |

---

### 五、最终验证：HTML 元素对照表

| HTML 元素 | 事件字段 | 前端组件 | 状态 |
|-----------|----------|----------|------|
| `.explore-round-title` | `title` | ExploreRound | ✅ |
| `.explore-tags` | `toolCalls` | ExploreTags | ✅ |
| `.explore-status .hit` | `hitCount` | ExploreStatus | ✅ |
| `.explore-status .warn` | `missingItems` | ExploreStatus | ✅ |
| `.explore-status` (灰色) | `statusText` | ExploreStatus | ✅ 新增 |
| `.explore-evidence` | `evidences` | ExploreEvidence | ✅ |
| "AI 分析与规划" | `explore_summary` | AIAnalysisCard | ✅ |
| `.step-description` | `stepDescription` | - | ✅ |
| `.tool-operation` | `toolOperation` | - | ✅ |

---

### 六、结论

**所有问题已修复，文档与 HTML 设计稿完全对应** ✅

1. `status_text` 字段已添加，支持灰色状态文本
2. 前端字段命名转换已说明
3. agentApi.ts 处理代码已提供
4. React 组件接口已更新

**可以按照文档开始实现开发**

---

## 历史记录

### ✅ 上传代码到 GitHub（2026-01-17）

**提交哈希：** 10362ae
**推送分支：** alin3.0
**状态：** ✅ 成功推送

---

## 第六轮 Review：修复 planning_examples.py 工具示例一致性（进行中）

### 待办清单

- [x] 盘点 `backend/app/services/agent/prompts/planning_examples.py` 中所有 get_writing_context 引用并记录对应示例
- [x] 将示例与说明文字统一改为 `explore_content`，同步调整流程描述（如 search_content → explore_content → locate_content）
- [x] 复核该文件确保无残留旧工具名
- [x] 在本节添加 review 总结

盘点记录：涉及 explore_content 示例说明、Agent 模式示例、编辑器工作流示例、新工具升级提示、locate_content 示例流程与说明。

### review

- 修改：`backend/app/services/agent/prompts/planning_examples.py` 全部示例与说明统一为 explore_content，并调整未指定章节的 locate_content 流程为 explore_content → locate_content → smart_rewrite → apply_chapter_edit。
- 同步：Agent 模式与编辑器工作流示例改用 explore_content + target_task 表达读取需求。
- 复核：`rg "get_writing_context"` 无匹配。

---

## 第七轮 Review：planning_examples.py 深度复核（待开始）

### 待办清单

- [x] 复查 `backend/app/services/agent/prompts/planning_examples.py` 变更片段，确认示例参数与 ref 路径一致性
- [x] 核对 locate_content 场景流程（未指定章节/跨章节/编辑器工作流）是否与工具规则一致
- [x] 验证是否引入新问题（search_content 示例、节点说明、流程描述冲突）
- [x] 必要时做最小修正并补充 review 总结

### review

- 修正：`backend/app/services/agent/prompts/planning_examples.py` 的搜索/Agent 模式示例统一改用 explore_content，避免与“统一入口”规则冲突。
- 补充：搜索示例说明文字改为“检索信息统一用 explore_content”，保持流程一致性。
- 观察：explore_content 结果字段（如 `context_for_task`、`chapters[0].id`）与文档输出格式存在潜在不一致，需与实际实现/规范统一。

---

## 第八轮 Review：explore_content 输出字段一致性（待开始）

### 待办清单

- [x] 对比 `backend/app/services/agent/tools/explore_tools.py` 的实际输出与 `docs/explore/06-output.md`、`docs/explore/08-integration.md` 的字段说明
- [x] 必要时更新文档字段（如 `context_for_task`、`explore_summary`、`frontend_display`、`chapters` 列表结构）以匹配实现
- [x] 复核 `backend/app/services/agent/prompts/planning_examples.py` 中 $ref 路径与实际输出一致
- [x] 在本节添加 review 总结

### review

- 对齐：`docs/explore/06-output.md` 补充 explore_content 实际返回格式（success/context_for_task/explore_summary/frontend_display/chapters 列表等），并更新示例/TaskRunner 说明以使用 context_for_task。
- 对齐：`docs/explore/08-integration.md` 更新 explore_content 签名与返回字段说明。
- 修正：`backend/app/services/agent/prompts/planning_examples.py` 移除不受支持的负索引 $ref。
- 同步：`docs/explore/03-state.md` 补齐 ChapterRead.id 与 ExploreRound 字段以匹配实现。

---

## 第九轮 Review：工具描述与示例收敛（待开始）

### 待办清单

- [x] 修正 `backend/app/services/agent/prompts/tool_descriptions.py` 中 explore_content 返回字段说明，与实际输出一致
- [x] 调整 `backend/app/services/agent/prompts/planning_examples.py` 中 explore_content 示例的章节引用，避免 `chapters[1]` 越界风险
- [x] 复核相关示例与工具描述无新增冲突，并补充 review 总结

### review

- 修正：`backend/app/services/agent/prompts/tool_descriptions.py` 的 explore_content 返回字段，补齐 context_for_task 与 frontend_display。
- 修正：`backend/app/services/agent/prompts/planning_examples.py` 中 explore_content 示例的 chapters 引用，避免越界。

---

## 第十轮 Review：Explore 聚合 UI 未生效（待开始）

### 待办清单

- [x] 复核 explore_content 执行链路与事件发射路径（ToolExecutor/ParallelExecutor/StreamEventHandler）
- [x] 核对前端 explore_round/explore_summary 事件消费与组件渲染路径
- [x] 最小修改保证 explore_content 保留完整 JSON 以便发射聚合事件
- [x] 复核 UI 数据字段映射，补充 review 总结

### review

- 原因定位：ToolExecutor 对 explore_content 结果做了摘要提取，ParallelExecutor 无法解析完整 JSON，导致 explore_round/explore_summary 未发射。
- 修正：`backend/app/services/agent/execution/task_runner.py` 传递 emit_explore_events 标记；`backend/app/services/agent/execution/tool_executor.py` 在该标记下返回完整 JSON。
- 验证：前端已消费 explore_round/explore_summary 并渲染 ExploreCard，无需改动 UI 组件。

---

## 第十一轮 Review：Explore 聚合链路复审（待开始）

### 待办清单

- [x] 复核本轮改动影响范围（`task_runner.py` / `tool_executor.py`），确认无副作用
- [x] 验证是否真正解决 Explore 聚合 UI 未生效问题（事件发射/数据解析链路）
- [x] 检查修改完整性（其他调用路径是否遗漏 explore_content 事件支持）
- [x] 核对逻辑一致性（后端输出字段 ↔ 前端事件映射）
- [x] 深入验证潜在遗漏点并补充 review 总结

### review

- 结论：标准 Planning 并行执行链路下，`explore_content` 返回完整 JSON → `ParallelExecutor` 可解析并发射 explore_round/explore_summary，UI 可渲染 Explore 轨迹卡片。
- 风险：`enable_reflection=True` 的 DeepAgent 分支不走 `ParallelExecutor`，现在会保留完整 JSON 作为任务结果，可能导致上下文膨胀且仍无 explore 事件。
- 遗漏：非 Planning 路径（如 `ToolDispatcher` 直呼工具）未设置 `emit_explore_events`，仍可能只显示普通工具调用而无 Explore 轨迹。

---

## 第十二轮：ToolDispatcher 路径补发 Explore 事件（待开始）

### 待办清单

- [x] 复核 ToolDispatcher 的 explore_content 调用路径与当前返回格式
- [x] 在 ToolDispatcher 中为 explore_content 设置 emit_explore_events 并触发 explore_round/explore_summary
- [x] 保持返回值为 explore_summary（避免上下文膨胀），验证不影响现有工具调用
- [x] 添加 review 总结

### review

- 新增：`backend/app/services/agent/core/tool_dispatcher.py` 在 explore_content 路径设置 emit_explore_events，解析结果并补发 explore_round/explore_summary。
- 保持：返回 explore_summary/ context_for_task，避免把完整 JSON 直接注入对话上下文。

---

## 第十三轮 Review：ToolDispatcher Explore 路径复审（待开始）

### 待办清单

- [x] 复核 ToolDispatcher 新增事件发射逻辑是否影响其他工具
- [x] 验证 explore_content 在非规划路径的 UI 表现与输出一致性
- [x] 检查返回值处理（summary/context_for_task）是否导致下游解析异常
- [x] 核对事件字段映射（FlowEventBuilder ↔ 前端解析）
- [x] 补充 review 总结

### review

- 结论：ToolDispatcher 路径已补齐 explore_round/explore_summary 事件发射，前端可复用现有 Explore 卡片渲染。
- 兼容：返回 explore_summary/context_for_task 避免上下文膨胀；异常时回退原始 tool_result。
- 注意：该路径使用固定 step_id=1；若需与 StepCard 对齐，可后续接入实际 step_id（当前不影响 Explore 卡片显示）。

---

## 第十四轮 Review：Explore 胶囊层级与布局问题（待开始）

### 待办清单

- [x] 复核 Explore 事件与 StepCard 渲染顺序/层级（`ExecutionFlow` 与 `ExploreCard` 组件）
- [x] 核对 explore_round/explore_summary 在 flow items 中的插入时机与 stepId 关联
- [x] 定位 UI 层级不一致原因并给出最小修复方案（如按 stepId 归组渲染）
- [x] 评估修复对现有 StepCard/ExploreCard 的影响与风险
- [x] 添加 review 总结

### review

- 原因：Explore 事件以独立 FlowItem 插入，`ExecutionFlow` 未按 stepId 归组，导致 Explore 胶囊与 StepCard 仅按时间序列并列渲染，无法呈现“同一层级/同一折叠块”关系。
- 关联风险：后端 explore_round 的 step_id 目前与 StepCard 的 stepId 不严格一致（并行任务 + task_id/step_counter 差异、ToolDispatcher 默认 step_id=1），导致即便前端归组也可能错位。
- 建议：前端按 stepId 归组并在 StepCard 内容区渲染 Explore 卡片；若要稳定归组需后端对齐 explore_round 的 step_id（用 step_start 生成的 step_id）。

---

## 第十五轮：Explore 步骤归组与胶囊调整（待开始）

### 待办清单

- [x] 复核 Explore 事件顺序与 stepId 映射，确定归组策略
- [x] 前端按 stepId 将 explore_round/explore_summary 归入对应 StepCard 内容区
- [x] 隐藏 explore_content 的 “调用工具” 胶囊
- [x] 评估是否需要前端顺序动画（逐个出现）并给出最小实现
- [x] 添加 review 总结

### review

- 分组：`src/components/agent/ExecutionFlow/index.tsx` 按 stepId 归组 explore_round/explore_summary，并在 StepCard 内容区渲染；无匹配的 Explore 项继续独立显示。
- 隐藏：`src/components/agent/ExecutionFlow/StepCard.tsx` 对 explore_content 不显示“调用工具”胶囊。
- 顺序：Explore 事件按流式到达顺序逐条追加，前端无需额外动画即可逐个出现；如需更强的节奏感可再加轻量 stagger 动效。

---

## 第十六轮 Review：Explore 归组后验证（待开始）

### 待办清单

- [x] 验证 Explore 归组是否影响其他 StepCard/Explore 卡片显示
- [x] 检查 explore_content 胶囊隐藏逻辑是否误伤其他工具
- [x] 复核无 stepId 的 Explore 事件是否仍可单独显示
- [x] 核对渲染顺序与重复渲染风险
- [x] 添加 review 总结

### review

- 结论：Explore 事件按 stepId 归组后，仅影响同 stepId 的 Explore 项，其他 StepCard/Explore 卡片不受影响；无 stepId 匹配仍会独立显示。
- 逻辑：explore_content 的工具胶囊仅对该工具隐藏，不影响其他工具的 StepCard 展示。
- 风险：后端 explore_round 使用 task_id 作为 step_id，若与 StepCard 的 stepId 不一致，归组可能失败导致 Explore 仍独立显示。

---

## 第十七轮：Explore 子代理流式事件与 stepId 对齐（待开始）

### 待办清单

- [x] 复核 explore_content 事件发射位置与 stepId 来源，设计流式回调传递方案
- [x] 为 explore_content 增加上下文回调（按轮次即时发 explore_round），并在结果中标记已发事件
- [x] 在 ToolExecutor/ParallelExecutor/ToolDispatcher 接入回调与 stepId 映射，避免重复发事件
- [x] 对齐 stepId（task_id → stepId 映射），确保 Explore 归组稳定
- [x] 添加 review 总结

### review
- 新增：`backend/app/services/agent/utils/tool_context.py` 提供 stream_event_handler 与 explore step_id 的上下文传递。
- 流式：`backend/app/services/agent/tools/explore_tools.py` 通过回调逐轮发送 explore_round，并输出 `events_emitted` 标记，汇总事件也在工具内发送。
- 事件：`backend/app/services/agent/execution/tool_executor.py` 使用 contextvar 注入 stream handler 与 step_id；`backend/app/services/agent/execution/parallel_executor.py` 与 `backend/app/services/agent/core/tool_dispatcher.py` 在已发事件时跳过补发，确保不重复。
- 对齐：`backend/app/services/agent/langgraph_agent.py` 写入任务 step_id，`backend/app/services/agent/execution/parallel_executor.py` 以 step_id 发事件并注入 state，Explore 卡片可归组到 StepCard。

---

## 第十八轮：Explore 事件稳健性与 stepId 隔离（待开始）

### 待办清单

- [x] 复核 explore_content 事件发射条件，避免 events_emitted 误判导致缺失卡片
- [x] 调整 events_emitted 判定逻辑（以实际成功发射为准）
- [x] 移除对任务对象的 _step_id 直接写入，改用内部映射传递
- [x] 贯通 Planning/DeepAgent/ToolDispatcher 路径，确保 stepId 一致且不外泄
- [x] 添加 review 总结

### review
- 修复：`backend/app/services/agent/stream/stream_event_handler.py` 提供回调检测与发射成功返回值，避免仅凭 handler 存在就标记发射成功。
- 修复：`backend/app/services/agent/tools/explore_tools.py` 仅在回调可用时启用发射，并以实际发射结果更新 `events_emitted`。
- 收敛：`backend/app/services/agent/langgraph_agent.py` 不再写入任务 `_step_id`，改用内部映射传递；标准/DeepAgent 路径共享 stepId 映射。
- 对齐：`backend/app/services/agent/execution/parallel_executor.py` 改用 `task_step_map` 获取 stepId，避免对任务对象的侵入式字段。

---

## 第十九轮：Explore next_tool 不显示（待开始）

### 待办清单

- [x] 复核 explore_summary 与前端展示的 next_tool 使用位置
- [x] 移除/置空 explore_tools.py 中 next_tool 字段，避免卡片显示固定 smart_continue
- [x] 复核 explore_summary 事件与 frontend_display 保持一致
- [x] 添加 review 总结

### review
- 修正：`backend/app/services/agent/tools/explore_tools.py` 移除 explore_summary 与前端展示中的 `next_tool` 字段，避免固定显示 smart_continue。

---

## 第二十轮：Explore Review 标签去重（待开始）

### 待办清单

- [x] 定位 Review 重复渲染来源（toolCalls 中包含 Review + reviewStatus 额外渲染）
- [x] 调整 ExploreRoundCard 渲染逻辑：当 toolCalls 含 Review 时，不重复显示 reviewStatus
- [x] 复核 LegacyRoundCard 与 ExploreRoundCard 视觉一致性
- [x] 添加 review 总结

### review
- 修复：`src/components/agent/ExecutionFlow/ExploreCard.tsx` 当 toolCalls 已包含 Review 标签时不再额外渲染 reviewStatus，避免重复显示。

---

## 第二十一轮：ExploreSummary next_tool 参数修复（待开始）

### 待办清单

- [x] 复核 explore_summary 事件构造是否缺失 next_tool 导致工具失败
- [x] 在 explore_tools.py 传入空字符串 next_tool，前端保持不显示
- [x] 复核日志与错误链路，确认不再触发 tool_failed
- [x] 添加 review 总结

### review
- 修复：`backend/app/services/agent/tools/explore_tools.py` 在 explore_summary 事件中传入 `next_tool=""`，满足后端参数要求且前端不展示。

---

## 第二十二轮 Review：Explore 聚合工具是否为子代理（待开始）

### 待办清单

- [x] 复核 Explore 聚合工具实现与定位文档（explore_tools.py、docs/explore/01-overview.md、docs/Agent 架构的探索.md）
- [x] 对照子代理定义（上下文隔离、并行、专用工具、Token 效率）评估 Explore 定位
- [x] 输出 review 结论与风险点（含文件与行号）
- [x] 添加 review 总结

### review
- 结论：Explore 当前是"工具内循环的 mini-agent/聚合工具"，并不满足子代理定义中的上下文隔离、并行、专用工具与 Token 效率等关键特征。
- 风险：若按子代理预期使用，可能误判能力边界（上下文仍被主 Agent 污染、无并行分工、返回内容反而放大上下文）。

---

## Explore SubAgent 升级计划（2026-01-18）

### 一、设计决策总结

| 问题 | 决策 |
|------|------|
| **Q1 触发方式** | 方案 A：仍作为工具，内部有 ReAct 循环 |
| **Q2 可用工具** | 3 个：search_content、get_writing_context、read_paragraph |
| **Q3 停止条件** | 完全由 AI 决定（不设硬性上限） |
| **Q4 任务理解** | Explore 自己扩展，不改 Planning prompt |
| **长期目标** | 先 A 验证效果，再演进到 B（Planning + SubAgents 架构） |

### 二、当前问题

Explore 当前是**伪 subagent（规则驱动的状态机）**：

| 决策点 | 当前实现 | 目标实现 |
|--------|----------|----------|
| 搜索词生成 | 关键词提取规则 | AI 理解任务，生成语义查询 |
| 章节选择 | 从证据中提取章节号 | AI 判断哪些章节最相关 |
| 充足判断 | 5条证据+1章节+3轮上限 | AI 评估覆盖度 |
| 停止条件 | 固定3轮 | AI 判断可以停止 |

### 三、实现计划

#### Phase 1：注入 AI 决策点

- [ ] 1.1 添加 `_ai_understand_task()` - 第0步理解任务
- [ ] 1.2 添加 `_ai_plan_round()` - 每轮 AI 决定搜索策略
- [ ] 1.3 添加 `_ai_assess_sufficiency()` - AI 判断信息充足性
- [ ] 1.4 移除硬编码规则（`_generate_search_queries`、`_evaluate_sufficiency`）

#### Phase 2：启用 read_paragraph 工具

- [ ] 2.1 在 ReAct 循环中支持 read_paragraph 调用
- [ ] 2.2 AI 决定何时用 read_paragraph vs get_writing_context

#### Phase 3：测试验证

- [ ] 3.1 单元测试：AI 决策质量
- [ ] 3.2 集成测试：端到端探索效果
- [ ] 3.3 成本评估：token 消耗对比

### 四、核心代码改动

**文件**：`backend/app/services/agent/tools/explore_tools.py`

```python
class ContentExplorer:
    def __init__(self, ..., ai_service: HTTPAIService):
        self.ai_service = ai_service  # 注入 AI 服务

    async def explore(self) -> ExploreResult:
        # 第0步：AI 理解任务
        exploration_plan = await self._ai_understand_task()

        for round_idx in range(1, self.max_rounds + 1):
            # AI 决定本轮策略
            plan = await self._ai_plan_round(round_idx, exploration_plan)

            # 执行工具调用
            for query in plan.search_queries:
                await self._do_search(query)
            for chapter_order in plan.chapters_to_read:
                await self._read_chapter(chapter_order)
            for para in plan.paragraphs_to_read:
                await self._read_paragraph(para)

            # AI 评估是否充足
            assessment = await self._ai_assess_sufficiency()
            if assessment.sufficient:
                break

        return self._build_result()
```

### 五、AI Prompt 设计

#### 5.1 任务理解 Prompt

```
目标任务：{target_task}

请分析这个任务需要收集哪些信息：
1. 关键实体（人物、地点、物品等）
2. 需要了解的方面（关系、事件、状态等）
3. 建议的初始搜索策略

输出 JSON：
{
  "key_entities": ["主角", "师傅"],
  "aspects_to_find": ["初遇场景", "传授功法", "当前关系"],
  "initial_queries": ["主角 师傅 初遇", "师傅 传授 功法"],
  "understanding": "用户想续写，需要了解师徒关系的发展脉络"
}
```

#### 5.2 轮次规划 Prompt

```
目标任务：{target_task}
任务理解：{exploration_plan.understanding}
当前轮次：{round_idx}
已收集信息：
- 证据 {n} 条：{evidence_summary}
- 章节 {chapters}
- 世界观 {worldview_categories}

请决定本轮行动：
1. 需要搜索什么？（基于已收集信息，避免重复）
2. 需要读取哪些章节？
3. 需要精确读取哪些段落？

输出 JSON：
{
  "search_queries": ["..."],
  "chapters_to_read": [3, 5],
  "paragraphs_to_read": [{"chapter": 3, "paragraph": 15}],
  "reason": "需要补充..."
}
```

#### 5.3 充足性判断 Prompt

```
目标任务：{target_task}
任务理解：{exploration_plan.understanding}
需要了解的方面：{aspects_to_find}

已收集信息：
- 证据 {n} 条，覆盖章节：{chapters_in_evidences}
- 完整章节：{chapters_read}
- 世界观条目：{worldview_count}

问题：
1. 信息是否足够完成目标任务？
2. 还缺少什么关键信息？

输出 JSON：
{
  "sufficient": true/false,
  "coverage": "已覆盖初遇、传授，缺少当前状态",
  "missing": ["当前关系状态"]
}
```

### 六、预期效果

```
用户请求：续写第6章，需要了解主角与师傅的关系

【Explore 内部】

第0步 - 任务理解：
  理解：用户想续写，需要了解师徒关系发展
  关键实体：主角、师傅
  需要了解：初遇、传授、当前状态

第1轮：
  AI 决定：搜索"主角 师傅 初遇"
  结果：找到第2章、第3章相关内容
  AI 评估：找到初遇，缺少传授和当前状态

第2轮：
  AI 决定：搜索"师傅 传授 功法"，读取第3章
  结果：第3章有完整传授场景
  AI 评估：有初遇+传授，缺少当前状态

第3轮：
  AI 决定：读取第5章（最近章节）
  结果：第5章末师傅离开
  AI 评估：✅ 信息充足，停止探索

【输出】
chapters: [3, 5]
evidences: 8条
analysis: 师徒关系发展：初遇→传授→分离
```

### 七、待确认

- [x] 确认 HTTPAIService 注入方式 → 使用懒初始化单例
- [x] 确认 AI 调用的 task_type 参数 → DEEP_ANALYSIS / SIMPLE_QA / QUALITY_EVALUATION
- [x] 确认 token 预算限制（如有）→ 无硬性限制，AI 自主决定停止

---

### 八、实现完成（2026-01-18）

**状态：✅ 已完成**

#### 8.1 代码改动

| 文件 | 改动类型 | 说明 |
|------|----------|------|
| `explore_tools.py` | 重构 | AI 驱动的 SubAgent 模式 |

#### 8.2 新增组件

| 组件 | 说明 |
|------|------|
| `_get_ai_service()` | 懒初始化 AI 服务 |
| `ExplorationPlan` | AI 任务理解结果 |
| `RoundPlan` | AI 轮次规划结果 |
| `SufficiencyAssessment` | AI 充足性评估结果 |
| `_ai_understand_task()` | 第0步：AI 理解任务（DEEP_ANALYSIS） |
| `_ai_plan_round()` | 每轮：AI 决定搜索策略（SIMPLE_QA） |
| `_ai_assess_sufficiency()` | 每轮：AI 判断是否充足（QUALITY_EVALUATION） |
| `_execute_round_with_plan()` | 根据 AI 计划执行探索 |
| `_build_collected_summary()` | 构建已收集信息摘要 |
| `_parse_json_response()` | 解析 AI 返回的 JSON（支持嵌套） |
| `_normalize_json_types()` | 规范化 JSON 类型 |

---

### 九、深度 Review（2026-01-18）

#### 9.1 发现的问题及修复

| 问题 | 严重程度 | 状态 | 修复方案 |
|------|----------|------|----------|
| JSON 解析不支持嵌套 | 🔴 高 | ✅ 已修复 | 改用 `find('{')` 和 `rfind('}')` |
| sufficient 字段类型不安全 | 🟡 中 | ✅ 已修复 | 添加 `_normalize_json_types()` |
| initial_queries 未使用 | 🟡 中 | ✅ 已修复 | 首轮兜底和 prompt 中使用 |
| paragraphs_to_read 未实现 | 🟡 中 | ✅ 已修复 | 添加 read_paragraph 调用 |
| 首轮兜底未用 initial_queries | 🟡 中 | ✅ 已修复 | 优先使用 exploration_plan |

#### 9.2 验证清单

| 检查项 | 结果 |
|--------|------|
| 是否引入新问题？ | ✅ 已修复所有发现的问题 |
| 是否解决原问题？ | ✅ 规则驱动 → AI 驱动 |
| 修改完整性？ | ✅ 所有 AI 决策点已实现 |
| 逻辑一致性？ | ✅ 设计与实现一致 |
| 语法检查？ | ✅ 通过 |

#### 9.3 核心流程

```
explore()
  │
  ├── AI 理解任务 (_ai_understand_task)
  │   └── 返回：key_entities, aspects_to_find, initial_queries, understanding
  │
  └── for 每轮:
        │
        ├── AI 规划本轮 (_ai_plan_round)
        │   └── 参考 initial_queries（首轮）
        │   └── 返回：search_queries, chapters_to_read, paragraphs_to_read, reason
        │
        ├── 执行计划 (_execute_round_with_plan)
        │   ├── 获取世界观（首轮）
        │   ├── 执行搜索
        │   ├── 读取章节
        │   ├── 读取段落（新增）
        │   └── 兜底：从证据提取章节
        │
        └── AI 评估充足性 (_ai_assess_sufficiency)
            └── sufficient? → 停止
```

---

### 十、下一步

- [ ] 实际测试验证效果
- [ ] 观察 AI 决策质量
- [ ] 评估 token 消耗

---

## 第二十三轮 Review：代码一致性深度验证（2026-01-18）

### 一、Review 触发

**问题来源**：Backend.md 日志显示运行时错误：
```
FlowEventBuilder.explore_summary() missing 1 required positional argument: 'next_tool'
```

### 二、验证发现

#### 2.1 代码文件检查

| 文件 | 检查项 | 结果 |
|------|--------|------|
| `explore_tools.py:1443` | `_emit_summary_event` 调用 | ✅ 传入了 `next_tool=""` |
| `explore_tools.py:500-509` | `to_frontend_display` ai_analysis | ❌ 缺少 `next_tool` 字段 |
| `flow_events.py:315-322` | `explore_summary` 签名 | ✅ 有 `@staticmethod` |
| `parallel_executor.py:737` | 调用 explore_summary | ✅ 使用 `.get("next_tool", "")` |
| `tool_dispatcher.py:811` | 调用 explore_summary | ✅ 使用 `.get("next_tool", "")` |

#### 2.2 根因分析

**日志错误与代码不一致**：
- 代码文件中 `_emit_summary_event` 确实传入了 `next_tool=""`
- 但运行时抛出 `missing 1 required positional argument: 'next_tool'`

**结论**：服务器运行的是旧版本代码，需要**重启后端服务**。

### 三、修复内容

| 问题 | 修复 |
|------|------|
| `to_frontend_display` 缺少 `next_tool` | 添加 `"next_tool": ""` 字段（行 503） |

### 四、验证清单

| 检查项 | 结果 |
|--------|------|
| 是否引入新问题？ | ✅ 否 |
| 是否真正解决原问题？ | ✅ 规则驱动 → AI 驱动 |
| 修改完整性？ | ✅ 所有 AI 决策点已实现 |
| 逻辑一致性？ | ✅ 设计与实现一致 |
| 语法检查？ | ✅ 通过 |
| 数据结构一致性？ | ✅ 已修复 `to_frontend_display` |

### 五、待用户操作

**⚠️ 重要：请重启后端服务器，确保加载最新代码。**

```bash
# 重启后端服务
# 方式一：直接重启 Python 进程
# 方式二：使用 uvicorn --reload 开发模式
```

### 六、AI 驱动验证点

| 组件 | 状态 |
|------|------|
| `_ai_understand_task()` | ✅ 使用 DEEP_ANALYSIS TaskType |
| `_ai_plan_round()` | ✅ 使用 SIMPLE_QA TaskType |
| `_ai_assess_sufficiency()` | ✅ 使用 QUALITY_EVALUATION TaskType |
| `HTTPAIService.call_ai()` | ✅ 签名匹配 |
| `read_paragraph` 工具 | ✅ 存在于 langgraph_tools.py |

---

## 将代码上传到GitHub（2026-01-19）

### 待办清单

- [ ] 查看当前修改的文件详情
- [ ] 暂存所有修改的文件
- [ ] 创建提交（包含本次修改的描述）
- [ ] 推送到远程仓库 origin/alin3.0
- [ ] 验证推送成功

### 当前状态

**分支**：alin3.0
**远程仓库**：https://github.com/alin776/ai_writer.git

**修改的文件**：
- Backend.md
- INFO.md
- backend/app/services/agent/execution/tool_executor.py
- backend/app/services/agent/prompts/tool_descriptions.py
- backend/app/services/agent/tools/explore_tools.py
- src/components/agent/ExecutionFlow/ExploreCard.tsx
- todo.md

### 预期结果

所有修改成功推送到GitHub远程仓库的alin3.0分支。

---
