# Phase 2.1 监控系统集成 - 实施计划

**创建时间**: 2025-01-07
**预计工时**: 1-1.5天
**优先级**: P2 (生产环境必备)

---

## 📊 现状分析

### ✅ 已实现的监控系统

#### 1. monitoring.py (860行)
**位置**: `backend/app/services/agent/utils/monitoring.py`

**核心组件**:
- ✅ `MetricsCollector`: 指标收集器
  - Counter（计数器）
  - Gauge（仪表盘）
  - Histogram（直方图）
  - Timer（计时器）
- ✅ `HealthChecker`: 健康检查器
  - CPU/内存/磁盘检查
  - 自定义健康检查注册
- ✅ `AlertManager`: 告警管理器
  - 告警规则
  - 告警处理器
- ✅ `SystemMonitor`: 系统监控器（整合上述组件）

**已有功能**:
- 系统级监控（CPU、内存、磁盘、进程）
- 指标历史记录（可配置大小）
- 统计信息（min/max/mean/median）
- 告警检测和去重
- 异步监控循环

#### 2. business_metrics.py (711行)
**位置**: `backend/app/services/agent/utils/business_metrics.py`

**核心组件**:
- ✅ `BusinessMetricsCollector`: 业务指标收集器
  - 内容生成跟踪
  - 用户行为跟踪
  - LLM调用跟踪
  - 工具调用跟踪
  - 缓存操作跟踪

**已有功能**:
- 内容质量监控
- LLM性能监控
- 用户活动监控
- 业务健康检查
- 业务摘要报告

### ❌ 缺失的功能

1. **API层集成** - 完全未集成
   - `/agent/chat/stream` 端点无监控
   - `/agent/react/stream` 端点无监控
   - 无请求追踪（trace_id）
   - 无错误监控

2. **Agent关键节点监控** - 部分未集成
   - `chat_stream()` 方法无监控
   - 意图识别无监控
   - 上下文构建无监控
   - Prompt渲染无监控

3. **Prometheus导出** - 未实现
   - 无 `/metrics` 端点
   - 无Prometheus格式化

4. **结构化日志** - 未实现
   - 日志格式不统一
   - 缺少trace_id关联
   - 缺少关键字段（mode、intent等）

---

## 🎯 Phase 2.1 目标

### 主要目标
1. ✅ 将现有监控系统集成到API层和Agent关键节点
2. ✅ 实现Prometheus格式导出
3. ✅ 实现统一的结构化日志
4. ✅ 确保零侵入性（不影响现有功能）

### 成功标准
- [ ] 所有API请求都有监控（请求数、耗时、成功率）
- [ ] Agent关键节点都有计时监控
- [ ] 可以通过 `/metrics` 访问Prometheus格式指标
- [ ] 所有日志包含trace_id和关键业务字段
- [ ] 不影响现有功能，性能开销<5%

---

## 📋 实施计划

### Task 1: API层监控集成（3小时）

#### 1.1 创建监控中间件
**文件**: `backend/app/api/middleware/monitoring_middleware.py` (新建)

**功能**:
```python
class MonitoringMiddleware:
    """API监控中间件"""

    async def __call__(self, request, call_next):
        # 生成trace_id
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        # 记录请求开始
        start_time = time.time()
        path = request.url.path
        method = request.method

        # 增加请求计数
        increment_counter("api_requests_total",
                         labels={"path": path, "method": method})

        try:
            response = await call_next(request)

            # 记录成功
            increment_counter("api_requests_success",
                            labels={"path": path, "method": method})

            return response

        except Exception as e:
            # 记录失败
            increment_counter("api_requests_error",
                            labels={"path": path, "error_type": type(e).__name__})
            raise

        finally:
            # 记录耗时
            duration = time.time() - start_time
            record_timer("api_request_duration",
                        duration,
                        labels={"path": path, "method": method})
```

**工作量**: 1小时

#### 1.2 集成到agent.py端点
**文件**: `backend/app/api/v1/agent.py` (修改)

**修改点**:
```python
@router.post("/chat/stream")
async def agent_chat_stream(request: Request, ...):
    trace_id = request.state.trace_id
    start_time = time.time()

    # 业务监控
    increment_counter("chat_requests_total", labels={"mode": mode})

    try:
        async for event in langgraph_agent.chat_stream(...):
            # 注入trace_id到事件
            event["trace_id"] = trace_id
            yield event

        # 记录成功
        increment_counter("chat_success_total", labels={"mode": mode})

    except Exception as e:
        # 记录错误
        increment_counter("chat_errors_total",
                         labels={"mode": mode, "error": type(e).__name__})
        raise

    finally:
        # 记录总耗时
        record_timer("chat_duration", time.time() - start_time,
                    labels={"mode": mode})
```

**工作量**: 1小时

#### 1.3 创建 /metrics 端点
**文件**: `backend/app/api/v1/monitoring.py` (新建)

**功能**:
```python
@router.get("/metrics")
async def get_prometheus_metrics():
    """导出Prometheus格式的指标"""
    monitor = get_system_monitor()
    metrics_text = monitor.metrics_collector.export_prometheus()
    return Response(content=metrics_text, media_type="text/plain")

@router.get("/health")
async def health_check():
    """健康检查端点"""
    monitor = get_system_monitor()
    return monitor.get_monitoring_summary()

@router.get("/metrics/business")
async def get_business_metrics():
    """获取业务指标"""
    collector = get_business_metrics_collector()
    return collector.get_business_summary(time_window_hours=24)
```

**工作量**: 1小时

---

### Task 2: Agent关键节点监控（2小时）

#### 2.1 chat_stream 监控
**文件**: `backend/app/services/agent/langgraph_agent.py` (修改)

**修改点**:
```python
async def chat_stream(self, message: str, session_id: str, ...):
    """Chat流式执行 - 添加监控"""

    # 总体计时
    overall_start = time.time()

    try:
        # 上下文构建监控
        ctx_start = time.time()
        context_bundle = await self.context_manager.build_context(session_id)
        record_timer("context_build_duration", time.time() - ctx_start)

        # 意图识别监控
        intent_start = time.time()
        intent_data = await self._classify_intent_async(message)
        record_timer("intent_classification_duration", time.time() - intent_start)

        # 记录意图分布
        increment_counter("intent_distribution",
                         labels={"intent": intent_data["intent"]})

        # Prompt渲染监控
        prompt_start = time.time()
        system_prompt = self.prompt_manager.render(...)
        record_timer("prompt_render_duration", time.time() - prompt_start)

        # LangGraph执行监控
        graph_start = time.time()
        async for event in self.graph.astream(...):
            yield event
        record_timer("graph_execution_duration", time.time() - graph_start)

        # 记录成功
        increment_counter("chat_stream_success")

    except Exception as e:
        increment_counter("chat_stream_error",
                         labels={"error_type": type(e).__name__})
        raise

    finally:
        # 记录总耗时
        record_timer("chat_stream_total_duration",
                    time.time() - overall_start)
```

**影响范围**: 仅添加监控代码，不改变业务逻辑

**工作量**: 1.5小时

#### 2.2 LLM调用监控
**文件**: `backend/app/services/ai/http_ai_service.py` (修改)

**修改点**:
```python
async def _stream_chat(self, messages, ...):
    """流式聊天 - 添加监控"""

    start_time = time.time()

    try:
        # ... 现有逻辑

        # 记录Token使用
        if hasattr(response, 'usage'):
            set_gauge("llm_token_usage_prompt", response.usage.prompt_tokens,
                     labels={"model": model})
            set_gauge("llm_token_usage_completion", response.usage.completion_tokens,
                     labels={"model": model})

            # 业务监控
            track_llm_call(
                model=model,
                tokens_used={
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens
                },
                cost=cost,
                response_time=time.time() - start_time,
                success=True
            )

        increment_counter("llm_calls_success", labels={"model": model})

    except Exception as e:
        increment_counter("llm_calls_error",
                         labels={"model": model, "error": type(e).__name__})
        raise

    finally:
        record_timer("llm_response_time", time.time() - start_time,
                    labels={"model": model})
```

**工作量**: 0.5小时

---

### Task 3: Prometheus导出实现（1.5小时）

#### 3.1 实现 export_prometheus 方法
**文件**: `backend/app/services/agent/utils/monitoring.py` (修改)

**修改 MetricsCollector 类**:
```python
def export_prometheus(self) -> str:
    """导出Prometheus格式的指标"""
    lines = []

    with self._lock:
        # 导出计数器
        for key, value in self._counters.items():
            name, labels = self._parse_key(key)
            metric_name = f"{name}_total"

            # 添加HELP和TYPE
            lines.append(f"# HELP {metric_name} Total count of {name}")
            lines.append(f"# TYPE {metric_name} counter")

            # 添加指标
            if labels:
                label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
                lines.append(f"{metric_name}{{{label_str}}} {value}")
            else:
                lines.append(f"{metric_name} {value}")

        # 导出仪表盘
        for key, value in self._gauges.items():
            name, labels = self._parse_key(key)

            lines.append(f"# HELP {name} Current value of {name}")
            lines.append(f"# TYPE {name} gauge")

            if labels:
                label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
                lines.append(f"{name}{{{label_str}}} {value}")
            else:
                lines.append(f"{name} {value}")

        # 导出直方图统计
        for key, values in self._histograms.items():
            if not values:
                continue

            name, labels = self._parse_key(key)

            lines.append(f"# HELP {name} Histogram of {name}")
            lines.append(f"# TYPE {name} histogram")

            # 计算分位数
            sorted_values = sorted(values)
            count = len(sorted_values)
            total = sum(sorted_values)

            label_base = ",".join(f'{k}="{v}"' for k, v in labels.items()) if labels else ""

            # 分位数
            for quantile in [0.5, 0.9, 0.95, 0.99]:
                idx = int(count * quantile)
                value = sorted_values[min(idx, count-1)]

                if label_base:
                    lines.append(f'{name}_bucket{{quantile="{quantile}",{label_base}}} {value}')
                else:
                    lines.append(f'{name}_bucket{{quantile="{quantile}"}} {value}')

            # 总数和和
            if label_base:
                lines.append(f"{name}_count{{{label_base}}} {count}")
                lines.append(f"{name}_sum{{{label_base}}} {total}")
            else:
                lines.append(f"{name}_count {count}")
                lines.append(f"{name}_sum {total}")

    return "\n".join(lines) + "\n"

def _parse_key(self, key: str) -> tuple[str, dict]:
    """解析键，提取名称和标签"""
    if '[' not in key:
        return key, {}

    name, label_str = key.split('[', 1)
    label_str = label_str.rstrip(']')

    labels = {}
    for pair in label_str.split(','):
        k, v = pair.split('=', 1)
        labels[k] = v

    return name, labels
```

**工作量**: 1.5小时

---

### Task 4: 结构化日志实现（2小时）

#### 4.1 创建结构化日志Formatter
**文件**: `backend/app/core/logging_config.py` (新建)

**功能**:
```python
import json
import logging
from datetime import datetime
from typing import Optional

class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器"""

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录"""

        # 基础字段
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # 可选字段（从extra提取）
        optional_fields = [
            "trace_id", "session_id", "user_id",
            "mode", "intent", "confidence",
            "model", "tokens", "cost",
            "duration_ms", "error_type"
        ]

        for field in optional_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)

        # 异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            log_data["exc_type"] = record.exc_info[0].__name__

        return json.dumps(log_data, ensure_ascii=False)


class TraceContextFilter(logging.Filter):
    """追踪上下文过滤器 - 从contextvars注入trace_id"""

    def filter(self, record: logging.LogRecord) -> bool:
        """注入trace_id到日志记录"""
        if not hasattr(record, 'trace_id'):
            record.trace_id = trace_context.get(None)
        return True


def configure_structured_logging():
    """配置结构化日志"""

    # 创建handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(StructuredFormatter())
    console_handler.addFilter(TraceContextFilter())

    # 配置根logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.INFO)

    # 应用logger也使用结构化格式
    app_logger = logging.getLogger("app")
    app_logger.addHandler(console_handler)
    app_logger.setLevel(logging.INFO)
```

**工作量**: 1小时

#### 4.2 使用contextvars传递trace_id
**文件**: `backend/app/api/middleware/trace_middleware.py` (新建)

**功能**:
```python
from contextvars import ContextVar
import uuid

# 全局trace_id context
trace_context: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)

class TraceMiddleware:
    """追踪中间件 - 为每个请求生成trace_id"""

    async def __call__(self, request: Request, call_next):
        # 生成或提取trace_id
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())

        # 设置到context
        trace_context.set(trace_id)

        # 添加到request state
        request.state.trace_id = trace_id

        try:
            response = await call_next(request)

            # 添加到响应头
            response.headers["X-Trace-ID"] = trace_id

            return response
        finally:
            # 清理context
            trace_context.set(None)
```

**工作量**: 0.5小时

#### 4.3 在关键位置使用结构化日志
**文件**: 多个文件（修改）

**示例**:
```python
# 在 chat_stream 中
logger.info(
    "意图识别完成",
    extra={
        "trace_id": trace_id,
        "session_id": session_id,
        "intent": intent_data["intent"],
        "confidence": intent_data["confidence"],
        "duration_ms": duration * 1000
    }
)

# 在 LLM调用中
logger.info(
    "LLM调用完成",
    extra={
        "trace_id": trace_id,
        "model": model,
        "tokens": total_tokens,
        "cost": cost,
        "duration_ms": duration * 1000
    }
)
```

**工作量**: 0.5小时

---

## 🧪 测试验证

### 单元测试
```bash
# 测试Prometheus导出
pytest tests/test_prometheus_export.py -v

# 测试结构化日志
pytest tests/test_structured_logging.py -v
```

### 集成测试
```bash
# 1. 启动服务
cd backend && python -m app.main

# 2. 发送测试请求
curl -X POST http://localhost:8000/api/v1/agent/chat/stream \
  -H "Content-Type: application/json" \
  -H "X-Trace-ID: test-trace-123" \
  -d '{"message": "续写第一章", "session_id": "test_session"}'

# 3. 查看Prometheus指标
curl http://localhost:8000/api/v1/metrics

# 4. 查看健康检查
curl http://localhost:8000/api/v1/health

# 5. 查看业务指标
curl http://localhost:8000/api/v1/metrics/business
```

### 监控验证清单
- [ ] 请求计数正常（api_requests_total）
- [ ] 响应时间记录（api_request_duration）
- [ ] 意图分布统计（intent_distribution）
- [ ] LLM调用监控（llm_calls_total, llm_response_time）
- [ ] Token使用记录（llm_token_usage_*）
- [ ] 健康检查响应正常
- [ ] Prometheus格式正确
- [ ] 所有日志包含trace_id
- [ ] 日志格式为JSON

---

## 📊 预期收益

### 可观测性提升
- ✅ 实时性能监控（P50/P90/P99）
- ✅ 详细的错误追踪（按类型统计）
- ✅ Token使用分析（按模型统计）
- ✅ 业务指标可视化

### 运维能力提升
- ✅ 快速定位问题（trace_id关联）
- ✅ 容量规划（基于历史数据）
- ✅ 告警及时响应
- ✅ 性能瓶颈识别

### 成本优化
- ✅ Token使用趋势分析
- ✅ 模型选择优化依据
- ✅ 缓存效果评估

---

## ⏱️ 时间规划

```
Day 1上午 (4小时):
  - Task 1: API层监控集成（3小时）
  - 测试验证（1小时）

Day 1下午 (4小时):
  - Task 2: Agent关键节点监控（2小时）
  - Task 3: Prometheus导出（1.5小时）
  - 测试验证（0.5小时）

Day 2上午 (2-3小时):
  - Task 4: 结构化日志（2小时）
  - 集成测试（0.5小时）
  - 文档更新（0.5小时）

────────────────────────────────
总计: 10-11小时 (约1.5天)
```

---

## ⚠️ 风险控制

### 潜在风险
1. **性能影响**: 监控代码可能增加延迟
   - 缓解: 使用异步记录，最小化阻塞
   - 监控: 对比优化前后响应时间

2. **内存占用**: 指标历史记录占用内存
   - 缓解: 设置合理的max_history
   - 监控: 定期清理过期数据

3. **日志量增加**: 结构化日志可能产生大量数据
   - 缓解: 设置合适的日志级别
   - 监控: 使用日志轮转

### 回滚方案
- 所有监控代码都是非侵入式的
- 可以通过环境变量关闭监控
- 不影响核心业务逻辑

---

## 📝 验收标准

### 功能验收
- [ ] `/metrics` 端点返回Prometheus格式
- [ ] `/health` 端点返回健康状态
- [ ] 所有API请求都有监控记录
- [ ] Agent关键��点都有计时统计
- [ ] 所有日志为JSON格式且包含trace_id

### 性能验收
- [ ] 监控开销 < 5% （响应时间增加<50ms）
- [ ] 内存占用增加 < 100MB
- [ ] 日志写入不阻塞主流程

### 质量验收
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试全部通过
- [ ] 文档完整清晰

---

## 🚀 下一步

完成 Phase 2.1 后的可选优化：
1. **Grafana Dashboard**: 创建可视化监控面板
2. **告警配置**: 配置Prometheus AlertManager
3. **分布式追踪**: 集成OpenTelemetry
4. **日志聚合**: 集成ELK或Loki

---

**文档版本**: v1.0
**创建时间**: 2025-01-07
**负责人**: Claude Code
**状态**: ⏸️ 待确认后开始实施
