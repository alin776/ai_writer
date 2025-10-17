@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 重启 NovelAIde 后端服务
echo ========================================
echo.

REM 杀死所有 uvicorn 进程
echo [1/3] 停止现有服务...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq NovelAIde Backend*" >nul 2>&1
timeout /t 2 /nobreak >nul

REM 激活虚拟环境
echo [2/3] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 清除 Python 缓存
echo [3/3] 清除缓存并启动服务...
for /r %%i in (__pycache__) do @if exist "%%i" rd /s /q "%%i"
del /s /q *.pyc >nul 2>&1

echo.
echo ========================================
echo 启动服务（配置已重新加载）
echo ========================================
echo.
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
