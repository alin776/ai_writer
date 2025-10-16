@echo off
chcp 65001 >nul
echo ========================================
echo    NovelAIde Backend 一键安装脚本
echo ========================================
echo.

:: 检查 Python 是否安装
echo [1/7] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python,请先安装 Python 3.8 或以上版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

:: 检查 PostgreSQL 是否安装
echo [2/7] 检查 PostgreSQL 环境...
psql --version >nul 2>&1
if errorlevel 1 (
    echo [警告] 未检测到 PostgreSQL
    echo.
    echo PostgreSQL 是本项目的必需数据库,请先安装.
    echo.
    echo 下载地址: https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe
    echo 或访问官网: https://www.postgresql.org/download/windows/
    echo.
    echo 安装指南请查看: docs\POSTGRESQL_SETUP.md
    echo.
    choice /c YN /m "是否已安装但未配置环境变量？"
    if errorlevel 2 (
        echo.
        echo 请先安装 PostgreSQL 再运行此脚本
        pause
        exit /b 1
    )
    if errorlevel 1 (
        echo [提示] 如果已安装，请确保 PostgreSQL 的 bin 目录在系统 PATH 中
        echo 常见路径: C:\Program Files\PostgreSQL\15\bin
        echo.
    )
) else (
    psql --version
    echo PostgreSQL 已安装
)
echo.

:: 检查虚拟环境是否存在
echo [3/7] 检查虚拟环境...
if exist venv (
    echo 虚拟环境已存在，跳过创建
) else (
    echo 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    echo 虚拟环境创建成功
)
echo.

:: 激活虚拟环境并安装依赖
echo [4/7] 安装 Python 依赖包（这可能需要几分钟）...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] 部分依赖安装失败，请检查错误信息
)
echo.

:: 配置环境变量
echo [5/7] 配置环境变量...
if exist .env (
    echo .env 文件已存在，跳过配置
) else (
    echo 正在从模板创建 .env 文件...
    copy .env.example .env
    echo [重要] 请编辑 .env 文件，配置必要的参数：
    echo   - SECRET_KEY: JWT密钥（建议修改）
    echo   - DATABASE_URL: 数据库连接（已配置使用 SQLite）
    echo   - OPENAI_API_KEY: OpenAI API密钥（必须配置）
    echo.
)
echo.

:: 检查并配置数据库
echo [6/7] 配置数据库...
echo.
echo 请确保 PostgreSQL 数据库已创建：
echo   - 数据库名: novelaide
echo   - 用户名: novelaide
echo   - 密码: novelaide_password
echo.
echo 如果还未创建，请运行以下命令（以 postgres 用户登录）：
echo   psql -U postgres -f setup_db.sql
echo.
echo 或查看详细指南: docs\POSTGRESQL_SETUP.md
echo.
choice /c YN /m "数据库是否已创建并配置好？"
if errorlevel 2 (
    echo.
    echo [提示] 请先创建数据库再继续
    echo 创建方法：
    echo   1. 打开命令行运行: psql -U postgres
    echo   2. 输入超级用户密码
    echo   3. 运行: \i setup_db.sql
    echo   4. 或查看 docs\POSTGRESQL_SETUP.md 获取详细步骤
    echo.
    pause
    goto skip_db
)

echo.
echo 正在测试数据库连接...
python test_db_temp.py >nul 2>&1
if errorlevel 1 (
    echo [警告] 数据库连接失败，请检查：
    echo   1. PostgreSQL 服务是否运行
    echo   2. 数据库和用户是否已创建
    echo   3. .env 文件中的数据库配置是否正确
    echo.
    echo 详细配置方法请查看: docs\POSTGRESQL_SETUP.md
) else (
    echo [成功] 数据库连接正常
    echo.
    echo 正在初始化数据库表...
    python -c "import asyncio; from app.core.database import init_db; asyncio.run(init_db())"
    if errorlevel 1 (
        echo [警告] 数据库表初始化失败，请查看错误信息
    ) else (
        echo [成功] 数据库表初始化完成
    )
)

:skip_db
echo.

:: 创建必要的目录
echo [7/7] 创建必要的目录...
if not exist uploads mkdir uploads
if not exist logs mkdir logs
echo 目录创建完成
echo.

:: 完成
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 确保 PostgreSQL 数据库已创建（如未创建，请查看 docs\POSTGRESQL_SETUP.md）
echo 2. 编辑 .env 文件，配置 OPENAI_API_KEY（必须）
echo 3. 运行 quick_start.bat 启动服务器
echo 4. 访问 http://localhost:8000/docs 查看 API 文档
echo.
echo 提示: 运行 check_env.bat 可以检查环境配置
echo.
pause
