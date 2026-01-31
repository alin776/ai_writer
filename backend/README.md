# NovelAIde Backend

AI辅助写小说工具 - 后端 API 服务

## 技术栈

- **框架**: FastAPI 0.109+
- **数据库**: PostgreSQL 15+ (with pgvector) + Redis 7+
- **ORM**: SQLAlchemy 2.0 (Async)
- **认证**: JWT (python-jose)
- **AI**: OpenAI API (兼容接口)
- **向量数据库**: pgvector + sentence-transformers (小说分析功能)

## 快速开始

### 方式一：一键安装（推荐）⭐

```bash
# Windows用户
双击运行 setup.bat

# 或在命令行中运行
.\setup.bat
```

`setup.bat` 会自动完成以下步骤：
1. ✅ 检查Python和PostgreSQL环境
2. ✅ 创建虚拟环境
3. ✅ 安装Python依赖
4. ✅ 可选安装向量数据库依赖（小说分析功能需要）
5. ✅ 配置环境变量
6. ✅ 初始化数据库
7. ✅ 创建必要的目录

### 方式二：手动安装

#### 1. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装核心依赖
pip install -r requirements.txt

# 可选：安装向量数据库依赖（小说分析功能）
pip install pgvector sentence-transformers
```

#### 2. 安装pgvector扩展（小说分析功能需要）

⚠️ **重要**：如需使用小说分析功能，必须在PostgreSQL中安装pgvector扩展

**安装指南**（按推荐顺序）：
1. 📄 [安装pgvector扩展步骤.txt](./安装pgvector扩展步骤.txt) - 标准步骤（推荐）⭐
2. 📖 [INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md) - 完整文档

**概要步骤**：
1. 安装编译工具（Visual Studio Build Tools）
2. 编译安装pgvector
3. 重启PostgreSQL
4. 启用扩展：`CREATE EXTENSION vector;`

⚠️ 详细步骤请查看上述文档

#### 3. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置数据库和其他参数
```

### 4. 启动服务

#### 方式一：快速启动脚本（推荐）⭐

```bash
# Windows用户
双击运行 quick_start.bat

# 或在命令行中运行
.\quick_start.bat
```

#### 方式二：手动启动

```bash
# 确保 PostgreSQL 已启动

# 激活虚拟环境
venv\Scripts\activate

# 运行应用
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 方式三：使用 Docker Compose

```bash
# 启动所有服务（包括数据库）
docker-compose up -d

# 查看日志
docker-compose logs -f backend

# 停止服务
docker-compose down
```

### 5. 访问 API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs （推荐，可在线测试）
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

### 小说分析（需要pgvector扩展）
- `POST /api/v1/analysis/works/{work_id}/start` - 触发小说分析
- `GET /api/v1/analysis/works/{work_id}/status` - 获取分析状态
- `GET /api/v1/analysis/works/{work_id}/result` - 获取分析结果
- `DELETE /api/v1/analysis/works/{work_id}` - 删除分析

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

## 环境检查工具

遇到问题时，运行环境检查脚本：

```bash
# Windows
.\check_env.bat
```

会自动检查：
- Python版本
- PostgreSQL连接
- 环境变量配置
- 依赖包安装情况

## 常见问题

### 1. setup.bat运行失败
- 确保以管理员身份运行（如需安装服务）
- 检查Python是否在PATH中
- 查看错误信息，按提示操作

### 2. 数据库连接失败
- 确保 PostgreSQL 服务已启动
- 运行 `psql --version` 检查PostgreSQL是否安装
- 检查 `.env` 中的 `DATABASE_URL` 配置
- 确保数据库 `novelaide` 已创建

### 3. pgvector扩展相关错误
```
extension "vector" is not available
```
说明未安装pgvector扩展，参考：
- [INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md)
- [安装pgvector扩展步骤.txt](./安装pgvector扩展步骤.txt)

### 4. 向量数据库依赖安装失败
如果在setup.bat中跳过了向量依赖安装，可稍后手动安装：
```bash
.\install_vector_dependencies.bat
```

### 5. JWT Token 验证失败
检查 `.env` 中的 `SECRET_KEY` 是否正确配置

### 6. 小说分析功能无法使用
需要同时满足：
- ✅ 安装 pgvector Python包
- ✅ 安装 sentence-transformers
- ✅ PostgreSQL中安装并启用pgvector扩展

## 🎯 快速脚本参考

| 脚本 | 用途 | 何时使用 |
|------|------|----------|
| `setup.bat` | 一键安装配置 | 首次安装时 |
| `quick_start.bat` | 快速启动服务器 | 每天开发时 |
| `check_env.bat` | 环境检查 | 遇到问题时 |
| `restart_server.bat` | 重启服务器 | 修改代码后 |
| `install_vector_dependencies.bat` | 安装向量依赖 | 需要小说分析功能时 |

## 📚 相关文档

- 📖 [START_HERE.md](./START_HERE.md) - 快速开始指南
- 📘 [docs/](./docs/) - 完整文档目录
- 🔧 [INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md) - pgvector安装指南
- 📄 [安装向量数据库依赖.txt](./安装向量数据库依赖.txt) - 向量依赖安装

## 许可证

MIT License
