@echo off
chcp 65001 >nul
echo ========================================
echo    NovelAIde Backend 快速启动
echo ========================================
echo.

:: 检查虚拟环境是否存在
if not exist venv (
    echo [错误] 虚拟环境不存在，请先运行 setup.bat 进行安装
    pause
    exit /b 1
)

:: 检查 .env 文件
if not exist .env (
    echo [错误] .env 文件不存在，请先运行 setup.bat 进行配置
    pause
    exit /b 1
)

:: 激活虚拟环境
call venv\Scripts\activate

:: 检查数据库连接
echo 正在检查数据库连接...
python test_db_temp.py 2>nul
if errorlevel 1 (
    echo [错误] 数据库连接失败！
    echo.
    echo 请检查：
    echo   1. PostgreSQL 服务是否运行？
    echo      - PostgreSQL 15: net start postgresql-x64-15
    echo      - PostgreSQL 18: net start postgresql-x64-18
    echo   2. 数据库是否已创建？
    echo      - 查看: docs\POSTGRESQL_SETUP.md
    echo   3. .env 文件中的数据库配置是否正确？
    echo.
    pause
    exit /b 1
)

:: 启动服务器
echo.
echo 正在启动服务器...
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务器
echo.
echo ========================================
echo.

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
