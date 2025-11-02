# PostgreSQL 安装和配置指南

> 本项目使用 PostgreSQL 作为数据库，本指南将帮助你快速安装和配置。

## 📥 下载和安装

### 方式一：自动下载（推荐）

运行 `setup.bat` 时会自动检测 PostgreSQL，如未安装会提示下载。

### 方式二：手动下载

**下载地址**：https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe

或访问官网：https://www.postgresql.org/download/windows/

## 🔧 安装步骤

### 1. 运行安装程序

双击下载的 `postgresql-15.14-2-windows-x64.exe`

### 2. 安装向导

#### ① 选择安装目录
```
默认：C:\Program Files\PostgreSQL\15
建议：保持默认
```

#### ② 选择组件
- ✅ PostgreSQL Server（必须）
- ✅ pgAdmin 4（管理工具，推荐）
- ✅ Stack Builder（可选）
- ✅ Command Line Tools（必须）

#### ③ 设置数据目录
```
默认：C:\Program Files\PostgreSQL\15\data
建议：保持默认
```

#### ④ 设置超级用户密码
```
⚠️ 重要：请记住这个密码！
建议密码：postgres（开发环境）
或设置一个强密码并记录下来
```

#### ⑤ 设置端口
```
默认：5432
建议：保持默认
```

#### ⑥ 设置区域
```
默认：Chinese (Simplified), China
建议：保持默认
```

#### ⑦ 完成安装
点击"Next"开始安装，等待完成（约3-5分钟）

### 3. 验证安装

打开命令行，输入：

```bash
psql --version
```

如果显示版本信息（如 `psql (PostgreSQL) 15.14`），说明安装成功。

## 🗄️ 创建数据库

### 方式一：使用 pgAdmin（图形化，推荐新手）

1. 打开 pgAdmin 4（开始菜单 → PostgreSQL 15 → pgAdmin 4）
2. 输入超级用户密码
3. 右键点击"Databases" → "Create" → "Database"
4. 输入数据库名：`novelaide`
5. 点击"Save"

### 方式二：使用命令行（推荐）

#### 1. 连接到 PostgreSQL

```bash
# Windows
psql -U postgres

# 输入安装时设置的超级用户密码
```

#### 2. 运行数据库初始化脚本

```sql
-- 创建数据库
CREATE DATABASE novelaide
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Chinese (Simplified)_China.936'
    LC_CTYPE = 'Chinese (Simplified)_China.936'
    CONNECTION LIMIT = -1;

-- 创建用户
CREATE USER novelaide WITH PASSWORD 'novelaide_password';

-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE novelaide TO novelaide;

-- 切换到 novelaide 数据库
\c novelaide

-- 授予 schema 权限
GRANT ALL PRIVILEGES ON SCHEMA public TO novelaide;

-- 安装 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 退出
\q
```

#### 3. 或者直接运行 SQL 文件

```bash
# 在 backend 目录下运行
psql -U postgres < setup_db.sql
# 输入超级用户密码
```

### 方式三：自动初始化（最简单）

运行项目的启动脚本 `quick_start.bat` 会自动创建数据库表结构。

前提：数据库 `novelaide` 和用户 `novelaide` 已创建。

## ⚙️ 配置项目

### 1. 修改 .env 文件

打开 `backend/.env`，确认数据库配置：

```bash
DATABASE_URL=postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide
```

**参数说明**：
- `novelaide` - 数据库用户名
- `novelaide_password` - 数据库密码
- `localhost` - 数据库地址
- `5432` - 数据库端口
- `novelaide` - 数据库名

### 2. 如果修改了密码

如果你在创建用户时使用了不同的密码，需要修改 `.env` 中的 `DATABASE_URL`：

```bash
# 格式
DATABASE_URL=postgresql+asyncpg://用户名:密码@地址:端口/数据库名

# 示例
DATABASE_URL=postgresql+asyncpg://novelaide:your_password@localhost:5432/novelaide
```

## 🧪 测试连接

### 1. 使用 Python 测试

在 `backend` 目录下运行：

```bash
python -c "import asyncio; from app.core.database import engine; asyncio.run(engine.connect().aclose())"
```

如果没有报错，说明连接成功。

### 2. 使用 psql 测试

```bash
psql -U novelaide -d novelaide -h localhost -p 5432
# 输入密码：novelaide_password
```

如果能登录，说明配置正确。

## 🚨 常见问题

### Q1: psql 命令找不到？

**原因**：PostgreSQL 的 bin 目录不在系统 PATH 中。

**解决方法**：

1. 找到 PostgreSQL 安装目录（如 `C:\Program Files\PostgreSQL\15\bin`）
2. 添加到系统环境变量 PATH
3. 重新打开命令行

或者直接使用完整路径：

```bash
"C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres
```

### Q2: 连接被拒绝（Connection refused）

**可能原因**：
1. PostgreSQL 服务未启动
2. 端口被占用
3. 防火墙阻止

**解决方法**：

#### 检查服务是否运行

```bash
# Windows 服务管理
services.msc

# 找到 postgresql-x64-15
# 确认状态为"正在运行"
```

或命令行：

```bash
sc query postgresql-x64-15
```

如果未运行，启动服务：

```bash
# 以管理员身份运行命令行
net start postgresql-x64-15
```

### Q3: 密码认证失败

**错误信息**：`password authentication failed for user "novelaide"`

**解决方法**：

1. 检查 `.env` 中的密码是否正确
2. 重新设置用户密码：

```sql
-- 以 postgres 用户登录
psql -U postgres

-- 修改密码
ALTER USER novelaide WITH PASSWORD 'novelaide_password';

-- 退出
\q
```

### Q4: 数据库不存在

**错误信息**：`database "novelaide" does not exist`

**解决方法**：

```bash
# 以 postgres 用户登录
psql -U postgres

# 创建数据库
CREATE DATABASE novelaide OWNER novelaide;

# 退出
\q
```

### Q5: 权限不足

**错误信息**：`permission denied for schema public`

**解决方法**：

```bash
# 以 postgres 用户登录
psql -U postgres -d novelaide

# 授予权限
GRANT ALL PRIVILEGES ON SCHEMA public TO novelaide;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO novelaide;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO novelaide;

# 退出
\q
```

### Q6: 中文乱码

**解决方法**：

确保数据库编码为 UTF8：

```sql
-- 检查编码
SELECT datname, encoding FROM pg_database WHERE datname = 'novelaide';

-- 如果不是 UTF8，重建数据库
DROP DATABASE novelaide;
CREATE DATABASE novelaide WITH ENCODING 'UTF8';
```

## 🔒 安全建议

### 开发环境
- ✅ 可以使用简单密码（如 `novelaide_password`）
- ✅ 可以使用默认端口 5432
- ✅ 只监听 localhost

### 生产环境
- ⚠️ 必须使用强密码（至少 16 字符，包含大小写字母、数字、特殊字符）
- ⚠️ 考虑修改默认端口
- ⚠️ 配置防火墙规则
- ⚠️ 启用 SSL 连接
- ⚠️ 定期备份数据库
- ⚠️ 限制数据库用户权限

## 🛠️ 管理工具

### pgAdmin 4（推荐）
- 图形化管理界面
- 自带在 PostgreSQL 安装包中
- 适合：查看数据、执行查询、管理数据库

### DBeaver（推荐）
- 免费、开源
- 支持多种数据库
- 下载：https://dbeaver.io/

### DataGrip（付费）
- JetBrains 出品
- 功能强大
- 适合专业开发者

## 📖 数据库结构

项目会自动创建以下表：

- `users` - 用户表
- `works` - 作品表
- `chapters` - 章节表

表结构会在首次启动时自动创建（通过 SQLAlchemy）。

## 🔄 数据库迁移

使用 Alembic 管理数据库版本：

```bash
# 查看当前版本
alembic current

# 升级到最新版本
alembic upgrade head

# 创建新的迁移
alembic revision --autogenerate -m "描述"

# 回滚到上一个版本
alembic downgrade -1
```

## 📞 获取帮助

如果以上方法都无法解决问题：

1. 查看 PostgreSQL 日志：`C:\Program Files\PostgreSQL\15\data\log\`
2. 查看项目日志：`backend/logs/app.log`
3. 运行 `check_env.bat` 检查环境
4. 联系后端开发者

## 📚 参考资源

- PostgreSQL 官方文档：https://www.postgresql.org/docs/15/
- PostgreSQL 中文文档：http://www.postgres.cn/docs/15/
- pgAdmin 文档：https://www.pgadmin.org/docs/

---

祝安装顺利！🎉
