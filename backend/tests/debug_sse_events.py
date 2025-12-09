# -*- coding: utf-8 -*-
"""
Debug script to inspect actual SSE events
"""
import httpx
import json

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
CHAT_STREAM_URL = f"{BASE_URL}/api/v1/agent/chat/stream"

TEST_EMAIL = "2072855200@qq.com"
TEST_PASSWORD = "zrt3ljnygz@163.com"


def main():
    print("=" * 60)
    print("[DEBUG] Inspecting SSE Events")
    print("=" * 60)

    # Login
    form_data = {"username": TEST_EMAIL, "password": TEST_PASSWORD}
    resp = httpx.post(LOGIN_URL, data=form_data, timeout=30.0)
    token = resp.json().get("access_token")
    print(f"[LOGIN] Token obtained: {token[:20]}...")

    # Chat stream
    payload = {"message": "hi", "work_id": "test-001"}
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    print("\n[STREAM] Starting SSE stream...")
    print("-" * 60)

    with httpx.stream("POST", CHAT_STREAM_URL, json=payload, headers=headers, timeout=120.0) as response:
        print(f"[HEADER] Status: {response.status_code}")
        print(f"[HEADER] X-Conversation-Id: {response.headers.get('X-Conversation-Id')}")
        print("-" * 60)

        event_count = 0
        for line in response.iter_lines():
            if not line:
                continue

            print(f"[RAW] {line[:150]}")

            if line.startswith("data: "):
                data = line[6:]
                if data.strip() == "[DONE]":
                    print("[EVENT] [DONE]")
                    break

                try:
                    event_data = json.loads(data)
                    event_type = event_data.get("type", "unknown")
                    conv_id = event_data.get("conversation_id")

                    print(f"[EVENT #{event_count}] type={event_type}, conversation_id={conv_id}")

                    # Show first 3 events in detail
                    if event_count < 3:
                        print(f"  [DETAIL] {json.dumps(event_data, ensure_ascii=False)[:200]}")

                    event_count += 1

                    # Stop after 10 events to avoid too much output
                    if event_count >= 10:
                        print("... (truncated)")
                        break

                except json.JSONDecodeError as e:
                    print(f"[PARSE ERROR] {e}")

    print("-" * 60)
    print(f"[SUMMARY] Total events inspected: {event_count}")


if __name__ == "__main__":
    main()
