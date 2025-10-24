# 数据库迁移问题修复指南

## 问题描述
运行 `alembic upgrade head` 时出错：
```
错误: 关系 "entity_relationships" 已经存在
```

## 原因
数据库中的表已经存在，但 Alembic 迁移版本记录不一致。

---

## 🔧 解决方案（3选1）

### 方案 1：使用 stamp 命令（推荐）⭐

**最简单安全的方法**，直接标记数据库为最新版本：

```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
alembic stamp head
```

然后检查是否成功：
```bash
alembic current
```

应该显示最新版本号。

---

### 方案 2：手动修复特定迁移

如果方案 1 不行，手动跳过有问题的迁移：

```bash
# 1. 检查当前版本
alembic current

# 2. 标记为下一个版本（跳过出错的迁移）
alembic stamp d1e2f3g4h5i6

# 3. 再次尝试升级
alembic upgrade head
```

---

### 方案 3：完全重置迁移（慎用）⚠️

**警告：这会删除所有数据！仅用于开发环境！**

```bash
# 1. 进入 PostgreSQL
psql -U your_username -d your_database

# 2. 删除所有表
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

# 3. 退出 psql，重新运行迁移
\q
alembic upgrade head
```

---

## ✅ 验证修复

修复后，运行以下命令验证：

```bash
# 检查当前版本
alembic current

# 应该显示最新版本
# INFO  [alembic.runtime.migration] d1e2f3g4h5i6 (head)
```

---

## 🚀 修复后继续测试

修复成功后，继续启动服务：

```bash
# 终端 1 - 后端
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000

# 终端 2 - 前端
cd D:\Java\ai_writer
npm run dev
```

---

## 📞 如果还有问题

请提供以下信息：
1. 执行 `alembic current` 的输出
2. 执行 `alembic history` 的输出
3. 数据库中是否有 user_sessions 表
   ```sql
   SELECT tablename FROM pg_tables WHERE tablename = 'user_sessions';
   ```
