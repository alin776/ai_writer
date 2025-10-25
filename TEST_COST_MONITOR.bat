@echo off
chcp 65001 >nul
echo ========================================
echo 成本监控功能测试脚本
echo ========================================
echo.

echo [提示] 此脚本将帮助你测试成本监控前端对接功能
echo.

:menu
echo ========================================
echo 请选择操作：
echo ========================================
echo 1. 启动后端服务
echo 2. 启动前端服务
echo 3. 打开成本监控页面 (需先登录)
echo 4. 测试 API 端点 (curl)
echo 5. 查看环境变量配置
echo 6. 查看修改的文件列表
echo 7. 🔍 诊断：检查后端服务状态
echo 8. 🔍 诊断：检查数据库连接
echo 9. 🔍 诊断：检查是否有测试数据
echo 0. 💡 故障排查指南
echo X. 退出
echo ========================================
echo.

set /p choice="请输入选项: "

if "%choice%"=="1" goto start_backend
if "%choice%"=="2" goto start_frontend
if "%choice%"=="3" goto open_page
if "%choice%"=="4" goto test_api
if "%choice%"=="5" goto check_env
if "%choice%"=="6" goto show_files
if "%choice%"=="7" goto check_backend
if "%choice%"=="8" goto check_database
if "%choice%"=="9" goto check_data
if "%choice%"=="0" goto troubleshoot
if /i "%choice%"=="X" goto end
goto menu

:start_backend
echo.
echo ========================================
echo 正在启动后端服务...
echo ========================================
echo.
echo [提示] 后端服务将在新窗口中启动
echo [提示] 确保 PostgreSQL 数据库已启动
echo.
start "AI Writer Backend" cmd /k "cd backend && START_BACKEND.bat"
echo ✅ 后端服务启动命令已执行
echo.
pause
goto menu

:start_frontend
echo.
echo ========================================
echo 正在启动前端服务...
echo ========================================
echo.
echo [提示] 前端服务将在新窗口中启动
echo [提示] 访问地址通常为: http://localhost:5173
echo.
start "AI Writer Frontend" cmd /k "npm run dev"
echo ✅ 前端服务启动命令已执行
echo.
pause
goto menu

:open_page
echo.
echo ========================================
echo 打开成本监控页面
echo ========================================
echo.
echo [提示] 请先确保：
echo   1. 前端服务已启动
echo   2. 已登录管理员账号
echo.
echo 正在打开浏览器...
start http://localhost:5173/admin/cost
echo ✅ 浏览器已打开
echo.
pause
goto menu

:test_api
echo.
echo ========================================
echo 测试 API 端点
echo ========================================
echo.
echo [提示] 请先确保后端服务已启动
echo [提示] 你需要替换下面的 {TOKEN} 为真实的 JWT token
echo.
echo 测试命令示例：
echo.
echo curl -X GET "http://localhost:8000/api/v1/ai-logs/admin/cost-metrics" ^
     -H "Authorization: Bearer {TOKEN}" ^
     -H "Content-Type: application/json"
echo.
echo.
set /p token="请输入你的 JWT Token (或按 Enter 跳过): "
if "%token%"=="" (
    echo.
    echo [跳过] 未提供 Token
    echo.
) else (
    echo.
    echo 正在测试 API...
    curl -X GET "http://localhost:8000/api/v1/ai-logs/admin/cost-metrics" -H "Authorization: Bearer %token%" -H "Content-Type: application/json"
    echo.
    echo.
)
pause
goto menu

:check_env
echo.
echo ========================================
echo 环境变量配置检查
echo ========================================
echo.

if exist ".env" (
    echo ✅ 找到 .env 文件
    echo.
    echo 检查 VITE_USE_MOCK 配置...
    findstr "VITE_USE_MOCK" .env >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  未找到 VITE_USE_MOCK 配置
        echo [建议] 添加: VITE_USE_MOCK=false
    ) else (
        echo 当前配置:
        findstr "VITE_USE_MOCK" .env
        echo.
        echo [提示] 确保设置为 false 以使用真实 API
    )
) else (
    echo ⚠️  未找到 .env 文件
    echo.
    echo [建议] 创建 .env 文件并添加:
    echo VITE_USE_MOCK=false
    echo VITE_API_BASE_URL=http://localhost:8000/api/v1
)
echo.
pause
goto menu

:show_files
echo.
echo ========================================
echo 本次修改的文件列表
echo ========================================
echo.
echo 1. src/utils/currency.ts (新建)
echo    - 汇率转换工具函数
echo    - USD_TO_CNY_RATE = 7.19
echo.
echo 2. src/types/index.ts (已更新)
echo    - AICallLog 接口
echo    - AICallLogPaginatedResponse 接口
echo    - AICallLogStats 接口
echo    - CostMetrics 接口 ⭐核心
echo.
echo 3. src/services/DataService.ts (已更新并修复)
echo    - getMyAILogs() - 获取当前用户日志
echo    - getMyAIStats() - 获取当前用户统计
echo    - getAllAIStats() - 获取全局统计
echo    - getCostMetrics() - 获取成本指标 ⭐核心
echo    - getUserAILogs() - 获取指定用户日志
echo    - getUserAIStats() - 获取指定用户统计
echo    - getOldCostMetrics() - 旧版方法 (已废弃)
echo.
echo 4. src/views/AdminCostView/index.tsx (已重构并修复)
echo    - 对接真实 API
echo    - 加载/错误状态处理
echo    - 汇率转换显示
echo    - 修复图表数据字段
echo.
echo ========================================
echo 修复的关键问题：
echo ========================================
echo.
echo ✅ 问题1: DataService.ts 方法名冲突
echo    - 将旧版 getCostMetrics() 重命名为 getOldCostMetrics()
echo.
echo ✅ 问题2: 成本趋势图数据字段不匹配
echo    - 移除了"调用次数"线条
echo    - 简化为单 Y 轴显示成本
echo.
pause
goto menu

:check_backend
echo.
echo ========================================
echo 检查后端服务状态
echo ========================================
echo.
echo 正在检查后端服务是否运行...
echo.

curl -s http://localhost:8000/docs >nul 2>&1
if errorlevel 1 (
    echo ❌ 后端服务未运行
    echo.
    echo [原因] 无法访问 http://localhost:8000
    echo [解决] 请先使用选项 1 启动后端服务
    echo.
) else (
    echo ✅ 后端服务正在运行
    echo.
    echo API 文档地址: http://localhost:8000/docs
    echo.
)
pause
goto menu

:check_database
echo.
echo ========================================
echo 检查数据库连接
echo ========================================
echo.
echo [提示] 此检查需要后端服务已启动
echo.

curl -s http://localhost:8000/api/v1/health >nul 2>&1
if errorlevel 1 (
    echo ❌ 无法检查数据库状态
    echo.
    echo [原因] 后端服务未运行或健康检查端点不可用
    echo.
) else (
    echo ✅ 数据库连接正常
    echo.
    echo [提示] 如果后端启动时有数据库错误，请检查：
    echo   1. PostgreSQL 服务是否启动
    echo   2. backend/.env 中的数据库配置是否正确
    echo   3. 数据库是否已创建 (ai_call_logs 表)
    echo.
)
pause
goto menu

:check_data
echo.
echo ========================================
echo 检查测试数据
echo ========================================
echo.
echo [提示] 需要提供管理员 JWT Token
echo.
set /p token="请输入 JWT Token (或按 Enter 跳过): "
if "%token%"=="" (
    echo.
    echo [跳过] 未提供 Token
    echo.
    echo [手动检查方法]
    echo 1. 登录管理员账号
    echo 2. 打开浏览器开发者工具 (F12)
    echo 3. 访问 /admin/cost 页面
    echo 4. 查看 Network 面板中的 API 请求
    echo 5. 检查响应数据中是否有 todayCost、topModels 等字段
    echo.
) else (
    echo.
    echo 正在检查数据...
    echo.
    curl -s -X GET "http://localhost:8000/api/v1/ai-logs/admin/cost-metrics" -H "Authorization: Bearer %token%" -H "Content-Type: application/json" > temp_response.json 2>&1

    if errorlevel 1 (
        echo ❌ API 请求失败
        echo.
        echo [原因] 可能是 Token 无效或后端服务未运行
        echo.
    ) else (
        echo ✅ API 请求成功
        echo.
        echo 响应数据:
        type temp_response.json
        echo.
        echo.
        echo [检查要点]
        echo - 如果返回 401: Token 无效或已过期
        echo - 如果返回 403: 权限不足，需要管理员账号
        echo - 如果所有成本为 0: 数据库中没有 AI 调用日志
        echo - 如果有数据: 说明一切正常！
        echo.
        del temp_response.json >nul 2>&1
    )
)
pause
goto menu

:troubleshoot
echo.
echo ========================================
echo 💡 故障排查指南
echo ========================================
echo.
echo 【问题 1】页面显示"加载失败"或错误状态
echo ----------------------------------------
echo 检查步骤：
echo 1. 打开浏览器开发者工具 (F12)
echo 2. 切换到 Console 面板，查看是否有红色报错
echo 3. 切换到 Network 面板，找到 cost-metrics 请求
echo 4. 检查请求状态码：
echo    - 404: API 路由不存在，检查后端代码
echo    - 401: 未登录或 Token 过期，重新登录
echo    - 403: 权限不足，需要管理员账号
echo    - 500: 后端错误，查看后端日志
echo    - 失败/红色: 后端服务未启动
echo.
echo ========================================
echo 【问题 2】所有成本显示为 ¥0.00
echo ----------------------------------------
echo 可能原因：
echo 1. 数据库中没有 AI 调用日志数据
echo 2. 时间筛选问题（如：只查询今天，但今天没有调用）
echo.
echo 解决方法：
echo 1. 使用应用的 AI 功能生成一些调用记录
echo 2. 或使用后端脚本插入测试数据
echo 3. 检查数据库: SELECT COUNT(*) FROM ai_call_logs;
echo.
echo ========================================
echo 【问题 3】图表显示异常或空白
echo ----------------------------------------
echo 检查步骤：
echo 1. Console 中是否有 "Cannot read property" 错误
echo 2. Network 中检查 API 返回的数据格式
echo 3. 确认返回的字段名称：
echo    - dailyCosts: 包含 date 和 cost
echo    - topModels: 包含 modelName、totalCost、totalCalls
echo    - topUsers: 包含 userId、totalCost、totalCalls
echo.
echo ========================================
echo 【问题 4】前端服务无法启动
echo ----------------------------------------
echo 可能原因：
echo 1. node_modules 未安装
echo 2. 端口 5173 被占用
echo 3. TypeScript 编译错误
echo.
echo 解决方法：
echo 1. 运行: npm install
echo 2. 关闭占用 5173 端口的程序
echo 3. 忽略 TS 错误: 项目中有历史遗留的 TS 错误，不影响运行
echo.
echo ========================================
echo 【问题 5】后端服务无法启动
echo ----------------------------------------
echo 检查步骤：
echo 1. PostgreSQL 是否启动
echo 2. backend/.env 配置是否正确
echo 3. Python 虚拟环境是否激活
echo 4. 依赖包是否安装完整
echo.
echo 查看后端启动窗口的错误信息
echo.
echo ========================================
echo.
echo [快捷诊断] 使用选项 7、8、9 进行自动检查
echo.
pause
goto menu

:end
echo.
echo ========================================
echo 测试提示
echo ========================================
echo.
echo 完整测试流程：
echo 1. 先启动后端服务 (选项 1)
echo 2. 再启动前端服务 (选项 2)
echo 3. 在浏览器中登录管理员账号
echo 4. 访问 /admin/cost 页面 (选项 3)
echo 5. 验证数据显示是否正确
echo.
echo 验证项：
echo ✓ 今日成本/本月成本卡片显示
echo ✓ 最近7天成本趋势图渲染
echo ✓ 模型成本分布饼图显示
echo ✓ 用户成本排行 Top 5
echo ✓ 模型详细使用表格
echo ✓ 所有金额正确转换为人民币 (¥)
echo.
echo 有问题请查看:
echo - tasks/todo.md (任务清单)
echo - INFO.md (开发报告)
echo.
echo 再见！
echo.
pause
exit
