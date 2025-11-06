"""
测试运行器 - 自动运行所有Phase 1.2测试

一键运行：
1. 单元测试（pytest）
2. 端到端集成测试
3. 30轮长对话测试
"""

import subprocess
import sys
import os
import io

# 🔧 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(msg):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}")
    print(f"{msg}")
    print(f"{'='*70}{Colors.ENDC}\n")


def print_success(msg):
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")


def print_error(msg):
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")


def print_info(msg):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.ENDC}")


def run_command(cmd, description):
    """运行命令并返回结果"""
    print_info(f"运行: {description}")
    print(f"  命令: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            capture_output=False,  # 显示实时输出
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        if result.returncode == 0:
            print_success(f"{description} - 通过")
            return True
        else:
            print_error(f"{description} - 失败 (退出码: {result.returncode})")
            return False

    except Exception as e:
        print_error(f"{description} - 异常: {str(e)}")
        return False


def main():
    """主测试流程"""

    print_header("Phase 1.2 上下文管理 - 自动测试套件")

    results = {}

    # ========== 测试1: 单元测试 ==========
    print_header("测试1: 单元测试 (pytest)")

    results['unit_tests'] = run_command(
        [sys.executable, "-m", "pytest", "test_context_manager.py", "-v"],
        "单元测试"
    )

    # ========== 测试2: 端到端集成测试 ==========
    print_header("测试2: 端到端集成测试")

    results['e2e_tests'] = run_command(
        [sys.executable, "test_e2e_context_integration.py"],
        "端到端集成测试"
    )

    # ========== 测试3: 30轮长对话测试 ==========
    print_header("测试3: 30轮长对话测试")

    print_info("⚠️ 此测试需要较长时间（约5-10分钟），请耐心等待...")

    results['long_conversation'] = run_command(
        [sys.executable, "test_long_conversation_30.py"],
        "30轮长对话测试"
    )

    # ========== 总结 ==========
    print_header("测试总结")

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    print(f"{Colors.BOLD}测试结果:{Colors.ENDC}")
    print(f"  总测试套件: {total}")
    print(f"  {Colors.GREEN}通过: {passed}{Colors.ENDC}")
    print(f"  {Colors.RED}失败: {failed}{Colors.ENDC}\n")

    print(f"{Colors.BOLD}详细结果:{Colors.ENDC}")
    for name, result in results.items():
        status = f"{Colors.GREEN}✓ 通过{Colors.ENDC}" if result else f"{Colors.RED}✗ 失败{Colors.ENDC}"
        print(f"  {name}: {status}")

    print("\n" + "="*70)

    if all(results.values()):
        print(f"{Colors.GREEN}{Colors.BOLD}✅ 所有测试通过！Phase 1.2 验收成功！{Colors.ENDC}\n")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ 部分测试失败，请检查错误信息{Colors.ENDC}\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
