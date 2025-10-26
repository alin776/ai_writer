# 测试脚本修复说明

## 🐛 修复的问题

### 1. **Pytest 模块导入错误**

**问题**: 所有测试都失败，错误 `ModuleNotFoundError: No module named 'app'`

**原因**: PYTHONPATH 未正确设置

**解决方案**:
- 创建 `backend/tests/conftest.py` 文件
- 自动添加 backend 目录到 Python 路径

```python
# tests/conftest.py
import sys
from pathlib import Path

backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))
```

---

### 2. **需要手动输入Token问题**

**问题**: 运行测试时需要手动输入登录token，很不方便

**原因**: 测试脚本没有自动登录功能

**解决方案**:
- 在 `test_humanize_auto.py` 中添加 `auto_login()` 方法
- 默认使用账号 `admin/123456` 自动登录
- 支持通过环境变量 `TEST_USERNAME` 和 `TEST_PASSWORD` 自定义

```python
async def auto_login(self, username: str = None, password: str = None):
    """自动登录获取token"""
    if not username:
        username = os.getenv("TEST_USERNAME", "admin")
    if not password:
        password = os.getenv("TEST_PASSWORD", "123456")

    # 自动调用登录API获取token
    ...
```

---

### 3. **run_tests.py 环境设置**

**问题**: Windows 环境下 PYTHONPATH 未设置

**解决方案**:
- 在 `run_tests.py` 的 `main()` 函数开始时设置环境变量
- 自动登录提示，不再询问token

```python
def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.environ["PYTHONPATH"] = os.getcwd()  # 设置环境变量
```

---

## ✅ 修复后的使用方式

### 快速使用 (推荐)

```bash
cd backend
python run_tests.py
```

**自动完成**:
- ✅ 自动设置 PYTHONPATH
- ✅ 自动登录获取 token (默认 admin/123456)
- ✅ 运行所有测试

### 自定义测试账号

**方式1: 环境变量**
```bash
# Windows PowerShell
$env:TEST_USERNAME="test"
$env:TEST_PASSWORD="test123"
python run_tests.py

# Linux/Mac
export TEST_USERNAME=test
export TEST_PASSWORD=test123
python run_tests.py
```

**方式2: .env 文件**
```bash
# backend/.env
TEST_USERNAME=test
TEST_PASSWORD=test123
```

### 单独运行测试

**单元测试**:
```bash
pytest tests/test_humanize.py -v
```

**Mock测试**:
```bash
pytest tests/test_humanize_mock.py -v
```

**自动化测试** (需要启动服务):
```bash
# 终端1: 启动服务
python -m uvicorn app.main:app --reload

# 终端2: 运行测试 (自动登录)
python tests/test_humanize_auto.py
```

---

## 📋 修复清单

- [x] 创建 `tests/conftest.py` 修复导入问题
- [x] 添加 `auto_login()` 自动登录功能
- [x] 修改 `run_tests.py` 设置环境变量
- [x] 删除错误的 `INFO.md` 测试日志文件
- [x] 更新测试文档

---

## 🔧 故障排查

### 自动登录失败

**错误**: `⚠️ 自动登录失败 (状态码: 401)`

**解决方案**:
1. 确保数据库中有测试账号 (默认: admin/123456)
2. 使用环境变量指定其他账号
3. 或手动提供 token: `python tests/test_humanize_auto.py --token "your_token"`

### 模块导入错误

**错误**: `ModuleNotFoundError: No module named 'app'`

**解决方案**:
1. 确保在 `backend` 目录下运行
2. 确保 `tests/conftest.py` 文件存在
3. 尝试手动设置: `export PYTHONPATH="$(pwd)"` (Linux/Mac) 或 `$env:PYTHONPATH="$(pwd)"` (Windows)

---

**修复日期**: 2025-10-26
**影响文件**:
- `backend/tests/conftest.py` (新建)
- `backend/tests/test_humanize_auto.py` (修改)
- `backend/run_tests.py` (修改)
- `backend/docs/INFO.md` (删除)
