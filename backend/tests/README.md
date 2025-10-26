# 测试脚本使用说明

## 📁 测试文件清单

```
backend/
├── tests/
│   ├── test_humanize.py           # ⭐ Pytest单元测试 (15个测试)
│   ├── test_humanize_auto.py      # 🤖 自动化集成测试 (8个测试)
│   └── test_humanize_mock.py      # 🎭 Mock测试 (避免AI调用)
├── run_tests.py                   # 🚀 一键运行所有测试
├── pytest.ini                     # ⚙️  Pytest配置
└── docs/
    └── TESTING_GUIDE.md           # 📖 测试指南

总计: 30+ 个测试用例
```

---

## 🚀 快速开始

### 方式1: 一键运行 (推荐)

```bash
cd backend
python run_tests.py
```

### 方式2: 运行单元测试

```bash
# 所有单元测试
pytest tests/test_humanize.py -v

# 所有Mock测试
pytest tests/test_humanize_mock.py -v

# 单个测试
pytest tests/test_humanize.py::test_user_profile_creation -v
```

### 方式3: 运行自动化测试

```bash
# 启动后端服务
python -m uvicorn app.main:app --reload

# 在另一个终端运行测试
python tests/test_humanize_auto.py --token "your_token"
```

---

## 📊 测试覆盖

### test_humanize.py (单元测试)

**UserProfile 测试 (4个)**
- ✅ 用户画像创建
- ✅ 统计数据更新
- ✅ 显示模式切换
- ✅ 设置更新

**HumanizeSession 测试 (2个)**
- ✅ 会话创建
- ✅ 会话与详情关联

**服务层测试 (2个)**
- ✅ 会话保存
- ✅ Token估算

**Prompt 测试 (3个)**
- ✅ 检测Prompt生成
- ✅ 三种强度Prompt
- ✅ 验证Prompt生成

**Schema 测试 (2个)**
- ✅ 检测结果Schema
- ✅ 用户画像Schema

### test_humanize_auto.py (自动化测试)

**API 测试 (5个)**
- ✅ API健康检查
- ✅ 获取用户画像
- ✅ 更新设置
- ✅ 获取历史记录
- ✅ 获取统计数据

**集成测试 (3个)**
- ✅ HumanizeService核心功能
- ✅ UserProfileService
- ✅ 数据库模型

### test_humanize_mock.py (Mock测试)

**Mock 测试 (7个)**
- ✅ 检测功能Mock
- ✅ 流式改写Mock
- ✅ 验证功能Mock
- ✅ 完整流程Mock
- ✅ Patch装饰器
- ✅ 性能测试
- ✅ 错误处理

---

## 💡 测试场景示例

### 场景1: 开发新功能后快速验证

```bash
# 只运行相关的单元测试
pytest tests/test_humanize.py::test_user_profile_creation -v
```

### 场景2: 提交代码前完整测试

```bash
# 运行所有测试
python run_tests.py
```

### 场景3: CI/CD 集成

```bash
# 在CI环境中运行 (不需要AI API)
pytest tests/test_humanize.py tests/test_humanize_mock.py -v --tb=short
```

### 场景4: 生成覆盖率报告

```bash
# 安装coverage
pip install pytest-cov

# 生成报告
pytest tests/test_humanize.py --cov=app.services.user_profile_service --cov-report=html

# 查看报告
open htmlcov/index.html
```

---

## 🔧 环境准备

### 安装依赖

```bash
pip install pytest pytest-asyncio pytest-cov httpx
```

### 启动服务 (自动化测试需要)

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 获取Token (自动化测试需要)

```bash
# 使用Swagger UI登录
open http://localhost:8000/docs

# 或使用curl
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'
```

---

## 📝 测试输出示例

### 成功输出

```
============================================================
🧪 AI去痕迹功能 - 自动化测试套件
============================================================

============================================================
🚀 单元测试 (Pytest)
============================================================
tests/test_humanize.py::test_user_profile_creation PASSED
tests/test_humanize.py::test_user_profile_update_stats PASSED
tests/test_humanize.py::test_user_profile_display_mode PASSED
...

✅ 单元测试 (Pytest) 成功

============================================================
📊 测试报告
============================================================
✅ 所有测试通过!
```

### 测试报告 (test_report.json)

```json
{
  "summary": {
    "total": 8,
    "passed": 8,
    "failed": 0,
    "pass_rate": "100.0%",
    "time": "2025-10-26T10:30:00"
  },
  "results": [
    {
      "name": "API健康检查",
      "passed": true,
      "message": "状态码: 200",
      "time": "2025-10-26T10:30:00"
    }
  ]
}
```

---

## 🐛 故障排查

### 问题1: 导入错误

```bash
ModuleNotFoundError: No module named 'app'
```

**解决方案:**
```bash
cd backend  # 确保在backend目录
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 问题2: 数据库连接失败

```bash
sqlalchemy.exc.OperationalError: connection refused
```

**解决方案:**
```bash
# 启动PostgreSQL
# 检查数据库配置
cat .env | grep DATABASE
```

### 问题3: 异步测试失败

```bash
RuntimeError: Event loop is closed
```

**解决方案:**
- 确保安装了 `pytest-asyncio`
- 检查 `pytest.ini` 中的 `asyncio_mode = auto`

---

## 📚 扩展阅读

- [完整测试指南](../docs/TESTING_GUIDE.md)
- [Pytest文档](https://docs.pytest.org/)
- [FastAPI测试](https://fastapi.tiangolo.com/tutorial/testing/)

---

**创建日期**: 2025-10-26
**维护者**: AI Writer Team
