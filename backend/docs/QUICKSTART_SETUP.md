# 🚀 AI去痕迹功能 - 快速启动指南

## ⚠️ 重要: 首次运行前必读

在运行测试或启动服务前，请**务必**完成以下步骤：

---

## 📦 步骤 1: 安装缺失的依赖

```bash
cd backend

# 激活虚拟环境 (如果还没激活)
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 安装 APScheduler (必需!)
pip install APScheduler==3.10.4
```

### ❓ 为什么需要这一步？

AI去痕迹功能使用 `APScheduler` 进行定时任务（每日清理过期数据）。如果不安装，服务将**无法启动**。

---

## 🗄️ 步骤 2: 运行数据库迁移

```bash
# 确保在 backend 目录
cd backend

# 运行迁移，创建新表
alembic upgrade head
```

### ❓ 这会创建哪些表？

- `user_profiles` - 用户画像表
- `humanize_sessions` - 去痕迹会话表 (核心数据)
- `humanize_session_details` - 会话详情表 (30天过期)

---

## ✅ 步骤 3: 验证安装

### 方式1: 启动服务

```bash
python -m uvicorn app.main:app --reload
```

**成功标志**:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
✅ APScheduler started successfully
```

**如果看到错误** `ModuleNotFoundError: No module named 'apscheduler'`:
- 回到步骤1，确认 APScheduler 已安装
- 确认虚拟环境已激活

### 方式2: 运行测试

```bash
python run_tests.py
```

**成功标志**:

```
✅ 单元测试 (Pytest) 成功
✅ 自动化API测试 成功
✅ 所有测试通过!
```

---

## 🎯 完整启动流程

```bash
# 1. 进入后端目录
cd backend

# 2. 激活虚拟环境
.\venv\Scripts\activate  # Windows

# 3. 安装依赖 (首次运行)
pip install APScheduler==3.10.4

# 4. 运行数据库迁移 (首次运行)
alembic upgrade head

# 5. 启动服务
python -m uvicorn app.main:app --reload

# 或运行测试
python run_tests.py
```

---

## 📚 相关文档

- **错误修复详情**: [ERROR_FIX_COMPLETE.md](./ERROR_FIX_COMPLETE.md)
- **测试修复说明**: [TESTING_FIX.md](./TESTING_FIX.md)
- **测试使用指南**: [TESTING_GUIDE.md](./TESTING_GUIDE.md)
- **功能使用指南**: [HUMANIZE_QUICKSTART.md](./HUMANIZE_QUICKSTART.md)

---

## 🐛 常见问题

### Q1: `ModuleNotFoundError: No module named 'apscheduler'`

**A**: 未安装 APScheduler

```bash
pip install APScheduler==3.10.4
```

### Q2: `relation "user_profiles" does not exist`

**A**: 未运行数据库迁移

```bash
alembic upgrade head
```

### Q3: `cannot import name 'async_session_maker'`

**A**: 代码已修复，如仍报错请清除缓存:

```bash
# Linux/Mac
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null

# Windows PowerShell
Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force
```

### Q4: 测试自动登录失败

**A**: 数据库中没有测试账号，可以:

**方式1**: 创建测试账号 (用户名: admin, 密码: 123456)

**方式2**: 使用环境变量指定其他账号

```bash
# Windows
$env:TEST_USERNAME="your_username"
$env:TEST_PASSWORD="your_password"

# Linux/Mac
export TEST_USERNAME=your_username
export TEST_PASSWORD=your_password
```

---

## ✨ 功能特点

完成安装后，你将获得：

- ✅ AI痕迹检测 (5维度评分)
- ✅ 三种强度的人性化改写 (light/medium/strong)
- ✅ 改写效果验证
- ✅ 智能用户画像 (自适应显示模式)
- ✅ 完整的统计和历史记录
- ✅ 自动化测试套件 (30+测试用例)

---

**文档更新**: 2025-10-26
**所需时间**: 2-3分钟
**难度**: ⭐ 简单
