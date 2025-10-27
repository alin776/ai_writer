"""
小说分析性能压测脚本

测试并行分析的性能提升效果
"""
import asyncio
import time
import sys
from pathlib import Path
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.services.ai.novel_analysis_orchestrator import NovelAnalysisOrchestrator
from app.services.novel_analysis_service import NovelAnalysisService
from app.models.work import Work
from sqlalchemy import select
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PerformanceTest:
    """性能压测"""

    def __init__(self):
        self.results = []

    async def run_analysis_test(
        self,
        work_id: str,
        test_name: str
    ) -> dict:
        """
        运行单个分析测试

        Args:
            work_id: 作品ID
            test_name: 测试名称

        Returns:
            测试结果字典
        """
        logger.info("=" * 80)
        logger.info(f"🧪 开始测试: {test_name}")
        logger.info(f"🔖 Work ID: {work_id}")
        logger.info("=" * 80)

        async with AsyncSessionLocal() as db:
            # 清理之前的分析数据
            analysis_service = NovelAnalysisService(db)
            await analysis_service.delete_analysis(work_id)

            # 获取作品信息
            result = await db.execute(
                select(Work).where(Work.id == work_id)
            )
            work = result.scalar_one_or_none()

            if not work:
                raise ValueError(f"作品不存在: {work_id}")

            chapter_count = work.total_words // 5000 if work.total_words else 0

            # 创建新的分析任务
            analysis = await analysis_service.create_analysis(work_id)

            # 记录开始时间
            start_time = time.time()
            start_datetime = datetime.now()

            # 运行分析
            orchestrator = NovelAnalysisOrchestrator(db)
            success = await orchestrator.run_full_analysis(work_id)

            # 记录结束时间
            end_time = time.time()
            elapsed_time = end_time - start_time

            # 获取分析结果
            final_analysis = await analysis_service.get_analysis_by_work(work_id)

            result = {
                'test_name': test_name,
                'work_id': work_id,
                'work_title': work.title,
                'success': success,
                'start_time': start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'total_time': elapsed_time,
                'total_chapters': final_analysis.total_chapters if final_analysis else 0,
                'analyzed_chapters': final_analysis.analyzed_chapters if final_analysis else 0,
                'avg_time_per_chapter': elapsed_time / final_analysis.analyzed_chapters if final_analysis and final_analysis.analyzed_chapters > 0 else 0,
                'status': final_analysis.status if final_analysis else 'unknown'
            }

            self.results.append(result)

            logger.info("=" * 80)
            logger.info(f"✅ 测试完成: {test_name}")
            logger.info(f"📊 总耗时: {elapsed_time:.1f}秒 ({elapsed_time/60:.1f}分钟)")
            logger.info(f"📊 分析章节: {result['analyzed_chapters']}/{result['total_chapters']}")
            logger.info(f"📊 平均速度: {result['avg_time_per_chapter']:.1f}秒/章")
            logger.info(f"📊 状态: {result['status']}")
            logger.info("=" * 80)

            return result

    def print_summary(self):
        """打印测试总结"""
        print("\n" + "=" * 80)
        print("📊 性能测试总结")
        print("=" * 80)

        if not self.results:
            print("❌ 没有测试结果")
            return

        # 表头
        print(f"\n{'测试名称':<30} {'章节数':>8} {'耗时(分钟)':>12} {'平均(秒/章)':>14} {'状态':>10}")
        print("-" * 80)

        # 测试结果
        for r in self.results:
            print(
                f"{r['test_name']:<30} "
                f"{r['analyzed_chapters']:>8} "
                f"{r['total_time']/60:>12.1f} "
                f"{r['avg_time_per_chapter']:>14.1f} "
                f"{r['status']:>10}"
            )

        print("-" * 80)

        # 性能对比
        if len(self.results) >= 2:
            baseline = self.results[0]
            optimized = self.results[-1]

            speedup = baseline['total_time'] / optimized['total_time'] if optimized['total_time'] > 0 else 0

            print("\n🚀 性能提升:")
            print(f"  优化前: {baseline['total_time']/60:.1f} 分钟 ({baseline['avg_time_per_chapter']:.1f}秒/章)")
            print(f"  优化后: {optimized['total_time']/60:.1f} 分钟 ({optimized['avg_time_per_chapter']:.1f}秒/章)")
            print(f"  提速倍数: {speedup:.1f}x ⚡")

        print("\n" + "=" * 80)

    def save_report(self, filepath: str = "performance_report.md"):
        """保存测试报告"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("# 小说分析性能测试报告\n\n")
            f.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("## 测试结果\n\n")
            f.write("| 测试名称 | 章节数 | 耗时(分钟) | 平均(秒/章) | 状态 |\n")
            f.write("|---------|--------|-----------|-----------|------|\n")

            for r in self.results:
                f.write(
                    f"| {r['test_name']} | {r['analyzed_chapters']} | "
                    f"{r['total_time']/60:.1f} | {r['avg_time_per_chapter']:.1f} | "
                    f"{r['status']} |\n"
                )

            if len(self.results) >= 2:
                baseline = self.results[0]
                optimized = self.results[-1]
                speedup = baseline['total_time'] / optimized['total_time'] if optimized['total_time'] > 0 else 0

                f.write("\n## 性能提升\n\n")
                f.write(f"- **优化前**: {baseline['total_time']/60:.1f} 分钟\n")
                f.write(f"- **优化后**: {optimized['total_time']/60:.1f} 分钟\n")
                f.write(f"- **提速倍数**: {speedup:.1f}x ⚡\n")

        logger.info(f"✅ 测试报告已保存: {filepath}")


async def main():
    """主函数"""
    tester = PerformanceTest()

    print("\n" + "=" * 80)
    print("🧪 小说分析性能压测")
    print("=" * 80)
    print("\n请选择测试场景:")
    print("1. 测试20章小说 (快速测试)")
    print("2. 测试100章小说 (标准测试)")
    print("3. 测试500章小说 (压力测试)")
    print("4. 运行全部测试 (1+2+3)")
    print("0. 退出")
    print()

    choice = input("请输入选项 (0-4): ").strip()

    try:
        if choice == "1":
            work_id = input("请输入20章小说的Work ID: ").strip()
            await tester.run_analysis_test(work_id, "20章小说性能测试")
            tester.print_summary()

        elif choice == "2":
            work_id = input("请输入100章小说的Work ID: ").strip()
            await tester.run_analysis_test(work_id, "100章小说性能测试")
            tester.print_summary()

        elif choice == "3":
            work_id = input("请输入500章小说的Work ID: ").strip()
            await tester.run_analysis_test(work_id, "500章小说性能测试")
            tester.print_summary()

        elif choice == "4":
            work_id_20 = input("请输入20章小说的Work ID: ").strip()
            work_id_100 = input("请输入100章小说的Work ID: ").strip()
            work_id_500 = input("请输入500章小说的Work ID: ").strip()

            await tester.run_analysis_test(work_id_20, "20章小说性能测试")
            await tester.run_analysis_test(work_id_100, "100章小说性能测试")
            await tester.run_analysis_test(work_id_500, "500章小说性能测试")

            tester.print_summary()
            tester.save_report()

        elif choice == "0":
            print("\n👋 再见!")

        else:
            print("\n❌ 无效选项")

    except Exception as e:
        logger.error(f"测试失败: {e}", exc_info=True)
        print(f"\n❌ 测试失败: {e}")


if __name__ == "__main__":
    asyncio.run(main())
