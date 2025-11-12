# Token 使用量监控和成本计算深度审计报告

## 核心发现

发现项目中存在 **6个不同位置定义定价信息**，导致以下问题：
1. 定价数据不一致 (如Gemini 2.5 Flash价格差异)
2. 成本计算硬编码多处
3. CostCalculator和CostTracker未充分利用
4. 维护困难

---

## 发现的所有定价定义位置

### 位置1: CostCalculator (主权威源 ✓)
文件: D:\Java\ai_writer\backend\app\utils\cost_calculator.py
- 第15-42行定义 PRICING 字典
- 定义模型: GPT-4系列、Gemini系列、Claude系列
- 推荐: 作为唯一的定价来源

### 位置2: ModelSelector (重复定义 ✗)
文件: D:\Java\ai_writer\backend\app\services\agent\model_selector.py
- 第113-202行: MODEL_TIERS (主模型)
- 第155-202行: ALTERNATIVE_MODELS (备选)
- 问题: 与CostCalculator定价不一致
  * gemini-2.5-flash: CostCalc=(0.30,2.50) vs ModelSel=(0.075,0.30) ❌
  * gemini-2.5-pro: CostCalc=(1.25,10.0) vs ModelSel=(1.25,5.00) ❌

### 位置3: LLMOptimizer (重复定义 ✗)
文件: D:\Java\ai_writer\backend\app\services\agent\utils\llm_optimizer.py
- 第248-260行: _estimate_cost方法中的cost_per_million字典
- 第270-274行: LLMOptimizer.__init__中的_model_costs字典
- 问题: 完全不使用CostCalculator，自己实现成本估算

### 位置4: HTTPAIService (硬编码 ✗ 关键)
文件: D:\Java\ai_writer\backend\app\services\ai\http_ai_service.py
- 第463-464行和467-468行:
  input_cost = (input_tokens / 1_000_000) * 0.50
  output_cost = (output_tokens / 1_000_000) * 1.50
- 问题: 硬编码费率，不使用CostCalculator

### 位置5: HumanizeService (混乱的费率 ✗)
文件: D:\Java\ai_writer\backend\app\api\v1\humanize.py
- 第672-675行:
  detection_cost = total_tokens * 0.3 * 0.0000002
  rewrite_cost = total_tokens * 0.6 * 0.000002
  verification_cost = total_tokens * 0.1 * 0.0000002
- 第760行:
  cost=estimated_tokens * 0.000001
- 问题: 使用非常奇怪的费率(0.0000002, 0.000002, 0.000001)，与任何模型定价不符

### 位置6: AILogService (找到的引用)
文件: D:\Java\ai_writer\backend\app\services\ai_log_service.py (位置不确定)
- 第89行: log.total_cost = tokens_used * 0.00001
- 问题: 又是不同的硬编码费率

---

## 集成问题

### 问题1: CostTracker和CostCalculator的关系
- CostTracker.track_api_call() 接收已计算的成本参数
- 但从未验证这些成本是否使用了正确的CostCalculator定价
- track_api_call参数示例中的 input_cost=0.0005, output_cost=0.00075 从何而来？

### 问题2: HTTPAIService._track_api_cost 不正确
- 第449行: 尝试从MODEL_TIERS获取model_config
- 第457-460行: 使用model_config.cost_per_1m_input/output
- 第463-464、467-468行: 如果找不到model_config，使用硬编码 0.50/1.50
- 这是错误的! 应该使用CostCalculator

### 问题3: AILogMiddleware正确使用了CostCalculator ✓
- 第81-85行正确调用了CostCalculator.calculate_cost()
- 这是应该被所有模块学习的模式

---

## 修改建议总结

### P1优先级 (关键业务逻辑缺陷)

#### 修复1: HTTPAIService._track_api_cost
替换硬编码费率为CostCalculator:
```python
from app.utils.cost_calculator import CostCalculator

# 使用CostCalculator计算成本
cost_data = CostCalculator.calculate_cost(
    model_name=self.model,
    prompt_tokens=input_tokens,
    completion_tokens=output_tokens
)
input_cost = cost_data["prompt_cost"]
output_cost = cost_data["completion_cost"]
```

#### 修复2: HumanizeService成本计算
替换奇怪的硬编码费率:
```python
from app.utils.cost_calculator import CostCalculator

# 计算实际成本而不是使用硬编码费率
cost_data = CostCalculator.calculate_cost(
    model_name="gemini-2.5-flash",  # 或从config读取
    prompt_tokens=int(total_tokens * 0.3),
    completion_tokens=int(total_tokens * 0.6)
)
estimated_cost = cost_data["total_cost"]
```

### P2优先级 (维护性和一致性)

#### 修复3: ModelSelector定价
使用CostCalculator作为唯一的定价源，或移除重复定义

#### 修复4: LLMOptimizer成本计算
替换硬编码的_estimate_cost为CostCalculator

#### 修复5: AILogService费率
检查并修复第89行的硬编码费率

### P3优先级 (长期维护)

#### 改进6: 添加成本验证
在CostTracker中验证传入的成本是否与CostCalculator计算一致

#### 改进7: 创建统一配置
考虑创建配置文件，所有定价信息在一个地方

---

## 文件清单

需要修改的文件(按优先级):
1. D:\Java\ai_writer\backend\app\services\ai\http_ai_service.py
2. D:\Java\ai_writer\backend\app\api\v1\humanize.py
3. D:\Java\ai_writer\backend\app\services\agent\model_selector.py
4. D:\Java\ai_writer\backend\app\services\agent\utils\llm_optimizer.py
5. D:\Java\ai_writer\backend\app\services\ai_log_service.py (确认位置)
6. D:\Java\ai_writer\backend\app\services\agent\cost_tracker.py (需要验证)

参考模型文件(正确使用CostCalculator):
- D:\Java\ai_writer\backend\app\services\ai\ai_log_middleware.py ✓

---

## 检查清单

已验证的问题:
- [x] CostCalculator使用了正确的定价 ✓
- [x] ModelSelector与CostCalculator定价不一致 ✗
- [x] HTTPAIService使用硬编码费率 ✗
- [x] HumanizeService使用奇怪的费率 ✗
- [x] LLMOptimizer重复定义了定价 ✗
- [x] AILogMiddleware正确使用了CostCalculator ✓
- [x] CostTracker未验证传入的成本 ✗

