# NovelAIde 后端一键部署包

## 📦 给前端开发者

这是一个完整的后端部署包，让你在 **5-10 分钟内**快速运行起后端服务，无需复杂配置。

### 🚀 三步启动

```bash
1. 进入 backend 目录
2. 双击 setup.bat（首次运行）
3. 双击 quick_start.bat
```

### 📖 必读文档

- **backend/docs/前端开发者指南.md** ⭐⭐⭐（导航页，从这里开始）
- **backend/docs/QUICK_START_FOR_FRONTEND.md** ⭐⭐⭐（快速启动）
- **backend/docs/API_REFERENCE.md** ⭐⭐⭐（完整 API 文档）
- **backend/docs/API_QUICK_REFERENCE.md** ⭐⭐（速查表）

**所有文档位于**：`backend/docs/` 目录，查看 `backend/docs/README.md` 获取完整索引

## 📁 目录结构

```
ai_writer/
├── backend/                               # 后端目录
│   ├── docs/                             # 📚 所有文档目录
│   │   ├── README.md                     # 📍 文档索引（从这里开始）
│   │   ├── 前端开发者指南.md             # 导航页
│   │   ├── QUICK_START_FOR_FRONTEND.md   # 快速启动
│   │   ├── POSTGRESQL_SETUP.md           # 数据库安装
│   │   ├── API_REFERENCE.md              # API 完整文档
│   │   ├── API_QUICK_REFERENCE.md        # API 速查表
│   │   ├── CONFIG_GUIDE.md               # 配置指南
│   │   ├── DATABASE_SCHEMA.md            # 数据库结构
│   │   ├── 数据库配置说明.md             # 数据库配置
│   │   └── 一键部署包说明.md             # 部署说明
│   │
│   ├── app/                              # 源代码
│   │   ├── api/                          # API 路由
│   │   ├── core/                         # 核心配置
│   │   ├── models/                       # 数据模型
│   │   ├── schemas/                      # 数据验证
│   │   └── services/                     # 业务逻辑
│   │
│   ├── 🚀 setup.bat                      # ⭐ 一键安装脚本
│   ├── 🚀 quick_start.bat                # ⭐ 快速启动脚本
│   ├── 🔍 check_env.bat                  # ⭐ 环境检查脚本
│   ├── 📍 START_HERE.md                  # 快速开始指南
│   │
│   ├── .env.example                      # 环境变量模板
│   ├── requirements.txt                  # Python 依赖
│   └── README.md                         # 项目README
│
├── DEPLOYMENT_PACKAGE_README.md          # 📍 当前文件
└── [其他项目文件]
```

## 🎯 快速开始

### 前置要求

- ✅ Python 3.8 或更高版本
- ✅ PostgreSQL 15+
  - 下载：https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe
  - 安装指南：backend/POSTGRESQL_SETUP.md
- ✅ 20 分钟时间（含 PostgreSQL 安装）

**不需要**：
- ❌ Redis（可选）
- ❌ Docker（可选）

### 安装步骤

#### 1️⃣ 运行安装脚本

```bash
cd backend
setup.bat
```

脚本会自动：
- 检查 Python 环境
- 创建虚拟环境
- 安装所有依赖
- 配置环境变量
- 初始化数据库

#### 2️⃣ 配置 API Key

编辑 `backend/.env` 文件：

```bash
OPENAI_API_KEY=your-real-api-key-here  # ⚠️ 必须修改
```

#### 3️⃣ 启动服务

```bash
quick_start.bat
```

访问：
- 🌐 API 服务：http://localhost:8000
- 📖 API 文档：http://localhost:8000/docs

## ✨ 已配置功能

- ✅ 用户认证（JWT）
- ✅ 作品管理（CRUD）
- ✅ 章节管理（CRUD）
- ✅ AI 写作辅助（OpenAI）
- ✅ 文件上传
- ✅ CORS 跨域（前端友好）
- ✅ API 文档（Swagger）
- ✅ 错误处理
- ✅ 日志记录

## 📚 文档指南

### 不同角色看什么文档

| 角色 | 推荐文档 | 说明 |
|------|---------|------|
| 前端开发者 | `QUICK_START_FOR_FRONTEND.md` | 5分钟快速上手 |
| 需要修改配置 | `CONFIG_GUIDE.md` | 详细配置说明 |
| 后端开发者 | `backend/README.md` | 完整技术文档 |
| 第一次接触项目 | `一键部署包说明.md` | 部署包概览 |

## 🔧 默认配置

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| 服务地址 | http://localhost:8000 | 后端 API 地址 |
| 数据库 | PostgreSQL (novelaide) | 需要手动创建 |
| 数据库用户 | novelaide / novelaide_password | 配置在 setup_db.sql |
| 日志目录 | backend/logs/ | 自动创建 |
| 上传目录 | backend/uploads/ | 自动创建 |
| 允许跨域 | localhost:5173, :3000 | Vite/React |

## 🛠️ 工具脚本说明

### setup.bat（一键安装）
- 检查 Python 环境
- 创建虚拟环境
- 安装依赖包
- 配置环境变量
- 初始化数据库
- **只需运行一次**

### quick_start.bat（快速启动）
- 激活虚拟环境
- 检查配置
- 启动开发服务器
- 支持热重载
- **日常使用**

### check_env.bat（环境检查）
- 检查 Python
- 检查虚拟环境
- 检查配置文件
- 检查数据库
- 检查依赖包
- **遇到问题时运行**

## 🚨 常见问题

### 启动失败？

```bash
# 1. 检查环境
check_env.bat

# 2. 查看错误信息（终端输出）

# 3. 重新安装
setup.bat
```

### 端口被占用？

修改 `backend/.env`：
```bash
PORT=8001  # 改为其他端口
```

### API Key 未配置？

编辑 `backend/.env`：
```bash
OPENAI_API_KEY=sk-xxxxx  # 填入真实的 Key
```

### 数据库问题？

```bash
# 删除数据库文件，重新启动会自动创建
del backend\novelaide.db
quick_start.bat
```

## 📖 API 文档

**完整的 API 接口文档**：`backend/docs/API_REFERENCE.md` ⭐⭐⭐

包含：
- 所有接口的详细说明
- 请求参数和响应格式
- 数据模型定义
- 错误码说明
- JavaScript/TypeScript 使用示例
- Axios 封装示例

## 📖 API 快速示例

### 1. 注册用户

```bash
POST http://localhost:8000/api/v1/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### 2. 登录获取 Token

```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

### 3. 使用 Token 访问 API

```bash
GET http://localhost:8000/api/v1/users/me
Authorization: Bearer {your-token-here}
```

**更多示例**：访问 http://localhost:8000/docs 在线测试所有接口！

## 🔐 安全提醒

- ⚠️ `.env` 文件包含敏感信息，不要提交到 Git
- ⚠️ `OPENAI_API_KEY` 要保密
- ⚠️ 生产环境必须修改 `SECRET_KEY`
- ⚠️ 生产环境建议使用 PostgreSQL

## 📞 获取帮助

### 自助排查
1. 运行 `check_env.bat` 检查环境
2. 查看终端输出的错误信息
3. 查看 `backend/logs/app.log` 日志
4. 访问 http://localhost:8000/docs 测试接口

### 查看文档
- `QUICK_START_FOR_FRONTEND.md` - 快速入门
- `CONFIG_GUIDE.md` - 配置说明
- `backend/README.md` - 完整文档

### 联系开发者
如果以上方法都无法解决，请联系后端开发者并提供：
- 错误信息（终端输出）
- 日志文件（logs/app.log）
- 运行环境（Python 版本等）

## 🎉 开始开发

```bash
# 进入后端目录
cd backend

# 首次运行（约10分钟）
setup.bat

# 配置 API Key
notepad .env

# 启动服务（约10秒）
quick_start.bat

# 访问文档
# http://localhost:8000/docs
```

祝开发顺利！🚀
