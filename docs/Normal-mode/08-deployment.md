# 部署运维指南

> 📋 **文档**: 08-deployment.md | **最后更新**: 2025-10-24

[← 返回文档导航](./README.md)

---

## 📋 目录

- [开发环境搭建](#开发环境搭建)
- [环境变量配置](#环境变量配置)
- [数据库迁移](#数据库迁移)
- [生产环境部署](#生产环境部署)
- [Docker 部署](#docker-部署)
- [监控与日志](#监控与日志)
- [常见问题](#常见问题)

---

## 💻 开发环境搭建

### 系统要求

- **操作系统**: Windows 10+, macOS 12+, Ubuntu 20.04+
- **Python**: 3.11+
- **Node.js**: 18+
- **PostgreSQL**: 15+
- **Redis**: 7+ (可选)

### 1. 克隆项目

```bash
git clone https://github.com/your-org/novelaide.git
cd novelaide
```

### 2. 后端setup

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 前端安装

```bash
cd frontend

# 安装依赖
npm install

# 或使用 pnpm (推荐)
pnpm install
```

### 4. 数据库设置

```bash
# 创建数据库
createdb novelaide_dev

# 安装 pgvector 扩展
psql -d novelaide_dev -c "CREATE EXTENSION vector;"

# 运行迁移
cd backend
alembic upgrade head
```

---

## 🔧 环境变量配置

### 后端环境变量 (`.env`)

```bash
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/novelaide_dev

# JWT 密钥
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24小时
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI API 配置
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://204992.xyz

# Redis 配置 (可选)
REDIS_URL=redis://localhost:6379/0

# 腾讯云 COS 配置 (头像上传)
COS_SECRET_ID=your-secret-id
COS_SECRET_KEY=your-secret-key
COS_REGION=ap-guangzhou
COS_BUCKET=novelaide-1234567890

# CORS 设置
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# 环境标识
ENVIRONMENT=development
```

### 前端环境变量 (`.env.local`)

```bash
# API Base URL
VITE_API_BASE_URL=http://localhost:8000/api/v1

# 应用配置
VITE_APP_TITLE=NovelAIde
VITE_APP_VERSION=2.12.0
```

---

## 🗄️ 数据库迁移

### Alembic 迁移工具

```bash
cd backend

# 创建新迁移
alembic revision --autogenerate -m "描述变更内容"

# 查看迁移历史
alembic history

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1

# 回滚到特定版本
alembic downgrade <revision_id>
```

### 重要迁移记录

| 时间 | 版本 | 说明 |
|------|------|------|
| 2025-10-24 | `20251024_1800` | 添加 AI 调用日志表 |
| 2025-10-24 | `e1f2g3h4i5j6` | 添加 ChapterStatus 枚举 |
| 2025-10-23 | `d5e6f7g8h9i0` | 添加用户会话管理表 |

---

## 🚀 运行项目

### 开发模式

**启动后端**:
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**启动前端**:
```bash
cd frontend
npm run dev
# 或
pnpm dev
```

访问:
- **前端**: http://localhost:5173
- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs

---

## 🏭 生产环境部署

### 1. 后端部署

#### 使用 Gunicorn + Uvicorn

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动服务
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 300 \
  --access-logfile -\
  --error-logfile -
```

#### 使用 Systemd (推荐)

创建服务文件 `/etc/systemd/system/novelaide-api.service`:

```ini
[Unit]
Description=NovelAIde API Server
After=network.target postgresql.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/novelaide/backend
Environment="PATH=/var/www/novelaide/backend/venv/bin"
ExecStart=/var/www/novelaide/backend/venv/bin/gunicorn \
  app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
sudo systemctl start novelaide-api
sudo systemctl enable novelaide-api
sudo systemctl status novelaide-api
```

### 2. 前端部署

```bash
cd frontend

# 构建生产版本
npm run build

# 产物在 dist/ 目录
```

#### 使用 Nginx 部署

Nginx 配置 (`/etc/nginx/sites-available/novelaide`):

```nginx
server {
    listen 80;
    server_name novelaide.com www.novelaide.com;

    # 前端静态文件
    location / {
        root /var/www/novelaide/frontend/dist;
        try_files $uri $uri/ /index.html;

        # Gzip 压缩
        gzip on;
        gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    }

    # API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE 支持
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 300s;
    }
}
```

启用站点:
```bash
sudo ln -s /etc/nginx/sites-available/novelaide /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. HTTPS 配置

使用 Let's Encrypt:

```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d novelaide.com -d www.novelaide.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 🐳 Docker 部署

### Docker Compose 配置

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: novelaide
      POSTGRES_USER: novelaide
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U novelaide"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://novelaide:${DB_PASSWORD}@postgres:5432/novelaide
      REDIS_URL: redis://redis:6379/0
      SECRET_KEY: ${SECRET_KEY}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    command: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
  redis_data:
```

### 后端 Dockerfile

`backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY . .

# 运行迁移和启动
CMD alembic upgrade head && \
    gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 前端 Dockerfile

`frontend/Dockerfile`:

```dockerfile
# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 启动服务

```bash
# 创建 .env 文件
cp .env.example .env
# 编辑 .env 配置

# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

---

## 📊 监控与日志

### 应用日志

**后端日志配置** (`backend/app/core/logging.py`):

```python
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('logs/app.log', maxBytes=10485760, backupCount=10),
        logging.StreamHandler()
    ]
)
```

**查看日志**:
```bash
# 实时查看
tail -f logs/app.log

# 搜索错误
grep "ERROR" logs/app.log
```

### 性能监控

推荐使用:
- **Sentry**: 错误追踪
- **Prometheus + Grafana**: 指标监控
- **ELK Stack**: 日志分析

---

## ❓ 常见问题

### Q1: 数据库连接失败

**错误**: `could not connect to server`

**解决**:
```bash
# 检查 PostgreSQL 服务状态
sudo systemctl status postgresql

# 检查数据库是否存在
psql -l

# 验证连接字符串
psql "postgresql://user:password@localhost:5432/novelaide_dev"
```

### Q2: 迁移失败

**错误**: `Alembic migration failed`

**解决**:
```bash
# 查看当前版本
alembic current

# 回滚到上一版本
alembic downgrade -1

# 手动修复数据库
psql -d novelaide_dev

# 重新运行迁移
alembic upgrade head
```

### Q3: 前端构建错误

**错误**: `npm run build` 失败

**解决**:
```bash
# 清除缓存
rm -rf node_modules
rm package-lock.json

# 重新安装
npm install

# 检查 Node 版本
node -v  # 需要 18+
```

### Q4: AI API 调用失败

**错误**: `OpenAI API error`

**解决**:
```bash
# 检查 API Key
echo $OPENAI_API_KEY

# 测试连接
curl https://204992.xyz/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# 检查网络
ping 204992.xyz
```

---

## 🔗 相关链接

- **上一章**: [API参考文档](./07-api-reference.md)
- **下一章**: [参考资源](./09-references.md)
- **返回**: [文档导航](./README.md)
- **主文档**: [NovelAIde 项目文档 v2.12.md](../NovelAIde%20项目文档%20v2.12.md)

---

**最后更新**: 2025-10-24
**维护者**: NovelAIde 团队
