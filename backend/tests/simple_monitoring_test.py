"""
简化监控系统测试脚本

测试核心监控功能，避免编码和依赖问题。
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
import time
from datetime import datetime

# 模拟psutil
class MockPsutil:
    class MockProcess:
        def __init__(self):
            self.pid = 12345

        def cpu_percent(self):
            return 25.5

        def memory_info(self):
            class MemoryInfo:
                def __init__(self):
                    self.rss = 200 * 1024 * 1024  # 200MB
            return MemoryInfo()

        @property
        def status(self):
            return "running"

    @staticmethod
    def cpu_percent(interval=1):
        return 25.5

    @staticmethod
    def virtual_memory():
        class Memory:
            def __init__(self):
                self.total = 8 * 1024 * 1024 * 1024
                self.available = 3 * 1024 * 1024 * 1024
                self.percent = 62.5

        return Memory()

    @staticmethod
    def disk_usage(path='/'):
        class Disk:
            def __init__(self):
                self.total = 100 * 1024 * 1024 * 1024
                self.used = 45 * 1024 * 1024 * 1024
                self.free = 55 * 1024 * 1024 * 1024

        return Disk()

    @staticmethod
    def Process():
        return MockPsutil.MockProcess()

# 添加模拟psutil到sys.modules
sys.modules['psutil'] = MockPsutil()

def test_basic_imports():
    """测试基础导入"""
    print("测试基础模块导入...")

    try:
        from app.services.agent.utils.monitoring import (
            get_system_monitor, AlertLevel, HealthStatus
        )
        print("  monitoring 模块导入成功")

        from app.services.agent.utils.business_metrics import (
            get_business_metrics_collector, ContentType, UserAction
        )
        print("  business_metrics 模块导入成功")

        return True
    except Exception as e:
        print(f"  导入失败: {e}")
        return False

def test_system_monitor():
    """测试系统监控器"""
    print("测试系统监控器...")

    try:
        from app.services.agent.utils.monitoring import get_system_monitor

        monitor = get_system_monitor()

        # 测试指标收集
        monitor.metrics_collector.increment_counter("test_counter", 1)
        monitor.metrics_collector.set_gauge("test_gauge", 42.5)
        monitor.metrics_collector.record_timer("test_timer", 1.23)

        # 验证指标
        counter = monitor.metrics_collector.get_metric("test_counter")
        gauge = monitor.metrics_collector.get_metric("test_gauge")
        timer = monitor.metrics_collector.get_metric("test_timer")

        success = (counter is not None and gauge is not None and timer is not None)

        if success:
            print(f"  计数器值: {counter.value}")
            print(f"  仪表盘值: {gauge.value}")
            print(f"  计时器值: {timer.value}")

        return success

    except Exception as e:
        print(f"  系统监控器测试失败: {e}")
        return False

def test_business_metrics():
    """测试业务指标"""
    print("测试业务指标...")

    try:
        from app.services.agent.utils.business_metrics import (
            get_business_metrics_collector, track_content_generation,
            track_user_action, track_llm_call, ContentType, UserAction
        )

        collector = get_business_metrics_collector()

        # 测试内容生成跟踪
        track_content_generation(
            content_id="test_content_001",
            content_type=ContentType.NOVEL_CHAPTER,
            user_id="test_user",
            project_id="test_project",
            tokens_generated=1000,
            generation_time=2.5,
            quality_score=0.85
        )
        print("  内容生成跟踪成功")

        # 测试用户操作跟踪
        track_user_action(
            user_id="test_user",
            action=UserAction.CREATE_PROJECT,
            session_id="test_session"
        )
        print("  用户操作跟踪成功")

        # 测试LLM调用跟踪
        track_llm_call(
            model="gpt-3.5-turbo",
            tokens_used={"prompt_tokens": 100, "completion_tokens": 200, "total_tokens": 300},
            cost=0.01,
            response_time=1.5,
            success=True
        )
        print("  LLM调用跟踪成功")

        # 获取业务摘要
        summary = collector.get_business_summary(1)
        print(f"  生成内容数: {summary['content_metrics']['total_generated']}")
        print(f"  总Token数: {summary['content_metrics']['total_tokens']}")
        print(f"  活跃用户数: {summary['user_metrics']['active_users_count']}")

        return True

    except Exception as e:
        print(f"  业务指标测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_checks():
    """测试健康检查"""
    print("测试健康检查...")

    try:
        import asyncio
        from app.services.agent.utils.monitoring import get_system_monitor

        async def run_health_checks():
            monitor = get_system_monitor()
            results = await monitor.health_checker.run_all_checks()

            print(f"  健康检查总数: {len(results)}")

            status_counts = {}
            for name, check in results.items():
                status = check.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
                print(f"  {name}: {status}")

            overall_status = monitor.health_checker.get_overall_status()
            print(f"  总体状态: {overall_status.value}")

            return len(results) > 0

        return asyncio.run(run_health_checks())

    except Exception as e:
        print(f"  健康检查测试失败: {e}")
        return False

def test_alerts():
    """测试告警系统"""
    print("测试告警系统...")

    try:
        from app.services.agent.utils.monitoring import get_system_monitor, AlertLevel

        monitor = get_system_monitor()

        # 创建测试告警
        info_alert = monitor.alert_manager.create_alert(
            level=AlertLevel.INFO,
            title="测试信息告警",
            message="这是一个测试信息告警"
        )

        warning_alert = monitor.alert_manager.create_alert(
            level=AlertLevel.WARNING,
            title="测试警告告警",
            message="这是一个测试警告告警"
        )

        # 检查活跃告警
        active_alerts = monitor.alert_manager.get_active_alerts()

        print(f"  创建告警数: 2")
        print(f"  活跃告警数: {len(active_alerts)}")

        # 按级别统计
        alert_stats = {}
        for alert in active_alerts:
            level = alert.level.value
            alert_stats[level] = alert_stats.get(level, 0) + 1

        print(f"  告警分布: {alert_stats}")

        return len(active_alerts) >= 2

    except Exception as e:
        print(f"  告警系统测试失败: {e}")
        return False

def test_reports():
    """测试报告生成"""
    print("测试报告生成...")

    try:
        import asyncio
        from app.services.agent.utils.monitoring_reports import get_report_generator

        async def generate_test_reports():
            generator = get_report_generator()

            # 生成健康检查报告
            health_report = await generator.generate_health_report()
            print(f"  健康检查报告: {health_report.title}")
            print(f"  章节数: {len(health_report.sections)}")

            # 生成日报
            daily_report = await generator.generate_daily_summary()
            print(f"  日报: {daily_report.title}")
            print(f"  章节数: {len(daily_report.sections)}")

            return True

        return asyncio.run(generate_test_reports())

    except Exception as e:
        print(f"  报告生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("AI Writer 监控系统简化测试")
    print("=" * 50)

    test_results = {}

    # 运行各项测试
    tests = [
        ("基础导入", test_basic_imports),
        ("系统监控器", test_system_monitor),
        ("业务指标", test_business_metrics),
        ("健康检查", test_health_checks),
        ("告警系统", test_alerts),
        ("报告生成", test_reports)
    ]

    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            result = test_func()
            test_results[test_name] = result
            status = "[通过]" if result else "[失败]"
            print(f"结果: {status}")
        except Exception as e:
            test_results[test_name] = False
            print(f"结果: [异常] - {e}")

    # 测试总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)

    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)

    print(f"总测试数: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")

    print("\n详细结果:")
    for test_name, result in test_results.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"  {status} {test_name}")

    # 保存测试结果
    results_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total,
        "passed_tests": passed,
        "pass_rate": passed/total*100,
        "detailed_results": test_results
    }

    with open("simple_monitoring_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results_data, f, ensure_ascii=False, indent=2)

    print(f"\n测试结果已保存到: simple_monitoring_test_results.json")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)