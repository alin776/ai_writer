"""
自动化性能压测脚本

带完整登录流程和详细日志的性能测试
"""
import asyncio
import time
import sys
import httpx
from pathlib import Path
from datetime import datetime
import json

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.services.ai.novel_analysis_orchestrator import NovelAnalysisOrchestrator
from app.services.novel_analysis_service import NovelAnalysisService
from app.models.work import Work
from sqlalchemy import select
import logging

# 配置日志格式 - 包含更详细的信息
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AutomatedPerformanceTest:
    """自动化性能压测"""

    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.access_token = None
        self.user_id = None
        self.email = None  # 添加email字段
        self.results = []

        logger.info("=" * 80)
        logger.info("自动化性能压测初始化")
        logger.info(f"后端地址: {self.base_url}")
        logger.info("=" * 80)

    async def login(self, email: str, password: str) -> bool:
        """
        登录并获取访问令牌

        Args:
            email: 用户邮箱
            password: 用户密码

        Returns:
            bool: 登录是否成功
        """
        logger.info("=" * 80)
        logger.info("步骤1: 用户登录")
        logger.info(f"邮箱: {email}")
        logger.info("=" * 80)

        # 保存email到实例变量
        self.email = email

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 准备登录数据 (使用OAuth2 form格式)
                login_data = {
                    "username": email,  # OAuth2标准使用username字段
                    "password": password
                }

                logger.info(f"发送登录请求到: {self.base_url}/api/v1/auth/login")
                logger.debug(f"登录数据: username={email}")

                # 发送登录请求 (正确的路由是 /api/v1/auth/login)
                response = await client.post(
                    f"{self.base_url}/api/v1/auth/login",
                    data=login_data,  # 使用data参数发送form数据
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                )

                logger.info(f"登录响应状态码: {response.status_code}")

                if response.status_code != 200:
                    logger.error(f"登录失败! 状态码: {response.status_code}")
                    logger.error(f"响应内容: {response.text}")
                    return False

                # 解析响应
                data = response.json()
                logger.debug(f"登录响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")

                self.access_token = data.get("access_token")

                if not self.access_token:
                    logger.error("登录响应中未找到access_token!")
                    logger.error(f"响应数据: {data}")
                    return False

                logger.info(f"✓ 登录成功! Token: {self.access_token[:20]}...")

                # 获取用户信息
                await self._get_user_info()

                return True

        except httpx.ConnectError as e:
            logger.error(f"连接后端服务失败: {e}")
            logger.error(f"请确认后端服务是否运行在 {self.base_url}")
            return False
        except Exception as e:
            logger.error(f"登录过程发生异常: {e}", exc_info=True)
            return False

    async def _get_user_info(self):
        """获取当前用户信息"""
        try:
            logger.info("获取用户信息...")

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v1/users/me",
                    headers={
                        "Authorization": f"Bearer {self.access_token}"
                    }
                )

                logger.info(f"用户信息响应状态码: {response.status_code}")

                if response.status_code == 200:
                    user_data = response.json()
                    self.user_id = user_data.get("id")
                    logger.info(f"✓ 用户ID: {self.user_id}")
                    logger.info(f"✓ 用户名: {user_data.get('username')}")
                    logger.info(f"✓ 邮箱: {user_data.get('email')}")
                else:
                    logger.warning(f"获取用户信息失败: {response.text}")

        except Exception as e:
            logger.warning(f"获取用户信息异常: {e}")

    async def trigger_analysis(self, work_id: str) -> bool:
        """
        通过API触发分析任务

        Args:
            work_id: 作品ID

        Returns:
            bool: 触发是否成功
        """
        logger.info("=" * 80)
        logger.info("步骤2: 触发分析任务")
        logger.info(f"作品ID: {work_id}")
        logger.info("=" * 80)

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/api/v1/analysis/works/{work_id}/start"

                logger.info(f"发送POST请求到: {url}")
                logger.debug(f"使用Token: {self.access_token[:20]}...")

                response = await client.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {self.access_token}",
                        "Content-Type": "application/json"
                    }
                )

                logger.info(f"触发分析响应状态码: {response.status_code}")

                if response.status_code in [200, 201]:
                    data = response.json()
                    logger.info(f"✓ 分析任务已触发!")
                    logger.debug(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                    return True
                else:
                    logger.error(f"触发分析失败! 状态码: {response.status_code}")
                    logger.error(f"响应内容: {response.text}")
                    return False

        except Exception as e:
            logger.error(f"触发分析异常: {e}", exc_info=True)
            return False

    async def wait_for_analysis_complete(
        self,
        work_id: str,
        max_wait_time: int = 1800,  # 30分钟
        check_interval: int = 5  # 每5秒检查一次
    ) -> dict:
        """
        等待分析完成并监控进度

        Args:
            work_id: 作品ID
            max_wait_time: 最大等待时间(秒)
            check_interval: 检查间隔(秒)

        Returns:
            dict: 分析结果统计
        """
        logger.info("=" * 80)
        logger.info("步骤3: 监控分析进度")
        logger.info(f"最大等待时间: {max_wait_time}秒 ({max_wait_time/60:.1f}分钟)")
        logger.info(f"检查间隔: {check_interval}秒")
        logger.info("=" * 80)

        start_time = time.time()
        last_progress = 0
        check_count = 0

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}/api/v1/analysis/works/{work_id}"

                while True:
                    check_count += 1
                    elapsed = time.time() - start_time

                    # 检查超时
                    if elapsed > max_wait_time:
                        logger.error(f"⏰ 等待超时! 已等待 {elapsed:.1f}秒")
                        break

                    # 查询分析状态
                    logger.debug(f"[检查 #{check_count}] 查询分析状态... (已用时 {elapsed:.1f}秒)")

                    try:
                        response = await client.get(
                            url,
                            headers={
                                "Authorization": f"Bearer {self.access_token}"
                            }
                        )

                        if response.status_code != 200:
                            logger.warning(f"查询状态失败: {response.status_code} - {response.text}")
                            await asyncio.sleep(check_interval)
                            continue

                        data = response.json()

                        status = data.get("status", "unknown")
                        analyzed = data.get("analyzed_chapters", 0)
                        total = data.get("total_chapters", 0)
                        progress = (analyzed / total * 100) if total > 0 else 0

                        # 只在进度变化时打印
                        if analyzed != last_progress:
                            logger.info(
                                f"📊 进度更新: {analyzed}/{total} 章 "
                                f"({progress:.1f}%) | 状态: {status} | "
                                f"用时: {elapsed:.1f}秒"
                            )
                            last_progress = analyzed

                        # 检查是否完成
                        if status in ["completed", "failed", "cancelled"]:
                            logger.info(f"✓ 分析结束! 最终状态: {status}")

                            result = {
                                "status": status,
                                "total_chapters": total,
                                "analyzed_chapters": analyzed,
                                "total_time": elapsed,
                                "avg_time_per_chapter": elapsed / analyzed if analyzed > 0 else 0,
                                "success_rate": (analyzed / total * 100) if total > 0 else 0
                            }

                            logger.info("=" * 80)
                            logger.info("分析结果统计:")
                            logger.info(f"  总章节数: {total}")
                            logger.info(f"  已分析: {analyzed}")
                            logger.info(f"  成功率: {result['success_rate']:.1f}%")
                            logger.info(f"  总耗时: {elapsed:.1f}秒 ({elapsed/60:.1f}分钟)")
                            logger.info(f"  平均速度: {result['avg_time_per_chapter']:.1f}秒/章")
                            logger.info("=" * 80)

                            return result

                    except httpx.ReadTimeout:
                        logger.warning("查询超时,继续等待...")
                    except Exception as e:
                        logger.warning(f"查询异常: {e}")

                    # 等待下一次检查
                    await asyncio.sleep(check_interval)

        except Exception as e:
            logger.error(f"监控过程异常: {e}", exc_info=True)

        # 超时返回
        return {
            "status": "timeout",
            "total_time": time.time() - start_time,
            "error": "等待超时"
        }

    async def run_test(
        self,
        email: str,
        password: str,
        work_id: str,
        test_name: str = "20章性能测试"
    ) -> dict:
        """
        运行完整的性能测试

        Args:
            email: 用户邮箱
            password: 用户密码
            work_id: 作品ID
            test_name: 测试名称

        Returns:
            dict: 测试结果
        """
        logger.info("\n" + "=" * 80)
        logger.info(f"🧪 开始自动化性能测试: {test_name}")
        logger.info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80 + "\n")

        test_start_time = time.time()

        # 1. 登录
        success = await self.login(email, password)
        if not success:
            logger.error("❌ 登录失败,测试终止!")
            return {"success": False, "error": "登录失败"}

        # 2. 触发分析
        success = await self.trigger_analysis(work_id)
        if not success:
            logger.error("❌ 触发分析失败,测试终止!")
            return {"success": False, "error": "触发分析失败"}

        # 3. 等待完成
        result = await self.wait_for_analysis_complete(work_id)

        # 4. 汇总结果
        test_total_time = time.time() - test_start_time

        result.update({
            "test_name": test_name,
            "work_id": work_id,
            "test_total_time": test_total_time,
            "success": result.get("status") == "completed"
        })

        self.results.append(result)

        logger.info("\n" + "=" * 80)
        logger.info(f"✅ 测试完成: {test_name}")
        logger.info(f"总耗时(包含登录): {test_total_time:.1f}秒 ({test_total_time/60:.1f}分钟)")
        logger.info("=" * 80 + "\n")

        return result

    def print_summary(self):
        """打印测试总结"""
        print("\n" + "=" * 80)
        print("📊 自动化性能测试总结")
        print("=" * 80 + "\n")

        if not self.results:
            print("❌ 没有测试结果\n")
            return

        for result in self.results:
            print(f"测试名称: {result.get('test_name')}")
            print(f"作品ID: {result.get('work_id')}")
            print(f"状态: {result.get('status')}")
            print(f"章节: {result.get('analyzed_chapters')}/{result.get('total_chapters')}")
            print(f"耗时: {result.get('total_time', 0)/60:.1f} 分钟")
            print(f"平均速度: {result.get('avg_time_per_chapter', 0):.1f} 秒/章")
            print(f"成功: {'✓' if result.get('success') else '✗'}")
            print("-" * 80)

        print()

    def save_report(self, filepath: str = "automated_performance_report.md"):
        """保存测试报告"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# 自动化性能测试报告\n\n")
                f.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                f.write("## 测试结果\n\n")
                f.write("| 测试名称 | 章节数 | 耗时(分钟) | 平均(秒/章) | 状态 | 成功 |\n")
                f.write("|---------|--------|-----------|-----------|------|------|\n")

                for r in self.results:
                    f.write(
                        f"| {r.get('test_name', 'N/A')} | "
                        f"{r.get('analyzed_chapters', 0)}/{r.get('total_chapters', 0)} | "
                        f"{r.get('total_time', 0)/60:.1f} | "
                        f"{r.get('avg_time_per_chapter', 0):.1f} | "
                        f"{r.get('status', 'unknown')} | "
                        f"{'✓' if r.get('success') else '✗'} |\n"
                    )

                # 添加详细日志
                f.write("\n## 测试配置\n\n")
                f.write(f"- **后端地址**: {self.base_url}\n")
                f.write(f"- **测试账号**: {self.email}\n")
                f.write(f"- **并发配置**: 5个并发任务\n")
                f.write(f"- **超时时间**: 120秒/章\n")

            logger.info(f"✓ 测试报告已保存: {filepath}")

        except Exception as e:
            logger.error(f"保存报告失败: {e}", exc_info=True)


async def main():
    """主函数"""

    # 测试配置
    email = "2072855200@qq.com"
    password = "zrt3ljnygz@163.com"
    work_id_20 = "ddc0183e-76f5-4187-a491-9692a341996b"  # 20章小说（你的账号）

    # 创建测试实例
    tester = AutomatedPerformanceTest()

    # 运行测试
    try:
        result = await tester.run_test(
            email=email,
            password=password,
            work_id=work_id_20,
            test_name="20章小说自动化性能测试"
        )

        # 打印总结
        tester.print_summary()

        # 保存报告
        tester.save_report()

        # 返回结果
        if result.get("success"):
            logger.info("🎉 测试成功完成!")
            sys.exit(0)
        else:
            logger.error("❌ 测试失败!")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("\n⚠️  测试被用户中断!")
        sys.exit(2)
    except Exception as e:
        logger.error(f"❌ 测试过程发生异常: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
