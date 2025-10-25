# 成本监控前端对接实施计划

## 项目概述

**目标**: 将后端 AI 日志统计 API 对接到前端成本监控页面
**优先级**: P0 (本周完成)
**预计时间**: 3.5 小时
**负责人**: 待分配
**开始日期**: 2025-10-25
**状态**: 计划中

---

## 背景说明

### 后端已完成
- AI 日志数据库表 (ai_call_logs) - 2025-10-24 完成
- 6个完整的 API 端点 (用户统计/管理员统计/成本指标)
- 日志记录中间件 (自动记录每次 AI 调用)
- 统计服务 (AILogService) - 异步化重构完成
- 测试验证通过 (100% 成功率)

### 前端现状
- AdminCostView 页面存在,但使用 Mock 数据
- 当前显示功能开发中占位符 (isFeatureAvailable = false)
- UI 组件已完整 (图表/卡片/表格)

### 可用的后端 API

| API 端点 | 方法 | 功能 | 状态 |
|---------|------|------|------|
| /api/v1/ai-logs/me | GET | 获取当前用户日志列表 (分页) | 已完成 |
| /api/v1/ai-logs/me/stats | GET | 获取当前用户统计 | 已完成 |
| /api/v1/ai-logs/admin/stats | GET | 获取全局统计 (管理员) | 已完成 |
| /api/v1/ai-logs/admin/cost-metrics | GET | 获取成本指标 (管理员) | 已完成 |
| /api/v1/ai-logs/admin/user/{id}/logs | GET | 获取指定用户日志 (管理员) | 已完成 |
| /api/v1/ai-logs/admin/user/{id}/stats | GET | 获取指定用户统计 (管理员) | 已完成 |

---

## 实施步骤

### Step 1: 创建汇率工具函数 (15分钟)

**文件**: src/utils/currency.ts (新建)

**任务清单**:
- [ ] 创建 currency.ts 工具文件
- [ ] 定义汇率常量 USD_TO_CNY_RATE = 7.19 (基于 2025-01-10 官方汇率)
- [ ] 实现 formatUsdToCny(usd, decimals) - 美元转人民币并格式化
- [ ] 实现 usdToCny(usd) - 美元转人民币 (不格式化)
- [ ] 实现 formatCostDual(usd) - 同时显示美元和人民币
- [ ] 添加 JSDoc 注释

---

### Step 2: 定义 TypeScript 类型 (15分钟)

**文件**: src/types/index.ts

**任务清单**:
- [ ] 添加 AICallLog 接口 (单条日志)
- [ ] 添加 AICallLogPaginatedResponse 接口 (分页响应)
- [ ] 添加 AICallLogStats 接口 (统计数据)
- [ ] 添加 CostMetrics 接口 (成本指标) - 重点

---

### Step 3: DataService 添加方法 (20分钟)

**文件**: src/services/DataService.ts

**任务清单**:
- [ ] 在文件末尾添加 AI 日志相关方法注释分隔符
- [ ] 实现 getMyAILogs(params) - 当前用户日志列表
- [ ] 实现 getMyAIStats(days) - 当前用户统计
- [ ] 实现 getAllAIStats(days) - 全局统计 (管理员)
- [ ] 实现 getCostMetrics() - 成本指标 (管理员) - 核心方法
- [ ] 实现 getUserAILogs(userId, params) - 指定用户日志 (管理员)
- [ ] 实现 getUserAIStats(userId, days) - 指定用户统计 (管理员)
- [ ] 更新 import type 引入新类型

---

### Step 4: 改造 AdminCostView 组件 (1.5小时)

**文件**: src/views/AdminCostView/index.tsx

**任务清单**:
- [ ] 导入 DataService 和汇率工具
- [ ] 导入 CostMetrics 类型
- [ ] 添加状态管理 (metrics, loading, error)
- [ ] 实现 loadCostMetrics() 方法
- [ ] 添加 useEffect 自动加载数据
- [ ] 实现加载状态 UI
- [ ] 实现错误状态 UI (带重试按钮)
- [ ] 移除 isFeatureAvailable 检查
- [ ] 数据转换: 后端数据 到 图表数据
- [ ] 所有金额使用 formatUsdToCny() 转换
- [ ] 测试数据绑定正确性

---

### Step 5: 测试和优化 (1小时)

**任务清单**:
- [ ] 启动后端服务 (START_BACKEND.bat)
- [ ] 启动前端服务 (npm run dev)
- [ ] 登录管理员账号
- [ ] 访问成本监控页面 (/admin/cost)
- [ ] 验证 API 调用成功 (Network 面板)
- [ ] 验证数据渲染正确
- [ ] 测试加载状态
- [ ] 测试错误处理 (断开后端测试)
- [ ] 测试空数据情况
- [ ] 检查控制台无报错
- [ ] 检查 TypeScript 类型无错误
- [ ] 优化 UI 细节 (对齐、间距、颜色)

---

## 时间估算

| 步骤 | 任务 | 预计时间 | 实际时间 |
|------|------|---------|---------|
| Step 1 | 创建汇率工具函数 | 15分钟 | - |
| Step 2 | 定义 TypeScript 类型 | 15分钟 | - |
| Step 3 | DataService 添加方法 | 20分钟 | - |
| Step 4 | 改造 AdminCostView | 1.5小时 | - |
| Step 5 | 测试和优化 | 1小时 | - |
| **总计** | | **3小时20分钟** | - |

---

## 验收标准

### 功能验收
- [ ] 成本监控页面不再显示功能开发中
- [ ] 成功调用后端 /api/v1/ai-logs/admin/cost-metrics API
- [ ] 今日成本、本月成本等统计卡片显示真实数据
- [ ] 成本趋势图正确渲染最近7天数据
- [ ] 模型成本分布饼图正确显示
- [ ] 用户成本排行 Top 5 正确显示
- [ ] 模型详细使用表格正确显示
- [ ] 所有金额正确转换为人民币显示

### 技术验收
- [ ] TypeScript 无类型错误
- [ ] 控制台无报错
- [ ] API 调用返回 200 OK
- [ ] 数据格式正确 (camelCase)
- [ ] 汇率转换准确 (1 USD = 7.19 CNY)
- [ ] 错误处理完善
- [ ] 加载状态流畅

---

## 技术决策记录

### 货币存储方案

**选择**: 后端存美元 + 前端转换人民币

**理由**:
- 与 AI API 账单一致 (OpenAI/Gemini 都是美元计费)
- 便于成本核算和对账
- 汇率波动不影响历史数据准确性
- 未来国际化无需改动数据库
- 精度更高 (AI 成本很小, 如 0.000042 美元)

**汇率**: 1 USD = 7.19 CNY (基于 2025-01-10 中国人民银行官方汇率)

**实现**: 创建 currency.ts 工具函数统一转换

---

## 相关文档

- 后端 API 文档: backend/docs/API_REFERENCE.md
- AI 日志模型: backend/app/models/ai_call_log.py
- AI 日志 Service: backend/app/services/ai_log_service.py
- AI 日志 API: backend/app/api/ai_logs.py
- AI 日志 Schema: backend/app/schemas/ai_call_log.py
- 项目文档: NovelAIde 项目文档 v2.12.md

---

**创建时间**: 2025-10-25
**预计完成时间**: 2025-10-25 (当天完成)
**优先级**: P0 (最高优先级)

---

## 🔧 修复记录 (2025-10-25 补充)

### 修复内容

1. **修复 DataService.ts 方法名冲突**
   - 问题：存在两个同名的 `getCostMetrics()` 方法
     - 第 689 行：返回 `CostMetric[]`，调用旧版 `/cost-metrics` API
     - 第 1112 行：返回 `CostMetrics`，调用新版 `/ai-logs/admin/cost-metrics` API
   - 修复：将旧版方法重命名为 `getOldCostMetrics()` 并标记为 `@deprecated`
   - 位置：src/services/DataService.ts:690

2. **修复成本趋势图数据字段不匹配**
   - 问题：图表尝试显示 `calls` 数据，但后端 `dailyCosts` 只返回 `date` 和 `cost`
   - 修复：
     - 移除图表中的"调用次数"线条（第 263-269 行）
     - 移除双 Y 轴配置，简化为单 Y 轴
     - 更新描述文字："每日成本和调用次数变化" → "最近7天每日成本变化"
     - 添加 Tooltip formatter 格式化金额显示
   - 位置：src/views/AdminCostView/index.tsx:234-259

### 修复结果

✅ 消除了 TypeScript 方法名冲突错误
✅ 图表数据字段与后端 API 响应完全匹配
✅ 代码逻辑正确，准备好进行联调测试

### 待测试项

请按照 Step 5 进行以下测试：
- [x] 启动后端服务 (START_BACKEND.bat)
- [x] 启动前端服务 (npm run dev)
- [x] 登录管理员账号
- [x] 访问成本监控页面 (/admin/cost)
- [x] 验证 API 调用成功 (Network 面板) - HTTP 200
- [ ] 验证数据渲染正确 - **发现问题**
- [ ] 测试加载状态
- [ ] 测试错误处理

---

## 🐛 发现的问题 (2025-10-25 测试)

### 测试环境
- 后端服务：✅ 正常运行 (http://localhost:8000)
- 前端服务：✅ 正常运行 (http://localhost:5173)
- API 测试：✅ 成功 (HTTP 200)
- 测试数据：✅ 存在 (5次调用，$0.0002125)

### 问题清单

#### 问题 1: 模型成本分布饼图不显示 🔴 高优先级

**现象**：
- 右侧饼图区域显示深蓝色空白方框
- 未渲染任何图表内容

**可能原因**：
1. 数据值太小（$0.0002125 → ¥0.0015），饼图可能有最小值限制
2. PieChart 组件配置问题
3. 数据格式不匹配

**排查步骤**：
- [ ] 检查浏览器 Console 是否有 Recharts 报错
- [ ] 检查 modelCostData 数据结构
- [ ] 测试使用较大金额数据（如 $10）
- [ ] 检查 PieChart 的 dataKey 和 Cell 配置

**位置**：`src/views/AdminCostView/index.tsx:274-305`

---

#### 问题 2: 成本趋势图数据点不明显 🟡 中优先级

**现象**：
- 图表框架正常显示
- X 轴日期显示正确 (10-19 到 10-25)
- Y 轴刻度显示正常 (0-4)
- 但看不到明显的数据线或数据点

**可能原因**：
1. 数据值太小（成本接近 0），导致线条贴近 X 轴
2. 数据点颜色与背景色对比度不够
3. 10月24日的数据点（$0.0002125）显示不明显

**排查步骤**：
- [ ] 检查 costTrendData 数组内容
- [ ] 查看 10月24日的数据是否正确转换
- [ ] 尝试放大 Y 轴范围或使用对数刻度
- [ ] 增大数据点的 radius (r: 4 → r: 6)
- [ ] 修改线条颜色或粗细

**位置**：`src/views/AdminCostView/index.tsx:234-259`

**API 返回的原始数据**：
```json
"daily_costs": [
  {"date": "2025-10-24", "cost": 0.0002125}  // 其他天都是 0
]
```

---

#### 问题 3: 成本金额显示精度问题 🟡 中优先级

**现象**：
- 所有成本卡片都显示 `¥0.00`
- 实际成本 $0.0002125 约等于 ¥0.0015

**问题**：
- 使用 `toFixed(2)` 四舍五入导致显示为 0.00
- 用户无法感知到实际有产生成本

**建议修复**：
1. 对于小于 0.01 的金额，显示更多小数位（如 4 位）
2. 或者显示科学记数法
3. 或者添加"< ¥0.01"的提示

**位置**：`src/utils/currency.ts:29` 和 `src/views/AdminCostView/index.tsx:80-119`

---

#### 问题 4: 模型详细使用表格 - 总Token数缺失 ℹ️ 信息

**现象**：
- 表格中"总 Token 数"列显示 `-`

**原因**：
- 后端 API 暂未返回 Token 统计数据
- 这是已知限制（见 INFO.md）

**状态**：✅ 已知问题，暂不修复

---

#### 问题 5: 用户成本排行显示用户ID ℹ️ 信息

**现象**：
- 显示的是用户 UUID 的前8位
- 不够友好，建议显示用户名

**状态**：✅ 已知问题，待后续优化

---

### 修复优先级

**P0 (必须修复)**：
1. 问题 1: 模型成本分布饼图不显示

**P1 (建议修复)**：
2. 问题 2: 成本趋势图数据点不明显
3. 问题 3: 成本金额显示精度问题

**P2 (可选优化)**：
4. 问题 4: 总 Token 数缺失（需要后端支持）
5. 问题 5: 用户排行显示优化

---

### 下一步行动

1. **立即排查**：打开浏览器 Console，查看是否有 JavaScript 报错
2. **数据验证**：在 Console 输入以下代码检查数据：
   ```javascript
   // 检查页面数据
   console.log('API Response:', window.__API_DATA__);
   ```
3. **逐个修复**：按优先级从 P0 开始修复问题

---

## 🔧 第二轮修复 (2025-10-25)

### 修复时间
开始时间：2025-10-25
完成时间：2025-10-25

### 修复内容

#### 修复 1: 成本金额显示精度问题 ✅

**问题**：
- 所有成本卡片显示 `¥0.00`
- 实际成本 $0.0002125 约等于 ¥0.0015
- 使用 `toFixed(2)` 导致四舍五入为 0.00

**修复方案**：
1. 修改 `src/utils/currency.ts` 的 `formatUsdToCny()` 函数
2. 实现智能精度显示：
   - `cny === 0`：显示 `¥0.00`
   - `cny < 0.01`：显示 4 位小数（如 `¥0.0015`）
   - `cny < 1`：显示 3 位小数（如 `¥0.156`）
   - `cny >= 1`：显示 2 位小数（如 `¥12.50`）
3. 保持函数签名兼容性，`decimals` 参数改为可选

**修改文件**：
- `src/utils/currency.ts:29-50`

---

#### 修复 2: 模型成本分布饼图不显示 ✅

**问题**：
- 饼图显示深蓝色空白方框
- 数据值太小导致渲染问题
- 标签重叠不清晰

**修复方案**：
1. 修改饼图配置：
   - 启用 `labelLine={true}` 显示标签连接线
   - 增大 `outerRadius` 从 80 到 90
   - 添加 `innerRadius={40}` 创建环形图效果
   - 添加 `paddingAngle={2}` 增加扇区间距
   - 增大数据点边框 `strokeWidth: 2, stroke: '#fff'`
2. 修改数据精度：保留 4 位小数而非 2 位
3. 添加空数据处理：显示"暂无数据"提示
4. 优化 Tooltip 显示：使用 4 位小数格式化

**修改文件**：
- `src/views/AdminCostView/index.tsx:129-136` (数据转换)
- `src/views/AdminCostView/index.tsx:263-304` (饼图组件)

---

#### 修复 3: 成本趋势图数据点不明显 ✅

**问题**：
- 数据值太小（接近 0），线条贴近 X 轴
- 数据点半径太小（r: 4）
- Y 轴格式化不够精确

**修复方案**：
1. 修改趋势数据精度：保留 4 位小数
2. 增大数据点配置：
   - `strokeWidth: 3` (线条宽度从 2 增加到 3)
   - `dot={{ r: 6, strokeWidth: 2, stroke: '#fff' }}` (半径从 4 增加到 6，添加白色边框)
   - `activeDot={{ r: 8, strokeWidth: 2 }}` (激活时半径 8)
3. 优化 Y 轴显示：
   - 添加 `tickFormatter` 显示 4 位小数
4. 优化 Tooltip：显示 4 位小数格式

**修改文件**：
- `src/views/AdminCostView/index.tsx:123-126` (趋势数据)
- `src/views/AdminCostView/index.tsx:234-264` (趋势图组件)

---

#### 其他优化 ✅

1. **模型详细使用表格**：
   - 总成本和平均成本都改为 4 位小数
   - 位置：`src/views/AdminCostView/index.tsx:150-159`

2. **用户成本排行**：
   - 用户成本显示改为 4 位小数
   - 位置：`src/views/AdminCostView/index.tsx:139-147,363`

---

### 修复效果预期

**成本卡片**：
- 今日成本：`¥0.0015`（原 `¥0.00`）
- 本月成本：`¥0.0015`（原 `¥0.00`）
- 平均每次：`¥0.0003`（原 `¥0.00`）
- 昨日成本：`¥0.00`（确实为 0）

**成本趋势图**：
- 数据点清晰可见（白色边框 + 更大半径）
- Y 轴显示 4 位小数（如 `¥0.0015`）
- Tooltip 显示完整精度

**模型成本分布饼图**：
- 环形图样式（内半径 40，外半径 90）
- 标签连接线清晰
- 扇区间有间隔（paddingAngle: 2）
- Tooltip 显示 4 位小数

**模型详细表格**：
- 总成本列：`¥0.0015`
- 平均成本列：`¥0.0003`

**用户排行**：
- 成本显示：`¥0.0015`

---

### 待测试项

请重新启动前端服务测试：
- [ ] 成本卡片是否正确显示小额（4位小数）
- [ ] 成本趋势图数据点是否清晰可见
- [ ] 模型成本分布饼图是否正常渲染
- [ ] 所有金额格式是否符合预期
- [ ] 控制台是否有报错

---

### 技术总结

**核心问题**：前端显示精度不足导致小额成本被四舍五入为 0

**解决思路**：
1. 智能精度函数：根据金额大小自动调整小数位数
2. 数据保留精度：从 2 位提升到 4 位小数
3. 图表视觉优化：增大数据点、添加边框、优化配色
4. 空数据处理：添加友好的空状态提示

**影响范围**：
- `src/utils/currency.ts` (1 个函数)
- `src/views/AdminCostView/index.tsx` (5 处数据转换 + 2 处图表配置)

**兼容性**：
- 向后兼容：`formatUsdToCny()` 仍支持指定 `decimals` 参数
- 无破坏性修改：仅增强显示精度

---

## 📊 数据面板模块Bug修复计划 (2025-10-25)

### 项目概述

**目标**: 修复数据面板模块的严重bug并实现缺失的功能
**优先级**: P0 (最高优先级)
**预计时间**: 3-5个工作日
**负责人**: 待分配
**开始日期**: 2025-10-25
**状态**: 计划中

---

### 问题清单

根据代码审查,发现以下问题:

#### 🔴 P0 - 严重Bug (必须立即修复)

**Bug 1: AdminUsersView 存在重复的 loadUsers() 函数定义**
- **位置**: `src/views/AdminUsersView/index.tsx:30-46` 和 `69-81`
- **问题**: 完全相同的函数定义了两次,造成代码冗余
- **影响**: 代码维护困难,可能导致逻辑不一致
- **修复**: 删除第二个定义 (lines 69-81)

**Bug 2: AdminDashboardView 成本显示精度不足**
- **位置**: `src/views/AdminDashboardView/index.tsx:102`
- **问题**: 成本卡片使用 `toLocaleString()` 会四舍五入小数
- **代码**:
  ```typescript
  value: `¥${(cost.total || 0).toLocaleString()}`
  ```
- **影响**: 小额成本显示为 ¥0,用户无法感知真实成本
- **修复**: 使用 `formatUsdToCny()` 工具函数

**Bug 3: AdminDashboardView 成本趋势颜色逻辑错误**
- **位置**: `src/views/AdminDashboardView/index.tsx:108`
- **问题**: 成本上升显示红色,下降显示绿色 (应该相反)
- **代码**:
  ```typescript
  trendColor: (cost.change || '+0%').startsWith('-') ? 'text-green-600' : 'text-red-600',
  ```
- **影响**: 用户误解成本趋势,认为成本下降是坏事
- **修复**: 交换颜色逻辑

**Bug 4: AdminDashboardView AI使用图表成本单位错误**
- **位置**: `src/views/AdminDashboardView/index.tsx:247`
- **问题**: 图表显示 "成本 (¥)" 但数据实际是美元
- **代码**:
  ```typescript
  <Bar dataKey="cost" fill="#F59E0B" name="成本 (¥)" radius={[8, 8, 0, 0]} />
  ```
- **影响**: 数据误导,用户看到的金额与实际不符
- **修复**: 数据转换为人民币 或 修改标签为 "成本 ($)"

---

#### 🟡 P1 - 主要缺失功能 (本周内完成)

**缺失 1: AI模型管理功能完全未实现**
- **位置**: `src/views/AdminAIModelsView/index.tsx`
- **问题**:
  - 前端显示 "功能开发中,敬请期待"
  - 后端没有任何 AI 模型相关的数据库模型
  - 后端没有 AI 模型的 CRUD API
- **影响**: 管理员无法管理 AI 模型配置
- **所需工作**:
  1. 后端: 创建 AIModel 数据库模型
  2. 后端: 实现 AI 模型 CRUD API (6个端点)
  3. 前端: 实现模型列表/添加/编辑/删除功能
  4. 前端: 连接后端 API
- **预计时间**: 2-3 天

**缺失 2: 管理员统计数据使用 Mock 数据**
- **位置**: `src/services/DataService.ts:620-634`
- **问题**: `getAdminStatistics()` 返回硬编码的测试数据
- **代码分析**:
  ```typescript
  static async getAdminStatistics() {
    const response = await apiClient.get<AdminStatistics>('/admin/statistics');
    return response.data;
  }
  ```
- **后端状态**: 未验证 `/admin/statistics` API 是否返回真实数据
- **影响**: 管理后台显示的统计数据不准确
- **修复**: 检查后端实现,确保从数据库统计真实数据

**缺失 3: 用户增长趋势使用 Mock 数据**
- **位置**: `src/services/DataService.ts:636-644`
- **问题**: `getUsersGrowth()` 可能返回测试数据
- **后端状态**: 未验证数据来源
- **影响**: 增长趋势图不准确
- **修复**: 验证后端是否从用户表统计真实增长数据

**缺失 4: AI 使用统计未连接真实日志数据**
- **位置**: `src/services/DataService.ts:646-649`
- **问题**: `getAIUsage()` 未确认是否使用 `ai_call_logs` 表
- **期望**: 应该从 `ai_call_logs` 表统计模型使用情况
- **影响**: AI 使用图表可能显示假数据
- **修复**: 确认后端实现使用真实日志数据

---

#### 🟢 P2 - 优化建议 (未来改进)

**优化 1: 用户列表缺少分页功能**
- **位置**: `src/views/AdminUsersView/index.tsx`
- **问题**: 一次性加载所有用户,数据量大时性能差
- **建议**: 实现分页或虚拟滚动

**优化 2: 缺少用户活动日志系统**
- **问题**: 无法追踪用户操作历史
- **建议**: 实现活动日志记录和查看功能

---

### 实施计划

#### Phase 1: 修复严重 Bug (0.5天)

**任务清单**:
- [ ] Bug 1: 删除 AdminUsersView 重复的 loadUsers() 函数
- [ ] Bug 2: 修复 AdminDashboardView 成本显示精度
- [ ] Bug 3: 修复 AdminDashboardView 成本趋势颜色逻辑
- [ ] Bug 4: 修复 AdminDashboardView AI使用图表成本单位

**实施细节**:

**1.1 删除重复函数 (5分钟)**
```typescript
// 文件: src/views/AdminUsersView/index.tsx
// 删除 lines 69-81 的重复定义
// 保留 lines 30-46 的第一个定义
```

**1.2 修复成本显示精度 (10分钟)**
```typescript
// 文件: src/views/AdminDashboardView/index.tsx:102
// 修改前:
value: `¥${(cost.total || 0).toLocaleString()}`

// 修改后:
value: formatUsdToCny(cost.total || 0)

// 同时需要导入:
import { formatUsdToCny } from '../../utils/currency';
```

**1.3 修复成本趋势颜色 (5分钟)**
```typescript
// 文件: src/views/AdminDashboardView/index.tsx:108
// 修改前:
trendColor: (cost.change || '+0%').startsWith('-') ? 'text-green-600' : 'text-red-600',

// 修改后:
trendColor: (cost.change || '+0%').startsWith('+') ? 'text-red-600' : 'text-green-600',
```

**1.4 修复AI成本单位 (15分钟)**

**方案A**: 转换数据为人民币
```typescript
// 文件: src/views/AdminDashboardView/index.tsx
// 在 loadData() 中转换 aiUsageData:
const aiUsage = await DataService.getAIUsage();
const convertedData = (aiUsage.data || []).map(item => ({
  ...item,
  cost: parseFloat((item.cost * 7.19).toFixed(4))
}));
setAiUsageData(convertedData);
```

**方案B**: 修改标签
```typescript
// 文件: src/views/AdminDashboardView/index.tsx:247
<Bar dataKey="cost" fill="#F59E0B" name="成本 ($)" radius={[8, 8, 0, 0]} />
```

**推荐**: 方案A (统一显示人民币)

---

#### Phase 2: 验证数据统计 API (1天)

**任务清单**:
- [ ] 检查后端 `/admin/statistics` API 实现
- [ ] 检查后端 `/users/growth` API 实现
- [ ] 检查后端 `/ai/usage` API 实现
- [ ] 确认所有 API 使用真实数据库数据
- [ ] 修复发现的 Mock 数据问题

**实施步骤**:

**2.1 检查后端统计 API**
```bash
# 搜索后端 API 定义
cd backend
grep -r "admin/statistics" app/api/
grep -r "users/growth" app/api/
grep -r "ai/usage" app/api/
```

**2.2 验证数据查询逻辑**
- 检查 API 是否从数据库表查询
- 确认没有硬编码的测试数据
- 验证统计计算逻辑正确

**2.3 测试 API 返回数据**
```bash
# 使用 curl 或 Postman 测试
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/admin/statistics
```

**2.4 修复发现的问题**
- 如果发现 Mock 数据,替换为真实查询
- 如果 API 不存在,创建对应的 API 端点

---

#### Phase 3: 实现 AI 模型管理功能 (2-3天)

**任务清单**:
- [ ] 后端: 创建 AIModel 数据库模型
- [ ] 后端: 创建 AIModel Schema
- [ ] 后端: 实现 AI 模型 CRUD API
- [ ] 前端: 移除 "功能开发中" 占位符
- [ ] 前端: 实现模型列表展示
- [ ] 前端: 实现添加模型功能
- [ ] 前端: 实现编辑模型功能
- [ ] 前端: 实现删除模型功能
- [ ] 前端: 连接后端 API
- [ ] 测试完整功能

**3.1 后端数据库模型 (30分钟)**

**文件**: `backend/app/models/ai_model.py` (新建)

```python
from sqlalchemy import Column, String, Float, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

from app.database import Base

class AIModel(Base):
    """AI 模型配置表"""
    __tablename__ = "ai_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, comment="模型名称")
    provider = Column(String(50), nullable=False, comment="提供商")
    model_id = Column(String(100), nullable=False, unique=True, comment="模型ID")
    input_price = Column(Float, nullable=False, comment="输入价格 (USD/1M tokens)")
    output_price = Column(Float, nullable=False, comment="输出价格 (USD/1M tokens)")
    context_window = Column(Integer, comment="上下文窗口大小")
    description = Column(Text, comment="模型描述")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**3.2 后端 Schema (20分钟)**

**文件**: `backend/app/schemas/ai_model.py` (新建)

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID

class AIModelBase(BaseModel):
    name: str = Field(..., description="模型名称")
    provider: str = Field(..., description="提供商")
    model_id: str = Field(..., description="模型ID")
    input_price: float = Field(..., description="输入价格")
    output_price: float = Field(..., description="输出价格")
    context_window: Optional[int] = Field(None, description="上下文窗口")
    description: Optional[str] = Field(None, description="模型描述")
    is_active: bool = Field(True, description="是否启用")

class AIModelCreate(AIModelBase):
    pass

class AIModelUpdate(BaseModel):
    name: Optional[str] = None
    provider: Optional[str] = None
    input_price: Optional[float] = None
    output_price: Optional[float] = None
    context_window: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class AIModelResponse(AIModelBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

**3.3 后端 API 端点 (1小时)**

**文件**: `backend/app/api/ai_models.py` (新建)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.database import get_db
from app.models.ai_model import AIModel
from app.schemas.ai_model import AIModelCreate, AIModelUpdate, AIModelResponse
from app.api.auth import get_current_admin_user

router = APIRouter(prefix="/api/v1/admin/ai-models", tags=["AI Models"])

@router.get("", response_model=List[AIModelResponse])
async def get_ai_models(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """获取所有 AI 模型"""
    models = db.query(AIModel).all()
    return models

@router.post("", response_model=AIModelResponse, status_code=status.HTTP_201_CREATED)
async def create_ai_model(
    model_data: AIModelCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """创建 AI 模型"""
    # 检查 model_id 是否已存在
    existing = db.query(AIModel).filter(AIModel.model_id == model_data.model_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="模型ID已存在")

    model = AIModel(**model_data.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model

@router.get("/{model_id}", response_model=AIModelResponse)
async def get_ai_model(
    model_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """获取单个 AI 模型"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return model

@router.put("/{model_id}", response_model=AIModelResponse)
async def update_ai_model(
    model_id: UUID,
    model_data: AIModelUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """更新 AI 模型"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    for field, value in model_data.dict(exclude_unset=True).items():
        setattr(model, field, value)

    db.commit()
    db.refresh(model)
    return model

@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_model(
    model_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_admin_user)
):
    """删除 AI 模型"""
    model = db.query(AIModel).filter(AIModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")

    db.delete(model)
    db.commit()
    return None
```

**3.4 前端类型定义 (10分钟)**

**文件**: `src/types/index.ts` (添加)

```typescript
export interface AIModel {
  id: string;
  name: string;
  provider: string;
  modelId: string;
  inputPrice: number;
  outputPrice: number;
  contextWindow?: number;
  description?: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface AIModelCreate {
  name: string;
  provider: string;
  modelId: string;
  inputPrice: number;
  outputPrice: number;
  contextWindow?: number;
  description?: string;
  isActive?: boolean;
}

export interface AIModelUpdate {
  name?: string;
  provider?: string;
  inputPrice?: number;
  outputPrice?: number;
  contextWindow?: number;
  description?: string;
  isActive?: boolean;
}
```

**3.5 前端 DataService 方法 (15分钟)**

**文件**: `src/services/DataService.ts:651-681` (替换现有 Mock 方法)

```typescript
// AI 模型管理
static async getAIModels(): Promise<AIModel[]> {
  const response = await apiClient.get<AIModel[]>('/admin/ai-models');
  return response.data;
}

static async getAIModel(id: string): Promise<AIModel> {
  const response = await apiClient.get<AIModel>(`/admin/ai-models/${id}`);
  return response.data;
}

static async createAIModel(data: AIModelCreate): Promise<AIModel> {
  const response = await apiClient.post<AIModel>('/admin/ai-models', data);
  return response.data;
}

static async updateAIModel(id: string, data: AIModelUpdate): Promise<AIModel> {
  const response = await apiClient.put<AIModel>(`/admin/ai-models/${id}`, data);
  return response.data;
}

static async deleteAIModel(id: string): Promise<void> {
  await apiClient.delete(`/admin/ai-models/${id}`);
}
```

**3.6 前端 UI 实现 (1.5天)**

**文件**: `src/views/AdminAIModelsView/index.tsx` (完全重写)

需要实现:
- 模型列表表格
- 添加模型弹窗
- 编辑模型弹窗
- 删除确认弹窗
- 加载状态
- 错误处理
- 搜索过滤

(详细代码略,参考 AdminUsersView 的实现模式)

---

#### Phase 4: 测试和优化 (0.5天)

**任务清单**:
- [ ] 启动后端服务
- [ ] 启动前端服务
- [ ] 测试所有修复的 Bug
- [ ] 测试 AI 模型管理完整流程
- [ ] 检查控制台无报错
- [ ] 检查 TypeScript 类型无错误
- [ ] 优化 UI 细节
- [ ] 编写测试用例

---

### 时间估算

| Phase | 任务 | 预计时间 | 实际时间 |
|-------|------|---------|---------|
| Phase 1 | 修复严重 Bug | 0.5天 | - |
| Phase 2 | 验证数据统计 API | 1天 | - |
| Phase 3 | 实现 AI 模型管理 | 2-3天 | - |
| Phase 4 | 测试和优化 | 0.5天 | - |
| **总计** | | **4-5天** | - |

---

### 验收标准

#### Phase 1 验收
- [ ] AdminUsersView 无重复函数
- [ ] AdminDashboardView 成本卡片显示正确精度 (如 ¥0.0015)
- [ ] AdminDashboardView 成本趋势颜色正确 (上升红色,下降绿色)
- [ ] AdminDashboardView AI成本图表单位正确 (统一为人民币)
- [ ] 控制台无报错
- [ ] TypeScript 类型检查通过

#### Phase 2 验收
- [ ] 所有统计 API 返回真实数据库数据
- [ ] 用户增长趋势显示真实历史数据
- [ ] AI 使用统计连接 ai_call_logs 表
- [ ] 数据面板显示数据准确

#### Phase 3 验收
- [ ] AI 模型数据库表创建成功
- [ ] 可以添加新的 AI 模型
- [ ] 可以编辑现有 AI 模型
- [ ] 可以删除 AI 模型
- [ ] 可以查看模型列表
- [ ] 模型列表显示所有字段正确
- [ ] AdminAIModelsView 不再显示 "功能开发中"

#### Phase 4 验收
- [ ] 所有功能测试通过
- [ ] UI 体验流畅
- [ ] 无性能问题
- [ ] 错误处理完善

---

### 技术决策

**决策 1: 成本显示统一使用人民币**
- 理由: 用户主要在中国,人民币更直观
- 实现: 使用 `formatUsdToCny()` 工具函数
- 影响: AdminDashboardView 需要转换 AI 成本数据

**决策 2: AI 模型管理使用完整的 CRUD API**
- 理由: 管理员需要灵活管理模型配置
- 实现: RESTful API 设计
- 数据库: 独立的 ai_models 表

**决策 3: 优先修复严重 Bug,再实现新功能**
- 理由: 确保现有功能正确运行
- 顺序: Phase 1 → Phase 2 → Phase 3

---

### 风险和依赖

**风险**:
1. 后端统计 API 可能需要复杂的数据库查询优化
2. AI 模型管理的数据迁移可能影响现有系统
3. Phase 3 工作量可能超出估算

**依赖**:
- 后端 FastAPI 框架
- 数据库迁移工具 (Alembic)
- ai_call_logs 表已存在且有数据

---

**创建时间**: 2025-10-25
**预计完成时间**: 2025-10-30 (5个工作日)
**优先级**: P0 (最高优先级)
**当前状态**: 计划已完成,等待开始实施

---

