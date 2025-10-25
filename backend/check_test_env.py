"""
测试环境检查脚本

运行测试前检查所有必要的条件：
1. 检查依赖是否安装
2. 检查后端服务是否运行
3. 检查数据库连接
4. 检查数据库表是否存在
5. 检查测试用户是否存在
"""

import asyncio
import sys
import importlib.util


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'


def check_package(package_name: str) -> bool:
    """检查包是否安装"""
    spec = importlib.util.find_spec(package_name)
    return spec is not None


def print_check(name: str, passed: bool, details: str = ""):
    """打印检查结果"""
    status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed else f"{Colors.RED}FAIL{Colors.RESET}"
    print(f"[{status}] {name}")
    if details:
        print(f"  {details}")


async def check_backend_service():
    """检查后端服务"""
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/docs")
            return response.status_code == 200
    except Exception:
        return False


async def check_database():
    """检查数据库连接"""
    try:
        from sqlalchemy import text
        from app.core.database import engine

        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"  错误: {str(e)}")
        return False


async def check_tables():
    """检查数据库表"""
    try:
        from sqlalchemy import text
        from app.core.database import engine

        async with engine.begin() as conn:
            result = await conn.execute(
                text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'rewrite_sessions')")
            )
            sessions_exists = result.scalar()

            result = await conn.execute(
                text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'rewrite_results')")
            )
            results_exists = result.scalar()

        return sessions_exists and results_exists
    except Exception as e:
        print(f"  错误: {str(e)}")
        return False


async def check_test_user():
    """检查测试用户"""
    try:
        from sqlalchemy import text
        from app.core.database import engine

        async with engine.begin() as conn:
            result = await conn.execute(
                text("SELECT EXISTS (SELECT FROM users WHERE email = :email)"),
                {"email": "test@example.com"}
            )
            return result.scalar()
    except Exception as e:
        print(f"  错误: {str(e)}")
        return False


async def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}测试环境检查{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

    all_passed = True

    # 1. 检查 Python 依赖
    print(f"{Colors.BOLD}1. 检查 Python 依赖{Colors.RESET}")
    httpx_installed = check_package("httpx")
    print_check("httpx", httpx_installed, "用于 HTTP 请求" if httpx_installed else "请运行: pip install httpx")
    all_passed = all_passed and httpx_installed

    sqlalchemy_installed = check_package("sqlalchemy")
    print_check("sqlalchemy", sqlalchemy_installed, "数据库 ORM")
    all_passed = all_passed and sqlalchemy_installed

    asyncpg_installed = check_package("asyncpg")
    print_check("asyncpg", asyncpg_installed, "PostgreSQL 驱动")
    all_passed = all_passed and asyncpg_installed

    # 2. 检查后端服务
    print(f"\n{Colors.BOLD}2. 检查后端服务{Colors.RESET}")
    service_running = await check_backend_service()
    print_check(
        "后端服务运行中",
        service_running,
        "http://localhost:8000" if service_running else "请启动后端服务: python -m uvicorn app.main:app"
    )
    all_passed = all_passed and service_running

    # 3. 检查数据库连接
    print(f"\n{Colors.BOLD}3. 检查数据库连接{Colors.RESET}")
    db_connected = await check_database()
    print_check(
        "数据库连接正常",
        db_connected,
        "PostgreSQL" if db_connected else "请检查数据库配置和连接"
    )
    all_passed = all_passed and db_connected

    # 4. 检查数据库表
    if db_connected:
        print(f"\n{Colors.BOLD}4. 检查数据库表{Colors.RESET}")
        tables_exist = await check_tables()
        print_check(
            "改写历史表存在",
            tables_exist,
            "rewrite_sessions, rewrite_results" if tables_exist else "请运行: alembic upgrade head"
        )
        all_passed = all_passed and tables_exist

    # 5. 检查测试用户
    if db_connected:
        print(f"\n{Colors.BOLD}5. 检查测试用户{Colors.RESET}")
        user_exists = await check_test_user()
        print_check(
            "测试用户存在",
            user_exists,
            "test@example.com" if user_exists else "请创建测试用户或修改 TEST_USERNAME"
        )
        # 测试用户不存在不影响测试（可以用其他账号）
        if not user_exists:
            print(f"  {Colors.YELLOW}提示: 可以使用其他账号运行测试{Colors.RESET}")

    # 总结
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}Environment check passed! Ready to run tests.{Colors.RESET}")
        print(f"\nRun test:")
        print(f"  python test_rewrite_arena.py")
    else:
        print(f"{Colors.RED}{Colors.BOLD}Environment check failed. Please fix the issues above.{Colors.RESET}")
        sys.exit(1)

    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")


if __name__ == "__main__":
    asyncio.run(main())
