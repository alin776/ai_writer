@echo off
chcp 65001 >nul
echo ========================================
echo NovelAIde 后端服务启动
echo ========================================
echo.

echo 激活虚拟环境...
call venv\Scripts\activate.bat

echo.
echo 检查环境变量...
if not exist .env (
    echo [错误] .env 文件不存在！
    echo 请复制 .env.example 并配置环境变量
    pause
    exit /b 1
)

echo.
echo ========================================
echo 启动后端服务...
echo ========================================
echo.
echo 服务地址: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
