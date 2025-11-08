# 上下文工程优化 - 实施待办事项 📋

> **创建时间**: 2025-11-08
> **预计工期**: 1周（快速启动路径）
> **当前阶段**: 阶段一 - 基础优化（P0）
> **实施状态**: 待确认启动

---

## 📊 实施总览

### 目标和预期成果

| 指标 | 当前值 | 目标值 | 提升幅度 |
|------|--------|--------|---------|
| Token估算准确率 | 70% | 95%+ | +36% |
| 摘要质量评分 | 3/10 | 8/10 | +167% |
| 监控覆盖率 | 0% | 100% | 新增 |
| 测试覆盖率 | 30% | 90%+ | +200% |

### 实施路径

**阶段一**（P0必须完成，1-2周）
- Day 1-2: Token估算改进 ⭐⭐⭐⭐⭐
- Day 3-4: LLM摘要生成改进 ⭐⭐⭐⭐⭐
- Day 5: 监控系统集成 ⭐⭐⭐⭐
- Day 6-7: 端到端测试验证 ⭐⭐⭐⭐

---

## ✅ Day 1-2: Token估算改进

**目标**: 将Token估算准确率从70%提升到95%+

### 步骤1: 验证环境准备（30分钟）
- [ ] 1.1 验证tiktoken已安装（requirements.txt包含tiktoken==0.7.0）
- [ ] 1.2 测试tiktoken导入
  ```bash
  cd D:\Java\ai_writer\backend
  ./venv/Scripts/python.exe -c "import tiktoken; print(tiktoken.__version__)"
  ```
- [ ] 1.3 如安装有问题，重新安装tiktoken

### 步骤2: 创建TokenCounter类（2小时）
- [ ] 2.1 创建文件 `backend/app/services/context/token_counter.py`
- [ ] 2.2 实现TokenCounter类
  - [ ] 实现三层降级策略
    - 策略1: tiktoken精确计数（准确率100%）
    - 策略2: 中文优化估算（准确率95%）
    - 策略3: 简单估算（准确率75%）
  - [ ] 实现_init_encoding()初始化方法
  - [ ] 实现count_tokens()核心计数方法
  - [ ] 实现_estimate_tokens_with_chinese()降级策略
  - [ ] 实现count_messages_tokens()消息列表计数
  - [ ] 实现get_stats()统计接口
- [ ] 2.3 实现全局单例get_token_counter()
- [ ] 2.4 实现便捷函数count_tokens()

### 步骤3: 修改models.py（1小时）
- [ ] 3.1 添加导入：`from app.services.context.token_counter import count_tokens`
- [ ] 3.2 修改ShortMemory.get_token_count()（第37-40行）
  ```python
  # 替换: sum(len(msg.content) // 4 for msg in self.messages)
  # 改为: sum(count_tokens(msg.content) for msg in self.messages)
  ```
- [ ] 3.3 修改SummaryMemory.get_token_count()（第50-54行）
  ```python
  # 使用count_tokens()替换 len() // 4
  ```
- [ ] 3.4 修改Context.get_total_tokens()（第80-86行）
  ```python
  # 使用count_tokens()替换 len() // 4
  ```

### 步骤4: 修改llm_optimizer.py（1小时）
- [ ] 4.1 添加导入：`from app.services.context.token_counter import count_tokens`
- [ ] 4.2 修改LLMRequest.estimate_tokens()（第39-42行）
  ```python
  # 替换: len(self.prompt) // 4 + len(self.prompt) % 4
  # 改为: count_tokens(self.prompt, model=self.model)
  ```
- [ ] 4.3 修改LLMOptimizer.estimate_tokens()（第285-293行）
  ```python
  # 使用count_tokens()统一Token计数逻辑
  ```

### 步骤5: 更新模块导出（5分钟）
- [ ] 5.1 修改 `backend/app/services/context/__init__.py`
- [ ] 5.2 添加导入和导出
  ```python
  from .token_counter import TokenCounter, count_tokens
  __all__ = [..., "TokenCounter", "count_tokens"]
  ```

### 步骤6: 编写单元测试（2小时）
- [ ] 6.1 创建测试文件 `backend/tests/integration/test_token_counter.py`
- [ ] 6.2 实现测试用例
  - [ ] test_tiktoken_available - 测试tiktoken是否可用
  - [ ] test_english_text_counting - 测试英文文本计数
  - [ ] test_chinese_text_counting - 测试中文文本计数
  - [ ] test_mixed_text_counting - 测试中英混合文本
  - [ ] test_empty_text - 测试空文本处理
  - [ ] test_long_text_counting - 测试长文本计数
  - [ ] test_fallback_strategy - 测试降级策略
  - [ ] test_messages_counting - 测试消息列表计数
  - [ ] test_accuracy_comparison - 测试准确率对比

### 步骤7: 运行测试验证（30分钟）
- [ ] 7.1 运行单元测试
  ```bash
  cd D:\Java\ai_writer\backend
  ./venv/Scripts/python.exe -m pytest tests/integration/test_token_counter.py -v
  ```
- [ ] 7.2 验证models.py修改
- [ ] 7.3 验证llm_optimizer.py修改
- [ ] 7.4 性能基准测试（单次计数 < 10ms）

### 验收标准
- [ ] ✅ Token估算准确率 > 95%（英文+中文）
- [ ] ✅ 单次计数性能 < 10ms
- [ ] ✅ 降级策略误差 < 10%
- [ ] ✅ 所有单元测试通过（8/8）

---

## ✅ Day 3-4: LLM摘要生成改进

**目标**: 将摘要质量从3/10提升到8/10

### 步骤1: 创建SummaryService（3小时）
- [ ] 1.1 创建文件 `backend/app/services/context/summary_service.py`
- [ ] 1.2 实现SummaryService类
  - [ ] 实现__init__初始化（懒加载AI服务）
  - [ ] 实现summarize_conversation()主方法
  - [ ] 设计结构化Prompt（提取用户需求、已完成任务、重要决策）
  - [ ] 实现_build_summary_prompt()构建Prompt
  - [ ] 实现_validate_summary()质量验证
  - [ ] 实现_fallback_summary()降级策略
  - [ ] 配置使用gpt-4o-mini模型（成本优化）
  - [ ] 控制摘要长度100-200字

### 步骤2: 修改ContextManager（2小时）
- [ ] 2.1 修改 `backend/app/services/context/manager.py`
- [ ] 2.2 修改__init__方法
  ```python
  def __init__(
      self,
      store: Optional[ContextStore] = None,
      token_budget: Optional[TokenBudget] = None,
      ai_service: Optional[HTTPAIService] = None  # 新增参数
  ):
  ```
- [ ] 2.3 添加属性
  ```python
  self.ai_service = ai_service
  self._summary_service = None  # 懒加载
  ```
- [ ] 2.4 修改_generate_summary()方法（manager.py:200-227）
  - [ ] 检查ai_service是否存在
  - [ ] 懒加载SummaryService
  - [ ] 调用LLM生成摘要
  - [ ] 异常处理和降级策略
- [ ] 2.5 添加set_ai_service()方法（向后兼容）
  ```python
  def set_ai_service(self, ai_service: HTTPAIService):
      self.ai_service = ai_service
  ```

### 步骤3: 编写集成测试（2小时）
- [ ] 3.1 创建测试文件 `backend/tests/integration/test_summary_integration.py`
- [ ] 3.2 实现测试用例
  - [ ] test_llm_summary_generation - 测试LLM摘要生成
  - [ ] test_llm_summary_quality - 测试摘要质量
  - [ ] test_summary_fallback - 测试降级策略
  - [ ] test_backward_compatibility - 测试向后兼容性
  - [ ] test_multi_turn_summary - 测试多轮对话摘要
  - [ ] test_summary_length_control - 测试长度控制

### 步骤4: 更新调用代码（1小时）
- [ ] 4.1 检查哪些地方需要注入ai_service
- [ ] 4.2 更新ContextManager实例化代码
  ```python
  # 推荐方式：构造时注入
  manager = ContextManager(ai_service=ai_service)

  # 兼容方式：setter注入
  manager = ContextManager()
  manager.set_ai_service(ai_service)
  ```

### 验收标准
- [ ] ✅ 摘要质量评分 ≥ 8/10（人工评估5个样本）
- [ ] ✅ 摘要长度控制在100-200字
- [ ] ✅ LLM成功率 > 90%
- [ ] ✅ 降级率 < 10%
- [ ] ✅ 所有集成测试通过

---

## ✅ Day 5: 监控系统集成

**目标**: 建立完整的监控体系，实现100%可观测性

### 步骤1: 创建监控集成模块（2小时）
- [ ] 1.1 创建文件 `backend/app/services/context/monitoring_integration.py`
- [ ] 1.2 利用现有的monitoring.py（app/services/agent/utils/monitoring.py）
- [ ] 1.3 定义14+监控指标
  - [ ] context_token_count_total - Token计数调用次数
  - [ ] context_token_count_duration - Token计数耗时
  - [ ] context_summary_generation_total - 摘要生成调用次数
  - [ ] context_summary_generation_duration - 摘要生成耗时
  - [ ] context_summary_generation_success - 摘要生成成功次数
  - [ ] context_summary_generation_fallback - 摘要降级次数
  - [ ] context_compression_ratio - 压缩比率
  - [ ] context_build_total - 构建上下文次数
  - [ ] context_build_duration - 构建上下文耗时
  - [ ] context_update_total - 更新上下文次数
  - [ ] context_update_duration - 更新上下文耗时
  - [ ] context_short_memory_size - 短期记忆大小
  - [ ] context_summary_memory_size - 摘要记忆大小
  - [ ] context_total_tokens - 总Token数

### 步骤2: 实现监控装饰器（2小时）
- [ ] 2.1 实现@monitor_token_counting装饰器
- [ ] 2.2 实现@monitor_summary_generation装饰器
- [ ] 2.3 实现@monitor_context_build装饰器
- [ ] 2.4 实现record_compression_metrics()函数

### 步骤3: 集成到ContextManager（1小时）
- [ ] 3.1 在token计数方法添加监控
  ```python
  @monitor_token_counting
  def get_token_count(self) -> int:
  ```
- [ ] 3.2 在摘要生成方法添加监控
  ```python
  @monitor_summary_generation
  async def _generate_summary(self, messages):
  ```
- [ ] 3.3 在context构建方法添加监控
  ```python
  @monitor_context_build
  async def build_context(self, session_id):
  ```
- [ ] 3.4 在压缩操作添加监控
  ```python
  record_compression_metrics(original, compressed, session_id)
  ```

### 步骤4: 验证监控指标（1小时）
- [ ] 4.1 启动应用并触发几次对话
- [ ] 4.2 检查Prometheus指标是否正常采集
- [ ] 4.3 验证监控数据准确性
- [ ] 4.4 检查监控不影响性能（开销 < 5%）

### 验收标准
- [ ] ✅ 监控覆盖率100%（所有关键操作都有监控）
- [ ] ✅ 14+监控指标正常记录
- [ ] ✅ Prometheus可查询所有指标
- [ ] ✅ 监控开销 < 5%

---

## ✅ Day 6-7: 端到端测试验证

**目标**: 全面验证系统稳定性和性能

### 步骤1: 补充长对话测试（2小时）
- [ ] 1.1 创建30轮对话测试用例
  ```python
  async def test_long_conversation_30_rounds():
  ```
- [ ] 1.2 验证每轮Token使用率 < 90%
- [ ] 1.3 验证摘要生成正常
- [ ] 1.4 验证上下文压缩正常
- [ ] 1.5 验证最终Token控制在预算内

### 步骤2: 添加并发测试（2小时）
- [ ] 2.1 创建10个并发会话测试
  ```python
  async def test_concurrent_10_sessions():
  ```
- [ ] 2.2 验证会话隔离性（互不干扰）
- [ ] 2.3 验证Redis并发访问安全
- [ ] 2.4 验证无资源竞争和死锁

### 步骤3: 添加性能基准测试（2小时）
- [ ] 3.1 测试单个会话完整流程 < 2s
  ```python
  async def test_performance_benchmark():
  ```
- [ ] 3.2 测试Token计数性能 < 10ms
- [ ] 3.3 测试摘要生成性能 < 5s
- [ ] 3.4 测试Redis读写性能 < 100ms

### 步骤4: 完整集成测试（2小时）
- [ ] 4.1 测试完整对话流程（新会话 → 多轮对话 → 压缩 → 继续对话）
- [ ] 4.2 测试异常处理（LLM失败、Redis故障、网络超时）
- [ ] 4.3 测试降级策略（tiktoken失败、摘要失败）
- [ ] 4.4 测试监控指标采集
- [ ] 4.5 测试日志输出完整性

### 步骤5: 回归测试（1小时）
- [ ] 5.1 运行所有现有测试，确保无破坏
  ```bash
  ./venv/Scripts/python.exe -m pytest tests/ -v
  ```
- [ ] 5.2 运行上下文管理测试
  ```bash
  ./venv/Scripts/python.exe -m pytest tests/integration/test_context_manager.py -v
  ```
- [ ] 5.3 验证所有测试通过

### 验收标准
- [ ] ✅ 30轮对话测试通过，Token使用率 < 90%
- [ ] ✅ 10并发会话测试通过，无异常
- [ ] ✅ 性能基准全部达标（< 2s）
- [ ] ✅ 测试覆盖率 > 90%
- [ ] ✅ 所有回归测试通过

---

## 📝 实施注意事项

### 核心原则（必须遵守）
1. **简单至上**: 每个任务尽可能简单，影响最小代码量
2. **降级策略**: 所有新功能都要有降级方案，确保系统高可用
3. **向后兼容**: 不破坏现有功能，保持API兼容性
4. **测试驱动**: 每个功能都要有对应的测试用例
5. **监控优先**: 关键操作都要添加监控指标
6. **日志详细**: 重要操作都要有清晰的日志输出

### 质量标准
- 代码规范: 遵循PEP 8
- 类型注解: 所有函数都要有类型提示
- 文档字符串: 所有公开API都要有docstring
- 错误处理: 所有异常都要妥善处理
- 日志级别: DEBUG用于调试，INFO用于关键操作，ERROR用于错误

### 回滚方案
如果遇到问题，可以：
1. **紧急回滚**: 设置FORCE_DISABLE标志
2. **完全回滚**: git checkout恢复原始代码
3. **部分回滚**: 只回滚有问题的部分

---

## 📊 Review 总结区域

> **说明**: 等待实施完成后填写此部分

### 已完成的变更
<!-- Day 1-2完成后填写 -->
- [ ] TokenCounter类创建
- [ ] models.py修改
- [ ] llm_optimizer.py修改
- [ ] 单元测试编写

<!-- Day 3-4完成后填写 -->
- [ ] SummaryService创建
- [ ] ContextManager集成
- [ ] 集成测试编写

<!-- Day 5完成后填写 -->
- [ ] 监控集成模块创建
- [ ] 14+监控指标定义
- [ ] ContextManager监控集成

<!-- Day 6-7完成后填写 -->
- [ ] 长对话测试
- [ ] 并发测试
- [ ] 性能基准测试

### 遇到的问题和解决方案
<!-- 在实施过程中记录 -->

**Day 1-2问题**:


**Day 3-4问题**:


**Day 5问题**:


**Day 6-7问题**:


### 效果评估（实施完成后填写）

| 指标 | 实施前 | 实施后 | 提升幅度 | 达标情况 |
|------|--------|--------|----------|----------|
| Token估算准确率 | 70% | __%  | +__% | ☐ 是 ☐ 否 |
| 摘要质量评分 | 3/10 | __/10 | +__% | ☐ 是 ☐ 否 |
| 监控覆盖率 | 0% | __% | +__% | ☐ 是 ☐ 否 |
| 测试覆盖率 | 30% | __% | +__% | ☐ 是 ☐ 否 |

### 后续建议
<!-- 实施完成后填写 -->

**是否继续阶段二**（自适应Token分配）:
- [ ] 是，继续实施
- [ ] 否，暂缓实施

**是否继续阶段三**（向量检索长期记忆）:
- [ ] 是，继续实施
- [ ] 否，暂缓实施

**其他建议**:


---

## 🔗 参考文档

### 实施文档（核心）
- [00_README_总览和规划.md](../docs/Agent/上下文工程/实施文档/00_README_总览和规划.md)
- [01_Day1-2_Token估算改进.md](../docs/Agent/上下文工程/实施文档/01_Day1-2_Token估算改进.md)
- [02_Day3-4_摘要生成改进.md](../docs/Agent/上下文工程/实施文档/02_Day3-4_摘要生成改进.md)
- [03_Day5_监控集成.md](../docs/Agent/上下文工程/实施文档/03_Day5_监控集成.md)
- [04_Day6-7_端到端测试.md](../docs/Agent/上下文工程/实施文档/04_Day6-7_端到端测试.md)

### 状态跟踪
- [IMPLEMENTATION_STATUS.md](../docs/Agent/上下文工程/实施文档/IMPLEMENTATION_STATUS.md)
- [REVIEW_审查报告.md](../docs/Agent/上下文工程/实施文档/REVIEW_审查报告.md)

### 参考文档
- [08_API接口参考.md](../docs/Agent/上下文工程/实施文档/08_API接口参考.md)
- [09_配置和FAQ.md](../docs/Agent/上下文工程/实施文档/09_配置和FAQ.md)

---

**待办列表创建时间**: 2025-11-08
**预计开始时间**: 待用户确认
**预计完成时间**: 开始后1周
**当前状态**: ⏸️ 待确认启动
