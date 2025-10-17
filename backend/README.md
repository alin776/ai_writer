# NovelAIde Backend

AI辅助写小说工具 - 后端 API 服务

## 技术栈

- **框架**: FastAPI 0.109+
- **数据库**: PostgreSQL 15+ + Redis 7+
- **ORM**: SQLAlchemy 2.0 (Async)
- **认证**: JWT (python-jose)
- **AI**: OpenAI API (兼容接口)

## 快速开始

### 1. 安装依赖

```bash
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

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置数据库和其他参数
```

### 3. 启动服务

#### 方式一：直接运行

```bash
# 确保 PostgreSQL 和 Redis 已启动

# 运行应用
python -m app.main

# 或使用 uvicorn
uvicorn app.main:app --reload
```

#### 方式二：使用 Docker Compose（推荐）

```bash
# 启动所有服务（包括数据库）
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

### 4. 访问 API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
backend/
├── app/
│   ├── api/                 # API 路由
│   │   └── v1/
│   │       ├── auth.py     # 认证相关
│   │       ├── users.py    # 用户管理
│   │       ├── works.py    # 作品管理
│   │       └── chapters.py # 章节管理
│   ├── core/               # 核心配置
│   │   ├── config.py       # 配置文件
│   │   ├── database.py     # 数据库配置
│   │   └── security.py     # 安全相关
│   ├── models/             # 数据库模型
│   │   ├── user.py
│   │   ├── work.py
│   │   └── chapter.py
│   ├── schemas/            # Pydantic 模型
│   │   ├── user.py
│   │   ├── work.py
│   │   └── chapter.py
│   ├── services/           # 业务逻辑
│   │   ├── user_service.py
│   │   ├── work_service.py
│   │   └── chapter_service.py
│   └── main.py            # 应用入口
├── alembic/               # 数据库迁移
├── tests/                 # 测试文件
├── requirements.txt       # 依赖列表
├── Dockerfile            # Docker 配置
└── docker-compose.yml    # Docker Compose 配置
```

## API 端点

### 认证
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新 Token

### 用户
- `GET /api/v1/users/me` - 获取当前用户信息
- `PUT /api/v1/users/me` - 更新当前用户信息
- `GET /api/v1/users/{user_id}` - 获取用户信息
- `GET /api/v1/users` - 获取用户列表

### 作品
- `GET /api/v1/works` - 获取作品列表
- `GET /api/v1/works/{work_id}` - 获取作品详情
- `POST /api/v1/works` - 创建作品
- `PUT /api/v1/works/{work_id}` - 更新作品
- `DELETE /api/v1/works/{work_id}` - 删除作品

### 章节
- `GET /api/v1/chapters/work/{work_id}` - 获取作品的章节列表
- `GET /api/v1/chapters/{chapter_id}` - 获取章节详情
- `POST /api/v1/chapters` - 创建章节
- `PUT /api/v1/chapters/{chapter_id}` - 更新章节
- `DELETE /api/v1/chapters/{chapter_id}` - 删除章节
- `POST /api/v1/chapters/reorder` - 重新排序章节

## 数据库迁移

```bash
# 初始化 Alembic
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 开发指南

### 代码规范
- 遵循 PEP 8 规范
- 使用类型注解
- 使用 Black 格式化代码
- 使用 isort 排序导入

### 格式化代码
```bash
# 格式化
black .

# 排序导入
isort .

# 代码检查
flake8

# 类型检查
mypy app
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_users.py

# 查看覆盖率
pytest --cov=app tests/
```

## 常见问题

### 1. 数据库连接失败
确保 PostgreSQL 服务已启动，且 `.env` 中的数据库配置正确。

### 2. Redis 连接失败
确保 Redis 服务已启动，且 `.env` 中的 Redis URL 正确。

### 3. JWT Token 验证失败
检查 `SECRET_KEY` 是否正确配置。

## 许可证

MIT License
