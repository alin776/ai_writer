# Pytest 测试修复计划

## 📋 问题总结

### 核心错误
- **错误类型:** `AttributeError: 'async_generator' object has no attribute 'execute'`
- **影响范围:** 7个测试失败 (涉及数据库操作的测试)
- **根本原因:** `conftest.py` 中的 `db_session` fixture 实现正确,但测试代码中可能混用了不同的 session 获取方式

### 错误详情
```
FAILED tests/test_humanize.py::test_user_profile_creation - AttributeError: 'async_generator' object has no attribute 'execute'
FAILED tests/test_humanize.py::test_user_profile_update_stats - 同上
FAILED tests/test_humanize.py::test_user_profile_display_mode - 同上
FAILED tests/test_humanize.py::test_user_profile_settings_update - 同上
FAILED tests/test_humanize.py::test_humanize_session_creation - AttributeError: 'async_generator' object has no attribute 'add'
FAILED tests/test_humanize.py::test_humanize_session_with_detail - 同上
FAILED tests/test_session_service_save - 同上
```

### 对比分析
- ✅ **自动化API测试:** 100% 通过 (使用真实数据库连接)
- ❌ **Pytest单元测试:** 7/13 失败 (使用 fixture)

---

## 🎯 修复方案

### 方案1: 修复 conftest.py (推荐)

**问题:** 当前 `conftest.py` 的 `db_session` fixture 实现是正确的,但可能存在作用域问题

**修复步骤:**
1. 检查 `db_session` fixture 的作用域
2. 确保 `test_user_id` fixture 正确依赖 `db_session`
3. 添加必要的 pytest 配置

**修复内容:**
```python
# conftest.py

@pytest.fixture(scope="function")  # 明确指定作用域
async def db_session():
    """数据库会话 - 自动事务回滚"""
    from app.core.database import async_session_maker

    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()  # 添加显式关闭


@pytest.fixture(scope="function")
async def test_user_id(db_session):
    """测试用户ID - 创建真实用户"""
    from app.models.user import User
    from uuid import uuid4

    user_id = uuid4()
    test_user = User(
        id=user_id,
        username=f"test_user_{user_id.hex[:8]}",
        email=f"test_{user_id.hex[:8]}@example.com",
        hashed_password="dummy_hash_for_test",
        is_active=True
    )

    db_session.add(test_user)
    await db_session.flush()

    yield user_id
```

### 方案2: 修复测试代码中的 session 使用

**问题:** 测试中可能直接调用了 `get_db()` 而不是使用 fixture

**检查点:**
1. 所有测试是否正确使用 `db_session` 参数
2. Service 类是否正确接收 session 对象
3. 是否有测试代码直接调用了 `get_db()`

### 方案3: 添加 pytest 配置

**问题:** pytest-asyncio 配置可能不完整

**修复内容:**
```ini
# pytest.ini
[pytest]
asyncio_mode = auto  # 自动检测异步测试
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

## 📝 待办任务

### ✅ 任务1: 分析当前 conftest.py
- [x] 读取 conftest.py
- [x] 确认 fixture 实现正确
- [x] 发现问题: fixture 缺少显式关闭 session

### 🔧 任务2: 修复 conftest.py
- [ ] 添加 `scope="function"` 明确作用域
- [ ] 在 finally 中添加 `await session.close()`
- [ ] 确保 `test_user_id` fixture 正确依赖

### 🔧 任务3: 检查测试代码
- [ ] 读取 test_humanize.py
- [ ] 确认所有测试正确使用 `db_session` fixture
- [ ] 检查是否有直接调用 `get_db()` 的情况

### 🔧 任务4: 优化 pytest.ini
- [ ] 确认 asyncio_mode 配置
- [ ] 添加其他必要的 pytest 配置

### ✅ 任务5: 运行测试验证
- [ ] 运行 `pytest tests/test_humanize.py -v`
- [ ] 确认所有测试通过
- [ ] 检查是否有新的警告或错误

---

## 🔍 其他发现的问题

### 1. Pydantic 弃用警告 (低优先级)
```
PydanticDeprecatedSince20: Support for class-based `config` is deprecated
```
- **影响:** 仅产生警告,不影响功能
- **建议:** 后续迁移到 Pydantic V2 `ConfigDict`
- **优先级:** P3 (低)

### 2. datetime.utcnow() 弃用警告 (低优先级)
```python
# tests/test_humanize.py:168
expires_at=datetime.utcnow() + timedelta(days=30)  # 已弃用

# 应该改为:
expires_at=datetime.now(datetime.UTC) + timedelta(days=30)
```
- **影响:** 仅产生警告
- **优先级:** P3 (低)

### 3. API健康检查失败 (已解决)
- **问题:** 第一次测试时返回 503 (服务未启动)
- **状态:** 第二次测试时已解决 (启动后端服务)
- **无需修复**

### 4. 正则表达式转义警告 (中优先级)
```python
# app/services/worldview_extraction_service.py:306
conflict_match = re.search(f'{stage}[^：:]*[:：]\s*([^\n]{{20,200}})', conflict_section)
# 应该使用 r'' 原始字符串

# app/services/worldview_extraction_service.py:574
text = re.sub(r'[，。！？、；：""''《》（）【】\.,!?;:\'"()\[\]]+', '', text)
```
- **影响:** 产生 SyntaxWarning
- **优先级:** P2 (中)

---

## 📊 修复优先级

| 优先级 | 问题 | 影响 | 工作量 |
|--------|------|------|--------|
| P0 | Pytest 测试失败 (async_generator 错误) | 高 | 0.5小时 |
| P1 | 无 | - | - |
| P2 | 正则表达式转义警告 | 中 | 0.2小时 |
| P3 | Pydantic V2 迁移 | 低 | 1小时 |
| P3 | datetime.utcnow() 弃用 | 低 | 0.1小时 |

---

## ✅ 修复步骤

1. **立即修复 conftest.py** (解决 P0 问题)
2. **运行测试验证**
3. **修复正则表达式警告** (解决 P2 问题)
4. **后续考虑 Pydantic V2 迁移** (P3 问题)

---

**创建时间:** 2025-10-26
**状态:** 🔧 待修复
