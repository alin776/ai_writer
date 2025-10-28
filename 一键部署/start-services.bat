@echo off
chcp 65001 >nul
echo ====================================
echo   AI Writer 启动服务
echo ====================================
echo.

REM 切换到项目根目录（上一级目录）
cd /d "%~dp0.."

REM 检查环境
echo [1/3] 检查环境...

if not exist "backend\venv" (
    echo ❌ Python 虚拟环境不存在
    echo    请先运行: 一键部署.bat
    pause
    exit /b 1
)

if not exist "node_modules" (
    echo ❌ 前端依赖未安装
    echo    请先运行: 一键部署.bat
    pause
    exit /b 1
)

if not exist ".env" (
    echo ❌ 环境变量文件不存在
    echo    请先运行: 一键部署.bat
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

REM 检查端口占用
echo [2/3] 检查端口占用...

netstat -ano | findstr ":8000" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  端口 8000 已被占用
    echo    可能服务已经在运行
    echo    或者运行: stop-services.bat 停止旧服务
    echo.
)

netstat -ano | findstr ":5173" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  端口 5173 已被占用
    echo    可能服务已经在运行
    echo    或者运行: stop-services.bat 停止旧服务
    echo.
)

REM 启动服务
echo [3/3] 启动服务...
echo.
echo 💡 提示:
echo    - 前端地址: http://localhost:5173
echo    - 后端地址: http://localhost:8000
echo    - API 文档: http://localhost:8000/docs
echo.
echo    将打开两个新的命令行窗口:
echo    1. 后端服务窗口（不要关闭）
echo    2. 前端服务窗口（不要关闭）
echo.
pause

REM 启动后端
echo 🔧 启动后端服务...
start "AI Writer - 后端服务 (端口 8000)" cmd /k "cd /d %CD%\backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

REM 等待后端启动
echo ⏳ 等待后端服务启动...
timeout /t 5 /nobreak >nul

REM 启动前端
echo 🎨 启动前端服务...
start "AI Writer - 前端服务 (端口 5173)" cmd /k "cd /d %CD% && npm run dev"

echo.
echo ====================================
echo   ✅ 服务启动完成！
echo ====================================
echo.
echo 🌐 前端地址: http://localhost:5173
echo 🔧 后端地址: http://localhost:8000
echo 📚 API 文档: http://localhost:8000/docs
echo.
echo 💡 提示:
echo    - 两个服务窗口已打开，请勿关闭
echo    - 要停止服务，运行: stop-services.bat
echo    - 或在服务窗口中按 Ctrl+C
echo.

REM 等待几秒后打开浏览器
echo 正在自动打开浏览器...
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo.
pause
