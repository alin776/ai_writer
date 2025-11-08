import asyncio
import httpx

async def test_login():
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            print("Sending login request...")
            response = await client.post(
                "http://localhost:8000/api/v1/auth/login",
                data={
                    "username": "2072855200@qq.com",
                    "password": "zrt3ljnygz@163.com"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_login())
