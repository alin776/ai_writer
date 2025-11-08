================================================================================
 ChatGPT Fix Automated Test Suite
================================================================================
Base URL: http://localhost:8000
Test Account: 2072855200@qq.com
Test Time: 2025-11-08 12:23:32

================================================================================
 Test 1: OAuth2 Form Data Login
================================================================================
[RUN] Logging in with OAuth2 Form Data...
    Attempting login to: http://localhost:8000/api/v1/auth/login
    Username: 2072855200@qq.com
    Response status: 200
[OK] Login successful! Token: eyJhbGciOiJIUzI1NiIs...
[OK] OAuth2 Login (0.48s)

================================================================================
 Test 2: chat() Non-Streaming Mode
================================================================================
[RUN] Sending message: Hello, how are you today?
[OK] chat() mode (74.37s)
    Details: Response length: 55 chars
    Response preview: ????????????????????

?????????????????????????????????...

================================================================================
 Test 3: chat_stream() Streaming Mode
================================================================================
[RUN] Sending message: Help me write a story opening about a detective
[OK] chat_stream() mode (22.43s)
    Details: Received 21 chunks

================================================================================
 Test 4: Planning Mode (3-Phase Streaming)
================================================================================
[RUN] Sending message: Help me plan a fantasy novel outline with 5 chapters
[OK] Planning mode (47.83s)
    Details: Detected 0 phase transitions

================================================================================
 Test 5: ChatGPT Parameter Passing Verification
================================================================================
[RUN] Testing temperature parameter variations...
[OK] Parameter passing (0.00s)
    Details: Both temperature variations responded correctly

================================================================================
 Test Summary
================================================================================
Total Tests:  5
Passed:       5 [OK]
Failed:       0 [FAIL]
Pass Rate:    100.0%
Duration:     173.01s

[OK] All tests passed!
(venv) PS D:\Java\ai_writer\backend>