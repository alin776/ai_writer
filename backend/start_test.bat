@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 启动 AI 服务测试
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [2/2] 运行测试...
echo.
python test_ai_service.py

echo.
echo ========================================
echo 测试完成
echo ========================================
pause
