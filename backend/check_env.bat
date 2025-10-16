@echo off
chcp 65001 >nul
echo ========================================
echo    环境检查工具
echo ========================================
echo.

set ERROR_COUNT=0

:: 检查 Python
echo [检查] Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [❌] Python 未安装
    set /a ERROR_COUNT+=1
) else (
    python --version
    echo [✓] Python 已安装
)
echo.

:: 检查虚拟环境
echo [检查] 虚拟环境
if exist venv (
    echo [✓] 虚拟环境存在
) else (
    echo [❌] 虚拟环境不存在，请运行 setup.bat
    set /a ERROR_COUNT+=1
)
echo.

:: 检查 .env 文件
echo [检查] 配置文件
if exist .env (
    echo [✓] .env 文件存在
    
    :: 检查关键配置
    findstr /C:"OPENAI_API_KEY=your-openai-api-key" .env >nul
    if not errorlevel 1 (
        echo [⚠] OPENAI_API_KEY 未配置（使用默认值）
        echo     请在 .env 文件中配置有效的 API Key
    )
) else (
    echo [❌] .env 文件不存在，请运行 setup.bat
    set /a ERROR_COUNT+=1
)
echo.

:: 检查 PostgreSQL
echo [检查] PostgreSQL 数据库
psql --version >nul 2>&1
if errorlevel 1 (
    echo [❌] PostgreSQL 未安装或未配置到 PATH
    echo     下载: https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe
    set /a ERROR_COUNT+=1
) else (
    psql --version
    echo [✓] PostgreSQL 已安装
    
    :: 测试数据库连接
    if exist venv (
        call venv\Scripts\activate
        if exist test_db_temp.py (
            python test_db_temp.py >nul 2>&1
            if errorlevel 1 (
                echo [⚠] 数据库连接失败
                echo     请检查：
                echo     1. PostgreSQL 服务是否运行
                echo     2. 数据库 novelaide 是否已创建
                echo     3. .env 文件中的数据库配置
                echo     详见: docs\POSTGRESQL_SETUP.md
            ) else (
                echo [✓] 数据库连接正常
            )
        )
    )
)
echo.

:: 检查必要目录
echo [检查] 必要目录
if exist uploads (
    echo [✓] uploads 目录存在
) else (
    echo [⚠] uploads 目录不存在，将在启动时创建
    mkdir uploads
)

if exist logs (
    echo [✓] logs 目录存在
) else (
    echo [⚠] logs 目录不存在，将在启动时创建
    mkdir logs
)
echo.

:: 测试依赖包
echo [检查] Python 依赖包
if exist venv (
    call venv\Scripts\activate
    python -c "import fastapi, sqlalchemy, pydantic" 2>nul
    if errorlevel 1 (
        echo [❌] 部分依赖包未安装，请运行 setup.bat
        set /a ERROR_COUNT+=1
    ) else (
        echo [✓] 核心依赖包已安装
    )
) else (
    echo [跳过] 虚拟环境不存在
)
echo.

:: 总结
echo ========================================
if %ERROR_COUNT% EQU 0 (
    echo [✓] 环境检查通过，可以运行 quick_start.bat 启动服务
) else (
    echo [❌] 发现 %ERROR_COUNT% 个错误，请先运行 setup.bat 安装配置
)
echo ========================================
echo.
pause
