@echo off
chcp 65001 >nul
echo.
echo ╔════════════════════════════════════════════════════╗
echo ║         NovelAIde AI 服务快速测试                 ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM 检查虚拟环境
if not exist "venv\Scripts\activate.bat" (
    echo ❌ 错误：虚拟环境不存在
    echo    请先运行 setup.bat 创建虚拟环境
    pause
    exit /b 1
)

echo [1/3] 激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo [2/3] 检查后端服务...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ⚠️  后端服务未启动
    echo    正在启动后端服务...
    echo.
    start "NovelAIde Backend" cmd /c "venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    echo    等待服务启动（10秒）...
    timeout /t 10 /nobreak >nul
)

echo.
echo [3/3] 运行 AI 服务测试...
echo.
python test_ai_service.py

echo.
echo ════════════════════════════════════════════════════
echo 测试完成！
echo ════════════════════════════════════════════════════
echo.
pause
