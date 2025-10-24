@echo off
chcp 65001 >nul
echo ============================================
echo 小说分析性能压测工具
echo ============================================
echo.

echo [1/3] 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ 错误：未找到Python，请先安装Python 3.11+
    pause
    exit /b 1
)

echo ✓ Python环境正常

echo.
echo [2/3] 激活虚拟环境...
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo ✓ 虚拟环境已激活
) else (
    echo ⚠ 警告：未找到虚拟环境，使用全局Python
)

echo.
echo [3/3] 开始运行压测...
echo ============================================
echo.

python tests\performance\test_novel_analysis_performance.py

echo.
echo ============================================
echo 压测完成！
echo ============================================
pause
