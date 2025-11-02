# 配置说明文档

> 详细的配置参数说明

## 环境变量配置 (.env)

### 应用配置

```bash
# 应用名称
APP_NAME=NovelAIde

# 应用版本
APP_VERSION=1.0.0

# API 路径前缀
API_V1_PREFIX=/api/v1

# 调试模式（开发环境：True，生产环境：False）
DEBUG=True

# JWT 密钥（生产环境必须修改为复杂的随机字符串）
SECRET_KEY=your-secret-key-here-change-in-production
```

### 服务器配置

```bash
# 监听地址
# 0.0.0.0 = 允许外部访问
# 127.0.0.1 = 仅本地访问
HOST=0.0.0.0

# 监听端口
PORT=8000
```

### 数据库配置

#### SQLite（推荐用于开发）

```bash
DATABASE_URL=sqlite+aiosqlite:///./novelaide.db
DB_ECHO=False  # True 会打印所有 SQL 语句
```

#### PostgreSQL（推荐用于生产）

```bash
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/database_name
DB_ECHO=False
```

**参数说明**：
- `username`: 数据库用户名
- `password`: 数据库密码
- `localhost:5432`: 数据库地址和端口
- `database_name`: 数据库名称

### Redis 配置（可选）

```bash
# Redis 连接 URL
REDIS_URL=redis://localhost:6379/0

# 如果 Redis 需要密码
REDIS_URL=redis://:password@localhost:6379/0
```

**说明**：Redis 用于缓存和会话管理，如果不配置，系统会使用内存缓存。

### JWT 配置

```bash
# Access Token 过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Refresh Token 过期时间（天）
REFRESH_TOKEN_EXPIRE_DAYS=7

# 加密算法（不建议修改）
ALGORITHM=HS256
```

### CORS 配置

```bash
# 允许的前端地址（JSON 数组格式）
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# 生产环境示例：
# CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

### OpenAI 配置

```bash
# OpenAI API 密钥（必须配置）
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# API 基础 URL（可选，用于使用代理或兼容接口）
OPENAI_BASE_URL=https://api.openai.com/v1

# 使用 Azure OpenAI 示例：
# OPENAI_BASE_URL=https://your-resource.openai.azure.com
```

### 文件上传配置

```bash
# 最大上传大小（字节）
MAX_UPLOAD_SIZE=10485760  # 10MB

# 上传文件保存目录
UPLOAD_DIR=./uploads
```

### 日志配置

```bash
# 日志级别：DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL=INFO

# 日志文件路径
LOG_FILE=./logs/app.log
```

### 监控配置（可选）

```bash
# Sentry DSN（用于错误追踪）
SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

# 留空则不启用 Sentry
SENTRY_DSN=
```

### 管理员账号

```bash
# 管理员邮箱
ADMIN_EMAIL=admin@example.com

# 管理员密码（首次运行时会创建）
ADMIN_PASSWORD=change-this-password
```

## 配置文件模板

### 开发环境 (.env.development)

```bash
APP_NAME=NovelAIde
DEBUG=True
SECRET_KEY=dev-secret-key

HOST=127.0.0.1
PORT=8000

DATABASE_URL=sqlite+aiosqlite:///./novelaide_dev.db
DB_ECHO=True

OPENAI_API_KEY=sk-your-dev-key
OPENAI_BASE_URL=https://api.openai.com/v1

CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

LOG_LEVEL=DEBUG
```

### 生产环境 (.env.production)

```bash
APP_NAME=NovelAIde
DEBUG=False
SECRET_KEY=use-strong-random-key-here-at-least-32-characters

HOST=0.0.0.0
PORT=8000

DATABASE_URL=postgresql+asyncpg://novelaide:strong_password@db-server:5432/novelaide
DB_ECHO=False

REDIS_URL=redis://:redis_password@redis-server:6379/0

OPENAI_API_KEY=sk-your-production-key
OPENAI_BASE_URL=https://api.openai.com/v1

CORS_ORIGINS=["https://yourdomain.com"]

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=/var/app/uploads

LOG_LEVEL=INFO
LOG_FILE=/var/log/novelaide/app.log

SENTRY_DSN=https://xxxxx@sentry.io/xxxxx

ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=strong_admin_password
```

## 安全建议

### 1. SECRET_KEY

- ✅ 使用至少 32 字符的随机字符串
- ✅ 包含大小写字母、数字和特殊字符
- ❌ 不要使用默认值
- ❌ 不要提交到 Git

**生成随机密钥**：

```python
# Python 命令
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. 数据库密码

- ✅ 使用强密码（至少 12 字符）
- ✅ 定期更换密码
- ❌ 不要使用简单密码如 "password123"

### 3. API Key

- ✅ 使用环境变量，不要硬编码
- ✅ 定期检查使用量和账单
- ❌ 不要提交到 Git
- ❌ 不要在日志中打印

### 4. CORS

- ✅ 生产环境只允许真实的前端域名
- ❌ 不要使用 `*` 允许所有来源

### 5. 生产环境

- ✅ 设置 `DEBUG=False`
- ✅ 使用 PostgreSQL 替代 SQLite
- ✅ 启用 HTTPS
- ✅ 配置防火墙
- ✅ 启用日志和监控

## 配置验证

### 检查配置是否正确

```bash
# Windows
check_env.bat

# 或手动检查
python -c "from app.core.config import settings; print(settings)"
```

### 测试数据库连接

```bash
python -c "import asyncio; from app.core.database import engine; asyncio.run(engine.connect())"
```

### 测试 OpenAI 连接

```bash
python -c "import openai; import os; openai.api_key = os.getenv('OPENAI_API_KEY'); print(openai.Model.list())"
```

## 常见问题

### Q: 如何切换数据库？

**A**: 修改 `.env` 中的 `DATABASE_URL`：

```bash
# SQLite
DATABASE_URL=sqlite+aiosqlite:///./novelaide.db

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname

# MySQL
DATABASE_URL=mysql+aiomysql://user:password@localhost/dbname
```

### Q: 如何修改端口？

**A**: 修改 `.env` 中的 `PORT` 或直接修改 `quick_start.bat`：

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
```

### Q: 如何允许外部访问？

**A**: 修改 `.env` 中的 `HOST`：

```bash
HOST=0.0.0.0
```

然后在 `CORS_ORIGINS` 中添加外部地址。

### Q: OpenAI API 太慢/失败怎么办？

**A**: 可以使用国内代理或兼容接口：

```bash
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://your-proxy.com/v1
```

## 配置优先级

1. 环境变量（最高优先级）
2. `.env` 文件
3. 默认值（代码中的默认值）

**示例**：

```bash
# 命令行设置环境变量
set PORT=8001
python -m uvicorn app.main:app

# 这会覆盖 .env 文件中的 PORT 配置
```

## 更多帮助

- 查看 `.env.example` 获取完整配置模板
- 查看 `app/core/config.py` 了解配置加载逻辑
- 遇到问题查看日志文件 `logs/app.log`
