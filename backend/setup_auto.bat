@echo off
chcp 65001 >nul
echo ========================================
echo    NovelAIde Backend 自动安装脚本
echo ========================================
echo.

:: 设置PostgreSQL路径
set "PATH=%PATH%;C:\Program Files\PostgreSQL\18\bin"

:: 检查 Python
echo [1/6] 检查 Python 环境...
python --version
echo.

:: 检查 PostgreSQL
echo [2/6] 检查 PostgreSQL 环境...
psql --version
echo.

:: 检查虚拟环境
echo [3/6] 检查虚拟环境...
if exist venv (
    echo 虚拟环境已存在
) else (
    echo 正在创建虚拟环境...
    python -m venv venv
)
echo.

:: 安装依赖
echo [4/6] 安装 Python 依赖包（可能需要几分钟）...
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [警告] 部分依赖安装失败
    pause
)
echo.

:: 检查.env文件
echo [5/6] 检查环境变量配置...
if exist .env (
    echo .env 文件已存在
) else (
    echo 正在创建 .env 文件...
    copy .env.example .env
    echo [重要] 请编辑 .env 文件配置 OPENAI_API_KEY
)
echo.

:: 测试数据库连接并运行迁移
echo [6/6] 初始化数据库...
echo.
echo 正在运行数据库迁移...
python -m alembic upgrade head
if errorlevel 1 (
    echo.
    echo [错误] 数据库迁移失败
    echo.
    echo 可能原因：
    echo 1. pgvector扩展未安装（如果看到"extension vector is not available"）
    echo 2. 数据库连接配置错误
    echo 3. 数据库未创建
    echo.
    echo 如果是pgvector问题，请先：
    echo   1. 以管理员身份运行: compile_pgvector.bat
    echo   2. 重启PostgreSQL服务
    echo   3. 连接数据库执行: CREATE EXTENSION vector;
    echo   4. 再次运行此脚本
    echo.
    pause
    exit /b 1
)
echo.

:: 创建目录
echo 创建必要的目录...
if not exist uploads mkdir uploads
if not exist logs mkdir logs
echo.

:: 完成
echo ========================================
echo    安装完成！
echo ========================================
echo.
echo 下一步：
echo 1. 编辑 .env 文件配置 OPENAI_API_KEY
echo 2. 运行 quick_start.bat 启动服务器
echo 3. 访问 http://localhost:8000/docs 查看API文档
echo.
pause
