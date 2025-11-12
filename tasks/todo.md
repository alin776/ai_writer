# 数据库连接泄漏Bug修复计划

## 问题概述
后台日志中发现**严重的数据库连接泄漏**问题，垃圾回收器正在尝试清理未归还连接池的数据库连接。

## 错误信息
```
sqlalchemy.pool.impl.AsyncAdaptedQueuePool ERROR
The garbage collector is trying to clean up non-checked-in connection
Please ensure that SQLAlchemy pooled connections are returned to the pool explicitly,
either by calling ``close()`` or by using appropriate context managers to manage their lifecycle.
```

## 发生位置（日志行号）
- 第311-319行：LangGraph Agent Stream处理时
- 第462-476行：AI续写请求时
- 第532-534行：小说分析服务启动时

## 待修复的任务清单

### Phase 1: 问题调查
- [ ] 检查 `backend/app/services/agent/langgraph_agent.py` 数据库连接使用
- [ ] 检查 `backend/app/services/ai/http_ai_service.py` 数据库连接使用
- [ ] 检查 `backend/app/services/novel_analysis_service.py` 数据库连接使用
- [ ] 检查数据库会话上下文管理器使用情况
- [ ] 识别所有未使用 `async with` 的数据库操作

### Phase 2: 代码修复
- [ ] 修复 LangGraph Agent 中的连接泄漏
- [ ] 修复 AI 服务中的连接泄漏
- [ ] 修复小说分析服务中的连接泄漏
- [ ] 确保所有数据库操作都使用上下文管理器
- [ ] 添加连接池监控日志

### Phase 3: 验证与测试
- [ ] 运行后台服务
- [ ] 测试Agent聊天功能
- [ ] 测试AI续写功能
- [ ] 测试小说分析功能
- [ ] 确认日志中无连接泄漏警告

### Phase 4: 其他问题
- [ ] 检查Redis连接超时问题（第567行）
- [ ] 优化Redis连接重试机制

---

## 次要问题

### Redis连接超时（非致命）
- 第567行：`Redis连接失败,缓存功能将禁用: Timeout connecting to server`
- 系统已做容错处理，降级为不使用缓存
- 需要检查Redis服务状态

---

## 下一步

等待用户确认此计划，然后开始调查和修复数据库连接泄漏问题。
