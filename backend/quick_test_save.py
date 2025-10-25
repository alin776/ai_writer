"""
快速验证保存改写历史功能

只测试保存功能，不测试其他接口
"""

import asyncio
import httpx
import os


async def test_save_history():
    """测试保存改写历史"""
    base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
    username = os.getenv("TEST_USERNAME", "test@example.com")
    password = os.getenv("TEST_PASSWORD", "password123")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. 登录
        print("▶ 1. 登录...")
        response = await client.post(
            f"{base_url}/api/v1/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code != 200:
            print(f"✗ 登录失败: {response.status_code}")
            return False

        token = response.json()["access_token"]
        print(f"✓ 登录成功")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 2. 保存改写历史
        print("\n▶ 2. 保存改写历史...")
        response = await client.post(
            f"{base_url}/api/v1/rewrite-history/sessions",
            headers=headers,
            json={
                "original_text": "测试文本：主角走进房间。",
                "mode": "expand",
                "context_before": None,
                "context_after": None,
                "custom_requirement": None,
                "results": [
                    {
                        "model_name": "gemini-2.5-pro",
                        "rewritten_text": "主角推开那扇厚重的木门，缓缓走进了这间房间。",
                        "word_count": 25,
                        "elapsed_time": 2.5,
                        "error": None,
                        "is_selected": False
                    },
                    {
                        "model_name": "gpt-5",
                        "rewritten_text": "房门在主角的推动下缓缓打开，他迈步走了进去。",
                        "word_count": 23,
                        "elapsed_time": 1.8,
                        "error": None,
                        "is_selected": False
                    }
                ]
            }
        )

        if response.status_code == 200:
            data = response.json()
            print(f"✓ 保存成功！")
            print(f"  会话ID: {data.get('id')}")
            print(f"  结果数量: {len(data.get('results', []))}")
            return True
        else:
            print(f"✗ 保存失败: {response.status_code}")
            print(f"  错误: {response.text[:200]}")
            return False


async def main():
    print("\n" + "="*60)
    print("快速验证：保存改写历史功能")
    print("="*60 + "\n")

    success = await test_save_history()

    print("\n" + "="*60)
    if success:
        print("✅ 测试通过！修复成功！")
    else:
        print("❌ 测试失败！需要进一步检查")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
