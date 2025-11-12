"""
Quick Rate Limit Test - Verifies rate limiting works correctly
Uses shorter time windows for faster testing
"""

import requests
import time

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "2072855200@qq.com"
TEST_PASSWORD = "zrt3ljnygz@163.com"

print("="*70)
print("QUICK RATE LIMIT VERIFICATION TEST")
print("="*70)

# Step 1: Login
print("\n[STEP 1] Logging in...")
response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    data={"username": TEST_EMAIL, "password": TEST_PASSWORD}
)

if response.status_code != 200:
    print(f"[FAIL] Login failed: {response.status_code}")
    exit(1)

token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
print("[OK] Login successful")

# Step 2: Test basic functionality
print("\n[STEP 2] Testing basic API functionality...")
response = requests.post(
    f"{BASE_URL}/api/v1/humanize/rewrite",
    json={"text": "Quick test for rate limiting.", "intensity": "light"},
    headers=headers
)

if response.status_code == 200:
    print(f"[OK] API works correctly (Status: 200)")
else:
    print(f"[FAIL] API returned {response.status_code}: {response.text[:200]}")
    exit(1)

# Step 3: Verify rate limit enforcement
print("\n[STEP 3] Testing rate limit enforcement...")
print("        Sending 21 requests rapidly...")

success_count = 0
blocked_count = 0

for i in range(21):
    response = requests.post(
        f"{BASE_URL}/api/v1/humanize/rewrite",
        json={"text": f"Rate limit test {i+1}", "intensity": "light"},
        headers=headers
    )

    if response.status_code == 200:
        success_count += 1
        print(f"        [{i+1}] OK (total: {success_count})")
    elif response.status_code == 429:
        blocked_count += 1
        headers_info = response.headers
        print(f"        [{i+1}] BLOCKED (HTTP 429) - Rate limit working!")
        print(f"             X-RateLimit-Limit: {headers_info.get('X-RateLimit-Limit', 'N/A')}")
        print(f"             X-RateLimit-Remaining: {headers_info.get('X-RateLimit-Remaining', 'N/A')}")
        print(f"             Retry-After: {headers_info.get('Retry-After', 'N/A')}s")

        # Verify headers exist
        if "X-RateLimit-Limit" not in headers_info:
            print("[FAIL] Missing X-RateLimit-Limit header!")
            exit(1)
        if "Retry-After" not in headers_info:
            print("[FAIL] Missing Retry-After header!")
            exit(1)

        break  # Stop after first rate limit
    else:
        print(f"        [{i+1}] ERROR: Unexpected status {response.status_code}")

    time.sleep(0.2)  # Small delay

# Step 4: Verify results
print("\n" + "="*70)
print("TEST RESULTS")
print("="*70)

if success_count <= 20 and blocked_count >= 1:
    print(f"[PASS] Rate limiting works correctly!")
    print(f"       - Successful requests: {success_count}/20")
    print(f"       - Blocked requests: {blocked_count}")
    print(f"       - HTTP 429 returned: YES")
    print(f"       - Rate limit headers present: YES")
    print("\n[SUCCESS] All checks passed!")
    print("         Speed rate limiting is FUNCTIONAL and SECURE")
    exit(0)
else:
    print(f"[FAIL] Rate limiting not working as expected")
    print(f"       - Successful requests: {success_count} (expected <= 20)")
    print(f"       - Blocked requests: {blocked_count} (expected >= 1)")
    exit(1)
