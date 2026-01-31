# AI 写作助手 - 超详细部署教程

## 📋 部署前的准备工作

### 你需要准备的信息:
- ✅ 服务器 IP 地址: `_____________`
- ✅ 服务器 SSH 密码: `_____________`
- ✅ 域名: `_____________` (例如: www.example.com)
- ✅ 宝塔面板地址: `http://你的IP:8888`
- ✅ 宝塔面板账号密码: `_____________`
- ✅ OpenAI API Key: `_____________`

---

# 第一部分: 通过宝塔面板安装必要软件

## 步骤 1: 登录宝塔面板

1. 打开浏览器,访问: `http://你的服务器IP:8888`
2. 输入宝塔面板的用户名和密码
3. 登录成功后,你会看到宝塔面板的主界面

---

## 步骤 2: 安装 PostgreSQL 数据库

### 2.1 打开软件商店
1. 在宝塔面板左侧菜单,点击 **"软件商店"**
2. 在搜索框中输入: `PostgreSQL`

### 2.2 安装 PostgreSQL
1. 找到 **"PostgreSQL 15.x"** (或更高版本)
2. 点击右侧的 **"安装"** 按钮
3. 在弹出的对话框中,点击 **"确定"**
4. 等待安装完成 (大约 3-5 分钟)
5. 安装完成后,会显示 **"已安装"**

### 2.3 配置 PostgreSQL
1. 点击 PostgreSQL 右侧的 **"设置"** 按钮
2. 记下默认的端口号: `5432`
3. 点击 **"root 密码"** 标签,设置一个强密码,例如: `YourStrong_PG_Password123`
4. 记下这个密码,后面会用到!
5. 点击 **"确定"** 保存

---

## 步骤 3: 安装 Redis

### 3.1 搜索 Redis
1. 在软件商店搜索框中输入: `Redis`
2. 找到 **"Redis"** (版本 6.x 或 7.x)

### 3.2 安装 Redis
1. 点击右侧的 **"安装"** 按钮
2. 点击 **"确定"**
3. 等待安装完成 (大约 1-2 分钟)
4. 安装完成后,显示 **"已安装"**

### 3.3 启动 Redis
1. 点击 Redis 右侧的 **"设置"** 按钮
2. 确保 **"服务状态"** 显示为 **"运行中"**
3. 如果没有运行,点击 **"启动"** 按钮

---

## 步骤 4: 安装 Python 3.11

### 4.1 安装 Python 项目管理器
1. 在软件商店搜索: `Python项目管理器`
2. 找到 **"Python项目管理器"**
3. 点击 **"安装"**
4. 等待安装完成

### 4.2 安装 Python 3.11 版本
1. 安装完成后,点击 **"设置"**
2. 点击 **"版本管理"** 标签
3. 在列表中找到 **"Python 3.11"**
4. 如果没有安装,点击 **"安装"** 按钮
5. 等待安装完成 (大约 5-10 分钟)

---

## 步骤 5: 安装 Node.js

### 5.1 安装 PM2 管理器
1. 在软件商店搜索: `PM2`
2. 找到 **"PM2 管理器"**
3. 点击 **"安装"**
4. 这会自动安装 Node.js 和 PM2
5. 等待安装完成 (大约 3-5 分钟)

### 5.2 验证安装
1. 安装完成后,点击 **"设置"**
2. 可以看到 Node.js 的版本信息

**版本要求:** Node.js 14.x 或更高版本都可以
- ✅ 推荐: 16.x, 18.x, 20.x
- ✅ 最低: 14.x
- ❌ 不支持: 12.x 及以下

---

## 步骤 6: 安装 Supervisor (进程守护)

1. 在软件商店搜索: `Supervisor`
2. 找到 **"Supervisor 管理器"**
3. 点击 **"安装"**
4. 等待安装完成

---

# 第二部分: 创建数据库和用户

## 步骤 7: 使用 SSH 连接服务器

### 7.1 使用 Windows 自带的 PowerShell (推荐)
1. 按 `Win + R` 打开运行对话框
2. 输入 `powershell` 并回车
3. 在 PowerShell 中输入:
```powershell
ssh root@你的服务器IP
```
4. 第一次连接会提示: `Are you sure you want to continue connecting?`
5. 输入 `yes` 并回车
6. 输入服务器的 root 密码
7. 登录成功!

### 7.2 或者使用宝塔面板的终端
1. 在宝塔面板左侧菜单,点击 **"终端"**
2. 点击 **"打开终端"**
3. 直接进入命令行界面

---

## 步骤 8: 创建 PostgreSQL 数据库

### 8.1 切换到 postgres 用户
在终端中依次输入以下命令:

```bash
# 切换到 postgres 用户
sudo -u postgres psql
```

你会看到提示符变成: `postgres=#`

### 8.2 创建数据库和用户
**依次复制以下每一行命令,粘贴到终端并回车:**

```sql
-- 创建数据库
CREATE DATABASE novelaide;
```
看到 `CREATE DATABASE` 表示成功

```sql
-- 创建用户 (请修改密码!)
CREATE USER novelaide WITH PASSWORD 'YourStrong_DB_Password123';
```
看到 `CREATE ROLE` 表示成功

```sql
-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE novelaide TO novelaide;
```
看到 `GRANT` 表示成功

```sql
-- 切换到 novelaide 数据库
\c novelaide
```
看到 `You are now connected to database "novelaide"` 表示成功

```sql
-- 启用 pgvector 扩展 (用于 AI 向量存储)
CREATE EXTENSION IF NOT EXISTS vector;
```
看到 `CREATE EXTENSION` 表示成功

```sql
-- 授予 schema 权限
GRANT ALL ON SCHEMA public TO novelaide;
```
看到 `GRANT` 表示成功

```sql
-- 退出
\q
```

### 8.3 记录数据库信息
**请把这些信息记录下来,后面配置时需要用到:**
- 数据库名: `novelaide`
- 用户名: `novelaide`
- 密码: `131457` (你刚才设置的密码)
- 主机: `localhost`
- 端口: `5432`

---

# 第三部分: 上传项目文件到服务器

## 步骤 9: 创建项目目录

### 9.1 在终端中创建目录
```bash
# 创建项目目录
mkdir -p /www/wwwroot/ai-writer

# 进入目录
cd /www/wwwroot/ai-writer

# 查看当前路径
pwd
```
应该显示: `/www/wwwroot/ai-writer`

---

## 步骤 10: 上传项目文件

### 方法 1: 使用宝塔面板上传 (最简单)

#### 10.1 压缩本地项目
1. 在你的 Windows 电脑上,找到项目文件夹: `C:\Users\Administrator\Desktop\ai-writer`
2. 右键点击 `ai-writer` 文件夹
3. 选择 **"发送到"** -> **"压缩(zipped)文件夹"**
4. 会生成 `ai-writer.zip` 文件

#### 10.2 通过宝塔面板上传
1. 在宝塔面板左侧菜单,点击 **"文件"**
2. 在路径栏中输入: `/www/wwwroot`
3. 点击右侧的 **"上传"** 按钮
4. 选择刚才压缩的 `ai-writer.zip` 文件
5. 点击 **"开始上传"**
6. 等待上传完成 (根据网速,可能需要 5-30 分钟)

#### 10.3 解压文件
1. 上传完成后,在文件列表中找到 `ai-writer.zip`
2. 右键点击,选择 **"解压"**
3. 解压到当前目录
4. 解压完成后,会看到 `ai-writer` 文件夹
5. 可以删除 `ai-writer.zip` 文件

#### 10.4 检查文件
1. 点击进入 `ai-writer` 文件夹
2. 应该能看到以下文件和目录:
   - `backend/` (后端代码)
   - `src/` (前端代码)
   - `package.json`
   - `vite.config.ts`
   - 其他文件...

### 方法 2: 使用 Git 克隆 (如果你的代码在 GitHub/GitLab)

```bash
# 如果项目在 Git 仓库
cd /www/wwwroot
git clone https://github.com/你的用户名/ai-writer.git
cd ai-writer
```

---

# 第四部分: 配置和部署后端

## 步骤 11: 配置后端环境变量

### 11.1 进入后端目录
在终端中输入:
```bash
cd /www/wwwroot/ai-writer/backend
pwd
```
应该显示: `/www/wwwroot/ai-writer/backend`

### 11.2 复制环境变量模板
```bash
# 复制 .env.example 为 .env
cp .env.example .env

# 查看文件是否创建成功
ls -la .env
```

### 11.3 编辑 .env 文件

**方法 1: 使用宝塔面板编辑 (推荐)**
1. 在宝塔面板的 **"文件"** 页面
2. 进入 `/www/wwwroot/ai-writer/backend`
3. 找到 `.env` 文件
4. 右键点击,选择 **"编辑"**
5. 按照下面的说明修改内容

**方法 2: 使用终端编辑器**
```bash
nano .env
```

### 11.4 修改 .env 文件内容

**复制以下内容,替换整个 .env 文件:**

```bash
# ==================== 应用配置 ====================
APP_NAME=文枢AI
APP_VERSION=1.0.0
API_V1_PREFIX=/api/v1
DEBUG=False
SECRET_KEY=请在这里粘贴一个随机字符串

# ==================== 服务器配置 ====================
HOST=127.0.0.1
PORT=8000

# ==================== 数据库配置 ====================
# 格式: postgresql+asyncpg://用户名:密码@主机:端口/数据库名
DATABASE_URL=postgresql+asyncpg://novelaide:YourStrong_DB_Password123@localhost:5432/novelaide
DB_ECHO=False

# ==================== Redis 配置 ====================
REDIS_URL=redis://localhost:6379/0

# ==================== JWT 配置 ====================
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# ==================== CORS 配置 ====================
# 重要: 这里填写你的域名!
CORS_ORIGINS=["https://你的域名.com","https://www.你的域名.com"]

# ==================== OpenAI 配置 ====================
# 重要: 这里填写你的 OpenAI API Key!
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_BASE_URL=https://204992.xyz/v1
OPENAI_MODEL=gemini-2.5-pro

# 图书分析专用模型
BOOK_ANALYSIS_MODEL=gemini-2.5-flash-lite
BOOK_ANALYSIS_TIMEOUT=60

# ==================== 文件上传配置 ====================
MAX_UPLOAD_SIZE=10485760
UPLOAD_DIR=./uploads

# ==================== 日志配置 ====================
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# ==================== 管理员账号 ====================
# 重要: 首次部署后请立即修改密码!
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123456
```

### 11.5 生成 SECRET_KEY

在终端中执行:
```bash
# 生成一个随机的 SECRET_KEY
openssl rand -hex 32
```

会输出一串随机字符,例如:
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

**把这串字符复制,替换 .env 文件中的 `SECRET_KEY` 值**

### 11.6 修改数据库密码

找到这一行:
```bash
DATABASE_URL=postgresql+asyncpg://novelaide:YourStrong_DB_Password123@localhost:5432/novelaide
```

把 `YourStrong_DB_Password123` 替换为你在步骤 8.2 中设置的数据库密码

### 11.7 修改域名

找到这一行:
```bash
CORS_ORIGINS=["https://你的域名.com","https://www.你的域名.com"]
```

把 `你的域名.com` 替换为你的实际域名,例如:
```bash
CORS_ORIGINS=["https://example.com","https://www.example.com"]
```

### 11.8 填写 OpenAI API Key

找到这一行:
```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

把 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 替换为你的真实 OpenAI API Key

### 11.9 保存文件

**宝塔面板:**
- 点击右上角的 **"保存"** 按钮

**终端编辑器 (nano):**
- 按 `Ctrl + O` 保存
- 按 `Enter` 确认
- 按 `Ctrl + X` 退出

---

## 步骤 12: 安装 Python 依赖

### 12.1 创建 Python 虚拟环境

在终端中执行:
```bash
# 确保在 backend 目录
cd /www/wwwroot/ai-writer/backend

# 创建虚拟环境
python3.11 -m venv venv

# 查看是否创建成功
ls -la venv/
```

应该能看到 `venv` 目录及其中的 `bin`, `lib` 等子目录

### 12.2 激活虚拟环境

```bash
# 激活虚拟环境
source venv/bin/activate

# 激活后,命令提示符前面会出现 (venv)
# 例如: (venv) root@ubuntu:/www/wwwroot/ai-writer/backend#
```

### 12.3 升级 pip

```bash
# 升级 pip 到最新版本
pip install --upgrade pip

# 查看 pip 版本
pip --version
```

### 12.4 安装系统依赖包 (如果需要)

有些 Python 包需要编译,需要先安装系统依赖:
```bash
# 安装编译工具和开发库
sudo apt update
sudo apt install -y build-essential python3.11-dev libpq-dev
```

### 12.5 安装 Python 依赖

**这一步可能需要 10-20 分钟,请耐心等待:**
```bash
# 安装所有依赖
pip install -r requirements.txt

# 如果网络较慢,可以使用国内镜像:
# pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

安装过程中会看到很多输出信息,这是正常的。

**常见错误处理:**

如果看到类似 `error: Microsoft Visual C++ 14.0 is required` 的错误:
```bash
# 安装编译工具
sudo apt install -y gcc g++ make
```

如果看到 `psycopg2` 相关错误:
```bash
# 安装 PostgreSQL 开发库
sudo apt install -y libpq-dev
```

### 12.6 验证安装

```bash
# 查看已安装的包
pip list

# 应该能看到很多包,例如:
# fastapi, uvicorn, sqlalchemy, redis, openai 等
```

---

## 步骤 13: 初始化数据库

### 13.1 运行数据库迁移

**确保虚拟环境已激活 (命令提示符前有 `(venv)`)**

```bash
# 确保在 backend 目录
cd /www/wwwroot/ai-writer/backend

# 运行数据库迁移
python -m alembic upgrade head
```

**成功的输出示例:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001, initial migration
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, add users table
...
```

**如果遇到错误:**

1. **错误: Can't locate revision identified by 'xxxx'**
   ```bash
   # 查看当前数据库版本
   python -m alembic current

   # 如果显示空,说明数据库是全新的,直接运行:
   python -m alembic upgrade head
   ```

2. **错误: Connection refused**
   - 检查 PostgreSQL 是否运行: `sudo systemctl status postgresql`
   - 检查 .env 中的 DATABASE_URL 是否正确

3. **错误: password authentication failed**
   - 检查 .env 中的数据库密码是否正确

### 13.2 创建管理员账号

```bash
# 运行创建管理员脚本
python create_admin.py
```

**会提示输入管理员信息:**
```
请输入管理员邮箱 [admin@example.com]:
请输入管理员密码 [使用 .env 中的密码]:
请输入管理员昵称 [Admin]:
```

可以直接按回车使用默认值,或输入自定义值。

**成功输出:**
```
✓ 管理员账号创建成功!
  邮箱: admin@example.com
  密码: (你设置的密码)
```

---

## 步骤 14: 测试后端运行

### 14.1 手动启动后端 (测试用)

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 启动后端
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**成功的输出:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### 14.2 测试 API

**打开另一个终端窗口** (不要关闭正在运行后端的窗口),执行:
```bash
# 测试健康检查接口
curl http://127.0.0.1:8000/api/v1/health

# 应该返回:
# {"status":"ok"}
```

或者在浏览器中访问:
```
http://你的服务器IP:8000/api/docs
```

应该能看到 Swagger API 文档页面,说明后端运行正常!

### 14.3 停止测试

回到运行后端的终端窗口,按 `Ctrl + C` 停止后端

---

## 步骤 15: 配置 Supervisor 守护进程

### 15.1 使用宝塔面板配置 (推荐)

1. 在宝塔面板左侧菜单,点击 **"软件商店"**
2. 找到 **"Supervisor 管理器"**,点击 **"设置"**
3. 点击 **"添加守护进程"** 按钮

### 15.2 填写守护进程配置

在弹出的对话框中填写:

**名称:**
```
ai-writer-backend
```

**启动用户:**
```
root
```

**运行目录:**
```
/www/wwwroot/ai-writer/backend
```

**启动命令:**
```
/www/wwwroot/ai-writer/backend/venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
```

**进程数量:**
```
1
```

点击 **"确定"** 保存

### 15.3 启动守护进程

1. 在 Supervisor 管理器中,找到刚才创建的 `ai-writer-backend`
2. 点击右侧的 **"启动"** 按钮
3. 状态应该显示为 **"运行中"** (绿色)

### 15.4 查看日志

1. 点击 `ai-writer-backend` 右侧的 **"日志"** 按钮
2. 应该能看到类似的输出:
   ```
   INFO:     Started server process [12345]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

### 15.5 验证后端运行

在终端中执行:
```bash
curl http://127.0.0.1:8000/api/v1/health
```

应该返回: `{"status":"ok"}`

**恭喜!后端部署完成!** ✅

---

# 第五部分: 配置和部署前端

## 步骤 16: 配置前端环境变量

### 16.1 进入项目根目录

```bash
cd /www/wwwroot/ai-writer
pwd
```
应该显示: `/www/wwwroot/ai-writer`

### 16.2 创建生产环境配置文件

```bash
# 复制环境变量模板
cp .env.example .env.production

# 查看文件
ls -la .env.production
```

### 16.3 编辑 .env.production

**使用宝塔面板编辑:**
1. 在文件管理中进入 `/www/wwwroot/ai-writer`
2. 找到 `.env.production` 文件
3. 右键 -> 编辑

**修改内容如下:**

```bash
# ==================== API 配置 ====================
# 重要: 这里填写你的域名!
VITE_API_URL=https://你的域名.com

# ==================== 开发配置 ====================
VITE_USE_MOCK_AI=false

# 注意: 前端不需要配置 OPENAI_API_KEY
# API Key 由后端统一管理,更安全!
```

把 `https://你的域名.com` 替换为你的实际域名,例如:
```bash
VITE_API_URL=https://www.example.com
```

保存文件

---

## 步骤 17: 构建前端

### 17.1 安装 Node.js 依赖

```bash
# 确保在项目根目录
cd /www/wwwroot/ai-writer

# 安装依赖 (这可能需要 5-10 分钟)
npm install

# 如果网络较慢,可以使用国内镜像:
# npm install --registry=https://registry.npmmirror.com
```

**安装过程中可能看到一些警告,这是正常的,不影响使用**

### 17.2 构建生产版本

```bash
# 构建前端 (这可能需要 3-5 分钟)
npm run build
```

**成功的输出示例:**
```
vite v5.x.x building for production...
✓ 1234 modules transformed.
dist/index.html                   1.23 kB │ gzip:  0.56 kB
dist/assets/index-abc123.js     234.56 kB │ gzip: 78.90 kB
dist/assets/index-def456.css     12.34 kB │ gzip:  3.45 kB
✓ built in 123.45s
```

### 17.3 验证构建结果

```bash
# 查看 dist 目录
ls -la dist/

# 应该能看到:
# index.html
# assets/ (包含 js 和 css 文件)
# 其他静态资源
```

**恭喜!前端构建完成!** ✅

---

# 第六部分: 配置 Nginx

## 步骤 18: 配置网站

### 18.1 在宝塔面板添加网站

1. 在宝塔面板左侧菜单,点击 **"网站"**
2. 点击 **"添加站点"** 按钮

### 18.2 填写网站信息

**域名:**
```
你的域名.com
www.你的域名.com
```
例如:
```
example.com
www.example.com
```

**根目录:**
```
/www/wwwroot/ai-writer/dist
```

**重要:** 注意是 `dist` 目录,不是 `ai-writer` 目录!

**FTP:**
不创建

**数据库:**
不创建 (我们已经手动创建了)

**PHP 版本:**
纯静态 (因为这是 React 项目)

点击 **"提交"**

### 18.3 配置 SSL 证书

1. 在网站列表中,找到刚才创建的网站
2. 点击右侧的 **"设置"** 按钮
3. 点击左侧的 **"SSL"** 标签
4. 如果你已经有 SSL 证书:
   - 选择 **"其他证书"**
   - 粘贴你的证书内容
5. 如果没有证书,可以申请免费的 Let's Encrypt 证书:
   - 选择 **"Let's Encrypt"**
   - 输入邮箱
   - 点击 **"申请"**
   - 等待申请完成 (约 1-2 分钟)
6. 申请成功后,开启 **"强制HTTPS"** 开关

### 18.4 配置 Nginx 反向代理

1. 在网站设置页面,点击左侧的 **"配置文件"** 标签
2. 找到 `server` 块中的内容
3. **完整替换**为以下配置:

```nginx
server {
    listen 80;
    listen 443 ssl http2;
    server_name 你的域名.com www.你的域名.com;

    # SSL 证书配置 (宝塔自动生成,不要修改)
    # ssl_certificate    /www/server/panel/vhost/cert/你的域名/fullchain.pem;
    # ssl_certificate_key    /www/server/panel/vhost/cert/你的域名/privkey.pem;

    # SSL 优化配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 强制 HTTPS
    if ($server_port !~ 443){
        rewrite ^(/.*)$ https://$host$1 permanent;
    }

    # 错误页面
    error_page 497 https://$host$request_uri;

    # 访问日志
    access_log /www/wwwlogs/ai-writer-access.log;
    error_log /www/wwwlogs/ai-writer-error.log;

    # ==================== 前端静态文件 ====================
    location / {
        root /www/wwwroot/ai-writer/dist;
        index index.html;
        try_files $uri $uri/ /index.html;

        # 安全头
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # 禁用缓存 HTML 文件
        location = /index.html {
            add_header Cache-Control "no-cache, no-store, must-revalidate";
            add_header Pragma "no-cache";
            add_header Expires "0";
        }

        # 缓存静态资源 (JS, CSS, 图片等)
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # ==================== 后端 API 代理 ====================
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket 支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时设置 (AI 响应可能较慢)
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # 缓冲区设置
        proxy_buffering off;
        proxy_buffer_size 4k;
    }

    # ==================== 文件上传路径 ====================
    location /uploads {
        alias /www/wwwroot/ai-writer/backend/uploads;
        expires 1y;
        add_header Cache-Control "public";

        # 安全设置: 禁止执行脚本
        location ~ \.(php|asp|aspx|jsp)$ {
            deny all;
        }
    }

    # ==================== 禁止访问敏感文件 ====================
    location ~ /\.(git|env|htaccess) {
        deny all;
    }

    location ~ \.(sql|bak|backup|log)$ {
        deny all;
    }
}
```

**重要修改:**
- 把所有的 `你的域名.com` 替换为你的实际域名
- 保留宝塔自动生成的 SSL 证书路径 (以 `ssl_certificate` 开头的两行)

### 18.5 保存并重启 Nginx

1. 点击右上角的 **"保存"** 按钮
2. 在宝塔面板左侧菜单,点击 **"软件商店"**
3. 找到 **"Nginx"**,点击 **"设置"**
4. 点击 **"服务"** 标签
5. 点击 **"重载配置"** 按钮 (或 **"重启"**)

---

## 步骤 19: 配置文件上传目录

### 19.1 创建必要的目录

在终端中执行:
```bash
# 创建上传目录
mkdir -p /www/wwwroot/ai-writer/backend/uploads
mkdir -p /www/wwwroot/ai-writer/backend/logs

# 设置权限
chmod -R 755 /www/wwwroot/ai-writer/backend/uploads
chmod -R 755 /www/wwwroot/ai-writer/backend/logs

# 设置所有者
chown -R www-data:www-data /www/wwwroot/ai-writer/backend/uploads
chown -R www-data:www-data /www/wwwroot/ai-writer/backend/logs
```

### 19.2 验证目录权限

```bash
# 查看目录权限
ls -la /www/wwwroot/ai-writer/backend/

# 应该看到:
# drwxr-xr-x  2 www-data www-data 4096 ... uploads
# drwxr-xr-x  2 www-data www-data 4096 ... logs
```

---

# 第七部分: 测试和验证

## 步骤 20: 全面测试

### 20.1 测试前端访问

1. 打开浏览器
2. 访问: `https://你的域名.com`
3. 应该能看到登录页面
4. 如果看到 "无法访问此网站" 或 "连接超时":
   - 检查域名 DNS 解析是否正确
   - 检查防火墙是否开放 80 和 443 端口
   - 检查 Nginx 是否运行: `sudo systemctl status nginx`

### 20.2 测试 API 连接

1. 在浏览器中访问: `https://你的域名.com/api/v1/health`
2. 应该看到: `{"status":"ok"}`
3. 如果看到 502 错误:
   - 检查后端是否运行
   - 在宝塔面板 -> Supervisor 管理器中查看 `ai-writer-backend` 状态
   - 查看后端日志: `/www/wwwroot/ai-writer/backend/logs/app.log`

### 20.3 测试注册登录

1. 在登录页面,点击 **"注册"**
2. 填写信息:
   - 邮箱: `test@example.com`
   - 密码: `Test123456`
   - 昵称: `测试用户`
3. 点击 **"注册"**
4. 应该能成功注册并跳转到首页

### 20.4 测试管理员登录

1. 使用管理员账号登录:
   - 邮箱: 在步骤 13.2 中设置的管理员邮箱
   - 密码: 在步骤 13.2 中设置的管理员密码
2. 应该能看到更多管理功能

### 20.5 测试 AI 功能

1. 登录后,点击 **"AI 写作"**
2. 输入一段文字,点击 **"润色"** 或 **"续写"**
3. 应该能看到 AI 返回的内容
4. 如果提示 "API 调用失败":
   - 检查后端 .env 中的 `OPENAI_API_KEY` 是否正确
   - 检查 API Key 是否有余额
   - 查看后端日志: `tail -f /www/wwwroot/ai-writer/backend/logs/app.log`

### 20.6 测试文件上传

1. 在编辑器中,尝试上传图片
2. 应该能成功上传并显示
3. 如果上传失败:
   - 检查 `/www/wwwroot/ai-writer/backend/uploads` 目录权限
   - 查看 Nginx 错误日志: `tail -f /www/wwwlogs/ai-writer-error.log`

---

## 步骤 21: 性能优化

### 21.1 启用 Gzip 压缩

1. 在宝塔面板 -> 软件商店 -> Nginx -> 设置
2. 点击 **"配置修改"** 标签
3. 找到 `http` 块,确保有以下配置:

```nginx
gzip on;
gzip_min_length 1k;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript application/json application/javascript application/xml+rss;
gzip_vary on;
gzip_disable "MSIE [1-6]\.";
```

4. 保存并重载 Nginx

### 21.2 配置 Redis 持久化

1. 在宝塔面板 -> 软件商店 -> Redis -> 设置
2. 点击 **"配置修改"** 标签
3. 找到以下配置,确保开启:

```
save 900 1
save 300 10
save 60 10000
```

4. 保存并重启 Redis

### 21.3 优化 PostgreSQL

1. 在终端中执行:
```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```

2. 找到并修改以下配置 (根据服务器内存调整):

```ini
# 如果服务器有 4GB 内存
shared_buffers = 1GB
effective_cache_size = 3GB
maintenance_work_mem = 256MB
work_mem = 16MB

# 如果服务器有 2GB 内存
# shared_buffers = 512MB
# effective_cache_size = 1536MB
# maintenance_work_mem = 128MB
# work_mem = 8MB
```

3. 保存并重启 PostgreSQL:
```bash
sudo systemctl restart postgresql
```

---

## 步骤 22: 配置自动备份

### 22.1 配置数据库自动备份

1. 在宝塔面板左侧菜单,点击 **"计划任务"**
2. 点击 **"添加计划任务"**
3. 填写信息:
   - 任务类型: **Shell脚本**
   - 任务名称: `备份AI写作助手数据库`
   - 执行周期: **每天** `03:00`
   - 脚本内容:
   ```bash
   #!/bin/bash
   BACKUP_DIR="/www/backup/ai-writer"
   DATE=$(date +%Y%m%d_%H%M%S)

   # 创建备份目录
   mkdir -p $BACKUP_DIR

   # 备份数据库
   sudo -u postgres pg_dump novelaide > $BACKUP_DIR/novelaide_$DATE.sql

   # 压缩备份文件
   gzip $BACKUP_DIR/novelaide_$DATE.sql

   # 删除 30 天前的备份
   find $BACKUP_DIR -name "novelaide_*.sql.gz" -mtime +30 -delete

   echo "数据库备份完成: novelaide_$DATE.sql.gz"
   ```
4. 点击 **"确定"**

### 22.2 配置文件自动备份

1. 添加另一个计划任务
2. 填写信息:
   - 任务类型: **Shell脚本**
   - 任务名称: `备份AI写作助手上传文件`
   - 执行周期: **每周日** `03:30`
   - 脚本内容:
   ```bash
   #!/bin/bash
   BACKUP_DIR="/www/backup/ai-writer"
   DATE=$(date +%Y%m%d_%H%M%S)

   # 创建备份目录
   mkdir -p $BACKUP_DIR

   # 备份上传文件
   tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /www/wwwroot/ai-writer/backend/uploads

   # 删除 60 天前的备份
   find $BACKUP_DIR -name "uploads_*.tar.gz" -mtime +60 -delete

   echo "文件备份完成: uploads_$DATE.tar.gz"
   ```
3. 点击 **"确定"**

---

## 步骤 23: 安全加固

### 23.1 配置防火墙

1. 在宝塔面板左侧菜单,点击 **"安全"**
2. 确保以下端口已开放:
   - `22` (SSH) ✅
   - `80` (HTTP) ✅
   - `443` (HTTPS) ✅
   - `8888` (宝塔面板) ✅

3. 其他端口应该关闭,特别是:
   - `5432` (PostgreSQL) ❌ 不要对外开放!
   - `6379` (Redis) ❌ 不要对外开放!
   - `8000` (后端) ❌ 不要对外开放!

### 23.2 修改宝塔面板端口 (可选但推荐)

1. 在宝塔面板 -> 设置 -> 面板设置
2. 修改 **"面板端口"** 为自定义端口,例如 `18888`
3. 保存后,下次访问宝塔需要使用新端口: `http://IP:18888`

### 23.3 配置 SSH 密钥登录 (可选但推荐)

1. 在本地电脑生成 SSH 密钥 (如果还没有):
```powershell
ssh-keygen -t rsa -b 4096
```

2. 将公钥复制到服务器:
```powershell
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh root@你的服务器IP "cat >> ~/.ssh/authorized_keys"
```

3. 之后可以免密码登录

### 23.4 禁用 root 密码登录 (可选)

**警告: 只有在配置好 SSH 密钥登录后才能执行此步骤!**

```bash
sudo nano /etc/ssh/sshd_config
```

修改以下配置:
```
PasswordAuthentication no
```

保存并重启 SSH:
```bash
sudo systemctl restart sshd
```

---

## 步骤 24: 监控和日志

### 24.1 查看实时日志

**后端日志:**
```bash
# 查看后端应用日志
tail -f /www/wwwroot/ai-writer/backend/logs/app.log

# 查看 Supervisor 日志
tail -f /www/wwwroot/ai-writer/backend/logs/supervisor.log
```

**Nginx 日志:**
```bash
# 访问日志
tail -f /www/wwwlogs/ai-writer-access.log

# 错误日志
tail -f /www/wwwlogs/ai-writer-error.log
```

**PostgreSQL 日志:**
```bash
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

### 24.2 配置日志轮转

编辑日志轮转配置:
```bash
sudo nano /etc/logrotate.d/ai-writer
```

添加以下内容:
```
/www/wwwroot/ai-writer/backend/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    sharedscripts
    postrotate
        supervisorctl restart ai-writer-backend > /dev/null 2>&1 || true
    endscript
}
```

---

# 第八部分: 常见问题排查

## 问题 1: 网站无法访问

### 症状:
- 浏览器显示 "无法访问此网站" 或 "连接超时"

### 排查步骤:

1. **检查域名解析**
   ```bash
   # 在本地电脑 PowerShell 中执行
   nslookup 你的域名.com
   ```
   应该返回你的服务器 IP 地址

2. **检查 Nginx 状态**
   ```bash
   sudo systemctl status nginx
   ```
   应该显示 "active (running)"

3. **检查防火墙**
   ```bash
   sudo ufw status
   ```
   确保 80 和 443 端口开放

4. **检查 Nginx 配置**
   ```bash
   sudo nginx -t
   ```
   应该显示 "test is successful"

---

## 问题 2: API 返回 502 错误

### 症状:
- 前端可以访问,但 API 请求返回 502 Bad Gateway

### 排查步骤:

1. **检查后端是否运行**
   - 在宝塔面板 -> Supervisor 管理器
   - 查看 `ai-writer-backend` 状态
   - 如果显示 "已停止",点击 "启动"

2. **查看后端日志**
   ```bash
   tail -100 /www/wwwroot/ai-writer/backend/logs/app.log
   ```
   查看是否有错误信息

3. **测试后端直接访问**
   ```bash
   curl http://127.0.0.1:8000/api/v1/health
   ```
   应该返回 `{"status":"ok"}`

4. **检查端口占用**
   ```bash
   sudo netstat -tulpn | grep 8000
   ```
   应该显示 uvicorn 进程监听 8000 端口

---

## 问题 3: 数据库连接失败

### 症状:
- 后端日志显示 "connection refused" 或 "password authentication failed"

### 排查步骤:

1. **检查 PostgreSQL 状态**
   ```bash
   sudo systemctl status postgresql
   ```
   应该显示 "active (running)"

2. **测试数据库连接**
   ```bash
   psql -U novelaide -d novelaide -h localhost
   ```
   输入数据库密码,应该能登录

3. **检查 .env 配置**
   ```bash
   cat /www/wwwroot/ai-writer/backend/.env | grep DATABASE_URL
   ```
   确认数据库 URL 格式正确

4. **查看 PostgreSQL 日志**
   ```bash
   sudo tail -50 /var/log/postgresql/postgresql-15-main.log
   ```

---

## 问题 4: 文件上传失败

### 症状:
- 上传文件时提示失败或 403 错误

### 排查步骤:

1. **检查目录权限**
   ```bash
   ls -la /www/wwwroot/ai-writer/backend/uploads
   ```
   应该显示 `drwxr-xr-x ... www-data www-data`

2. **修复权限**
   ```bash
   sudo chown -R www-data:www-data /www/wwwroot/ai-writer/backend/uploads
   sudo chmod -R 755 /www/wwwroot/ai-writer/backend/uploads
   ```

3. **检查磁盘空间**
   ```bash
   df -h
   ```
   确保有足够的磁盘空间

---

## 问题 5: AI 功能不工作

### 症状:
- AI 润色、续写等功能提示错误

### 排查步骤:

1. **检查 API Key**
   ```bash
   cat /www/wwwroot/ai-writer/backend/.env | grep OPENAI_API_KEY
   ```
   确认 API Key 正确

2. **测试 API Key**
   ```bash
   curl https://204992.xyz/v1/models \
     -H "Authorization: Bearer 你的API_KEY"
   ```
   应该返回可用模型列表

3. **查看后端日志**
   ```bash
   tail -100 /www/wwwroot/ai-writer/backend/logs/app.log
   ```
   查看 AI 调用相关的错误信息

---

# 第九部分: 更新和维护

## 如何更新代码

### 更新后端:

```bash
# 1. 进入项目目录
cd /www/wwwroot/ai-writer

# 2. 拉取最新代码
git pull

# 3. 进入后端目录
cd backend

# 4. 激活虚拟环境
source venv/bin/activate

# 5. 更新依赖
pip install -r requirements.txt

# 6. 运行数据库迁移
python -m alembic upgrade head

# 7. 重启后端
sudo supervisorctl restart ai-writer-backend

# 8. 查看状态
sudo supervisorctl status ai-writer-backend
```

### 更新前端:

```bash
# 1. 进入项目目录
cd /www/wwwroot/ai-writer

# 2. 拉取最新代码 (如果还没拉取)
git pull

# 3. 安装依赖
npm install

# 4. 构建前端
npm run build

# 5. 无需重启,刷新浏览器即可
```

---

## 日常维护命令

### 查看服务状态:
```bash
# 查看后端状态
sudo supervisorctl status ai-writer-backend

# 查看 Nginx 状态
sudo systemctl status nginx

# 查看 PostgreSQL 状态
sudo systemctl status postgresql

# 查看 Redis 状态
sudo systemctl status redis-server
```

### 重启服务:
```bash
# 重启后端
sudo supervisorctl restart ai-writer-backend

# 重启 Nginx
sudo systemctl restart nginx

# 重启 PostgreSQL
sudo systemctl restart postgresql

# 重启 Redis
sudo systemctl restart redis-server
```

### 查看日志:
```bash
# 查看后端日志 (最新 100 行)
tail -100 /www/wwwroot/ai-writer/backend/logs/app.log

# 实时查看后端日志
tail -f /www/wwwroot/ai-writer/backend/logs/app.log

# 查看 Nginx 访问日志
tail -100 /www/wwwlogs/ai-writer-access.log

# 查看 Nginx 错误日志
tail -100 /www/wwwlogs/ai-writer-error.log
```

---

# 🎉 恭喜!部署完成!

## 验证清单

请逐一检查以下项目:

- ✅ 可以访问网站: `https://你的域名.com`
- ✅ SSL 证书有效 (浏览器地址栏显示锁图标)
- ✅ 可以注册新用户
- ✅ 可以登录
- ✅ AI 功能正常工作
- ✅ 文件上传功能正常
- ✅ 后端 API 正常响应: `https://你的域名.com/api/v1/health`
- ✅ 后端进程在 Supervisor 中显示 "运行中"
- ✅ 数据库可以正常连接
- ✅ Redis 正常运行

## 下一步

1. **修改管理员密码**
   - 使用管理员账号登录
   - 进入个人设置
   - 修改密码

2. **配置邮件服务** (可选)
   - 用于找回密码、发送通知等
   - 在后端 .env 中配置 SMTP 信息

3. **配置 CDN** (可选)
   - 加速静态资源访问
   - 减少服务器带宽消耗

4. **定期备份**
   - 确保自动备份任务正常运行
   - 定期测试备份恢复

5. **监控告警** (可选)
   - 使用宝塔面板的监控报警功能
   - 或集成第三方监控服务

## 获取帮助

如果遇到问题:
1. 查看本文档的 "常见问题排查" 部分
2. 查看日志文件获取详细错误信息
3. 搜索错误信息寻找解决方案
4. 提交 Issue 获取技术支持

---

## 附录: 完整目录结构

部署完成后的目录结构:

```
/www/wwwroot/ai-writer/
├── backend/                    # 后端代码
│   ├── app/                   # 应用代码
│   ├── alembic/               # 数据库迁移
│   ├── venv/                  # Python 虚拟环境
│   ├── uploads/               # 上传文件目录
│   ├── logs/                  # 日志目录
│   ├── .env                   # 后端环境变量
│   ├── requirements.txt       # Python 依赖
│   └── ...
├── src/                       # 前端源代码
├── dist/                      # 前端构建产物 (Nginx 指向这里)
├── node_modules/              # Node.js 依赖
├── .env.production           # 前端环境变量
├── package.json              # 前端依赖配置
├── vite.config.ts            # Vite 配置
└── ...

/www/backup/ai-writer/         # 备份目录
├── novelaide_20240101.sql.gz # 数据库备份
└── uploads_20240101.tar.gz    # 文件备份
```

---

**祝你使用愉快!** 🚀
