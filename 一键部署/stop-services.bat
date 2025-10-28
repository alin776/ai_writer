@echo off
chcp 65001 >nul
echo ====================================
echo   AI Writer 停止服务
echo ====================================
echo.

REM 切换到项目根目录（上一级目录）
cd /d "%~dp0.."

echo 正在查找并停止服务...
echo.

REM 停止后端服务（端口 8000）
echo [1/2] 停止后端服务...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000"') do (
    set PID=%%a
    if defined PID (
        echo 找到后端进程: PID !PID!
        taskkill /F /PID !PID! >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo ✅ 后端服务已停止
        ) else (
            echo ⚠️  无法停止进程 !PID!
        )
    )
)

REM 停止前端服务（端口 5173）
echo.
echo [2/2] 停止前端服务...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5173"') do (
    set PID=%%a
    if defined PID (
        echo 找到前端进程: PID !PID!
        taskkill /F /PID !PID! >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo ✅ 前端服务已停止
        ) else (
            echo ⚠️  无法停止进程 !PID!
        )
    )
)

REM 额外清理：停止所有相关的 node 和 python 进程
echo.
echo 清理相关进程...

REM 查找标题包含 "AI Writer" 的窗口并关闭
tasklist /FI "WINDOWTITLE eq AI Writer*" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo 关闭 AI Writer 窗口...
    taskkill /FI "WINDOWTITLE eq AI Writer*" /F >nul 2>&1
)

echo.
echo ====================================
echo   ✅ 服务已停止
echo ====================================
echo.

REM 验证端口是否已释放
netstat -ano | findstr ":8000" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  端口 8000 仍被占用
) else (
    echo ✅ 端口 8000 已释放
)

netstat -ano | findstr ":5173" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠️  端口 5173 仍被占用
) else (
    echo ✅ 端口 5173 已释放
)

echo.
echo 💡 提示:
echo    - 如需重新启动服务，运行: start-services.bat
echo    - 如果端口仍被占用，请手动查找进程:
echo      netstat -ano ^| findstr ":端口号"
echo      taskkill /F /PID 进程ID
echo.
pause
