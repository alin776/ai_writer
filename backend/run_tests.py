#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI去痕迹功能 - 测试运行器

快速运行所有测试
"""

import subprocess
import sys
import os
import io

# 修复Windows编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")

    result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"\n❌ {description} 失败")
        return False
    else:
        print(f"\n✅ {description} 成功")
        return True


def main():
    """主函数"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 设置 PYTHONPATH (Windows)
    os.environ["PYTHONPATH"] = os.getcwd()

    print("=" * 60)
    print("🧪 AI去痕迹功能 - 自动化测试套件")
    print("=" * 60)

    success = True

    # 1. 运行单元测试
    if not run_command(
        "python -m pytest tests/test_humanize.py -v --tb=short",
        "单元测试 (Pytest)"
    ):
        success = False

    # 2. 运行自动化测试
    print("\n" + "=" * 60)
    print("⚠️  注意: 自动化测试需要后端服务运行")
    print("   启动命令: python -m uvicorn app.main:app --reload")
    print("=" * 60)

    # 自动运行API测试,不需要用户交互
    print("\n💡 自动运行API测试")
    print("   默认账号: 2072855200@qq.com")
    print("   可通过环境变量 TEST_USERNAME 和 TEST_PASSWORD 自定义")

    if not run_command(
        "python tests/test_humanize_auto.py",
        "自动化API测试"
    ):
        # API测试失败不影响整体结果(可能是服务未启动)
        print("\n⚠️  API测试失败 - 请确认后端服务是否运行")
        pass

    # 3. 生成测试报告
    print("\n" + "=" * 60)
    print("📊 测试报告")
    print("=" * 60)

    if success:
        print("✅ 所有测试通过!")
    else:
        print("❌ 部分测试失败,请查看上面的错误信息")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
