"""
监控仪表板

提供监控数据的Web API接口，用于构建监控仪表板。
"""

import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import json

from .monitoring import get_system_monitor, AlertLevel, HealthStatus
from .business_metrics import get_business_metrics_collector
from .monitoring_reports import get_report_generator, ReportType
from .logger import get_logger
from app.utils.datetime_utils import get_utc_now

logger = get_logger("monitoring_dashboard")


class MonitoringDashboard:
    """监控仪表板"""

    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        """
        初始化监控仪表板

        Args:
            host: 主机地址
            port: 端口号
        """
        self.host = host
        self.port = port
        self.app = FastAPI(title="AI Writer Monitoring Dashboard", version="1.0.0")
        self.system_monitor = get_system_monitor()
        self.business_metrics = get_business_metrics_collector()
        self.report_generator = get_report_generator()

        # 注册路由
        self._register_routes()

    def _register_routes(self):
        """注册API路由"""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home():
            """仪表板主页"""
            return self._generate_dashboard_html()

        @self.app.get("/api/health")
        async def health_check():
            """健康检查API"""
            try:
                health_results = await self.system_monitor.health_checker.run_all_checks()
                overall_status = self.system_monitor.health_checker.get_overall_status()

                return {
                    "status": overall_status.value,
                    "checks": {name: check.to_dict() for name, check in health_results.items()},
                    "timestamp": get_utc_now().isoformat()
                }
            except Exception as e:
                logger.error(f"Health check API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/metrics/summary")
        async def metrics_summary(
            time_window_hours: int = Query(default=24, ge=1, le=168)  # 1小时到1周
        ):
            """指标摘要API"""
            try:
                # 系统指标
                monitoring_summary = self.system_monitor.get_monitoring_summary()

                # 业务指标
                business_summary = self.business_metrics.get_business_summary(time_window_hours)

                return {
                    "system": monitoring_summary,
                    "business": business_summary,
                    "time_window_hours": time_window_hours,
                    "timestamp": get_utc_now().isoformat()
                }
            except Exception as e:
                logger.error(f"Metrics summary API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/metrics/system")
        async def system_metrics(
            metric_name: Optional[str] = Query(default=None),
            since_hours: int = Query(default=24, ge=1, le=168)
        ):
            """系统指标API"""
            try:
                since_time = get_utc_now() - timedelta(hours=since_hours)

                if metric_name:
                    # 获取特定指标的历史数据
                    metrics = self.system_monitor.metrics_collector.get_metrics_history(
                        metric_name, since=since_time
                    )
                    return {
                        "metric_name": metric_name,
                        "data": [metric.to_dict() for metric in metrics],
                        "since": since_time.isoformat(),
                        "count": len(metrics)
                    }
                else:
                    # 获取所有指标的最新值
                    all_metrics = self.system_monitor.get_metrics_summary()
                    return {
                        "metrics": all_metrics,
                        "timestamp": get_utc_now().isoformat()
                    }
            except Exception as e:
                logger.error(f"System metrics API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/metrics/business")
        async def business_metrics(
            time_window_hours: int = Query(default=24, ge=1, le=168)
        ):
            """业务指标API"""
            try:
                business_summary = self.business_metrics.get_business_summary(time_window_hours)
                detailed_metrics = self.business_metrics.get_detailed_metrics(limit=1000)

                return {
                    "summary": business_summary,
                    "detailed": detailed_metrics,
                    "time_window_hours": time_window_hours,
                    "timestamp": get_utc_now().isoformat()
                }
            except Exception as e:
                logger.error(f"Business metrics API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/alerts")
        async def alerts(
            level: Optional[str] = Query(default=None),
            active_only: bool = Query(default=True),
            limit: int = Query(default=100, ge=1, le=1000)
        ):
            """告警API"""
            try:
                if active_only:
                    alerts = self.system_monitor.alert_manager.get_active_alerts()
                else:
                    alerts = self.system_monitor.alert_manager.get_all_alerts(limit)

                # 按级别过滤
                if level:
                    try:
                        alert_level = AlertLevel(level)
                        alerts = [alert for alert in alerts if alert.level == alert_level]
                    except ValueError:
                        raise HTTPException(status_code=400, detail=f"Invalid alert level: {level}")

                return {
                    "alerts": [alert.to_dict() for alert in alerts],
                    "total_count": len(alerts),
                    "filters": {
                        "level": level,
                        "active_only": active_only,
                        "limit": limit
                    },
                    "timestamp": get_utc_now().isoformat()
                }
            except Exception as e:
                logger.error(f"Alerts API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/alerts/{alert_id}/resolve")
        async def resolve_alert(alert_id: str):
            """解决告警API"""
            try:
                success = self.system_monitor.alert_manager.resolve_alert(alert_id)
                if success:
                    return {"message": f"Alert {alert_id} resolved successfully"}
                else:
                    raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
            except Exception as e:
                logger.error(f"Resolve alert API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/reports/generate")
        async def generate_report(
            report_type: str = Query(..., description="报告类型: daily, weekly, health"),
            date: Optional[str] = Query(default=None, description="日期 (YYYY-MM-DD)")
        ):
            """生成报告API"""
            try:
                # 解析报告类型
                if report_type == "daily":
                    report_date = datetime.strptime(date, "%Y-%m-%d") if date else None
                    report = await self.report_generator.generate_daily_summary(report_date)
                elif report_type == "weekly":
                    start_date = datetime.strptime(date, "%Y-%m-%d") if date else None
                    report = await self.report_generator.generate_weekly_summary(start_date)
                elif report_type == "health":
                    report = await self.report_generator.generate_health_report()
                else:
                    raise HTTPException(status_code=400, detail=f"Invalid report type: {report_type}")

                # 保存报告
                saved_files = await self.report_generator.save_report(report)

                return {
                    "report": report.to_dict(),
                    "saved_files": saved_files,
                    "message": f"{report_type} report generated successfully"
                }
            except ValueError as e:
                raise HTTPException(status_code=400, detail=str(e))
            except Exception as e:
                logger.error(f"Generate report API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/reports/list")
        async def list_reports(
            limit: int = Query(default=20, ge=1, le=100)
        ):
            """列出报告API"""
            try:
                # 这里可以实现报告列表功能
                # 暂时返回示例数据
                return {
                    "reports": [
                        {
                            "report_id": "daily_summary_20251101",
                            "report_type": "daily_summary",
                            "title": "AI Writer 日报 - 2025年11月01日",
                            "generated_at": "2025-11-01T10:00:00",
                            "files": {
                                "json": "reports/daily_summary_20251101_20251101_100000.json",
                                "markdown": "reports/daily_summary_20251101_20251101_100000.md"
                            }
                        }
                    ],
                    "total_count": 1,
                    "limit": limit,
                    "timestamp": get_utc_now().isoformat()
                }
            except Exception as e:
                logger.error(f"List reports API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/stats/realtime")
        async def realtime_stats():
            """实时统计API"""
            try:
                # 获取最新系统指标
                cpu_metric = self.system_monitor.metrics_collector.get_metric("system_cpu_usage")
                memory_metric = self.system_monitor.metrics_collector.get_metric("system_memory_usage")
                disk_metric = self.system_monitor.metrics_collector.get_metric("system_disk_usage")

                # 获取活跃告警数
                active_alerts = self.system_monitor.alert_manager.get_active_alerts()

                # 获取健康状态
                health_status = self.system_monitor.health_checker.get_overall_status()

                return {
                    "system_resources": {
                        "cpu_usage": cpu_metric.value if cpu_metric else 0,
                        "memory_usage": memory_metric.value if memory_metric else 0,
                        "disk_usage": disk_metric.value if disk_metric else 0
                    },
                    "alerts": {
                        "active_count": len(active_alerts),
                        "critical_count": len([a for a in active_alerts if a.level == AlertLevel.CRITICAL]),
                        "error_count": len([a for a in active_alerts if a.level == AlertLevel.ERROR])
                    },
                    "health": {
                        "status": health_status.value,
                        "checks_count": len(self.system_monitor.health_checker.get_last_results())
                    },
                    "timestamp": get_utc_now().isoformat()
                }
            except Exception as e:
                logger.error(f"Realtime stats API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/config")
        async def get_config():
            """获取配置API"""
            try:
                return {
                    "dashboard": {
                        "title": "AI Writer Monitoring Dashboard",
                        "version": "1.0.0",
                        "refresh_interval": 30  # 秒
                    },
                    "monitoring": {
                        "running": self.system_monitor._running,
                        "interval": 30  # 秒
                    },
                    "features": {
                        "system_monitoring": True,
                        "business_metrics": True,
                        "health_checks": True,
                        "alerts": True,
                        "reports": True
                    }
                }
            except Exception as e:
                logger.error(f"Config API error: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    def _generate_dashboard_html(self) -> str:
        """生成仪表板HTML页面"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Writer 监控仪表板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #333;
        }
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
        .chart-container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .chart-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .alert-list {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .alert-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 4px solid;
        }
        .alert-critical { border-left-color: #dc3545; background-color: #f8d7da; }
        .alert-error { border-left-color: #fd7e14; background-color: #fff3cd; }
        .alert-warning { border-left-color: #ffc107; background-color: #fff3cd; }
        .alert-info { border-left-color: #17a2b8; background-color: #d1ecf1; }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-healthy { background-color: #28a745; }
        .status-warning { background-color: #ffc107; }
        .status-unhealthy { background-color: #dc3545; }
        .refresh-btn {
            background: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 0;
        }
        .refresh-btn:hover { background: #0056b3; }
        @media (max-width: 768px) {
            .chart-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Writer 监控仪表板</h1>
            <p>实时系统状态 · 业务指标 · 性能监控</p>
            <button class="refresh-btn" onclick="refreshData()">🔄 刷新数据</button>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value" id="cpu-usage">-</div>
                <div class="stat-label">CPU 使用率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="memory-usage">-</div>
                <div class="stat-label">内存使用率</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="active-alerts">-</div>
                <div class="stat-label">活跃告警</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="health-status">
                    <span class="status-indicator" id="health-indicator"></span>
                    <span id="health-text">-</span>
                </div>
                <div class="stat-label">系统健康状态</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart-container">
                <h3>系统资源使用趋势</h3>
                <canvas id="resourceChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>内容生成统计</h3>
                <canvas id="contentChart"></canvas>
            </div>
        </div>

        <div class="chart-container">
            <h3>LLM 调用性能</h3>
            <canvas id="performanceChart"></canvas>
        </div>

        <div class="alert-list">
            <h3>🚨 最新告警</h3>
            <div id="alerts-container">
                <p>加载中...</p>
            </div>
        </div>
    </div>

    <script>
        let resourceChart, contentChart, performanceChart;

        async function initCharts() {
            // 资源使用趋势图
            const resourceCtx = document.getElementById('resourceChart').getContext('2d');
            resourceChart = new Chart(resourceCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CPU (%)',
                        data: [],
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        tension: 0.1
                    }, {
                        label: '内存 (%)',
                        data: [],
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });

            // 内容生成统计图
            const contentCtx = document.getElementById('contentChart').getContext('2d');
            contentChart = new Chart(contentCtx, {
                type: 'doughnut',
                data: {
                    labels: [],
                    datasets: [{
                        data: [],
                        backgroundColor: [
                            '#FF6384',
                            '#36A2EB',
                            '#FFCE56',
                            '#4BC0C0',
                            '#9966FF'
                        ]
                    }]
                },
                options: {
                    responsive: true
                }
            });

            // 性能图
            const performanceCtx = document.getElementById('performanceChart').getContext('2d');
            performanceChart = new Chart(performanceCtx, {
                type: 'bar',
                data: {
                    labels: ['响应时间', '成功率'],
                    datasets: [{
                        label: 'LLM 调用',
                        data: [0, 0],
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        async function refreshData() {
            try {
                // 获取实时统计
                const realtimeResponse = await fetch('/api/stats/realtime');
                const realtimeData = await realtimeResponse.json();

                // 更新统计卡片
                document.getElementById('cpu-usage').textContent =
                    realtimeData.system_resources.cpu_usage.toFixed(1) + '%';
                document.getElementById('memory-usage').textContent =
                    realtimeData.system_resources.memory_usage.toFixed(1) + '%';
                document.getElementById('active-alerts').textContent =
                    realtimeData.alerts.active_count;

                // 更新健康状态
                const healthStatus = realtimeData.health.status;
                const healthIndicator = document.getElementById('health-indicator');
                const healthText = document.getElementById('health-text');

                healthIndicator.className = 'status-indicator status-' + healthStatus;
                healthText.textContent = healthStatus === 'healthy' ? '健康' :
                                       healthStatus === 'warning' ? '警告' : '异常';

                // 获取业务指标
                const metricsResponse = await fetch('/api/metrics/business');
                const metricsData = await metricsResponse.json();

                // 更新内容生成图表
                const contentTypes = Object.keys(metricsData.summary.content_metrics.by_type);
                const contentCounts = Object.values(metricsData.summary.content_metrics.by_type);

                contentChart.data.labels = contentTypes;
                contentChart.data.datasets[0].data = contentCounts;
                contentChart.update();

                // 更新性能图表
                const perfMetrics = metricsData.summary.performance_metrics;
                performanceChart.data.datasets[0].data = [
                    perfMetrics.llm_avg_response_time || 0,
                    perfMetrics.llm_success_rate * 100 || 0
                ];
                performanceChart.update();

                // 获取告警
                const alertsResponse = await fetch('/api/alerts?active_only=true&limit=10');
                const alertsData = await alertsResponse.json();

                // 更新告警列表
                const alertsContainer = document.getElementById('alerts-container');
                if (alertsData.alerts.length === 0) {
                    alertsContainer.innerHTML = '<p>✅ 暂无活跃告警</p>';
                } else {
                    alertsContainer.innerHTML = alertsData.alerts.map(alert => `
                        <div class="alert-item alert-${alert.level}">
                            <strong>${alert.title}</strong> - ${alert.message}
                            <br><small>${new Date(alert.timestamp).toLocaleString()}</small>
                        </div>
                    `).join('');
                }

                console.log('数据刷新完成');

            } catch (error) {
                console.error('刷新数据失败:', error);
            }
        }

        // 初始化
        document.addEventListener('DOMContentLoaded', function() {
            initCharts();
            refreshData();

            // 自动刷新
            setInterval(refreshData, 30000); // 30秒刷新一次
        });
    </script>
</body>
</html>
        """

    async def start(self):
        """启动仪表板服务"""
        logger.info(f"Starting monitoring dashboard on {self.host}:{self.port}")

        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )

        server = uvicorn.Server(config)
        await server.serve()


# 便捷函数
async def start_dashboard(host: str = "127.0.0.1", port: int = 8080):
    """启动监控仪表板"""
    dashboard = MonitoringDashboard(host, port)
    await dashboard.start()


# 导出常用功能
__all__ = [
    "MonitoringDashboard",
    "start_dashboard"
]