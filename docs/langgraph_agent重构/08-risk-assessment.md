# 风险评估与回滚方案

## 文档版本
- 版本：1.1
- 日期：2025-12-19
- 更新：更新工具数量统计

---

## 一、风险矩阵

### 1.1 风险等级定义

| 等级 | 概率 | 影响 | 说明 |
|------|------|------|------|
| 🔴 高风险 | >50% | 严重 | 需要预案，优先处理 |
| 🟡 中风险 | 20-50% | 中等 | 需要监控，准备方案 |
| 🟢 低风险 | <20% | 轻微 | 知晓即可 |

### 1.2 风险清单

| ID | 风险描述 | 概率 | 影响 | 等级 | 应对策略 |
|----|----------|------|------|------|----------|
| R1 | Deep Agents 依赖版本冲突 | 30% | 高 | 🟡 | 提前验证，固定版本 |
| R2 | 性能退化超过 20% | 20% | 高 | 🟡 | 性能测试，优化或回滚 |
| R3 | 功能遗漏导致用户投诉 | 40% | 中 | 🟡 | 完整测试，快速修复 |
| R4 | interrupt 机制前端适配问题 | 50% | 中 | 🟡 | 提前联调，降级方案 |
| R5 | 记忆系统数据丢失 | 10% | 高 | 🟢 | 数据备份，迁移脚本 |
| R6 | 上线后大面积故障 | 10% | 极高 | 🟡 | 灰度发布，一键回滚 |
| R7 | 工具迁移不完整 | 30% | 中 | 🟡 | 工具清单，逐个验证 |
| R8 | Token 消耗异常增加 | 20% | 中 | 🟢 | 成本监控，预算限制 |

---

## 二、详细风险分析

### 2.1 R1: 依赖版本冲突

**风险描述：**
Deep Agents 依赖的 langgraph/langchain 版本与现有版本不兼容。

**影响范围：**
- 安装失败
- 运行时报错
- 功能异常

**预防措施：**
```bash
# 1. 在独立虚拟环境测试
python -m venv test_env
source test_env/bin/activate
pip install deepagents

# 2. 验证现有依赖
pip install -r requirements.txt
python -c "import deepagents; import langgraph; print('OK')"

# 3. 固定版本
# requirements.txt
deepagents==1.0.0
langgraph==1.0.1
langchain==1.0.2
```

**应对方案：**
```
若发生冲突：
1. 尝试升级现有依赖到兼容版本
2. 若无法升级，考虑 fork deepagents 修改依赖
3. 最坏情况：放弃 Deep Agents，手动实现 interrupt
```

### 2.2 R2: 性能退化

**风险描述：**
新系统响应时间、吞吐量等指标低于旧系统。

**影响范围：**
- 用户体验下降
- 服务器资源消耗增加

**监控指标：**
```python
# 性能监控点
metrics = {
    "first_response_time": "首次响应时间",
    "stream_first_token": "流式首字延迟",
    "total_latency": "总延迟",
    "memory_usage": "内存占用",
    "cpu_usage": "CPU 使用率",
    "tokens_per_request": "每请求 Token 数"
}
```

**性能基线：**
| 指标 | 旧系统 | 新系统目标 | 触发回滚阈值 |
|------|--------|-----------|-------------|
| 首次响应 | 2s | ≤2s | >3s |
| 流式首字 | 500ms | ≤500ms | >1s |
| P99 延迟 | 10s | ≤10s | >15s |
| 内存占用 | 500MB | ≤500MB | >800MB |

**应对方案：**
```
若性能不达标：
1. 分析性能瓶颈（使用 profiler）
2. 优化中间件（减少不必要的处理）
3. 优化工具调用（缓存、并行）
4. 若无法优化，回滚到旧系统
```

### 2.3 R3: 功能遗漏

**风险描述：**
迁移过程中遗漏某些功能，导致用户使用异常。

**高风险功能清单：**
| 功能 | 现有位置 | 迁移状态 | 验证方法 |
|------|----------|----------|----------|
| 智能改写多版本 | editor_tools.py | 待迁移 | E2E 测试 |
| 章节一致性检查 | consistency_checker.py | 待迁移 | 单元测试 |
| 风格适配 | style_adapter.py | 待迁移 | 单元测试 |
| 长期记忆召回 | memory/*.py | 待迁移 | 集成测试 |
| Token 预算管理 | context/*.py | 待迁移 | 集成测试 |

**预防措施：**
```python
# 功能对照检查表
FEATURE_CHECKLIST = [
    ("基本对话", "test_basic_chat"),
    ("续写功能", "test_continue_writing"),
    ("改写多版本", "test_smart_rewrite"),
    ("文本分析", "test_analyze_text"),
    ("一致性检查", "test_consistency_check"),
    ("记忆召回", "test_memory_recall"),
    ("Token 预算", "test_token_budget"),
    # ...
]

# 迁移验证脚本
def verify_feature_migration():
    for feature, test_name in FEATURE_CHECKLIST:
        result = run_test(test_name)
        if not result.passed:
            raise MigrationError(f"功能遗漏: {feature}")
```

### 2.4 R4: 前端适配问题

**风险描述：**
interrupt 机制需要前端配合，可能出现联调问题。

**影响范围：**
- 中断 UI 不显示
- 用户无法响应
- 流程卡死

**接口契约：**
```typescript
// SSE 事件格式
interface InterruptEvent {
  type: "interrupt";
  data: {
    interrupt_id: string;
    interrupt_type: "confirmation" | "select_version" | "text_input";
    message: string;
    options?: Array<{value: string, label: string}>;
    versions?: Array<{id: number, content: string, style: string}>;
  }
}

// 恢复请求格式
interface ResumeRequest {
  thread_id: string;
  interrupt_id: string;
  response: string | number | object;
}
```

**降级方案：**
```python
# 如果前端未适配，使用简化模式
class InterruptFallback:
    """中断降级处理"""

    @staticmethod
    async def handle(interrupt_data: dict) -> any:
        interrupt_type = interrupt_data.get("type")

        if interrupt_type == "confirmation":
            # 默认确认
            return "确认"

        elif interrupt_type == "select_version":
            # 默认选第一个
            return 1

        elif interrupt_type == "text_input":
            # 跳过输入
            return ""

        return None
```

### 2.5 R5: 记忆数据丢失

**风险描述：**
迁移过程中记忆数据丢失或损坏。

**预防措施：**
```bash
# 1. 数据备份
redis-cli BGSAVE
cp /var/lib/redis/dump.rdb /backup/redis_$(date +%Y%m%d).rdb

# 2. ChromaDB 备份
cp -r /data/chromadb /backup/chromadb_$(date +%Y%m%d)

# 3. 验证备份完整性
python scripts/verify_backup.py
```

**恢复脚本：**
```python
# scripts/restore_memory.py

async def restore_memory_data(backup_date: str):
    """从备份恢复记忆数据"""

    # 1. 恢复 Redis
    redis_backup = f"/backup/redis_{backup_date}.rdb"
    await restore_redis(redis_backup)

    # 2. 恢复 ChromaDB
    chroma_backup = f"/backup/chromadb_{backup_date}"
    await restore_chromadb(chroma_backup)

    # 3. 验证数据完整性
    await verify_data_integrity()

    print(f"记忆数据已从 {backup_date} 备份恢复")
```

### 2.6 R6: 上线后大面积故障

**风险描述：**
上线后出现严重 bug 导致服务不可用。

**预防措施：**
1. 灰度发布（10% → 50% → 100%）
2. 每阶段观察至少 1 小时
3. 实时监控告警
4. 准备一键回滚

**告警规则：**
```yaml
# alerting_rules.yml
groups:
  - name: deep_agents_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(agent_errors_total[5m]) > 0.01
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Agent 错误率超过 1%"

      - alert: CriticalErrorRate
        expr: rate(agent_errors_total[5m]) > 0.05
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agent 错误率超过 5%，触发自动回滚"

      - alert: HighLatency
        expr: histogram_quantile(0.99, agent_latency_bucket) > 15
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P99 延迟超过 15 秒"
```

---

## 三、回滚方案

### 3.1 回滚触发条件

| 条件 | 自动/手动 | 说明 |
|------|----------|------|
| 错误率 > 5% 持续 1 分钟 | 自动 | 严重故障 |
| P99 延迟 > 15s 持续 5 分钟 | 手动 | 性能问题 |
| 用户投诉超过 10 个 | 手动 | 功能问题 |
| 内存泄漏 | 手动 | 稳定性问题 |

### 3.2 回滚步骤

#### 快速回滚（功能开关）

```bash
# 1. 关闭功能开关
curl -X POST http://localhost:8000/admin/config \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"USE_DEEP_AGENTS": false}'

# 2. 验证回滚生效
curl http://localhost:8000/api/v1/agent/status
# 应返回 {"engine": "legacy"}

# 3. 监控确认
# 观察错误率是否下降
```

#### 完整回滚（代码回滚）

```bash
# 1. 停止服务
docker-compose stop backend

# 2. 代码回滚
git checkout HEAD~1 -- backend/app/services/agent/
# 或
git revert <commit_hash>

# 3. 恢复旧代码
cp -r backend/app/services/agent/legacy/* backend/app/services/agent/

# 4. 重启服务
docker-compose up -d backend

# 5. 验证服务
curl http://localhost:8000/health
```

### 3.3 回滚验证清单

- [ ] 服务正常启动
- [ ] 健康检查通过
- [ ] 基本对话功能正常
- [ ] 错误率恢复正常
- [ ] 延迟恢复正常
- [ ] 用户反馈正常

---

## 四、应急响应流程

### 4.1 故障等级定义

| 等级 | 定义 | 响应时间 | 处理时间 |
|------|------|----------|----------|
| P0 | 服务完全不可用 | 5 分钟 | 30 分钟 |
| P1 | 核心功能不可用 | 15 分钟 | 2 小时 |
| P2 | 部分功能异常 | 30 分钟 | 4 小时 |
| P3 | 轻微问题 | 2 小时 | 24 小时 |

### 4.2 应急响应流程

```
┌─────────────────────────────────────────────────────────┐
│                     故障发生                            │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   1. 故障确认                           │
│  - 检查监控告警                                         │
│  - 验证用户反馈                                         │
│  - 确定影响范围                                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   2. 等级评估                           │
│  - 根据影响范围确定等级                                 │
│  - 通知相关人员                                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   3. 快速止血                           │
│  - P0/P1: 立即回滚                                     │
│  - P2/P3: 评估是否需要回滚                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   4. 根因分析                           │
│  - 收集日志                                             │
│  - 分析调用链                                           │
│  - 定位问题代码                                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   5. 修复验证                           │
│  - 开发修复                                             │
│  - 测试验证                                             │
│  - 灰度发布                                             │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│                   6. 复盘总结                           │
│  - 编写故障报告                                         │
│  - 改进措施                                             │
│  - 更新文档                                             │
└─────────────────────────────────────────────────────────┘
```

### 4.3 故障报告模板

```markdown
# 故障报告

## 基本信息
- 故障时间：YYYY-MM-DD HH:MM - HH:MM
- 故障等级：P0/P1/P2/P3
- 影响范围：XX 用户 / XX 功能

## 故障描述
简要描述故障现象

## 时间线
- HH:MM 告警触发
- HH:MM 确认故障
- HH:MM 执行回滚
- HH:MM 服务恢复

## 根因分析
详细分析故障原因

## 修复方案
如何修复的

## 改进措施
- [ ] 措施1
- [ ] 措施2
```

---

## 五、监控与告警

### 5.1 监控指标

```python
# 关键监控指标
METRICS = {
    # 可用性
    "agent_requests_total": "请求总数",
    "agent_errors_total": "错误总数",
    "agent_success_rate": "成功率",

    # 性能
    "agent_latency_seconds": "请求延迟",
    "agent_first_token_seconds": "首字延迟",
    "agent_stream_duration_seconds": "流式总时长",

    # 资源
    "agent_memory_bytes": "内存使用",
    "agent_cpu_percent": "CPU 使用率",
    "agent_active_threads": "活跃线程数",

    # 业务
    "agent_tokens_used": "Token 使用量",
    "agent_interrupt_count": "中断次数",
    "agent_resume_count": "恢复次数",
}
```

### 5.2 Grafana 仪表盘

```
┌─────────────────────────────────────────────────────────┐
│                Deep Agents 监控仪表盘                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  成功率     │  │  P99延迟    │  │  错误率     │    │
│  │   99.5%    │  │   2.3s     │  │   0.5%     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │              请求量趋势图                        │  │
│  │  ▃▅▆▇▆▅▃▂▃▅▆▇▇▆▅▄▃▂▁▂▃▄▅▆▇▆▅▄▃               │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐  │
│  │              延迟分布图                          │  │
│  │  P50: 0.8s  P90: 1.5s  P99: 2.3s               │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 六、检查清单

### 6.1 上线前检查

- [ ] 所有测试通过
- [ ] 性能基准达标
- [ ] 监控告警配置完成
- [ ] 回滚脚本测试通过
- [ ] 数据备份完成
- [ ] 团队成员 on-call 安排

### 6.2 上线中检查

- [ ] 灰度比例按计划执行
- [ ] 监控指标正常
- [ ] 无告警触发
- [ ] 用户反馈正常

### 6.3 上线后检查

- [ ] 全量运行稳定 24 小时
- [ ] 无 P0/P1 故障
- [ ] 性能指标稳定
- [ ] 旧代码归档完成

---

## 七、总结

### 7.1 关键风险

1. **依赖兼容性** - 提前验证，固定版本
2. **性能退化** - 性能测试，监控告警
3. **功能遗漏** - 完整测试，功能清单
4. **前端适配** - 提前联调，降级方案

### 7.2 关键保障

1. **灰度发布** - 降低影响范围
2. **功能开关** - 快速回滚能力
3. **监控告警** - 及时发现问题
4. **数据备份** - 防止数据丢失

### 7.3 成功标准

- 全量发布后 24 小时无 P0/P1 故障
- 性能指标不低于旧系统
- 用户无感知切换
- interrupt/resume 功能正常

---

## 八、附录

### A. 相关文档

- [00-overview.md](./00-overview.md) - 重构概述
- [01-current-analysis.md](./01-current-analysis.md) - 现状分析
- [07-implementation-plan.md](./07-implementation-plan.md) - 实施计划

### B. 联系人

| 角色 | 负责人 | 联系方式 |
|------|--------|----------|
| 技术负责人 | - | - |
| 前端负责人 | - | - |
| 运维负责人 | - | - |

### C. 相关工具

- 监控：Prometheus + Grafana
- 告警：AlertManager
- 日志：ELK Stack
- 回滚：Git + Docker
