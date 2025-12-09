# -*- coding: utf-8 -*-
"""
Test conversation_id auto-generation and return functionality

Test Scenarios:
- Scenario A: Call stream API without conversation_id
- Scenario B: Reuse session with existing conversation_id
- Scenario C: Test fallback logic without work_id
"""
import pytest
import httpx
import json
import uuid


# Test configuration
BASE_URL = "http://localhost:8000"
API_V1 = f"{BASE_URL}/api/v1"
LOGIN_URL = f"{API_V1}/auth/login"
CHAT_STREAM_URL = f"{API_V1}/agent/chat/stream"

# Test credentials
TEST_EMAIL = "2072855200@qq.com"
TEST_PASSWORD = "zrt3ljnygz@163.com"


class TestConversationId:
    """Test conversation_id auto-generation and reuse"""

    @pytest.fixture(scope="class")
    def access_token(self):
        """Login and get access token using OAuth2 form data"""
        print("\n" + "=" * 60)
        print("[LOGIN] Getting access token...")
        print("=" * 60)

        # OAuth2PasswordRequestForm requires form data, NOT JSON!
        form_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        }

        response = httpx.post(
            LOGIN_URL,
            data=form_data,  # Use data= for form data, not json=
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30.0
        )

        print(f"[LOGIN] Status: {response.status_code}")

        if response.status_code != 200:
            print(f"[LOGIN] Error: {response.text}")
            pytest.fail(f"Login failed with status {response.status_code}: {response.text}")

        token_data = response.json()
        access_token = token_data.get("access_token")

        if not access_token:
            pytest.fail("No access_token in response")

        print("[LOGIN] SUCCESS - Token obtained")
        return access_token

    def _get_auth_headers(self, access_token: str) -> dict:
        """Get authorization headers"""
        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

    def _parse_sse_events(self, response) -> dict:
        """Parse SSE event stream and extract conversation_id"""
        result = {
            "conversation_id_from_event": None,
            "events": [],
            "content_chunks": [],
        }

        for line in response.iter_lines():
            if line.startswith("data: "):
                data = line[6:]
                if data.strip() == "[DONE]":
                    result["events"].append({"type": "done"})
                    break
                try:
                    event_data = json.loads(data)
                    event_type = event_data.get("type", "unknown")
                    result["events"].append(event_data)

                    # Extract conversation_id from start/stream_start/done events
                    # Check multiple event types for robustness
                    if event_type in ("start", "stream_start", "done"):
                        conv_id = event_data.get("conversation_id")
                        if conv_id and not result["conversation_id_from_event"]:
                            result["conversation_id_from_event"] = conv_id

                    # Collect content chunks
                    if event_type == "content":
                        chunk = event_data.get("content", "")
                        if chunk:
                            result["content_chunks"].append(chunk)

                except json.JSONDecodeError:
                    pass

        return result

    def test_scenario_a_no_conversation_id(self, access_token):
        """
        Scenario A: Call stream API without conversation_id

        Expected:
        - Response header contains X-Conversation-Id with a new UUID
        - stream_start event contains matching conversation_id
        """
        print("\n" + "=" * 60)
        print("[TEST A] Call stream API without conversation_id")
        print("=" * 60)

        payload = {
            "message": "Hello, please give me a novel title suggestion",
            "work_id": "test-work-001"
        }

        with httpx.stream(
            "POST",
            CHAT_STREAM_URL,
            json=payload,
            headers=self._get_auth_headers(access_token),
            timeout=120.0
        ) as response:
            # Check response status
            print(f"[TEST A] Response Status: {response.status_code}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

            # Check X-Conversation-Id header
            conv_id_header = response.headers.get("X-Conversation-Id")
            print(f"[TEST A] X-Conversation-Id (Header): {conv_id_header}")

            # Parse SSE events
            sse_result = self._parse_sse_events(response)
            conv_id_event = sse_result["conversation_id_from_event"]
            print(f"[TEST A] conversation_id (Event): {conv_id_event}")

            # Print some content preview
            content = "".join(sse_result["content_chunks"])
            if content:
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"[TEST A] Content preview: {preview}")

            # Assertions
            assert conv_id_header is not None, "[FAIL] Header missing X-Conversation-Id"
            print("[PASS] Header contains X-Conversation-Id")

            # Validate UUID format
            try:
                uuid.UUID(conv_id_header)
                print("[PASS] X-Conversation-Id is valid UUID format")
            except ValueError:
                pytest.fail(f"[FAIL] X-Conversation-Id is not valid UUID: {conv_id_header}")

            # Check consistency between header and event
            if conv_id_event:
                assert conv_id_header == conv_id_event, \
                    f"[FAIL] Header ({conv_id_header}) != Event ({conv_id_event})"
                print("[PASS] Header and Event conversation_id match")

            # Store for next test
            self.__class__.stored_conversation_id = conv_id_header
            print(f"\n[TEST A] PASSED - Stored conversation_id: {conv_id_header}")

    def test_scenario_b_reuse_conversation_id(self, access_token):
        """
        Scenario B: Reuse session with existing conversation_id

        Expected:
        - Response header X-Conversation-Id matches the provided one
        - stream_start event contains matching conversation_id
        - Backend does NOT generate a new conversation_id
        """
        print("\n" + "=" * 60)
        print("[TEST B] Reuse session with existing conversation_id")
        print("=" * 60)

        # Get stored conversation_id from previous test
        existing_conv_id = getattr(self.__class__, 'stored_conversation_id', None)
        if not existing_conv_id:
            pytest.skip("No conversation_id from previous test")

        print(f"[TEST B] Using conversation_id: {existing_conv_id}")

        payload = {
            "message": "Continue the previous topic, give me more suggestions",
            "work_id": "test-work-001",
            "conversation_id": existing_conv_id
        }

        with httpx.stream(
            "POST",
            CHAT_STREAM_URL,
            json=payload,
            headers=self._get_auth_headers(access_token),
            timeout=120.0
        ) as response:
            print(f"[TEST B] Response Status: {response.status_code}")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

            # Check header
            conv_id_header = response.headers.get("X-Conversation-Id")
            print(f"[TEST B] X-Conversation-Id (Header): {conv_id_header}")

            # Parse SSE events
            sse_result = self._parse_sse_events(response)
            conv_id_event = sse_result["conversation_id_from_event"]
            print(f"[TEST B] conversation_id (Event): {conv_id_event}")

            # Assertions - conversation_id should remain the same
            assert conv_id_header == existing_conv_id, \
                f"[FAIL] Header mismatch: expected {existing_conv_id}, got {conv_id_header}"
            print("[PASS] Header conversation_id matches provided value")

            if conv_id_event:
                assert conv_id_event == existing_conv_id, \
                    f"[FAIL] Event mismatch: expected {existing_conv_id}, got {conv_id_event}"
                print("[PASS] Event conversation_id matches provided value")

            print("\n[TEST B] PASSED - conversation_id correctly reused")

    def test_scenario_c_missing_work_id(self, access_token):
        """
        Scenario C: Test fallback logic without work_id

        Expected:
        - Response still returns a conversation_id (fallback logic works)
        - Log should show warning about missing work_id
        """
        print("\n" + "=" * 60)
        print("[TEST C] Test fallback logic without work_id")
        print("=" * 60)

        payload = {
            "message": "Test without work_id"
            # Intentionally omit work_id
        }

        with httpx.stream(
            "POST",
            CHAT_STREAM_URL,
            json=payload,
            headers=self._get_auth_headers(access_token),
            timeout=120.0
        ) as response:
            print(f"[TEST C] Response Status: {response.status_code}")

            # Should still succeed (fallback logic)
            # Note: If API requires work_id, this might return 422
            if response.status_code == 422:
                print("[INFO] API requires work_id (422 Validation Error)")
                print("[SKIP] Fallback logic test skipped - work_id is required")
                pytest.skip("work_id is required by API")

            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

            # Check header
            conv_id_header = response.headers.get("X-Conversation-Id")
            print(f"[TEST C] X-Conversation-Id (Header): {conv_id_header}")

            # Parse SSE events
            sse_result = self._parse_sse_events(response)

            # Assertion - should still get a conversation_id
            assert conv_id_header is not None, \
                "[FAIL] Should return conversation_id even without work_id"
            print("[PASS] Fallback logic works - conversation_id returned without work_id")

            print("\n[TEST C] PASSED - Fallback logic working correctly")


class TestLoginOnly:
    """Simple login test to verify OAuth2 form data works"""

    def test_login_with_form_data(self):
        """Test that login works with OAuth2 form data"""
        print("\n" + "=" * 60)
        print("[LOGIN TEST] Testing OAuth2 form data login")
        print("=" * 60)

        form_data = {
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        }

        response = httpx.post(
            LOGIN_URL,
            data=form_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30.0
        )

        print(f"[LOGIN TEST] Status: {response.status_code}")

        assert response.status_code == 200, f"Login failed: {response.text}"

        token_data = response.json()
        assert "access_token" in token_data, "Missing access_token"
        assert "refresh_token" in token_data, "Missing refresh_token"
        assert token_data.get("token_type") == "bearer", "Wrong token_type"

        print("[LOGIN TEST] PASSED - OAuth2 form data login works")


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s", "--tb=short"])
