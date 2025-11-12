"""
Standalone Rate Limiter Test (No app imports)

Tests the RateLimiter class directly by importing only the module file.
"""

import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import directly from the rate_limiter file
import importlib.util
spec = importlib.util.spec_from_file_location(
    "rate_limiter",
    os.path.join(os.path.dirname(__file__), '..', 'app', 'api', 'middleware', 'rate_limiter.py')
)
rate_limiter_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rate_limiter_module)

RateLimiter = rate_limiter_module.RateLimiter


def test_allows_under_limit():
    """Test that requests under the limit are allowed"""
    print("\n[TEST 1] Testing requests under limit...")
    limiter = RateLimiter()

    success = 0
    for i in range(10):
        allowed, info = limiter.check_rate_limit(
            identifier="test_user_1",
            endpoint="/api/test",
            max_requests=10,
            window_seconds=60
        )

        if allowed and info["current"] == i + 1:
            success += 1

    assert success == 10, f"Expected 10 successful requests, got {success}"
    print(f"[PASS] All 10 requests under limit were allowed")
    return True


def test_blocks_over_limit():
    """Test that requests over the limit are blocked"""
    print("\n[TEST 2] Testing requests over limit...")
    limiter = RateLimiter()

    # Allow 5 requests
    for i in range(5):
        allowed, _ = limiter.check_rate_limit(
            identifier="test_user_2",
            endpoint="/api/test",
            max_requests=5,
            window_seconds=60
        )
        assert allowed, f"Request {i+1} should be allowed"

    # 6th request should be blocked
    allowed, info = limiter.check_rate_limit(
        identifier="test_user_2",
        endpoint="/api/test",
        max_requests=5,
        window_seconds=60
    )

    assert not allowed, "6th request should be blocked"
    assert info["remaining"] == 0
    print(f"[PASS] Request over limit was blocked")
    print(f"       - Retry after: {info['retry_after']} seconds")
    return True


def test_sliding_window():
    """Test that sliding window works correctly"""
    print("\n[TEST 3] Testing sliding window...")
    limiter = RateLimiter()

    # Make 3 requests with 3-second window
    for i in range(3):
        allowed, _ = limiter.check_rate_limit(
            identifier="test_user_3",
            endpoint="/api/test",
            max_requests=3,
            window_seconds=3
        )
        assert allowed

    # 4th request immediately - should be blocked
    allowed, _ = limiter.check_rate_limit(
        identifier="test_user_3",
        endpoint="/api/test",
        max_requests=3,
        window_seconds=3
    )
    assert not allowed, "4th request should be blocked"
    print("       [INFO] 4th request blocked (window not expired)")

    # Wait for window to pass
    print("       [INFO] Waiting 4 seconds for window to expire...")
    time.sleep(4)

    # Now should be allowed
    allowed, _ = limiter.check_rate_limit(
        identifier="test_user_3",
        endpoint="/api/test",
        max_requests=3,
        window_seconds=3
    )
    assert allowed, "Request should be allowed after window expires"
    print(f"[PASS] Sliding window works correctly")
    return True


def test_per_identifier():
    """Test that rate limits are per-identifier"""
    print("\n[TEST 4] Testing per-identifier isolation...")
    limiter = RateLimiter()

    # User 1 makes 5 requests
    for i in range(5):
        limiter.check_rate_limit(
            identifier="user_1",
            endpoint="/api/test",
            max_requests=5,
            window_seconds=60
        )

    # User 1's 6th request should be blocked
    allowed, _ = limiter.check_rate_limit(
        identifier="user_1",
        endpoint="/api/test",
        max_requests=5,
        window_seconds=60
    )
    assert not allowed, "User 1 should be blocked"

    # User 2 should still be allowed
    allowed, info = limiter.check_rate_limit(
        identifier="user_2",
        endpoint="/api/test",
        max_requests=5,
        window_seconds=60
    )
    assert allowed, "User 2 should not be blocked"
    assert info["current"] == 1

    print(f"[PASS] Rate limits are correctly isolated per identifier")
    return True


def test_per_endpoint():
    """Test that rate limits are per-endpoint"""
    print("\n[TEST 5] Testing per-endpoint isolation...")
    limiter = RateLimiter()

    # Make 3 requests to endpoint A
    for i in range(3):
        limiter.check_rate_limit(
            identifier="test_user",
            endpoint="/api/endpoint_a",
            max_requests=3,
            window_seconds=60
        )

    # 4th request to endpoint A should be blocked
    allowed, _ = limiter.check_rate_limit(
        identifier="test_user",
        endpoint="/api/endpoint_a",
        max_requests=3,
        window_seconds=60
    )
    assert not allowed, "Endpoint A should be blocked"

    # But endpoint B should still be allowed
    allowed, info = limiter.check_rate_limit(
        identifier="test_user",
        endpoint="/api/endpoint_b",
        max_requests=3,
        window_seconds=60
    )
    assert allowed, "Endpoint B should not be blocked"
    assert info["current"] == 1

    print(f"[PASS] Rate limits are correctly isolated per endpoint")
    return True


def main():
    """Run all tests"""
    print("="*70)
    print("RATE LIMITER STANDALONE UNIT TESTS")
    print("="*70)

    tests = [
        test_allows_under_limit,
        test_blocks_over_limit,
        test_sliding_window,
        test_per_identifier,
        test_per_endpoint
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"[FAIL] {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] {test_func.__name__}: {e}")
            failed += 1

    print("\n" + "="*70)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*70)

    if failed == 0:
        print("\n[SUCCESS] All rate limiter tests passed!")
        print("\nVerified functionality:")
        print("  [OK] Allows requests under limit")
        print("  [OK] Blocks requests over limit")
        print("  [OK] Sliding window algorithm works")
        print("  [OK] Per-identifier isolation")
        print("  [OK] Per-endpoint isolation")
        return 0
    else:
        print(f"\n[FAILURE] {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
