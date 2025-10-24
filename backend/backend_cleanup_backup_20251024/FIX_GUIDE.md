# 数据库手动修复指南

## 问题
数据库缺少 `notification_settings` 和 `preferences` 字段，导致登录失败。

## 解决方案

### 方法 1：使用 psql 命令行（推荐）

```bash
# 1. 找到你的数据库连接信息（从 .env 文件）
# DATABASE_URL=postgresql://用户名:密码@localhost:端口/数据库名

# 2. 执行修复 SQL
cd D:\Java\ai_writer\backend
psql -U your_username -d your_database -f fix_database.sql

# 或者一行命令（替换连接信息）
psql postgresql://用户名:密码@localhost:端口/数据库名 -f fix_database.sql
```

### 方法 2：使用 pgAdmin 或其他 GUI 工具

1. 打开 pgAdmin 或 DBeaver
2. 连接到你的数据库
3. 打开查询编辑器
4. 复制 `fix_database.sql` 的内容
5. 执行 SQL

### 方法 3：使用 Python 脚本自动执行

我创建了一个 Python 脚本来自动执行：

```bash
cd D:\Java\ai_writer\backend
venv\Scripts\activate
python scripts/run_fix_sql.py
```

---

## 验证修复成功

修复后，应该看到：

```
 column_name           | data_type
-----------------------+-----------
 notification_settings | jsonb
 preferences           | jsonb

 user_sessions_exists
----------------------
 t
```

---

## 修复后重启后端

```bash
# 停止当前后端（Ctrl+C）
# 重新启动
python -m uvicorn app.main:app --reload --port 8000
```

---

## 如果还有问题

请提供：
1. 你的 DATABASE_URL（隐藏密码）
2. PostgreSQL 版本
3. 是否能访问 psql 命令
