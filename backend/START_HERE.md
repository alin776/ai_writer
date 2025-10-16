# 🚀 NovelAIde Backend - 从这里开始

> **欢迎！** 这是一个快速启动指南，帮助你快速上手。

## 📖 完整文档

**所有文档已整理到 `docs/` 目录**，请查看：

👉 **[docs/README.md](./docs/README.md)** - 文档中心索引（推荐从这里开始）

## ⚡ 快速启动（3步）

### 1️⃣ 安装 PostgreSQL
下载：https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe

详细步骤：[docs/POSTGRESQL_SETUP.md](./docs/POSTGRESQL_SETUP.md)

### 2️⃣ 运行安装脚本
```bash
双击 setup.bat
```

### 3️⃣ 启动服务
```bash
双击 quick_start.bat
```

## 📚 常用文档快速链接

### 给前端开发者
- 📘 [前端开发者指南](./docs/前端开发者指南.md) - 导航页
- 🚀 [快速启动指南](./docs/QUICK_START_FOR_FRONTEND.md) - 5分钟上手
- 📡 [API 完整文档](./docs/API_REFERENCE.md) - 所有接口
- 📋 [API 速查表](./docs/API_QUICK_REFERENCE.md) - 打印备查

### 数据库相关
- 🐘 [PostgreSQL 安装](./docs/POSTGRESQL_SETUP.md) - 安装指南
- 💾 [数据库配置](./docs/数据库配置说明.md) - 配置说明
- 📊 [数据库表结构](./docs/DATABASE_SCHEMA.md) - 表结构

### 配置相关
- ⚙️ [配置指南](./docs/CONFIG_GUIDE.md) - 环境变量配置
- 📦 [部署说明](./docs/一键部署包说明.md) - 部署包说明

## 🛠️ 核心脚本

| 脚本 | 用途 | 使用频率 |
|------|------|----------|
| `setup.bat` | 一键安装配置 | 只用一次 |
| `quick_start.bat` | 快速启动服务器 | 每天使用 |
| `check_env.bat` | 检查环境配置 | 遇到问题时 |

## 🌐 重要地址

- API 服务：http://localhost:8000
- API 文档：http://localhost:8000/docs （可在线测试）

## 🆘 遇到问题？

1. 查看 [docs/QUICK_START_FOR_FRONTEND.md](./docs/QUICK_START_FOR_FRONTEND.md) 的"常见问题"
2. 运行 `check_env.bat` 检查环境
3. 查看 [docs/README.md](./docs/README.md) 找到对应文档

## 📂 目录结构

```
backend/
├── docs/                    # 📚 所有文档（从这里开始）
│   ├── README.md           # 文档索引
│   ├── 前端开发者指南.md   # 导航页
│   └── ...                 # 其他文档
│
├── app/                     # 应用源码
├── setup.bat               # 一键安装脚本
├── quick_start.bat         # 快速启动脚本
└── START_HERE.md          # 📍 当前文件
```

---

**👉 下一步：查看 [docs/README.md](./docs/README.md) 或 [docs/前端开发者指南.md](./docs/前端开发者指南.md)**

祝开发顺利！🎉
