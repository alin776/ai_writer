# AI 日志系统测试指南

## 📋 测试前准备

### 1. 确保后端服务正在运行

```bash
cd backend
# 使用虚拟环境
./venv/Scripts/activate  # Windows
source venv/bin/activate  # Linux/Mac

# 启动服务
uvicorn app.main:app --reload
```

服务应该运行在 `http://localhost:8000`

### 2. 确保有测试用户

需要一个测试用户账号：
- **邮箱**: `test@example.com`
- **密码**: `test123456`

如果没有，可以通过前端注册或直接在数据库创建。

---

## 🚀 快速测试（推荐）

使用简化版测试脚本，**不需要直接连接数据库**：

```bash
cd backend
python test_ai_logs_quick.py
```

### 测试内容

1. ✅ 用户登录
2. ✅ AI 续写调用（带日志记录）
3. ✅ AI 润色调用（带日志记录）
4. ✅ 用户统计 API (`GET /api/v1/ai-logs/me/stats`)
5. ✅ 日志列表 API (`GET /api/v1/ai-logs/me`)

### 预期输出

如果成功，你会看到类似这样的输出：

```
✅ 登录成功！用户: test (ID: xxx)
✅ AI 续写完成！生成 123 字符
✅ AI 润色完成！
✅ 统计 API 调用成功！

📈 您的 AI 使用统计 (最近7天):
  📞 总调用次数: 5
  🎯 总 Token 数: 1,234
  💰 总成本: $0.001234
  ✅ 成功率: 100.00%
  ⏱️  平均耗时: 1250ms

📊 按操作类型统计:
    • continue     :   2次 | 1,000 tokens | $0.000500
    • polish       :   3次 |   234 tokens | $0.000234
```

---

## 🔬 完整测试（需要数据库连接）

如果想直接查询数据库验证数据，使用完整版：

```bash
cd backend
python test_ai_logs.py
```

这个脚本会：
1. 连接数据库直接查询日志表
2. 显示最新日志的详细信息
3. 验证数据库中的记录

**注意**：需要在 `backend/.env` 中配置正确的数据库连接。

---

## 🔍 手动验证

### 1. 通过前端测试

1. 启动前端服务
2. 登录测试账号
3. 使用任意 AI 功能（续写、润色等）
4. 打开浏览器开发者工具，查看 Network 请求
5. 观察 `/api/v1/ai/complete` 等接口是否正常返回

### 2. 查询数据库

直接连接 PostgreSQL 数据库查询：

```sql
-- 查看最新的 10 条日志
SELECT
    created_at,
    operation_type,
    model_name,
    total_tokens,
    total_cost,
    duration_ms,
    is_success
FROM ai_call_logs
ORDER BY created_at DESC
LIMIT 10;

-- 统计今日使用情况
SELECT
    operation_type,
    COUNT(*) as calls,
    SUM(total_tokens) as total_tokens,
    SUM(total_cost) as total_cost
FROM ai_call_logs
WHERE created_at >= CURRENT_DATE
GROUP BY operation_type;

-- 查看特定用户的使用情况
SELECT
    COUNT(*) as total_calls,
    SUM(total_cost) as total_cost,
    AVG(duration_ms) as avg_duration
FROM ai_call_logs
WHERE user_id = 'your-user-id-here';
```

### 3. 测试统计 API

使用 curl 或 Postman 测试：

```bash
# 登录获取 token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123456"

# 获取用户统计（替换 YOUR_TOKEN）
curl -X GET "http://localhost:8000/api/v1/ai-logs/me/stats?days=7" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 获取日志列表
curl -X GET "http://localhost:8000/api/v1/ai-logs/me?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## ✅ 验证清单

- [ ] 数据库迁移已执行（`ai_call_logs` 表已创建）
- [ ] 后端服务正常启动
- [ ] AI API 调用返回正常（续写、润色等）
- [ ] 调用 AI 后，数据库中有新的日志记录
- [ ] 日志记录包含完整信息（token、成本、耗时）
- [ ] 统计 API 返回正确数据
- [ ] 日志列表 API 返回正确数据

---

## 🐛 常见问题

### 1. 登录失败

**原因**: 测试用户不存在或密码错误

**解决**:
- 修改脚本中的 `TEST_USER_EMAIL` 和 `TEST_USER_PASSWORD`
- 或者创建对应的测试用户

### 2. API 调用失败

**原因**: 后端服务未启动或端口不对

**解决**:
- 检查后端服务是否运行在 `http://localhost:8000`
- 修改脚本中的 `API_BASE_URL`

### 3. 日志未记录

**原因**: 可能是数据库连接问题或中间件异常

**解决**:
- 检查后端日志，查看是否有错误信息
- 确认数据库连接配置正确
- 检查 `.env` 文件中的 `DATABASE_URL`

### 4. Token 统计不准确

**原因**: 使用的是估算方法

**说明**:
- 当前使用文本长度估算 token 数量
- 如果 AI API 返回准确的 token 数据，可以修改代码使用精确值
- 估算公式：中文 1 token ≈ 1.5 字符，英文 1 token ≈ 4 字符

---

## 📊 测试成功的标志

如果看到以下输出，说明日志系统工作正常：

1. ✅ AI API 调用成功返回内容
2. ✅ 统计 API 显示调用次数 > 0
3. ✅ 统计 API 显示总成本 > 0
4. ✅ 日志列表 API 返回记录
5. ✅ 数据库中有对应的记录

---

## 📞 需要帮助？

如果测试遇到问题：

1. 查看后端服务日志
2. 查看数据库是否有错误
3. 检查网络请求是否正常
4. 确认所有依赖已安装

