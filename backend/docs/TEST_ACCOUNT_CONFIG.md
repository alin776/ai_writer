# 🔐 测试账号配置说明

## 📝 当前配置

测试脚本现在使用以下账号自动登录：

**默认测试账号**:
- 用户名: `2072855200@qq.com`
- 密码: `zrt3ljnygz@163.com`

---

## 🔧 如何使用

### 方式 1: 直接运行（使用默认账号）

```bash
cd backend
python run_tests.py
```

测试脚本会自动使用管理员账号登录。

---

### 方式 2: 使用环境变量（自定义账号）

如果你想使用其他账号测试：

**Windows PowerShell**:
```powershell
$env:TEST_USERNAME="your_username"
$env:TEST_PASSWORD="your_password"
python run_tests.py
```

**Linux/Mac**:
```bash
export TEST_USERNAME=your_username
export TEST_PASSWORD=your_password
python run_tests.py
```

---

### 方式 3: 永久配置（.env 文件）

创建 `backend/.env.test` 文件：

```ini
# 测试账号配置
TEST_USERNAME=2072855200@qq.com
TEST_PASSWORD=zrt3ljnygz@163.com
```

然后加载：

```bash
# Windows
Get-Content .env.test | ForEach-Object {
    if ($_ -match '^([^=]+)=(.+)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2])
    }
}

# Linux/Mac
set -a
source .env.test
set +a
```

---

## 🔒 安全建议

### ⚠️ 重要提醒

当前配置将**真实管理员账号**硬编码在测试脚本中，这在生产环境中是**不安全**的。

### 推荐做法

1. **开发环境**:
   - ✅ 可以使用当前配置（方便快速测试）

2. **CI/CD 环境**:
   - ❌ 不要提交真实密码到Git
   - ✅ 使用环境变量
   - ✅ 使用CI系统的密钥管理（如 GitHub Secrets）

3. **生产环境**:
   - ❌ 绝对不要使用测试账号
   - ✅ 使用独立的测试账号
   - ✅ 定期更换密码

---

## 🔐 创建专用测试账号（推荐）

建议创建一个专门用于测试的账号：

```bash
# 使用 Swagger UI 或 API 创建
POST /api/v1/auth/register
{
  "username": "test_user",
  "email": "test@example.com",
  "password": "test_password_123"
}
```

然后修改 `test_humanize_auto.py`:

```python
username = os.getenv("TEST_USERNAME", "test_user")
password = os.getenv("TEST_PASSWORD", "test_password_123")
```

---

## 📊 当前配置文件

| 文件 | 配置内容 |
|------|---------|
| `tests/test_humanize_auto.py` | 自动登录逻辑 + 默认账号 |
| `run_tests.py` | 测试运行器 + 提示信息 |

---

## 🚀 快速验证

测试登录是否成功：

```bash
# 启动服务
python -m uvicorn app.main:app --reload

# 在另一个终端运行测试
python tests/test_humanize_auto.py
```

**成功标志**:
```
✅ 自动登录成功 (用户: 2072855200@qq.com)
```

---

## 🐛 故障排查

### 问题 1: 401 Unauthorized

**原因**: 账号密码错误

**解决**:
1. 检查账号是否存在
2. 检查密码是否正确
3. 确认账号状态为 `is_active=true`

### 问题 2: 422 Validation Error

**原因**: 请求格式错误

**解决**: 确保使用 `data={}` 而不是 `json={}`

---

**更新日期**: 2025-10-26
**配置方式**: 硬编码（开发环境）
**安全级别**: ⚠️ 仅适用于开发/测试环境
