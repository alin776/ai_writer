"""
模型选择器使用示例 - Week 7

展示如何使用 ModelSelector 和 CostTracker
"""

import asyncio
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.agent.model_selector import (
    ModelSelector,
    TaskType,
    TaskComplexity,
    select_model_for_task
)
from app.services.agent.cost_tracker import (
    CostTracker,
    get_cost_tracker
)


# ==================== 示例 1: 基础使用 ====================

def example_1_basic_usage():
    """示例1: 基础使用 - 通过任务类型选择模型"""
    print("=" * 60)
    print("示例1: 基础使用 - 通过任务类型选择模型")
    print("=" * 60)

    # 创建模型选择器
    selector = ModelSelector()

    # 场景1: 质量评估 (SIMPLE) → Gemini 2.5 Flash Lite
    print("\n场景1: 质量评估任务")
    result = selector.select_model(
        task_type=TaskType.QUALITY_EVALUATION,
        input_tokens=500,
        output_tokens=200
    )

    print(f"  选中模型: {result.model.name}")
    print(f"  模型ID: {result.model.model_id}")
    print(f"  任务复杂度: {result.complexity.value}")
    print(f"  预估成本: ${result.estimated_cost:.6f}")
    print(f"  选择原因: {result.reason}")

    # 场景2: 文本润色 (MEDIUM) → Gemini 2.5 Flash
    print("\n场景2: 文本润色任务")
    result = selector.select_model(
        task_type=TaskType.TEXT_POLISH,
        input_tokens=2000,
        output_tokens=2500
    )

    print(f"  选中模型: {result.model.name}")
    print(f"  预估成本: ${result.estimated_cost:.6f}")

    # 场景3: 小说创作 (COMPLEX) → Gemini 2.5 Pro
    print("\n场景3: 小说创作任务")
    result = selector.select_model(
        task_type=TaskType.CONTENT_CREATION,
        input_tokens=3000,
        output_tokens=2000
    )

    print(f"  选中模型: {result.model.name}")
    print(f"  预估成本: ${result.estimated_cost:.6f}")
    print(f"  备选模型: {[m.name for m in result.alternative_models]}")


# ==================== 示例 2: 使用便捷函数 ====================

def example_2_convenience_function():
    """示例2: 使用便捷函数"""
    print("\n" + "=" * 60)
    print("示例2: 使用便捷函数 - select_model_for_task()")
    print("=" * 60)

    # 直接使用便捷函数
    result = select_model_for_task(
        task_type=TaskType.SUMMARIZATION,
        input_tokens=1500,
        output_tokens=500
    )

    print(f"\n摘要生成任务:")
    print(f"  选中模型: {result.model.name}")
    print(f"  成本: ${result.estimated_cost:.6f}")


# ==================== 示例 3: 成本约束 ====================

def example_3_cost_constraint():
    """示例3: 成本约束 - 自动降级"""
    print("\n" + "=" * 60)
    print("示例3: 成本约束 - 自动降级到更便宜的模型")
    print("=" * 60)

    selector = ModelSelector()

    # 场景: 复杂任务，但预算有限
    print("\n创作任务，预算限制 $0.001:")

    result = selector.select_model(
        task_type=TaskType.CONTENT_CREATION,
        input_tokens=3000,
        output_tokens=2000,
        max_cost=0.001  # 预算不足以使用 Gemini 2.5 Pro
    )

    print(f"  原本应选: Gemini 2.5 Pro (${0.01375:.6f})")
    print(f"  实际选择: {result.model.name}")
    print(f"  预估成本: ${result.estimated_cost:.6f}")
    print(f"  原因: 预算约束导致降级")


# ==================== 示例 4: 手动指定复杂度 ====================

def example_4_manual_complexity():
    """示例4: 手动指定任务复杂度"""
    print("\n" + "=" * 60)
    print("示例4: 手动指定任务复杂度")
    print("=" * 60)

    selector = ModelSelector()

    # 直接指定复杂度
    for complexity in [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM, TaskComplexity.COMPLEX]:
        result = selector.select_model(
            complexity=complexity,
            input_tokens=1000,
            output_tokens=1000
        )

        print(f"\n复杂度={complexity.value}:")
        print(f"  模型: {result.model.name}")
        print(f"  成本: ${result.estimated_cost:.6f}")


# ==================== 示例 5: 根据上下文长度推断复杂度 ====================

def example_5_infer_complexity():
    """示例5: 根据上下文长度和质量要求推断复杂度"""
    print("\n" + "=" * 60)
    print("示例5: 根据上下文长度和质量要求推断复杂度")
    print("=" * 60)

    selector = ModelSelector()

    # 场景1: 短文本 + 低质量要求 → SIMPLE
    print("\n场景1: 短文本 (200字) + 低质量要求")
    result = selector.select_model(
        context_length=200,
        quality_requirement="low",
        input_tokens=500,
        output_tokens=200
    )
    print(f"  推断复杂度: {result.complexity.value}")
    print(f"  选中模型: {result.model.name}")

    # 场景2: 中等长度 + 中等质量 → MEDIUM
    print("\n场景2: 中等长度 (1000字) + 中等质量")
    result = selector.select_model(
        context_length=1000,
        quality_requirement="medium",
        input_tokens=2000,
        output_tokens=1500
    )
    print(f"  推断复杂度: {result.complexity.value}")
    print(f"  选中模型: {result.model.name}")

    # 场景3: 长文本 + 高质量要求 → COMPLEX
    print("\n场景3: 长文本 (5000字) + 高质量要求")
    result = selector.select_model(
        context_length=5000,
        quality_requirement="high",
        input_tokens=8000,
        output_tokens=3000
    )
    print(f"  推断复杂度: {result.complexity.value}")
    print(f"  选中模型: {result.model.name}")


# ==================== 示例 6: 成本估算 ====================

def example_6_cost_estimation():
    """示例6: 成本估算"""
    print("\n" + "=" * 60)
    print("示例6: 成本估算 - 对比不同模型的成本")
    print("=" * 60)

    selector = ModelSelector()

    # 假设场景: 1000次API调用，每次 1000 input + 1000 output tokens
    calls = 1000
    input_tokens = 1000
    output_tokens = 1000

    print(f"\n假设场景: {calls}次调用, 每次{input_tokens}+{output_tokens} tokens")
    print("-" * 60)

    for complexity in [TaskComplexity.SIMPLE, TaskComplexity.MEDIUM, TaskComplexity.COMPLEX]:
        result = selector.select_model(
            complexity=complexity,
            input_tokens=input_tokens,
            output_tokens=output_tokens
        )

        total_cost = result.estimated_cost * calls

        print(f"\n{complexity.value.upper()}任务 ({result.model.name}):")
        print(f"  单次成本: ${result.estimated_cost:.6f}")
        print(f"  总成本 ({calls}次): ${total_cost:.2f}")


# ==================== 示例 7: 成本追踪 ====================

async def example_7_cost_tracking():
    """示例7: 成本追踪"""
    print("\n" + "=" * 60)
    print("示例7: 成本追踪 - 记录和统计API调用")
    print("=" * 60)

    # 获取全局成本追踪器
    tracker = get_cost_tracker()

    # 模拟几次API调用
    print("\n模拟API调用记录...")

    # 调用1: 质量评估 (SIMPLE)
    await tracker.track_api_call(
        user_id="user_001",
        model_provider="gemini",
        model_id="gemini-2.5-flash-lite",
        model_name="Gemini 2.5 Flash Lite",
        input_tokens=500,
        output_tokens=200,
        input_cost=0.000015,
        output_cost=0.000024,
        task_type="quality_evaluation",
        task_complexity="simple",
        response_time=2.5,
        success=True
    )

    # 调用2: 文本润色 (MEDIUM)
    await tracker.track_api_call(
        user_id="user_001",
        model_provider="gemini",
        model_id="gemini-2.5-flash",
        model_name="Gemini 2.5 Flash",
        input_tokens=2000,
        output_tokens=2500,
        input_cost=0.00015,
        output_cost=0.00075,
        task_type="text_polish",
        task_complexity="medium",
        response_time=4.2,
        success=True
    )

    # 调用3: 小说创作 (COMPLEX)
    await tracker.track_api_call(
        user_id="user_001",
        model_provider="gemini",
        model_id="gemini-2.5-pro",
        model_name="Gemini 2.5 Pro",
        input_tokens=3000,
        output_tokens=2000,
        input_cost=0.00375,
        output_cost=0.01000,
        task_type="content_creation",
        task_complexity="complex",
        response_time=6.8,
        success=True
    )

    # 获取统计
    stats = await tracker.get_cost_statistics(
        user_id="user_001",
        period="all"
    )

    print(f"\n成本统计:")
    print(f"  总调用次数: {stats.total_calls}")
    print(f"  总token数: {stats.total_tokens:,}")
    print(f"  总成本: ${stats.total_cost:.6f}")
    print(f"  平均每次成本: ${stats.avg_cost_per_call:.6f}")
    print(f"  成功率: {stats.success_rate * 100:.1f}%")

    print(f"\n按模型分组:")
    for model_id, cost in stats.cost_by_model.items():
        calls = stats.calls_by_model[model_id]
        print(f"  {model_id}: {calls}次调用, ${cost:.6f}")

    print(f"\n按任务类型分组:")
    for task_type, cost in stats.cost_by_task_type.items():
        print(f"  {task_type}: ${cost:.6f}")


# ==================== 示例 8: 成本限额检查 ====================

async def example_8_cost_limit():
    """示例8: 成本限额检查"""
    print("\n" + "=" * 60)
    print("示例8: 成本限额检查")
    print("=" * 60)

    tracker = get_cost_tracker()

    # 模拟一些调用 (使用示例7的数据)
    await example_7_cost_tracking()

    # 检查成本限额
    result = await tracker.check_cost_limit(
        user_id="user_001",
        period="daily",
        limit=1.0  # 每日限额 $1.00
    )

    print(f"\n成本限额检查:")
    print(f"  限额: ${result['limit']:.2f}")
    print(f"  当前成本: ${result['current_cost']:.6f}")
    print(f"  剩余额度: ${result['remaining']:.6f}")
    print(f"  使用百分比: {result['usage_percentage']:.2f}%")
    print(f"  是否在限额内: {'[YES]' if result['within_limit'] else '[NO]'}")


# ==================== 示例 9: 成本报告 ====================

async def example_9_cost_report():
    """示例9: 生成成本报告"""
    print("\n" + "=" * 60)
    print("示例9: 生成成本报告")
    print("=" * 60)

    tracker = get_cost_tracker()

    # 生成成本报告
    report = await tracker.get_cost_report(
        user_id="user_001",
        period="all"
    )

    print(f"\n成本报告:")
    print(f"  时间范围: {report['date_range']['start']} 至 {report['date_range']['end']}")

    print(f"\n总体统计:")
    for key, value in report['summary'].items():
        print(f"  {key}: {value}")

    print(f"\n按模型分组:")
    for model, data in report['breakdown']['by_model'].items():
        print(f"  {model}:")
        print(f"    成本: ${data['cost']:.4f} ({data['percentage']:.1f}%)")
        print(f"    调用: {data['calls']}次")

    print(f"\n按任务类型分组:")
    for task, data in report['breakdown']['by_task_type'].items():
        print(f"  {task}: ${data['cost']:.4f} ({data['percentage']:.1f}%)")


# ==================== 示例 10: 获取推荐参数 ====================

def example_10_recommended_params():
    """示例10: 获取推荐的生成参数"""
    print("\n" + "=" * 60)
    print("示例10: 获取推荐的生成参数")
    print("=" * 60)

    selector = ModelSelector()

    # 不同任务类型的推荐参数
    task_types = [
        TaskType.QUALITY_EVALUATION,
        TaskType.TEXT_POLISH,
        TaskType.CONTENT_CREATION
    ]

    for task_type in task_types:
        result = selector.select_model(task_type=task_type)
        params = selector.get_recommended_params(result.model, task_type)

        print(f"\n{task_type.value}:")
        print(f"  模型: {result.model.name}")
        print(f"  推荐参数: {params}")


# ==================== 主函数 ====================

async def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("模型选择器使用示例")
    print("=" * 60)

    # 运行同步示例
    example_1_basic_usage()
    example_2_convenience_function()
    example_3_cost_constraint()
    example_4_manual_complexity()
    example_5_infer_complexity()
    example_6_cost_estimation()
    example_10_recommended_params()

    # 运行异步示例
    await example_7_cost_tracking()
    await example_8_cost_limit()
    await example_9_cost_report()

    print("\n" + "=" * 60)
    print("[OK] 所有示例运行完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
