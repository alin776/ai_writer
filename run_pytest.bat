@echo off
REM Pytest 自动化测试 - 快速启动脚本
REM 作者: Claude
REM 日期: 2025-11-08

echo.
echo ========================================
echo   Pytest 自动化测试
echo ========================================
echo.

REM 检查虚拟环境
if not exist "venv\Scripts\python.exe" (
    echo [错误] 虚拟环境不存在，请先创建虚拟环境
    pause
    exit /b 1
)

REM 检查pytest是否安装
venv\Scripts\python.exe -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo [提示] pytest未安装，正在安装测试依赖...
    echo.
    venv\Scripts\pip.exe install -r requirements-test.txt
    echo.
)

REM 选择测试模式
echo 请选择测试模式:
echo.
echo [1] 运行所有测试（默认）
echo [2] 运行Planning模式测试
echo [3] 运行React模式测试
echo [4] 运行chat()模式测试
echo [5] 生成HTML报告
echo [6] 失败重试模式（重试3次）
echo [7] 快速模式（只运行连接测试）
echo.

set /p choice="请输入选项 (1-7, 默认1): "

if "%choice%"=="" set choice=1

echo.
echo [开始测试]
echo.

if "%choice%"=="1" (
    echo 运行所有测试...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v
)

if "%choice%"=="2" (
    echo 运行Planning模式测试...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v -k "planning"
)

if "%choice%"=="3" (
    echo 运行React模式测试...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v -k "chat_stream"
)

if "%choice%"=="4" (
    echo 运行chat()模式测试...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v -k "chat_mode"
)

if "%choice%"=="5" (
    echo 运行所有测试并生成HTML报告...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v --html=report.html --self-contained-html
    echo.
    echo [完成] 报告已生成: report.html
    start report.html
)

if "%choice%"=="6" (
    echo 失败重试模式（重试3次）...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v --reruns 3
)

if "%choice%"=="7" (
    echo 快速模式（只运行连接测试）...
    venv\Scripts\pytest.exe tests\test_chatgpt_fix_pytest.py -v -k "connection or login"
)

echo.
echo ========================================
echo   测试完成
echo ========================================
echo.

pause
