"""
Simple test to debug the issue
"""
import requests

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "2072855200@qq.com"
TEST_PASSWORD = "zrt3ljnygz@163.com"

print("1. Testing login...")
response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data={
        "username": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:200]}")

if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"   Token: {token[:50]}...")

    print("\n2. Testing humanize endpoint...")
    response = requests.post(
        f"{BASE_URL}/api/v1/humanize/rewrite",
        json={
            "text": "This is a test text for AI humanization.",
            "intensity": "medium"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:500]}")
else:
    print("   Login failed, cannot continue")
