"""
监控报告生成器

生成各类监控报告，包括性能报告、业务报告、健康报告等。
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path

from .monitoring import get_system_monitor, HealthStatus, AlertLevel
from .business_metrics import get_business_metrics_collector, ContentType
from .logger import get_logger
from app.utils.datetime_utils import get_utc_now

logger = get_logger("monitoring_reports")


class ReportType(Enum):
    """报告类型"""
    DAILY_SUMMARY = "daily_summary"
    WEEKLY_SUMMARY = "weekly_summary"
    MONTHLY_SUMMARY = "monthly_summary"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    HEALTH_CHECK = "health_check"
    BUSINESS_ANALYSIS = "business_analysis"
    ALERT_SUMMARY = "alert_summary"


@dataclass
class ReportSection:
    """报告章节"""
    title: str
    content: Dict[str, Any]
    charts: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class MonitoringReport:
    """监控报告"""
    report_id: str
    report_type: ReportType
    title: str
    generated_at: datetime = field(default_factory=datetime.now)
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    sections: List[ReportSection] = field(default_factory=list)
    summary: str = ""
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "report_id": self.report_id,
            "report_type": self.report_type.value,
            "title": self.title,
            "generated_at": self.generated_at.isoformat(),
            "period_start": self.period_start.isoformat() if self.period_start else None,
            "period_end": self.period_end.isoformat() if self.period_end else None,
            "sections": [
                {
                    "title": section.title,
                    "content": section.content,
                    "charts": section.charts,
                    "tables": section.tables,
                    "recommendations": section.recommendations
                }
                for section in self.sections
            ],
            "summary": self.summary,
            "recommendations": self.recommendations,
            "metadata": self.metadata
        }

    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    def to_markdown(self) -> str:
        """转换为Markdown格式"""
        md_lines = [
            f"# {self.title}",
            f"",
            f"**报告类型:** {self.report_type.value}",
            f"**生成时间:** {self.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
        ]

        if self.period_start and self.period_end:
            md_lines.extend([
                f"**统计周期:** {self.period_start.strftime('%Y-%m-%d')} 至 {self.period_end.strftime('%Y-%m-%d')}",
                ""
            ])

        # 摘要
        if self.summary:
            md_lines.extend([
                "## 摘要",
                "",
                self.summary,
                ""
            ])

        # 各个章节
        for section in self.sections:
            md_lines.extend([
                f"## {section.title}",
                ""
            ])

            # 内容
            for key, value in section.content.items():
                if isinstance(value, (int, float)):
                    md_lines.append(f"- **{key}:** {value}")
                elif isinstance(value, str):
                    md_lines.append(f"- **{key}:** {value}")
                elif isinstance(value, dict):
                    md_lines.append(f"- **{key}:**")
                    for sub_key, sub_value in value.items():
                        md_lines.append(f"  - {sub_key}: {sub_value}")
                md_lines.append("")

            # 表格
            for table in section.tables:
                if table.get("headers") and table.get("rows"):
                    md_lines.append(f"### {table.get('title', '表格')}")
                    headers = table["headers"]
                    md_lines.append("| " + " | ".join(headers) + " |")
                    md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                    for row in table["rows"]:
                        md_lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
                    md_lines.append("")

            # 建议
            if section.recommendations:
                md_lines.append("### 建议")
                for rec in section.recommendations:
                    md_lines.append(f"- {rec}")
                md_lines.append("")

        # 总体建议
        if self.recommendations:
            md_lines.extend([
                "## 总体建议",
                ""
            ])
            for rec in self.recommendations:
                md_lines.append(f"- {rec}")
            md_lines.append("")

        return "\n".join(md_lines)


class ReportGenerator:
    """报告生成器"""

    def __init__(self, output_dir: str = "reports"):
        """
        初始化报告生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.system_monitor = get_system_monitor()
        self.business_metrics = get_business_metrics_collector()

    async def generate_daily_summary(self, date: Optional[datetime] = None) -> MonitoringReport:
        """生成日报"""
        if date is None:
            date = get_utc_now().date()
        else:
            date = date.date()

        start_time = datetime.combine(date, datetime.min.time())
        end_time = datetime.combine(date, datetime.max.time())

        report = MonitoringReport(
            report_id=f"daily_summary_{date.strftime('%Y%m%d')}",
            report_type=ReportType.DAILY_SUMMARY,
            title=f"AI Writer 日报 - {date.strftime('%Y年%m月%d日')}",
            period_start=start_time,
            period_end=end_time
        )

        # 系统概览章节
        system_section = await self._generate_system_overview_section(start_time, end_time)
        report.sections.append(system_section)

        # 业务指标章节
        business_section = await self._generate_business_metrics_section(start_time, end_time)
        report.sections.append(business_section)

        # 性能分析章节
        performance_section = await self._generate_performance_section(start_time, end_time)
        report.sections.append(performance_section)

        # 健康检查章节
        health_section = await self._generate_health_section()
        report.sections.append(health_section)

        # 生成摘要和建议
        report.summary = self._generate_summary(report.sections)
        report.recommendations = self._generate_recommendations(report.sections)

        return report

    async def generate_weekly_summary(self, start_date: Optional[datetime] = None) -> MonitoringReport:
        """生成周报"""
        if start_date is None:
            # 默认为本周开始
            today = get_utc_now().date()
            start_date = datetime.combine(today - timedelta(days=today.weekday()), datetime.min.time())

        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)

        report = MonitoringReport(
            report_id=f"weekly_summary_{start_date.strftime('%Y%m%d')}",
            report_type=ReportType.WEEKLY_SUMMARY,
            title=f"AI Writer 周报 - {start_date.strftime('%Y年%m月%d日')} 至 {end_date.strftime('%Y年%m月%d日')}",
            period_start=start_date,
            period_end=end_date
        )

        # 添加周报特有的章节
        trends_section = await self._generate_trends_section(start_date, end_date)
        report.sections.append(trends_section)

        # 其他章节与日报类似
        system_section = await self._generate_system_overview_section(start_date, end_date)
        report.sections.append(system_section)

        business_section = await self._generate_business_metrics_section(start_date, end_date)
        report.sections.append(business_section)

        performance_section = await self._generate_performance_section(start_date, end_date)
        report.sections.append(performance_section)

        # 生成摘要和建议
        report.summary = self._generate_summary(report.sections)
        report.recommendations = self._generate_recommendations(report.sections)

        return report

    async def generate_health_report(self) -> MonitoringReport:
        """生成健康检查报告"""
        report = MonitoringReport(
            report_id=f"health_report_{get_utc_now().strftime('%Y%m%d_%H%M%S')}",
            report_type=ReportType.HEALTH_CHECK,
            title="AI Writer 系统健康检查报告"
        )

        health_section = await self._generate_health_section()
        report.sections.append(health_section)

        alerts_section = await self._generate_alerts_section()
        report.sections.append(alerts_section)

        report.summary = self._generate_summary(report.sections)
        report.recommendations = self._generate_recommendations(report.sections)

        return report

    async def _generate_system_overview_section(self, start_time: datetime, end_time: datetime) -> ReportSection:
        """生成系统概览章节"""
        # 获取系统监控摘要
        monitoring_summary = self.system_monitor.get_monitoring_summary()

        # 获取指标统计
        metrics_summary = self.system_monitor.get_metrics_summary()

        content = {
            "总体健康状态": monitoring_summary["overall_health"],
            "活跃健康检查数": monitoring_summary["active_health_checks"],
            "活跃告警数": monitoring_summary["active_alerts_count"],
            "监控状态": "运行中" if monitoring_summary["monitoring_running"] else "已停止"
        }

        # 生成趋势表格
        cpu_metrics = self.system_monitor.metrics_collector.get_metrics_history("system_cpu_usage", since=start_time)
        memory_metrics = self.system_monitor.metrics_collector.get_metrics_history("system_memory_usage", since=start_time)

        system_trends_table = {
            "title": "系统资源趋势",
            "headers": ["指标", "平均值", "最大值", "最小值"],
            "rows": []
        }

        if cpu_metrics:
            cpu_values = [m.value for m in cpu_metrics]
            system_trends_table["rows"].append([
                "CPU使用率(%)",
                f"{sum(cpu_values) / len(cpu_values):.1f}",
                f"{max(cpu_values):.1f}",
                f"{min(cpu_values):.1f}"
            ])

        if memory_metrics:
            memory_values = [m.value for m in memory_metrics]
            system_trends_table["rows"].append([
                "内存使用率(%)",
                f"{sum(memory_values) / len(memory_values):.1f}",
                f"{max(memory_values):.1f}",
                f"{min(memory_values):.1f}"
            ])

        recommendations = []
        if monitoring_summary["active_alerts_count"] > 0:
            recommendations.append("系统存在活跃告警，建议及时处理")

        return ReportSection(
            title="系统概览",
            content=content,
            tables=[system_trends_table],
            recommendations=recommendations
        )

    async def _generate_business_metrics_section(self, start_time: datetime, end_time: datetime) -> ReportSection:
        """生成业务指标章节"""
        # 获取业务摘要
        business_summary = self.business_metrics.get_business_summary(
            time_window_hours=int((end_time - start_time).total_seconds() / 3600)
        )

        content = {
            "内容生成总数": business_summary["content_metrics"]["total_generated"],
            "活跃用户数": business_summary["user_metrics"]["active_users_count"],
            "总Token数": business_summary["content_metrics"]["total_tokens"],
            "平均质量分数": f"{business_summary['content_metrics']['average_quality']:.2f}",
            "LLM调用总数": business_summary["performance_metrics"]["llm_calls_total"],
            "LLM成功率": f"{business_summary['performance_metrics']['llm_success_rate']:.1%}",
            "LLM总成本": f"${business_summary['performance_metrics']['llm_total_cost']:.2f}"
        }

        # 内容类型分布表格
        content_types_table = {
            "title": "内容类型分布",
            "headers": ["内容类型", "生成数量"],
            "rows": []
        }

        for content_type, count in business_summary["content_metrics"]["by_type"].items():
            content_types_table["rows"].append([content_type, count])

        recommendations = []
        if business_summary["content_metrics"]["average_quality"] < 0.7:
            recommendations.append("内容质量分数偏低，建议优化生成策略")
        if business_summary["performance_metrics"]["llm_success_rate"] < 0.95:
            recommendations.append("LLM调用成功率偏低，建议检查网络和模型配置")
        if business_summary["user_metrics"]["active_users_count"] == 0:
            recommendations.append("没有活跃用户，建议检查用户访问情况")

        return ReportSection(
            title="业务指标",
            content=content,
            tables=[content_types_table],
            recommendations=recommendations
        )

    async def _generate_performance_section(self, start_time: datetime, end_time: datetime) -> ReportSection:
        """生成性能分析章节"""
        # 获取性能指标
        llm_response_times = self.system_monitor.metrics_collector.get_metrics_history("llm_response_time", since=start_time)
        tool_response_times = self.system_monitor.metrics_collector.get_metrics_history("tool_response_time", since=start_time)

        content = {
            "LLM调用次数": len(llm_response_times),
            "工具调用次数": len(tool_response_times)
        }

        if llm_response_times:
            response_times = [m.value for m in llm_response_times]
            content.update({
                "LLM平均响应时间": f"{sum(response_times) / len(response_times):.2f}s",
                "LLM最大响应时间": f"{max(response_times):.2f}s",
                "LLM最小响应时间": f"{min(response_times):.2f}s"
            })

        if tool_response_times:
            tool_times = [m.value for m in tool_response_times]
            content.update({
                "工具平均响应时间": f"{sum(tool_times) / len(tool_times):.3f}s",
                "工具最大响应时间": f"{max(tool_times):.3f}s"
            })

        # 性能趋势表格
        performance_table = {
            "title": "性能指标趋势",
            "headers": ["指标名称", "调用次数", "平均响应时间", "最大响应时间"],
            "rows": []
        }

        if llm_response_times:
            response_times = [m.value for m in llm_response_times]
            performance_table["rows"].append([
                "LLM调用",
                len(response_times),
                f"{sum(response_times) / len(response_times):.2f}s",
                f"{max(response_times):.2f}s"
            ])

        if tool_response_times:
            tool_times = [m.value for m in tool_response_times]
            performance_table["rows"].append([
                "工具调用",
                len(tool_times),
                f"{sum(tool_times) / len(tool_times):.3f}s",
                f"{max(tool_times):.3f}s"
            ])

        recommendations = []
        if llm_response_times:
            avg_llm_time = sum(m.value for m in llm_response_times) / len(llm_response_times)
            if avg_llm_time > 10:
                recommendations.append("LLM响应时间较长，建议优化模型配置或使用更快的模型")
        if tool_response_times:
            avg_tool_time = sum(m.value for m in tool_response_times) / len(tool_response_times)
            if avg_tool_time > 1:
                recommendations.append("工具响应时间较长，建议优化工具实现")

        return ReportSection(
            title="性能分析",
            content=content,
            tables=[performance_table],
            recommendations=recommendations
        )

    async def _generate_health_section(self) -> ReportSection:
        """生成健康检查章节"""
        health_results = self.system_monitor.health_checker.get_last_results()

        content = {
            "总体健康状态": self.system_monitor.health_checker.get_overall_status().value,
            "健康检查数量": len(health_results)
        }

        # 健康检查状态表格
        health_table = {
            "title": "健康检查详情",
            "headers": ["检查项", "状态", "响应时间", "消息"],
            "rows": []
        }

        for name, check in health_results.items():
            health_table["rows"].append([
                name,
                check.status.value,
                f"{check.response_time:.3f}s",
                check.message
            ])

        recommendations = []
        unhealthy_checks = [name for name, check in health_results.items() if check.status == HealthStatus.UNHEALTHY]
        warning_checks = [name for name, check in health_results.items() if check.status == HealthStatus.WARNING]

        if unhealthy_checks:
            recommendations.append(f"以下健康检查失败: {', '.join(unhealthy_checks)}")
        if warning_checks:
            recommendations.append(f"以下健康检查有警告: {', '.join(warning_checks)}")

        return ReportSection(
            title="系统健康",
            content=content,
            tables=[health_table],
            recommendations=recommendations
        )

    async def _generate_alerts_section(self) -> ReportSection:
        """生成告警章节"""
        active_alerts = self.system_monitor.alert_manager.get_active_alerts()
        recent_alerts = self.system_monitor.alert_manager.get_all_alerts(limit=50)

        content = {
            "活跃告警数": len(active_alerts),
            "近期告警总数": len(recent_alerts)
        }

        # 活跃告警表格
        active_alerts_table = {
            "title": "活跃告警",
            "headers": ["级别", "标题", "时间", "消息"],
            "rows": []
        }

        for alert in active_alerts:
            active_alerts_table["rows"].append([
                alert.level.value,
                alert.title,
                alert.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                alert.message
            ])

        # 告警统计
        alert_stats = {}
        for alert in recent_alerts:
            level = alert.level.value
            alert_stats[level] = alert_stats.get(level, 0) + 1

        content["告警统计"] = alert_stats

        recommendations = []
        critical_alerts = [a for a in active_alerts if a.level == AlertLevel.CRITICAL]
        error_alerts = [a for a in active_alerts if a.level == AlertLevel.ERROR]

        if critical_alerts:
            recommendations.append(f"存在 {len(critical_alerts)} 个严重告警，需要立即处理")
        if error_alerts:
            recommendations.append(f"存在 {len(error_alerts)} 个错误告警，建议尽快处理")

        return ReportSection(
            title="告警信息",
            content=content,
            tables=[active_alerts_table],
            recommendations=recommendations
        )

    async def _generate_trends_section(self, start_time: datetime, end_time: datetime) -> ReportSection:
        """生成趋势分析章节"""
        # 这里可以实现更复杂的趋势分析逻辑
        # 比如对比本周与上周的数据，计算增长率等

        content = {
            "趋势分析": "功能开发中，将包含周环比分析、趋势预测等"
        }

        return ReportSection(
            title="趋势分析",
            content=content
        )

    def _generate_summary(self, sections: List[ReportSection]) -> str:
        """生成报告摘要"""
        summary_parts = []

        # 从各个章节提取关键信息
        for section in sections:
            if section.title == "系统概览":
                overall_health = section.content.get("总体健康状态", "未知")
                active_alerts = section.content.get("活跃告警数", 0)
                summary_parts.append(f"系统整体状态为{overall_health}，当前有{active_alerts}个活跃告警")

            elif section.title == "业务指标":
                total_content = section.content.get("内容生成总数", 0)
                active_users = section.content.get("活跃用户数", 0)
                avg_quality = section.content.get("平均质量分数", 0)
                summary_parts.append(f"期间共生成内容{total_content}个，服务{active_users}个活跃用户，平均质量分数为{avg_quality}")

            elif section.title == "性能分析":
                llm_calls = section.content.get("LLM调用次数", 0)
                if llm_calls > 0:
                    avg_response = section.content.get("LLM平均响应时间", "0s")
                    summary_parts.append(f"完成LLM调用{llm_calls}次，平均响应时间{avg_response}")

            elif section.title == "系统健康":
                health_status = section.content.get("总体健康状态", "未知")
                checks_count = section.content.get("健康检查数量", 0)
                summary_parts.append(f"系统健康状态为{health_status}，共{checks_count}项健康检查")

        return "。".join(summary_parts) + "。"

    def _generate_recommendations(self, sections: List[ReportSection]) -> List[str]:
        """生成总体建议"""
        all_recommendations = []

        # 收集所有章节的建议
        for section in sections:
            all_recommendations.extend(section.recommendations)

        # 去重并返回
        return list(set(all_recommendations))

    async def save_report(self, report: MonitoringReport, formats: List[str] = None) -> Dict[str, str]:
        """
        保存报告到文件

        Args:
            report: 监控报告
            formats: 保存格式列表，支持 ['json', 'markdown']

        Returns:
            Dict[str, str]: 保存的文件路径
        """
        if formats is None:
            formats = ['json', 'markdown']

        saved_files = {}
        timestamp = get_utc_now().strftime('%Y%m%d_%H%M%S')

        # 保存JSON格式
        if 'json' in formats:
            json_file = self.output_dir / f"{report.report_id}_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                f.write(report.to_json())
            saved_files['json'] = str(json_file)

        # 保存Markdown格式
        if 'markdown' in formats:
            md_file = self.output_dir / f"{report.report_id}_{timestamp}.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(report.to_markdown())
            saved_files['markdown'] = str(md_file)

        logger.info(f"Report saved: {saved_files}")
        return saved_files


# 全局报告生成器实例
_report_generator: Optional[ReportGenerator] = None


def get_report_generator(output_dir: str = "reports") -> ReportGenerator:
    """获取报告生成器实例"""
    global _report_generator
    if _report_generator is None or _report_generator.output_dir.name != output_dir:
        _report_generator = ReportGenerator(output_dir)
    return _report_generator


# 便捷函数
async def generate_daily_report(date: Optional[datetime] = None, save: bool = True) -> MonitoringReport:
    """生成日报"""
    generator = get_report_generator()
    report = await generator.generate_daily_summary(date)

    if save:
        await generator.save_report(report)

    return report


async def generate_health_report(save: bool = True) -> MonitoringReport:
    """生成健康检查报告"""
    generator = get_report_generator()
    report = await generator.generate_health_report()

    if save:
        await generator.save_report(report)

    return report


# 导出常用功能
__all__ = [
    "ReportGenerator",
    "MonitoringReport",
    "ReportSection",
    "ReportType",
    "get_report_generator",
    "generate_daily_report",
    "generate_health_report"
]