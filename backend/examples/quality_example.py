"""
质量评估系统 - 使用示例

演示如何使用质量评估服务和质量循环管理器
"""

import asyncio
from app.services.ai.http_ai_service import HTTPAIService
from app.services.agent.quality.quality_evaluator import QualityEvaluatorService
from app.services.agent.quality.quality_loop import QualityLoopManager, SimpleQualityLoop
from app.services.agent.quality.quality_types import (
    QualityDimension,
    EvaluationContext
)


# ============================================
# 示例1: 基础质量评估
# ============================================

async def example_basic_evaluation():
    """基础质量评估示例"""
    print("\n" + "="*60)
    print("示例1: 基础质量评估")
    print("="*60 + "\n")

    # 1. 初始化服务
    ai_service = HTTPAIService()  # 使用默认模型
    evaluator = QualityEvaluatorService(ai_service, enable_cache=True)

    # 2. 准备评估内容
    content = """
    李云站在悬崖边,看着下方的万丈深渊。

    他刚刚突破到筑基期,体内的灵力比之前强大了数倍。不过他知道,
    修仙界强者如云,自己还需要继续努力。

    突然,一股强大的神识扫过他的身体。李云心中一惊,立刻收敛气息。
    """

    # 3. 准备评估上下文
    context = EvaluationContext(
        user_id="user_001",
        novel_id="novel_001",
        chapter_id="chapter_001",
        previous_content="李云在密室中修炼了七天七夜,终于突破了瓶颈。",
        target_length=200,
        writing_style="玄幻修仙风格",
        genre="玄幻"
    )

    # 4. 执行评估
    evaluation = await evaluator.evaluate(content, context)

    # 5. 输出结果
    print(f"总体评分: {evaluation.overall_score:.1f}/10")
    print(f"是否通过: {'✓' if evaluation.passes else '✗'}")
    print(f"综合反馈: {evaluation.feedback}")
    print(f"\n各维度评分:")
    for score in evaluation.dimension_scores:
        print(f"  - {score.dimension.value}: {score.score:.1f}/10")
        print(f"    反馈: {score.feedback[:60]}...")

    if evaluation.suggestions:
        print(f"\n改进建议:")
        for i, suggestion in enumerate(evaluation.suggestions, 1):
            print(f"  {i}. {suggestion}")

    # 6. 清理
    await ai_service.close()


# ============================================
# 示例2: 部分维度评估
# ============================================

async def example_partial_evaluation():
    """只评估特定维度"""
    print("\n" + "="*60)
    print("示例2: 部分维度评估 (只评估内容质量和连贯性)")
    print("="*60 + "\n")

    ai_service = HTTPAIService()
    evaluator = QualityEvaluatorService(ai_service)

    content = "这是一段测试内容..."

    context = EvaluationContext(
        user_id="user_001",
        novel_id="novel_001",
        chapter_id="chapter_001",
        target_length=100
    )

    # 只评估指定的维度
    dimensions = [
        QualityDimension.CONTENT_QUALITY,
        QualityDimension.COHERENCE
    ]

    evaluation = await evaluator.evaluate(
        content,
        context,
        dimensions=dimensions  # 指定维度
    )

    print(f"评估了 {len(evaluation.dimension_scores)} 个维度")
    print(f"总体评分: {evaluation.overall_score:.1f}/10")

    await ai_service.close()


# ============================================
# 示例3: 使用不同模型
# ============================================

async def example_different_models():
    """使用不同的评估模型"""
    print("\n" + "="*60)
    print("示例3: 使用快速模型进行评估")
    print("="*60 + "\n")

    # 使用gemini-2.5-flash-lite快速模型
    ai_service = HTTPAIService(model="gemini-2.5-flash-lite")
    evaluator = QualityEvaluatorService(ai_service)

    content = "这是一段测试内容..."

    context = EvaluationContext(
        user_id="user_001",
        novel_id="novel_001",
        chapter_id="chapter_001",
        target_length=100
    )

    evaluation = await evaluator.evaluate(content, context)

    print(f"使用模型: gemini-2.5-flash-lite")
    print(f"总体评分: {evaluation.overall_score:.1f}/10")

    await ai_service.close()


# ============================================
# 示例4: 缓存机制
# ============================================

async def example_cache():
    """演示缓存机制的效果"""
    print("\n" + "="*60)
    print("示例4: 缓存机制")
    print("="*60 + "\n")

    ai_service = HTTPAIService()
    evaluator = QualityEvaluatorService(ai_service, enable_cache=True)

    content = "这是一段测试内容..."
    context = EvaluationContext(
        user_id="user_001",
        novel_id="novel_001",
        chapter_id="chapter_001",
        target_length=100
    )

    import time

    # 第一次评估 (无缓存)
    print("第一次评估 (无缓存)...")
    start = time.time()
    evaluation1 = await evaluator.evaluate(content, context)
    time1 = time.time() - start
    print(f"耗时: {time1:.2f}s")

    # 第二次评估 (命中缓存)
    print("\n第二次评估 (命中缓存)...")
    start = time.time()
    evaluation2 = await evaluator.evaluate(content, context)
    time2 = time.time() - start
    print(f"耗时: {time2:.2f}s")

    # 对比
    speedup = time1 / time2 if time2 > 0 else 0
    print(f"\n性能提升: {speedup:.1f}x")

    # 缓存统计
    stats = evaluator.get_cache_stats()
    print(f"缓存统计: {stats}")

    # 清空缓存
    evaluator.clear_cache()
    print("缓存已清空")

    await ai_service.close()


# ============================================
# 示例5: 简单的质量循环
# ============================================

async def example_simple_quality_loop():
    """简单的质量循环示例"""
    print("\n" + "="*60)
    print("示例5: 简单质量循环")
    print("="*60 + "\n")

    ai_service = HTTPAIService()

    # 定义一个简单的生成函数
    attempt = [0]  # 使用列表来模拟可变的闭包变量

    async def simple_generator(prompt: str, style: str) -> str:
        """模拟的内容生成函数"""
        attempt[0] += 1
        print(f"  第{attempt[0]}次生成...")

        # 实际应用中,这里应该调用真实的AI生成接口
        # 这里为了演示,返回固定内容
        if attempt[0] == 1:
            return "这是第一次生成的内容,质量一般。" * 10
        elif attempt[0] == 2:
            return "这是第二次生成的内容,根据反馈进行了改进,增加了更多细节描写。" * 15
        else:
            return "这是第三次生成的内容,质量已经很高了,包含丰富的情节和细腻的描写。" * 20

    # 使用简单质量循环
    loop = SimpleQualityLoop(ai_service, max_iterations=3, target_score=8.0)

    context = EvaluationContext(
        user_id="user_001",
        novel_id="novel_001",
        chapter_id="chapter_001",
        target_length=300
    )

    # 运行质量循环
    result = await loop.run(
        generator=simple_generator,
        generator_kwargs={"prompt": "续写小说", "style": "玄幻风格"},
        context=context
    )

    # 输出结果
    print(f"\n质量循环完成!")
    print(f"迭代次数: {result['iterations']}")
    print(f"最终评分: {result['evaluation'].overall_score:.1f}/10")
    print(f"最终内容长度: {len(result['content'])}字")

    await ai_service.close()


# ============================================
# 示例6: 高级质量循环(带参数优化)
# ============================================

async def example_advanced_quality_loop():
    """高级质量循环,支持参数动态优化"""
    print("\n" + "="*60)
    print("示例6: 高级质量循环 (带参数优化)")
    print("="*60 + "\n")

    ai_service = HTTPAIService()
    evaluator = QualityEvaluatorService(ai_service)
    loop_manager = QualityLoopManager(evaluator)

    # 定义生成函数(会根据参数变化)
    async def adaptive_generator(prompt: str, temperature: float = 0.7) -> str:
        """支持参数调整的生成函数"""
        print(f"  生成中... (temperature={temperature:.2f})")
        # 实际应用中调用AI生成
        return f"生成的内容 (temperature={temperature})..." * 20

    context = EvaluationContext(
        user_id="user_001",
        novel_id="novel_001",
        chapter_id="chapter_001",
        target_length=300
    )

    # 运行质量循环,支持参数自动优化
    result = await loop_manager.run_quality_loop(
        generator=adaptive_generator,
        generator_kwargs={"prompt": "续写", "temperature": 0.8},
        context=context,
        max_iterations=3
    )

    print(f"\n质量循环完成!")
    print(f"迭代次数: {result['iterations']}")
    print(f"最佳评分: {result['evaluation'].overall_score:.1f}/10")
    print(f"\n迭代历史:")
    for i, history in enumerate(result['iteration_history'], 1):
        print(f"  第{i}次: 评分{history['score']:.1f}")

    await ai_service.close()


# ============================================
# 运行所有示例
# ============================================

async def main():
    """运行所有示例"""
    print("\n🚀 质量评估系统 - 使用示例")

    # 基础示例
    await example_basic_evaluation()

    # 部分维度评估
    # await example_partial_evaluation()

    # 不同模型
    # await example_different_models()

    # 缓存机制
    # await example_cache()

    # 简单质量循环
    # await example_simple_quality_loop()

    # 高级质量循环
    # await example_advanced_quality_loop()

    print("\n✅ 所有示例运行完成!")


if __name__ == "__main__":
    # 注意: 实际使用时需要配置环境变量和数据库连接
    # 这里的示例可能需要适当调整才能运行

    print("注意: 运行示例需要:")
    print("  1. 配置.env文件(API密钥等)")
    print("  2. 确保backend环境已激活")
    print("  3. 取消main()中要运行的示例的注释")
    print("\n运行命令:")
    print("  cd backend && python -m examples.quality_example")

    # asyncio.run(main())
