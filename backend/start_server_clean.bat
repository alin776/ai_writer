@echo off
chcp 65001 >nul
cls
echo.
echo ========================================
echo 启动 NovelAIde 后端服务
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [2/3] 清除 Python 缓存...
for /r %%i in (__pycache__) do @if exist "%%i" rd /s /q "%%i" 2>nul
del /s /q *.pyc >nul 2>&1

echo [3/3] 启动服务...
echo.
echo 服务地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
