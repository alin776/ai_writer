PS D:\Java\ai_writer\backend> .\venv\Scripts\python.exe -m pytest tests/test_conversation_id.py -v -s
============================================== test session starts ==============================================
platform win32 -- Python 3.12.4, pytest-7.4.4, pluggy-1.6.0 -- D:\Java\ai_writer\backend\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\Java\ai_writer\backend
configfile: pytest.ini
plugins: anyio-4.11.0, langsmith-0.4.38, asyncio-0.23.3, cov-4.1.0
asyncio: mode=Mode.STRICT
collected 4 items

tests/test_conversation_id.py::TestConversationId::test_scenario_a_no_conversation_id
============================================================
[LOGIN] Getting access token...
============================================================
[LOGIN] Status: 200
[LOGIN] SUCCESS - Token obtained

============================================================
[TEST A] Call stream API without conversation_id
============================================================
[TEST A] Response Status: 200
[TEST A] X-Conversation-Id (Header): c30d1ef1-493f-4e2b-8764-37b2f0c971bb
[TEST A] conversation_id (Event): c30d1ef1-493f-4e2b-8764-37b2f0c971bb
[TEST A] Content preview: 抱歉，我未能生成小说标题。请您提供更多关于小说主题、类型或任何关键元素的信息，以便我能更好地帮助您。
[PASS] Header contains X-Conversation-Id
[PASS] X-Conversation-Id is valid UUID format
[PASS] Header and Event conversation_id match

[TEST A] PASSED - Stored conversation_id: c30d1ef1-493f-4e2b-8764-37b2f0c971bb
PASSED
tests/test_conversation_id.py::TestConversationId::test_scenario_b_reuse_conversation_id
============================================================
[TEST B] Reuse session with existing conversation_id
============================================================
[TEST B] Using conversation_id: c30d1ef1-493f-4e2b-8764-37b2f0c971bb
[TEST B] Response Status: 200
[TEST B] X-Conversation-Id (Header): c30d1ef1-493f-4e2b-8764-37b2f0c971bb
[TEST B] conversation_id (Event): c30d1ef1-493f-4e2b-8764-37b2f0c971bb
[PASS] Header conversation_id matches provided value
[PASS] Event conversation_id matches provided value

[TEST B] PASSED - conversation_id correctly reused
PASSED
tests/test_conversation_id.py::TestConversationId::test_scenario_c_missing_work_id
============================================================
[TEST C] Test fallback logic without work_id
============================================================
[TEST C] Response Status: 200
[TEST C] X-Conversation-Id (Header): 34289375-c34b-4ba6-a980-86fce1a60f47
[PASS] Fallback logic works - conversation_id returned without work_id

[TEST C] PASSED - Fallback logic working correctly
PASSED
tests/test_conversation_id.py::TestLoginOnly::test_login_with_form_data
============================================================
[LOGIN TEST] Testing OAuth2 form data login
============================================================
[LOGIN TEST] Status: 200
[LOGIN TEST] PASSED - OAuth2 form data login works
PASSED

========================================= 4 passed in 64.09s (0:01:04) ==========================================
PS D:\Java\ai_writer\backend>