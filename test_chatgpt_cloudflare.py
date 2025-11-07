"""
快速测试 ChatOpenAI 是否会被 Cloudflare 拦截
"""
import sys
sys.path.insert(0, r"D:\Java\ai_writer\backend")

import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import httpx

async def test_chatgpt_mode():
    """测试 ChatOpenAI 模式"""
    print("=" * 60)
    print("[TEST] ChatOpenAI Mode - Cloudflare Check")
    print("=" * 60)

    # 创建自定义 httpx 客户端
    async_http_client = httpx.AsyncClient(
        headers={
            "User-Agent": "okhttp/4.12.0",
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        },
        timeout=httpx.Timeout(120.0, connect=10.0),
        follow_redirects=True,
        http2=False,
    )

    # 创建 ChatOpenAI 实例
    llm = ChatOpenAI(
        model="gemini-2.5-pro",
        api_key="sk-6d9175726392996b969a9ded28fe2a47dce1884c2023f28fc3cb666d22db57d8",
        base_url="https://204992.xyz/v1",
        temperature=0.7,
        http_async_client=async_http_client
    )

    try:
        print("\n[REQUEST] Sending test message...")
        print("-" * 60)

        # 调用 LLM
        response = await llm.ainvoke([HumanMessage(content="你好，请回复一个字：好")])

        print(f"[SUCCESS] Response received!")
        print(f"[RESPONSE] {response.content}")
        print("-" * 60)
        print("\n[RESULT] ChatOpenAI mode works! NO Cloudflare blocking!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"[FAILED] Request failed: {type(e).__name__}")
        print(f"[ERROR] {str(e)}")
        print("-" * 60)

        if "cloudflare" in str(e).lower() or "403" in str(e) or "forbidden" in str(e).lower():
            print("\n[RESULT] ChatOpenAI mode BLOCKED by Cloudflare!")
        else:
            print("\n[RESULT] Failed, but unclear if Cloudflare-related")

        print("=" * 60)
        return False

    finally:
        await async_http_client.aclose()

if __name__ == "__main__":
    asyncio.run(test_chatgpt_mode())
