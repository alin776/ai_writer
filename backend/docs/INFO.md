(venv) PS D:\Java\ai_writer\backend> python run_tests.py
============================================================
🧪 AI去痕迹功能 - 自动化测试套件
============================================================

============================================================
🚀 单元测试 (Pytest)
============================================================
======================================================== test session starts ========================================================
platform win32 -- Python 3.12.4, pytest-7.4.4, pluggy-1.6.0 -- D:\Java\ai_writer\backend\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\Java\ai_writer\backend
configfile: pytest.ini
plugins: anyio-4.11.0, asyncio-0.23.3, cov-4.1.0
asyncio: mode=Mode.STRICT
collected 13 items

tests/test_humanize.py::test_user_profile_creation FAILED                                                                      [  7%]
tests/test_humanize.py::test_user_profile_update_stats FAILED                                                                  [ 15%]
tests/test_humanize.py::test_user_profile_display_mode FAILED                                                                  [ 23%]
tests/test_humanize.py::test_user_profile_settings_update FAILED                                                               [ 30%]
tests/test_humanize.py::test_humanize_session_creation FAILED                                                                  [ 38%]
tests/test_humanize.py::test_humanize_session_with_detail FAILED                                                               [ 46%]
tests/test_humanize.py::test_session_service_save FAILED                                                                       [ 53%]
tests/test_humanize.py::test_session_service_token_estimation PASSED                                                           [ 61%]
tests/test_humanize.py::test_detection_prompt PASSED                                                                           [ 69%]
tests/test_humanize.py::test_humanize_prompts PASSED                                                                           [ 76%]
tests/test_humanize.py::test_verification_prompt PASSED                                                                        [ 84%]
tests/test_humanize.py::test_ai_detection_result_schema PASSED                                                                 [ 92%]
tests/test_humanize.py::test_user_profile_response_schema PASSED                                                               [100%]

============================================================= FAILURES ==============================================================
____________________________________________________ test_user_profile_creation _____________________________________________________
tests\test_humanize.py:62: in test_user_profile_creation
    profile = await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
__________________________________________________ test_user_profile_update_stats ___________________________________________________
tests\test_humanize.py:79: in test_user_profile_update_stats
    profile = await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
__________________________________________________ test_user_profile_display_mode ___________________________________________________
tests\test_humanize.py:103: in test_user_profile_display_mode
    profile = await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
_________________________________________________ test_user_profile_settings_update _________________________________________________
tests\test_humanize.py:128: in test_user_profile_settings_update
    await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
__________________________________________________ test_humanize_session_creation ___________________________________________________
tests\test_humanize.py:166: in test_humanize_session_creation
    db_session.add(session)
E   AttributeError: 'async_generator' object has no attribute 'add'
_________________________________________________ test_humanize_session_with_detail _________________________________________________
tests\test_humanize.py:192: in test_humanize_session_with_detail
    db_session.add(session)
E   AttributeError: 'async_generator' object has no attribute 'add'
_____________________________________________________ test_session_service_save _____________________________________________________
tests\test_humanize.py:243: in test_session_service_save
    session = await service.save_session(
app\services\humanize_session_service.py:83: in save_session
    self.db.add(session)
E   AttributeError: 'async_generator' object has no attribute 'add'
========================================================= warnings summary ==========================================================
tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\core\config.py:40: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    @validator("CORS_ORIGINS", pre=True)

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\core\config.py:6: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\user.py:80: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserResponse(UserBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\user.py:124: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserSessionResponse(BaseModel):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\work.py:30: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class WorkResponse(WorkBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\chapter.py:39: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class ChapterResponse(ChapterBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:21: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    dimensions: Dict[str, DimensionScore] = Field(

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:83: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class HumanizeSessionResponse(HumanizeSessionBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:97: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class HumanizeSessionDetailResponse(BaseModel):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:152: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserProfileResponse(UserProfileBase):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
====================================================== short test summary info ======================================================
FAILED tests/test_humanize.py::test_user_profile_creation - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_update_stats - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_display_mode - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_settings_update - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_humanize_session_creation - AttributeError: 'async_generator' object has no attribute 'add'
FAILED tests/test_humanize.py::test_humanize_session_with_detail - AttributeError: 'async_generator' object has no attribute 'add'
FAILED tests/test_humanize.py::test_session_service_save - AttributeError: 'async_generator' object has no attribute 'add'
============================================= 7 failed, 6 passed, 10 warnings in 2.56s ==============================================

❌ 单元测试 (Pytest) 失败

============================================================
⚠️  注意: 自动化测试需要后端服务运行
   启动命令: python -m uvicorn app.main:app --reload
============================================================

是否运行自动化API测试? (y/n): y

💡 测试脚本将自动登录获取token
   默认账号: 2072855200@qq.com
   可通过环境变量 TEST_USERNAME 和 TEST_PASSWORD 自定义

============================================================
🚀 自动化API测试
============================================================
============================================================
🚀 AI去痕迹功能 - 自动化测试开始
============================================================
测试服务器: http://localhost:8000
测试时间: 2025-10-26 10:50:09
============================================================

🔐 未提供token,尝试自动登录...
⚠️  自动登录失败 (状态码: 503)
   提示: 请检查账号密码是否正确

📡 API 接口测试:
❌ FAIL - API健康检查
   状态码: 503
⚠️  跳过需要认证的API测试 (未登录)

⚙️  服务层测试:
✅ PASS - UserProfileService - 创建画像
   画像ID: ea575cf5-aa86-4593-abb9-41e5bc78f201
✅ PASS - UserProfileService - 更新统计
   使用次数: 1
✅ PASS - 数据库模型 - UserProfile
   Profile ID: 11c59369-4dd9-4cee-babd-f7992c2b6e0a
✅ PASS - 数据库模型 - HumanizeSession
   Session ID: ed65e5d9-5ff3-47f5-83b9-ce364f5da567
D:\Java\ai_writer\backend\tests\test_humanize_auto.py:454: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  expires_at=datetime.utcnow() + timedelta(days=30)
✅ PASS - 数据库模型 - HumanizeSessionDetail
   Detail ID: 571860b1-a0c1-403a-ab9b-235f052adeee

============================================================
📊 测试总结:
   总计: 6 个测试
   通过: 5 个 ✅
   失败: 1 个 ❌
   通过率: 83.3%
============================================================

❌ 失败的测试:
   - API健康检查: 状态码: 503

📄 详细测试报告已保存到: test_report.json

✅ 自动化API测试 成功

============================================================
📊 测试报告
============================================================
❌ 部分测试失败,请查看上面的错误信息
(venv) PS D:\Java\ai_writer\backend> python run_tests.py
============================================================
🧪 AI去痕迹功能 - 自动化测试套件
============================================================

============================================================
🚀 单元测试 (Pytest)
============================================================
======================================================== test session starts ========================================================
platform win32 -- Python 3.12.4, pytest-7.4.4, pluggy-1.6.0 -- D:\Java\ai_writer\backend\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\Java\ai_writer\backend
configfile: pytest.ini
plugins: anyio-4.11.0, asyncio-0.23.3, cov-4.1.0
asyncio: mode=Mode.STRICT
collected 13 items

tests/test_humanize.py::test_user_profile_creation FAILED                                                                      [  7%]
tests/test_humanize.py::test_user_profile_update_stats FAILED                                                                  [ 15%]
tests/test_humanize.py::test_user_profile_display_mode FAILED                                                                  [ 23%]
tests/test_humanize.py::test_user_profile_settings_update FAILED                                                               [ 30%]
tests/test_humanize.py::test_humanize_session_creation FAILED                                                                  [ 38%]
tests/test_humanize.py::test_humanize_session_with_detail FAILED                                                               [ 46%]
tests/test_humanize.py::test_session_service_save FAILED                                                                       [ 53%]
tests/test_humanize.py::test_session_service_token_estimation PASSED                                                           [ 61%]
tests/test_humanize.py::test_detection_prompt PASSED                                                                           [ 69%]
tests/test_humanize.py::test_humanize_prompts PASSED                                                                           [ 76%]
tests/test_humanize.py::test_verification_prompt PASSED                                                                        [ 84%]
tests/test_humanize.py::test_ai_detection_result_schema PASSED                                                                 [ 92%]
tests/test_humanize.py::test_user_profile_response_schema PASSED                                                               [100%]

============================================================= FAILURES ==============================================================
____________________________________________________ test_user_profile_creation _____________________________________________________
tests\test_humanize.py:27: in test_user_profile_creation
    profile = await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
__________________________________________________ test_user_profile_update_stats ___________________________________________________
tests\test_humanize.py:44: in test_user_profile_update_stats
    profile = await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
__________________________________________________ test_user_profile_display_mode ___________________________________________________
tests\test_humanize.py:68: in test_user_profile_display_mode
    profile = await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
_________________________________________________ test_user_profile_settings_update _________________________________________________
tests\test_humanize.py:93: in test_user_profile_settings_update
    await service.get_or_create_profile(test_user_id)
app\services\user_profile_service.py:37: in get_or_create_profile
    result = await self.db.execute(
E   AttributeError: 'async_generator' object has no attribute 'execute'
__________________________________________________ test_humanize_session_creation ___________________________________________________
tests\test_humanize.py:131: in test_humanize_session_creation
    db_session.add(session)
E   AttributeError: 'async_generator' object has no attribute 'add'
_________________________________________________ test_humanize_session_with_detail _________________________________________________
tests\test_humanize.py:157: in test_humanize_session_with_detail
    db_session.add(session)
E   AttributeError: 'async_generator' object has no attribute 'add'
_____________________________________________________ test_session_service_save _____________________________________________________
tests\test_humanize.py:208: in test_session_service_save
    session = await service.save_session(
app\services\humanize_session_service.py:83: in save_session
    self.db.add(session)
E   AttributeError: 'async_generator' object has no attribute 'add'
========================================================= warnings summary ==========================================================
tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\core\config.py:40: PydanticDeprecatedSince20: Pydantic V1 style `@validator` validators are deprecated. You should migrate to Pydantic V2 style `@field_validator` validators, see the migration guide for more details. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    @validator("CORS_ORIGINS", pre=True)

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\core\config.py:6: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class Settings(BaseSettings):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\user.py:80: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserResponse(UserBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\user.py:124: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserSessionResponse(BaseModel):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\work.py:30: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class WorkResponse(WorkBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\chapter.py:39: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class ChapterResponse(ChapterBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:21: PydanticDeprecatedSince20: Using extra keyword arguments on `Field` is deprecated and will be removed. Use `json_schema_extra` instead. (Extra keys: 'example'). Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    dimensions: Dict[str, DimensionScore] = Field(

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:83: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class HumanizeSessionResponse(HumanizeSessionBase):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:97: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class HumanizeSessionDetailResponse(BaseModel):

tests/test_humanize.py::test_user_profile_creation
  D:\Java\ai_writer\backend\app\schemas\humanize.py:152: PydanticDeprecatedSince20: Support for class-based `config` is deprecated, use ConfigDict instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/
    class UserProfileResponse(UserProfileBase):

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
====================================================== short test summary info ======================================================
FAILED tests/test_humanize.py::test_user_profile_creation - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_update_stats - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_display_mode - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_settings_update - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_humanize_session_creation - AttributeError: 'async_generator' object has no attribute 'add'
FAILED tests/test_humanize.py::test_humanize_session_with_detail - AttributeError: 'async_generator' object has no attribute 'add'
FAILED tests/test_humanize.py::test_session_service_save - AttributeError: 'async_generator' object has no attribute 'add'
============================================= 7 failed, 6 passed, 10 warnings in 1.98s ==============================================

❌ 单元测试 (Pytest) 失败

============================================================
⚠️  注意: 自动化测试需要后端服务运行
   启动命令: python -m uvicorn app.main:app --reload
============================================================

是否运行自动化API测试? (y/n): y

💡 测试脚本将自动登录获取token
   默认账号: 2072855200@qq.com
   可通过环境变量 TEST_USERNAME 和 TEST_PASSWORD 自定义

============================================================
🚀 自动化API测试
============================================================
============================================================
🚀 AI去痕迹功能 - 自动化测试开始
============================================================
测试服务器: http://localhost:8000
测试时间: 2025-10-26 10:54:47
============================================================

🔐 未提供token,尝试自动登录...
✅ 自动登录成功 (用户: 2072855200@qq.com)

📡 API 接口测试:
✅ PASS - API健康检查
   状态码: 200
✅ PASS - 获取用户画像
   total_uses: 0, display_mode: detailed
✅ PASS - 更新用户画像设置
   设置更新成功
✅ PASS - 获取历史记录
   总记录: 0, 当前页: 0条
✅ PASS - 获取统计数据
   总使用: 0, 平均改进: 0.0分

⚙️  服务层测试:
✅ PASS - UserProfileService - 创建画像
   画像ID: 1547b20d-cd70-4f68-8f77-24a06ece29f4
✅ PASS - UserProfileService - 更新统计
   使用次数: 1
✅ PASS - 数据库模型 - UserProfile
   Profile ID: c5ea9150-38dc-47a8-9e1f-8eb49bc42bf9
✅ PASS - 数据库模型 - HumanizeSession
   Session ID: a724204a-c781-4caa-b3e1-d916b20483fb
D:\Java\ai_writer\backend\tests\test_humanize_auto.py:454: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  expires_at=datetime.utcnow() + timedelta(days=30)
✅ PASS - 数据库模型 - HumanizeSessionDetail
   Detail ID: fcf6e0d1-70c2-48d1-9d66-4785971a8809

============================================================
📊 测试总结:
   总计: 10 个测试
   通过: 10 个 ✅
   失败: 0 个 ❌
   通过率: 100.0%
============================================================

📄 详细测试报告已保存到: test_report.json

✅ 自动化API测试 成功

============================================================
📊 测试报告
============================================================
❌ 部分测试失败,请查看上面的错误信息
(venv) PS D:\Java\ai_writer\backend>