# ReAct Stream 功能测试指南

**测试日期**: 2025-01-06
**功能**: ReAct流式对话
**端点**: `/api/v1/agent/chat/react-stream`

---

## 📋 测试清单概览

- [ ] 1. 代码验证（语法检查）
- [ ] 2. 启动服务
- [ ] 3. 功能开关测试
- [ ] 4. 正常流程测试
- [ ] 5. 错误场景测试
- [ ] 6. 性能测试
- [ ] 7. 前端集成测试

---

## 1️⃣ 代码验证

### Python语法检查

```bash
# 进入后端目录
cd D:\Java\ai_writer\backend

# 检查新增的文件
python -m py_compile app/core/features.py
python -m py_compile app/api/v1/agent_react_stream.py

# 如果没有输出，说明语法正确 ✅
```

**预期结果**: 无输出表示语法正确

---

### TypeScript编译检查

```bash
# 进入项目根目录
cd D:\Java\ai_writer

# 方法1: 完整编译
npm run build

# 方法2: 仅类型检查（不生成文件，更快）
npx tsc --noEmit
```

**预期结果**: 无类型错误

**可能的问题**:
- 如果提示 `Cannot find module '@/...'`，需要检查 `tsconfig.json` 的路径别名配置
- 如果提示 `AgentChatRequest not found`，需要检查 `types/agent.ts` 是否存在该类型

---

## 2️⃣ 启动服务

### 启动后端服务

```bash
cd D:\Java\ai_writer\backend

# 激活虚拟环境
.\venv\Scripts\activate

# 启动服务（开发模式）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**预期输出**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**检查点**:
- ✅ 无导入错误
- ✅ 路由注册成功
- ✅ 服务启动成功

---

### 启动前端服务

```bash
# 新开一个终端
cd D:\Java\ai_writer

# 启动前端开发服务器
npm run dev
```

**预期输出**:
```
VITE ready in xxx ms
➜  Local:   http://localhost:5173/
```

**检查点**:
- ✅ 无编译错误
- ✅ 前端服务启动成功

---

## 3️⃣ 功能开关测试

### 测试1: 功能开关关闭时

**修改配置**:
```python
# backend/app/core/features.py
class FeatureFlags:
    ENABLE_REACT_STREAM = False  # 改为False
```

**重启后端服务**

**测试**:
```bash
curl -X POST http://localhost:8000/api/v1/agent/chat/react-stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "测试"}'
```

**预期结果**:
```json
{
  "detail": "ReAct流式模式当前未启用"
}
```

**状态码**: 503 Service Unavailable

✅ **通过标准**: 返回503错误，提示功能未启用

---

### 测试2: 功能开关开启时

**恢复配置**:
```python
# backend/app/core/features.py
class FeatureFlags:
    ENABLE_REACT_STREAM = True  # 改回True
```

**重启后端服务**

**测试**: 继续后续测试

---

## 4️⃣ 正常流程测试

### 方法A: 使用Demo页面（推荐）

#### 步骤1: 访问Demo页面

需要先将Demo组件集成到路由，或者创建临时测试路由：

```tsx
// src/App.tsx 或路由配置文件
import AgentStreamDemo from './components/agent/AgentStreamDemo';

// 添加路由（示例）
{
  path: '/test/agent-stream',
  element: <AgentStreamDemo />
}
```

#### 步骤2: 访问页面

浏览器打开: `http://localhost:5173/test/agent-stream`

#### 步骤3: 测试基本对话

**输入**:
- 消息: "你好，我想写第三章"
- Work ID: 留空（可选）
- Chapter ID: 留空（可选）

**点击**: "发送消息"

**预期观察**:
1. ✅ 显示会话ID
2. ✅ 显示实时进度（"正在分析您的需求..."）
3. ✅ 如果调用工具，显示工具调用（如"读取章节"）
4. ✅ 显示生成的内容（逐步累加）
5. ✅ 最终显示完整结果
6. ✅ 显示进度历史记录

**检查点**:
- [ ] 会话ID正确生成
- [ ] 进度事件实时显示
- [ ] 工具调用可见
- [ ] 内容流式更新
- [ ] 最终结果完整
- [ ] 无JavaScript错误（F12检查控制台）

---

### 方法B: 使用curl测试（底层测试）

```bash
# 获取Token（先登录）
# 假设你已经有了token，替换下面的YOUR_TOKEN

curl -X POST http://localhost:8000/api/v1/agent/chat/react-stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "message": "你好，我想写第三章"
  }'
```

**预期输出**（SSE格式）:
```
data: {"type":"start","conversation_id":"xxx-xxx-xxx","timestamp":"2025-01-06T..."}

data: {"type":"progress","data":{"step":"intent_analysis","description":"正在分析您的需求...","timestamp":"..."}}

data: {"type":"progress","data":{"step":"thinking","description":"正在思考如何帮助您...","timestamp":"..."}}

data: {"type":"tool_call","data":{"tool":"get_chapter_by_order_tool","args":{...},"timestamp":"..."}}

data: {"type":"content","data":{"content":"根据..."}}

data: {"type":"done","data":{"response":"...","metadata":{...},"suggested_actions":[...]}}
```

**检查点**:
- [ ] 每行以 `data: ` 开头
- [ ] JSON格式正确
- [ ] 包含所有事件类型
- [ ] 最后有done事件

---

### 方法C: 使用Postman测试

#### 步骤1: 创建请求

1. 新建请求
2. 方法: POST
3. URL: `http://localhost:8000/api/v1/agent/chat/react-stream`
4. Headers:
   - `Content-Type: application/json`
   - `Authorization: Bearer YOUR_TOKEN`
5. Body (raw JSON):
```json
{
  "message": "你好，我想写第三章"
}
```

#### 步骤2: 发送请求

点击 "Send"

#### 步骤3: 观察响应

Postman会实时显示SSE事件流

**预期**: 看到逐步到达的事件

---

## 5️⃣ 错误场景测试

### 测试1: 未授权访问

```bash
curl -X POST http://localhost:8000/api/v1/agent/chat/react-stream \
  -H "Content-Type: application/json" \
  -d '{"message": "测试"}'
```

**预期结果**: 401 Unauthorized

---

### 测试2: 无效的Token

```bash
curl -X POST http://localhost:8000/api/v1/agent/chat/react-stream \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer INVALID_TOKEN" \
  -d '{"message": "测试"}'
```

**预期结果**: 401 Unauthorized

---

### 测试3: 空消息

使用Demo页面或curl发送空消息

**预期结果**: 422 Validation Error（FastAPI自动验证）

---

### 测试4: 模拟chat_stream失败

**方法**: 临时修改代码模拟异常

```python
# backend/app/api/v1/agent_react_stream.py
# 在 run_agent() 函数开头添加
async def run_agent():
    nonlocal result
    try:
        # 临时添加：模拟异常
        raise Exception("模拟的异常，用于测试")

        result = await agent_graph.chat_stream(...)
```

**测试**: 发送任意消息

**预期结果**:
```
data: {"type":"start",...}
data: {"type":"error","error":"模拟的异常，用于测试","timestamp":"..."}
```

**检查点**:
- [ ] 前端显示错误信息
- [ ] 没有崩溃
- [ ] 后端日志记录了异常

**记得**: 测试完成后删除模拟异常代码

---

### 测试5: 网络中断

**方法**: 发送请求后，在收到部分事件时强制关闭浏览器标签页

**预期**:
- 后端应该检测到连接断开
- 后端日志记录断开（可能）
- 不应该导致后端崩溃

**检查**: 查看后端日志，确认无异常

---

## 6️⃣ 性能测试

### 测试1: 长对话（进度历史限制）

**步骤**:
1. 使用Demo页面
2. 连续发送多条消息（不点击"重置"）
3. 每次对话后，检查进度历史数量

**预期**: 进度历史最多保留100条

**验证**:
```typescript
// 在浏览器控制台执行
console.log(progressHistory.length);  // 应该 <= 100
```

---

### 测试2: 并发请求

**脚本**（Python）:
```python
import asyncio
import aiohttp

async def send_request(session, i):
    url = "http://localhost:8000/api/v1/agent/chat/react-stream"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_TOKEN"
    }
    data = {"message": f"测试消息 {i}"}

    async with session.post(url, json=data, headers=headers) as resp:
        async for line in resp.content:
            if line:
                print(f"Request {i}: {line.decode()}")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, i) for i in range(5)]
        await asyncio.gather(*tasks)

asyncio.run(main())
```

**预期**:
- 所有请求都能正常处理
- 响应时间在合理范围内
- 无内存泄漏

---

### 测试3: 内存占用

**步骤**:
1. 启动后端服务
2. 记录初始内存占用
3. 发送10-20条消息
4. 检查内存占用变化

**工具**:
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep python
```

**预期**: 内存占用增长在合理范围内（不应该无限增长）

---

## 7️⃣ 前端集成测试

### 测试1: Hook状态管理

在浏览器DevTools中添加React DevTools扩展，然后：

1. 打开Demo页面
2. 打开React DevTools
3. 找到使用 `useAgentChatStream` 的组件
4. 观察状态变化

**验证状态**:
- `loading`: false → true → false
- `conversationId`: null → "xxx-xxx"
- `currentProgress`: null → {...} → null
- `progressHistory`: [] → [...items]
- `content`: "" → "逐步累加"
- `result`: null → {...}

---

### 测试2: 进度显示组件

**验证UI渲染**:
- [ ] 进度指示器正确显示
- [ ] 工具调用列表正确显示
- [ ] 时间戳格式正确
- [ ] 友好的工具名称显示（中文）
- [ ] 动画效果正常

---

### 测试3: 错误UI

**触发错误**:
1. 关闭后端服务
2. 发送消息

**预期**:
- [ ] 显示红色错误框
- [ ] 错误信息清晰
- [ ] 有关闭按钮
- [ ] loading状态正确结束

---

## 8️⃣ 日志检查

### 后端日志

**启动服务时带日志级别**:
```bash
# 设置为DEBUG级别查看详细日志
uvicorn app.main:app --reload --log-level debug
```

**关键日志**:
```
[React Stream] 开始 - User: xxx, MessageLength: xxx
[React Stream] Progress: 正在分析您的需求...
[React Stream] Tool call: get_chapter_by_order_tool
[React Stream] 完成 - User: xxx, Intent: writing, Events: 5
```

**错误日志**（如果有异常）:
```
[React Stream] run_agent failed: ...
[React Stream] Agent task error: ...
```

---

### 前端控制台

打开浏览器 F12 → Console

**正常日志**:
```
[Demo] Progress: {...}
[Demo] Tool call: {...}
[Demo] Content chunk: ...
[Demo] Complete: {...}
```

**错误日志**（如果有）:
```
[AgentApi] React Stream error: ...
[Demo] Error: ...
```

---

## 📋 测试报告模板

### 测试执行记录

| 测试项 | 状态 | 备注 |
|--------|------|------|
| Python语法检查 | ⏳ 待执行 | |
| TypeScript编译 | ⏳ 待执行 | |
| 功能开关-关闭 | ⏳ 待执行 | |
| 功能开关-开启 | ⏳ 待执行 | |
| 正常对话流程 | ⏳ 待执行 | |
| 未授权访问 | ⏳ 待执行 | |
| 空消息验证 | ⏳ 待执行 | |
| 异常处理 | ⏳ 待执行 | |
| 长对话测试 | ⏳ 待执行 | |
| 并发请求 | ⏳ 待执行 | |
| 前端集成 | ⏳ 待执行 | |

### 发现的问题

| 问题描述 | 严重程度 | 重现步骤 | 状态 |
|---------|---------|---------|------|
| （示例）进度显示不更新 | High | 1. 打开Demo 2. 发送消息 3. ... | 待修复 |

---

## 🚀 快速开始（一键测试）

如果你想快速验证基本功能，执行以下步骤：

### Step 1: 代码检查（2分钟）
```bash
cd D:\Java\ai_writer\backend
python -m py_compile app/core/features.py
python -m py_compile app/api/v1/agent_react_stream.py

cd ..
npx tsc --noEmit
```

### Step 2: 启动服务（1分钟）
```bash
# 终端1 - 后端
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload

# 终端2 - 前端
npm run dev
```

### Step 3: 简单测试（3分钟）

1. 打开浏览器: `http://localhost:5173`
2. 登录系统（如果需要）
3. 打开浏览器控制台（F12）
4. 在控制台执行：

```javascript
// 快速测试API
fetch('http://localhost:8000/api/v1/agent/chat/react-stream', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_TOKEN'  // 替换为实际token
  },
  body: JSON.stringify({
    message: '你好'
  })
}).then(resp => {
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();

  function read() {
    reader.read().then(({done, value}) => {
      if (done) {
        console.log('Stream complete!');
        return;
      }
      console.log(decoder.decode(value));
      read();
    });
  }

  read();
});
```

**预期**: 在控制台看到SSE事件流

---

## ❓ 常见问题

### Q1: 如何获取Token？

**方法1**: 从浏览器中获取
1. 登录系统
2. F12 → Application → Local Storage
3. 找到 `auth-storage`
4. 复制其中的 `token` 字段

**方法2**: 使用登录API
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"your_username","password":"your_password"}'
```

---

### Q2: SSE事件看不到？

**检查**:
1. 后端是否正常启动？
2. Token是否有效？
3. 功能开关是否开启？
4. 浏览器是否支持SSE？（现代浏览器都支持）

---

### Q3: 前端报错 "Cannot find module"？

**解决**:
1. 检查 `tsconfig.json` 的路径别名
2. 检查导入路径是否正确
3. 运行 `npm install` 确保依赖安装

---

## 📞 需要帮助？

如果测试中遇到问题：

1. **查看日志**: 后端日志 + 前端控制台
2. **检查网络**: F12 → Network → 查看请求详情
3. **查看文档**: 参考代码审查报告和修复文档

---

**测试指南版本**: v1.0
**最后更新**: 2025-01-06
**维护者**: Claude Code
