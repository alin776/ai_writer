# 文枢AI 云服务器一键部署指南

> 本文档包含部署到云服务器所需的所有配置文件和命令

---

## 目录

1. [服务器要求](#1-服务器要求)
2. [快速部署步骤](#2-快速部署步骤)
3. [配置文件清单](#3-配置文件清单)
4. [详细部署命令](#4-详细部署命令)
5. [常见问题](#5-常见问题)

---

## 1. 服务器要求

| 配置项 | 最低要求 | 推荐配置 |
|--------|---------|---------|
| CPU | 2核 | 4核+ |
| 内存 | 4GB | 8GB+ |
| 磁盘 | 40GB SSD | 100GB SSD |
| 系统 | Ubuntu 20.04+ | Ubuntu 22.04 |
| 带宽 | 5Mbps | 10Mbps+ |

**需要开放的端口：**
- 80 (HTTP)
- 443 (HTTPS)
- 22 (SSH)

---

## 2. 快速部署步骤

```bash
# 1. 上传项目到服务器
scp -r ./ai_writer root@你的服务器IP:/root/

# 2. SSH登录服务器
ssh root@你的服务器IP

# 3. 进入项目目录
cd /root/ai_writer

# 4. 执行部署脚本
chmod +x deploy.sh
./deploy.sh
```

---

## 3. 配置文件清单

部署需要以下文件，请按照下面的内容创建：

### 3.1 项目根目录结构

```
ai_writer/
├── backend/                 # 后端代码
│   ├── app/
│   ├── alembic/
│   ├── Dockerfile          # 后端Docker镜像 [已有]
│   ├── requirements.txt
│   └── .env                # 后端环境变量 [需配置]
├── src/                    # 前端源码
├── dist/                   # 前端构建产物 [需构建]
├── package.json
├── Dockerfile              # 前端Docker镜像 [需创建]
├── nginx.conf              # Nginx配置 [需创建]
├── docker-compose.prod.yml # 生产环境编排 [需创建]
└── deploy.sh               # 部署脚本 [需创建]
```

---

### 3.2 前端 Dockerfile（项目根目录）

创建文件：`Dockerfile`

```dockerfile
# ============================================
# 文枢AI 前端 Dockerfile
# ============================================

# 阶段1：构建前端
FROM node:22-alpine AS builder

WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --registry=https://registry.npmmirror.com

# 复制源代码
COPY . .

# 设置环境变量（构建时使用）
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# 构建
RUN npm run build

# 阶段2：Nginx服务
FROM nginx:alpine

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

### 3.3 Nginx 配置文件

创建文件：`nginx.conf`

```nginx
# ============================================
# 文枢AI Nginx 配置
# ============================================

server {
    listen 80;
    server_name localhost;

    # 前端静态文件
    root /usr/share/nginx/html;
    index index.html;

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml;
    gzip_comp_level 6;

    # 前端路由 - SPA支持
    location / {
        try_files $uri $uri/ /index.html;

        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置（AI接口需要较长时间）
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # 大文件上传支持
        client_max_body_size 20M;
    }

    # WebSocket 支持（如有实时功能）
    location /ws/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "OK";
        add_header Content-Type text/plain;
    }
}
```

---

### 3.4 生产环境 Docker Compose

创建文件：`docker-compose.prod.yml`

```yaml
# ============================================
# 文枢AI 生产环境 Docker Compose
# ============================================

version: '3.8'

services:
  # ==================== 数据库 ====================
  postgres:
    image: postgres:15-alpine
    container_name: wenshu_postgres
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER:-novelaide}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-novelaide_password}
      POSTGRES_DB: ${DB_NAME:-novelaide}
      TZ: Asia/Shanghai
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - wenshu_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U novelaide"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==================== 缓存 ====================
  redis:
    image: redis:7-alpine
    container_name: wenshu_redis
    restart: always
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - wenshu_network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ==================== 后端API ====================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: wenshu_backend
    restart: always
    env_file:
      - ./backend/.env.prod
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER:-novelaide}:${DB_PASSWORD:-novelaide_password}@postgres:5432/${DB_NAME:-novelaide}
      - REDIS_URL=redis://redis:6379/0
      - ENABLE_SCHEDULER=false
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - wenshu_network
    volumes:
      - backend_logs:/app/logs
      - backend_uploads:/app/uploads

  # ==================== 定时任务 ====================
  scheduler:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: wenshu_scheduler
    restart: always
    command: ["python", "-m", "app.tasks.scheduler_runner"]
    env_file:
      - ./backend/.env.prod
    environment:
      - DATABASE_URL=postgresql+asyncpg://${DB_USER:-novelaide}:${DB_PASSWORD:-novelaide_password}@postgres:5432/${DB_NAME:-novelaide}
      - REDIS_URL=redis://redis:6379/0
      - ENABLE_SCHEDULER=true
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - wenshu_network
    volumes:
      - backend_logs:/app/logs

  # ==================== 前端 + Nginx ====================
  frontend:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        VITE_API_URL: ""
    container_name: wenshu_frontend
    restart: always
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - backend
    networks:
      - wenshu_network
    volumes:
      - ./ssl:/etc/nginx/ssl:ro  # SSL证书目录（可选）

# ==================== 数据卷 ====================
volumes:
  postgres_data:
    name: wenshu_postgres_data
  redis_data:
    name: wenshu_redis_data
  backend_logs:
    name: wenshu_backend_logs
  backend_uploads:
    name: wenshu_backend_uploads

# ==================== 网络 ====================
networks:
  wenshu_network:
    name: wenshu_network
    driver: bridge
```

---

### 3.5 后端生产环境变量

创建文件：`backend/.env.prod`

```bash
# ============================================
# 文枢AI 后端生产环境配置
# ============================================

# ==================== 应用配置 ====================
APP_NAME=文枢AI
APP_VERSION=1.0.0
API_V1_PREFIX=/api/v1
DEBUG=False

# !!! 重要：请修改为随机密钥 !!!
# 生成方法: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=请替换为你的随机密钥

# ==================== 服务器配置 ====================
HOST=0.0.0.0
PORT=8000

# ==================== 数据库配置 ====================
# Docker内部使用，不需要修改
DATABASE_URL=postgresql+asyncpg://novelaide:novelaide_password@postgres:5432/novelaide
DB_ECHO=False

# ==================== Redis配置 ====================
REDIS_URL=redis://redis:6379/0

# ==================== JWT配置 ====================
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# ==================== CORS配置 ====================
# !!! 修改为你的域名 !!!
CORS_ORIGINS=["https://你的域名.com","http://你的域名.com"]

# ==================== OpenAI/AI配置 ====================
# !!! 重要：填入你的API密钥 !!!
OPENAI_API_KEY=你的API密钥
OPENAI_BASE_URL=https://204992.xyz/v1
OPENAI_MODEL=gemini-2.5-pro
OPENAI_TIMEOUT=120
OPENAI_CONNECT_TIMEOUT=30
OPENAI_MAX_RETRIES=3

# 模型配置
MODEL_SIMPLE_TASK=gemini-2.5-flash-lite
MODEL_MEDIUM_TASK=gemini-2.5-flash
MODEL_COMPLEX_TASK=gemini-2.5-pro
REVIEW_MODEL=gemini-2.5-flash
BOOK_ANALYSIS_MODEL=gemini-2.5-flash-lite
BOOK_ANALYSIS_TIMEOUT=60

# ==================== Agent配置 ====================
ENABLE_ENHANCED_MEMORY=True
ENABLE_QUALITY_LOOP=True
ENABLE_VERSION_CONTROL=True
ENABLE_MODEL_SELECTION=True
ENABLE_SMART_PROMPTS=True
AGENT_USE_DUAL_PROMPT=False

# Memory配置
MEMORY_SHORT_TERM_SIZE=10
MEMORY_MEDIUM_TERM_SIZE=100
MEMORY_FORGET_THRESHOLD=0.1

# 质量循环配置
QUALITY_LOOP_MAX_ITERATIONS=3
QUALITY_LOOP_PASS_THRESHOLD=8.0

# ==================== 积分系统 ====================
CREDITS_ENABLED=True
ADMIN_CREDITS_EXEMPT=True
CREDITS_PER_DOLLAR=12400
NEW_USER_GIFT_CREDITS=50000.00
INVITATION_REWARD_CREDITS=50000.00
DAILY_COST_LIMIT_PER_USER=10.0

# ==================== 文件上传 ====================
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads

# ==================== 腾讯云COS（可选）====================
COS_HOST=
COS_SECRET_ID=
COS_SECRET_KEY=
COS_REGION=
COS_BUCKET=
COS_SCHEME=https
COS_PREFIX=uploads

# ==================== 日志配置 ====================
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# ==================== 邮件配置（可选）====================
SMTP_HOST=
SMTP_PORT=465
SMTP_USER=
SMTP_PASSWORD=
SMTP_USE_TLS=True

# ==================== 监控配置（可选）====================
SENTRY_DSN=

# ==================== 管理员账号 ====================
# !!! 重要：请修改密码 !!!
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=请修改为安全密码
```

---

### 3.6 一键部署脚本

创建文件：`deploy.sh`

```bash
#!/bin/bash

# ============================================
# 文枢AI 一键部署脚本
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# 检查是否为root用户
check_root() {
    if [ "$EUID" -ne 0 ]; then
        error "请使用 root 用户运行此脚本: sudo ./deploy.sh"
    fi
}

# 检查并安装Docker
install_docker() {
    if ! command -v docker &> /dev/null; then
        info "正在安装 Docker..."
        curl -fsSL https://get.docker.com | sh
        systemctl start docker
        systemctl enable docker
        success "Docker 安装完成"
    else
        success "Docker 已安装: $(docker --version)"
    fi
}

# 检查并安装Docker Compose
install_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        info "正在安装 Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        success "Docker Compose 安装完成"
    else
        success "Docker Compose 已安装: $(docker-compose --version)"
    fi
}

# 检查配置文件
check_config() {
    info "检查配置文件..."

    if [ ! -f "backend/.env.prod" ]; then
        warning "未找到 backend/.env.prod，正在从模板创建..."
        if [ -f "backend/.env.example" ]; then
            cp backend/.env.example backend/.env.prod
            warning "请编辑 backend/.env.prod 配置文件后重新运行脚本"
            warning "特别注意修改: SECRET_KEY, OPENAI_API_KEY, ADMIN_PASSWORD, CORS_ORIGINS"
            exit 1
        else
            error "未找到 backend/.env.example 模板文件"
        fi
    fi

    if [ ! -f "docker-compose.prod.yml" ]; then
        error "未找到 docker-compose.prod.yml 文件"
    fi

    if [ ! -f "nginx.conf" ]; then
        error "未找到 nginx.conf 文件"
    fi

    if [ ! -f "Dockerfile" ]; then
        error "未找到前端 Dockerfile 文件"
    fi

    success "配置文件检查完成"
}

# 构建并启动服务
deploy() {
    info "开始部署..."

    # 停止旧容器（如果存在）
    info "停止旧容器..."
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true

    # 构建镜像
    info "构建 Docker 镜像（可能需要几分钟）..."
    docker-compose -f docker-compose.prod.yml build --no-cache

    # 启动服务
    info "启动服务..."
    docker-compose -f docker-compose.prod.yml up -d

    # 等待数据库就绪
    info "等待数据库就绪..."
    sleep 10

    # 执行数据库迁移
    info "执行数据库迁移..."
    docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head

    success "部署完成！"
}

# 显示服务状态
show_status() {
    echo ""
    info "服务状态："
    docker-compose -f docker-compose.prod.yml ps
    echo ""
    success "=========================================="
    success "  文枢AI 部署成功！"
    success "=========================================="
    echo ""
    info "访问地址: http://$(curl -s ifconfig.me 2>/dev/null || echo '服务器IP')"
    info "API文档:  http://$(curl -s ifconfig.me 2>/dev/null || echo '服务器IP')/api/v1/docs"
    echo ""
    info "常用命令："
    echo "  查看日志:   docker-compose -f docker-compose.prod.yml logs -f"
    echo "  重启服务:   docker-compose -f docker-compose.prod.yml restart"
    echo "  停止服务:   docker-compose -f docker-compose.prod.yml down"
    echo "  查看状态:   docker-compose -f docker-compose.prod.yml ps"
    echo ""
}

# 主函数
main() {
    echo ""
    echo "============================================"
    echo "       文枢AI 云服务器部署脚本"
    echo "============================================"
    echo ""

    check_root
    install_docker
    install_docker_compose
    check_config
    deploy
    show_status
}

# 执行主函数
main "$@"
```

---

## 4. 详细部署命令

### 4.1 服务器初始化（首次部署）

```bash
# 1. 更新系统
apt update && apt upgrade -y

# 2. 安装必要工具
apt install -y git curl vim

# 3. 上传项目代码（在本地执行）
# 方式一：使用 scp
scp -r ./ai_writer root@你的服务器IP:/root/

# 方式二：使用 git（如果有仓库）
git clone https://github.com/你的用户名/ai_writer.git

# 4. 登录服务器
ssh root@你的服务器IP

# 5. 进入项目目录
cd /root/ai_writer

# 6. 创建必要的配置文件
# （复制上面的配置内容到对应文件）

# 7. 修改配置
vim backend/.env.prod
# 修改: SECRET_KEY, OPENAI_API_KEY, ADMIN_PASSWORD, CORS_ORIGINS

# 8. 执行部署
chmod +x deploy.sh
./deploy.sh
```

### 4.2 常用运维命令

```bash
# 进入项目目录
cd /root/ai_writer

# 查看所有容器状态
docker-compose -f docker-compose.prod.yml ps

# 查看实时日志
docker-compose -f docker-compose.prod.yml logs -f

# 只看后端日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 重启所有服务
docker-compose -f docker-compose.prod.yml restart

# 重启单个服务
docker-compose -f docker-compose.prod.yml restart backend

# 停止所有服务
docker-compose -f docker-compose.prod.yml down

# 停止并删除数据卷（谨慎！会删除数据库）
docker-compose -f docker-compose.prod.yml down -v

# 重新构建并启动
docker-compose -f docker-compose.prod.yml up -d --build

# 进入后端容器
docker exec -it wenshu_backend bash

# 进入数据库
docker exec -it wenshu_postgres psql -U novelaide -d novelaide

# 执行数据库迁移
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# 查看磁盘使用
docker system df

# 清理无用镜像
docker system prune -a
```

### 4.3 数据库备份与恢复

```bash
# 备份数据库
docker exec wenshu_postgres pg_dump -U novelaide novelaide > backup_$(date +%Y%m%d).sql

# 恢复数据库
cat backup_20241216.sql | docker exec -i wenshu_postgres psql -U novelaide -d novelaide

# 自动备份脚本（添加到crontab）
# crontab -e
# 0 2 * * * cd /root/ai_writer && docker exec wenshu_postgres pg_dump -U novelaide novelaide > /root/backups/backup_$(date +\%Y\%m\%d).sql
```

---

## 5. 常见问题

### Q1: 端口被占用
```bash
# 查看端口占用
netstat -tlnp | grep 80

# 停止占用进程
kill -9 进程PID

# 或者修改 docker-compose.prod.yml 中的端口映射
```

### Q2: 数据库连接失败
```bash
# 检查数据库容器状态
docker-compose -f docker-compose.prod.yml logs postgres

# 重启数据库
docker-compose -f docker-compose.prod.yml restart postgres
```

### Q3: 前端页面空白
```bash
# 检查前端构建日志
docker-compose -f docker-compose.prod.yml logs frontend

# 检查 nginx 配置
docker exec wenshu_frontend cat /etc/nginx/conf.d/default.conf
```

### Q4: API 请求失败
```bash
# 检查后端日志
docker-compose -f docker-compose.prod.yml logs backend

# 检查网络连接
docker exec wenshu_frontend ping backend
```

### Q5: 配置 HTTPS（可选）

```bash
# 1. 安装 certbot
apt install -y certbot

# 2. 获取证书
certbot certonly --standalone -d 你的域名.com

# 3. 复制证书到项目
mkdir -p ssl
cp /etc/letsencrypt/live/你的域名.com/fullchain.pem ssl/
cp /etc/letsencrypt/live/你的域名.com/privkey.pem ssl/

# 4. 修改 nginx.conf 添加 HTTPS 配置
# （需要额外配置，这里省略）
```

---

## 6. 服务架构图

```
                    ┌─────────────────┐
                    │     用户访问     │
                    │  http://域名:80  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │     Nginx       │
                    │   (前端+反代)    │
                    │   端口: 80/443   │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
     ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
     │   静态文件   │  │  /api/*     │  │   /ws/*    │
     │  前端 SPA   │  │  后端 API   │  │  WebSocket │
     └─────────────┘  └──────┬──────┘  └──────┬──────┘
                             │                │
                    ┌────────▼────────────────▼┐
                    │      FastAPI 后端        │
                    │       端口: 8000         │
                    └────────┬────────────────┬┘
                             │                │
                    ┌────────▼──────┐  ┌──────▼────────┐
                    │  PostgreSQL   │  │     Redis     │
                    │   端口: 5432  │  │  端口: 6379   │
                    └───────────────┘  └───────────────┘
```

---

## 快速检查清单

部署前请确认：

- [ ] 服务器满足最低配置要求
- [ ] 已修改 `backend/.env.prod` 中的敏感信息
  - [ ] `SECRET_KEY` - 已修改为随机密钥
  - [ ] `OPENAI_API_KEY` - 已填入有效的API密钥
  - [ ] `ADMIN_PASSWORD` - 已修改为安全密码
  - [ ] `CORS_ORIGINS` - 已修改为你的域名
- [ ] 已开放服务器 80 端口
- [ ] 域名已解析到服务器IP（如果使用域名）

---

**部署遇到问题？** 请检查日志：`docker-compose -f docker-compose.prod.yml logs -f`
