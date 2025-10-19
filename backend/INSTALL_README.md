# 🚀 NovelAIde Backend 安装指南

完整的安装步骤和说明

---

## 📋 目录

1. [前置要求](#前置要求)
2. [一键安装](#一键安装-推荐)
3. [手动安装](#手动安装)
4. [小说分析功能安装](#小说分析功能安装可选)
5. [验证安装](#验证安装)
6. [常见问题](#常见问题)

---

## 前置要求

### 必须安装

✅ **Python 3.8+**
```cmd
python --version
```
如果没有：https://www.python.org/downloads/

✅ **PostgreSQL 15+**
```cmd
psql --version
```
如果没有：https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe

### 可选安装（小说分析功能）

🔧 **Build Tools for Visual Studio**（pgvector编译需要）
- 下载：https://aka.ms/vs/17/release/vs_BuildTools.exe
- 安装时勾选："使用C++的桌面开发"

🔧 **Git for Windows**（pgvector下载需要）
- 下载：https://git-scm.com/download/win

---

## 一键安装（推荐）⭐

### 步骤

1. **打开命令提示符（CMD）**
   - 进入backend目录
   ```cmd
   cd C:\Users\Administrator\Desktop\ai-writer\backend
   ```

2. **运行安装脚本**
   ```cmd
   setup.bat
   ```

3. **按照提示操作**
   - 检查Python和PostgreSQL环境 ✅
   - 自动创建虚拟环境 ✅
   - 安装Python依赖 ✅
   - **询问是否安装向量依赖**：
     - 选择 `Y`：安装小说分析功能依赖（约500MB，需5-10分钟）
     - 选择 `N`：跳过（可稍后手动安装）
   - 配置环境变量 ✅
   - **询问数据库是否已创建**：
     - 选择 `Y`：继续初始化数据库
     - 选择 `N`：查看提示创建数据库
   - 初始化数据库表 ✅

4. **完成**
   ```
   ========================================
      安装完成！
   ========================================
   ```

### 安装后配置

1. **编辑 .env 文件**
   - 配置 `OPENAI_API_KEY`（必须）
   - 检查 `DATABASE_URL`
   
2. **如需小说分析功能，安装pgvector扩展**
   - 参考：[INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md)
   - 或：[安装pgvector扩展步骤.txt](./安装pgvector扩展步骤.txt)

---

## 手动安装

### 1. 创建虚拟环境

```cmd
python -m venv venv
```

### 2. 激活虚拟环境

```cmd
venv\Scripts\activate
```

### 3. 安装核心依赖

```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. 安装向量依赖（可选）

```cmd
pip install pgvector sentence-transformers
```

⚠️ 这些包较大（约500MB），需要5-10分钟

### 5. 配置环境变量

```cmd
copy .env.example .env
notepad .env
```

编辑以下配置：
- `SECRET_KEY`：JWT密钥
- `DATABASE_URL`：PostgreSQL连接字符串
- `OPENAI_API_KEY`：OpenAI API密钥（必须）

### 6. 创建数据库

```cmd
psql -U postgres
```

```sql
CREATE DATABASE novelaide;
CREATE USER novelaide WITH PASSWORD 'novelaide_password';
GRANT ALL PRIVILEGES ON DATABASE novelaide TO novelaide;
```

### 7. 运行数据库迁移

```cmd
python -m alembic upgrade head
```

### 8. 创建必要目录

```cmd
mkdir uploads
mkdir logs
```

---

## 小说分析功能安装（可选）

### 为什么需要？

小说分析功能提供：
- 📊 章节级微观分析（人物、事件、时间线）
- 📈 全局宏观分析（人物成长、世界观、矛盾演变）
- 🔍 向量相似度搜索（RAG检索）

### 安装步骤

#### 1. 安装Python依赖

如果setup.bat时跳过了，可运行：

```cmd
install_vector_dependencies.bat
```

或手动安装：
```cmd
venv\Scripts\activate
pip install pgvector sentence-transformers
```

#### 2. 安装pgvector扩展（系统级）

**这是关键步骤！** pgvector是PostgreSQL的扩展，需要编译安装。

**详细指南**：
- 📖 [INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md) - 完整文档
- 📄 [安装pgvector扩展步骤.txt](./安装pgvector扩展步骤.txt) - 快速参考

**快速步骤**：

1. 安装 Build Tools for Visual Studio
   - https://aka.ms/vs/17/release/vs_BuildTools.exe
   - 勾选："使用C++的桌面开发"

2. 以管理员身份打开 "x64 Native Tools Command Prompt for VS"

3. 编译安装pgvector
   ```cmd
   set "PGROOT=C:\Program Files\PostgreSQL\16"
   cd %TEMP%
   git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
   cd pgvector
   nmake /F Makefile.win
   nmake /F Makefile.win install
   ```

4. 重启PostgreSQL
   ```cmd
   net stop postgresql-x64-16
   net start postgresql-x64-16
   ```

5. 在数据库中启用
   ```cmd
   psql -U postgres -d novelaide
   ```
   ```sql
   CREATE EXTENSION vector;
   ```

6. 运行数据库迁移
   ```cmd
   cd C:\Users\Administrator\Desktop\ai-writer\backend
   venv\Scripts\python.exe -m alembic upgrade head
   ```

---

## 验证安装

### 1. 检查环境

```cmd
check_env.bat
```

### 2. 启动服务

```cmd
quick_start.bat
```

或手动启动：
```cmd
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

### 3. 访问API文档

打开浏览器：http://localhost:8000/docs

如果能看到Swagger UI，说明安装成功！✅

### 4. 测试小说分析功能（如果已安装）

在数据库中检查pgvector扩展：
```cmd
psql -U postgres -d novelaide
```
```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

如果有一行结果，说明pgvector扩展已启用！✅

---

## 常见问题

### Q1: setup.bat运行失败

**A**: 
- 确保Python已安装并在PATH中
- 确保PostgreSQL已安装
- 查看错误信息，按提示操作

### Q2: 数据库连接失败

**A**:
1. 检查PostgreSQL服务是否运行：
   ```cmd
   net start postgresql-x64-16
   ```
2. 检查数据库是否已创建：
   ```cmd
   psql -U postgres -l
   ```
3. 检查.env中的DATABASE_URL配置

### Q3: alembic upgrade head 失败，提示 "extension vector is not available"

**A**: 
说明pgvector扩展未安装，参考：
- [INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md)
- [安装pgvector扩展步骤.txt](./安装pgvector扩展步骤.txt)

### Q4: 向量依赖安装超时

**A**:
sentence-transformers包含PyTorch，约500MB：
- 使用稳定的网络
- 或使用国内镜像：
  ```cmd
  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pgvector sentence-transformers
  ```

### Q5: 找不到 "x64 Native Tools Command Prompt"

**A**:
说明Visual Studio编译工具未安装：
- 下载：https://aka.ms/vs/17/release/vs_BuildTools.exe
- 安装时勾选："使用C++的桌面开发"

### Q6: nmake 编译失败

**A**:
1. 检查PGROOT路径是否正确
2. 检查PostgreSQL版本号是否匹配
3. 确保以管理员身份运行

---

## 📚 相关文档

- 📖 [README.md](./README.md) - 项目概览
- 📘 [START_HERE.md](./START_HERE.md) - 快速开始
- 🔧 [INSTALL_PGVECTOR_EXTENSION.md](./INSTALL_PGVECTOR_EXTENSION.md) - pgvector安装
- 📄 [安装向量数据库依赖.txt](./安装向量数据库依赖.txt) - 快速参考

---

**安装顺利！🎉**
