# Explore 前端 UI 设计规范

> 本文档基于 `agent-writing-preview - 副本 (2).html` 设计稿，确保实现一比一复刻。

## 1. 整体布局结构

### 1.1 作为执行步骤呈现

Explore 轨迹作为 `execution-step` 的一部分，与其他步骤（获取世界观、读取章节等）保持一致的外观。

```
execution-step
├── step-header
│   ├── step-icon.completed (✓ 图标)
│   ├── step-title-area
│   │   ├── step-title ("Explore 轨迹（N 轮）")
│   │   └── step-toggle (∧/∨)
│   └── step-spacer
└── step-content
    ├── explore-panel (探索面板)
    │   ├── explore-round (轮次1)
    │   ├── explore-round (轮次2)
    │   └── explore-round (轮次N)
    ├── step-description (描述文本)
    ├── AI 分析与规划 (knowledge-section)
    └── tool-operation (工具调用标签)
```

### 1.2 步骤标题格式

```
Explore 轨迹（{total_rounds} 轮）
```

示例：`Explore 轨迹（3 轮）`

---

## 2. explore-round 轮次组件

### 2.1 组件结构

```html
<div class="explore-round">
    <div class="explore-round-capsule collapsed">
        <div class="explore-round-header compact" onclick="toggleExploreRound(this)">
            <div class="explore-round-index">
                <i data-lucide="scan" style="width:12px;height:12px"></i>
            </div>
            <div class="explore-round-title compact">{轮次标题}</div>
            <span class="explore-round-toggle">∧</span>
        </div>
        <div class="explore-round-body hidden">
            <!-- 展开后的内容 -->
        </div>
    </div>
</div>
```

### 2.2 轮次标题命名规范

| 轮次 | 标题示例 | 说明 |
|------|----------|------|
| 第1轮 | "初次检索与定位" | 首轮信息收集 |
| 第2轮 | "补漏检索与二次定位" | 补充缺失信息 |
| 第3轮 | "交叉验证与收敛" | 最终验证 |
| 通用 | "深度探索（第N轮）" | 默认格式 |

### 2.3 折叠/展开状态

**折叠状态（默认）**：
- 类名：`.explore-round-capsule.collapsed`
- 显示：图标 + 轮次标题
- body 隐藏：`.explore-round-body.hidden`

**展开状态**：
- 类名：`.explore-round-capsule`（移除 collapsed）
- 显示：完整内容
- body 显示：移除 `.hidden`

### 2.4 CSS 样式规范

```css
.explore-panel {
    margin: 8px 0;
}

.explore-round {
    display: flex;
    gap: 10px;
    padding: 8px 0;
    align-items: flex-start;
}

.explore-round-capsule {
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 16px;
    padding: 6px 10px;
    width: auto;
    align-self: flex-start;
    display: inline-flex;
    flex-direction: column;
    max-width: 100%;
}

.explore-round-capsule.collapsed {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    width: auto;
    padding: 4px 10px;
    border-radius: 16px;
    flex-direction: row;
    max-width: 100%;
}

.explore-round-index {
    color: #888;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 500;
}

.explore-round-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: #888;
    margin-bottom: 0;
}

.explore-round-toggle {
    font-size: 10px;
    color: #666;
    margin-left: auto;
}

.explore-round-body {
    flex: 1;
    width: fit-content;
    max-width: 100%;
}
```

---

## 3. explore-tags 工具标签

### 3.1 组件结构

```html
<div class="explore-tags">
    <span class="explore-tag">
        <i data-lucide="search" style="width:12px;height:12px"></i>
        Search: <span class="tag-strong">{搜索关键词}</span>
    </span>
    <span class="explore-tag">
        <i data-lucide="crosshair" style="width:12px;height:12px"></i>
        Locate: 第{chapter}章 · 第{para}段
    </span>
    <span class="explore-tag">
        <i data-lucide="file-text" style="width:12px;height:12px"></i>
        ReadRaw: 第{chapter}章
    </span>
    <span class="explore-tag">
        <i data-lucide="check-circle" style="width:12px;height:12px"></i>
        Review: {状态}
    </span>
</div>
```

### 3.2 工具类型与图标映射

| 工具类型 | Lucide 图标 | 标签前缀 | 值格式 |
|----------|-------------|----------|--------|
| 搜索 | `search` | `Search:` | 搜索关键词（高亮） |
| 定位 | `crosshair` | `Locate:` | `第N章 · 第M段` |
| 读取原文 | `file-text` | `ReadRaw:` | `第N章` |
| 审查 | `check-circle` | `Review:` | 状态文本 |

### 3.3 Review 状态值

| 状态 | 显示文本 | 说明 |
|------|----------|------|
| 覆盖不足 | "覆盖不足" | 需要继续探索 |
| 补齐要点 | "补齐要点" | 补充后达标 |
| 通过 | "通过" | 信息充足 |

### 3.4 CSS 样式规范

```css
.explore-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    width: fit-content;
    max-width: 100%;
}

.explore-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 16px;
    padding: 4px 10px;
    font-size: 12px;
    color: #888;
}

.explore-tag i {
    color: #888;
}

.explore-tag .tag-strong {
    color: #5c9eff;
    font-weight: 500;
}
```

---

## 4. explore-status 状态显示

### 4.1 组件结构

```html
<div class="explore-status">
    <span class="hit">命中 {count} 条</span>
    <!-- 以下两者根据情况显示其一 -->
    <span class="warn">缺少：{missing_item}</span>  <!-- 黄色，有缺失项时 -->
    <span>{status_text}</span>                      <!-- 灰色，无缺失项时 -->
</div>
```

### 4.2 状态类型

| 类型 | 类名 | 颜色 | 条件 | 示例 |
|------|------|------|------|------|
| 命中 | `.hit` | `#10b981` (绿色) | 始终显示 | "命中 4 条" |
| 警告 | `.warn` | `#f59e0b` (黄色) | `missing_items.length > 0` | "缺少：浑圆桩训练" |
| 普通 | 无 | `#777` (灰色) | `missing_items.length === 0` | "补漏完成" / "覆盖度达标" |

### 4.3 状态文本规范

| review_status | status_text | 说明 |
|---------------|-------------|------|
| "覆盖不足" | - | 显示 warn，不显示 status_text |
| "补齐要点" | "补漏完成" | 第二轮补漏后 |
| "通过" | "覆盖度达标" | 最终验证通过 |

### 4.4 前端渲染逻辑

```tsx
<div className="explore-status">
  <span className="hit">命中 {hitCount} 条</span>
  {missingItems.length > 0 ? (
    <span className="warn">缺少：{missingItems.join('、')}</span>
  ) : statusText ? (
    <span>{statusText}</span>
  ) : null}
</div>
```

### 4.5 CSS 样式规范

```css
.explore-status {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 6px;
    font-size: 11px;
    color: #777;
    width: fit-content;
    max-width: 100%;
}

.explore-status .hit {
    color: #10b981;
}

.explore-status .warn {
    color: #f59e0b;
}
```

---

## 5. explore-evidence 证据片段

### 5.1 组件结构

```html
<div class="explore-evidence">
    <div class="explore-evidence-header" onclick="toggleExplore(this)">
        <span class="explore-evidence-title">证据片段（{count}）</span>
        <span class="explore-evidence-toggle">∧</span>
    </div>
    <div class="explore-items">
        <div class="explore-item">
            <div class="meta">第{chapter}章 · 第{para}段</div>
            {文本内容}
        </div>
        <!-- 更多证据项 -->
    </div>
</div>
```

### 5.2 CSS 样式规范

```css
.explore-evidence {
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    border-radius: 16px;
    padding: 4px 10px;
    margin-top: 6px;
    font-size: 12px;
    color: #888;
    width: fit-content;
    max-width: 100%;
}

.explore-evidence strong {
    color: #bdbdbd;
}

.explore-evidence-header {
    display: flex;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    user-select: none;
}

.explore-evidence-title {
    font-size: 11px;
    color: #888;
}

.explore-evidence-toggle {
    font-size: 9px;
    color: #666;
}

.explore-items {
    padding-top: 4px;
}

.explore-item {
    padding: 2px 0;
    border-top: 1px dashed #2a2a2a;
}

.explore-item:first-child {
    border-top: none;
}

.explore-item .meta {
    font-size: 10px;
    color: #6f6f6f;
}
```

---

## 6. AI 分析与规划卡片

### 6.1 组件结构

```html
<div class="knowledge-section" style="margin-top: 12px;">
    <div style="background: #2a2a2a; border: 1px solid #3a3a3a; border-radius: 16px; padding: 4px 10px; display: inline-block; max-width: 100%;">
        <!-- Header -->
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px; cursor: pointer;" onclick="toggleAINarrative(this)">
            <span style="color: #888;"><i data-lucide="brain" style="width:12px;height:12px"></i></span>
            <span style="font-size: 13px; color: #fff; font-weight: 500;">AI 分析与规划</span>
            <span class="narrative-toggle" style="font-size: 9px; color: #666; margin-left: auto;">∧</span>
        </div>

        <!-- Content -->
        <div class="narrative-content">
            <!-- 探索总结 -->
            <div style="margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                    <span style="color: #888;"><i data-lucide="file-search" style="width:12px;height:12px"></i></span>
                    <span style="font-size: 12px; color: #888; font-weight: 500;">探索总结</span>
                </div>
                <div style="font-size: 12px; color: #999; line-height: 1.7; padding-left: 18px;">
                    {探索总结内容}
                </div>
            </div>

            <!-- 下一步行动 -->
            <div style="margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                    <span style="color: #888;"><i data-lucide="arrow-right-circle" style="width:12px;height:12px"></i></span>
                    <span style="font-size: 12px; color: #888; font-weight: 500;">下一步行动</span>
                </div>
                <div style="font-size: 12px; color: #999; line-height: 1.7; padding-left: 18px;">
                    {下一步行动描述，工具名使用 <span style="color: #5c9eff; font-family: monospace;">smart_continue</span> 高亮}
                </div>
            </div>

            <!-- 统计数据 -->
            <div style="display: flex; gap: 8px; flex-wrap: wrap; padding-left: 18px;">
                {统计标签}
            </div>
        </div>
    </div>
</div>
```

### 6.2 统计标签结构

```html
<div style="display: flex; align-items: center; gap: 4px; padding: 2px 6px; background: #222; border-radius: 4px; font-size: 11px;">
    <i data-lucide="{icon}" style="width:11px;height:11px;color:#666"></i>
    <span style="color: #666;">{label}</span>
    <span style="color: #5c9eff; font-weight: 500;">{value}</span>
</div>
```

### 6.3 统计标签类型

| 标签 | 图标 | 标签文本 | 值格式 | 值颜色 |
|------|------|----------|--------|--------|
| 世界观 | `book-open` | "世界观" | 数字 | `#5c9eff` |
| 章节 | `file-text` | "章节" | 范围如 "1-4" | `#5c9eff` |
| 证据 | `layers` | "证据" | 数字 | `#5c9eff` |
| 覆盖度 | `check-circle` | "覆盖度" | 百分比如 "95%" | `#10b981` |

---

## 7. 完整的 explore-round-body 结构

```html
<div class="explore-round-body">
    <!-- 1. 工具标签 -->
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

    <!-- 2. 状态信息 -->
    <div class="explore-status">
        <span class="hit">命中 4 条</span>
        <span class="warn">缺少：浑圆桩训练</span>
    </div>

    <!-- 3. 证据片段 -->
    <div class="explore-evidence">
        <div class="explore-evidence-header" onclick="toggleExplore(this)">
            <span class="explore-evidence-title">证据片段（4）</span>
            <span class="explore-evidence-toggle">∧</span>
        </div>
        <div class="explore-items">
            <div class="explore-item">
                <div class="meta">第5章 · 第7段</div>
                赵穆的那柄刀，只有他一个人用过，吞噬效果也只有一条……
            </div>
            <div class="explore-item">
                <div class="meta">第5章 · 第9段</div>
                器灵吞噬后，刀身泛起一道寒芒……
            </div>
        </div>
    </div>
</div>
```

---

## 8. 交互行为

### 8.1 toggleExploreRound - 轮次折叠/展开

```javascript
function toggleExploreRound(header) {
    const body = header.parentElement.querySelector('.explore-round-body');
    const toggle = header.querySelector('.explore-round-toggle');
    const capsule = header.parentElement;
    const title = header.querySelector('.explore-round-title');

    if (body.classList.contains('hidden')) {
        // 展开
        body.classList.remove('hidden');
        toggle.textContent = '∧';
        capsule.classList.remove('collapsed');
        header.classList.remove('compact');
        title.classList.remove('compact');
    } else {
        // 折叠
        body.classList.add('hidden');
        toggle.textContent = '∨';
        capsule.classList.add('collapsed');
        header.classList.add('compact');
        title.classList.add('compact');
    }
}
```

### 8.2 toggleExplore - 证据片段折叠/展开

```javascript
function toggleExplore(header) {
    const items = header.parentElement.querySelector('.explore-items');
    const toggle = header.querySelector('.explore-evidence-toggle');

    if (items.classList.contains('hidden')) {
        items.classList.remove('hidden');
        toggle.textContent = '∧';
    } else {
        items.classList.add('hidden');
        toggle.textContent = '∨';
    }
}
```

### 8.3 toggleAINarrative - AI 分析折叠/展开

```javascript
function toggleAINarrative(header) {
    const content = header.nextElementSibling;
    const toggle = header.querySelector('.narrative-toggle');
    const title = header.querySelector('span:nth-child(2)');

    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        toggle.textContent = '∧';
        header.style.marginBottom = '10px';
        title.style.color = '#fff';
        title.style.fontWeight = '500';
    } else {
        content.classList.add('hidden');
        toggle.textContent = '∨';
        header.style.marginBottom = '0';
        title.style.color = '#888';
        title.style.fontWeight = 'normal';
    }
}
```

---

## 9. 颜色规范汇总

| 用途 | 颜色代码 | 示例 |
|------|----------|------|
| 背景色（深） | `#1e1e1e` | body 背景 |
| 背景色（胶囊） | `#2a2a2a` | 各种胶囊容器 |
| 背景色（标签内） | `#222` | 统计标签背景 |
| 边框色 | `#3a3a3a` | 胶囊边框 |
| 主文字色 | `#e0e0e0` | 正文 |
| 标题色 | `#fff` | 标题文字 |
| 次要文字 | `#888` | 标签、图标 |
| 辅助文字 | `#666` | toggle 按钮 |
| 高亮色（蓝） | `#5c9eff` | 关键词、链接 |
| 成功色（绿） | `#10b981` | 命中、覆盖度 |
| 警告色（黄） | `#f59e0b` | 缺失警告 |

---

## 10. 图标规范汇总

| 用途 | Lucide 图标名 | 尺寸 |
|------|---------------|------|
| 轮次标识 | `scan` | 12x12 |
| 搜索 | `search` | 12x12 |
| 定位 | `crosshair` | 12x12 |
| 读取原文 | `file-text` | 12x12 |
| 审查 | `check-circle` | 12x12 |
| AI 分析 | `brain` | 12x12 |
| 探索总结 | `file-search` | 12x12 |
| 下一步 | `arrow-right-circle` | 12x12 |
| 世界观 | `book-open` | 11x11 |
| 章节 | `file-text` | 11x11 |
| 证据 | `layers` | 11x11 |
| 覆盖度 | `check-circle` | 11x11 |

---

## 11. React 组件接口设计

### 11.1 ExplorePanel 组件

```typescript
interface ExploreRoundData {
  roundIdx: number;
  title: string;
  toolCalls: ToolCallTag[];
  hitCount: number;
  missingItems: string[];
  statusText: string;        // 新增：状态文本（灰色，如"补漏完成"）
  evidences: EvidenceItem[];
  reviewStatus: string;      // "覆盖不足" | "补齐要点" | "通过"
  status: 'running' | 'done';
}

interface ToolCallTag {
  type: 'Search' | 'Locate' | 'ReadRaw' | 'Review';
  value: string;
  highlight?: string;  // Search 类型的高亮关键词
}

interface EvidenceItem {
  chapter: number;
  paragraph: number;
  text: string;
}

interface AIAnalysis {
  summary: string;
  nextAction: string;
  nextTool?: string;
  stats: {
    worldview: number;
    chapters: string;  // "1-4"
    evidences: number;
    coverage: string;  // "95%"
  };
}

interface ExplorePanelProps {
  rounds: ExploreRoundData[];
  aiAnalysis: AIAnalysis;
  totalRounds: number;
  stepDescription: string;
  toolOperation: {
    icon: string;
    name: string;
  };
}
```

### 11.2 使用示例

```tsx
<ExplorePanel
  rounds={[
    {
      roundIdx: 1,
      title: "初次检索与定位",
      toolCalls: [
        { type: 'Search', value: '吞噬器灵 羚羊献食', highlight: '吞噬器灵 羚羊献食' },
        { type: 'Locate', value: '第5章 · 第7段' },
        { type: 'ReadRaw', value: '第5章' },
        { type: 'Review', value: '覆盖不足' }
      ],
      hitCount: 4,
      missingItems: ['浑圆桩训练'],
      statusText: '',  // 有缺失项时为空
      evidences: [
        { chapter: 5, paragraph: 7, text: '赵穆的那柄刀...' },
        { chapter: 5, paragraph: 9, text: '器灵吞噬后...' }
      ],
      reviewStatus: '覆盖不足',
      status: 'done'
    },
    {
      roundIdx: 2,
      title: "补漏检索与二次定位",
      toolCalls: [
        { type: 'Search', value: '浑圆桩 训练', highlight: '浑圆桩 训练' },
        { type: 'Locate', value: '第2章 · 第12段' },
        { type: 'ReadRaw', value: '第2章' },
        { type: 'Review', value: '补齐要点' }
      ],
      hitCount: 5,
      missingItems: [],  // 无缺失项
      statusText: '补漏完成',  // 显示状态文本
      evidences: [...],
      reviewStatus: '补齐要点',
      status: 'done'
    },
    {
      roundIdx: 3,
      title: "交叉验证与收敛",
      toolCalls: [...],
      hitCount: 3,
      missingItems: [],
      statusText: '覆盖度达标',  // 最终状态
      evidences: [...],
      reviewStatus: '通过',
      status: 'done'
    }
  ]}
  aiAnalysis={{
    summary: "经过3轮深度探索，我收集到续写第5章所需的完整背景信息...",
    nextAction: "基于这些背景信息，我将执行续写第5章...",
    nextTool: "smart_continue",
    stats: {
      worldview: 5,
      chapters: "1-4",
      evidences: 13,
      coverage: "95%"
    }
  }}
  totalRounds={3}
  stepDescription="多轮检索-定位-原文读取，逐轮 review 覆盖度，补漏后输出完整证据链。"
  toolOperation={{
    icon: "Scan",
    name: "explore_content (max_rounds: 3)"
  }}
/>
```
