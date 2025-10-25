@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════════════════╗
echo ║         如何获取管理员 JWT Token - 图文教程                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 方法一：从浏览器开发者工具获取（推荐）                          │
echo └────────────────────────────────────────────────────────────────┘
echo.
echo 步骤 1: 启动前端服务并登录
echo    → 运行: npm run dev
echo    → 打开浏览器访问: http://localhost:5173
echo    → 使用管理员账号登录
echo.
echo 步骤 2: 打开浏览器开发者工具
echo    → 按 F12 键（或右键点击页面 → 检查）
echo.
echo 步骤 3: 切换到 Application 标签页
echo    → Chrome/Edge: Application 标签
echo    → Firefox: Storage 标签
echo.
echo 步骤 4: 查找 Token
echo    → 左侧菜单找到 "Local Storage" 或 "Session Storage"
echo    → 展开 http://localhost:5173
echo    → 查找以下可能的 key：
echo       - token
echo       - authToken
echo       - jwt
echo       - accessToken
echo       - user (可能包含 token 字段)
echo.
echo 步骤 5: 复制 Token
echo    → 右侧 Value 列会显示 Token（通常很长的字符串）
echo    → 点击复制整个字符串
echo    → Token 格式通常类似: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 方法二：从 Network 请求中获取                                   │
echo └────────────────────────────────────────────────────────────────┘
echo.
echo 步骤 1: 登录后保持开发者工具打开
echo    → 按 F12 打开开发者工具
echo    → 切换到 Network（网络）标签
echo.
echo 步骤 2: 刷新页面或访问任意页面
echo    → 按 F5 刷新页面
echo    → 或访问 /admin/cost 页面
echo.
echo 步骤 3: 查找带有 Authorization 的请求
echo    → 在请求列表中选择任意 API 请求（如 cost-metrics）
echo    → 点击该请求
echo.
echo 步骤 4: 查看请求头
echo    → 右侧切换到 Headers（请求头）标签
echo    → 找到 "Request Headers" 部分
echo    → 找到 "Authorization" 字段
echo    → 格式为: Authorization: Bearer eyJhbGci...
echo    → 复制 "Bearer " 后面的所有内容（不包括 "Bearer "）
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 方法三：使用后端 API 直接登录获取（编程方式）                   │
echo └────────────────────────────────────────────────────────────────┘
echo.
echo 使用 curl 命令登录：
echo.
echo curl -X POST "http://localhost:8000/api/v1/auth/login" ^
     -H "Content-Type: application/json" ^
     -d "{\"username\":\"admin\",\"password\":\"your_password\"}"
echo.
echo 返回结果示例：
echo {
echo   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
echo   "token_type": "bearer"
echo }
echo.
echo 复制 "access_token" 的值即可
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │ 常见问题                                                        │
echo └────────────────────────────────────────────────────────────────┘
echo.
echo Q: Token 是什么样子的？
echo A: JWT Token 由三部分组成，用点号分隔：
echo    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzIi...
echo    通常很长（几百个字符）
echo.
echo Q: Token 会过期吗？
echo A: 是的，大多数 Token 有效期为 24 小时或更短
echo    如果过期需要重新登录获取新 Token
echo.
echo Q: 为什么需要管理员账号？
echo A: 成本监控 API 需要管理员权限才能访问全局统计数据
echo    普通用户只能看到自己的数据
echo.
echo Q: 找不到 Token 怎么办？
echo A: 检查项目是否使用 localStorage、sessionStorage 或 Cookie
echo    查看前端登录代码确认 Token 存储位置
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 需要我帮你获取 Token 吗？
echo.
set /p DO_LOGIN="是否尝试通过 API 登录获取 Token? (y/n): "

if /i "!DO_LOGIN!" neq "y" goto end

echo.
set /p USERNAME="请输入管理员用户名: "
set /p PASSWORD="请输入密码: "

echo.
echo 正在登录...
echo.

curl -X POST "http://localhost:8000/api/v1/auth/login" ^
     -H "Content-Type: application/json" ^
     -d "{\"username\":\"!USERNAME!\",\"password\":\"!PASSWORD!\"}" ^
     -o login_response.json 2>&1

if errorlevel 1 (
    echo ✗ 登录失败
    echo.
    echo 可能的原因：
    echo 1. 后端服务未运行
    echo 2. 用户名或密码错误
    echo 3. API 路径不正确
    echo.
) else (
    echo ✓ 登录成功
    echo.
    echo 完整响应：
    type login_response.json
    echo.
    echo.
    echo 请复制上面的 "access_token" 值
    echo.
    del login_response.json >nul 2>&1
)

:end
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 获取 Token 后，可以：
echo 1. 运行 AUTO_TEST.bat 进行 API 测试
echo 2. 运行 TEST_COST_MONITOR.bat 选项 4 测试 API
echo 3. 使用 curl 命令手动测试
echo.
pause
