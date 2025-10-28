"""
Token追踪功能自动化测试
测试完整的humanize API流程,验证token统计是否正确

修复内容:
- P0: 添加依赖检查
- P0: 添加服务器连接检查
- P0: 修复Unicode编码问题
- P1: 使用环境变量管理凭证
- P1: 添加timeout参数
- P2: 增强Token验证
"""

import sys
import os
import time

# ========== P0修复: 依赖检查 ==========
try:
    import requests
except ImportError:
    print("[ERROR] 缺少依赖: requests")
    print("请运行: pip install requests")
    sys.exit(1)

# ========== P0修复: 设置UTF-8编码(Windows兼容) ==========
if sys.platform == 'win32':
    import io
    # 强制stdout使用UTF-8编码,避免Unicode字符乱码
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding='utf-8',
        errors='replace'
    )

# ========== P1修复: 使用环境变量 ==========
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
EMAIL = os.getenv("TEST_EMAIL", "2072855200@qq.com")
PASSWORD = os.getenv("TEST_PASSWORD", "zrt3ljnygz@163.com")

# 超时设置
DEFAULT_TIMEOUT = 10  # 默认10秒
REWRITE_TIMEOUT = 120  # 改写120秒


def check_server():
    """P0修复: 检查服务器是否运行"""
    print("\n[INFO] 检查服务器连接...")
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=3)
        if response.status_code == 200:
            print(f"[OK] 服务器正在运行: {BASE_URL}")
            return True
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] 无法连接到服务器: {BASE_URL}")
        print("请确保后端服务正在运行:")
        print("  cd backend")
        print("  uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"[ERROR] 服务器检查失败: {e}")
        return False


def login():
    """登录获取token - 使用form data"""
    print("\n" + "="*60)
    print("Step 1: 登录")
    print("="*60)

    url = f"{BASE_URL}/api/v1/auth/login"

    # OAuth2PasswordRequestForm 需要使用 form data
    data = {
        "username": EMAIL,
        "password": PASSWORD
    }

    print(f"POST {url}")
    print(f"Form Data: username={EMAIL}")

    try:
        response = requests.post(url, data=data, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 200:
            result = response.json()
            token = result["access_token"]
            print(f"[OK] 登录成功")
            print(f"  Token: {token[:20]}...")
            return token
        else:
            print(f"[FAIL] 登录失败: {response.status_code}")
            print(f"  Response: {response.text}")
            raise Exception("登录失败")
    except requests.exceptions.Timeout:
        print(f"[ERROR] 请求超时 (>{DEFAULT_TIMEOUT}秒)")
        raise


def get_profile(token):
    """获取用户画像"""
    print("\n" + "="*60)
    print("Step 2: 获取用户画像")
    print("="*60)

    url = f"{BASE_URL}/api/v1/humanize/profile"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"GET {url}")

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 200:
            profile = response.json()
            print(f"[OK] 获取成功")
            print(f"  用户ID: {profile.get('user_id', 'N/A')}")
            print(f"  总使用次数: {profile.get('total_uses', 0)}")
            print(f"  偏好强度: {profile.get('preferred_intensity', 'N/A')}")
            return profile
        else:
            print(f"[FAIL] 获取失败: {response.status_code}")
            print(f"  Response: {response.text}")
            raise Exception("获取画像失败")
    except requests.exceptions.Timeout:
        print(f"[ERROR] 请求超时 (>{DEFAULT_TIMEOUT}秒)")
        raise


def test_humanize_rewrite(token, test_case):
    """测试人性化改写"""
    print("\n" + "="*60)
    print(f"Step 3: 测试改写 - {test_case['name']}")
    print("="*60)

    url = f"{BASE_URL}/api/v1/humanize/rewrite"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": test_case['text'],
        "intensity": test_case['intensity'],
        "ai_function": "rewrite"
    }

    print(f"POST {url}")
    print(f"  文本长度: {len(test_case['text'])} 字符")
    print(f"  强度: {test_case['intensity']}")

    start_time = time.time()

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=REWRITE_TIMEOUT)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            result = response.json()

            print(f"\n[OK] 改写成功 (耗时: {elapsed:.2f}秒)")
            print(f"\n【会话信息】")
            print(f"  Session ID: {result.get('id', 'N/A')}")
            print(f"  AI分数(改写前): {result.get('score_before', 0):.1f}")
            print(f"  AI分数(改写后): {result.get('score_after', 0):.1f}")
            print(f"  改进幅度: {result.get('improvement', 0):.1f}")
            print(f"  处理时间: {result.get('processing_time', 0):.2f}秒")

            print(f"\n【Token统计】★ 关键验证")
            tokens_used = result.get('tokens_used', 0)
            cost = result.get('cost', 0)
            print(f"  总Token: {tokens_used}")
            print(f"  成本: ${cost:.6f}")

            # P2修复: 增强Token验证
            print(f"\n【Token验证】")

            # 验证1: Token必须大于0
            assert tokens_used > 0, "tokens_used应大于0"
            print(f"  [PASS] Token大于0: {tokens_used}")

            # 验证2: Token在合理范围
            assert 100 < tokens_used < 50000, \
                f"tokens_used={tokens_used} 超出合理范围(100-50000)"
            print(f"  [PASS] Token在合理范围")

            # 验证3: 成本大于0
            assert cost > 0, "cost应大于0"
            print(f"  [PASS] 成本大于0: ${cost:.6f}")

            # 验证4: 成本与Token的比例合理
            cost_per_token = cost / tokens_used if tokens_used > 0 else 0
            assert 0.0000001 < cost_per_token < 0.00001, \
                f"单Token成本={cost_per_token:.8f}异常"
            print(f"  [PASS] 单Token成本合理: ${cost_per_token:.8f}")

            # 验证5: 处理时间合理
            processing_time = result.get('processing_time', 0)
            assert processing_time > 0, "processing_time应大于0"
            assert processing_time < 180, "processing_time不应超过3分钟"
            print(f"  [PASS] 处理时间合理: {processing_time:.2f}秒")

            # 显示详细信息
            if result.get('detail'):
                detail = result['detail']
                print(f"\n【详细信息】")

                # 检测到的模式
                if detail.get('detected_patterns'):
                    print(f"  检测到的AI痕迹:")
                    for pattern in detail['detected_patterns'][:3]:
                        print(f"    - {pattern}")

                # 改写预览
                if detail.get('humanized_preview'):
                    preview = detail['humanized_preview']
                    print(f"  改写后预览: {preview[:100]}...")

            print(f"\n[OK] 所有验证通过")

            return result
        else:
            print(f"[FAIL] 改写失败: {response.status_code}")
            print(f"  Response: {response.text}")
            raise Exception("改写失败")
    except requests.exceptions.Timeout:
        print(f"[ERROR] 请求超时 (>{REWRITE_TIMEOUT}秒)")
        print("  改写操作耗时较长,这可能是正常的")
        raise


def get_history(token):
    """获取历史记录"""
    print("\n" + "="*60)
    print("Step 4: 获取历史记录")
    print("="*60)

    url = f"{BASE_URL}/api/v1/humanize/history?page=1&page_size=5"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"GET {url}")

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 200:
            history = response.json()
            print(f"[OK] 获取成功")
            print(f"  总记录数: {history.get('total', 0)}")
            print(f"  当前页: {history.get('page', 1)}")
            print(f"  返回记录: {len(history.get('items', []))}")

            if history.get('items'):
                print(f"\n  最近一条记录:")
                latest = history['items'][0]
                print(f"    - Session ID: {latest.get('id', 'N/A')}")
                print(f"    - 改进幅度: {latest.get('improvement', 0):.1f}")
                print(f"    - Token使用: {latest.get('tokens_used', 0)}")
                print(f"    - 成本: ${latest.get('cost', 0):.6f}")

            return history
        else:
            print(f"[FAIL] 获取失败: {response.status_code}")
            print(f"  Response: {response.text}")
            raise Exception("获取历史失败")
    except requests.exceptions.Timeout:
        print(f"[ERROR] 请求超时 (>{DEFAULT_TIMEOUT}秒)")
        raise


def get_stats(token):
    """获取统计数据"""
    print("\n" + "="*60)
    print("Step 5: 获取统计数据")
    print("="*60)

    url = f"{BASE_URL}/api/v1/humanize/stats"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    print(f"GET {url}")

    try:
        response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

        if response.status_code == 200:
            stats = response.json()
            print(f"[OK] 获取成功")
            print(f"  总使用次数: {stats.get('total_uses', 0)}")
            print(f"  平均改进幅度: {stats.get('avg_improvement', 0):.1f}")
            print(f"  接受率: {stats.get('accept_rate', 0)*100:.1f}%")
            print(f"  总Token消耗: {stats.get('total_tokens', 0)}")
            print(f"  总成本: ${stats.get('total_cost', 0):.6f}")
            print(f"  最常用功能: {stats.get('most_used_function', 'N/A')}")

            return stats
        else:
            print(f"[FAIL] 获取失败: {response.status_code}")
            print(f"  Response: {response.text}")
            raise Exception("获取统计失败")
    except requests.exceptions.Timeout:
        print(f"[ERROR] 请求超时 (>{DEFAULT_TIMEOUT}秒)")
        raise


def main():
    """主测试流程"""
    print("\n" + "="*70)
    print(" Token追踪功能 - 自动化测试 (已修复)")
    print("="*70)
    print(f" 服务器: {BASE_URL}")
    print(f" 账号: {EMAIL}")
    print("="*70)

    # P0修复: 先检查服务器
    if not check_server():
        return False

    # 测试用例
    test_cases = [
        {
            "name": "轻度改写",
            "text": "人工智能技术正在快速发展，为人类社会带来巨大变革。机器学习算法可以从大量数据中学习规律，深度学习模型在图像识别和自然语言处理等领域取得了突破性进展。",
            "intensity": "light"
        }
    ]

    try:
        # Step 1: 登录
        token = login()

        # Step 2: 获取用户画像
        profile = get_profile(token)

        # Step 3: 测试改写
        for test_case in test_cases:
            session = test_humanize_rewrite(token, test_case)
            time.sleep(1)  # 稍作延迟

        # Step 4: 获取历史记录
        history = get_history(token)

        # Step 5: 获取统计数据
        stats = get_stats(token)

        # 总结
        print("\n" + "="*70)
        print(" [SUCCESS] 所有测试通过!")
        print("="*70)
        print(f"\n【测试总结】")
        print(f"  [OK] 登录认证: 通过")
        print(f"  [OK] 用户画像: 通过")
        print(f"  [OK] AI改写: 通过")
        print(f"  [OK] Token统计: 通过 (tokens_used > 0)")
        print(f"  [OK] Token验证: 通过 (范围/比例/成本)")
        print(f"  [OK] 历史记录: 通过")
        print(f"  [OK] 统计数据: 通过")

        print(f"\n【关键验证】★★★")
        print(f"  [OK] Token追踪已正确实现")
        print(f"  [OK] 改写阶段Token已被正确收集")
        print(f"  [OK] 成本计算正常")
        print(f"  [OK] Token在合理范围内")

        return True

    except Exception as e:
        print("\n" + "="*70)
        print(f" [FAIL] 测试失败: {e}")
        print("="*70)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
