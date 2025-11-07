# Phase 4: 部署和灰度发布

**阶段**: Phase 4
**预计时间**: 持续进行
**状态**: ⏸️ 待开始
**依赖**: Phase 3完成且通过验收

---

## 🎯 阶段目标

安全地将Chat模式优化部署到生产环境，通过灰度发布逐步切换流量，持续监控和优化。

---

## 📋 部署准备 (1-2天)

### 任务1: Code Review和文档

#### Code Review清单:
- [ ] 所有代码通过团队review
- [ ] 代码规范符合标准
- [ ] 注释完整清晰
- [ ] 无安全隐患
- [ ] 无明显性能问题

#### 文档清单:
- [ ] API文档更新
- [ ] 部署文档编写
- [ ] 运维手册更新
- [ ] 回滚方案文档

---

### 任务2: 部署脚本准备

#### 部署脚本:
```bash
# deploy.sh
#!/bin/bash

echo "=== 部署Chat优化功能 ==="

# 1. 备份当前版本
echo "1. 备份当前版本..."
cp -r /app/current /app/backup_$(date +%Y%m%d_%H%M%S)

# 2. 停止服务
echo "2. 停止服务..."
supervisorctl stop app:*

# 3. 更新代码
echo "3. 更新代码..."
git pull origin main
pip install -r requirements.txt

# 4. 数据库迁移（如需要）
echo "4. 数据库迁移..."
# alembic upgrade head

# 5. 启动服务
echo "5. 启动服务..."
supervisorctl start app:*

# 6. 健康检查
echo "6. 健康检查..."
sleep 5
curl -f http://localhost:8000/health || exit 1

echo "=== 部署完成 ==="
```

#### 回滚脚本:
```bash
# rollback.sh
#!/bin/bash

echo "=== 回滚到上一版本 ==="

# 1. 停止服务
supervisorctl stop app:*

# 2. 恢复备份
BACKUP_DIR=$(ls -t /app/backup_* | head -1)
rm -rf /app/current
cp -r $BACKUP_DIR /app/current

# 3. 启动服务
supervisorctl start app:*

# 4. 验证
curl -f http://localhost:8000/health

echo "=== 回滚完成 ==="
```

---

### 任务3: 监控和告警配置

#### Prometheus指标:
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'chat_optimization'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

#### 告警规则:
```yaml
# alert_rules.yml
groups:
  - name: chat_optimization
    rules:
      - alert: HighErrorRate
        expr: rate(chat_errors_total[5m]) > 0.05
        labels:
          severity: critical
        annotations:
          summary: "Chat错误率过高"

      - alert: SlowResponse
        expr: histogram_quantile(0.99, chat_stream_duration) > 10
        labels:
          severity: warning
        annotations:
          summary: "Chat响应时间过长"

      - alert: HighTokenUsage
        expr: token_usage_total > 7000
        labels:
          severity: warning
        annotations:
          summary: "Token使用量过高"
```

---

## 📋 灰度发布计划

### 灰度策略总览

```
Phase 1: 10%流量  (Week 1)  → 观察1周
Phase 2: 30%流量  (Week 2)  → 观察1周
Phase 3: 50%流量  (Week 3-4) → 观察2周
Phase 4: 90%流量  (Week 5-8) → 观察1月
Phase 5: 100%流量 (Week 9+)  → Planning降级为备用
```

---

### Phase 4.1: 10%流量 (Week 1)

#### 配置灰度规则:
```python
# config/feature_flags.py
CHAT_OPTIMIZATION_ROLLOUT = {
    "enabled": True,
    "percentage": 10,  # 10%流量
    "whitelist": [      # 白名单用户
        "internal_tester_1",
        "internal_tester_2"
    ],
    "blacklist": []     # 黑名单用户
}

def should_use_chat_optimization(user_id: str) -> bool:
    """判断用户是否使用优化版本"""
    config = CHAT_OPTIMIZATION_ROLLOUT

    if not config["enabled"]:
        return False

    # 白名单用户
    if user_id in config["whitelist"]:
        return True

    # 黑名单用户
    if user_id in config["blacklist"]:
        return False

    # 按比例灰度
    hash_value = hash(user_id) % 100
    return hash_value < config["percentage"]
```

#### 监控重点:
- [ ] 错误率 (目标: <1%)
- [ ] 响应时间 (目标: ≤Planning模式)
- [ ] Token使用 (目标: -30~50%)
- [ ] 用户反馈 (目标: 无重大投诉)

#### 每日检查清单:
- [ ] 查看错误日志
- [ ] 检查性能指标
- [ ] 收集用户反馈
- [ ] 更新灰度报告

---

### Phase 4.2: 30%流量 (Week 2)

**前提条件**:
- [ ] 10%灰度运行稳定
- [ ] 无重大问题
- [ ] 性能指标达标

**执行**:
```python
CHAT_OPTIMIZATION_ROLLOUT["percentage"] = 30
```

**监控强化**:
- [ ] 增加监控采样率
- [ ] 建立告警机制
- [ ] 每日数据分析

---

### Phase 4.3: 50%流量 (Week 3-4)

**前提条件**:
- [ ] 30%灰度运行稳定2周
- [ ] 用户满意度良好

**执行**:
```python
CHAT_OPTIMIZATION_ROLLOUT["percentage"] = 50
```

**重点验证**:
- [ ] 长期稳定性
- [ ] 成本节省效果
- [ ] 用户体验提升

---

### Phase 4.4: 90%流量 (Week 5-8)

**前提条件**:
- [ ] 50%灰度运行稳定1月
- [ ] 所有指标达标

**执行**:
```python
CHAT_OPTIMIZATION_ROLLOUT["percentage"] = 90
```

**最后验证**:
- [ ] 大规模稳定性
- [ ] 边缘case处理
- [ ] 准备100%切换

---

### Phase 4.5: 100%流量 (Week 9+)

**前提条件**:
- [ ] 90%灰度运行稳定1月
- [ ] 管理层批准

**执行**:
```python
CHAT_OPTIMIZATION_ROLLOUT["percentage"] = 100
```

**Planning模式降级**:
- 保留代码作为备用
- 可通过特殊参数启用
- 定期测试确保可用

---

## 📊 监控指标

### 核心指标看板

| 指标 | 优化前 | 目标 | 当前 | 达成率 |
|------|--------|------|------|--------|
| 平均响应时间 | - | ≤优化前 | - | - |
| P99响应时间 | - | <10s | - | - |
| 错误率 | - | <1% | - | - |
| Token使用 | - | -30~50% | - | - |
| 成本节省 | - | 70% | - | - |
| 用户满意度 | - | ≥优化前 | - | - |

---

## 🚨 应急响应

### 回滚触发条件:
- ❌ 错误率 > 5%
- ❌ 响应时间增加 > 50%
- ❌ 大量用户投诉
- ❌ 系统稳定性下降

### 回滚流程:
1. **立即通知**: 通知相关人员
2. **暂停灰度**: 停止流量切换
3. **执行回滚**: 运行rollback.sh
4. **验证恢复**: 确认服务正常
5. **问题分析**: 分析root cause
6. **修复计划**: 制定修复方案

---

## 📝 灰度报告模板

### Week N 灰度报告

**灰度比例**: ____%
**观察时间**: ___ 至 ___
**影响用户**: ___ 人

#### 核心指标:
- 错误率: ___ (<1%目标)
- 响应时间: ___ (≤优化前目标)
- Token节省: ___ (30-50%目标)

#### 用户反馈:
- 正面: ___ 条
- 负面: ___ 条
- 中性: ___ 条

#### 发现问题:
1. ___
2. ___

#### 下周计划:
- [ ] ___

---

## ✅ Phase 4 完成标准

### 100%流量切换标准:
- [ ] 所有灰度阶段顺利完成
- [ ] 核心指标全部达标
- [ ] 用户满意度良好
- [ ] 无重大问题遗留
- [ ] Planning模式备用方案可用

---

**负责人**: _____
**开始时间**: _____
**当前阶段**: _____
**状态**: ⏸️ 待开始
