@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: 颜色定义（使用 echo 模拟）
set "CHECK=✓"
set "CROSS=✗"
set "ARROW=→"

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           成本监控功能 - 全自动化测试脚本                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

:: 测试计数器
set /a total_tests=0
set /a passed_tests=0
set /a failed_tests=0

:: ============================================================================
:: 第一部分：环境检查
:: ============================================================================
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 第一部分：环境检查                                              │
echo └────────────────────────────────────────────────────────────────┘
echo.

:: 检查 1: Node.js
echo [1/10] 检查 Node.js 是否安装...
set /a total_tests+=1
node --version >nul 2>&1
if errorlevel 1 (
    echo %CROSS% Node.js 未安装
    set /a failed_tests+=1
    echo    %ARROW% 请访问 https://nodejs.org 下载安装
) else (
    for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
    echo %CHECK% Node.js 已安装: !NODE_VER!
    set /a passed_tests+=1
)
echo.

:: 检查 2: npm
echo [2/10] 检查 npm 是否安装...
set /a total_tests+=1
npm --version >nul 2>&1
if errorlevel 1 (
    echo %CROSS% npm 未安装
    set /a failed_tests+=1
) else (
    for /f "tokens=*" %%i in ('npm --version') do set NPM_VER=%%i
    echo %CHECK% npm 已安装: !NPM_VER!
    set /a passed_tests+=1
)
echo.

:: 检查 3: Python
echo [3/10] 检查 Python 是否安装...
set /a total_tests+=1
python --version >nul 2>&1
if errorlevel 1 (
    echo %CROSS% Python 未安装
    set /a failed_tests+=1
    echo    %ARROW% 请访问 https://python.org 下载安装
) else (
    for /f "tokens=*" %%i in ('python --version') do set PY_VER=%%i
    echo %CHECK% Python 已安装: !PY_VER!
    set /a passed_tests+=1
)
echo.

:: 检查 4: curl
echo [4/10] 检查 curl 是否可用...
set /a total_tests+=1
curl --version >nul 2>&1
if errorlevel 1 (
    echo %CROSS% curl 不可用
    set /a failed_tests+=1
    set HAS_CURL=0
) else (
    echo %CHECK% curl 可用
    set /a passed_tests+=1
    set HAS_CURL=1
)
echo.

:: 检查 5: node_modules
echo [5/10] 检查前端依赖是否安装...
set /a total_tests+=1
if exist "node_modules" (
    echo %CHECK% node_modules 存在
    set /a passed_tests+=1
) else (
    echo %CROSS% node_modules 不存在
    set /a failed_tests+=1
    echo    %ARROW% 请运行: npm install
)
echo.

:: 检查 6: backend 目录
echo [6/10] 检查后端目录是否存在...
set /a total_tests+=1
if exist "backend" (
    echo %CHECK% backend 目录存在
    set /a passed_tests+=1
) else (
    echo %CROSS% backend 目录不存在
    set /a failed_tests+=1
)
echo.

:: 检查 7: .env 文件
echo [7/10] 检查前端环境变量配置...
set /a total_tests+=1
if exist ".env" (
    findstr /C:"VITE_USE_MOCK" .env >nul 2>&1
    if errorlevel 1 (
        echo %CROSS% .env 缺少 VITE_USE_MOCK 配置
        set /a failed_tests+=1
        echo    %ARROW% 建议添加: VITE_USE_MOCK=false
    ) else (
        for /f "tokens=2 delims==" %%i in ('findstr /C:"VITE_USE_MOCK" .env') do set USE_MOCK=%%i
        if "!USE_MOCK!"=="false" (
            echo %CHECK% VITE_USE_MOCK=false (正确)
            set /a passed_tests+=1
        ) else (
            echo %CROSS% VITE_USE_MOCK=!USE_MOCK! (应为 false)
            set /a failed_tests+=1
        )
    )
) else (
    echo %CROSS% .env 文件不存在
    set /a failed_tests+=1
    echo    %ARROW% 请创建 .env 文件
)
echo.

:: 检查 8: 后端虚拟环境
echo [8/10] 检查后端虚拟环境...
set /a total_tests+=1
if exist "backend\venv" (
    echo %CHECK% Python 虚拟环境存在
    set /a passed_tests+=1
) else (
    echo %CROSS% Python 虚拟环境不存在
    set /a failed_tests+=1
    echo    %ARROW% 请在 backend 目录运行: python -m venv venv
)
echo.

:: 检查 9: 修改的文件
echo [9/10] 检查本次修改的文件是否存在...
set /a total_tests+=1
set /a file_count=0
set /a file_missing=0

if exist "src\utils\currency.ts" (
    set /a file_count+=1
) else (
    set /a file_missing+=1
    echo    %CROSS% src\utils\currency.ts 缺失
)

if exist "src\types\index.ts" (
    set /a file_count+=1
) else (
    set /a file_missing+=1
    echo    %CROSS% src\types\index.ts 缺失
)

if exist "src\services\DataService.ts" (
    set /a file_count+=1
) else (
    set /a file_missing+=1
    echo    %CROSS% src\services\DataService.ts 缺失
)

if exist "src\views\AdminCostView\index.tsx" (
    set /a file_count+=1
) else (
    set /a file_missing+=1
    echo    %CROSS% src\views\AdminCostView\index.tsx 缺失
)

if !file_missing! equ 0 (
    echo %CHECK% 所有必需文件都存在 (4/4)
    set /a passed_tests+=1
) else (
    echo %CROSS% 缺少 !file_missing! 个文件
    set /a failed_tests+=1
)
echo.

:: 检查 10: 代码修复验证
echo [10/10] 验证关键代码修复...
set /a total_tests+=1
findstr /C:"getOldCostMetrics" "src\services\DataService.ts" >nul 2>&1
if errorlevel 1 (
    echo %CROSS% DataService.ts 方法名冲突未修复
    set /a failed_tests+=1
) else (
    echo %CHECK% DataService.ts 方法名冲突已修复
    set /a passed_tests+=1
)
echo.

:: ============================================================================
:: 第二部分：服务状态检查
:: ============================================================================
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 第二部分：服务状态检查                                          │
echo └────────────────────────────────────────────────────────────────┘
echo.

if !HAS_CURL! equ 0 (
    echo %CROSS% 无法执行服务检查 (curl 不可用)
    echo    %ARROW% 请手动检查服务状态
    goto :summary
)

:: 检查后端服务
echo [1/3] 检查后端服务 (http://localhost:8000)...
set /a total_tests+=1
curl -s -o nul -w "%%{http_code}" http://localhost:8000/docs > temp_status.txt 2>&1
set /p BACKEND_STATUS=<temp_status.txt
del temp_status.txt >nul 2>&1

if "!BACKEND_STATUS!"=="200" (
    echo %CHECK% 后端服务运行中 (HTTP 200)
    set /a passed_tests+=1
    set BACKEND_RUNNING=1
) else (
    echo %CROSS% 后端服务未运行
    set /a failed_tests+=1
    echo    %ARROW% 请运行: cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
    set BACKEND_RUNNING=0
)
echo.

:: 检查前端服务
echo [2/3] 检查前端服务 (http://localhost:5173)...
set /a total_tests+=1
curl -s -o nul -w "%%{http_code}" http://localhost:5173 > temp_status.txt 2>&1
set /p FRONTEND_STATUS=<temp_status.txt
del temp_status.txt >nul 2>&1

if "!FRONTEND_STATUS!"=="200" (
    echo %CHECK% 前端服务运行中 (HTTP 200)
    set /a passed_tests+=1
    set FRONTEND_RUNNING=1
) else (
    echo %CROSS% 前端服务未运行
    set /a failed_tests+=1
    echo    %ARROW% 请运行: npm run dev
    set FRONTEND_RUNNING=0
)
echo.

:: 检查数据库连接（通过后端健康检查）
echo [3/3] 检查数据库连接状态...
set /a total_tests+=1
if !BACKEND_RUNNING! equ 1 (
    curl -s http://localhost:8000/api/v1/health >nul 2>&1
    if errorlevel 1 (
        echo %CROSS% 数据库连接失败或健康检查端点不可用
        set /a failed_tests+=1
    ) else (
        echo %CHECK% 数据库连接正常
        set /a passed_tests+=1
    )
) else (
    echo %CROSS% 无法检查 (后端服务未运行)
    set /a failed_tests+=1
)
echo.

:: ============================================================================
:: 第三部分：API 测试（需要 Token）
:: ============================================================================
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 第三部分：API 端点测试                                          │
echo └────────────────────────────────────────────────────────────────┘
echo.

if !BACKEND_RUNNING! equ 0 (
    echo %CROSS% 跳过 API 测试 (后端服务未运行)
    echo.
    goto :summary
)

echo [提示] API 测试需要管理员 JWT Token
echo.
echo 如何获取 Token？
echo   1. 运行 GET_TOKEN.bat 查看详细教程
echo   2. 或从浏览器 F12 → Application → Local Storage 中找到 token
echo   3. 或从 Network 请求的 Authorization 头中复制
echo.
set /p DO_API_TEST="是否进行 API 测试? (y/n): "

if /i "!DO_API_TEST!" neq "y" (
    echo.
    echo [跳过] API 测试
    echo.
    goto :summary
)

echo.
set /p JWT_TOKEN="请输入 JWT Token: "
echo.

if "!JWT_TOKEN!"=="" (
    echo %CROSS% 未提供 Token，跳过 API 测试
    echo.
    goto :summary
)

echo [1/1] 测试成本指标 API...
set /a total_tests+=1
curl -s -X GET "http://localhost:8000/api/v1/ai-logs/admin/cost-metrics" ^
     -H "Authorization: Bearer !JWT_TOKEN!" ^
     -H "Content-Type: application/json" ^
     -o api_response.json 2>&1

if errorlevel 1 (
    echo %CROSS% API 请求失败
    set /a failed_tests+=1
) else (
    findstr /C:"todayCost" api_response.json >nul 2>&1
    if errorlevel 1 (
        echo %CROSS% API 返回数据格式错误
        set /a failed_tests+=1
        echo.
        echo 响应内容:
        type api_response.json
        echo.
    ) else (
        echo %CHECK% API 返回数据正确
        set /a passed_tests+=1
        echo.
        echo 响应数据预览:
        type api_response.json | findstr /C:"todayCost" /C:"thisMonthCost" /C:"topModels"
        echo.
    )
    del api_response.json >nul 2>&1
)
echo.

:: ============================================================================
:: 测试摘要
:: ============================================================================
:summary
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                         测试摘要                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 总测试数: !total_tests!
echo 通过: !passed_tests!
echo 失败: !failed_tests!
echo.

set /a success_rate=(!passed_tests! * 100) / !total_tests!
echo 成功率: !success_rate!%%
echo.

if !failed_tests! equ 0 (
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║  ✓ 所有检查通过！系统已准备好进行测试                           ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo 下一步操作：
    echo 1. 打开浏览器访问: http://localhost:5173
    echo 2. 使用管理员账号登录
    echo 3. 访问成本监控页面: http://localhost:5173/admin/cost
    echo 4. 验证数据显示是否正确
    echo.
) else (
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║  ✗ 发现 !failed_tests! 个问题，请根据上述提示修复                       ║
    echo ╚════════════════════════════════════════════════════════════════╝
    echo.
    echo 常见问题修复：
    echo.
    echo [问题] 后端服务未运行
    echo [解决] cd backend ^&^& venv\Scripts\activate ^&^& uvicorn app.main:app --reload
    echo.
    echo [问题] 前端服务未运行
    echo [解决] npm run dev
    echo.
    echo [问题] 依赖未安装
    echo [解决] npm install
    echo.
    echo [问题] 虚拟环境不存在
    echo [解决] cd backend ^&^& python -m venv venv
    echo.
)

echo.
echo ═══════════════════════════════════════════════════════════════════
echo.
pause
