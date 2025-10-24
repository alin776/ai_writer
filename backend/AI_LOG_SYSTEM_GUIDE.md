# AI 调用日志系统使用指南

## 📋 概述

AI 调用日志系统自动记录所有 AI API 调用的详细信息，包括 Token 使用量、成本、耗时等，为成本监控和使用分析提供数据基础。

## 🏗️ 系统架构

### 核心组件

1. **AICallLog (数据模型)** - `backend/app/models/ai_call_log.py`
   - 存储AI调用的完整日志信息
   - 支持外键关联到用户、作品、章节、分析

2. **AILogService (日志服务)** - `backend/app/services/ai_log_service.py`
   - 提供日志创建、查询、统计功能
   - 支持按时间范围、用户、模型、操作类型聚合统计

3. **CostCalculator (成本计算器)** - `backend/app/utils/cost_calculator.py`
   - 根据不同模型定价计算Token成本
   - 支持动态添加新模型定价

4. **AILogMiddleware (日志中间件)** - `backend/app/services/ai/ai_log_middleware.py`
   - 上下文管理器自动记录AI调用
   - 自动计算耗时、成本、Token数量

## 📊 数据库表结构

### ai_call_logs 表

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | UUID | 主键 |
| user_id | UUID | 用户ID（外键） |
| model_name | String(100) | AI模型名称 |
| operation_type | String(50) | 操作类型 |
| work_id | UUID | 作品ID（可选） |
| chapter_id | UUID | 章节ID（可选） |
| analysis_id | UUID | 分析ID（可选） |
| prompt_tokens | Integer | 输入Token数 |
| completion_tokens | Integer | 输出Token数 |
| total_tokens | Integer | 总Token数 |
| prompt_cost | Float | 输入成本($) |
| completion_cost | Float | 输出成本($) |
| total_cost | Float | 总成本($) |
| duration_ms | Integer | 耗时(毫秒) |
| is_success | Boolean | 是否成功 |
| error_message | Text | 错误信息 |
| metadata | JSONB | 额外数据 |
| created_at | DateTime | 创建时间 |

### 索引优化

- 单列索引: id, user_id, model_name, operation_type, created_at
- 复合索引:
  - (user_id, created_at) - 用户成本统计
  - (model_name, created_at) - 模型使用统计
  - (operation_type, created_at) - 操作类型分析
  - (work_id, created_at) - 作品AI使用情况

## 🔧 使用方法

### 1. 在AI服务中集成日志记录

```python
from sqlalchemy.orm import Session
from app.services.ai.ai_log_middleware import AILogMiddleware

async def my_ai_function(
    db: Session,
    user_id: UUID,
    text: str
):
    # 创建日志中间件
    log_middleware = AILogMiddleware(
        db=db,
        user_id=user_id,
        model_name="gemini-2.5-pro"
    )

    # 使用上下文管理器自动记录
    async with log_middleware.log_call(
        operation_type="polish",  # 操作类型
        chapter_id=chapter_id,    # 可选：关联章节
        metadata={                # 可选：额外数据
            "temperature": 0.7,
            "max_tokens": 1000
        }
    ) as token_counter:
        # AI调用逻辑
        result = await call_ai_api(text)

        # 设置Token数量（如果API返回）
        token_counter.set_tokens(
            prompt_tokens=100,
            completion_tokens=200
        )

        return result
```

### 2. 数据库迁移

```bash
# 进入backend目录
cd backend

# 运行迁移
alembic upgrade head
```

### 3. API 接口

#### 用户接口

**获取我的日志**
```http
GET /api/v1/ai-logs/me?skip=0&limit=100&start_date=2025-10-01&end_date=2025-10-31
Authorization: Bearer <token>
```

**获取我的统计**
```http
GET /api/v1/ai-logs/me/stats?days=30
Authorization: Bearer <token>
```

响应示例:
```json
{
  "total_calls": 150,
  "total_tokens": 45000,
  "total_cost": 0.125,
  "success_rate": 98.67,
  "avg_duration_ms": 1250.5,
  "by_model": {
    "gemini-2.5-pro": {
      "calls": 100,
      "tokens": 30000,
      "cost": 0.0875
    },
    "gpt-4-turbo": {
      "calls": 50,
      "tokens": 15000,
      "cost": 0.0375
    }
  },
  "by_operation": {
    "polish": {"calls": 80, "tokens": 24000, "cost": 0.072},
    "continue": {"calls": 40, "tokens": 12000, "cost": 0.036},
    "summarize": {"calls": 30, "tokens": 9000, "cost": 0.027}
  },
  "start_date": "2025-09-24T00:00:00Z",
  "end_date": "2025-10-24T00:00:00Z"
}
```

#### 管理员接口

**获取全局统计**
```http
GET /api/v1/ai-logs/admin/stats?days=30
Authorization: Bearer <admin_token>
```

**获取成本指标**
```http
GET /api/v1/ai-logs/admin/cost-metrics
Authorization: Bearer <admin_token>
```

响应示例:
```json
{
  "today_cost": 1.25,
  "yesterday_cost": 1.18,
  "this_month_cost": 35.67,
  "last_month_cost": 42.33,
  "today_calls": 120,
  "this_month_calls": 3500,
  "daily_costs": [
    {"date": "2025-10-18", "cost": 1.05},
    {"date": "2025-10-19", "cost": 1.32},
    {"date": "2025-10-20", "cost": 0.98},
    {"date": "2025-10-21", "cost": 1.45},
    {"date": "2025-10-22", "cost": 1.21},
    {"date": "2025-10-23", "cost": 1.18},
    {"date": "2025-10-24", "cost": 1.25}
  ],
  "top_users": [
    {"user_id": "uuid1", "total_cost": 5.67, "total_calls": 450},
    {"user_id": "uuid2", "total_cost": 4.32, "total_calls": 380}
  ],
  "top_models": [
    {"model_name": "gemini-2.5-pro", "total_cost": 20.15, "total_calls": 2100},
    {"model_name": "gpt-4-turbo", "total_cost": 15.52, "total_calls": 1400}
  ]
}
```

**查询指定用户日志**
```http
GET /api/v1/ai-logs/admin/user/{user_id}/logs
GET /api/v1/ai-logs/admin/user/{user_id}/stats
Authorization: Bearer <admin_token>
```

## 💰 成本计算

### 支持的模型定价 ($/百万Token)

| 模型 | 输入价格 | 输出价格 |
|------|---------|---------|
| gpt-4 | $30.00 | $60.00 |
| gpt-4-turbo | $10.00 | $30.00 |
| gpt-3.5-turbo | $0.50 | $1.50 |
| gemini-2.5-pro | $1.25 | $5.00 |
| gemini-2.0-flash | $0.10 | $0.30 |
| claude-3-opus | $15.00 | $75.00 |
| claude-3-sonnet | $3.00 | $15.00 |

### 添加新模型定价

```python
from app.utils.cost_calculator import CostCalculator

# 添加新模型
CostCalculator.add_model_pricing(
    model_name="new-model-name",
    input_price=1.0,   # $/百万Token
    output_price=2.0   # $/百万Token
)
```

## 📈 前端集成

### 管理后台成本监控

在管理后台 `/admin/settings` 页面，使用真实API替换Mock数据：

```typescript
// src/services/AdminService.ts
async getCostMetrics(): Promise<CostMetrics> {
  return this.adapter.get<CostMetrics>('/ai-logs/admin/cost-metrics');
}
```

### 用户个人统计

在用户设置页面显示AI使用情况：

```typescript
// src/services/UserService.ts
async getMyAIStats(days: number = 30): Promise<AICallLogStats> {
  return this.adapter.get<AICallLogStats>(`/ai-logs/me/stats?days=${days}`);
}
```

## ⚙️ 配置说明

### 操作类型枚举

建议的操作类型值:
- `continue` - 续写
- `polish` - 润色
- `summarize` - 总结
- `translate` - 翻译
- `expand` - 扩写
- `analyze_micro` - 微观分析
- `analyze_macro` - 宏观分析

### Token估算

中间件提供简单的Token估算功能:
- 英文: 1 token ≈ 4字符
- 中文: 1 token ≈ 1.5字符

如果AI API返回准确Token数，建议使用API返回值。

## 🔍 查询示例

### SQL查询示例

```sql
-- 查询今日总成本
SELECT SUM(total_cost) FROM ai_call_logs
WHERE created_at >= CURRENT_DATE;

-- 查询某用户本月使用最多的模型
SELECT model_name, COUNT(*) as calls, SUM(total_cost) as cost
FROM ai_call_logs
WHERE user_id = 'xxx'
  AND created_at >= date_trunc('month', CURRENT_DATE)
GROUP BY model_name
ORDER BY cost DESC;

-- 查询失败率高的操作类型
SELECT operation_type,
       COUNT(*) as total,
       SUM(CASE WHEN is_success = false THEN 1 ELSE 0 END) as failures,
       ROUND(100.0 * SUM(CASE WHEN is_success = false THEN 1 ELSE 0 END) / COUNT(*), 2) as failure_rate
FROM ai_call_logs
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY operation_type
HAVING COUNT(*) > 10
ORDER BY failure_rate DESC;
```

## 📝 注意事项

1. **性能优化**: 日志表会快速增长，建议:
   - 定期归档历史数据（如保留最近3个月）
   - 使用分区表（按月分区）
   - 定期执行 VACUUM ANALYZE

2. **异步记录**: 日志记录失败不应影响主业务流程

3. **隐私保护**: metadata字段不应存储敏感内容（如完整文本）

4. **成本更新**: 模型定价变化时需要手动更新 CostCalculator

## 🎯 下一步

- [ ] 集成到现有AI服务（续写、润色等）
- [ ] 前端成本监控页面对接真实API
- [ ] 添加成本预警功能（超出预算通知）
- [ ] 支持导出成本报表（Excel/CSV）

---

**文档版本**: v1.0
**创建日期**: 2025-10-24
**作者**: Claude Code
