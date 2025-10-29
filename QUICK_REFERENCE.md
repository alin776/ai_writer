# LangGraph Agent 双模式快速参考

## 当前状态

✅ **模式**: HTTPAIService（绕过 Cloudflare）
✅ **配置**: `AGENT_USE_CHATGPT=false`
✅ **状态**: 生产可用

---

## 快速切换

### 使用 HTTPAIService（当前）

```bash
# .env
AGENT_USE_CHATGPT=false
```

```bash
# 重启服务
cd backend
./venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

### 切换到 ChatOpenAI（未来）

```bash
# .env
AGENT_USE_CHATGPT=true
```

```bash
# 重启服务
cd backend
./venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

---

## 测试

```bash
cd backend
./venv/Scripts/python.exe test_langgraph_modes.py
```

---

## API 调用

```bash
curl -X POST "http://localhost:8000/api/v1/agent/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "我卡文了，不知道该怎么继续写下去"
  }'
```

---

## 核心文件

- `backend/app/services/agent/langgraph_agent.py` - 主实现（745行）
- `backend/app/api/v1/agent.py` - API端点
- `backend/app/core/config.py` - 配置
- `backend/test_langgraph_modes.py` - 测试脚本

---

## 文档

- `LANGGRAPH_DUAL_MODE_GUIDE.md` - 详细使用指南
- `LANGGRAPH_IMPLEMENTATION_SUMMARY.md` - 实现总结
- `AI写作平台Agent化改造方案.md` - 总体架构

---

## 故障排查

### Cloudflare 阻断
```
抱歉，处理您的请求时出错了：<!DOCTYPE html>...Cloudflare...
```

**解决**：确认 `AGENT_USE_CHATGPT=false`

### 工具调用失败
```
[ERROR] No AIMessage found in input
```

**解决**：检查模式配置是否正确

---

## 关键日志

```
[LangGraph] 使用 HTTPAIService 模式（手动工具调用，绕过 Cloudflare）
[LangGraph] 意图分类
[LangGraph] 路由到: stuck
[LangGraph] 处理stuck场景 (use_chatgpt=False)
[LangGraph] stuck 决策 (HTTPAIService): True
[LangGraph] stuck - 处理工具执行结果 (HTTPAIService)
```

---

## 模式对比

| 特性 | HTTPAIService | ChatOpenAI |
|------|--------------|------------|
| Cloudflare | ✅ 绕过 | ❌ 阻断 |
| 性能 | 多一次调用 | 更快 |
| 准确性 | JSON解析 | 原生 |
| 推荐 | 当前生产 | 未来 |
