@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 清除系统环境变量中的旧配置
echo ========================================
echo.

echo [1/3] 删除用户级别的 OPENAI 环境变量...
setx OPENAI_API_KEY "" >nul 2>&1
setx OPENAI_BASE_URL "" >nul 2>&1
setx OPENAI_MODEL "" >nul 2>&1

echo [2/3] 等待系统更新...
timeout /t 2 /nobreak >nul

echo [3/3] 清除当前会话的环境变量...
set OPENAI_API_KEY=
set OPENAI_BASE_URL=
set OPENAI_MODEL=

echo.
echo ========================================
echo ✅ 环境变量已清除！
echo ========================================
echo.
echo 请关闭所有终端窗口，然后重新打开并启动服务：
echo   cd backend
echo   .\restart_server.bat
echo.
pause
