# Phase 3: 测试和验证计划

**阶段**: Phase 3
**预计时间**: 2-3天
**状态**: ⏸️ 待开始
**依赖**: Phase 1和Phase 2完成

---

## 🎯 阶段目标

全面测试Chat模式优化的各项功能，确保质量、性能和稳定性达标。

---

## 📋 Day 1: 单元测试和集成测试

### 上午 (4小时): 核心功能单元测试

#### 测试范围:
- [ ] **ContextManager测试**
  - 上下文构建
  - 上下文更新
  - Token预算控制
  - 摘要生成
  - 长期记忆（如果实现）

- [ ] **PromptManager测试**
  - 模板加载
  - 模板渲染
  - 参数注入
  - 版本管理

- [ ] **API端点测试**
  - mode参数处理
  - React模式
  - Planning模式
  - 错误处理

**执行命令**:
```bash
cd backend
python -m pytest tests/ -v --cov=app --cov-report=html
```

**验收标准**:
- [ ] 所有单元测试通过
- [ ] 代码覆盖率 > 80%
- [ ] 无严重bug

---

### 下午 (4小时): 端到端集成测试

#### 测试场景:

1. **React模式完整流程**
```python
async def test_react_mode_e2e():
    # 1. 发送用户消息
    # 2. 意图识别
    # 3. Agent执行
    # 4. 工具调用（如需要）
    # 5. 响应生成
    # 6. 上下文更新
```

2. **Planning模式兼容性**
```python
async def test_planning_mode_compatibility():
    # 确保现有Planning模式不受影响
```

3. **模式切换测试**
```python
async def test_mode_switching():
    # 同一会话在不同模式间切换
```

**验收标准**:
- [ ] 所有集成测试通过
- [ ] React模式功能完整
- [ ] Planning模式不受影响
- [ ] 模式切换正常

---

## 📋 Day 2: 性能测试和边缘case

### 上午 (4小时): 性能基准测试

#### 响应时间测试:
```python
async def test_response_time():
    """
    测试目标:
    - 简单对话: < 2秒
    - 复杂任务: < 10秒
    - 工具调用: < 15秒
    """
```

#### Token使用测试:
```python
async def test_token_usage():
    """
    测试目标:
    - 对比优化前后
    - 降低30-50%
    - 长对话<80%窗口
    """
```

#### 并发性能测试:
```bash
# 使用locust或类似工具
locust -f tests/load_test.py --users 100 --spawn-rate 10
```

**性能指标**:
| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| 简单对话响应时间 | <2s | - | - |
| 复杂任务响应时间 | <10s | - | - |
| Token降低比例 | 30-50% | - | - |
| 并发处理能力 | 100 QPS | - | - |

---

### 下午 (4小时): 边缘case测试

#### 测试用例:

1. **极长消息**
```python
async def test_very_long_message():
    message = "很长的消息 " * 1000
    # 测试是否正确处理
```

2. **快速连续请求**
```python
async def test_rapid_requests():
    tasks = [
        agent.chat_stream(f"消息{i}")
        for i in range(10)
    ]
    await asyncio.gather(*tasks)
```

3. **并发请求**
```python
async def test_concurrent_sessions():
    # 100个并发会话
```

4. **网络中断恢复**
```python
async def test_network_interruption():
    # 模拟网络中断
    # 验证恢复机制
```

5. **异常输入**
```python
async def test_invalid_inputs():
    # 空消息
    # 特殊字符
    # SQL注入尝试
    # XSS尝试
```

**验收标准**:
- [ ] 所有边缘case处理正确
- [ ] 无崩溃或死锁
- [ ] 错误提示友好

---

## 📋 Day 3: 长对话和压力测试

### 上午 (4小时): 长对话稳定性测试

#### 30轮对话测试:
```python
async def test_30_turn_conversation():
    session_id = "long_test_001"

    for turn in range(30):
        result = await agent.chat_stream(
            message=f"第{turn+1}轮对话",
            conversation_id=session_id
        )

        # 验证:
        # - 对话连贯性
        # - Token使用合理
        # - 响应质量稳定
```

#### 60轮对话测试:
```python
async def test_60_turn_conversation():
    # 更长的对话测试
    # 重点验证上下文压缩
```

#### Token管理验证:
- [ ] 每轮对话后检查Token使用
- [ ] 验证摘要生成质量
- [ ] 检查短期记忆管理

---

### 下午 (4小时): 压力测试和性能调优

#### 压力测试场景:

1. **高并发测试**
```bash
# 100个并发用户
ab -n 1000 -c 100 http://localhost:8000/api/v1/agent/chat/stream
```

2. **持续负载测试**
```bash
# 持续1小时
locust -f load_test.py --users 50 --run-time 1h
```

3. **资源使用监控**
```bash
# 监控CPU、内存、网络
top -b -n 60 >> performance.log
```

#### 性能调优:
- [ ] 识别性能瓶颈
- [ ] 优化慢查询
- [ ] 调整资源配置
- [ ] 缓存策略优化

**验收标准**:
- [ ] 100并发稳定运行
- [ ] 资源使用合理
- [ ] 无内存泄漏
- [ ] 响应时间稳定

---

## 📊 测试报告模板

### 测试执行摘要

**测试时间**: _____
**测试环境**: _____
**测试人员**: _____

#### 测试统计:
- 总测试用例数: _____
- 通过: _____
- 失败: _____
- 跳过: _____
- 覆盖率: _____%

#### 性能指标:
| 指标 | 目标 | 实际 | 达标 |
|------|------|------|------|
| 简单对话响应 | <2s | ___ | ☐ |
| 复杂任务响应 | <10s | ___ | ☐ |
| Token降低 | 30-50% | ___ | ☐ |
| 30轮对话稳定性 | 稳定 | ___ | ☐ |
| 并发处理 | 100 QPS | ___ | ☐ |

#### 发现的问题:
| 编号 | 描述 | 严重性 | 状态 |
|------|------|--------|------|
| 1 | ___ | ___ | ___ |

---

## ✅ Phase 3 完成标准

### 必须完成:
- [ ] 所有单元测试通过 (覆盖率>80%)
- [ ] 所有集成测试通过
- [ ] 性能指标达标
- [ ] 长对话测试通过
- [ ] 无严重bug

### 输出产物:
- [ ] 测试报告
- [ ] 性能分析报告
- [ ] 问题清单
- [ ] 优化建议

---

## ⏭️ 下一步

**Phase 3完成后**:
1. 召开测试评审会议
2. 确认是否开始Phase 4
3. 准备灰度发布计划

**如果未通过**:
1. 修复关键问题
2. 重新测试
3. 调整发布计划

---

**负责人**: _____
**测试时间**: _____
**状态**: ⏸️ 待开始
