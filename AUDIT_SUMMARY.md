=============================================================
Token 使用量监控和成本计算深度审计 - 执行摘要
=============================================================

## 发现概述

共发现 8 个定价定义位置和 6 处硬编码费率的问题。

---

## 所有需要修改的文件清单

### 优先级P1（关键）- 立即修复

1. ✗ D:\Java\ai_writer\backend\app\services\ai\http_ai_service.py
   问题: 第463-468行 硬编码费率 0.50 / 1.50
   需求: 使用CostCalculator计算实际成本
   
2. ✗ D:\Java\ai_writer\backend\app\api\v1\humanize.py  
   问题: 第672-675行、760行 混乱的硬编码费率
         (0.0000002, 0.000002, 0.000001)
   需求: 使用CostCalculator计算实际成本

3. ✗ D:\Java\ai_writer\backend\app\services\agent\model_selector.py
   问题: 第113-152行 MODEL_TIERS定价与CostCalculator不一致
         - gemini-2.5-flash: (0.075,0.30) vs (0.30,2.50) ← 差异8倍！
         - gemini-2.5-pro: (1.25,5.00) vs (1.25,10.0) ← 输出差异
   需求: 与CostCalculator同步或删除重复定义

### 优先级P2（重要）- 应该修复

4. ✗ D:\Java\ai_writer\backend\app\services\agent\utils\llm_optimizer.py
   问题: 第248-260行、270-274行 硬编码定价，未使用CostCalculator
   需求: 使用CostCalculator而不是硬编码

5. ✗ D:\Java\ai_writer\backend\app\services\ai_log_service.py
   问题: 第89行 硬编码费率 0.00001
   需求: 使用CostCalculator计算

### 优先级P3（改进）- 长期维护

6. ⚠ D:\Java\ai_writer\backend\app\services\agent\cost_tracker.py
   问题: 未验证传入的成本是否与CostCalculator一致
   需求: 添加验证逻辑

---

## 正确使用CostCalculator的参考实现

✓ D:\Java\ai_writer\backend\app\services\ai\ai_log_middleware.py
  第81-85行 - 所有模块应学习这个模式:
  
  ```python
  cost_data = CostCalculator.calculate_cost(
      model_name=self.model_name,
      prompt_tokens=token_counter.prompt_tokens,
      completion_tokens=token_counter.completion_tokens
  )
  ```

---

## 数据不一致示例

| 模型 | CostCalculator | ModelSelector | 问题 |
|-----|---------|---------|------|
| gemini-2.5-flash | (0.30, 2.50) | (0.075, 0.30) | ❌ 差异8倍 |
| gemini-2.5-pro | (1.25, 10.0) | (1.25, 5.00) | ❌ 输出差异50% |
| gpt-3.5-turbo | (0.5, 1.5) | (0.50, 1.50) | ✓ 一致 |

---

## 修复工作估计

- HTTPAIService: 30分钟（改4行）
- HumanizeService: 45分钟（改4行，理解逻辑）
- ModelSelector: 60分钟（更新定价或重构）
- LLMOptimizer: 45分钟（替换成本函数）
- AILogService: 15分钟（修1行）
- CostTracker: 30分钟（添加验证）
- 测试: 60分钟

**总计**: 约4-5小时

---

## 关键收获

1. CostCalculator是正确的权威定价源
2. 其他模块正在进行不同形式的成本计算
3. 定价数据存在严重不一致（差异高达8倍）
4. 有些地方使用的费率来源不明
5. AILogMiddleware展示了正确的做法

---

## 建议行动

1. 立即修复P1问题（关键业务逻辑）
2. 将CostCalculator设置为唯一的定价来源
3. 删除所有重复的定价定义
4. 添加单元测试验证定价一致性
5. 创建文档说明如何正确使用CostCalculator

---

详细分析见: D:\Java\ai_writer\TOKEN_PRICING_AUDIT.md

