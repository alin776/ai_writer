@echo off
REM ========================================
REM 新开发者数据库初始化脚本
REM ========================================

echo.
echo ========================================
echo   NovelAIde - 数据库初始化
echo ========================================
echo.

REM 步骤1：检查虚拟环境
if not exist "venv\Scripts\alembic.exe" (
    echo [错误] 虚拟环境不存在！
    echo 请先运行: python -m venv venv
    echo 然后运行: venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

REM 步骤2：检查.env文件
if not exist ".env" (
    echo [警告] .env 文件不存在！
    echo 请复制 .env.example 为 .env 并配置数据库连接
    pause
    exit /b 1
)

REM 步骤3：显示当前迁移状态
echo [步骤1] 检查当前数据库迁移版本...
echo ----------------------------------------
.\venv\Scripts\alembic current
echo.

REM 步骤4：显示迁移历史
echo [步骤2] 查看迁移历史...
echo ----------------------------------------
.\venv\Scripts\alembic history
echo.

REM 步骤5：询问是否执行迁移
set /p CONFIRM="是否执行数据库迁移？(y/n): "
if /i not "%CONFIRM%"=="y" (
    echo 已取消
    pause
    exit /b 0
)

REM 步骤6：执行迁移
echo.
echo [步骤3] 执行数据库迁移...
echo ----------------------------------------
.\venv\Scripts\alembic upgrade head

REM 步骤7：验证结果
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   ✅ 迁移成功！
    echo ========================================
    echo.
    echo [当前版本]
    .\venv\Scripts\alembic current
    echo.
    echo 数据库已准备就绪，可以启动服务器了！
    echo 启动命令: python -m uvicorn app.main:app --reload
) else (
    echo.
    echo ========================================
    echo   ❌ 迁移失败！
    echo ========================================
    echo.
    echo 请检查错误信息，常见问题：
    echo 1. 数据库连接配置错误（检查 .env 文件）
    echo 2. 表已存在（运行: alembic stamp head）
    echo 3. PostgreSQL 服务未启动
    echo.
    echo 详细帮助请查看: docs\数据库迁移指南.md
)

echo.
pause
