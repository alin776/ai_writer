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
- [ ] 启动后端服务 (START_BACKEND.bat)
- [ ] 启动前端服务 (npm run dev)
- [ ] 登录管理员账号
- [ ] 访问成本监控页面 (/admin/cost)
- [ ] 验证 API 调用成功 (Network 面板)
- [ ] 验证数据渲染正确
- [ ] 测试加载状态
- [ ] 测试错误处理

