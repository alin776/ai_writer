"""
快速测试脚本 - AI改写竞技场优化

运行方式:
    python scripts/quick_test.py

依赖安装:
    pip install requests
"""

import sys

# 检查依赖
try:
    import requests
    import time
except ImportError as e:
    print(f"❌ 缺少依赖: {e}")
    print(f"\n请运行: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"
EMAIL = "2072855200@qq.com"
PASSWORD = "zrt3ljnygz@163.com"


def login():
    """登录获取Token (使用form data)"""
    print("🔐 登录中...")

    # ⚠️ 使用 form data 而不是 JSON
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        data={  # 使用 data 参数
            "username": EMAIL,
            "password": PASSWORD
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ 登录成功! Token: {token[:20]}...")
        return token
    else:
        print(f"❌ 登录失败: {response.status_code}")
        print(response.text)
        return None


def test_rewrite_arena(token):
    """测试改写竞技场"""
    print("\n🧪 测试改写竞技场...")

    # 只使用已启用的模型
    test_data = {
        "text": "主角走进房间，看到了桌子上的剑。",
        "mode": "expand",
        "model_names": ["gemini-2.5-pro", "gpt-5"]  # 只用enabled=True的模型
    }

    print(f"📝 测试文本: {test_data['text']}")
    print(f"🎯 模型数量: {len(test_data['model_names'])}")
    print(f"⏱️  预期: 15-20秒 (并发限制3,超时30s)")
    print(f"💡 使用已启用模型: {', '.join(test_data['model_names'])}")

    start_time = time.time()

    response = requests.post(
        f"{BASE_URL}/api/v1/ai/rewrite-arena/rewrite",
        json=test_data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        timeout=120
    )

    elapsed = time.time() - start_time

    if response.status_code == 200:
        data = response.json()
        results = data["results"]

        print(f"\n✅ 测试完成! 总耗时: {elapsed:.2f}秒")
        print(f"\n📊 结果:")

        for i, result in enumerate(results, 1):
            model = result["model_name"]
            error = result.get("error")
            time_cost = result["elapsed_time"]
            words = result["word_count"]

            if error:
                print(f"   {i}. [{model}] ❌ {error} ({time_cost:.2f}s)")
            else:
                print(f"   {i}. [{model}] ✅ 成功 ({time_cost:.2f}s, {words}字)")

        # 统计
        success = sum(1 for r in results if not r.get("error"))
        timeout = sum(1 for r in results if r.get("error") and "超时" in r.get("error", ""))

        print(f"\n📈 统计:")
        print(f"   成功: {success}/{len(results)}")
        print(f"   超时: {timeout}/{len(results)}")

    else:
        print(f"❌ 测试失败: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    print("=" * 60)
    print("AI改写竞技场优化 - 快速测试")
    print("=" * 60)

    token = login()
    if token:
        test_rewrite_arena(token)

    print("\n" + "=" * 60)
