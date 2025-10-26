# AI去痕迹功能 - 测试指南

## 📋 测试概述

本项目包含三种测试方式:

1. **单元测试** - 使用 Pytest,测试各个服务和模型
2. **自动化测试** - 完整的API和集成测试
3. **手动测试** - 使用Swagger UI或curl

---

## 🚀 快速开始

### 方式1: 一键运行所有测试

```bash
cd backend
python run_tests.py
```

### 方式2: 单独运行单元测试

```bash
# 运行所有测试
pytest tests/test_humanize.py -v

# 运行单个测试
pytest tests/test_humanize.py::test_user_profile_creation -v

# 显示打印输出
pytest tests/test_humanize.py -v -s

# 生成覆盖率报告
pytest tests/test_humanize.py --cov=app.services --cov-report=html
```

### 方式3: 运行自动化测试

```bash
# 不带认证 (只测试公开接口)
python tests/test_humanize_auto.py

# 带认证token
python tests/test_humanize_auto.py --token "your_jwt_token_here"

# 指定服务地址
python tests/test_humanize_auto.py --url http://localhost:8000
```

---

## 📝 测试清单

### 单元测试 (test_humanize.py)

#### UserProfile 测试
- [x] test_user_profile_creation - 用户画像创建
- [x] test_user_profile_update_stats - 统计更新
- [x] test_user_profile_display_mode - 显示模式切换
- [x] test_user_profile_settings_update - 设置更新

#### HumanizeSession 测试
- [x] test_humanize_session_creation - 会话创建
- [x] test_humanize_session_with_detail - 会话与详情关联

#### 服务层测试
- [x] test_session_service_save - 会话保存
- [x] test_session_service_token_estimation - Token估算

#### Prompt 测试
- [x] test_detection_prompt - 检测Prompt生成
- [x] test_humanize_prompts - 三种强度Prompt
- [x] test_verification_prompt - 验证Prompt生成

#### Schema 测试
- [x] test_ai_detection_result_schema - 检测结果Schema
- [x] test_user_profile_response_schema - 用户画像Schema

### 自动化测试 (test_humanize_auto.py)

#### API 测试
- [x] test_api_health - API健康检查
- [x] test_get_profile - 获取用户画像
- [x] test_update_profile_settings - 更新设置
- [x] test_get_history - 获取历史记录
- [x] test_get_stats - 获取统计数据

#### 服务测试
- [x] test_humanize_service - HumanizeService核心功能
- [x] test_user_profile_service - UserProfileService
- [x] test_database_models - 数据库模型

---

## 🔧 测试前准备

### 1. 安装测试依赖

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### 2. 启动后端服务 (自动化测试需要)

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 3. 获取测试Token (可选)

```bash
# 方式1: 使用Swagger UI登录
open http://localhost:8000/docs

# 方式2: 使用curl登录
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'
```

---

## 📊 测试报告

### 单元测试报告

```bash
# 生成HTML覆盖率报告
pytest tests/test_humanize.py --cov=app --cov-report=html

# 查看报告
open htmlcov/index.html
```

### 自动化测试报告

运行后会自动生成 `test_report.json`:

```json
{
  "summary": {
    "total": 8,
    "passed": 7,
    "failed": 1,
    "pass_rate": "87.5%",
    "time": "2025-10-26T10:30:00"
  },
  "results": [...]
}
```

---

## 🐛 常见问题

### 问题1: 数据库连接失败

**解决方案**:
```bash
# 确保PostgreSQL运行
# 确保数据库已迁移
cd backend
alembic upgrade head
```

### 问题2: 导入错误

**解决方案**:
```bash
# 确保在backend目录运行
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题3: Token认证失败

**解决方案**:
- 检查token是否过期
- 使用Swagger UI重新登录获取新token

---

## 💡 测试最佳实践

1. **隔离测试**: 每个测试独立,不依赖其他测试
2. **清理数据**: 测试后回滚数据库事务
3. **Mock外部依赖**: AI API调用使用Mock
4. **覆盖边界情况**: 测试空值、极值、异常情况

---

## 🎯 测试覆盖目标

| 模块 | 目标覆盖率 | 当前覆盖率 |
|------|-----------|-----------|
| models | 90% | 待测试 |
| services | 80% | 待测试 |
| api | 70% | 待测试 |
| schemas | 100% | 待测试 |

---

## 📚 参考资料

- [Pytest 文档](https://docs.pytest.org/)
- [pytest-asyncio](https://github.com/pytest-dev/pytest-asyncio)
- [FastAPI 测试](https://fastapi.tiangolo.com/tutorial/testing/)

---

**更新日期**: 2025-10-26
