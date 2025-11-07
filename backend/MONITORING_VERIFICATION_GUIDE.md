# Phase 2 监控验证指南

**目标**：验证监控系统100%工作，确认所有LLM调用被正确监控

---

## 📋 前置准备

### 1. 检查环境配置

确保以下文件配置正确：

```bash
# 检查 .env 文件存在
cd backend
dir .env
```

必须的环境变量：
- `DATABASE_URL` - 数据库连接
- `REDIS_URL` - Redis连接（如果需要）
- `OPENAI_API_KEY` 或相关AI服务配置

### 2. 安装依赖

```bash
cd backend
pip install httpx  # 用于监控验证脚本
```

---

## 🚀 启动步骤

### Step 1: 启动Backend服务

**方法一：命令行启动（推荐用于测试）**

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**方法二：使用venv（如果配置了虚拟环境）**

```bash
cd backend
./venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

**启动成功标志**：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: 验证服务启动

打开浏览器访问：
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/v1/monitoring/health

---

## 🔍 监控验证测试

### 方法一：运行自动化验证脚本（推荐）

**在新的命令行窗口运行**：

```bash
cd backend
python test_monitoring_verification.py
```

**预期输出**：
```
================================================================================
  Phase 2 监控验证 - 开始
================================================================================

================================================================================
  Test 1: 健康检查端点
================================================================================
[PASS] 健康检查端点 - 状态码
      status_code=200
[PASS] 健康检查端点 - 响应字段
      包含字段: ['status', 'timestamp', ...]

================================================================================
  Test 2: 监控指标端点
================================================================================
[PASS] 监控指标端点 - 状态码
      status_code=200
[PASS] 监控指标 - API层指标
      API指标数: X
[PASS] 监控指标 - LLM层指标
      LLM指标数: Y

... (更多测试)

================================================================================
  监控验证总结
================================================================================
总测试数: 11
通过: 11
失败: 0
通过率: 100.0%
```

### 方法二：手动验证

**1. 测试健康检查端点**

```bash
curl http://localhost:8000/api/v1/monitoring/health
```

**2. 测试监控指标端点**

```bash
curl http://localhost:8000/api/v1/monitoring/metrics
```

**3. 触发Agent请求（产生监控数据）**

```bash
curl -X POST http://localhost:8000/api/v1/agent/react-stream/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"你好，测试监控","work_id":"test_001","mode":"chat"}'
```

**4. 再次查看监控指标**

```bash
curl http://localhost:8000/api/v1/monitoring/metrics
```

应该能看到指标增加（api_requests_total, llm_calls_total等）

---

## ✅ 验证检查清单

### API层监控 ✅

- [ ] `api_requests_total` - API总请求数
- [ ] `api_requests_success` - 成功请求数
- [ ] `api_requests_error` - 错误请求数
- [ ] `api_request_duration` - 请求响应时间

### Agent层监控 ✅

- [ ] `intent_classification_duration` - 意图识别耗时
- [ ] `prompt_render_duration` - Prompt渲染耗时
- [ ] `context_build_duration` - 上下文构建耗时
- [ ] `graph_execution_duration` - 图执行耗时
- [ ] `chat_stream_total_duration` - 总执行耗时

### LLM层监控 ✅

- [ ] `llm_calls_total` - LLM总调用数
- [ ] `llm_calls_success` - 成功调用数
- [ ] `llm_calls_error` - 错误调用数
- [ ] `llm_response_time` - LLM响应时间
- [ ] `llm_token_usage_*` - Token使用量

### MonitoringCallback验证 ✅

- [ ] 查看backend日志，确认有 `[MonitoringCallback]` 输出
- [ ] 确认每次LLM调用都有 `on_llm_start` 和 `on_llm_end` 日志
- [ ] 确认Token统计正确

---

## 📊 监控覆盖率计算

### 预期覆盖率

| 层级 | 覆盖的调用路径 | 目标覆盖率 |
|------|---------------|-----------|
| API层 | 所有 `/api/v1/*` 端点 | 100% |
| Agent层 | 所有 `_handle_*` 节点 | 100% |
| LLM层 | 所有 ChatOpenAI 调用 | 100% |

### 覆盖率验证方法

1. **查看日志文件**

```bash
cd backend
tail -f logs/app.log | findstr "MonitoringCallback"
```

2. **分析监控指标**

运行完监控验证脚本后，检查：
- API请求数应该 > 0
- LLM调用数应该 > 0
- 所有场景（general/writing/planning/analysis/stuck）都应该有指标

3. **计算覆盖率**

```
覆盖率 = (实际监控的LLM调用数 / 总LLM调用数) × 100%
```

对于P0-P2重构后的架构，预期覆盖率 = **100%**

---

## 🐛 常见问题

### Q1: 服务启动失败

**问题**：ModuleNotFoundError 或导入错误

**解决**：
```bash
cd backend
pip install -r requirements.txt
```

### Q2: 数据库连接错误

**问题**：Database connection failed

**解决**：
1. 检查 `.env` 中的 `DATABASE_URL` 配置
2. 确保PostgreSQL服务运行中
3. 或者使用 SQLite：`DATABASE_URL=sqlite:///./test.db`

### Q3: 监控指标为空

**问题**：访问 `/api/v1/monitoring/metrics` 返回空数据

**解决**：
1. 先触发几个Agent请求产生数据
2. 检查backend日志是否有错误
3. 确认监控中间件已启用（检查 `app/main.py`）

### Q4: MonitoringCallback未触发

**问题**：日志中没有 `[MonitoringCallback]` 输出

**解决**：
1. 检查 `backend/app/services/agent/langgraph_agent.py` 中ChatOpenAI的callbacks配置
2. 确认 `backend/app/api/callbacks/monitoring_callback.py` 文件存在
3. 重启backend服务

---

## 📝 验证报告模板

完成验证后，记录以下信息：

```
## Phase 2 监控验证报告

**验证时间**：2025-01-07

### 测试结果
- 总测试数：__
- 通过：__
- 失败：__
- 通过率：__%

### API层监控
- api_requests_total: __
- api_requests_success: __
- api_requests_error: __

### LLM层监控
- llm_calls_total: __
- llm_calls_success: __
- llm_calls_error: __
- 平均响应时间: __ ms

### MonitoringCallback
- [x] 日志中有MonitoringCallback输出
- [x] on_llm_start 触发正常
- [x] on_llm_end 触发正常
- [x] Token统计正确

### 监控覆盖率
- API层: __%
- Agent层: __%
- LLM层: __%
- **整体: __%**

### 结论
- [ ] 监控系统工作正常
- [ ] 覆盖率达到100%
- [ ] 准备投入生产
```

---

## 🚀 下一步

验证通过后：

1. ✅ **更新文档**
   - 记录监控验证结果到 `docs/Agent/tasks/P2_完成总结.md`
   - 更新 `tasks/todo.md`

2. ✅ **生产环境准备**
   - 配置Prometheus（如需要）
   - 设置监控告警
   - 配置日志聚合

3. ✅ **持续监控**
   - 定期检查监控指标
   - 分析性能瓶颈
   - 优化慢查询

---

**准备好了吗？启动backend服务并运行监控验证！** 🚀
