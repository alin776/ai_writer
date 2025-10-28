@echo off
chcp 65001 >nul
echo ====================================
echo   AI Writer 环境检查工具
echo ====================================
echo.

REM 切换到项目根目录（上一级目录）
cd /d "%~dp0.."

setlocal enabledelayedexpansion
set ERROR_COUNT=0

REM ============================================
REM 检查 Python
REM ============================================
echo [1/7] 检查 Python...
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
    echo ✅ Python 已安装: !PYTHON_VER!
) else (
    echo ❌ Python 未安装或未添加到 PATH
    echo    下载: https://www.python.org/downloads/
    set /a ERROR_COUNT+=1
)
echo.

REM ============================================
REM 检查 pip
REM ============================================
echo [2/7] 检查 pip...
pip --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ pip 可用
) else (
    echo ❌ pip 不可用
    set /a ERROR_COUNT+=1
)
echo.

REM ============================================
REM 检查 Node.js
REM ============================================
echo [3/7] 检查 Node.js...
node --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=1" %%i in ('node --version') do set NODE_VER=%%i
    echo ✅ Node.js 已安装: !NODE_VER!
) else (
    echo ❌ Node.js 未安装
    echo    下载: https://nodejs.org/
    set /a ERROR_COUNT+=1
)
echo.

REM ============================================
REM 检查 npm
REM ============================================
echo [4/7] 检查 npm...
npm --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=1" %%i in ('npm --version') do set NPM_VER=%%i
    echo ✅ npm 可用: !NPM_VER!
) else (
    echo ❌ npm 不可用
    set /a ERROR_COUNT+=1
)
echo.

REM ============================================
REM 检查 PostgreSQL
REM ============================================
echo [5/7] 检查 PostgreSQL...
psql --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=3" %%i in ('psql --version') do set PG_VER=%%i
    echo ✅ PostgreSQL 已安装: !PG_VER!

    REM 检查 PostgreSQL 服务
    sc query postgresql-x64-15 >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ PostgreSQL 服务已安装
    ) else (
        echo ⚠️  PostgreSQL 服务未找到（可能使用不同版本）
    )
) else (
    echo ❌ PostgreSQL 未安装或未添加到 PATH
    echo    下载: https://www.postgresql.org/download/windows/
    set /a ERROR_COUNT+=1
)
echo.

REM ============================================
REM 检查 Redis
REM ============================================
echo [6/7] 检查 Redis...
set REDIS_OK=0

redis-cli --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Redis CLI 已安装
    redis-cli ping >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Redis 服务运行中
        set REDIS_OK=1
    ) else (
        echo ⚠️  Redis 服务未运行
    )
)

if !REDIS_OK! EQU 0 (
    memurai-cli --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        echo ✅ Memurai CLI 已安装
        memurai-cli ping >nul 2>&1
        if %ERRORLEVEL% EQU 0 (
            echo ✅ Memurai 服务运行中
            set REDIS_OK=1
        ) else (
            echo ⚠️  Memurai 服务未运行
        )
    )
)

if !REDIS_OK! EQU 0 (
    echo ❌ Redis/Memurai 未安装或未运行
    echo    选项1: https://www.memurai.com/ (推荐)
    echo    选项2: https://github.com/tporadowski/redis/releases
    echo    选项3: WSL2 + Redis
    set /a ERROR_COUNT+=1
)
echo.

REM ============================================
REM 检查项目文件
REM ============================================
echo [7/7] 检查项目文件...

if exist "package.json" (
    echo ✅ package.json 存在
) else (
    echo ❌ package.json 不存在
    set /a ERROR_COUNT+=1
)

if exist "backend\requirements.txt" (
    echo ✅ requirements.txt 存在
) else (
    echo ❌ requirements.txt 不存在
    set /a ERROR_COUNT+=1
)

if exist ".env" (
    echo ✅ .env 文件存在
) else (
    echo ⚠️  .env 文件不存在（运行部署脚本会自动创建）
)

if exist "backend\.env" (
    echo ✅ backend\.env 文件存在
) else (
    echo ⚠️  backend\.env 文件不存在（运行部署脚本会自动创建）
)

if exist "node_modules" (
    echo ✅ 前端依赖已安装
) else (
    echo ⚠️  前端依赖未安装（运行部署脚本会自动安装）
)

if exist "backend\venv" (
    echo ✅ Python 虚拟环境存在
) else (
    echo ⚠️  Python 虚拟环境不存在（运行部署脚本会自动创建）
)

echo.
echo ====================================
echo   检查完成
echo ====================================
echo.

if !ERROR_COUNT! EQU 0 (
    echo ✅ 所有必需软件已安装！
    echo.
    echo 💡 下一步:
    echo    1. 如果还没有运行过部署，执行: 一键部署.bat
    echo    2. 如果已经部署过，执行: start-services.bat
) else (
    echo ❌ 发现 !ERROR_COUNT! 个问题
    echo.
    echo 💡 解决方案:
    echo    1. 根据上面的提示安装缺少的软件
    echo    2. 确保软件已添加到系统 PATH
    echo    3. 重新打开命令行窗口
    echo    4. 再次运行此脚本检查
)

echo.
pause
