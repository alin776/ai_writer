@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   NovelAIde 环境检查工具
echo   Git Commit: ad8355ae7b04
echo ========================================
echo.

set ERROR_COUNT=0
set WARNING_COUNT=0

:: ========================================
:: 1. 检查Python
:: ========================================
echo [1/8] 检查Python环境...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do (
        echo ✅ Python已安装: %%v
    )
) else (
    echo ❌ Python未安装或未添加到PATH
    echo    下载: https://www.python.org/downloads/
    set /a ERROR_COUNT+=1
)
echo.

:: ========================================
:: 2. 检查PostgreSQL
:: ========================================
echo [2/8] 检查PostgreSQL环境...
psql --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=3" %%v in ('psql --version 2^>^&1') do (
        echo ✅ PostgreSQL已安装: %%v
    )
) else (
    echo ❌ PostgreSQL未安装或未添加到PATH
    echo    下载: https://get.enterprisedb.com/postgresql/postgresql-15.14-2-windows-x64.exe
    set /a ERROR_COUNT+=1
)
echo.

:: ========================================
:: 3. 检查Git
:: ========================================
echo [3/8] 检查Git（pgvector下载需要）...
git --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=3" %%v in ('git --version 2^>^&1') do (
        echo ✅ Git已安装: %%v
    )
) else (
    echo ⚠️  Git未安装（编译pgvector需要）
    echo    下载: https://git-scm.com/download/win
    set /a WARNING_COUNT+=1
)
echo.

:: ========================================
:: 4. 检查Visual Studio Build Tools
:: ========================================
echo [4/8] 检查Visual Studio Build Tools（编译pgvector需要）...
where nmake >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%p in ('where nmake') do (
        echo ✅ Visual Studio Build Tools已安装
        echo    路径: %%p
    )
) else (
    echo ⚠️  Visual Studio Build Tools未安装
    echo    这是编译pgvector必须的工具
    echo    下载: https://aka.ms/vs/17/release/vs_BuildTools.exe
    echo    安装时勾选: "使用C++的桌面开发"
    set /a WARNING_COUNT+=1
)
echo.

:: ========================================
:: 5. 检查虚拟环境
:: ========================================
echo [5/8] 检查Python虚拟环境...
if exist "backend\venv\Scripts\python.exe" (
    echo ✅ 虚拟环境已创建: backend\venv
) else (
    echo ⚠️  虚拟环境未创建
    echo    运行: cd backend ^&^& python -m venv venv
    set /a WARNING_COUNT+=1
)
echo.

:: ========================================
:: 6. 检查Python依赖
:: ========================================
echo [6/8] 检查Python依赖...
if exist "backend\venv\Scripts\python.exe" (
    backend\venv\Scripts\python.exe -c "import pgvector" >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ pgvector已安装
    ) else (
        echo ⚠️  pgvector未安装（向量存储需要）
        set /a WARNING_COUNT+=1
    )
    
    backend\venv\Scripts\python.exe -c "import sentence_transformers" >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ sentence-transformers已安装
    ) else (
        echo ⚠️  sentence-transformers未安装（文本嵌入需要）
        set /a WARNING_COUNT+=1
    )
    
    backend\venv\Scripts\python.exe -c "import langchain" >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ langchain已安装
    ) else (
        echo ⚠️  langchain未安装（AI编排需要）
        set /a WARNING_COUNT+=1
    )
) else (
    echo ⚠️  无法检查依赖（虚拟环境未创建）
    set /a WARNING_COUNT+=1
)
echo.

:: ========================================
:: 7. 检查.env配置
:: ========================================
echo [7/8] 检查环境配置文件...
if exist "backend\.env" (
    echo ✅ .env文件已创建
    findstr /C:"OPENAI_API_KEY" backend\.env >nul 2>&1
    if !errorlevel! equ 0 (
        echo ✅ OPENAI_API_KEY已配置
    ) else (
        echo ⚠️  OPENAI_API_KEY未配置
        set /a WARNING_COUNT+=1
    )
) else (
    echo ⚠️  .env文件不存在
    echo    复制: backend\.env.example → backend\.env
    set /a WARNING_COUNT+=1
)
echo.

:: ========================================
:: 8. 检查pgvector扩展
:: ========================================
echo [8/8] 检查PostgreSQL pgvector扩展...
echo    提示: 需要手动验证，这里提供检查命令
echo.
echo    检查命令:
echo    psql -U postgres -d novelaide -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
echo.
echo    如果未安装，参考文档:
echo    backend\安装pgvector扩展步骤.txt
echo.

:: ========================================
:: 总结
:: ========================================
echo ========================================
echo   环境检查完成
echo ========================================
echo.

if %ERROR_COUNT% gtr 0 (
    echo ❌ 发现 %ERROR_COUNT% 个严重错误，必须解决
)

if %WARNING_COUNT% gtr 0 (
    echo ⚠️  发现 %WARNING_COUNT% 个警告，建议解决
)

if %ERROR_COUNT% equ 0 (
    if %WARNING_COUNT% equ 0 (
        echo ✅ 所有检查通过！
        echo.
        echo 下一步:
        echo 1. cd backend
        echo 2. setup.bat          （一键安装）
        echo 3. 安装pgvector扩展  （参考文档）
        echo 4. 启动后端: venv\Scripts\python.exe -m uvicorn app.main:app --reload
        echo 5. 启动前端: npm run dev
    ) else (
        echo.
        echo ⚠️  可以继续，但建议先解决警告
        echo.
        echo 快速解决方案:
        if exist "backend\venv\Scripts\python.exe" (
            echo 1. cd backend
            echo 2. venv\Scripts\activate.bat
            echo 3. pip install -r requirements.txt
        ) else (
            echo 1. cd backend
            echo 2. python -m venv venv
            echo 3. venv\Scripts\activate.bat
            echo 4. pip install -r requirements.txt
        )
    )
)

echo.
echo ========================================
echo   详细文档
echo ========================================
echo 📖 项目交接文档: 项目交接文档-小说分析系统.md
echo 📖 安装指南: backend\INSTALL_README.md
echo 📖 pgvector安装: backend\安装pgvector扩展步骤.txt
echo 📖 项目主文档: NovelAIde 项目文档 v2.7.md
echo.

pause
