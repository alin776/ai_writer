@echo off
chcp 65001 >nul
echo ====================================
echo   AI Writer 一键部署脚本
echo   Windows 本地开发环境
echo ====================================
echo.

REM 切换到项目根目录（上一级目录）
cd /d "%~dp0.."

REM 设置错误处理
setlocal enabledelayedexpansion

REM ============================================
REM 第一步：检查 Python
REM ============================================
echo [1/10] 检查 Python 环境...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python 未安装
    echo.
    echo 请按以下步骤安装 Python:
    echo 1. 访问: https://www.python.org/downloads/
    echo 2. 下载 Python 3.11 或更高版本
    echo 3. 安装时务必勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
python --version
echo ✅ Python 已安装
echo.

REM ============================================
REM 第二步：检查 Node.js
REM ============================================
echo [2/10] 检查 Node.js 环境...
node --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js 未安装
    echo.
    echo 请按以下步骤安装 Node.js:
    echo 1. 访问: https://nodejs.org/
    echo 2. 下载 LTS 版本
    echo 3. 运行安装程序（使用默认设置）
    echo.
    pause
    exit /b 1
)
node --version
echo ✅ Node.js 已安装
echo.

REM ============================================
REM 第三步：检查 PostgreSQL
REM ============================================
echo [3/10] 检查 PostgreSQL...
psql --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PostgreSQL 未安装或未添加到 PATH
    echo.
    echo 请按以下步骤安装 PostgreSQL:
    echo 1. 访问: https://www.postgresql.org/download/windows/
    echo 2. 下载 PostgreSQL 15 或更高版本
    echo 3. 安装时记住设置的密码
    echo 4. 安装后运行本脚本
    echo.
    pause
    exit /b 1
)
psql --version
echo ✅ PostgreSQL 已安装
echo.

REM ============================================
REM 第四步：检查 Redis
REM ============================================
echo [4/10] 检查 Redis...
echo ⚠️  Redis 有多种安装方式:
echo    1. Memurai (推荐): https://www.memurai.com/
echo    2. WSL2 + Redis
echo    3. 预编译版本: https://github.com/tporadowski/redis/releases
echo.
redis-cli ping >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Redis 已安装并运行中
) else (
    memurai-cli ping >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Memurai 已安装并运行中
    ) else (
        echo ⚠️  Redis/Memurai 未运行
        echo    请确保 Redis 服务已启动
        echo    按任意键继续（如果你确定 Redis 已经在运行）...
        pause >nul
    )
)
echo.

REM ============================================
REM 第五步：配置环境变量
REM ============================================
echo [5/10] 配置环境变量...

REM 检查根目录 .env 文件
if not exist ".env" (
    if exist ".env.example" (
        echo 📋 复制前端环境变量模板...
        copy .env.example .env >nul
        echo ✅ 已创建 .env 文件
        echo.
        echo ⚠️  重要: 请编辑 .env 文件，填入你的 OpenAI API Key
        echo    文件位置: %CD%\.env
        echo.
        echo 按任意键打开编辑器...
        pause >nul
        notepad .env
    ) else (
        echo ❌ .env.example 文件不存在
        exit /b 1
    )
) else (
    echo ✅ 前端环境变量已存在
)

REM 检查后端 .env 文件
if not exist "backend\.env" (
    echo 📋 创建后端环境变量...
    (
        echo # 数据库连接
        echo DATABASE_URL=postgresql+asyncpg://novelaide:novelaide_password@localhost:5432/novelaide
        echo.
        echo # Redis 连接
        echo REDIS_URL=redis://localhost:6379/0
        echo.
        echo # JWT 密钥
        echo SECRET_KEY=your-secret-key-for-development-change-in-production
        echo.
        echo # 调试模式
        echo DEBUG=True
        echo.
        echo # OpenAI API Key
        echo OPENAI_API_KEY=sk-your-openai-api-key-here
        echo.
        echo # CORS 配置
        echo CORS_ORIGINS=["http://localhost:5173","http://127.0.0.1:5173"]
    ) > backend\.env
    echo ✅ 已创建 backend\.env 文件
    echo.
    echo ⚠️  重要: 请编辑 backend\.env 文件，填入你的 OpenAI API Key
    echo    文件位置: %CD%\backend\.env
    echo.
    echo 按任意键打开编辑器...
    pause >nul
    notepad backend\.env
) else (
    echo ✅ 后端环境变量已存在
)
echo.

REM ============================================
REM 第六步：创建数据库
REM ============================================
echo [6/10] 配置数据库...
echo 正在尝试创建数据库...
echo.

REM 提示用户输入 PostgreSQL 密码
echo 请输入 PostgreSQL 的 postgres 用户密码:
set /p PGPASSWORD=密码:

REM 创建数据库和用户
echo.
echo 执行数据库初始化...
set PGPASSWORD=%PGPASSWORD%
psql -U postgres -h localhost -c "CREATE DATABASE novelaide;" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ 数据库创建成功
) else (
    echo ⚠️  数据库可能已存在
)

psql -U postgres -h localhost -c "CREATE USER novelaide WITH PASSWORD 'novelaide_password';" 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ 用户创建成功
) else (
    echo ⚠️  用户可能已存在
)

psql -U postgres -h localhost -c "GRANT ALL PRIVILEGES ON DATABASE novelaide TO novelaide;" 2>nul
echo ✅ 权限配置完成
echo.

REM ============================================
REM 第七步：安装前端依赖
REM ============================================
echo [7/10] 安装前端依赖...
if not exist "node_modules" (
    echo 📦 正在安装前端依赖，这可能需要几分钟...
    echo.
    call npm install
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo ❌ 前端依赖安装失败
        echo.
        echo 尝试解决方案:
        echo 1. 使用国内镜像: npm install --registry=https://registry.npmmirror.com
        echo 2. 清理缓存: npm cache clean --force
        echo.
        pause
        exit /b 1
    )
    echo ✅ 前端依赖安装完成
) else (
    echo ✅ 前端依赖已存在，跳过安装
    echo    （如需重新安装，请删除 node_modules 文件夹）
)
echo.

REM ============================================
REM 第八步：安装后端依赖
REM ============================================
echo [8/10] 安装后端依赖...
cd backend

if not exist "venv" (
    echo 🐍 创建 Python 虚拟环境...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo ❌ 虚拟环境创建失败
        cd ..
        pause
        exit /b 1
    )
    echo ✅ 虚拟环境创建成功
)

echo 🐍 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
echo 正在安装 Python 包，这可能需要几分钟...
echo.
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ 后端依赖安装失败
    echo.
    echo 尝试解决方案:
    echo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    echo.
    cd ..
    pause
    exit /b 1
)
echo ✅ 后端依赖安装完成
cd ..
echo.

REM ============================================
REM 第九步：初始化数据库表
REM ============================================
echo [9/10] 初始化数据库表...
echo 正在运行数据库迁移，创建所有表...
cd backend
call venv\Scripts\activate.bat

REM 运行 Alembic 迁移
alembic upgrade head
if %ERRORLEVEL% EQU 0 (
    echo ✅ 数据库表创建成功
    echo.
    echo 已创建以下数据表:
    echo    - users (用户表)
    echo    - works (作品表)
    echo    - chapters (章节表)
    echo    - characters (角色表)
    echo    - locations (地点表)
    echo    - settings (设定表)
    echo    - ai_guidelines (AI指引表)
    echo    - novel_analyses (小说分析表)
    echo    - timeline_events (时间线事件表)
    echo    - entity_relationships (实体关系表)
    echo    - ai_call_logs (AI调用日志表)
    echo    - rewrite_history (重写历史表)
    echo    - humanize_sessions (人性化会话表)
    echo    - knowledge_items (知识库表)
    echo    - 以及其他支持表...
) else (
    echo ⚠️  数据库迁移遇到问题，但可以继续
    echo    如果遇到错误，请检查数据库连接配置
)

cd ..
echo.

REM ============================================
REM 第十步：启动服务
REM ============================================
echo [10/10] 启动服务...
echo.
echo ====================================
echo   🚀 正在启动服务...
echo ====================================
echo.
echo 📝 提示:
echo    - 前端地址: http://localhost:5173
echo    - 后端地址: http://localhost:8000
echo    - API 文档: http://localhost:8000/docs
echo.
echo    将打开两个新的命令行窗口:
echo    1. 后端服务窗口（不要关闭）
echo    2. 前端服务窗口（不要关闭）
echo.
echo    要停止服务: 在窗口中按 Ctrl+C 或运行 stop-services.bat
echo.
pause

REM 启动后端
echo 🔧 启动后端服务...
start "AI Writer - 后端服务 (端口 8000)" cmd /k "cd /d %CD%\backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
echo ⏳ 等待后端服务启动...
timeout /t 8 /nobreak >nul

REM 启动前端
echo 🎨 启动前端服务...
start "AI Writer - 前端服务 (端口 5173)" cmd /k "cd /d %CD% && npm run dev"

REM 等待前端启动
echo ⏳ 等待前端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo ====================================
echo   ✅ 部署完成！
echo ====================================
echo.
echo 🌐 前端地址: http://localhost:5173
echo 🔧 后端地址: http://localhost:8000
echo 📚 API 文档: http://localhost:8000/docs
echo.
echo 💡 提示:
echo    - 两个服务窗口已打开，请勿关闭
echo    - 如需停止服务，运行: stop-services.bat
echo    - 下次启动，运行: start-services.bat
echo.
echo 正在自动打开浏览器...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
echo 按任意键关闭此窗口...
pause >nul
