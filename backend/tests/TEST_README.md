# Phase 1.2 上下文管理 - 测试指南

## 📋 测试概览

本目录包含Phase 1.2上下文管理的完整测试套件：

| 测试类型 | 文件 | 描述 | 预计时间 |
|---------|------|------|---------|
| **单元测试** | `test_context_manager.py` | 测试Context Manager核心功能 | 10秒 |
| **集成测试** | `test_e2e_context_integration.py` | 测试chat_stream与上下文管理集成 | 2分钟 |
| **长对话测试** | `test_long_conversation_30.py` | 测试30轮对话的Token管理 | 5-10分钟 |
| **测试运行器** | `run_all_tests.py` | 一键运行所有测试 | ~15分钟 |

## 🚀 快速开始

### 方法1: 运行所有测试（推荐）

```bash
cd backend/tests
python run_all_tests.py
```

这会自动运行所有测试并生成完整报告。

### 方法2: 运行单个测试

**运行单元测试:**
```bash
cd backend
python -m pytest tests/test_context_manager.py -v
```

**运行集成测试:**
```bash
cd backend/tests
python test_e2e_context_integration.py
```

**运行长对话测试:**
```bash
cd backend/tests
python test_long_conversation_30.py
```

## ✅ 验收标准

Phase 1.2完成的标志是所有测试通过：

### 1. 单元测试 (8个测试用例)
- ✅ 新会话上下文构建
- ✅ 上下文更新
- ✅ Token预算控制
- ✅ 上下文压缩
- ✅ 上下文持久化
- ✅ 清除上下文
- ✅ 多会话隔离

### 2. 集成测试 (5个测试点)
- ✅ 首次对话正常
- ✅ 历史对话加载
- ✅ 多轮对话连续性
- ✅ 会话隔离
- ✅ 元数据完整

### 3. 长对话测试 (5个验收点)
- ✅ Token使用 < 90%预算
- ✅ 压缩机制生效
- ✅ 短期记忆限制 ≤ 12条
- ✅ 摘要生成成功
- ✅ 30轮对话完成

## 📊 预期结果

### Token使用趋势
在30轮对话中，Token使用应该呈现如下模式：
```
轮次 1-10:  逐渐上升 (500 → 3000)
轮次 11-20: 触发压缩，下降后再上升 (3000 → 2000 → 3500)
轮次 21-30: 保持稳定，不超过80%预算 (3000 → 4000)
```

### 压缩效果
- 触发次数: 2-5次
- 每次压缩后Token降低: 30-50%
- 摘要生成: 包含关键对话信息

## 🐛 常见问题

### Q: 测试失败 - Redis连接错误
**A:** 上下文管理使用Redis存储。确保Redis运行：
```bash
# Windows
redis-server

# Linux/Mac
redis-server
```

测试使用内存存储，不需要Redis也能运行。

### Q: 长对话测试超时
**A:** 长对话测试需要调用30次LLM，耗时5-10分钟是正常的。如果超过20分钟，可能是：
- LLM服务响应慢
- 网络连接问题
- 配置的模型不可用

### Q: Token计数不准确
**A:** Token计数使用简单的字符数/4估算。实际Token数可能有10-20%误差，这是正常的。

## 📝 测试输出示例

成功的测试输出应该类似：

```
============================================================
Phase 1.2 上下文管理 - 自动测试套件
============================================================

============================================================
测试1: 单元测试 (pytest)
============================================================
ℹ 运行: 单元测试
  命令: python -m pytest test_context_manager.py -v

test_build_context_new_session PASSED
test_update_context PASSED
test_token_budget_control PASSED
...
✓ 单元测试 - 通过

============================================================
测试总结
============================================================
测试结果:
  总测试套件: 3
  通过: 3
  失败: 0

✅ 所有测试通过！Phase 1.2 验收成功！
```

## 🔧 故障排除

如果测试失败，请检查：

1. **环境配置**
   - Python 3.8+
   - 已安装依赖: `pip install -r requirements.txt`
   - Redis运行中（如果使用RedisContextStore）

2. **代码完整性**
   - 所有模块文件存在
   - `app/services/context/` 目录完整
   - `langgraph_agent.py` 已集成ContextManager

3. **配置正确**
   - `settings.py` 中Redis配置正确
   - LLM服务可访问
   - API密钥有效

## 📞 获取帮助

如果测试仍然失败，请提供以下信息：
- 失败的测试名称
- 完整错误信息
- Python版本
- 依赖版本 (`pip list | grep -E "langgraph|langchain|redis"`)
