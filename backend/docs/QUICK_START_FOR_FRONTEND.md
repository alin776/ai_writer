# NovelAIde 后端快速启动指南（前端开发者版）

> 这是一份专为前端开发者准备的快速启动指南，帮助你在5分钟内运行起后端服务。

## 📋 前置要求

- **Python 3.8+** （[下载地址](https://www.python.org/downloads/)）
- **10分钟** 的时间

**需要安装**：
- ✅ PostgreSQL 15+（必须）
  - 下载：https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe
  - 详细安装指南：[POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md)

**不需要**：
- ❌ 不需要安装 Redis（可选功能）
- ❌ 不需要 Docker（虽然支持，但不必要）

## 🚀 快速开始（3步）

### 第1步：安装配置（只需一次）

双击运行 `setup.bat`，脚本会自动：
- ✅ 检查 Python 环境
- ✅ 创建虚拟环境
- ✅ 安装所有依赖包
- ✅ 配置环境变量
- ✅ 初始化数据库

```bash
# 或者在命令行运行
setup.bat
```

**注意**：安装依赖包可能需要 3-5 分钟，请耐心等待。

### 第2步：安装和配置 PostgreSQL（必须）

#### 安装 PostgreSQL

下载并安装：https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe

**重要**：安装过程中设置的超级用户密码请记住！

详细安装步骤请查看：[POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md)

#### 创建数据库

打开命令行，运行：

```bash
# 进入 backend 目录
cd backend

# 运行数据库初始化脚本
psql -U postgres -f setup_db.sql
# 输入安装时设置的超级用户密码
```

或者手动创建：

```bash
# 连接到 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE novelaide;

# 创建用户
CREATE USER novelaide WITH PASSWORD 'novelaide_password';

# 授权
GRANT ALL PRIVILEGES ON DATABASE novelaide TO novelaide;
\c novelaide
GRANT ALL PRIVILEGES ON SCHEMA public TO novelaide;

# 退出
\q
```

### 第3步：配置 API Key（必须）

编辑 `.env` 文件：

```bash
# 找到这一行并修改
OPENAI_API_KEY=your-openai-api-key  # ⚠️ 必须修改为真实的 API Key

# 数据库配置（如果修改了密码，需要同步修改）
DATABASE_URL=postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide
```

如果没有 OpenAI API Key，可以：
- 使用兼容接口（如 Azure OpenAI、国内代理等）
- 联系后端开发者获取测试用的 Key

### 第4步：启动服务

双击运行 `quick_start.bat`：

```bash
# 或者在命令行运行
quick_start.bat
```

看到以下信息表示启动成功：

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**访问地址**：
- 🌐 API 服务：http://localhost:8000
- 📖 API 文档：http://localhost:8000/docs （可以在这里测试所有接口）
- 📄 备用文档：http://localhost:8000/redoc

## 🔍 遇到问题？

### 检查环境

运行环境检查工具：

```bash
check_env.bat
```

这会检查所有必要的配置和依赖。

### 常见问题

#### 1. 启动时报错 "ModuleNotFoundError"

**解决方法**：重新运行 `setup.bat` 安装依赖

#### 2. 端口 8000 被占用

**解决方法**：修改 `quick_start.bat`，将 `--port 8000` 改为其他端口（如 8001）

#### 3. 数据库连接失败

**解决方法**：
- 检查 PostgreSQL 服务是否运行：`net start postgresql-x64-15`
- 检查数据库是否已创建：查看 [POSTGRESQL_SETUP.md](./POSTGRESQL_SETUP.md)
- 检查 `.env` 中的数据库配置是否正确

#### 4. API 调用返回 401/403

**解决方法**：检查是否已登录，某些接口需要先调用 `/api/v1/auth/login` 获取 token

## 📚 API 使用说明

**完整的 API 接口文档请查看：[API_REFERENCE.md](./API_REFERENCE.md)** ⭐

这里只列出常用的快速示例，详细的接口参数、响应格式、错误码等请查看完整文档。

### 认证流程

1. **注册账号**：`POST /api/v1/auth/register`

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

2. **登录获取 Token**：`POST /api/v1/auth/login`

```json
{
  "username": "testuser",
  "password": "password123"
}
```

返回：
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

3. **使用 Token 调用接口**

在请求头中添加：
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### 主要接口

| 功能 | 方法 | 路径 | 需要认证 |
|------|------|------|----------|
| 用户注册 | POST | `/api/v1/auth/register` | ❌ |
| 用户登录 | POST | `/api/v1/auth/login` | ❌ |
| 获取当前用户 | GET | `/api/v1/users/me` | ✅ |
| 获取作品列表 | GET | `/api/v1/works` | ✅ |
| 创建作品 | POST | `/api/v1/works` | ✅ |
| 获取章节列表 | GET | `/api/v1/chapters/work/{work_id}` | ✅ |
| 创建章节 | POST | `/api/v1/chapters` | ✅ |

**提示**：访问 http://localhost:8000/docs 可以在线测试所有接口！

## 📁 项目结构（供参考）

```
backend/
├── app/                    # 应用源码
│   ├── api/               # API 路由
│   ├── core/              # 核心配置
│   ├── models/            # 数据库模型
│   ├── schemas/           # 数据验证模型
│   └── services/          # 业务逻辑
├── venv/                  # Python 虚拟环境（自动创建）
├── novelaide.db           # SQLite 数据库（自动创建）
├── .env                   # 环境变量配置
├── requirements.txt       # Python 依赖
├── setup.bat              # 一键安装脚本 ⭐
├── quick_start.bat        # 一键启动脚本 ⭐
└── check_env.bat          # 环境检查脚本 ⭐
```

## 🔧 配置说明

### .env 文件（重要配置）

```bash
# 必须配置
OPENAI_API_KEY=your-openai-api-key    # OpenAI API 密钥（必须）

# 可选配置（一般不需要改）
PORT=8000                              # 服务端口
DEBUG=True                             # 调试模式
SECRET_KEY=auto-generated              # JWT 密钥（已自动生成）
DATABASE_URL=sqlite+aiosqlite:///./novelaide.db  # 数据库
```

### CORS 配置

默认允许的前端地址：
- http://localhost:5173 （Vite 默认端口）
- http://localhost:3000 （React/Next.js 默认端口）

如果你的前端使用其他端口，需要在 `.env` 中添加：

```bash
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000","http://localhost:5174"]
```

## 💡 开发技巧

### 1. 查看数据库内容

推荐使用 PostgreSQL 客户端：
- [pgAdmin 4](https://www.pgadmin.org/) （自带在 PostgreSQL 安装包中）
- [DBeaver](https://dbeaver.io/) （免费，功能强大）
- [DataGrip](https://www.jetbrains.com/datagrip/) （付费，专业）

### 2. 实时日志

启动服务器时会显示所有 API 请求日志，方便调试。

### 3. 自动重载

服务器运行在 `--reload` 模式，修改代码后会自动重启（约1秒）。

### 4. 测试数据

首次使用可以创建测试账号：
- 用户名：`demo`
- 邮箱：`demo@example.com`
- 密码：`demo123456`

## 📞 获取帮助

如果遇到问题：

1. **查看日志**：服务器终端会显示详细错误信息
2. **查看文档**：http://localhost:8000/docs
3. **检查环境**：运行 `check_env.bat`
4. **联系后端开发者**

## 🎯 下一步

- ✅ 后端服务运行成功
- ✅ 能访问 API 文档
- ✅ 了解认证流程
- 📌 开始开发前端功能！

祝开发顺利！🚀
